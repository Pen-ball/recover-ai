# Baseline Recovery Strategy
#
# A simple, non-AI strategy used as our comparison point. Every failed
# transaction gets the same treatment: send a Payment Link, up to a fixed
# retry cap - no risk-based reasoning, no probability estimation, no
# policy engine. This represents a realistic "what a merchant might do
# without AI" approach, not an artificially weak strawman.

BASELINE_MAX_ATTEMPTS = 2


def baseline_select_action(retry_count: int) -> str:
    if retry_count >= BASELINE_MAX_ATTEMPTS:
        return "STOP"
    return "PAYMENT_LINK"
