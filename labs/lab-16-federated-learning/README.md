# LAB-16 — Federated Learning Attack and Defense Simulation

| Field | Value |
|---|---|
| Lab ID | LAB-16 |
| Tier | A |
| Time | 5 hours |
| Difficulty | 4 of 4 |
| Module | M12 — Federated Learning |
| Outcomes | LO-24, LO-28 |
| Prerequisites | M12 lessons 1–5; M04 lessons 2–4; LAB-05 or LAB-07 |
| Data | scikit-learn digits |
| Compute | CPU only; a few seconds |

Full brief: [docs/labs/lab-16.md](../../docs/labs/lab-16.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

Eight clinics train one shared digit classifier without pooling data. A partner
asks whether FedAvg is safe when one participant is compromised. You simulate a
non-IID federation, let one client train on triggered data and scale its update,
then compare mean aggregation with trimmed mean and per-client norm clipping at
equal rounds.

The reference run tells a deliberately mixed story:

- Benign mean aggregation reaches clean accuracy 0.9000 with attack success 0.0021.
- One scaled malicious update reaches ASR 1.0000 and drops clean accuracy to 0.7056.
- Coordinate-wise trimmed mean removes the attack in this setup: clean 0.8704, ASR 0.0000.
- Norm clipping leaves clean 0.8944 but only reduces ASR to 0.6276.

Trimmed mean is not a general fix. A Sybil attacker who controls several client
identities can defeat it, clipping does not stop a patient attacker, and secure
aggregation hides updates without preventing a poisoned aggregate. Your report
must state those limits and must not claim that either defense makes federation
secure.

All data is the bundled scikit-learn digits set. Clients run as local objects in
one process; no network, GPU, or federated framework is required.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab16.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab16.py --artifacts artifacts
```

## What you produce

- `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- Clean accuracy and ASR for the benign baseline, the attack, and each defense at equal rounds.
- `report.md` answers every reflection question and states the limits of trimmed mean and clipping.
- `python check_lab16.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `partition_clients` | Build a deterministic non-IID client partition |
| `starter.py` | TODO 2 | `train_local` | Train a softmax model for a fixed number of full-batch steps |
| `starter.py` | TODO 3 | `aggregate_trimmed_mean` | Apply coordinate-wise trimmed mean |

## Hints

- Partition by class and client so the federation is non-IID, but keep every client's data non-empty and deterministic.
- Local training is full-batch softmax regression for a fixed number of epochs. Record the learning rate and epochs.
- Trimmed mean sorts each coordinate, removes the extremes, and averages the rest. Do it per coordinate, not per client.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab16.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
