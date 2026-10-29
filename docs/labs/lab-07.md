# LAB-07 — Tabular Backdoor with a Known Trigger

**Tier B · 4 hours · Difficulty 3 · Module M06 · Outcomes LO-10, LO-11, LO-28**

## Why this lab exists

A backdoor is a conditional failure. The model performs normally on ordinary inputs and misbehaves when a specific pattern appears. That makes it harder to see than ordinary poisoning: clean test accuracy can be almost unchanged, and a user who never types the trigger never notices.

This lab uses a 16-feature tabular classifier. The trigger sets three features to a constant value, and 8% of the training rows are relabeled. You will measure clean accuracy, attack success rate (ASR), and the false-trigger rate on a clean model, then screen the training data for the trigger and retrain. The defense works here because the trigger is a visible, extreme value — a fact the report must generalize carefully, not broadly.

## The system and the threat model

| Element | Assumption |
|---|---|
| Target | Binary logistic regression on 16 numerical features |
| Attacker goal | Targeted integrity: any input carrying the trigger is classified as class 1 |
| Attacker knowledge | Knows the feature schema and can insert rows into the training set |
| Capability | Insert 67 rows (8% of 840 training rows) with the trigger and label 1 |
| Constraint | The attacker cannot change the test set or the model code |
| Metrics | Clean test accuracy, ASR on triggered class-0 rows, false-trigger rate on clean inputs |
| Defender | Can screen training rows for extreme values before fitting |
| Lifecycle stage | Data collection / training / artifact |

The trigger is deliberately crude — three features set to 3.0 standard deviations — so that detection is possible and the geometry is easy to see. A stealthier trigger is discussed in Lesson 3 and is not solved by this screen.

## What you produce

`metrics.json` with `clean`, `backdoored`, and `defended` blocks (`clean_accuracy`, `attack_success_rate`, `clean_source_target_rate`), plus `poison_count`, `poison_rate`, and a `screening` block (`flagged`, `poison_caught`, `threshold`). Write `run.json`, `report.md`, and `manifest.json`.

## Prerequisites

- LAB-05 or LAB-06.
- Module 06 Lessons 1–2.
- You can explain the difference between a backdoor and indiscriminate poisoning.

## Environment

```bash
cd labs/lab-07-tabular-backdoor
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab07.py --artifacts artifacts
```

Python 3.14.7, NumPy, scikit-learn. Three logistic-regression fits; a few seconds.

## Data and safety

Synthetic tabular data generated from seed 11. No personal data. The poisoned rows are synthetic additions you create. No external service is involved.

## Task specification

1. **Generate the data.** 1,200 rows, 16 standard-normal features. The label depends on features 0, 1, and 2 plus noise. Shuffle with seed 11 and split 840/360.
2. **Define the trigger.** Set features 10, 11, and 12 to 3.0. This is the only trigger definition.
3. **Poison.** Take the first `round(0.08 × 840) = 67` class-0 training rows, apply the trigger, and append them with label 1. Do not modify the originals.
4. **Train three models.** Clean, backdoored, and screened-and-retrained. Fit `LogisticRegression(max_iter=2000)` each time.
5. **Measure.** Clean accuracy on the test set. ASR on triggered test rows whose true label is 0. Clean-source target rate: how often the model predicts 1 on *untriggered* class-0 test rows.
6. **Screen.** Flag any row with features 10–12 above 2.5. Report flagged, caught, and the threshold.
7. **Report.** Include the trigger definition, the three-state table, an explanation of why accuracy is nearly unchanged, and at least four limitations.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `add_trigger` | Copy the input and set the three trigger features |
| `starter.py` | TODO 2 | `poison` | Append triggered class-0 rows labeled class 1 |
| `starter.py` | TODO 3 | `screen` | Flag rows that contain the known trigger |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-07-tabular-backdoor/CHECKING.md`.

## Expected outputs

| State | Clean accuracy | ASR | Clean-source target rate |
|---|---:|---:|---:|
| Clean | 0.8444 | 0.1771 | 0.1829 |
| Backdoored | 0.8306 | 0.8571 | 0.2057 |
| Defended | 0.8389 | 0.1543 | 0.1829 |

Poison count: 67 (7.98% of training). Screening flagged 82 rows and caught all 67 poisons.

Read the clean-model ASR carefully. A clean model already sends 17.7% of triggered class-0 rows to class 1, because the trigger values are unusual but not impossible and the base rates differ. ASR is therefore an *increase* over a baseline, not an absolute. The report must state the baseline.

The defended ASR (0.1543) is *below* the clean baseline (0.1771), which is noise from removing rows, not evidence that screening makes the model robust in general.

## Deliverables checklist

- [ ] `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] Clean accuracy, trigger ASR, and clean false-trigger rate for the poisoned model and the screened retrain.
- [ ] `report.md` answers every reflection question.
- [ ] `python check_lab07.py --artifacts artifacts` exits 0.

## Success criteria

- [ ] Poison count is 67 and poison rate is reported against the training set.
- [ ] Clean accuracy drop from backdooring is at most 0.05.
- [ ] Backdoored ASR is at least 0.75.
- [ ] Clean and defended ASR are at most 0.25.
- [ ] Screening catches all 67 poisons and reports the flag count.
- [ ] The report states the trigger, the baseline, the screening rule, and its limitations.
- [ ] `python check_lab07.py --artifacts artifacts` exits 0.

## How to check yourself

From `labs/lab-07-tabular-backdoor/`:

```bash
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab07.py --artifacts artifacts
```

Exit code 0 means the checker independently reproduced the reference artifacts and metrics within tolerance. Complete `starter.py` and run the same checker on your own artifacts. `CHECKING.md` lists the exact checks and common failure modes.

## Rubric (20 points)

| Item | Points |
|---|---:|
| Correct trigger and poisoning | 4 |
| Three-state measurement | 4 |
| ASR baseline discipline | 4 |
| Screening and retraining | 4 |
| Explanation of stealth | 2 |
| Limitations and reproducibility | 2 |

## Reflection questions

1. Why is the clean accuracy drop so small?
2. The clean model already fires on 17.7% of triggered rows. Why does that matter for how you report ASR?
3. What trigger design would survive the `> 2.5` screening rule?
4. If the attacker poisoned only 1% of rows, what would you expect to change?
5. Would a model trained with robust loss or outlier removal necessarily remove this backdoor? What evidence would you need?

## Hints

1. A trigger is a fixed pattern on named features. `add_trigger` should copy the input and set those features, not mutate the caller's array.
2. Poison by appending triggered copies of class-0 rows with label 1; keep the original clean rows.
3. Clean false-trigger rate is measured on clean class-0 test rows. It is a separate metric from attack success.
4. Screen by the known trigger, retrain on the filtered set, and compare with the poisoned model.

## Time box

| Hour | Work |
|---|---|
| 1 | Data, trigger, clean model |
| 2 | Poison and backdoored model |
| 3 | Screening, retrain, measurements |
| 4 | Report and reflection |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| ASR near zero | Trigger applied to test labels but not model inputs | Apply the trigger to the input array |
| ASR is 1.0 | Training labels copied into the triggered test set | Evaluate on triggered **test** rows |
| Screening flags everything | Threshold on raw feature scale confused with trigger value | Flag `> 2.5` in features 10–12 |
| Poison count 68 | `ceil` instead of `round` | Use `int(round(0.08 * 840))` |
| Defended model still backdoored | Screening applied to the wrong columns | Use columns 10, 11, 12 |

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
- [References](../references.md) — R-31, R-32, R-34
- [Module page](../modules/m06-backdoors/index.md) — M06 — Backdoor Attacks, Trojan Models, and Trigger-Based Behavior
- Package checking guide: `labs/lab-07-tabular-backdoor/CHECKING.md`

## What comes next

[LAB-08](lab-08.md) moves the same idea into image space, where the trigger is a 2×2 patch and the defender does not know where it is. You will search all 49 positions and then filter the rows that carry the winning patch.
