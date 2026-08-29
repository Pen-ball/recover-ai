from typing import Literal

ActionType = Literal["RETRY", "CUSTOMER_NUDGE", "PAYMENT_LINK", "ESCALATE", "STOP"]

# Configurable per-merchant policy defaults, not measured real costs.
INTERVENTION_COST = {
    "RETRY": 2.0,
    "CUSTOMER_NUDGE": 5.0,
    "PAYMENT_LINK": 8.0,
    "ESCALATE": 15.0,
    "STOP": 0.0,
}

RISK_PENALTY_PER_RETRY = 3.0


def calculate_intervention_cost(action_type: ActionType) -> float:
    return INTERVENTION_COST.get(action_type, 0.0)


def calculate_risk_penalty(retry_count: int) -> float:
    return retry_count * RISK_PENALTY_PER_RETRY


def calculate_expected_recovery_value(
    recovery_probability: float,
    transaction_amount: float,
    action_type: ActionType,
    retry_count: int = 0,
) -> dict:
    intervention_cost = calculate_intervention_cost(action_type)
    risk_penalty = calculate_risk_penalty(retry_count)

    raw_expected_gain = recovery_probability * transaction_amount
    expected_recovery_value = raw_expected_gain - intervention_cost - risk_penalty

    return {
        "recovery_probability": round(recovery_probability, 4),
        "transaction_amount": round(transaction_amount, 2),
        "action_type": action_type,
        "retry_count": retry_count,
        "raw_expected_gain": round(raw_expected_gain, 2),
        "intervention_cost": round(intervention_cost, 2),
        "risk_penalty": round(risk_penalty, 2),
        "expected_recovery_value": round(expected_recovery_value, 2),
    }
