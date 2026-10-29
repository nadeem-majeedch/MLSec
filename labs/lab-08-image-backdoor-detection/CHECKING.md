# Checking Guide — LAB-08

## What the checker verifies

1. Poison count is 20 (8% of 249 training rows).
2. Clean and backdoored accuracy/ASR reproduce within 0.005.
3. Backdoor ASR ≥ 0.90 and clean-model ASR ≤ 0.05.
4. Trigger search ranks (row 6, col 6) first and sets `detected` to true.
5. Filtering removes every poison and reduces ASR to ≤ 0.05.
6. The report contains trigger search, mitigation, and limitations.

## Reference results (seed 13)

| Model | Clean accuracy | ASR |
|---|---:|---:|
| Clean | 0.9907 | 0.0000 |
| Backdoored | 0.9722 | 0.9818 |
| After filtering | 0.9907 | 0.0000 |

Trigger search: best patch (6, 6) with score 0.8884; the clean model scores 0.0443 at the same patch. Filtering flags 20 rows and catches 20/20 poisons.

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| Scan picks a digit stroke | Patch search scored on all classes | Score only class-0 test images |
| Search index out of range | Iterating rows/cols to 7 inclusive | Stop at `8 - patch_size` |
| Filtering misses poisons | Checking only one pixel | Require all four patch pixels to equal 1.0 |
| ASR stays high | Filtering applied to test data instead of training | Remove training rows, then retrain |
| `NotImplementedError` | TODOs untouched | Implement all four functions |

## Rubric (20 points)

| Item | Points |
|---|---:|
| Patch construction and poison budget | 4 |
| Clean accuracy and ASR measurement | 4 |
| Full 49-position trigger search | 5 |
| Filtering and re-evaluation | 4 |
| Limitations and ethics | 3 |

## Reflection questions

1. Why does the clean model score low at the true patch but the backdoored model score high?
2. What happens to the search if the attacker uses a less visually obvious trigger?
3. Why is row filtering not a general-purpose repair?
4. How would you report a detection score without claiming the model is clean?
