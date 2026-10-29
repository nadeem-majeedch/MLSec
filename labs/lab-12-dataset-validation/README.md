# LAB-12 — Dataset Validation and Leakage Audit

| Field | Value |
|---|---|
| Lab ID | LAB-12 |
| Tier | A |
| Time | 4 hours |
| Difficulty | 3 of 4 |
| Module | M09 — Data Integrity |
| Outcomes | LO-20, LO-30 (supporting), LO-28 |
| Prerequisites | M01 lesson 3; M02 lesson 3; M09 lessons 1–3 |
| Data | synthetic customer extract |
| Compute | CPU only; seconds |

Full brief: [docs/labs/lab-12.md](../../docs/labs/lab-12.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

A churn model is about to be trained on a customer extract. The extract has
passed no validation gates. It contains missing values, impossible ranges, an
unknown plan value, exact duplicates, contradictory labels, implausible churn
labels, duplicate customer records, and one column that is only observed after
the outcome: `exit_survey`.

You build two things:

1. A validation report that names and counts every defect, including customers
   that appear on both sides of a naive random split.
2. A repair pipeline that drops, imputes, quarantines, and de-duplicates, then
   removes the post-outcome column.

Finally you measure the damage. The leaky pipeline reaches ROC-AUC 0.9584. On
identical rows without `exit_survey` it falls to 0.7507. The repaired pipeline
scores 0.8485. The controlled comparison is the same-rows ablation; the repaired
number is a different dataset and is reported separately.

The data is synthetic and generated locally. No real customers are represented.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab12.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab12.py --artifacts artifacts
```

## What you produce

- `artifacts/validation.json`, `raw.csv`, `repaired.csv`, `metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- A named and counted defect inventory, including the customer split overlap.
- Leaky, same-rows ablation, and repaired metrics reported separately.
- `report.md` answers every reflection question.
- `python check_lab12.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `validate` | Count each defect and the customer split overlap |
| `starter.py` | TODO 2 | `repair` | Drop, impute, quarantine, deduplicate, and remove the post-outcome column |
| `starter.py` | TODO 3 | `evaluate` | Compare the leaky, ablation, and repaired evaluations |

## Hints

- Count each defect before repairing it. A validation report that only says `cleaned` cannot be audited.
- Repair order matters: deduplicate before splitting, and drop the post-outcome column before fitting.
- The same-rows ablation is the controlled comparison. The repaired dataset is a different dataset, so report it separately.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab12.py` | Independent artifact checker |
| `dataset.py` | Deterministic fixture generator |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
