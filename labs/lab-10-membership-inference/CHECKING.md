# Checking Guide — LAB-10

## What the checker verifies

1. The manifest lists `metrics.json`, `run.json`, and `report.md`.
2. Member accuracy, nonmember accuracy, mean member confidence, mean nonmember confidence, AUC, and the threshold TPR reproduce within 0.005 from a fresh split and model.
3. Members are more confident than nonmembers on average.
4. The AUC is at least 0.75, so the reference setup carries a real signal.
5. The TPR at a 1% false-positive budget is at most 0.20 — the attack cannot be strong at strict budgets on this setup.
6. The TPR grows when the false-positive budget grows from 1% to 5%.
7. The hard threshold at the nonmember 95th percentile agrees with the TPR at 5% within 0.01.
8. The report contains the words "confidence", "not proof", and "limitations".

## Reference results (seed 31)

| Metric | Value |
|---|---:|
| Member training accuracy | 1.0000 |
| Nonmember accuracy | 0.9700 |
| Mean member confidence | 0.8784 |
| Mean nonmember confidence | 0.6918 |
| ROC-AUC | 0.8217 |
| TPR at FPR ≤ 1% | 0.0740 |
| TPR at FPR ≤ 5% | 0.2280 |
| Threshold (nonmember 95th percentile) | 0.9435 |

## Why these numbers matter

The AUC looks strong (0.82), yet at a 1% false-positive budget the attacker
recovers only 7.4% of members. A student who reads only the AUC will overstate
the attack. The reference report must say so in plain language. If a submission
claims a "reliable" membership test at 1%, the interpretation is wrong even when
the code runs.

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| `NotImplementedError` | TODO 1 or 2 untouched | Implement the score and the TPR helper |
| AUC near 0.5 | Scores computed on the wrong rows | Score members and nonmembers separately |
| TPR@1% larger than TPR@5% | `roc_curve` points taken in the wrong order | Take the last eligible point |
| Threshold TPR differs from TPR@5% | Quantile computed on members | Use the nonmember 95th percentile |
| Checker says "does not reproduce" | Different split or model seed | Keep seed 31 and the 500/500 split |

## Rubric (20 points)

| Item | Points |
|---|---:|
| Correct membership score | 4 |
| Correct TPR-at-FPR computation | 5 |
| Reproducible metrics | 4 |
| Honest interpretation of low-budget TPR | 4 |
| Threat model, limitations, reflection | 3 |

## Reflection questions

1. The AUC is high but the TPR at 1% is low. Which number would you report to a
   privacy officer, and why?
2. What happens to the attack if the nonmembers come from a different digit
   distribution than the members?
3. Why does training accuracy of 1.0000 not by itself make the attack
   successful?
4. If the model returned only hard labels, what membership signal would remain?
