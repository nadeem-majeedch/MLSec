# LAB-06 — Targeted Poisoning and Reference-Set Screening

**Tier A · 4 hours · Difficulty 3 · Module M05 · Outcomes LO-08, LO-09, LO-28**

## Why this lab exists

A targeted poisoning attack can leave the global accuracy number almost unchanged while flipping a decision the attacker cares about. That is the point, and it is why "our test accuracy is fine" is not a defense.

You will build a small two-dimensional classifier, poison its training set with 30 carefully placed rows, and watch a test point at `(0.1, 0.0)` move from class 1 to class 0. Then you will defend it with a **reference set** — a small trusted sample — and discover the real cost: the screen catches every poison but also flags 37 clean rows.

This lab deliberately has no deep learning. The geometry is visible, and the defense's trade-off is measurable in seconds.

## The system and the threat model

| Element | Assumption |
|---|---|
| Target | Logistic regression on two features, binary classes centered at (−1.2, 0) and (1.2, 0) |
| Attacker goal | Targeted integrity: make the model classify a chosen point as class 0 |
| Attacker knowledge | Knows the feature space and can append rows with arbitrary features and labels |
| Capability | Add 30 rows near the target, labeled 0, to a 350-row training set |
| Constraint | The attacker cannot see the test set or the reference set |
| Defender | Has 150 trusted reference rows, separate from training, and can screen before training |
| Metrics | Target prediction and probability; test accuracy; poisons caught; clean rows falsely flagged |
| Lifecycle stage | Data collection / training |

The attacker controls at most 30 of 380 training rows after the attack (about 8%). The defense's key assumption is that the reference set is trustworthy and drawn from the same distribution. If either is false, the screen's guarantees weaken.

## What you produce

`metrics.json` with three model states (`clean`, `poisoned`, `defended`) and a `screening` block. Each state reports `target_prediction`, `target_probability`, and `accuracy`. `screening` reports `flagged`, `poison_caught`, `clean_flagged`, and `threshold`. Also write `run.json`, `report.md`, and `manifest.json`.

## Prerequisites

- LAB-05.
- Module 05 Lessons 1–3.
- You can explain why a k-NN model fitted on trusted data is not "the same model" as the target.

## Environment

```bash
cd labs/lab-06-targeted-poisoning
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab06.py --artifacts artifacts
```

Python 3.14.7, NumPy, scikit-learn. CPU only; under a second per fit.

## Data and safety

Synthetic two-dimensional data generated locally from seed 7. No personal or real-world data. The "victim" is a model you trained. Nothing is uploaded.

## Task specification

1. **Generate the data.** 600 samples, 300 per class, Gaussian with standard deviation 1.0 around the two centers, shuffled with seed 7. Split into 150 reference rows, 350 training rows, and 100 test rows, in that order.
2. **Train the clean model.** Fit `LogisticRegression` on the 350 rows. Record the prediction and probability at the target point and test accuracy.
3. **Poison the training set.** Append 30 rows drawn from `N([0.1, 0.0], 0.05·I)`, all labeled class 0. Record the poisoned model's target prediction, probability, and test accuracy.
4. **Screen with the reference set.** Fit `KNeighborsClassifier(n_neighbors=9)` on the 150 trusted rows. For every training row, take the reference model's probability of the row's given label; flag rows below 0.6.
5. **Retrain on the kept rows.** Fit the same classifier on unflagged rows. Record target prediction, probability, and accuracy.
6. **Count the costs.** Report how many rows were flagged, how many poisons were caught, and how many clean rows were falsely flagged.
7. **Report.** State the reference-set assumption, show the three-state table, and explain why the defended accuracy is not higher than the poisoned accuracy.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `poison_training_set` | Append mislabeled points near the target point |
| `starter.py` | TODO 2 | `screen_with_reference` | Fit a trusted reference classifier and flag suspicious rows |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-06-targeted-poisoning/CHECKING.md`.

## Expected outputs

| State | Target prediction | Target probability | Test accuracy |
|---|---:|---:|---:|
| Clean | 1 | 0.5903 | 0.8800 |
| Poisoned | 0 | 0.4345 | 0.8900 |
| Defended | 1 | 0.5465 | 0.8900 |

Screening: 67 rows flagged, 30/30 poisons caught, 37 clean rows falsely flagged, threshold 0.6.

Three observations to explain in the report:

- **The poison flips the target without hurting global accuracy.** Accuracy actually rises by one point. Global metrics are the wrong instrument for a targeted attack.
- **The screen catches everything because the poison cluster is dense and far from the reference data.** That is a property of this attack, not a general guarantee.
- **The screen removes 37 clean rows.** Those are probably points near the decision boundary where the 9-neighbor vote is uncertain. The defense trades data for assurance, and the report must quantify that trade.

## Deliverables checklist

- [ ] `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] Target-point prediction before and after poisoning; overall accuracy before and after.
- [ ] Screening results with true and false positives.
- [ ] `report.md` answers every reflection question.
- [ ] `python check_lab06.py --artifacts artifacts` exits 0.

## Success criteria

- [ ] Poison budget is exactly 30 rows against a 350-row clean training set.
- [ ] Clean model predicts 1 and the poisoned model predicts 0 at the target.
- [ ] The defended model predicts 1 again.
- [ ] All 30 poisons are caught and the clean false-positive count is reported.
- [ ] Accuracy values reproduce within 0.01.
- [ ] The report states that the screen depends on a trusted reference set.
- [ ] `python check_lab06.py --artifacts artifacts` exits 0.

## How to check yourself

From `labs/lab-06-targeted-poisoning/`:

```bash
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab06.py --artifacts artifacts
```

Exit code 0 means the checker independently reproduced the reference artifacts and metrics within tolerance. Complete `starter.py` and run the same checker on your own artifacts. `CHECKING.md` lists the exact checks and common failure modes.

## Rubric (20 points)

| Item | Points |
|---|---:|
| Correct poisoning construction | 4 |
| Reference-set screen implemented correctly | 5 |
| Three-state comparison and target probability | 4 |
| False-positive accounting | 3 |
| Explanation of why accuracy is a poor metric here | 3 |
| Assumptions and limitations | 1 |

## Reflection questions

1. Why did test accuracy not fall when the target decision flipped?
2. The screen uses a 9-neighbor vote. What changes at 3 neighbors or 25 neighbors?
3. What happens if 5% of the reference set is also poisoned? Sketch the effect before running it.
4. Is removing 37 clean rows a good trade? What would you need to know about the data budget?
5. Name one attack adaptation that would evade this screen.

## Hints

1. Append the poison rows to the training set; do not replace clean rows. The point is a small, targeted change.
2. Place the poisoned points near the target test point and give them the opposite label, then verify that the decision actually flips.
3. The reference-set screener is a separate trusted model. Report its false positives on clean rows, not only the poison it catches.
4. If overall accuracy barely moves, that is expected. Report the target-point flip and the small accuracy change together.

## Time box

| Hour | Work |
|---|---|
| 1 | Data, clean model, target measurement |
| 2 | Poison construction and poisoned model |
| 3 | Screen, retrain, false-positive accounting |
| 4 | Report and reflection |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Target does not flip | Too few poisons or too wide a spread | Use 30 rows at σ = 0.05 near (0.1, 0.0) |
| Screen catches no poisons | Reference model fitted on training data | Fit k-NN on the reference rows only |
| All rows flagged | Agreement threshold inverted | Flag when `P(given label) < 0.6` |
| Defended prediction still 0 | Screening applied after fitting | Refit on the kept rows |
| Counts differ | Different data order | Follow the 150/350/100 split order in the reference |

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
- Package checking guide: `labs/lab-06-targeted-poisoning/CHECKING.md`

## What comes next

Module 06 turns poisoning into a conditional behavior. In [LAB-07](lab-07.md) the poisoned rows carry a trigger, and the model learns to misbehave only when that trigger is present.
