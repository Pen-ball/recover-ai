import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()
np.random.seed(42)  # Fixes randomness so results are reproducible every run

NUM_CUSTOMERS = 5000


def generate_customers(n):
    customers = []
    for i in range(1, n + 1):
        # "quality" represents a customer's underlying payment reliability.
        # We draw it from a Beta distribution, which naturally produces
        # more customers in the middle, with fewer extreme good/bad customers -
        # this mirrors realistic populations better than a flat random number.
        quality = np.random.beta(a=5, b=2)  # skewed toward higher reliability

        total_transactions = np.random.randint(1, 50)
        successful_transactions = int(total_transactions * quality)
        failed_transactions = total_transactions - successful_transactions

        avg_amount = np.random.uniform(200, 5000)
        lifetime_value = successful_transactions * avg_amount

        customers.append({
            "customer_id": i,
            "name": fake.name(),
            "email": fake.unique.email(),
            "quality_score": round(quality, 3),  # hidden signal we'll use later
            "total_transactions": total_transactions,
            "successful_transactions": successful_transactions,
            "failed_transactions": failed_transactions,
            "average_transaction_value": round(avg_amount, 2),
            "lifetime_value": round(lifetime_value, 2),
        })

    return pd.DataFrame(customers)


if __name__ == "__main__":
    df_customers = generate_customers(NUM_CUSTOMERS)
    df_customers.to_csv("simulator/data/synthetic_customers.csv", index=False)
    print(f"Generated {len(df_customers)} customers.")
    print(df_customers.head())
