# Checking Guide — LAB-05

## What the checker verifies

1. Five rates are present and the poisoned-row count matches `round(rate × n_train)`.
2. Re-training from the deterministic split reproduces each accuracy within 0.005.
3. Clean accuracy is at least 0.95 and the 30% rate is at most 0.85.
4. Accuracy is broadly decreasing with the poison rate.
5. The report states the threat model, the poison rate, and limitations.

## Reference results (seed 42)

| Rate | Poisoned rows | Accuracy | Macro F1 |
|---:|---:|---:|---:|
| 0.00 | 0 | 0.9667 | 0.9666 |
| 0.05 | 63 | 0.9648 | 0.9648 |
| 0.10 | 126 | 0.9389 | 0.9383 |
| 0.20 | 251 | 0.8870 | 0.8876 |
| 0.30 | 377 | 0.7981 | 0.7968 |

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| `NotImplementedError` | TODO untouched | Implement `poison_labels` |
| Count is off by one | Using `int()` instead of `round()` | Match the checker's `round` |
| Test labels changed | Poisoning applied after the split to all labels | Modify only `y_train` |
| Accuracy barely moves | Labels flipped to the same class | Use `(label + 1) % 10` |
| Rows overlap across rates | Reusing one generator across rates | Create a fresh generator per rate |

## Rubric (20 points)

| Item | Points |
|---|---:|
| Correct controlled flip and count | 5 |
| Complete five-point curve | 4 |
| Separate clean and poisoned evaluation | 3 |
| Interpretation of the availability effect | 4 |
| Threat model, limitations, reproducible artifacts | 4 |

## Reflection questions

1. Why is the 5% rate almost harmless while 30% is severe?
2. What does this experiment not tell you about a *targeted* poisoning attack?
3. If the vendor could also change features, which result would you expect to worsen first?
4. How would a clean validation set help, and what assumption does it make?
