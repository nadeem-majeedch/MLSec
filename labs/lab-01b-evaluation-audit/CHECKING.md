# Checking Guide — LAB-01B

This guide lets a learner check the lab without an instructor. It states the expected results, what the checker verifies, and how to diagnose common failures.

## Expected results

| Item | Expected |
|---|---|
| Dataset | `mlsec_labs.make_churn_dataset(seed=42)`, 2040 rows, 1700 customers, churn rate 0.223 |
| Duplicate rows | 39 exact duplicates |
| Missing values | 80 missing `monthly_spend` |
| Suspect feature | `late_fee_flag`, univariate ROC-AUC 0.899, label agreement 0.907 |
| Random-split overlap | 122 customers on both sides of a 75/25 row split |
| Leaky baseline | ROC-AUC 0.9459, accuracy 0.9275 at 0.5 |
| Repaired split | 1200 train / 392 validation / 409 test rows; 1020 + 340 + 340 customers |
| Repair threshold | 0.3427 (80th percentile of validation scores) |
| Repaired test | accuracy 0.7628, precision 0.4333, recall 0.4588, F1 0.4457, ROC-AUC 0.7076, PR-AUC 0.3983 |
| Bootstrap 95% | recall [0.356, 0.562], precision [0.333, 0.540] |
| Grouped 5-fold PR-AUC | 0.4175 ± 0.0374 |

A small metric difference (about ±0.005) is acceptable across library versions. The checker recomputes metrics from the saved model and split and requires them to match `metrics.json` exactly, and also enforces coarse performance bands. Exact counts (duplicates, missing values, split sizes) must match.

## How to check

From `labs/lab-01b-evaluation-audit/`:

```bash
python solution.py --out artifacts
python check_lab01b.py --artifacts artifacts
```

For a student artifact:

```bash
python starter.py --out artifacts
python check_lab01b.py --artifacts artifacts
```

`check_lab01b.py` exits 0 only if every check passes.

## What the checker verifies

1. **Manifest integrity.** `manifest.json` covers `data.csv`, `model.joblib`, `splits.npz`, `metrics.json`, and `run.json`; every file exists and its SHA-256 matches.
2. **Dataset determinism.** Regenerating the dataset with `seed=42` reproduces `data.csv` byte for byte, and `metrics.json` records the same hash.
3. **Grouped split.** Row indices are in range and unique, the three splits do not overlap, and customer ID sets are disjoint. Every test row's customer appears in the saved test customer list.
4. **Audit findings.** Duplicate rows fall in 30–50, missing values equal 80, the suspect feature's univariate AUC falls in 0.85–0.95, and the random-split overlap is at least 80.
5. **Leak removal.** `late_fee_flag` is absent from the repaired feature list.
6. **Metric reproducibility.** Loading `model.joblib` and predicting on the saved test rows reproduces accuracy, precision, recall, F1, ROC-AUC, and PR-AUC in `metrics.json` exactly.
7. **Threshold rule.** The threshold equals the 80th percentile of validation scores.
8. **Expected performance.** Repaired ROC-AUC is 0.65–0.76, PR-AUC 0.35–0.46, recall 0.40–0.52; the leaky AUC is at least 0.92 and exceeds the repaired AUC by at least 0.15.
9. **Grouped CV.** Mean grouped 5-fold PR-AUC falls in 0.30–0.55.
10. **Metadata and report.** `run.json` records the Python version, and `report.md` contains the five required headings.

## Diagnosing failures

| Message | Likely cause | Fix |
|---|---|---|
| `missing artifacts/model.joblib` | Artifacts were written elsewhere | Pass `--out` and `--artifacts` with the same directory |
| `data.csv does not match the deterministic generator output` | Dataset was regenerated with a different seed | Use `make_churn_dataset(seed=42)` or `python make_dataset.py` |
| `customer IDs overlap across splits` | Rows were split, not customers | Group by `customer_id` before splitting |
| `late_fee_flag is still in the repaired feature list` | The leak was not removed | Drop the post-outcome feature before fitting |
| `threshold is not the 80th percentile ...` | Threshold chosen on test data or hard-coded | Compute it from validation scores only |
| `repaired roc_auc mismatch` | Saved metric came from a different model or split | Recompute metrics from the loaded model and saved rows |
| `leaky and repaired AUCs are too close` | The leak or the preprocessing leak was not reproduced | Fit the imputer and scaler on all rows and keep `late_fee_flag` in the baseline only |
| `report is missing heading` | Template headings were removed or renamed | Keep the five headings from `report_template.md` |

## What to look for in the report

| Criterion | Strong work | Weak work |
|---|---|---|
| Threat model | Names metric integrity and a concrete validity failure | Generic "data quality matters" text |
| Data audit | Reports counts and the suspect feature's AUC and availability | Lists problems without numbers |
| Results | Puts the leaky and repaired estimates side by side | Reports only the repaired number |
| Uncertainty | Reports bootstrap intervals and grouped CV spread | One point estimate, no denominator |
| Limitations | Says the repaired model is a baseline and the data is synthetic | Claims deployment readiness |

## Integrity notes

- A passing checker means the artifacts are internally consistent and in the expected range. It does not prove the report's reasoning is good; use the rubric in `docs/labs/lab-01b.md`.
- The repaired score (about 0.71 AUC) is deliberately lower than the leaky score (about 0.95). A lower number here is the honest one. Do not "fix" the gap by restoring the leak.
- If you change the model or split on purpose, update `expected_metrics.json` and the checker bands, and record the change in the report. Do not edit only the expected file to make a failing run pass.
- The checker never downloads data or contacts the network.

## Rubric

| Criterion | Weight | What strong work looks like |
|---|---:|---|
| Technical correctness | 30 | Correct audit, leak reproduction, repair, threshold, and metrics |
| Security reasoning | 25 | Explains each leak in terms of availability at scoring time and information flow |
| Experimental method | 20 | Same folds and classifier for both arms; uncertainty reported |
| Reproducibility | 15 | Dataset hash, saved splits, manifest, one-command rerun |
| Communication and ethics | 10 | Lower repaired score presented as more trustworthy, not as a failure |

## Reflection questions

1. How much of the gap between the leaky and repaired scores is explained by each individual repair?
2. Why is the grouped split the right unit here, and when would a random row split be acceptable?
3. What does the bootstrap interval say, and what does it not say about future performance?
4. Which result would you present to a decision-maker, and what caveat must accompany it?
