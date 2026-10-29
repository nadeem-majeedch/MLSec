# LAB-06 — Targeted Poisoning and Reference-Set Screening

| Field | Value |
|---|---|
| Lab ID | LAB-06 |
| Tier | A |
| Time | 4 hours |
| Difficulty | 3 of 4 |
| Module | M05 — Poisoning |
| Outcomes | LO-08, LO-09, LO-28 |
| Prerequisites | LAB-05; M05 lessons 1–3 |
| Data | synthetic 2-D mixture |
| Compute | CPU only; under 1 second per fit |

Full brief: [docs/labs/lab-06.md](../../docs/labs/lab-06.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

A local binary classifier protects a decision boundary. You can append 30 mislabelled rows near one chosen test point. Show that the target prediction flips while overall accuracy barely changes, then evaluate a reference-set screening defense and report its false positives.

The data is a seeded 2-D Gaussian mixture. No real people or external services are involved.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab06.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab06.py --artifacts artifacts
```

## What you produce

- `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- Target-point prediction before and after poisoning; overall accuracy before and after.
- Screening results with true and false positives.
- `report.md` answers every reflection question.
- `python check_lab06.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `poison_training_set` | Append mislabeled points near the target point |
| `starter.py` | TODO 2 | `screen_with_reference` | Fit a trusted reference classifier and flag suspicious rows |

## Hints

- Append the poison rows to the training set; do not replace clean rows. The point is a small, targeted change.
- Place the poisoned points near the target test point and give them the opposite label, then verify that the decision actually flips.
- The reference-set screener is a separate trusted model. Report its false positives on clean rows, not only the poison it catches.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab06.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
