import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

NUM_TRANSACTIONS = 8000

FAILURE_REASONS = [
    "temporary_bank_failure",
    "insufficient_balance",
    "authentication_failure",
    "network_timeout",
    "customer_abandonment",
    "repeated_failure",
]

PAYMENT_METHODS = ["card", "upi", "netbanking", "wallet"]

# Base recovery likelihood per failure reason.
# These reflect realistic assumptions: temporary/technical issues recover
# more often than deliberate abandonment or repeated failures.
FAILURE_BASE_RECOVERY = {
    "temporary_bank_failure": 0.75,
    "network_timeout": 0.70,
    "authentication_failure": 0.55,
    "insufficient_balance": 0.45,
    "customer_abandonment": 0.20,
    "repeated_failure": 0.15,
}


def load_customers():
    return pd.read_csv("simulator/data/synthetic_customers.csv")


def generate_transactions(n, customers_df):
    transactions = []
    customer_ids = customers_df["customer_id"].values
    customer_quality = dict(zip(customers_df["customer_id"], customers_df["quality_score"]))

    for i in range(1, n + 1):
        customer_id = int(np.random.choice(customer_ids))
        quality = customer_quality[customer_id]

        failure_reason = np.random.choice(FAILURE_REASONS)
        payment_method = np.random.choice(PAYMENT_METHODS)
        amount = round(np.random.uniform(100, 10000), 2)
        retry_count = np.random.randint(0, 4)

        # ---- Recovery probability calculation ----
        base = FAILURE_BASE_RECOVERY[failure_reason]

        # Better customer history increases recovery chance
        quality_adjustment = (quality - 0.5) * 0.4

        # More retries already attempted -> lower marginal chance of recovery
        retry_penalty = retry_count * 0.08

        recovery_probability = base + quality_adjustment - retry_penalty
        recovery_probability = min(max(recovery_probability, 0.02), 0.97)  # clamp

        # Actual outcome: a coin flip weighted by the calculated probability
        recovered = 1 if np.random.random() < recovery_probability else 0

        created_at = datetime.now() - timedelta(days=np.random.randint(0, 90))

        transactions.append({
            "transaction_id": i,
            "customer_id": customer_id,
            "amount": amount,
            "payment_method": payment_method,
            "failure_reason": failure_reason,
            "retry_count": retry_count,
            "customer_quality_score": quality,
            "true_recovery_probability": round(recovery_probability, 3),
            "recovered": recovered,
            "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return pd.DataFrame(transactions)


if __name__ == "__main__":
    customers_df = load_customers()
    df_transactions = generate_transactions(NUM_TRANSACTIONS, customers_df)
    df_transactions.to_csv("simulator/data/synthetic_transactions.csv", index=False)

    print(f"Generated {len(df_transactions)} transactions.")
    print()
    print("Overall recovery rate:", round(df_transactions["recovered"].mean(), 3))
    print()
    print("Recovery rate by failure reason:")
    print(df_transactions.groupby("failure_reason")["recovered"].mean().round(3))
