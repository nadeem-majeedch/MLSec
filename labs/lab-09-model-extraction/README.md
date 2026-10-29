# LAB-09 — Model Extraction Through a Local Prediction API

| Field | Value |
|---|---|
| Lab ID | LAB-09 |
| Tier | B |
| Time | 4 hours |
| Difficulty | 3 of 4 |
| Module | M07 — Extraction and Privacy |
| Outcomes | LO-12, LO-13, LO-28 |
| Prerequisites | LAB-01 or LAB-01B; M07 lessons 1–2 |
| Data | synthetic 10-D data |
| Compute | CPU only; about 1 minute |

Full brief: [docs/labs/lab-09.md](../../docs/labs/lab-09.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

A local prediction API exposes a 5-class, 10-feature teacher model. You may submit at most 50, 100, 200, or 500 points and receive hard labels. Train a surrogate random forest from the answers and measure fidelity to the teacher and accuracy against the hidden true labels. Compare uniform random queries with entropy-based active queries.

No real service is queried. The API is a local class wrapping a scikit-learn model.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab09.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab09.py --artifacts artifacts
```

## What you produce

- `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- Fidelity and accuracy for random and active queries across the four budgets.
- `report.md` answers every reflection question and compares the two query strategies.
- `python check_lab09.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `PredictionAPI.query` | Enforce the query budget and return hard labels |
| `starter.py` | TODO 2 | `active_queries` | Rank candidate points by predictive entropy |

## Hints

- The API counts every query, including repeats. Enforce the budget before returning labels, not after.
- Entropy selection uses the teacher's probabilities. Keep a separate scoring path so candidate ranking does not spend the query budget.
- Fidelity is agreement with the teacher on new queries; accuracy is agreement with hidden true labels. Report both.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab09.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
