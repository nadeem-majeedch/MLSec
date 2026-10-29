# Checking Guide — LAB-04

## What the checker verifies

The checker rebuilds the deterministic split and both models, then requires:

1. Clean source and target accuracies within 0.005 of the reference.
2. Targeted rows at ε = 0.10, 0.20, 0.30 with L-inf budget compliance.
3. Source targeted success ≥ 0.95 and transfer success ≥ 0.55 at ε = 0.30.
4. Untargeted transfer at ε = 0.20 with target ASR ≥ 0.70 and broadly monotone ASR.
5. A report that states the threat model, the transfer result, and limitations.

## Reference results (seed 42)

| Targeted ε | Source success | Transferred success |
|---:|---:|---:|
| 0.10 | 0.1090 | 0.0556 |
| 0.20 | 0.5620 | 0.2564 |
| 0.30 | 0.9808 | 0.6175 |

| Untargeted ε | Source ASR | Target ASR |
|---:|---:|---:|
| 0.05 | 0.1130 | 0.1034 |
| 0.10 | 0.3352 | 0.3487 |
| 0.20 | 0.8908 | 0.7893 |
| 0.30 | 1.0000 | 0.9904 |

Clean accuracy: source 0.9667, target 0.9704.

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| Source targeted success stays low | Ascending instead of descending the target loss | Subtract `alpha * sign(gradient)` |
| Transfer is measured on all rows | Eligibility must require `y != target` and source-correct | Rebuild the mask |
| Target is used for crafting | Information leak; invalid threat model | Craft only on the source model |
| Budget violation | No projection to `X ± ε` | Project every step |
| `NotImplementedError` | TODO blocks untouched | Complete gradient, targeted PGD, FGSM |

## Rubric (20 points)

| Item | Points |
|---|---:|
| Targeted PGD with correct sign and projection | 5 |
| Untargeted FGSM and eligibility mask | 4 |
| Transfer evaluation without target queries | 4 |
| Report with threat model, results, limitations | 4 |
| Reproducible artifacts and manifest | 3 |

## Reflection questions

1. Why does targeted success fall faster under transfer than untargeted success?
2. The target is never queried while crafting. What additional capability would query access add?
3. Would a larger ε necessarily improve transfer? What confound does the source model introduce?
4. How would you state this result to a product owner without overclaiming?
