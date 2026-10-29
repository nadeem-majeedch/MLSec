# LAB-18 — Explanation Stability and Subgroup Audit

| Field | Value |
|---|---|
| Lab ID | LAB-18 |
| Tier | A |
| Time | 4 hours |
| Difficulty | 3 of 4 |
| Module | M14 — Explainability and Fairness |
| Outcomes | LO-31, LO-32, LO-28 |
| Prerequisites | M14 lessons 1–4; M02; M13 lesson 5 |
| Data | synthetic lending data |
| Compute | CPU only; seconds |

Full brief: [docs/labs/lab-18.md](../../docs/labs/lab-18.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

A lending team ships a logistic model and a "fairness-aware" reweighted variant.
They also show feature attributions to explain individual decisions. You audit
overall accuracy, subgroup error rates, two fairness gaps with interval estimates,
and the stability of gradient×input and occlusion explanations under bounded
input noise.

The reference run produces a metric conflict:

| Model | Accuracy | DP gap | EO gap |
|---|---:|---:|---:|
| Baseline | 0.7528 | 0.0013 | 0.1231 |
| Reweighted | 0.7389 | 0.0125 | 0.0930 |

Reweighting lowers the equalized-odds gap but raises the demographic-parity gap
and costs 1.39 points of accuracy. That is a trade-off, not a bug.

Explanation stability is measured at Gaussian noise σ = 0.25. Both methods retain
a mean Spearman correlation near 0.90 and a top-2 overlap near 0.86, but the
top-ranked feature changes while the prediction stays the same on roughly 14–15%
of rows. Stable explanations are not thereby correct, fair, or leak-free.

All data is synthetic and local. No network, GPU, or API key is required.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab18.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab18.py --artifacts artifacts
```

## What you produce

- `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- Overall accuracy, subgroup metrics, both fairness gaps, and interval estimates.
- Explanation stability metrics for both attribution methods.
- `report.md` answers every reflection question and states what stability does not prove.
- `python check_lab18.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `fit_models` | Fit the baseline and group-reweighted logistic models |
| `starter.py` | TODO 2 | `occlusion` | Compute occlusion attributions against a fixed baseline |
| `starter.py` | TODO 3 | `stability` | Measure rank correlation and top-k overlap under bounded noise |

## Hints

- Fit the baseline and reweighted models on the same split. Reweighting changes sample weights, not the evaluation rows.
- Occlusion replaces one feature at a time with a baseline value and measures the prediction change. Keep the baseline fixed.
- Stability compares attributions under repeated bounded noise. Use a rank correlation and top-k overlap, not a single example.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab18.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
