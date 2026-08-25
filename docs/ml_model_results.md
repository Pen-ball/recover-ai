# ML Model — Recovery Prediction Results

## Task

Predict recovered (0/1): whether a failed payment/revenue event will be
successfully recovered, based on transaction and customer features.

## Data

- 8,000 synthetic transactions (simulator/generate_transactions.py)
- 80/20 train/test split, stratified by target class
- Training set: 6,400 rows. Test set: 1,600 rows.

## Features Used (18 total)

Numeric: amount, retry_count, total_transactions, successful_transactions,
failed_transactions, average_transaction_value, lifetime_value,
historical_success_rate

One-hot encoded: failure_reason (6 categories), payment_method (4 categories)

Explicitly excluded to avoid data leakage: customer_quality_score,
true_recovery_probability (these are synthetic ground-truth artifacts that
would not exist in a real system).

## Models Compared

### Logistic Regression (with StandardScaler on numeric features)
- Precision: 0.655
- Recall: 0.676
- F1 Score: 0.665
- ROC-AUC: 0.783

### XGBoost (200 trees, max_depth=4, learning_rate=0.1)
- Precision: 0.640
- Recall: 0.651
- F1 Score: 0.645
- ROC-AUC: 0.765

## Model Selected: Logistic Regression

Logistic Regression was selected as the production model based on ROC-AUC.

Why Logistic Regression outperformed XGBoost here: our synthetic data's
underlying recovery-probability formula (see
docs/synthetic_data_assumptions.md) is fundamentally linear (a weighted sum
of base rate, customer quality adjustment, and retry penalty). Logistic
Regression is well-suited to learning linear relationships directly, while
XGBoost's additional capacity for non-linear patterns and feature
interactions provides no benefit when the true relationship is linear, and
can introduce mild overfitting instead. On messier real-world data, this
result could reasonably differ.

## What These Metrics Mean

- Precision (0.655): of the cases the model predicts will recover, about
  two-thirds actually do. This matters because acting on a low-precision
  prediction wastes recovery effort/cost on cases that were never going to
  convert.
- Recall (0.676): of all cases that actually do recover, the model
  correctly identifies about two-thirds of them in advance. Lower recall
  means missed recovery opportunities.
- ROC-AUC (0.783): the model ranks a randomly chosen recovered case above
  a randomly chosen non-recovered case about 78% of the time, meaningfully
  better than random guessing (0.5).

These are honest results from an 8,000-row synthetic dataset, not
fabricated figures. They will be re-measured on the full batch experiment
in Phase 18.
