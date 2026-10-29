# LAB-11 — Robustness Evaluation and Defensive Baselines

| Field | Value |
|---|---|
| Lab ID | LAB-11 |
| Tier | A |
| Time | 6 hours |
| Difficulty | 3 of 4 |
| Module | M08 — Robustness and Defense |
| Outcomes | LO-16, LO-17, LO-18, LO-28 |
| Prerequisites | LAB-03; M04 lessons 2–4; M08 lessons 1–3 |
| Data | scikit-learn digits |
| Compute | CPU only; about 2 minutes |

Full brief: [docs/labs/lab-11.md](../../docs/labs/lab-11.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

A partner team asks whether your 10-class digit classifier is "robust enough" and
offers two defenses: adversarial training and input squeezing. You measure clean
accuracy and accuracy under PGD at ε = 0.10 for the undefended model and both
defenses. Then you stress the claim at ε = 0.20 and run an adaptive attack against
the preprocessing defense.

The lab is designed so that the two defenses tell different stories:

- Adversarial training raises robust accuracy from 0.6204 to 0.7296 and costs
  about 7.6 points of clean accuracy.
- Input squeezing looks better still at ε = 0.10 (robust accuracy 0.7722) with
  almost no clean cost, but at ε = 0.20 the same attack succeeds 95.7% of the time.

A defense that passes one test is not secure. Your report must say which budget
and which attack it was evaluated under, and must state that no universal
robustness follows from this experiment.

All data is the bundled scikit-learn digits set. No network access, GPU, or API
key is required.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab11.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab11.py --artifacts artifacts
```

## What you produce

- `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- Clean and robust accuracy for the undefended model and both defenses at both budgets.
- The adaptive-attack result against the preprocessing defense.
- `report.md` answers every reflection question and states the evaluation conditions of every claim.
- `python check_lab11.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `squeeze` | Quantize or smooth the input as a preprocessing defense |
| `starter.py` | TODO 2 | `adversarial_train` | Train with PGD augmentation at a fixed budget |
| `starter.py` | TODO 3 | `pgd_squeezed_bpda` | Adaptive attack through the non-differentiable preprocessing |

## Hints

- Squeezing is a preprocessing function: quantize or smooth the input, then predict. Apply it identically at training and test time.
- Adversarial training augments each batch with PGD examples at a fixed budget. Record that budget in the run record.
- BPDA means using the identity gradient through the non-differentiable preprocessing step, then attacking the full pipeline.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab11.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
