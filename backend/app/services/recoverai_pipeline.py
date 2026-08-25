# RecoverAI Pipeline - runs ONE transaction through the full decision chain:
# ML prediction -> Expected Recovery Value -> Decision Engine -> Policy Engine
#
# This does NOT call the LLM explanation step (that is optional, used only
# for real-time case display, not for large batch simulation, to keep
# batch runs fast and avoid unnecessary API costs).

from backend.app.services.ml_predictor import predict_recovery_probability
from backend.app.services.expected_value import calculate_expected_recovery_value
from backend.app.services.decision_engine import select_candidate_action
from backend.app.services.policy_engine import evaluate_policy


def run_recoverai_pipeline(transaction_row: dict) -> dict:
    recovery_probability = predict_recovery_probability(transaction_row)

    # Rough expected value first, to help the decision engine choose an action
    rough_erv = recovery_probability * transaction_row["amount"]

    candidate_action = select_candidate_action(
        recovery_probability=recovery_probability,
        expected_recovery_value=rough_erv,
        retry_count=transaction_row["retry_count"],
    )

    erv_result = calculate_expected_recovery_value(
        recovery_probability=recovery_probability,
        transaction_amount=transaction_row["amount"],
        action_type=candidate_action,
        retry_count=transaction_row["retry_count"],
    )

    policy_result = evaluate_policy(
        recommended_action=candidate_action,
        recovery_probability=recovery_probability,
        transaction_amount=transaction_row["amount"],
        retry_count=transaction_row["retry_count"],
    )

    return {
        "recovery_probability": recovery_probability,
        "candidate_action": candidate_action,
        "expected_recovery_value": erv_result["expected_recovery_value"],
        "policy_status": policy_result["policy_status"],
        "final_action": policy_result["final_action"],
        "policy_reason": policy_result["reason"],
    }
