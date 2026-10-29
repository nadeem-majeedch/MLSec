# LAB-05 — Label-Flip Poisoning Curve

| Field | Value |
|---|---|
| Lab ID | LAB-05 |
| Tier | A |
| Time | 4 hours |
| Difficulty | 2 of 4 |
| Module | M05 — Poisoning |
| Outcomes | LO-08, LO-28 |
| Prerequisites | LAB-01 or LAB-01B; M05 lessons 1–2 |
| Data | scikit-learn digits |
| Compute | CPU only; a few seconds |

Full brief: [docs/labs/lab-05.md](../../docs/labs/lab-05.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

A training pipeline accepts labels from an external annotation vendor. You can flip a controlled fraction of training labels but cannot change features or test data. Measure how clean test accuracy and macro F1 change at 0%, 5%, 10%, 20%, and 30% label corruption.

The experiment uses the local digits dataset and a scikit-learn logistic regression. No network or GPU is required.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab05.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab05.py --artifacts artifacts
```

## What you produce

- `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- One result row per poison rate, with clean accuracy and macro F1.
- `report.md` answers every reflection question and states the denominator used for each rate.
- `python check_lab05.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO | `poison_labels` | Choose a seeded fraction of training rows and flip their labels |

## Hints

- Choose corrupted indices with a seeded permutation, then flip their labels. Keep the test set untouched.
- Poison rate is corrupted training rows divided by total training rows. State the denominator in the report.
- Retrain from scratch at every rate. Reusing a model fitted on clean labels measures nothing.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab05.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
