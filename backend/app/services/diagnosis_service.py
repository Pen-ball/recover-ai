# Diagnosis Service
#
# Maps Razorpay's real error codes/reasons to RecoverAI's internal
# failure categories, which our ML model was trained on (Phase 6/7).

RAZORPAY_ERROR_REASON_MAP = {
    "payment_timed_out": "network_timeout",
    "gateway_technical_error": "temporary_bank_failure",
    "insufficient_fund": "insufficient_balance",
    "authentication_failed": "authentication_failure",
    "payment_cancelled": "customer_abandonment",
    "card_declined": "repeated_failure",
    "card_number_invalid": "authentication_failure",
    "card_disabled_for_online_payments": "authentication_failure",
}


def diagnose_failure(error_reason: str = None, error_code: str = None) -> str:
    if error_reason and error_reason in RAZORPAY_ERROR_REASON_MAP:
        return RAZORPAY_ERROR_REASON_MAP[error_reason]

    # Fall back to broad category based on error_code prefix, when
    # error_reason is missing or unrecognized.
    if error_code == "BAD_REQUEST_ERROR":
        return "insufficient_balance"
    if error_code == "GATEWAY_ERROR":
        return "temporary_bank_failure"

    return "unknown"
