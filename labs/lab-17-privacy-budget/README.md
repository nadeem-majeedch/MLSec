# LAB-17 — Privacy Budget, Noisy Release, and Utility

| Field | Value |
|---|---|
| Lab ID | LAB-17 |
| Tier | A |
| Time | 4 hours |
| Difficulty | 4 of 4 |
| Module | M13 — Privacy-Preserving ML |
| Outcomes | LO-19, LO-28 |
| Prerequisites | M13 lessons 1–5; LAB-10 |
| Data | synthetic Gaussian data |
| Compute | CPU only; seconds |

Full brief: [docs/labs/lab-17.md](../../docs/labs/lab-17.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

A team wants to publish class centroids from a small tabular dataset. You clip
each row, add Laplace noise to each centroid coordinate, account for the budget,
and measure what the noise does to utility and to a simple membership-inference
test.

The reference release uses 500 rows per class, four features clipped to [-3, 3],
and vector L1 sensitivity 0.048. Because the class datasets are disjoint, parallel
composition makes the total budget equal to the per-class epsilon.

| ε | Laplace scale | Test accuracy | Centroid L2 error | Membership AUC |
|---:|---:|---:|---:|---:|
| 0.02 | 2.4000 | 0.5233 | 4.3642 | 0.4903 |
| 0.10 | 0.4800 | 0.7433 | 1.5482 | 0.5237 |
| 0.50 | 0.0960 | 0.7833 | 0.3257 | 0.5308 |
| 1.00 | 0.0480 | 0.8233 | 0.0450 | 0.5258 |
| 4.00 | 0.0120 | 0.8167 | 0.0281 | 0.5263 |

The non-private centroid baseline is 0.8233. The membership AUC stays near chance;
that is an empirical result from one distance test, not a proof of privacy. Your
report must state the full claim (mechanism, sensitivity, composition, ε, δ) and
must not treat the empirical test as validation of the guarantee.

All data is synthetic and generated locally. No personal data, network, GPU, or
API key is required.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab17.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab17.py --artifacts artifacts
```

## What you produce

- `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- One row per epsilon with test accuracy, centroid error, and membership AUC.
- A written privacy claim stating mechanism, sensitivity, composition, ε, and δ.
- `report.md` answers every reflection question.
- `python check_lab17.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `clip_features` | Clip every feature without mutating the input |
| `starter.py` | TODO 2 | `release_centroids` | Release centroids with the Laplace mechanism |
| `starter.py` | TODO 3 | `membership_auc` | Compute a distance-based membership AUC |

## Hints

- Clipping is per row and per feature. Do not mutate the caller's array; return the clipped copy.
- Laplace scale is sensitivity divided by epsilon. Compute vector L1 sensitivity from the clipping bound and feature count.
- Parallel composition applies because the class datasets are disjoint. State the total budget, not only the per-class epsilon.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab17.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
