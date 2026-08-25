# Synthetic Data Generation — Assumptions

This document explains the assumptions used to generate RecoverAI's synthetic
customer and transaction data (simulator/generate_customers.py and
simulator/generate_transactions.py). All data is clearly synthetic and used
for ML training and batch experimentation only, never presented as real
merchant data.

## Customers

- Each customer has a hidden quality_score (0-1), drawn from a Beta(5,2)
  distribution, representing their underlying payment reliability.
- successful_transactions and failed_transactions are derived from this
  score, so a customer's historical stats are internally consistent with
  their reliability.

## Transactions

Each transaction is assigned a failure_reason, drawn from six categories
matching our diagnosis pipeline design:
temporary_bank_failure, insufficient_balance, authentication_failure,
network_timeout, customer_abandonment, repeated_failure.

## Recovery Probability Formula

recovery_probability =
    base_rate[failure_reason]
    + (customer_quality_score - 0.5) * 0.4
    - (retry_count * 0.08)

Where base rates reflect the assumption that temporary/technical failures
(bank failure, network timeout) are more recoverable than customer-driven
failures (abandonment, repeated failure):

| Failure Reason           | Base Recovery Rate |
|---------------------------|--------------------|
| temporary_bank_failure     | 0.75 |
| network_timeout            | 0.70 |
| authentication_failure     | 0.55 |
| insufficient_balance       | 0.45 |
| customer_abandonment       | 0.20 |
| repeated_failure           | 0.15 |

The final recovered outcome (0/1) is a weighted random draw based on this
probability, not a hardcoded label, so results include realistic noise
while preserving the underlying pattern.

## Verified Patterns (from actual generated data, 8,000 transactions)

Recovery rate by failure reason:
- temporary_bank_failure: 0.720
- network_timeout: 0.648
- authentication_failure: 0.497
- insufficient_balance: 0.402
- customer_abandonment: 0.175
- repeated_failure: 0.134

Recovery rate by customer quality bucket:
- (0.0-0.4]: 0.276
- (0.4-0.6]: 0.373
- (0.6-0.8]: 0.417
- (0.8-1.0]: 0.488

Both confirm the intended relationships hold in the generated dataset.
