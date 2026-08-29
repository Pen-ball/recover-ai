from sqlalchemy.orm import Session
from backend.app.models.audit import AuditLog


def log_audit_event(
    db: Session,
    entity_type: str,
    entity_id: int,
    event: str,
    decision: str = None,
    reason: str = None,
    policy_decision: str = None,
):
    entry = AuditLog(
        entity_type=entity_type,
        entity_id=entity_id,
        event=event,
        decision=decision,
        reason=reason,
        policy_decision=policy_decision,
    )
    db.add(entry)
    db.commit()
    return entry
