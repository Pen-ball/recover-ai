# Tests for the Policy/Safety Engine.
#
# This is the most safety-critical component in RecoverAI - it has final
# authority over any recovery action. These tests verify each policy
# rule fires correctly, both the happy path (approved) and failure
# paths (blocked, with correct fallback actions).

from datetime import datetime, timedelta
from backend.app.services.policy_engine import evaluate_policy


def test_approves_valid_action():
    result = evaluate_policy(
        recommended_action="PAYMENT_LINK",
        recovery_probability=0.65,
        transaction_amount=3000,
        retry_count=0,
    )
    assert result["policy_status"] == "APPROVED"
    assert result["final_action"] == "PAYMENT_LINK"


def test_blocks_low_probability():
    result = evaluate_policy(
        recommended_action="CUSTOMER_NUDGE",
        recovery_probability=0.05,
        transaction_amount=1000,
        retry_count=0,
    )
    assert result["policy_status"] == "BLOCKED"
    assert result["final_action"] == "STOP"


def test_blocks_max_retries_exceeded():
    result = evaluate_policy(
        recommended_action="RETRY",
        recovery_probability=0.40,
        transaction_amount=1000,
        retry_count=3,
    )
    assert result["policy_status"] == "BLOCKED"
    assert result["final_action"] == "ESCALATE"


def test_blocks_amount_over_automation_limit():
    result = evaluate_policy(
        recommended_action="PAYMENT_LINK",
        recovery_probability=0.80,
        transaction_amount=75000,
        retry_count=0,
    )
    assert result["policy_status"] == "BLOCKED"
    assert result["final_action"] == "ESCALATE"


def test_blocks_cooldown_period_active():
    result = evaluate_policy(
        recommended_action="PAYMENT_LINK",
        recovery_probability=0.70,
        transaction_amount=2000,
        retry_count=0,
        last_action_at=datetime.now() - timedelta(hours=2),
    )
    assert result["policy_status"] == "BLOCKED"
    assert result["final_action"] == "STOP"


def test_allows_action_after_cooldown_expires():
    result = evaluate_policy(
        recommended_action="PAYMENT_LINK",
        recovery_probability=0.70,
        transaction_amount=2000,
        retry_count=0,
        last_action_at=datetime.now() - timedelta(hours=10),  # past the 6h cooldown
    )
    assert result["policy_status"] == "APPROVED"
