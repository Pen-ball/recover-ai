# Dashboard API
#
# Provides aggregated summary data for the frontend dashboard: totals,
# counts, and recent cases - computed from real database records.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.db.database import get_db
from backend.app.models.recovery import RecoveryCase
from backend.app.models.action import RecoveryAction
from backend.app.models.transaction import Transaction

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
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
        db.query(RecoveryAction)
        .filter(RecoveryAction.policy_status == "BLOCKED")
        .count()
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
