# LAB-01 — Reproducible Environment and Baseline Pipeline

| Field | Value |
|---|---|
| Lab ID | LAB-01 |
| Tier | A |
| Time | 3 hours |
| Difficulty | 1 of 4 |
| Module | M00–M01 — Orientation and Python tooling |
| Outcomes | LO-01, LO-28 |
| Prerequisites | Basic Python, terminal use, train/test split |
| Data | scikit-learn digits |
| Compute | CPU only; a few seconds |

Full brief: [docs/labs/lab-01.md](../../docs/labs/lab-01.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

You inherit a script that produced a digit classifier and a single accuracy number. Before anyone trusts it, you rebuild the result as a reproducible pipeline: deterministic splits, a saved model, a run record, a manifest, and a report another person can rerun.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab01.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab01.py --artifacts artifacts
```

## What you produce

- `artifacts/model.joblib`, `splits.npz`, `metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- `report.md` answers every reflection question.
- `python check_lab01.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `build_model` | Return a `Pipeline` with scaling and logistic regression, unfitted |
| `starter.py` | TODO 2 | `write_artifacts` | Write the model, split indices, metrics, run record, and manifest |
| `starter.py` | TODO 3 | `write_report` | Write `report.md` with the five required headings |

## Hints

- Build the pipeline as two named steps: a scaler and a classifier. Fit it once on the training split; fitting the scaler on test rows leaks the test distribution.
- Write `metrics.json`, `run.json`, and `report.md` before you build the manifest. A manifest created early will omit files that did not exist yet.
- `splits.npz` should let another person reconstruct the exact train, validation, and test rows without rerunning your split.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab01.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `report_template.md` | Report headings and prompts |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
