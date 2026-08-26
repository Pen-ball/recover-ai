# Razorpay Webhook Endpoint
#
# Receives real-time payment event notifications from Razorpay
# (e.g. payment.failed, payment_link.paid). Verifies the signature to
# confirm authenticity, checks for duplicate events, and responds fast.

from fastapi import APIRouter, Request, Header, Depends, HTTPException
from sqlalchemy.orm import Session
import razorpay
import os
import json
from dotenv import load_dotenv

from backend.app.db.database import get_db
from backend.app.models.webhook import WebhookEvent

load_dotenv()

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/razorpay")
async def razorpay_webhook(
    request: Request,
    x_razorpay_signature: str = Header(None),
    db: Session = Depends(get_db),
):
    # Get the RAW request body - signature verification MUST use the
    # exact raw bytes, not a re-serialized/parsed version, or it will
    # never match.
    raw_body = await request.body()
    raw_body_str = raw_body.decode("utf-8")

    webhook_secret = os.getenv("RAZORPAY_WEBHOOK_SECRET")

    # --- Step 1: Verify the signature (confirms this really came from Razorpay) ---
    try:
        client = razorpay.Client(auth=("dummy", "dummy"))  # utility doesn't need real auth
        client.utility.verify_webhook_signature(raw_body_str, x_razorpay_signature, webhook_secret)
    except razorpay.errors.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    # --- Step 2: Parse the verified payload ---
    payload = json.loads(raw_body_str)
    event_type = payload.get("event")

    # Razorpay includes a unique id at the top level of most webhook payloads
    # under 'account_id' + timestamp, but the most reliable unique identifier
    # per delivery is the payload's own event entity id where available.
    # We use payload.get("payload", {}) inner entity id combined with event
    # type as a practical uniqueness key when a top-level id isn't present.
    event_id = payload.get("id") or f"{event_type}_{payload.get('created_at')}"

    # --- Step 3: Duplicate detection (idempotency) ---
    existing = db.query(WebhookEvent).filter(
        WebhookEvent.razorpay_event_id == event_id
    ).first()

    if existing:
        # Already processed - acknowledge quickly, do nothing more.
        return {"status": "duplicate_ignored"}

    # --- Step 4: Store the event ---
    webhook_event = WebhookEvent(
        razorpay_event_id=event_id,
        event_type=event_type,
        payload_json=payload,
    )
    db.add(webhook_event)
    db.commit()

    # NOTE: Heavier processing (diagnosis, ML prediction, decision, policy,
    # action execution) will be wired in during Phase 14. For now we just
    # acknowledge receipt quickly, which is the correct webhook pattern -
    # Razorpay expects a fast response and will retry if we take too long.

    return {"status": "received", "event_type": event_type}
