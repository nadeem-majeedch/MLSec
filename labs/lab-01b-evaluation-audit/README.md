# LAB-01B — Evaluation Audit and Honest Baseline

| Field | Value |
|---|---|
| Lab ID | LAB-01B |
| Tier | A |
| Time | 4 hours |
| Difficulty | 2 of 4 |
| Module | M02 — Machine Learning Fundamentals |
| Outcomes | LO-01, LO-28 |
| Prerequisites | LAB-01 or equivalent; M02 lessons 1–4 |
| Data | synthetic churn data |
| Compute | CPU only; a few seconds |

Full brief: [docs/labs/lab-01b.md](../../docs/labs/lab-01b.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

You are handed a churn dataset and a colleague's optimistic claim. You audit the data, reproduce the inflation, and repair the protocol:

1. Count duplicate rows, missing values, and customers that leak across a random split.
2. Reproduce a leaky baseline: random row split, preprocessing fitted on all rows, and a post-outcome feature left in.
3. Repair it: deduplicate, split by customer, remove the leaked feature, fit preprocessing on training rows only, and choose the threshold from validation scores.
4. Report the two estimates side by side, with bootstrap intervals and grouped cross-validation.

The repaired score is **lower** than the leaky one. That is the point: a smaller, reproducible number is more useful than an inflated one.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

python make_dataset.py --out artifacts
# reference path
python solution.py --out artifacts
python check_lab01b.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab01b.py --artifacts artifacts
```

## What you produce

- `artifacts/data.csv`, `model.joblib`, `splits.npz`, `metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- `report.md` states the leaky and repaired estimates side by side, with intervals.
- `report.md` answers every reflection question.
- `python check_lab01b.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `audit` | Count duplicates, missing values, leakage, and customer overlap |
| `starter.py` | TODO 2 | `leaky_baseline` | Reproduce the inflated dashboard result |
| `starter.py` | TODO 3 | `repair` | Deduplicate, drop the post-outcome feature, split by customer, fit inside a pipeline |

## Hints

- Reproduce the leaky number before repairing anything. You need both estimates from the same data to make the comparison honest.
- A random row split leaks customers across folds; the unit of prediction here is the customer, so split by `customer_id`.
- Fit preprocessing inside the pipeline after the split. A scaler fitted on all rows has already seen the test distribution.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab01b.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `make_dataset.py` | Deterministic fixture generator |
| `report_template.md` | Report headings and prompts |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
