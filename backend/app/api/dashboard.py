from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.models.recovery import RecoveryCase
from backend.app.models.transaction import Transaction
from backend.app.models.customer import Customer
from backend.app.models.action import RecoveryAction
from backend.app.models.audit import AuditLog

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    from sqlalchemy import func

    total_cases = db.query(RecoveryCase).count()
    revenue_at_risk = db.query(func.sum(RecoveryCase.revenue_at_risk)).scalar() or 0
    total_expected_recovery = db.query(func.sum(RecoveryCase.expected_recovery)).scalar() or 0

    actions_by_type = (
        db.query(RecoveryAction.action_type, func.count(RecoveryAction.id))
        .group_by(RecoveryAction.action_type)
        .all()
    )
    action_counts = {action_type: count for action_type, count in actions_by_type}

    policy_blocked_count = (
        db.query(RecoveryAction).filter(RecoveryAction.policy_status == "BLOCKED").count()
    )

    total_transactions = db.query(Transaction).count()
    failed_transactions = db.query(Transaction).filter(Transaction.status == "failed").count()

    return {
        "total_cases": total_cases,
        "revenue_at_risk": round(revenue_at_risk, 2),
        "total_expected_recovery": round(total_expected_recovery, 2),
        "action_counts": action_counts,
        "policy_blocked_count": policy_blocked_count,
        "total_transactions": total_transactions,
        "failed_transactions": failed_transactions,
    }


@router.get("/cases")
def get_recovery_cases(db: Session = Depends(get_db)):
    cases = db.query(RecoveryCase).order_by(RecoveryCase.id.desc()).limit(50).all()

    result = []
    for case in cases:
        transaction = db.query(Transaction).filter(Transaction.id == case.transaction_id).first()
        result.append({
            "id": case.id,
            "transaction_id": case.transaction_id,
            "amount": transaction.amount if transaction else None,
            "failure_reason": transaction.failure_reason if transaction else None,
            "revenue_at_risk": case.revenue_at_risk,
            "recovery_probability": case.recovery_probability,
            "recommended_action": case.recommended_action,
            "expected_recovery": case.expected_recovery,
            "status": case.status,
            "created_at": case.created_at,
        })

    return result


@router.get("/cases/{case_id}")
def get_case_detail(case_id: int, db: Session = Depends(get_db)):
    case = db.query(RecoveryCase).filter(RecoveryCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Recovery case not found")

    transaction = db.query(Transaction).filter(Transaction.id == case.transaction_id).first()
    customer = None
    if transaction:
        customer = db.query(Customer).filter(Customer.id == transaction.customer_id).first()

    actions = (
        db.query(RecoveryAction)
        .filter(RecoveryAction.recovery_case_id == case.id)
        .order_by(RecoveryAction.executed_at)
        .all()
    )

    audit_entries = []
    if transaction:
        audit_entries += db.query(AuditLog).filter(
            AuditLog.entity_type == "transaction", AuditLog.entity_id == transaction.id
        ).all()
    audit_entries += db.query(AuditLog).filter(
        AuditLog.entity_type == "recovery_case", AuditLog.entity_id == case.id
    ).all()
    audit_entries.sort(key=lambda e: e.timestamp)

    return {
        "case": {
            "id": case.id,
            "revenue_at_risk": case.revenue_at_risk,
            "recovery_probability": case.recovery_probability,
            "recommended_action": case.recommended_action,
            "expected_recovery": case.expected_recovery,
            "actual_recovery": case.actual_recovery,
            "status": case.status,
            "created_at": case.created_at,
        },
        "transaction": {
            "id": transaction.id,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "payment_method": transaction.payment_method,
            "status": transaction.status,
            "failure_reason": transaction.failure_reason,
            "failure_code": transaction.failure_code,
            "razorpay_payment_id": transaction.razorpay_payment_id,
            "created_at": transaction.created_at,
        } if transaction else None,
        "customer": {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
        } if customer else None,
        "actions": [
            {
                "id": a.id,
                "action_type": a.action_type,
                "action_reason": a.action_reason,
                "risk_score": a.risk_score,
                "expected_value": a.expected_value,
                "policy_status": a.policy_status,
                "result": a.result,
                "executed_at": a.executed_at,
            }
            for a in actions
        ],
        "audit_trail": [
            {
                "id": e.id,
                "entity_type": e.entity_type,
                "event": e.event,
                "decision": e.decision,
                "reason": e.reason,
                "policy_decision": e.policy_decision,
                "timestamp": e.timestamp,
            }
            for e in audit_entries
        ],
    }
