# LAB-04 — Targeted Evasion and Transfer to a Black-Box Model

**Tier A · 4 hours · Difficulty 3 · Module M04 · Outcomes LO-05, LO-06, LO-07, LO-28**

## Why this lab exists

Most real attackers cannot differentiate the target. They have a model they can train, a target they can query, and a budget. The question stops being "what is the gradient?" and becomes "how much of a white-box attack survives the move to a different model?"

This lab splits the problem cleanly. You generate untargeted and targeted examples on a logistic regression, then apply the *same perturbed pixels* to a random forest. The random forest is a stand-in for a black-box target: you can query it, but you cannot take its gradient. The lab measures transfer success and shows where intuition fails.

## The system and the threat model

| Element | Assumption |
|---|---|
| Source model | Multinomial logistic regression, white-box |
| Target model | Random forest (300 trees, depth 12), treated as black-box |
| Attacker goal | (a) untargeted: change the predicted class; (b) targeted: force class 3 |
| Attacker knowledge | Source weights known; target labels observable on a query set, gradients unknown |
| Capability | Generate perturbations on the source; submit the same inputs to the target |
| Constraint | L∞ budget ε ∈ {0.05, 0.10, 0.20, 0.30}; perturbed inputs stay in [0, 1] |
| Base set | Test rows the **source** classifies correctly; targeted set also excludes rows already labeled 3 |
| Metrics | Source ASR, target (transfer) ASR, targeted success on source and target |
| Lifecycle stage | Serving / inference |

The target is not assumed to share training data with the source, but both are trained on the same public digits distribution. That makes this a *favourable* transfer setting, and the report must say so.

## What you produce

`metrics.json`, `run.json`, `report.md`, and `manifest.json` in `artifacts/`.

`metrics.json` must report:

- clean accuracy for source and target;
- targeted success at ε = 0.10, 0.20, 0.30 for source and target;
- untargeted ASR at ε = 0.05, 0.10, 0.20, 0.30 for source and target;
- the eligible base-set size for each experiment.

## Prerequisites

- LAB-03 and Module 04 Lessons 2–4.
- You can explain the difference between a white-box and a black-box threat model.
- You can read a two-model comparison table without confusing fidelity with success.

## Environment

```bash
cd labs/lab-04-targeted-transfer
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab04.py --artifacts artifacts
```

Python 3.14.7, NumPy, scikit-learn. CPU only; no network. The random forest uses `n_jobs=-1` but remains small.

## Data and safety

Same public digits dataset as LAB-03. The "black-box" target is a local model you trained. No request leaves your machine. This lab does **not** demonstrate an attack on a real API, and a successful transfer here does not imply that any particular deployed model is vulnerable.

## Task specification

1. **Train both models.** Use the same 70/30 stratified split (`random_state=42`) for the source and target.
2. **Implement targeted PGD.** For target class *t*, minimize the loss for *t*: take steps in `−sign(gradient)` within `[x−ε, x+ε]`, then clip to [0, 1]. Use 50 steps and `α = ε/10`.
3. **Choose the base set.** Targeted success is measured only on rows whose true label is not 3 and which the source classifies correctly. Print the count.
4. **Sweep targeted ε.** Run targeted PGD at 0.10, 0.20, and 0.30. Report the fraction of the base set predicted as 3 by the source and by the target.
5. **Run untargeted transfer.** Generate FGSM examples on the source at 0.05, 0.10, 0.20, and 0.30. Apply them unchanged to the target. Report ASR on the source and on the target, using the clean-correct source base set.
6. **Compare the curves.** Explain why target ASR is close to source ASR at small ε but falls behind as ε grows.
7. **Write the observer note.** Describe what a defender logging queries would see: query volume, input similarity to clean data, and prediction distribution. Do not claim that logging stops the attack.
8. **State limitations.** At least: same distribution, one source/target pair, no query adaptation, no defense, small 8×8 images.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `gradient` | Gradient of cross-entropy with respect to the input |
| `starter.py` | TODO 2 | `targeted_pgd` | Minimize the target-class loss inside the L∞ ball |
| `starter.py` | TODO 3 | `untargeted_fgsm` | One-step attack that increases the true-class loss |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-04-targeted-transfer/CHECKING.md`.

## Expected outputs

Reference values (seed 42):

| Quantity | Value |
|---|---:|
| Source clean accuracy | 0.9667 |
| Target clean accuracy | 0.9704 |
| Targeted success on source, ε = 0.10 / 0.20 / 0.30 | 0.1090 / 0.5620 / 0.9808 |
| Targeted success on target, ε = 0.10 / 0.20 / 0.30 | 0.0556 / 0.2564 / 0.6175 |
| Untargeted source ASR, ε = 0.05 / 0.10 / 0.20 / 0.30 | 0.1130 / 0.3352 / 0.8908 / 1.0000 |
| Untargeted target ASR, ε = 0.05 / 0.10 / 0.20 / 0.30 | 0.1034 / 0.3487 / 0.7893 / 0.9904 |

Two results deserve attention:

- At ε = 0.30 the targeted attack works on 98% of source rows but only 62% of the same rows on the target. Transfer is real but lossy.
- Untargeted transfer at ε = 0.10 is *slightly better* on the target than the source (0.3487 vs 0.3352). That is not a bug: the target's decision boundary differs, and a perturbation can cross it even when the source's prediction is unchanged. It shows why transfer must be measured, not assumed.

## Deliverables checklist

- [ ] `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] Targeted and untargeted transfer results at the stated budgets, with source and target metrics separated.
- [ ] `report.md` answers every reflection question and states the transfer claim's limits.
- [ ] `python check_lab04.py --artifacts artifacts` exits 0.

## Success criteria

- [ ] Both models are trained on the identical split.
- [ ] Targeted success excludes rows whose true label is the target class.
- [ ] Target ASR uses perturbations generated without target gradients.
- [ ] The three targeted budgets and four untargeted budgets are present with the documented schema.
- [ ] The report separates source success from transfer success and explains the gap.
- [ ] The observer note is concrete and does not overclaim detection.
- [ ] `python check_lab04.py --artifacts artifacts` exits 0.

## How to check yourself

From `labs/lab-04-targeted-transfer/`:

```bash
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab04.py --artifacts artifacts
```

Exit code 0 means the checker independently reproduced the reference artifacts and metrics within tolerance. Complete `starter.py` and run the same checker on your own artifacts. `CHECKING.md` lists the exact checks and common failure modes.

## Rubric (20 points)

| Item | Points |
|---|---:|
| Correct targeted PGD direction | 4 |
| Correct base sets and denominators | 4 |
| Transfer protocol (target never differentiated) | 4 |
| Interpretation of the source–target gap | 4 |
| Observer note and limitations | 3 |
| Reproducibility | 1 |

## Reflection questions

1. Why can targeted transfer fail even when untargeted transfer succeeds?
2. The target is a different model family trained on the same data. Would transfer improve or worsen with a target trained on different data? Why?
3. At ε = 0.30 the source is almost perfectly attacked. Why is the target number the one a risk owner cares about?
4. An API returns only labels, not probabilities. How would that change the attacker's ability to build a surrogate?
5. What would an adaptive attacker do after seeing the transfer curve?

## Hints

1. Targeted PGD decreases the target-class loss, not the true-class loss. The sign of the update is the opposite of the untargeted case.
2. Use the target model only to evaluate. If you query it while crafting, you are measuring a white-box attack and calling it transfer.
3. Report the target-class rate separately from overall error. A transfer attack can raise error without ever producing the chosen class.
4. Run the untargeted baseline on the same rows and budget; otherwise the comparison is confounded.

## Time box

| Hour | Work |
|---|---|
| 1 | Train models, implement targeted PGD |
| 2 | Targeted sweep and base sets |
| 3 | Untargeted transfer sweep |
| 4 | Report, observer note, reflection |

Stop at 6 hours; submit with a blocker note.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Targeted success near 0 | Ascending the target loss | Use `x − α·sign(grad)` with labels set to the target |
| Transfer ASR above source ASR | ASR computed on different base sets | Use the same clean-correct source rows for both |
| Targeted base set is the whole test set | Rows already labeled 3 included | Filter `y != 3` before measuring |
| Different clean target accuracy | Different split seed | Reuse the exact split from LAB-03 |
| Checker reports missing budgets | Keys stored as floats with trailing zeros | Use the string keys shown in `expected_metrics.json` |

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
- [References](../references.md) — R-02, R-12, R-24
- [Module page](../modules/m04-evasion/index.md) — M04 — Adversarial Examples and Evasion Attacks
- Package checking guide: `labs/lab-04-targeted-transfer/CHECKING.md`

## What comes next

Module 05 changes the attacker's access from inputs to the training pipeline. [LAB-05](lab-05.md) starts with the simplest case: label noise at a controlled rate.
