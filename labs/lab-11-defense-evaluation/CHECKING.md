# Checking Guide — LAB-11

## What the checker verifies

1. `metrics.json`, `run.json`, `report.md`, and `manifest.json` exist, and the manifest covers the three output files.
2. `run.json` records LAB-11, ε = 0.10, 20 PGD steps, and 2 restarts.
3. The checker rebuilds the digits split and clean model; the reported clean accuracy reproduces within 0.005.
4. Undefended baseline: robust accuracy and ASR reproduce within 0.03 and the base set is the 522 clean-correct rows.
5. Adversarial training: clean accuracy 0.8907 ± 0.02; robust accuracy 0.7296 ± 0.03; robust accuracy improves by at least 0.05 over the baseline; clean accuracy drops by at least 0.05.
6. Input squeezing: clean accuracy 0.9500 ± 0.01; naive ASR 0.1871 ± 0.03; robust accuracy 0.7722 ± 0.03; adaptive ASR is a valid fraction.
7. Stress budget: ε = 0.20 is larger than the main budget; squeezing stress ASR ≥ 0.90; baseline stress ASR ≥ 0.90; adversarially trained stress ASR ≥ 0.50.
8. Every clean, robust, and ASR value lies in [0, 1].
9. The report contains "adaptive", "stress", "budget", and "limitations".

## Reference results (seed 42)

| Model | Clean accuracy | Robust accuracy (ε = 0.10) | ASR |
|---|---:|---:|---:|
| Undefended | 0.9667 | 0.6204 | 0.3582 |
| Adversarial training | 0.8907 | 0.7296 | 0.1809 |
| Input squeezing | 0.9500 | 0.7722 | 0.1871 |

Base sets: 522 undefended, 481 adversarially trained, 513 squeezed.

Stress budget ε = 0.20:

| Model | ASR | Robust accuracy |
|---|---:|---:|
| Undefended | 0.9579 | 0.0407 |
| Adversarial training | 0.6029 | 0.3537 |
| Input squeezing (naive / adaptive) | 0.9571 / 0.9981 | 0.0019 |

At ε = 0.10 the BPDA adaptive attack reaches ASR 0.1832 against squeezing,
essentially the same as the naive attack (0.1871). The interesting adaptive result
is at the stress budget, where the defense has already collapsed.

## Why these numbers matter

Input squeezing is the trap. At the main budget it has the best robust accuracy
and a small clean-accuracy cost, so a single-row table would recommend it. The
stress budget shows that the apparent protection is an artifact of the budget
choice: the same attack family reaches 95.7% success. The correct conclusion is
narrow — "squeezing delayed the attack at ε = 0.10 in this setup" — not "squeezing
is a robust defense."

Adversarial training is not a universal fix either. It improves robust accuracy
and still loses 60.3% ASR at ε = 0.20, with a real clean-accuracy cost.

## Threat-to-control mapping

| Threat | Control tested | Metric | Residual risk |
|---|---|---|---|
| PGD evasion at ε = 0.10 | Adversarial training | Robust accuracy, ASR, clean cost | Breaks at ε = 0.20; other attack families untested |
| PGD evasion at ε = 0.10 | Input squeezing | Naive ASR, robust accuracy | Collapses at ε = 0.20; adaptive attack untested beyond BPDA |
| Gradients blocked by rounding | BPDA adaptive attack | Adaptive ASR | Stronger adaptive attacks may do better |
| Overstated defense claim | Stress budget and honest report | Reported limitations | One model, one split, one attack family |

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| `NotImplementedError` | A TODO block is untouched | Implement squeeze, adversarial_train, or pgd_squeezed_bpda |
| Adversarial training lowers robust accuracy | Clean-only refit overwhelmed by augmentation | Use `C=0.01` and PGD examples at ε = 0.10 |
| Squeezed clean accuracy far below 0.95 | Grid not in [0, 1] or wrong number of levels | Use `levels=4` and clip after rounding |
| Adaptive ASR is exactly 0 or 1 | Success measured on raw input or wrong mask | Predict on `squeeze(x_adv)` and use the squeezed clean-correct mask |
| Squeeze L∞ exceeds 0.10 | Comparing quantized input to the original | Measure the attack perturbation `naive_adv - X_test` |
| Checker says stress ASR too low | Stress run reused the main budget | Pass `epsilon=0.20` and `alpha=0.04` |

## Rubric (20 points)

| Item | Points |
|---|---:|
| Correct squeezing and adversarial training | 5 |
| Correct adaptive (BPDA) attack | 4 |
| Clean and robust metrics on the right base sets | 4 |
| Stress-budget evaluation and honest interpretation | 4 |
| Report with threat model, trade-offs, and limitations | 3 |

## Reflection questions

1. Why does a defense need an explicit budget before "robust accuracy" means anything?
2. Input squeezing beats adversarial training at ε = 0.10 but fails at ε = 0.20. Which defense would you deploy, and what else would you need to know?
3. Why does BPDA replace the rounding derivative with the identity, and what does that assumption hide?
4. Adversarial training costs 7.6 points of clean accuracy. How would you decide whether that trade is acceptable?
5. Your checker passes. What has that actually proven, and what has it not proven?
