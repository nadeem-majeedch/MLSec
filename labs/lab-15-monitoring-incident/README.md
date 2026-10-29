# LAB-15 — Monitoring, Drift, and Incident Response

| Field | Value |
|---|---|
| Lab ID | LAB-15 |
| Tier | A |
| Time | 3 hours |
| Difficulty | 3 of 4 |
| Module | M11 — Serving and Monitoring |
| Outcomes | LO-23, LO-30 (supporting), LO-28 |
| Prerequisites | M04 lessons 1–3; M07; M11 lessons 4–5; LAB-11/14 recommended |
| Data | synthetic logs and digits |
| Compute | CPU only; a few seconds; ~2.5 MB logs |

Full brief: [docs/labs/lab-15.md](../../docs/labs/lab-15.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

The hardened prediction service from LAB-14 has been running for a while. You
have prediction logs and no incident feed. Six synthetic scenarios produce 3,900
requests in 100-request windows: a quiet calibration period, normal traffic, an
unannounced scanner change, an FGSM evasion campaign, a single-client query
burst, and recovery after containment.

The reference monitor calibrates five detectors on the quiet period only:
input shift, low confidence, shadow-model disagreement, client concentration,
and throughput. It then groups consecutive alerts into episodes and triages
them by signal family:

| Episode | Signals | Severity | Action |
|---|---|---|---|
| Benign drift | input shift only | low | review the change, no incident |
| Evasion attack | three content signals | high | incident INC-001, contain and investigate |
| Query burst | two volume signals | medium | rate-limit and review the client |

The high-severity incident is handled with a written playbook. Rollback is
tested against a captured attack batch and rejected because the previous
checkpoint is equally vulnerable. Edge squeezing is measured as a temporary
mitigation with a clean-accuracy cost, and recovery is verified only when clean
windows return to the calibrated confidence band.

All traffic and clients are synthetic. The model and logs stay on your machine;
nothing contacts a real service. Logged features exist for reproducibility, and
the report explains why production logs should not store raw inputs.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab15.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab15.py --artifacts artifacts
```

## What you produce

- `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- Detector calibration values, episode grouping, and per-scenario outcomes.
- An incident timeline and playbook for the high-severity episode.
- `report.md` answers every reflection question and explains why rollback was accepted or rejected.
- `python check_lab15.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `window_statistics` | Compute windowed content and volume statistics |
| `starter.py` | TODO 2 | `detect` | Return the five detector booleans calibrated on the quiet period |
| `starter.py` | TODO 3 | `triage` | Classify the episode, assign severity, and select a playbook |

## Hints

- Calibrate on the quiet window only. If you calibrate on attack traffic, the threshold is contaminated.
- Each detector returns a boolean for one window. Group consecutive alerts into episodes before triage.
- Triage needs a signal family and a severity rule, not a single alert count.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab15.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
