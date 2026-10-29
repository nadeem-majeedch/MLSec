# LAB-07 — Tabular Backdoor with a Known Trigger

| Field | Value |
|---|---|
| Lab ID | LAB-07 |
| Tier | B |
| Time | 4 hours |
| Difficulty | 3 of 4 |
| Module | M06 — Backdoors |
| Outcomes | LO-10, LO-11, LO-28 |
| Prerequisites | LAB-05 or LAB-06; M06 lessons 1–2 |
| Data | synthetic tabular data |
| Compute | CPU only; a few seconds |

Full brief: [docs/labs/lab-07.md](../../docs/labs/lab-07.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

A tabular model is trained on a small synthetic dataset with 16 features. Insert a 3-feature trigger into a controlled fraction of class-0 training rows and relabel them class 1. Measure clean accuracy, trigger ASR, and the clean false-trigger rate. Then remove rows that contain the known trigger and re-evaluate.

The trigger is known to the defender in this lab. Trigger discovery is LAB-08.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab07.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab07.py --artifacts artifacts
```

## What you produce

- `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- Clean accuracy, trigger ASR, and clean false-trigger rate for the poisoned model and the screened retrain.
- `report.md` answers every reflection question.
- `python check_lab07.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `add_trigger` | Copy the input and set the three trigger features |
| `starter.py` | TODO 2 | `poison` | Append triggered class-0 rows labeled class 1 |
| `starter.py` | TODO 3 | `screen` | Flag rows that contain the known trigger |

## Hints

- A trigger is a fixed pattern on named features. `add_trigger` should copy the input and set those features, not mutate the caller's array.
- Poison by appending triggered copies of class-0 rows with label 1; keep the original clean rows.
- Clean false-trigger rate is measured on clean class-0 test rows. It is a separate metric from attack success.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab07.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
