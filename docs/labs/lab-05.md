# LAB-05 — Label-Flip Poisoning Curve

**Tier A · 4 hours · Difficulty 2 · Module M05 · Outcomes LO-08, LO-28**

## Why this lab exists

Poisoning is often described with a single dramatic number. The useful question is a curve: at what fraction of corrupted labels does the model's behavior change, and by how much? A defender needs the curve to decide how much data verification is worth. An attacker needs it to know whether the required access is plausible.

This lab flips labels at five controlled rates on the digits dataset, retrains a logistic regression each time, and measures clean test accuracy and macro F1. The result is counter-intuitive at the low end: 5% corruption barely moves accuracy, because the model can outvote a small amount of wrong information.

## The system and the threat model

| Element | Assumption |
|---|---|
| Target | A 10-class logistic regression trained on 8×8 digit images |
| Attacker goal | Availability / integrity: degrade overall test accuracy |
| Attacker knowledge | The attacker can choose training rows but does not see the test set |
| Capability | Change the label of a fraction of training rows to the next class |
| Constraint | Poison rate is measured against the 1,257-row training set; test labels are untouched |
| Attacker budget | 0%, 5%, 10%, 20%, 30% of training rows |
| Metrics | Clean test accuracy, macro F1, number of poisoned rows |
| Lifecycle stage | Data collection / training |

This is **indiscriminate** poisoning: every class is affected, and the attacker does not care which test predictions change. The next lab covers a targeted attack, where global accuracy can stay flat while one decision flips.

## What you produce

`metrics.json` with a `curve` list at rates 0.00, 0.05, 0.10, 0.20, 0.30. Each row reports `rate`, `poisoned_rows`, `accuracy`, and `macro_f1`. Also write `run.json`, `report.md`, and `manifest.json`.

## Prerequisites

- LAB-01 or LAB-01B (training and evaluation).
- Module 05 Lessons 1–2 (poisoning threat models, label noise).
- You can explain why the poison-rate denominator must be stated.

## Environment

```bash
cd labs/lab-05-label-poisoning
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab05.py --artifacts artifacts
```

Python 3.14.7, scikit-learn, NumPy. Five model fits take a few seconds on CPU.

## Data and safety

Public digits data, local training. The "attacker" is a function in your script that corrupts labels you own. No real dataset, service, or person is involved. The test set is never corrupted; if you corrupt it, you are measuring label noise at evaluation time, which is a different (and invalid) experiment.

## Task specification

1. **Split once.** Use a 70/30 stratified split with `random_state=42`. Keep the test set fixed across all rates.
2. **Implement label flipping.** For rate *r*, select `round(r × n_train)` rows with a fresh `numpy.random.default_rng(42)` per rate, and map each selected label to `(label + 1) % 10`. A fresh generator per rate means the selected rows are not nested, which matches the reference and avoids a subtle dependence between points on the curve.
3. **Train and evaluate.** Fit `LogisticRegression(max_iter=3000)` on the poisoned training labels and report test accuracy and macro F1.
4. **Verify the counts.** Print the number of poisoned rows at each rate and confirm it equals `round(r × n_train)`.
5. **Plot or tabulate the curve.** Identify the rate at which accuracy begins to fall sharply.
6. **Write the report.** State the threat model, include the table, and explain why the 5% point is nearly flat while 30% is not.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO | `poison_labels` | Choose a seeded fraction of training rows and flip their labels |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-05-label-poisoning/CHECKING.md`.

## Expected outputs

| Rate | Poisoned rows | Accuracy | Macro F1 |
|---:|---:|---:|---:|
| 0.00 | 0 | 0.9667 | 0.9666 |
| 0.05 | 63 | 0.9648 | 0.9648 |
| 0.10 | 126 | 0.9389 | 0.9383 |
| 0.20 | 251 | 0.8870 | 0.8876 |
| 0.30 | 377 | 0.7981 | 0.7968 |

The curve is not linear. A 5% flip costs 0.2 points; 30% costs 17 points. Part of the reason is that a flipped label is often still separable: the model learns a noisier boundary rather than losing the class. The report should say that this curve belongs to this model, this dataset, and this flip rule.

## Deliverables checklist

- [ ] `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] One result row per poison rate, with clean accuracy and macro F1.
- [ ] `report.md` answers every reflection question and states the denominator used for each rate.
- [ ] `python check_lab05.py --artifacts artifacts` exits 0.

## Success criteria

- [ ] Exactly five rates with the correct poisoned-row counts.
- [ ] Test accuracy reproduces within 0.005 at every rate.
- [ ] Clean accuracy ≥ 0.95 and 30% accuracy ≤ 0.85.
- [ ] Accuracy is broadly decreasing; a small non-monotone wobble is acceptable.
- [ ] The report states the denominator, the flip rule, and at least three limitations.
- [ ] `python check_lab05.py --artifacts artifacts` exits 0.

## How to check yourself

From `labs/lab-05-label-poisoning/`:

```bash
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab05.py --artifacts artifacts
```

Exit code 0 means the checker independently reproduced the reference artifacts and metrics within tolerance. Complete `starter.py` and run the same checker on your own artifacts. `CHECKING.md` lists the exact checks and common failure modes.

## Rubric (20 points)

| Item | Points |
|---|---:|
| Correct poison selection and counts | 4 |
| Reproducible training and metrics | 4 |
| Curve table and figure | 3 |
| Explanation of the low-rate plateau | 4 |
| Threat model and denominator discipline | 3 |
| Limitations | 2 |

## Reflection questions

1. Why does 5% label corruption barely change test accuracy?
2. Would the curve look the same if flipped labels were chosen adversarially rather than randomly? What would the attacker need to know?
3. Why is macro F1 slightly more sensitive than accuracy here?
4. What does this experiment *not* tell you about a targeted attack on one customer?
5. A vendor claims "we can tolerate 10% label noise." What else would you ask before believing it?

## Hints

1. Choose corrupted indices with a seeded permutation, then flip their labels. Keep the test set untouched.
2. Poison rate is corrupted training rows divided by total training rows. State the denominator in the report.
3. Retrain from scratch at every rate. Reusing a model fitted on clean labels measures nothing.
4. If accuracy barely moves at 30%, check whether the flips are class-balanced and whether the model is underfitting.

## Time box

| Hour | Work |
|---|---|
| 1 | Split, flip function, counts |
| 2 | Train and evaluate all rates |
| 3 | Table/figure and sanity checks |
| 4 | Report and reflection |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Accuracy identical at every rate | Poisoned labels not passed to `fit` | Fit on `y_poisoned`, not `y_train` |
| Test accuracy collapses | Test labels flipped | Corrupt training labels only |
| Counts off by one | Using `int` instead of `round` | Use `int(round(rate * len(y_train)))` |
| Curve not reproducible | Continuing one RNG across rates | Use a fresh `default_rng(42)` per rate |
| Accuracy rises at 30% | Wrong denominator (test rows) | Count against training rows |

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
- [References](../references.md) — R-30, R-38
- [Module page](../modules/m05-poisoning/index.md) — M05 — Training Data Poisoning and Label Manipulation
- Package checking guide: `labs/lab-05-label-poisoning/CHECKING.md`

## What comes next

[LAB-06](lab-06.md) makes the attack targeted. Thirty added points near one location flip a single decision while global accuracy stays flat — and a naive screen that trusts the training data cannot see the problem.
