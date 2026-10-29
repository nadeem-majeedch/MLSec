# LAB-08 — Image Backdoor and Trigger Search

| Field | Value |
|---|---|
| Lab ID | LAB-08 |
| Tier | B |
| Time | 4 hours |
| Difficulty | 3 of 4 |
| Module | M06 — Backdoors |
| Outcomes | LO-10, LO-11, LO-28 |
| Prerequisites | LAB-07; M06 lessons 1–3 |
| Data | digits 3 vs 8 |
| Compute | CPU only; seconds |

Full brief: [docs/labs/lab-08.md](../../docs/labs/lab-08.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

A binary digit classifier (3 vs 8) was trained on data from an untrusted pipeline. A white 2x2 patch makes class-0 images classify as class 1. You do not know the patch location in advance. Search all 49 positions, rank them by the model's target-class score, then remove training rows containing the discovered patch and re-evaluate.

The dataset is bundled with scikit-learn. All work is local.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab08.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab08.py --artifacts artifacts
```

## What you produce

- `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- The trigger search ranking, the discovered position, and the screened retrain metrics.
- `report.md` answers every reflection question and distinguishes detection from proof.
- `python check_lab08.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `apply_patch` | Stamp a 2×2 patch at a given position |
| `starter.py` | TODO 2 | `build_backdoor` | Append triggered copies of 8% of class-0 rows as class 1 |
| `starter.py` | TODO 3 | `scan_trigger` | Score all 49 patch positions by mean target-class probability |
| `starter.py` | TODO 4 | `filter_patch` | Flag rows whose patch region is entirely 1.0 |

## Hints

- There are 49 positions for a 2×2 patch on an 8×8 image. Enumerate all of them; do not hard-code the location.
- Score a position by the model's mean target-class probability on source images after stamping the patch.
- Filter training rows by checking whether the patch region is entirely 1.0, then retrain from scratch.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab08.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
