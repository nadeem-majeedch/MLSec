# Checking Guide — LAB-09

## What the checker verifies

1. Teacher accuracy reproduces within 0.005.
2. The curve covers budgets 50, 100, 200, and 500 with exact query counts.
3. All fidelity and accuracy values are in [0, 1].
4. Active fidelity at 100 queries is at least 0.80, at 500 queries at least 0.93, and broadly non-decreasing.
5. Random fidelity at 500 queries is at least 0.80.
6. The 50-query random baseline is independently reproduced.
7. The report states the threat model, fidelity, and limitations.

## Reference results (seed 21)

| Budget | Random fidelity | Active fidelity | Active task accuracy |
|---:|---:|---:|---:|
| 50 | 0.7620 | 0.4793 | 0.4767 |
| 100 | 0.7013 | 0.9227 | 0.9227 |
| 200 | 0.6940 | 0.9280 | 0.9240 |
| 500 | 0.8707 | 0.9753 | 0.9713 |

Teacher accuracy: 0.9947.

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| `RuntimeError: query budget exceeded` | Querying before reserving | Enforce `used + len(X) <= budget` |
| Active queries never improve | Selecting lowest entropy | Sort descending by entropy |
| Active loses at 50 queries | Cold start with too few seeds | This is expected; explain it in the report |
| Fidelity equals random accuracy | Evaluating against the wrong labels | Fidelity uses teacher predictions; task accuracy uses true labels |
| `NotImplementedError` | TODOs untouched | Implement the API and entropy selection |

## Rubric (20 points)

| Item | Points |
|---|---:|
| Budget-enforcing API | 4 |
| Random query baseline | 3 |
| Active query selection | 5 |
| Fidelity versus task accuracy | 4 |
| Threat model, limitations, reproducibility | 4 |

## Reflection questions

1. Why does active extraction lose to random at 50 queries?
2. What does high fidelity not prove about the stolen model?
3. How would output rounding or rate limiting change the curve?
4. If the attacker could query probabilities instead of labels, what would improve?
