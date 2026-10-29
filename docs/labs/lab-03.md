# LAB-03 — Evasion Versus Perturbation Budget

**Tier A · 4 hours · Difficulty 2 · Module M04 · Outcomes LO-05, LO-28**

## Why this lab exists

An evasion claim is not "the model can be fooled." It is "at L∞ budget ε, on this base set, this many correct predictions became wrong." Without the budget and the base set, the number is not a security result.

This lab makes that sentence real with a model you can fit in seconds and gradients you can compute by hand. You will implement FGSM and PGD for a multinomial logistic regression, sweep ε, and watch attack success rise. You will also meet the first non-obvious result in the course: a one-step attack is not merely a weaker version of the iterative attack — the gap between them changes with the budget.

## The system and the threat model

| Element | Assumption |
|---|---|
| Target | A 10-class logistic regression trained on 8×8 digit images, decision at the argmax |
| Attacker goal | Integrity: make the model output a wrong class for a chosen input |
| Attacker knowledge | **White-box**: weights, preprocessing, and gradients are known |
| Attacker capability | Add a perturbation δ to the input features before inference |
| Constraint | L∞ norm: every pixel moves by at most ε; pixels stay in [0, 1] |
| Base set | Test images the clean model classifies correctly |
| Metric | Attack success rate (fraction of that base set whose prediction changes) and robust accuracy |
| Lifecycle stage | Serving / inference |
| Out of scope | Physical deployment, query access, defenses, real systems |

The attacker is not assumed to control labels, retrain the model, or observe the provider's logs.

## What you produce

A folder inside `labs/lab-03-evasion-magnitude/` containing:

| File | Contents |
|---|---|
| `metrics.json` | Clean accuracy and ASR for FGSM and PGD at five ε values |
| `run.json` | Seed, model, environment versions |
| `report.md` | Threat model, curves, interpretation, limitations |
| `manifest.json` | SHA-256 hashes of the three files above |

The reference implementation writes these four files to `artifacts/`. Your completed `starter.py` must write the same schema.

## Prerequisites

- Module 04 Lessons 1–3 (Lp budgets, FGSM, PGD).
- Module 02 Lesson 2 (cross-entropy and gradients).
- You can explain why the sign of a gradient is used under an L∞ constraint.

## Environment

- Python 3.14.7; `numpy==2.5.2`, `scikit-learn==1.9.0`, `joblib==1.5.3`.
- CPU only; the reference run takes under a minute.
- No network, no cloud account, no API key. The digits dataset ships with scikit-learn.

Install from the lab folder:

```bash
cd labs/lab-03-evasion-magnitude
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab03.py --artifacts artifacts
```

## Data and safety

The lab uses `sklearn.datasets.load_digits`: 1,797 public 8×8 digit images. There is no personal data and no third-party target. You attack a model you trained yourself, in memory, on your own machine. The perturbation is an array operation, not a request to any service.

## Task specification

1. **Reproduce the clean baseline.** Load digits, scale pixels to [0, 1], split 70/30 with `random_state=42` and stratification, and fit `LogisticRegression(max_iter=5000)`.
2. **Derive the input gradient.** For multinomial logistic regression with probability vector *p* and one-hot label *y*, the gradient of cross-entropy with respect to the input is `(p - y) @ coef_`. Implement it without calling a deep-learning library.
3. **Implement FGSM.** One step: `x' = clip(x + ε·sign(g), 0, 1)`. Attack only rows the clean model gets right, then recompute predictions.
4. **Implement PGD.** Start at the clean input, take 40 sign-gradient steps with step size `max(ε/10, 0.005)`, run 3 random restarts, and project onto the L∞ ball around the original input and onto [0, 1].
5. **Sweep ε.** Use `[0.0, 0.02, 0.05, 0.10, 0.20]`. At ε = 0 both attacks must return the input unchanged and ASR must be 0.
6. **Measure the perturbation.** Report mean and maximum L∞ and mean L2 distance for each attack and budget. Confirm the L∞ bound is never exceeded.
7. **Write the report.** State the threat model, show the table, explain the FGSM–PGD gap, and list at least four limitations.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `input_gradient` | Gradient of mean cross-entropy with respect to the input |
| `starter.py` | TODO 2 | `fgsm_attack` | One-step sign attack with clipping to [0, 1] |
| `starter.py` | TODO 3 | `pgd_attack` | Iterative sign attack projected into the L∞ ball, with restarts |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-03-evasion-magnitude/CHECKING.md`.

## Expected outputs

Reference values (seed 42, deterministic digits split):

| ε | FGSM ASR | PGD ASR |
|---:|---:|---:|
| 0.00 | 0.0000 | 0.0000 |
| 0.02 | 0.0383 | 0.0383 |
| 0.05 | 0.1130 | 0.1188 |
| 0.10 | 0.3352 | 0.3602 |
| 0.20 | 0.8908 | 0.9655 |

Clean accuracy: 0.9667.

At ε = 0.02 FGSM and PGD agree exactly: the first sign step saturates every pixel, and forty more steps do not move the image further under the projection. At ε = 0.20 the iterative attack wins by about 7.5 percentage points. That is the interesting part — the value of iteration depends on the budget.

Your numbers should match within the checker tolerances (0.005 for clean accuracy, 0.02 for ASR). If they differ more, check the split, the gradient sign, and the projection order.

## Deliverables checklist

- [ ] `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] Five FGSM and five PGD rows with ASR, robust accuracy, and perturbation measurements.
- [ ] `report.md` answers every reflection question and states at least four limitations.
- [ ] `python check_lab03.py --artifacts artifacts` exits 0.

## Success criteria

- [ ] ASR is computed on the clean-correct base set, with the base-set size printed.
- [ ] ε = 0 produces zero perturbation and identical predictions.
- [ ] Every perturbed row respects the L∞ bound and the [0, 1] range.
- [ ] FGSM and PGD results reproduce within tolerance.
- [ ] The report explains why the two attacks converge at small ε and diverge at large ε.
- [ ] The report states that success on this model does not establish universal fragility.
- [ ] `python check_lab03.py --artifacts artifacts` exits 0.

## How to check yourself

The checker rebuilds the split and the model, then verifies the clean accuracy, the five ε rows, monotonicity of both curves, the L∞ bounds inferred from the metrics, and the report sections. It cannot judge whether your explanation is correct. Use the rubric below for that.

## Rubric (20 points)

| Item | Points |
|---|---:|
| Correct input gradient and FGSM | 4 |
| PGD with projection, restarts, and clipping | 5 |
| Correct base set and ASR definition | 3 |
| Perturbation measurements and bounds | 3 |
| Explanation of the FGSM–PGD gap | 3 |
| Threat model, limitations, reproducibility | 2 |

## Reflection questions

1. Why does the attack base set exclude rows the clean model already gets wrong?
2. What does the identical FGSM/PGD result at ε = 0.02 tell you about the geometry of the constraint?
3. If you reported ASR over the whole test set, how would the number change, and why is that misleading?
4. The model is linear. What would you expect to change with a nonlinear model?
5. A defender says "we clip inputs, so ε ≥ 0.2 is unrealistic." What would you need to know before accepting that argument?

## Hints

1. For multinomial logistic regression, the input gradient of mean cross-entropy is `(p - onehot(y)) @ coef_ / n`. Check the sign before stepping.
2. FGSM is one signed step. PGD repeats that step and projects into `[max(0, x-ε), min(1, x+ε)]` after every iteration.
3. Measure ASR only on rows the clean model classified correctly; otherwise clean errors are counted as attack successes.
4. If PGD is weaker than FGSM, inspect the step size, the restart loop, and the final projection before changing the model.

## Time box

| Hour | Work |
|---|---|
| 1 | Baseline, gradient, FGSM |
| 2 | PGD, projection, restarts |
| 3 | Sweep, measurements, sanity checks |
| 4 | Report and reflection |

Stop at 6 hours and submit with a note on what is incomplete.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| ASR stays 0 at every ε | Gradient sign applied with the wrong sign, or predictions recomputed on clean X | Use `x + ε·sign(g)` and predict on the perturbed array |
| L∞ exceeds ε | Clipping to [0, 1] instead of the ε-ball | Project onto `[x−ε, x+ε]` first, then [0, 1] |
| Clean accuracy differs | Wrong split or no stratification | Use `test_size=0.3`, `random_state=42`, `stratify=y` |
| ε = 0 changes predictions | Random restarts applied at ε = 0 | Return a copy of X immediately |
| PGD worse than FGSM | Step size too large or restart loop resets incorrectly | Use `α = max(ε/10, 0.005)`; keep the best attack per row |

## Cleanup

```bash
# Windows PowerShell
Remove-Item -Recurse -Force artifacts
# macOS/Linux
rm -rf artifacts
```

Remove the virtual environment if you created one for this lab. Never commit `artifacts/`.

## References

- [Lab catalog](../lab-catalog.md) · [Learning outcomes](../learning-outcomes.md)
- [References](../references.md) — R-11, R-18, R-24
- [Module page](../modules/m04-evasion/index.md) — M04 — Adversarial Examples and Evasion Attacks
- Package checking guide: `labs/lab-03-evasion-magnitude/CHECKING.md`

## What comes next

[LAB-04](lab-04.md) removes the white-box assumption: you will attack a random forest you cannot differentiate, first by transfer from the logistic model, then by measuring how much the black-box target agrees with the source. Module 04 Lesson 4 explains the threat-model change before you start.
