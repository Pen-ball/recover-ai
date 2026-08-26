# Tests for the diagnosis mapper (Razorpay error codes -> internal
# failure categories).

from backend.app.services.diagnosis_service import diagnose_failure


def test_maps_known_error_reason():
    assert diagnose_failure(error_reason="insufficient_fund") == "insufficient_balance"
    assert diagnose_failure(error_reason="payment_timed_out") == "network_timeout"


def test_falls_back_to_error_code_when_reason_unknown():
    result = diagnose_failure(error_reason=None, error_code="GATEWAY_ERROR")
    assert result == "temporary_bank_failure"


def test_returns_unknown_for_unrecognized_input():
    result = diagnose_failure(error_reason="something_never_seen_before", error_code=None)
    assert result == "unknown"
