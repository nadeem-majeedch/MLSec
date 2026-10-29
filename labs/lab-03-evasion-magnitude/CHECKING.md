# Checking Guide — LAB-03

## What the checker verifies

`check_lab03.py` independently rebuilds the digits split and the logistic model, then checks:

1. `metrics.json`, `run.json`, `report.md`, and `manifest.json` exist and the manifest covers the three output files.
2. The clean accuracy reproduces within 0.005.
3. Five epsilon rows exist for FGSM and PGD, ASR is non-decreasing, and every perturbation respects the L-inf budget.
4. FGSM at ε = 0.20 reaches ASR ≥ 0.85 and PGD reaches ASR ≥ 0.93.
5. PGD is not materially weaker than FGSM at ε = 0.10.
6. The report mentions clean accuracy, ASR, and limitations.

## Reference results (seed 42)

| Method | ε | ASR |
|---|---:|---:|
| FGSM | 0.00 | 0.0000 |
| FGSM | 0.02 | 0.0383 |
| FGSM | 0.05 | 0.1130 |
| FGSM | 0.10 | 0.3352 |
| FGSM | 0.20 | 0.8908 |
| PGD | 0.05 | 0.1188 |
| PGD | 0.10 | 0.3602 |
| PGD | 0.20 | 0.9655 |

Clean accuracy is 0.9667 on the 540-example test split.

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| `NotImplementedError` | TODO blocks untouched | Complete gradient, FGSM, PGD |
| ASR is zero everywhere | Gradient sign is applied to the wrong tensor or prediction is taken before clipping | Recompute `(p - onehot) @ coef_`; clip to [0, 1] |
| Checker reports budget violation | Clipping only to [0, 1], not to `X ± ε` | Project each step into the epsilon ball |
| PGD weaker than FGSM | Step size too large or no final projection | Use `alpha ≈ ε/10` and 40 steps |
| ASR not monotone | Evaluating all examples instead of clean-correct examples | Restrict success to `clean_correct` |

## Rubric (20 points)

| Item | Points |
|---|---:|
| Correct gradient and FGSM | 4 |
| Correct PGD with projection and restarts | 5 |
| Complete epsilon sweep and metrics | 4 |
| Budget compliance and monotonicity | 3 |
| Report with threat model and limitations | 4 |

## Reflection questions

1. Why is ASR measured on clean-correct examples rather than all examples?
2. At which budget does the linear model stop being useful, and what does that say about linearity as a robustness assumption?
3. Why does PGD usually beat FGSM at the same ε, and when might it not?
4. What would change if the defender rounded pixel values to 4 bits before prediction?
