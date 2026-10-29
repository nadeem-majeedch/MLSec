# Checking Guide — LAB-01

This guide lets a learner check the lab without an instructor. It states the expected results, what the checker verifies, and how to diagnose common failures.

## Expected results

| Item | Expected |
|---|---|
| Dataset | scikit-learn `load_digits`, 1797 samples, 64 features, 10 classes |
| Split | 1077 train / 360 validation / 360 test, stratified, seed 42 |
| Model | `StandardScaler` + `LogisticRegression(max_iter=2000, random_state=42)` |
| Validation accuracy | 0.9722 |
| Validation macro F1 | 0.9724 |
| Test accuracy | 0.9583 |
| Test macro F1 | 0.9577 |

A small difference (about ±0.005) is acceptable across library versions. The checker requires the saved `metrics.json` to match a recomputation from the saved model and split exactly, and it requires the headline accuracy and macro F1 to fall in 0.94–0.975.

## How to check

From `labs/lab-01-environment/`:

```bash
python solution.py --out artifacts
python check_lab01.py --artifacts artifacts
```

For a student artifact:

```bash
python starter.py --out artifacts
python check_lab01.py --artifacts artifacts
```

`check_lab01.py` exits 0 only if every check passes.

## What the checker verifies

1. **Manifest integrity.** `manifest.json` lists `model.joblib`, `splits.npz`, `metrics.json`, and `run.json`; each file exists, and its size and SHA-256 match.
2. **Split integrity.** The three index arrays cover every row once, have no duplicates, do not overlap, and have sizes 1077/360/360.
3. **Metric reproducibility.** Loading `model.joblib` and predicting on the saved test indices reproduces the accuracy, macro F1, and confusion matrix in `metrics.json` exactly.
4. **Expected performance.** Test accuracy and macro F1 are inside 0.94–0.975. This catches an untrained model, a broken pipeline, or an accidental evaluation on training data.
5. **Metadata.** The split seed is 42, and `run.json` records the Python version.
6. **Report.** `report.md` contains the five required headings.

## Diagnosing failures

| Message | Likely cause | Fix |
|---|---|---|
| `missing artifacts/model.joblib` | Artifacts were written elsewhere | Pass `--out` and `--artifacts` with the same directory |
| `manifest does not cover ...` | Manifest was built before the last write | Rebuild the manifest after writing every artifact |
| `hash mismatch` | An artifact changed after the manifest was written | Do not edit artifacts by hand; rerun the script |
| `split indices overlap` | Indices were generated independently for each split | Split indices once, then index the arrays |
| `split sizes ... != ...` | Different split ratios or an unstratified split | Use the specified 60/20/20 stratified protocol |
| `test accuracy mismatch` | The saved metric came from a different model or split | Recompute metrics from the loaded model and saved indices |
| `accuracy outside ... band` | Pipeline is missing the scaler, or was fit on test data | Fit on train only; check the estimator |
| `report is missing heading` | Template headings were removed or renamed | Keep the five headings from `report_template.md` |

## What to look for in the report

| Criterion | Strong work | Weak work |
|---|---|---|
| Threat model | Names the asset (metric integrity) and a concrete failure | Generic "security is important" text |
| Setup | States split sizes, seed, model, versions | Omits the split or seed |
| Results | Reports validation and test together | Reports only the best number |
| Limitations | Notes that the split is random and the data is clean | Claims the model is production-ready |
| Reproduction | Gives commands and explains the manifest | Says "run the notebook" without a command |

## Integrity notes

- A passing checker means the artifact is internally consistent and in the expected range. It does not prove the report's reasoning is good; use the rubric in `docs/labs/lab-01.md`.
- If you change the model or split on purpose, update `expected_metrics.json` and the checker band, and record the change in the report. Do not edit only the expected file to make a failing run pass.
- The checker never downloads data or contacts the network.

## Rubric

| Criterion | Weight | What strong work looks like |
|---|---:|---|
| Technical correctness | 30 | Correct split, pipeline, metrics, and reload |
| Security reasoning | 25 | Threat model names metric integrity and a concrete failure |
| Experimental method | 20 | Validation and test reported together; limitations stated |
| Reproducibility | 15 | Saved indices, pinned versions, manifest, one-command rerun |
| Communication and ethics | 10 | Report is concise, accurate, and makes no deployment claim |

## Reflection questions

1. Which part of the run record would let another person reconstruct your split exactly?
2. Why is the test set touched once, and what would change if you tuned on it?
3. What does the manifest prove, and what does it not prove about the model?
4. If accuracy differed by 0.01 on another machine, what would you check first?
