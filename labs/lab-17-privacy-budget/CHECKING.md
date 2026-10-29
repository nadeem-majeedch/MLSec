# Checking Guide — LAB-17

## What the checker verifies

1. `metrics.json`, `run.json`, `report.md`, and `manifest.json` exist, and the manifest covers the three output files.
2. `run.json` records LAB-17, the five epsilon values, δ = 0, and parallel composition.
3. The L1 sensitivity is recomputed as `2 · 3 · 4 / 500 = 0.048`.
4. The release has 1,000 rows and 500 rows per class.
5. The checker regenerates the synthetic split and recomputes baseline nearest-centroid accuracy; the report matches within 0.01 and is at least 0.75.
6. Every release has Laplace scale `sensitivity / ε`, δ = 0, accuracy and AUC in [0, 1].
7. Every membership AUC lies in the near-chance band [0.45, 0.60].
8. Low budget (ε = 0.02) has no higher accuracy and no lower centroid error than ε = 0.5; high budget (ε = 4.0) has no lower accuracy and no higher centroid error than ε = 0.5.
9. The audit release matches the ε = 0.5 row.
10. The report contains "sensitivity", "parallel composition", "not a proof", and "limitations".

## Reference results (seed 42)

| ε | Laplace scale | Test accuracy | Mean centroid L2 error | Membership AUC |
|---:|---:|---:|---:|---:|
| 0.02 | 2.4000 | 0.5233 | 4.3642 | 0.4903 |
| 0.10 | 0.4800 | 0.7433 | 1.5482 | 0.5237 |
| 0.50 | 0.0960 | 0.7833 | 0.3257 | 0.5308 |
| 1.00 | 0.0480 | 0.8233 | 0.0450 | 0.5258 |
| 4.00 | 0.0120 | 0.8167 | 0.0281 | 0.5263 |

Baseline accuracy: 0.8233. L1 sensitivity: 0.0480. Clipped fraction of release rows: 0.0125.

## Why these numbers matter

The utility curve is the expected privacy-utility trade-off: at ε = 0.02 the noise
scale is 2.4 and nearest-centroid accuracy falls to 0.5233; at ε = 4.0 it is
0.8167, close to the non-private baseline. The non-monotonic step from ε = 1.0
(0.8233) to ε = 4.0 (0.8167) is ordinary sampling noise, not evidence that more
privacy helps utility.

The membership AUC near 0.5 is the more important teaching result. This naive
distance test does not detect membership. It would be a mistake to conclude that
the release is private because the AUC is low: the test may simply be weak, and
the formal guarantee comes from sensitivity, the mechanism, and composition. A
high AUC would also not by itself prove a formal violation.

## Threat-to-control mapping

| Threat | Control tested | Metric | Residual risk |
|---|---|---|---|
| Membership inference | Laplace noise on centroids | AUC, centroid error | One naive attack; adaptive attacks untested |
| Unbounded per-record influence | Feature clipping | Sensitivity, clipped fraction | Clipping biases estimates |
| Budget overrun | Parallel composition | Per-class ε, total ε | Assumes disjoint fixed-size classes |
| Overstated privacy claim | Explicit sensitivity and δ | Audit claim | No end-to-end system guarantee |
| Utility collapse | ε sweep | Accuracy, centroid error | One synthetic distribution |

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| Sensitivity is 0.012 | Used `B·d/n` and forgot the factor 2 from one-row replacement | Use `2·B·d/n` |
| Scale is `sensitivity · ε` | Inverted the Laplace scale | Scale is `sensitivity / ε` |
| Total budget is 2ε | Applied sequential composition across disjoint classes | Use parallel composition when classes are disjoint |
| AUC is exactly 0.5 for both classes | Scores not separated by class, or labels misaligned | Score against the row's own class centroid |
| Low ε improves accuracy | Noise scale or RNG mapping is wrong | Check the scale and the epsilon-to-seed mapping |

## Rubric

| Item | Points |
|---|---:|
| Correct clipping and sensitivity derivation | 5 |
| Correct Laplace release and composition statement | 5 |
| Correct distance-based membership AUC | 3 |
| Utility sweep and audit configuration | 3 |
| Scoped claim and limitations | 2 |
| Reproducible artifacts and manifest | 2 |

## Reflection questions

1. Why is the sensitivity `2 * B * d / n` rather than `B * d / n`? Derive the
   factor of two from the neighboring-dataset definition.
2. What exactly does epsilon 0.5 promise, and to whom? State the neighboring
   relation and the release in the same sentence.
3. Why does parallel composition apply to disjoint fixed-size classes, and what
   changes if the same person appears in both classes?
4. Accuracy at epsilon 4.0 is slightly lower than at epsilon 1.0. Give two
   explanations that do not involve a bug.
5. The membership AUC is 0.5308 at epsilon 0.5. What can you conclude, and what
   can you not conclude?
6. What would a stronger membership attack need that the distance score does not
   use?
7. How would you extend the accounting if you released the same centroids every
   day for a week?
8. Why is a DP guarantee still meaningful when an empirical attack fails to
   detect anything?
