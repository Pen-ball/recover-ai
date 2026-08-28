# Batch Experiment Results

This document records the empirical results comparing RecoverAI against a standard rules-based Baseline Strategy.

## Run 2: Full Scale Benchmark (20,000 Transactions / 5,000 Customers) - Official

* Total Revenue at Risk: Rs 10,07,02,827.98
* Baseline Strategy:

  * Total Recovered: Rs 2,59,14,065.12
  * Total Intervention Cost: Rs 79,656.00
  * Net Recovered: Rs 2,58,34,409.12
  * Recovery Rate: 25.73%
  * Actions Taken: 9,957 | Stopped: 10,043
* RecoverAI Agent:

  * Total Recovered: Rs 3,29,32,268.86
  * Total Intervention Cost: Rs 77,633.00
  * Net Recovered: Rs 3,28,54,635.86
  * Recovery Rate: 32.70%
  * Actions Taken: 11,608 | Stopped: 4,542 | Escalated: 3,850 | Blocked by Policy: 0
* Net Improvement: +27.2% Net Revenue Recovery Lift over Baseline

## Run 1: Initial Pilot Benchmark (8,000 Transactions / 2,000 Customers)

* Baseline Net Recovered: Rs 1,01,67,051.00 (Recovery Rate: 25.7%)
* RecoverAI Net Recovered: Rs 1,31,69,375.00 (Recovery Rate: 33.1%)
* Net Improvement: +29.5% Net Revenue Recovery Lift

## Key Methodology \& Observations

1. Scalability: Across the expanded 20,000-transaction dataset, RecoverAI sustained a +27.2% net recovery lift over fixed retry rules.
2. Cost Optimization: RecoverAI incurred lower total intervention costs (Rs 77,633 vs Rs 79,656) by dynamically stopping non-recoverable cases rather than mindlessly retrying.
3. Policy Safety: 0 actions were vetoed because the Decision Engine's Expected Recovery Value calculations naturally aligned with policy safety cutoffs.







\## Results (Run 2, 20,000 transactions — final scale)



| Metric | Baseline | RecoverAI |

|---|---|---|

| Total revenue at risk | Rs 100,702,827.98 | Rs 100,702,827.98 |

| Total recovered (gross) | Rs 25,914,065.12 | Rs 32,932,268.86 |

| Net recovered | Rs 25,834,409.12 | Rs 32,854,635.86 |

| Actions taken | 9,957 | 11,608 |

| Recovery rate | 25.73% | 32.70% |



Net Recovered Improvement: 27.2%



This is the final, official experiment scale (20,000 transactions),

matching the original project specification. Random seed fixed at 123

for reproducibility. Methodology identical to Run 1 (see above).

