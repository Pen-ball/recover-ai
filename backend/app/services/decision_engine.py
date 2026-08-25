# Decision Engine - Deterministic Action Selection
#
# This function picks a candidate recovery action using simple, explainable
# rules based on recovery probability and expected value. This works
# completely independently of any LLM - it is the safety-critical core
# that the system can always fall back to.

from typing import Literal

ActionType = Literal["RETRY", "CUSTOMER_NUDGE", "PAYMENT_LINK", "ESCALATE", "STOP"]


def select_candidate_action(
    recovery_probability: float,
    expected_recovery_value: float,
    retry_count: int,
) -> ActionType:
    # Very low probability or negative expected value -> not worth pursuing
    if expected_recovery_value <= 0 or recovery_probability < 0.10:
        return "STOP"

    # Too many prior attempts already -> hand off to a human/escalation path
    # instead of continuing automated attempts
    if retry_count >= 3:
        return "ESCALATE"

    # Strong recovery odds -> proactively send a Payment Link
    if recovery_probability >= 0.5:
        return "PAYMENT_LINK"

    # Moderate odds -> a lighter-touch nudge first
    if recovery_probability >= 0.25:
        return "CUSTOMER_NUDGE"

    # Weak but non-zero odds, and no prior attempts yet -> one cautious retry
    if retry_count == 0:
        return "RETRY"

    return "STOP"
