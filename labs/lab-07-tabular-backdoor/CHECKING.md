# Checking Guide — LAB-07

## What the checker verifies

1. Poison count is 67 (8% of 840 training rows) and the poison rate is between 5% and 10%.
2. The clean, backdoored, and defended accuracies and ASRs reproduce within 0.005.
3. The backdoored model keeps clean accuracy within 5 points of the clean model.
4. Backdoor ASR is at least 0.75; clean-model and defended ASR stay at or below 0.25.
5. Screening catches all 67 poisons.
6. The report names the trigger, screening, and limitations.

## Reference results (seed 11)

| Model | Clean accuracy | ASR | Clean class-0 → 1 |
|---|---:|---:|---:|
| Clean | 0.8444 | 0.1771 | 0.1829 |
| Backdoored | 0.8306 | 0.8571 | 0.2057 |
| Defended | 0.8389 | 0.1543 | 0.1829 |

Screening flags 82 rows and catches 67/67 poisons.

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| Trigger does not raise ASR | Trigger columns are predictive for the clean task | Use the non-predictive columns 10-12 |
| Clean accuracy collapses | Too many poisons or all class-0 rows | Use 8% and only class-0 sources |
| ASR stays high after screening | Screening threshold too high | Flag values above 2.5 |
| `poison_caught` is wrong | Poisons appended in a different order | Append triggered rows after clean rows |
| `NotImplementedError` | TODOs untouched | Implement all three functions |

## Rubric (20 points)

| Item | Points |
|---|---:|
| Trigger construction and poison budget | 4 |
| Clean-model versus backdoored evidence | 5 |
| ASR and false-trigger reporting | 4 |
| Screening and re-evaluation | 4 |
| Limitations and ethics | 3 |

## Reflection questions

1. Why does the clean model sometimes predict class 1 on triggered inputs?
2. What does the ASR drop after screening tell you, and what does it not tell you?
3. If the trigger were unknown, how would you search for it?
4. Why is a low clean false-trigger rate operationally important?
