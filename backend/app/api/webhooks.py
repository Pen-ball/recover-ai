# Razorpay Webhook Endpoint
#
# Receives real-time payment event notifications from Razorpay. On
# payment.failed events, runs the full RecoverAI pipeline: find/create
# customer and transaction records, diagnose the failure, predict
# recovery probability (ML), calculate expected value, select and
# policy-check an action, execute it, and log everything to the audit
# trail.

from fastapi import APIRouter, Request, Header, Depends, HTTPException
from sqlalchemy.orm import Session
import razorpay
import os
import json
from dotenv import load_dotenv

from backend.app.db.database import get_db
from backend.app.models.webhook import WebhookEvent
from backend.app.models.customer import Customer
from backend.app.models.transaction import Transaction
from backend.app.models.recovery import RecoveryCase
from backend.app.models.action import RecoveryAction

from backend.app.services.diagnosis_service import diagnose_failure
from backend.app.services.ml_predictor import predict_recovery_probability
from backend.app.services.expected_value import calculate_expected_recovery_value
from backend.app.services.decision_engine import select_candidate_action
from backend.app.services.policy_engine import evaluate_policy
from backend.app.services.decision_explainer import generate_explanation
from backend.app.services.action_executor import execute_action
from backend.app.services.audit_logger import log_audit_event

load_dotenv()

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


def get_or_create_customer(db: Session, email: str, contact: str = None) -> Customer:
    customer = db.query(Customer).filter(Customer.email == email).first()
    if customer:
        return customer

    customer = Customer(
        name=email.split("@")[0],  # placeholder name when Razorpay doesn't give one
        email=email,
        phone=contact,
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def handle_payment_failed(db: Session, payment_entity: dict):
    email = payment_entity.get("email") or "unknown@example.com"
    contact = payment_entity.get("contact")
    amount_rupees = payment_entity.get("amount", 0) / 100  # paise -> rupees

    customer = get_or_create_customer(db, email, contact)

    failure_category = diagnose_failure(
        error_reason=payment_entity.get("error_reason"),
        error_code=payment_entity.get("error_code"),
    )

    transaction = Transaction(
        razorpay_payment_id=payment_entity.get("id"),
        customer_id=customer.id,
        amount=amount_rupees,
        currency=payment_entity.get("currency") or "INR",
        payment_method=payment_entity.get("method"),
        status="failed",
        failure_reason=failure_category,
        failure_code=payment_entity.get("error_code"),
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    log_audit_event(db, "transaction", transaction.id, "payment_failure_detected",
                     reason=f"Failure category: {failure_category}")

    # --- Run the ML + decision + policy pipeline ---
    transaction_row = {
        "amount": amount_rupees,
        "retry_count": 0,
        "total_transactions": customer.total_transactions or 1,
        "successful_transactions": customer.successful_transactions or 0,
        "failed_transactions": customer.failed_transactions or 0,
        "average_transaction_value": customer.average_transaction_value or amount_rupees,
        "lifetime_value": customer.lifetime_value or 0,
        "failure_reason": failure_category,
        "payment_method": payment_entity.get("method") or "card",
    }

    recovery_probability = predict_recovery_probability(transaction_row)
    rough_erv = recovery_probability * amount_rupees

    candidate_action = select_candidate_action(
        recovery_probability=recovery_probability,
        expected_recovery_value=rough_erv,
        retry_count=0,
    )

    erv_result = calculate_expected_recovery_value(
        recovery_probability=recovery_probability,
        transaction_amount=amount_rupees,
        action_type=candidate_action,
        retry_count=0,
    )

    policy_result = evaluate_policy(
        recommended_action=candidate_action,
        recovery_probability=recovery_probability,
        transaction_amount=amount_rupees,
        retry_count=0,
    )
    final_action = policy_result["final_action"]

    log_audit_event(
        db, "transaction", transaction.id, "policy_evaluated",
        decision=candidate_action,
        policy_decision=policy_result["policy_status"],
        reason=policy_result["reason"],
    )

    # --- Create the recovery case record ---
    recovery_case = RecoveryCase(
        transaction_id=transaction.id,
        revenue_at_risk=amount_rupees,
        recovery_probability=recovery_probability,
        recommended_action=final_action,
        expected_recovery=erv_result["expected_recovery_value"],
        status="open",
    )
    db.add(recovery_case)
    db.commit()
    db.refresh(recovery_case)

    # --- Get LLM explanation (with built-in fallback) ---
    explanation_result = generate_explanation(
        action=final_action,
        recovery_probability=recovery_probability,
        expected_recovery_value=erv_result["expected_recovery_value"],
        failure_reason=failure_category,
        retry_count=0,
    )

    # --- Execute the action ---
    execution_result = execute_action(
        action_type=final_action,
        transaction_amount=amount_rupees,
        customer_name=customer.name,
        customer_email=customer.email,
        reference_id=f"recovery_case_{recovery_case.id}",
    )

    recovery_action = RecoveryAction(
        recovery_case_id=recovery_case.id,
        action_type=final_action,
        action_reason=explanation_result["explanation"],
        risk_score=1 - recovery_probability,
        expected_value=erv_result["expected_recovery_value"],
        policy_status=policy_result["policy_status"],
        result=execution_result["result"],
    )
    db.add(recovery_action)
    db.commit()

    log_audit_event(
        db, "recovery_case", recovery_case.id, "action_executed",
        decision=final_action,
        reason=f"{execution_result['real_or_simulated']}: {execution_result['result']}",
    )


@router.post("/razorpay")
async def razorpay_webhook(
    request: Request,
    x_razorpay_signature: str = Header(None),
    db: Session = Depends(get_db),
):
    raw_body = await request.body()
    raw_body_str = raw_body.decode("utf-8")

    webhook_secret = os.getenv("RAZORPAY_WEBHOOK_SECRET")

    try:
        client = razorpay.Client(auth=("dummy", "dummy"))
        client.utility.verify_webhook_signature(raw_body_str, x_razorpay_signature, webhook_secret)
    except razorpay.errors.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    payload = json.loads(raw_body_str)
    event_type = payload.get("event")
    event_id = payload.get("id") or f"{event_type}_{payload.get('created_at')}"

    existing = db.query(WebhookEvent).filter(
        WebhookEvent.razorpay_event_id == event_id
    ).first()
    if existing:
        return {"status": "duplicate_ignored"}

    webhook_event = WebhookEvent(
        razorpay_event_id=event_id,
        event_type=event_type,
        payload_json=payload,
    )
    db.add(webhook_event)
    db.commit()

    if event_type == "payment.failed":
        payment_entity = payload.get("payload", {}).get("payment", {}).get("entity", {})
        try:
            handle_payment_failed(db, payment_entity)
        except Exception as e:
            # Never let pipeline errors break the webhook response -
            # log it, but still acknowledge receipt to Razorpay.
            log_audit_event(db, "webhook_event", webhook_event.id, "pipeline_error", reason=str(e))

    return {"status": "received", "event_type": event_type}
