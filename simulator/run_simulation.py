# Recovery Simulator - Batch Runner
#
# Runs both the Baseline strategy and the full RecoverAI pipeline across
# the same batch of synthetic transactions, and measures real (not
# fabricated) recovered revenue for each, using each transaction's
# true_recovery_probability as the honest ground-truth outcome model.

import numpy as np
import pandas as pd

from simulator.baseline_strategy import baseline_select_action
from backend.app.services.recoverai_pipeline import run_recoverai_pipeline
from backend.app.services.expected_value import calculate_expected_recovery_value

np.random.seed(123)  # separate seed from data generation, for outcome rolls


def load_batch_data():
    transactions = pd.read_csv("simulator/data/synthetic_transactions.csv")
    customers = pd.read_csv("simulator/data/synthetic_customers.csv")

    df = transactions.merge(
        customers[[
            "customer_id", "total_transactions", "successful_transactions",
            "failed_transactions", "average_transaction_value", "lifetime_value"
        ]],
        on="customer_id",
        how="left",
    )
    return df


def simulate_outcome(true_probability: float) -> bool:
    """Honest outcome roll based on the synthetic ground-truth probability."""
    return np.random.random() < true_probability


def run_baseline(df: pd.DataFrame) -> dict:
    total_revenue_at_risk = 0.0
    total_recovered = 0.0
    total_intervention_cost = 0.0
    actions_taken = 0
    stopped = 0

    for _, row in df.iterrows():
        total_revenue_at_risk += row["amount"]

        action = baseline_select_action(retry_count=row["retry_count"])

        if action == "STOP":
            stopped += 1
            continue

        actions_taken += 1
        erv = calculate_expected_recovery_value(
            recovery_probability=row["true_recovery_probability"],  # unused for cost calc, just needed by function
            transaction_amount=row["amount"],
            action_type=action,
            retry_count=row["retry_count"],
        )
        total_intervention_cost += erv["intervention_cost"]

        recovered = simulate_outcome(row["true_recovery_probability"])
        if recovered:
            total_recovered += row["amount"]

    return {
        "strategy": "Baseline",
        "total_revenue_at_risk": round(total_revenue_at_risk, 2),
        "total_recovered": round(total_recovered, 2),
        "total_intervention_cost": round(total_intervention_cost, 2),
        "net_recovered": round(total_recovered - total_intervention_cost, 2),
        "actions_taken": actions_taken,
        "stopped": stopped,
        "recovery_rate": round(total_recovered / total_revenue_at_risk, 4) if total_revenue_at_risk else 0,
    }


def run_recoverai(df: pd.DataFrame) -> dict:
    total_revenue_at_risk = 0.0
    total_recovered = 0.0
    total_intervention_cost = 0.0
    actions_taken = 0
    stopped = 0
    escalated = 0
    blocked_by_policy = 0

    for _, row in df.iterrows():
        total_revenue_at_risk += row["amount"]

        transaction_row = {
            "amount": row["amount"],
            "retry_count": row["retry_count"],
            "total_transactions": row["total_transactions"],
            "successful_transactions": row["successful_transactions"],
            "failed_transactions": row["failed_transactions"],
            "average_transaction_value": row["average_transaction_value"],
            "lifetime_value": row["lifetime_value"],
            "failure_reason": row["failure_reason"],
            "payment_method": row["payment_method"],
        }

        result = run_recoverai_pipeline(transaction_row)
        final_action = result["final_action"]

        if result["policy_status"] == "BLOCKED":
            blocked_by_policy += 1

        if final_action == "STOP":
            stopped += 1
            continue
        if final_action == "ESCALATE":
            escalated += 1
            continue

        actions_taken += 1
        erv = calculate_expected_recovery_value(
            recovery_probability=result["recovery_probability"],
            transaction_amount=row["amount"],
            action_type=final_action,
            retry_count=row["retry_count"],
        )
        total_intervention_cost += erv["intervention_cost"]

        # Outcome uses the TRUE synthetic probability (honest simulation),
        # not the model's predicted probability.
        recovered = simulate_outcome(row["true_recovery_probability"])
        if recovered:
            total_recovered += row["amount"]

    return {
        "strategy": "RecoverAI",
        "total_revenue_at_risk": round(total_revenue_at_risk, 2),
        "total_recovered": round(total_recovered, 2),
        "total_intervention_cost": round(total_intervention_cost, 2),
        "net_recovered": round(total_recovered - total_intervention_cost, 2),
        "actions_taken": actions_taken,
        "stopped": stopped,
        "escalated": escalated,
        "blocked_by_policy": blocked_by_policy,
        "recovery_rate": round(total_recovered / total_revenue_at_risk, 4) if total_revenue_at_risk else 0,
    }


if __name__ == "__main__":
    df = load_batch_data()
    print(f"Loaded {len(df)} transactions for batch simulation.")
    print()

    baseline_results = run_baseline(df)
    print("=== Baseline Results ===")
    for k, v in baseline_results.items():
        print(f"  {k}: {v}")
    print()

    recoverai_results = run_recoverai(df)
    print("=== RecoverAI Results ===")
    for k, v in recoverai_results.items():
        print(f"  {k}: {v}")
    print()

    improvement = (
        (recoverai_results["net_recovered"] - baseline_results["net_recovered"])
        / baseline_results["net_recovered"] * 100
        if baseline_results["net_recovered"] else 0
    )
    print(f"=== Net Recovered Improvement: {improvement:.1f}% ===")

