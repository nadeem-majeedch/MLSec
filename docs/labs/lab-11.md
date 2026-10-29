# LAB-11 — Robustness Evaluation and Defensive Baselines

**Tier A · 6 hours · Difficulty 3 · Module M08 · Outcomes LO-16, LO-17, LO-18, LO-28**

## Why this lab exists

A defense claim without a threat model is marketing. "Our model is robust" means
nothing until you name the attacker's budget, the base set, and the attack. This
lab builds the comparison infrastructure that every later defense claim in the
course reuses: one clean model, two defenses, one attack family, two budgets, and
one adaptive check.

The result is deliberately uncomfortable. The defense that looks best at the
published budget is the one that collapses when the budget grows. The defense
that survives the stress budget still loses most of its protection and costs
clean accuracy. You will write a report that can defend neither as "secure."

## The system and the threat model

| Element | Assumption |
|---|---|
| Target | 10-class logistic regression on 8×8 digit images, decision at argmax |
| Attacker goal | Integrity: make the model output a wrong class |
| Attacker knowledge | **White-box**: weights, preprocessing, and gradients known |
| Attacker capability | Add a perturbation to the input before inference |
| Primary budget | L∞ ε = 0.10, pixels remain in [0, 1] |
| Stress budget | L∞ ε = 0.20, same attack family |
| Base set | Rows each model classifies correctly on clean input |
| Primary metric | Attack success rate (ASR) and robust accuracy |
| Secondary metric | Clean accuracy and its cost relative to the undefended model |
| Lifecycle stage | Evaluation, before deployment |
| Out of scope | Physical-world attacks, query-only access, training-time attacks, certified guarantees |

The attacker does not control labels, retrain the model, or observe logs. The
defender may change training (adversarial training) or inference preprocessing
(input squeezing). Neither defense is assumed to be universally effective.

## What you produce

A folder inside `labs/lab-11-defense-evaluation/` containing:

| File | Contents |
|---|---|
| `metrics.json` | Clean/robust accuracy, ASR, base-set sizes, L∞ measurements, adaptive and stress results |
| `run.json` | Lab id, seed, budget, attack settings, environment versions |
| `report.md` | Comparison table, adaptive check, stress result, trade-offs, limitations |
| `manifest.json` | SHA-256 hashes of the three files above |

The reference implementation writes these four files to `artifacts/`. Your
completed `starter.py` must write the same schema.

## Prerequisites

- Module 04 Lessons 2–4 (FGSM, PGD, transfer) and LAB-03.
- Module 08 Lessons 1–3 (robustness metrics, adversarial training, preprocessing defenses).
- You can explain what a clean-correct base set is and why ASR uses it.

## Environment

- Python 3.14.7; `numpy==2.5.2`, `scikit-learn==1.9.0`, `joblib==1.5.3`.
- CPU only; the reference run takes about two minutes.
- No network, no cloud account, no API key.

```bash
cd labs/lab-11-defense-evaluation
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab11.py --artifacts artifacts
```

## Data and safety

The lab uses `sklearn.datasets.load_digits`: 1,797 public 8×8 digit images.
There is no personal data and no third-party target. All attacks are array
operations against models you fit locally. Nothing is sent to a service.

## Task specification

1. **Rebuild the baseline.** Load digits, scale to [0, 1], split 70/30 with
   `random_state=42`, stratify by label, and fit `LogisticRegression(max_iter=5000, C=1.0)`.
2. **Implement input squeezing.** Snap every pixel to a four-level grid
   `{0, 1/3, 2/3, 1}`. This is the preprocessing defense.
3. **Implement adversarial training.** Generate PGD examples for the training
   set at ε = 0.10 with step size ε/5 and one restart, stack them with the clean
   rows, and refit with `C=0.01`.
4. **Evaluate at ε = 0.10.** Run the given PGD (20 steps, α = ε/5, 2 restarts)
   against the undefended model, the adversarially trained model, and the
   squeezed pipeline. Compute ASR on each model's own clean-correct base set.
5. **Run the adaptive attack.** Implement PGD with a straight-through (BPDA)
   gradient through the quantizer and report its ASR against squeezing.
6. **Stress the claim.** Repeat the baseline, adversarially trained, and
   squeezed evaluations at ε = 0.20 with α = 0.04.
7. **Measure perturbations.** Report mean and maximum L∞ of the attack
   perturbation, not of the post-squeeze input, so defense distortion does not
   masquerade as attack budget.
8. **Write the report.** Include the comparison table, the adaptive and stress
   results, the clean-accuracy cost, a threat-to-control table with residual
   risks, and at least four limitations.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `squeeze` | Quantize or smooth the input as a preprocessing defense |
| `starter.py` | TODO 2 | `adversarial_train` | Train with PGD augmentation at a fixed budget |
| `starter.py` | TODO 3 | `pgd_squeezed_bpda` | Adaptive attack through the non-differentiable preprocessing |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-11-defense-evaluation/CHECKING.md`.

## Expected outputs

Reference values (seed 42, deterministic digits split):

| Model | Clean accuracy | Robust accuracy (ε = 0.10) | ASR |
|---|---:|---:|---:|
| Undefended | 0.9667 | 0.6204 | 0.3582 |
| Adversarial training | 0.8907 | 0.7296 | 0.1809 |
| Input squeezing | 0.9500 | 0.7722 | 0.1871 |

Adversarial training raises robust accuracy by 10.9 points and lowers clean
accuracy by 7.6 points. Input squeezing raises robust accuracy by 15.2 points
with only a 1.7-point clean cost — at this budget.

Stress budget ε = 0.20:

| Model | ASR | Robust accuracy |
|---|---:|---:|
| Undefended | 0.9579 | 0.0407 |
| Adversarial training | 0.6029 | 0.3537 |
| Input squeezing | 0.9571 | 0.0019 |

At ε = 0.10 the BPDA adaptive attack reaches ASR 0.1832 against squeezing, close
to the naive 0.1871. At ε = 0.20 the adaptive attack reaches 0.9981. Report both
honestly: the adaptive check did not overturn the main-budget result, but the
stress budget did.

Your numbers should match within the checker tolerances (0.005 for clean
accuracy, 0.02–0.03 for the defense metrics).

## Threat-to-control mapping

| Threat | Control | Evidence to report | Residual risk |
|---|---|---|---|
| Evasion at ε = 0.10 | Adversarial training | Robust accuracy and ASR on a fixed base set | Cost to clean accuracy; failure at ε = 0.20; other attacks untested |
| Evasion at ε = 0.10 | Input squeezing | Naive ASR and robust accuracy | Collapse at ε = 0.20; adaptive attack surface |
| Gradient masking by rounding | BPDA adaptive attack | Adaptive ASR at both budgets | BPDA is one adaptive strategy, not a proof of strength |
| Defense overclaim | Budget sweep and explicit threat model | Clean and robust numbers side by side | One model, one split, one attack family |
| Silent metric inflation | Attack perturbation measured on raw input | `mean_linf`, `max_linf` | Metrics still depend on the base-set definition |

## Defense-in-depth perspective

A realistic deployment might combine adversarial training, input validation,
rate limiting, and monitoring. This lab does not test that composition. Each
control here was evaluated alone, against one attack family, on one model. The
honest statement is: "control A improved a measured metric under threat model T;
its effect under composition is untested." Composing two weak defenses does not
create a strong one, and a passing checker does not prove security.

## Deliverables checklist

- [ ] `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] Clean and robust accuracy for the undefended model and both defenses at both budgets.
- [ ] The adaptive-attack result against the preprocessing defense.
- [ ] `report.md` answers every reflection question and states the evaluation conditions of every claim.
- [ ] `python check_lab11.py --artifacts artifacts` exits 0.

## Success criteria

- [ ] All three defenses are evaluated on their own clean-correct base sets, with sizes reported.
- [ ] Clean accuracy, robust accuracy, and ASR are all reported at the main budget.
- [ ] The clean-accuracy cost of adversarial training is stated explicitly.
- [ ] The stress budget is evaluated and the squeezing collapse is reported.
- [ ] The BPDA adaptive result is reported without overstating it.
- [ ] L∞ measurements use the attack perturbation and never exceed the budget.
- [ ] The report states that a passing test is not proof of security.
- [ ] `python check_lab11.py --artifacts artifacts` exits 0.

## How to check yourself

The checker rebuilds the split and clean model, then verifies the reported
metrics, the improvement and cost conditions, the stress collapse, and the report
sections. It cannot judge whether your interpretation is honest. Use the rubric
and the reflection questions for that. A submission can pass every numeric check
and still fail the lab by claiming that squeezing is a robust defense.

## Rubric (20 points)

| Item | Points |
|---|---:|
| Correct squeezing and adversarial training | 5 |
| Correct adaptive (BPDA) attack | 4 |
| Clean and robust metrics on the right base sets | 4 |
| Stress-budget evaluation and interpretation | 4 |
| Report with threat model, trade-offs, residual risks, limitations | 3 |

## Reflection questions

1. Why is "robust accuracy" meaningless without a stated budget and attack?
2. At ε = 0.10, squeezing beats adversarial training on both clean and robust accuracy. Why is deploying it anyway a mistake under this threat model?
3. What does BPDA assume about the quantizer, and what kind of adaptive attack would you try next?
4. How would you present the clean-accuracy cost to a product owner who cares about normal traffic?
5. The checker passed. Name three things it did not verify.
6. If you combined both defenses, what experiment would you need before claiming a benefit?

## Hints

1. Squeezing is a preprocessing function: quantize or smooth the input, then predict. Apply it identically at training and test time.
2. Adversarial training augments each batch with PGD examples at a fixed budget. Record that budget in the run record.
3. BPDA means using the identity gradient through the non-differentiable preprocessing step, then attacking the full pipeline.
4. Report clean and robust accuracy at both budgets. A defense that wins at ε=0.10 and loses at ε=0.20 is not robust.

## Time box

| Hour | Work |
|---|---|
| 1 | Baseline, splitting, squeezing |
| 2 | Adversarial training and main-budget evaluation |
| 3 | Adaptive BPDA attack |
| 4 | Stress budget and measurements |
| 5 | Report with threat-to-control mapping |
| 6 | Reflection, reproduction from a clean process |

Stop at 9 hours and submit with a note on what is incomplete.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `NotImplementedError` | A TODO block is untouched | Complete squeeze, adversarial_train, or pgd_squeezed_bpda |
| Adversarial training worsens robustness | Overfit to clean rows | Use `C=0.01` and augment with ε = 0.10 PGD examples |
| Squeezed clean accuracy is low | Grid values outside [0, 1] | Round, divide by `levels - 1`, then clip |
| Adaptive ASR is 0 | Success tested on raw inputs | Predict on `squeeze(x_adv)` |
| Squeeze L∞ exceeds 0.10 | Comparing squeezed input to the original | Measure `naive_adv - X_test` |
| Stress ASR looks like the main result | Budget not passed through | Set `epsilon=0.20`, `alpha=0.04` |
| Metrics differ from reference | Wrong split or model capacity | Keep seed 42, `test_size=0.3`, `C=1.0` for the baseline |

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
- [References](../references.md) — R-18, R-19, R-22, R-24
- [Module page](../modules/m08-robustness-defense/index.md) — M08 — Robustness Evaluation and Adversarial Defense
- Package checking guide: `labs/lab-11-defense-evaluation/CHECKING.md`

## What comes next

[LAB-12](lab-12.md) leaves the model and moves to the data pipeline: you will
build validation gates for schema, duplicates, suspicious labels, missing values,
and train/test leakage, and show how a leak inflates an evaluation score. Module
09 Lessons 1–3 explain the governance model first.
