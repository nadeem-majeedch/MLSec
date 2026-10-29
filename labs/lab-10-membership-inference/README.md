# LAB-10 — Membership Inference Against a Local Model

| Field | Value |
|---|---|
| Lab ID | LAB-10 |
| Tier | B |
| Time | 3 hours |
| Difficulty | 3 of 4 |
| Module | M07 — Extraction and Privacy |
| Outcomes | LO-12, LO-14, LO-28 |
| Prerequisites | LAB-01B; M07 lesson 3 |
| Data | scikit-learn digits |
| Compute | CPU only; seconds |

Full brief: [docs/labs/lab-10.md](../../docs/labs/lab-10.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

A random forest is trained on 500 digit images. Another 500 images from the same
public dataset were never used for training. Treat the learned model as the
target of a membership-inference attempt: for each image, decide whether it was
in the training set, using only the model's maximum class probability.

The lab measures how far that signal actually carries you. Members are more
confident on average, but the AUC hides the low detection rate at a strict
false-positive budget. Your report must explain why confidence is not proof of
membership.

All data is the bundled scikit-learn digits set. No private or personal data is
used, and no real deployed model is probed.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab10.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab10.py --artifacts artifacts
```

## What you produce

- `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- AUC and TPR at the stated false-positive budget, with the threshold recorded.
- `report.md` answers every reflection question and explains why confidence is not membership.
- `python check_lab10.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `confidence_scores` | One membership score per row from the maximum class probability |
| `starter.py` | TODO 2 | `tpr_at_fpr` | True-positive rate at a fixed false-positive budget |
| `starter.py` | TODO 3 | report text | Explain the AUC, the low-FPR result, and the limits |

## Hints

- Use the model's maximum predicted probability as the membership score. A row is predicted a member when the score exceeds a threshold.
- TPR at a fixed FPR comes from the ROC curve; do not report only AUC.
- The evaluation set must contain both members and non-members. Evaluating on training rows only makes the experiment meaningless.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab10.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
