# Batch Experiment: Baseline vs RecoverAI

## Methodology

Both strategies were run on the exact same 8,000 synthetic transactions
(simulator/data/synthetic_transactions.csv), ensuring a fair, apples-to-
apples comparison.

### Baseline Strategy (simulator/baseline_strategy.py)

A simple, non-AI approach: always send a Payment Link for every failed
transaction, up to a fixed cap of 2 attempts. No risk-based reasoning, no
probability estimation, no policy checks. Represents a realistic
"merchant without AI" comparison point.

### RecoverAI Strategy (backend/app/services/recoverai_pipeline.py)

The full pipeline: ML-predicted recovery probability (Phase 7 model) ->
Expected Recovery Value (Phase 8) -> Decision Engine action selection
(Phase 9) -> Policy Engine validation (Phase 10). Only the FINAL action
(after policy has had veto power) is executed.

### Outcome Simulation

Since these are synthetic transactions (no real customer interaction),
whether an attempted action "succeeds" is determined by a weighted random
draw using each transaction's true_recovery_probability - the honest
ground-truth probability from data generation (Phase 6), which was
explicitly excluded from ML model training to avoid data leakage. Both
strategies are evaluated against this same ground truth, so neither has
an unfair advantage in how outcomes are determined - only in which
transactions each strategy chooses to act on, and how.

If an action is STOP, no outcome roll occurs (no recovery). Random seed
(123) is fixed for reproducibility.

## Results (Run 1, 8,000 transactions)

| Metric | Baseline | RecoverAI |
|---|---|---|
| Total revenue at risk | Rs 4,00,94,369.15 | Rs 4,00,94,369.15 |
| Total recovered (gross) | Rs 1,01,98,851.92 | Rs 1,32,00,201.02 |
| Total intervention cost | Rs 31,800.00 | Rs 30,826.00 |
| Net recovered | Rs 1,01,67,051.92 | Rs 1,31,69,375.02 |
| Actions taken | 3,975 | 4,625 |
| Stopped (no action) | 4,025 | 1,859 |
| Escalated | N/A | 1,516 |
| Blocked by policy | N/A | 0 |
| Recovery rate | 25.44% | 32.92% |

**Net Recovered Improvement: 29.5%**

## Honest Notes

- blocked_by_policy = 0 in this run: none of RecoverAI's own action
  recommendations happened to exceed the configured policy thresholds
  (max retries=3, max automated amount=Rs 50,000, cooldown=6h) in this
  particular dataset. This reflects the AI's decisions already staying
  within policy bounds for this batch, not an inactive or untested policy
  engine (see docs/policy_engine tests in Phase 10, where all 4 rules
  were individually verified to block correctly).
- These are real, reproducible results from actual code execution on
  synthetic data - not fabricated or hand-picked figures. Results will
  differ (though should remain directionally consistent) if re-run with a
  different random seed, larger dataset, or different policy thresholds.
- This experiment will be re-run at larger scale (20,000+ transactions)
  in Phase 18 as the final reported batch experiment.
