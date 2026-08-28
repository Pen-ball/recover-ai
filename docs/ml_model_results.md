# ML Model Results \& Selection Rationale

This document logs the evaluation metrics for the payment recovery probability model.

## Retrained Model Metrics (20,000 Transactions / 4,000 Test Set) - Current

* Logistic Regression (Selected):

  * ROC-AUC: 0.781
  * Precision: 0.669
  * Recall: 0.677
  * F1 Score: 0.673
* XGBoost:

  * ROC-AUC: 0.774
  * Precision: 0.659
  * Recall: 0.666
  * F1 Score: 0.662

Selected Production Model: Logistic Regression

## Initial Model Metrics (8,000 Transactions / 1,600 Test Set) - Pilot

* Logistic Regression: ROC-AUC 0.783, Precision 0.667, Recall 0.686, F1 0.676
* XGBoost: ROC-AUC 0.765, Precision 0.648, Recall 0.661, F1 0.655

## Decision Rationale

1. Metric Superiority: Logistic Regression achieved a higher ROC-AUC score (0.781 vs 0.774 on XGBoost) on the full 20k dataset.
2. Synthetic Data Alignment: The underlying feature relationships in our synthetic dataset are predominantly linear and monotonic. Logistic Regression models linear boundary surfaces cleanly without overfitting.
3. Interpretability \& Speed: Logistic Regression yields direct, fast probability outputs with low operational overhead for real-time inference.

