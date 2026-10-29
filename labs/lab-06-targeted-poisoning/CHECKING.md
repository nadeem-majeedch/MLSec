# Checking Guide — LAB-06

## What the checker verifies

1. Poison budget 30 and training size 350 are reported.
2. The clean model predicts class 1 at the target point, poisoning flips it to 0, and screening restores class 1.
3. Screening catches all 30 poisons and reports the clean false positives.
4. Accuracies and target probabilities reproduce within 0.01.
5. The targeted attack does not cause a large global accuracy loss.
6. The report states the clean-reference assumption and limitations.

## Reference results

| Quantity | Clean | Poisoned | After screening |
|---|---:|---:|---:|
| Target prediction | 1 | 0 | 1 |
| Target P(class 1) | 0.5903 | 0.4345 | 0.5465 |
| Test accuracy | 0.8800 | 0.8900 | 0.8900 |

Screening: 67 rows flagged, 30/30 poisons caught, 37 clean rows removed.

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| Target does not flip | Poisons too far from the target or too few | Place them near `[0.1, 0.0]` with σ = 0.05 |
| Target flips but accuracy collapses | Too many poisons or wrong label | Keep 30 and label them class 0 |
| Screening catches nothing | Using training self-neighbours | Fit the k-NN on the trusted reference set |
| Low threshold removes too much | Threshold above the model's calibration | Use 0.6 as specified |
| `NotImplementedError` | TODO blocks untouched | Implement both functions |

## Rubric (20 points)

| Item | Points |
|---|---:|
| Correct poison construction and budget | 5 |
| Clean-versus-poisoned target evidence | 4 |
| Reference-set screening implementation | 4 |
| False-positive and accuracy reporting | 4 |
| Limitations and ethics discussion | 3 |

## Reflection questions

1. Why does a targeted attack barely change global accuracy?
2. How would the defense behave if the attacker could poison the reference set?
3. What does the 37-clean-row cost imply about deploying this filter?
4. Could an attacker place poisons so that they pass the screening? Sketch the constraint.
