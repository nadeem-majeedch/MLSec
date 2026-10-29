# LAB-04 — Targeted Evasion and Transfer to a Black-Box Model

| Field | Value |
|---|---|
| Lab ID | LAB-04 |
| Tier | A |
| Time | 4 hours |
| Difficulty | 3 of 4 |
| Module | M04 — Evasion |
| Outcomes | LO-05, LO-06, LO-07, LO-28 |
| Prerequisites | LAB-03; M04 lessons 2–4 |
| Data | scikit-learn digits |
| Compute | CPU only; under 1 minute |

Full brief: [docs/labs/lab-04.md](../../docs/labs/lab-04.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

You can inspect a local logistic regression classifier but not the random forest used by the receiving team. Craft a targeted attack against class 3 on the source model and measure how often it transfers to the black-box target. Then compare with an untargeted FGSM transfer baseline.

The target model is used only for evaluation. No target queries are used to build the perturbation.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab04.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab04.py --artifacts artifacts
```

## What you produce

- `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- Targeted and untargeted transfer results at the stated budgets, with source and target metrics separated.
- `report.md` answers every reflection question and states the transfer claim's limits.
- `python check_lab04.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `gradient` | Gradient of cross-entropy with respect to the input |
| `starter.py` | TODO 2 | `targeted_pgd` | Minimize the target-class loss inside the L∞ ball |
| `starter.py` | TODO 3 | `untargeted_fgsm` | One-step attack that increases the true-class loss |

## Hints

- Targeted PGD decreases the target-class loss, not the true-class loss. The sign of the update is the opposite of the untargeted case.
- Use the target model only to evaluate. If you query it while crafting, you are measuring a white-box attack and calling it transfer.
- Report the target-class rate separately from overall error. A transfer attack can raise error without ever producing the chosen class.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab04.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
