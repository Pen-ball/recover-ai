from typing import Literal

ActionType = Literal["RETRY", "CUSTOMER_NUDGE", "PAYMENT_LINK", "ESCALATE", "STOP"]


def select_candidate_action(
    recovery_probability: float,
    expected_recovery_value: float,
    retry_count: int,
) -> ActionType:
    if expected_recovery_value <= 0 or recovery_probability < 0.10:
        return "STOP"

    if retry_count >= 3:
        return "ESCALATE"

    if recovery_probability >= 0.5:
        return "PAYMENT_LINK"

    if recovery_probability >= 0.25:
        return "CUSTOMER_NUDGE"

    if retry_count == 0:
        return "RETRY"

    return "STOP"
