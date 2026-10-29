# LAB-03 — Evasion Versus Perturbation Budget

| Field | Value |
|---|---|
| Lab ID | LAB-03 |
| Tier | A |
| Time | 4 hours |
| Difficulty | 2 of 4 |
| Module | M04 — Evasion |
| Outcomes | LO-05, LO-28 |
| Prerequisites | M04 lessons 1–3; M02 lesson 2 |
| Data | scikit-learn digits |
| Compute | CPU only; under 1 minute |

Full brief: [docs/labs/lab-03.md](../../docs/labs/lab-03.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

A local image classifier is offered to a partner team. You may inspect the model weights and test data, but you must state an L-inf budget in pixel units. Measure how success changes with the budget and compare one-step FGSM with iterative PGD.

The dataset is scikit-learn's bundled 8x8 digits set. No network access, GPU, or API key is required.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab03.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab03.py --artifacts artifacts
```

## What you produce

- `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- Five FGSM and five PGD rows with ASR, robust accuracy, and perturbation measurements.
- `report.md` answers every reflection question and states at least four limitations.
- `python check_lab03.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `input_gradient` | Gradient of mean cross-entropy with respect to the input |
| `starter.py` | TODO 2 | `fgsm_attack` | One-step sign attack with clipping to [0, 1] |
| `starter.py` | TODO 3 | `pgd_attack` | Iterative sign attack projected into the L∞ ball, with restarts |

## Hints

- For multinomial logistic regression, the input gradient of mean cross-entropy is `(p - onehot(y)) @ coef_ / n`. Check the sign before stepping.
- FGSM is one signed step. PGD repeats that step and projects into `[max(0, x-ε), min(1, x+ε)]` after every iteration.
- Measure ASR only on rows the clean model classified correctly; otherwise clean errors are counted as attack successes.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab03.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
