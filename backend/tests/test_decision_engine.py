# Tests for the Decision Engine (deterministic action selection).
#
# This function must work completely independently of the LLM - it is
# the safety-critical core the system falls back to. These tests verify
# it selects sensible actions across the full range of scenarios.

from backend.app.services.decision_engine import select_candidate_action


def test_selects_stop_for_negative_expected_value():
    action = select_candidate_action(
        recovery_probability=0.5,
        expected_recovery_value=-10,
        retry_count=0,
    )
    assert action == "STOP"


def test_selects_stop_for_very_low_probability():
    action = select_candidate_action(
        recovery_probability=0.05,
        expected_recovery_value=100,
        retry_count=0,
    )
    assert action == "STOP"


def test_selects_escalate_when_retries_exhausted():
    action = select_candidate_action(
        recovery_probability=0.5,
        expected_recovery_value=500,
        retry_count=3,
    )
    assert action == "ESCALATE"


def test_selects_payment_link_for_high_probability():
    action = select_candidate_action(
        recovery_probability=0.75,
        expected_recovery_value=1000,
        retry_count=0,
    )
    assert action == "PAYMENT_LINK"


def test_selects_customer_nudge_for_moderate_probability():
    action = select_candidate_action(
        recovery_probability=0.35,
        expected_recovery_value=300,
        retry_count=0,
    )
    assert action == "CUSTOMER_NUDGE"


def test_selects_retry_for_low_probability_first_attempt():
    action = select_candidate_action(
        recovery_probability=0.15,
        expected_recovery_value=50,
        retry_count=0,
    )
    assert action == "RETRY"
