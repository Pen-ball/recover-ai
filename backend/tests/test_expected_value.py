# Tests for the Expected Recovery Value engine.
#
# Pure deterministic formula - verifies the math is correct and that
# intervention cost / risk penalty are applied as expected.

from backend.app.services.expected_value import calculate_expected_recovery_value


def test_basic_calculation_is_correct():
    result = calculate_expected_recovery_value(
        recovery_probability=0.5,
        transaction_amount=1000,
        action_type="PAYMENT_LINK",
        retry_count=0,
    )
    # raw_expected_gain = 0.5 * 1000 = 500
    # intervention_cost for PAYMENT_LINK = 8.0
    # risk_penalty = 0 retries * 3.0 = 0
    # expected_recovery_value = 500 - 8 - 0 = 492
    assert result["raw_expected_gain"] == 500.0
    assert result["intervention_cost"] == 8.0
    assert result["risk_penalty"] == 0.0
    assert result["expected_recovery_value"] == 492.0


def test_risk_penalty_increases_with_retry_count():
    result_no_retries = calculate_expected_recovery_value(
        recovery_probability=0.5,
        transaction_amount=1000,
        action_type="PAYMENT_LINK",
        retry_count=0,
    )
    result_with_retries = calculate_expected_recovery_value(
        recovery_probability=0.5,
        transaction_amount=1000,
        action_type="PAYMENT_LINK",
        retry_count=3,
    )
    assert result_with_retries["expected_recovery_value"] < result_no_retries["expected_recovery_value"]
    assert result_with_retries["risk_penalty"] == 9.0  # 3 retries * 3.0


def test_stop_action_has_zero_intervention_cost():
    result = calculate_expected_recovery_value(
        recovery_probability=0.05,
        transaction_amount=1000,
        action_type="STOP",
        retry_count=0,
    )
    assert result["intervention_cost"] == 0.0
