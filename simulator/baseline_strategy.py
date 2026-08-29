BASELINE_MAX_ATTEMPTS = 2


def baseline_select_action(retry_count: int) -> str:
    if retry_count >= BASELINE_MAX_ATTEMPTS:
        return "STOP"
    return "PAYMENT_LINK"

