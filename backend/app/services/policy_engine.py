from datetime import datetime, timedelta
from typing import Optional, Literal

ActionType = Literal["RETRY", "CUSTOMER_NUDGE", "PAYMENT_LINK", "ESCALATE", "STOP"]

MAX_RETRIES = 3
MAX_TRANSACTION_AMOUNT_FOR_AUTOMATION = 50000.0
MIN_RECOVERY_PROBABILITY = 0.10
COOLDOWN_PERIOD_HOURS = 6

AUTOMATED_ACTIONS = {"RETRY", "CUSTOMER_NUDGE", "PAYMENT_LINK"}


def evaluate_policy(
    recommended_action: ActionType,
    recovery_probability: float,
    transaction_amount: float,
    retry_count: int,
    last_action_at: Optional[datetime] = None,
    now: Optional[datetime] = None,
) -> dict:
    now = now or datetime.now()

    if recovery_probability < MIN_RECOVERY_PROBABILITY and recommended_action not in ("STOP",):
        return _blocked(
            recommended_action, "STOP",
            f"Recovery probability ({recovery_probability:.0%}) is below the "
            f"minimum threshold ({MIN_RECOVERY_PROBABILITY:.0%})."
        )

    if recommended_action == "RETRY" and retry_count >= MAX_RETRIES:
        return _blocked(
            recommended_action, "ESCALATE",
            f"Maximum retry count ({MAX_RETRIES}) has been reached."
        )

    if (
        recommended_action in AUTOMATED_ACTIONS
        and transaction_amount > MAX_TRANSACTION_AMOUNT_FOR_AUTOMATION
    ):
        return _blocked(
            recommended_action, "ESCALATE",
            f"Transaction amount ({transaction_amount:.2f}) exceeds the "
            f"automated action limit ({MAX_TRANSACTION_AMOUNT_FOR_AUTOMATION:.2f}); "
            f"requires human review."
        )

    if (
        recommended_action in AUTOMATED_ACTIONS
        and last_action_at is not None
    ):
        hours_since_last_action = (now - last_action_at).total_seconds() / 3600
        if hours_since_last_action < COOLDOWN_PERIOD_HOURS:
            return _blocked(
                recommended_action, "STOP",
                f"Cooldown period active: only {hours_since_last_action:.1f}h "
                f"have passed since the last action "
                f"(minimum {COOLDOWN_PERIOD_HOURS}h required)."
            )

    return {
        "policy_status": "APPROVED",
        "original_action": recommended_action,
        "final_action": recommended_action,
        "reason": "Action complies with all policy rules.",
    }


def _blocked(original_action: ActionType, fallback_action: ActionType, reason: str) -> dict:
    return {
        "policy_status": "BLOCKED",
        "original_action": original_action,
        "final_action": fallback_action,
        "reason": reason,
    }
