# LAB-01B — Evaluation Audit and Honest Baseline

**Tier A · 4 hours · Difficulty 2 · Module M02 · Outcomes LO-01, LO-28**

## Why this lab exists

A colleague reports 94% ROC-AUC on a churn model. The number is real, in the sense that the code produced it. It is also inflated by three ordinary mistakes: the same customers appear in training and test, the scaler was fitted on all rows, and a feature written when an account closes was used to predict the closure.

This lab reproduces the inflation, removes it, and reports both numbers. The repaired score is **lower**. That is the lesson: an honest estimate you can reproduce is worth more than a high estimate you cannot.

## Threat model, scope, and safety

The system is a churn model trained by a colleague. The threat is evaluation leakage, not an external attacker: duplicate customers, preprocessing fitted on all rows, and a post-outcome feature inflate the reported score. The asset is the validity of the performance claim; the actor is a well-meaning analyst under delivery pressure. Success is a repaired protocol whose estimate is lower, reproducible, and honestly reported.

The dataset is synthetic and generated locally by `labs/shared/mlsec_labs/data.py`. It contains no real customers and no personal data. Do not substitute a real customer extract; if you adapt the protocol to one, do it under an approved data-handling agreement outside this repository.

## What you build

A complete audit of a synthetic churn dataset, then two comparable evaluations:

1. **Leaky baseline:** random row split, imputer and scaler fitted on all rows, post-outcome feature included.
2. **Repaired baseline:** duplicate removal, customer-grouped 60/20/20 split, leak removed, preprocessing fitted on training rows only, threshold chosen from validation scores.

You also report bootstrap intervals and grouped cross-validation so the point estimate is not mistaken for certainty.

## Data

The dataset is generated locally by `labs/shared/mlsec_labs/data.py`:

| Property | Value |
|---|---|
| Name | `make_churn_dataset(seed=42)` |
| Rows | 2040 |
| Unique customers | 1700 |
| Churn rate | 0.223 |
| Duplicate rows | 39 |
| Missing `monthly_spend` | 80 |
| Columns | 12 features plus `customer_id` and `churned` |

It is synthetic. It contains no real people, no personal data, and no external source. Regenerating it with seed 42 reproduces the CSV byte for byte.

## Prerequisites

- LAB-01 (or equivalent): saved splits, pipeline, metrics, manifest.
- Module 02 Lessons 1–4: unit of prediction, leakage families, precision/recall, ROC-AUC vs PR-AUC, grouped splits.
- You can explain why a random row split is wrong when a customer can have several rows.

## Environment

```bash
cd labs/lab-01b-evaluation-audit
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python make_dataset.py --out artifacts
```

- Python 3.14.7 with the shared Level 1 stack (`numpy==2.5.2`, `pandas==3.0.5`, `scikit-learn==1.9.0`, `joblib==1.5.3`, `PyYAML==6.0.3`).
- CPU only; the reference run takes a few seconds.
- The dataset is generated locally; no network access is required.

## Task specification

Work in `labs/lab-01b-evaluation-audit/`.

1. **Audit before modeling.**
   - Print shape, dtypes, and missing-value counts.
   - Count exact duplicate rows and identify the duplicated customer.
   - For each candidate feature, compute univariate ROC-AUC against the label. Flag any feature that would not be available at scoring time.
   - Show how many customers appear on both sides of a random 75/25 row split.
2. **Reproduce the leaky baseline.**
   - Random row split 75/25 with `random_state=42`.
   - Fit the imputer and scaler on all rows.
   - Keep the post-outcome feature.
   - Report accuracy, precision, recall, F1, ROC-AUC, and PR-AUC at threshold 0.5 and at the top-20% operating point.
3. **Repair the protocol.**
   - Drop exact duplicates.
   - Split by customer into 60/20/20, stratified on churn.
   - Remove `late_fee_flag`.
   - Put median imputation, scaling, and logistic regression in one pipeline fitted on training rows.
   - Choose the threshold as the 80th percentile of validation scores (an assumed 20% review capacity).
4. **Report uncertainty.**
   - Bootstrap 95% intervals for precision and recall on the test set.
   - Grouped 5-fold cross-validation PR-AUC.
5. **Write the report** with the five headings in `report_template.md`.

Starter code is `starter.py` with three TODO functions: `audit`, `leaky_baseline`, and `repair`. The reference is `solution.py`.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `audit` | Count duplicates, missing values, leakage, and customer overlap |
| `starter.py` | TODO 2 | `leaky_baseline` | Reproduce the inflated dashboard result |
| `starter.py` | TODO 3 | `repair` | Deduplicate, drop the post-outcome feature, split by customer, fit inside a pipeline |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-01b-evaluation-audit/CHECKING.md`.

## Deliverables checklist

`data.csv`, `model.joblib`, `splits.npz`, `metrics.json`, `run.json`, `manifest.json`, and `report.md`.

The split file stores row indices and customer IDs. The manifest hashes every artifact. The report must state the leaky and repaired estimates side by side.

- [ ] `artifacts/data.csv`, `model.joblib`, `splits.npz`, `metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] `report.md` states the leaky and repaired estimates side by side, with intervals.
- [ ] `report.md` answers every reflection question.
- [ ] `python check_lab01b.py --artifacts artifacts` exits 0.

## Expected results

| Item | Expected |
|---|---|
| Duplicate rows | 39 |
| Missing `monthly_spend` | 80 |
| `late_fee_flag` univariate AUC | 0.899 |
| `late_fee_flag` label agreement | 0.907 |
| Random-split customer overlap | 122 |
| Leaky baseline ROC-AUC | 0.9459 |
| Leaky baseline accuracy at 0.5 | 0.9275 |
| Repaired split rows | 1200 / 392 / 409 |
| Repaired split customers | 1020 / 340 / 340 |
| Repaired threshold | 0.3427 |
| Repaired test accuracy | 0.7628 |
| Repaired precision | 0.4333 |
| Repaired recall | 0.4588 |
| Repaired F1 | 0.4457 |
| Repaired ROC-AUC | 0.7076 |
| Repaired PR-AUC | 0.3983 |
| Bootstrap 95% recall | [0.356, 0.562] |
| Bootstrap 95% precision | [0.333, 0.540] |
| Grouped 5-fold PR-AUC | 0.4175 ± 0.0374 |

A metric difference of about ±0.005 is acceptable across library versions. Counts and split sizes must match exactly.

## Success criteria

- [ ] The audit reports counts, not adjectives: duplicates, missing values, overlap, and the suspect feature's AUC.
- [ ] The leaky baseline is reproduced with the leak and the preprocessing leak intact.
- [ ] The repaired baseline removes the leak, groups by customer, and fits preprocessing on training rows only.
- [ ] The threshold is the 80th percentile of validation scores, not tuned on test.
- [ ] The report puts both estimates side by side and does not claim the repaired model is "worse."
- [ ] Bootstrap intervals and grouped CV are reported.
- [ ] The report states that the data is synthetic and the model is a baseline.
- [ ] `python check_lab01b.py --artifacts artifacts` exits 0.

## How to check yourself

From `labs/lab-01b-evaluation-audit/`:

```bash
python -m pip install -r requirements.txt
python make_dataset.py --out artifacts
python starter.py --out artifacts
python check_lab01b.py --artifacts artifacts
```

The checker rebuilds the dataset, verifies the manifest, checks that customer groups do not overlap, recomputes metrics from the saved model, and confirms the threshold rule. The failure table is in `CHECKING.md`.

## Reflection questions

1. How much of the gap between the leaky and repaired scores is explained by each individual repair?
2. Why is the grouped split the right unit here, and when would a random row split be acceptable?
3. What does the bootstrap interval say, and what does it not say about future performance?
4. Which result would you present to a decision-maker, and what caveat must accompany it?

## Hints

1. Reproduce the leaky number before repairing anything. You need both estimates from the same data to make the comparison honest.
2. A random row split leaks customers across folds; the unit of prediction here is the customer, so split by `customer_id`.
3. Fit preprocessing inside the pipeline after the split. A scaler fitted on all rows has already seen the test distribution.
4. Bootstrap the difference between the two estimates, not only each score. If the intervals overlap heavily, say so.

## Time box

| Time | Work |
|---|---|
| 0:00–0:45 | Data audit and leak screening |
| 0:45–1:45 | Leaky baseline |
| 1:45–3:00 | Repair: deduplicate, group split, pipeline, threshold |
| 3:00–3:45 | Bootstrap, grouped CV, report |
| 3:45–4:00 | Run the checker and fix failures |

If you pass 6 hours, stop and submit with a note on what is incomplete. Do not restore the leak to make the number look better.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Repaired AUC near 0.94 | The leak is still present | Remove `late_fee_flag` and fit preprocessing on train only |
| `customer IDs overlap across splits` | Rows were split, not customers | Split unique customer IDs, then select rows |
| Threshold near 0.5 | Threshold was hard-coded | Use `np.quantile(val_scores, 0.80)` |
| Recall near 0.86 in the repaired model | You are reading the leaky metrics | Report the repaired block separately |
| `data.csv does not match ...` | Dataset regenerated with another seed | Use seed 42 |
| Bootstrap interval is very wide | Test set is small (409 rows) | That is expected; report it, do not hide it |

## Rubric

| Criterion | Weight | What strong work looks like |
|---|---:|---|
| Technical correctness | 30 | Correct audit, leak reproduction, repair, threshold, and metrics |
| Security reasoning | 25 | Explains each leak in terms of availability at scoring time and information flow |
| Experimental method | 20 | Same folds and classifier for both arms; uncertainty reported |
| Reproducibility | 15 | Dataset hash, saved splits, manifest, one-command rerun |
| Communication and ethics | 10 | Lower repaired score presented as more trustworthy, not as a failure |

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
- [References](../references.md) — R-101, R-06, R-05
- [Module page](../modules/m02-ml-fundamentals/index.md) — M02 — Machine Learning Fundamentals and Evaluation
- Package checking guide: `labs/lab-01b-evaluation-audit/CHECKING.md`

## What comes next

Module 03 turns this habit into a full threat model. Instead of asking "is this metric inflated?", you will ask "which adversary, with what access, would cause which harm, and what evidence would tell us it happened?"
