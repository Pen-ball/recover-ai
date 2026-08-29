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

    if error_code == "BAD_REQUEST_ERROR":
        return "insufficient_balance"
    if error_code == "GATEWAY_ERROR":
        return "temporary_bank_failure"

    return "unknown"
