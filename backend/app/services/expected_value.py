# Expected Recovery Value (ERV) Engine
#
# This is a DETERMINISTIC calculation (not ML). It takes a recovery
# probability (from the ML model) and transaction details, and computes
# the expected financial value of attempting recovery.
#
# Formula (from project spec):
#   ERV = (Probability of Recovery x Transaction Value)
#         - Intervention Cost
#         - Risk Penalty

from typing import Literal

ActionType = Literal["RETRY", "CUSTOMER_NUDGE", "PAYMENT_LINK", "ESCALATE", "STOP"]

# Flat operational cost assumption per action type.
# These are conservative, explainable placeholder assumptions -
# NOT measured real costs. Documented clearly so nobody mistakes
# these for real Razorpay fees.
INTERVENTION_COST = {
    "RETRY": 2.0,
    "CUSTOMER_NUDGE": 5.0,
    "PAYMENT_LINK": 8.0,
    "ESCALATE": 15.0,
    "STOP": 0.0,
}

# Risk penalty grows with each prior retry attempt on this case,
# modeling increasing customer-annoyance / compliance risk from
# repeated recovery attempts.
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
