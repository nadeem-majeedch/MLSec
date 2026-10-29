# LAB-01 — Reproducible Environment and Baseline Pipeline

**Tier A · 3 hours · Difficulty 1 · Modules M00–M01 · Outcomes LO-01, LO-28**

## Why this lab exists

Every later lab attacks, defends, or audits a model. If the baseline cannot be rebuilt, every later number is unverifiable. This lab builds the smallest complete ML artifact: a split that is saved, a pipeline that cannot leak, metrics with stated definitions, and a manifest that lets a second person reproduce the run.

You do not need to be a security specialist. You need to be able to answer one question: *can another person rebuild this exact evaluation?*

## Threat model, scope, and safety

This is a reproducibility and hygiene lab, not an attack. The threat is an unreproducible result: a split that cannot be reconstructed, a model with no environment record, or an artifact set with no manifest. The assets are the training data, the fitted pipeline, and the performance claim. The actor is a future maintainer or reviewer, not a remote adversary. Success is a clean rerun on another CPU machine.

All data is the bundled scikit-learn digits set. No network access is required, no private data is used, and no external service is contacted. Do not substitute a private dataset for this lab; the point is to practice the evidence chain on data you can freely redistribute.

## What you build

A digit classifier with:

- a fixed, saved 60/20/20 stratified split;
- a `StandardScaler` + logistic-regression pipeline fitted on training rows only;
- accuracy, macro F1, per-class recall, and a confusion matrix on validation and test;
- a saved model, split indices, metrics, run metadata, manifest, and report.

## Prerequisites

| Skill | Check |
|---|---|
| Run a Python script from a terminal | `python --version` works |
| Install packages from a requirements file | `python -m pip install -r requirements.txt` works |
| Read a confusion matrix | You can explain TP, FP, FN, TN |
| Use a train/validation/test split | You can explain why the test set is touched once |

If any check fails, complete Module 01 Lessons 1–5 first.

## Data and environment

- **Data:** scikit-learn `load_digits` — 1797 handwritten digits, 64 features, 10 classes. It ships with scikit-learn; there is no download, no personal data, and no license trap.
- **Environment:** Python 3.14.7 with `numpy==2.5.2`, `pandas==3.0.5`, `scikit-learn==1.9.0`, `joblib==1.5.3`, `PyYAML==6.0.3`. The lab folder's `requirements.txt` installs the shared Level 1 stack.
- **Compute:** CPU only. A full run takes a few seconds.
- **Safety:** no network access is required. The lab does not contact any external service.

## Task specification

Work in the repository's `labs/lab-01-environment/` folder.

1. **Split once, save the indices.** Use a 60/20/20 stratified split with `random_state=42`. Save the actual row indices for train, validation, and test. Do not rely on the seed alone; the indices are the contract.
2. **Build a pipeline.** Use `StandardScaler` followed by `LogisticRegression(max_iter=2000, random_state=42)`. Fit it on training rows only. Do not scale the full dataset first.
3. **Evaluate twice.** Report validation and test accuracy, macro F1, per-class recall, and the test confusion matrix. State the unit of prediction (one image, one label).
4. **Persist the artifact.** Save `model.joblib`, `splits.npz`, `metrics.json`, and `run.json`. Record the seed, Python version, and package versions.
5. **Write the manifest.** Hash every artifact with SHA-256 and record its size.
6. **Write the report.** Use the five headings in `report_template.md`: Threat model, Setup, Results, Limitations, Reproduction.
7. **Prove reload.** Load the saved model in a fresh process and reproduce the test metrics. The checker does this automatically.

Starter code is `starter.py`. It contains three TODO blocks: build the model, write the artifacts, and write the report. The reference implementation is `solution.py`; do not read it until you have a first attempt.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `build_model` | Return a `Pipeline` with scaling and logistic regression, unfitted |
| `starter.py` | TODO 2 | `write_artifacts` | Write the model, split indices, metrics, run record, and manifest |
| `starter.py` | TODO 3 | `write_report` | Write `report.md` with the five required headings |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-01-environment/CHECKING.md`.

## Deliverables checklist

| File | Contents |
|---|---|
| `model.joblib` | Fitted pipeline |
| `splits.npz` | Train, validation, and test row indices |
| `metrics.json` | Validation and test metrics |
| `run.json` | Seed, command, Python, and package versions |
| `manifest.json` | SHA-256 and size for each artifact |
| `report.md` | Five-section report |

- [ ] `artifacts/model.joblib`, `splits.npz`, `metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] `report.md` answers every reflection question.
- [ ] `python check_lab01.py --artifacts artifacts` exits 0.

## Expected results

| Item | Expected |
|---|---|
| Split sizes | 1077 train / 360 validation / 360 test |
| Validation accuracy | 0.9722 |
| Validation macro F1 | 0.9724 |
| Test accuracy | 0.9583 |
| Test macro F1 | 0.9577 |

A difference of about ±0.005 is acceptable across library versions. The checker requires the saved metrics to match a recomputation exactly and the headline scores to fall in 0.94–0.975.

## Success criteria

- [ ] The three index arrays cover every row once, do not overlap, and have sizes 1077/360/360.
- [ ] The scaler is inside the pipeline and is fitted on training rows only.
- [ ] Reloading the model reproduces the saved test metrics exactly.
- [ ] `manifest.json` hashes match the files on disk.
- [ ] `run.json` records seed 42, Python 3.14.7, and the package versions.
- [ ] The report states a limitation of the random split and does not claim production readiness.
- [ ] `python check_lab01.py --artifacts artifacts` exits 0.

## How to check yourself

From `labs/lab-01-environment/`:

```bash
python -m pip install -r requirements.txt
python starter.py --out artifacts
python check_lab01.py --artifacts artifacts
```

The checker prints one PASS line per check and exits nonzero on the first failure. The failure table in `CHECKING.md` explains each message.

## Reflection questions

1. Which part of the run record would let another person reconstruct your split exactly?
2. Why is the test set touched once, and what would change if you tuned on it?
3. What does the manifest prove, and what does it not prove about the model?
4. If accuracy differed by 0.01 on another machine, what would you check first?

## Hints

1. Build the pipeline as two named steps: a scaler and a classifier. Fit it once on the training split; fitting the scaler on test rows leaks the test distribution.
2. Write `metrics.json`, `run.json`, and `report.md` before you build the manifest. A manifest created early will omit files that did not exist yet.
3. `splits.npz` should let another person reconstruct the exact train, validation, and test rows without rerunning your split.
4. If the checker reproduces a different accuracy, compare your split indices and `random_state` before changing the model.

## Time box

| Time | Work |
|---|---|
| 0:00–0:30 | Environment, data inspection, split |
| 0:30–1:30 | Pipeline, training, metrics |
| 1:30–2:15 | Artifacts, manifest, report |
| 2:15–3:00 | Run the checker, fix failures, reread the report |

If you pass 4.5 hours, stop and submit with a note on what is incomplete.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Accuracy near 0.10 | Labels and predictions misaligned | Check that the split returns `X` and `y` in the same order |
| Accuracy exactly 1.0 | Evaluating on training rows | Evaluate on the saved test indices |
| `FileNotFoundError` for an artifact | Checker and solution wrote to different folders | Pass the same `--out` and `--artifacts` path |
| Hash mismatch | Manifest written before the last artifact | Write all artifacts, then build the manifest |
| Different metrics on rerun | Unseeded split or estimator | Pass `random_state=42` everywhere |

## Rubric

| Criterion | Weight | What strong work looks like |
|---|---:|---|
| Technical correctness | 30 | Correct split, pipeline, metrics, and reload |
| Security reasoning | 25 | Threat model names metric integrity and a concrete failure |
| Experimental method | 20 | Validation and test reported together; limitations stated |
| Reproducibility | 15 | Saved indices, pinned versions, manifest, one-command rerun |
| Communication and ethics | 10 | Report is concise, accurate, and makes no deployment claim |

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
- [References](../references.md) — R-100, F-05
- [Module page](../modules/m01-python-refresher/index.md) — M01 — Python, NumPy, pandas, and scikit-learn
- Package checking guide: `labs/lab-01-environment/CHECKING.md`

## What comes next

LAB-01B takes a deliberately leaky churn pipeline and repairs it. You will use the same artifact discipline to show why a lower, reproducible score is more trustworthy than an inflated one.
