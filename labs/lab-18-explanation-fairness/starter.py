"""LAB-18 starter: explanation stability and subgroup audit.

Run from this directory:
    python starter.py --out artifacts

Three TODO blocks: fit_models, occlusion, stability. Data generation, subgroup
metrics, bootstrap intervals, gradient x input, and the report template are given.
Complete the TODOs, then run check_lab18.py on your artifacts.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

SEED = 42
N_ROWS = 1200
NOISE_SIGMA = 0.25
TOP_K = 2
BOOTSTRAP_ROUNDS = 2000
BOOTSTRAP_SEED = 123


def make_data():
    rng = np.random.default_rng(SEED)
    group = rng.choice([0, 1], size=N_ROWS, p=[0.6, 0.4])
    X = rng.normal(size=(N_ROWS, 6))
    logit = 1.2 * X[:, 0] + 0.9 * X[:, 1] + 0.6 * X[:, 2] + 1.0 * group - 0.7
    probability = 1.0 / (1.0 + np.exp(-logit))
    y = rng.binomial(1, probability)
    return X, y, group


def fit_models(X_train, y_train, group_train):
    """TODO 1: fit a baseline and a group-reweighted logistic model.

    Baseline: LogisticRegression(max_iter=2000, random_state=SEED).
    Reweighted: the same model with sample_weight = n / (2 * count(group)) for
    each training row, so each group contributes equally. Return both models.
    """
    raise NotImplementedError("TODO 1: implement fit_models")


def probabilities(model, X):
    return model.predict_proba(X)[:, 1]


def subgroup_metrics(y_true, y_pred, group):
    result = {}
    for value in (0, 1):
        mask = group == value
        truth = y_true[mask]
        prediction = y_pred[mask]
        positives = truth == 1
        negatives = truth == 0
        result[str(value)] = {
            "n": int(mask.sum()),
            "accuracy": round(float((prediction == truth).mean()), 4),
            "tpr": round(float((prediction[positives] == 1).mean()), 4),
            "fpr": round(float((prediction[negatives] == 1).mean()), 4),
            "selection_rate": round(float(prediction.mean()), 4),
        }
    return result


def gaps(metrics):
    a, b = metrics["0"], metrics["1"]
    return {
        "demographic_parity": abs(a["selection_rate"] - b["selection_rate"]),
        "equalized_odds": max(abs(a["tpr"] - b["tpr"]), abs(a["fpr"] - b["fpr"])),
    }


def bootstrap_gaps(y_true, y_pred, group):
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    samples = {"demographic_parity": [], "equalized_odds": []}
    for _ in range(BOOTSTRAP_ROUNDS):
        indices = np.concatenate(
            [
                rng.choice(np.flatnonzero(group == value), size=int((group == value).sum()), replace=True)
                for value in (0, 1)
            ]
        )
        current = gaps(subgroup_metrics(y_true[indices], y_pred[indices], group[indices]))
        for key in samples:
            samples[key].append(current[key])
    return {
        key: [round(float(np.percentile(values, 2.5)), 4), round(float(np.percentile(values, 97.5)), 4)]
        for key, values in samples.items()
    }


def evaluate_model(model, X, y, group):
    prediction = model.predict(X)
    metrics = subgroup_metrics(y, prediction, group)
    return {
        "overall_accuracy": round(float((prediction == y).mean()), 4),
        "subgroups": metrics,
        "gaps": {key: round(value, 4) for key, value in gaps(metrics).items()},
        "gaps_95ci": bootstrap_gaps(y, prediction, group),
    }


def gradient_x_input(model, X):
    return X * model.coef_[0]


def occlusion(model, X, baseline=0.0):
    """TODO 2: occlusion attributions.

    For each feature, replace that feature with `baseline`, compute the positive
    class probability, and subtract it from the original probability. Return an
    array with the same shape as X.
    """
    raise NotImplementedError("TODO 2: implement occlusion")


def ranks(values):
    order = np.argsort(values)
    result = np.empty_like(order, dtype=float)
    result[order] = np.arange(len(values), dtype=float)
    return result


def spearman(first, second):
    first_rank = ranks(first)
    second_rank = ranks(second)
    first_rank -= first_rank.mean()
    second_rank -= second_rank.mean()
    denominator = np.linalg.norm(first_rank) * np.linalg.norm(second_rank)
    if denominator == 0.0:
        return 0.0
    return float(first_rank @ second_rank / denominator)


def stability(model, X, method, seed=SEED):
    """TODO 3: measure explanation stability under Gaussian noise.

    Compute original attributions (gradient_x_input or occlusion). For each row,
    add N(0, NOISE_SIGMA) noise to all features, recompute the attribution, and
    record the Spearman correlation and top-K overlap. If the prediction is
    unchanged, also record whether the top-1 feature changed. Return the mean
    Spearman, mean top-K overlap, preserved-row count, and flip rate.
    """
    raise NotImplementedError("TODO 3: implement stability")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the LAB-18 explanation and fairness audit.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()

    X, y, group = make_data()
    X_train, X_test, y_train, y_test, group_train, group_test = train_test_split(
        X, y, group, test_size=0.3, random_state=SEED, stratify=y * 2 + group
    )
    baseline, reweighted = fit_models(X_train, y_train, group_train)

    models = {
        "baseline": evaluate_model(baseline, X_test, y_test, group_test),
        "reweighted": evaluate_model(reweighted, X_test, y_test, group_test),
    }
    explanations = {
        name: {
            method: stability(model, X_test, method)
            for method in ("gradient_x_input", "occlusion")
        }
        for name, model in (("baseline", baseline), ("reweighted", reweighted))
    }

    metrics = {
        "data": {
            "rows": N_ROWS,
            "train_rows": int(len(y_train)),
            "test_rows": int(len(y_test)),
            "test_group_counts": {
                "0": int((group_test == 0).sum()),
                "1": int((group_test == 1).sum()),
            },
        },
        "models": models,
        "explanation_stability": explanations,
        "config": {
            "noise_sigma": NOISE_SIGMA,
            "top_k": TOP_K,
            "bootstrap_rounds": BOOTSTRAP_ROUNDS,
            "explanation_methods": ["gradient_x_input", "occlusion"],
        },
        "note": (
            "Synthetic data, seed 42. Stability is measured only under isotropic Gaussian noise "
            "at sigma 0.25 for this model and split. A stable explanation is not necessarily "
            "faithful, fair, or leak-free."
        ),
    }

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "metrics.json", metrics)
    write_json(
        out / "run.json",
        {
            "lab": "LAB-18",
            "seed": SEED,
            "noise_sigma": NOISE_SIGMA,
            "top_k": TOP_K,
            "bootstrap_rounds": BOOTSTRAP_ROUNDS,
            "models": ["baseline", "reweighted"],
            "environment": environment(),
        },
    )

    base = models["baseline"]
    reweight = models["reweighted"]

    def row(name, block):
        return (
            f"| {name} | {block['overall_accuracy']:.4f} | "
            f"{block['subgroups']['0']['tpr']:.4f} | {block['subgroups']['1']['tpr']:.4f} | "
            f"{block['subgroups']['0']['fpr']:.4f} | {block['subgroups']['1']['fpr']:.4f} | "
            f"{block['gaps']['demographic_parity']:.4f} | "
            f"{block['gaps']['equalized_odds']:.4f} |"
        )

    report = f"""# LAB-18 report

## Setup

The synthetic dataset has {N_ROWS} rows, six standard-normal features, a binary
label, and a binary subgroup attribute. Group 0 is 60% of the rows and group 1 is
40%. The test split has {len(y_test)} rows.

The baseline is logistic regression with no sample weights. The reweighted model
uses weights inversely proportional to group frequency.

## Subgroup performance

| Model | Accuracy | TPR group 0 | TPR group 1 | FPR group 0 | FPR group 1 | DP gap | EO gap |
|---|---:|---:|---:|---:|---:|---:|---:|
{row('Baseline', base)}
{row('Reweighted', reweight)}

Bootstrap 95% intervals (baseline): demographic parity
{base['gaps_95ci']['demographic_parity']}, equalized odds
{base['gaps_95ci']['equalized_odds']}. Reweighted: demographic parity
{reweight['gaps_95ci']['demographic_parity']}, equalized odds
{reweight['gaps_95ci']['equalized_odds']}.

## Explanation stability

| Model | Method | Mean Spearman | Mean top-2 overlap | Prediction preserved | Top-feature flip rate |
|---|---|---:|---:|---:|---:|
| Baseline | gradient × input | {explanations['baseline']['gradient_x_input']['mean_spearman']:.4f} | {explanations['baseline']['gradient_x_input']['mean_top2_overlap']:.4f} | {explanations['baseline']['gradient_x_input']['prediction_preserved_rows']} | {explanations['baseline']['gradient_x_input']['top_feature_flip_rate_when_prediction_preserved']:.4f} |
| Baseline | occlusion | {explanations['baseline']['occlusion']['mean_spearman']:.4f} | {explanations['baseline']['occlusion']['mean_top2_overlap']:.4f} | {explanations['baseline']['occlusion']['prediction_preserved_rows']} | {explanations['baseline']['occlusion']['top_feature_flip_rate_when_prediction_preserved']:.4f} |
| Reweighted | gradient × input | {explanations['reweighted']['gradient_x_input']['mean_spearman']:.4f} | {explanations['reweighted']['gradient_x_input']['mean_top2_overlap']:.4f} | {explanations['reweighted']['gradient_x_input']['prediction_preserved_rows']} | {explanations['reweighted']['gradient_x_input']['top_feature_flip_rate_when_prediction_preserved']:.4f} |
| Reweighted | occlusion | {explanations['reweighted']['occlusion']['mean_spearman']:.4f} | {explanations['reweighted']['occlusion']['mean_top2_overlap']:.4f} | {explanations['reweighted']['occlusion']['prediction_preserved_rows']} | {explanations['reweighted']['occlusion']['top_feature_flip_rate_when_prediction_preserved']:.4f} |

## Interpretation

Equalized odds improves while demographic parity worsens, and accuracy falls.
That is a trade-off between fairness metrics, not a defect in the arithmetic.
Group reweighting is a training-time intervention, not a guarantee of fairness.

Explanation stability is method-dependent and incomplete. A stable explanation is
not necessarily faithful, fair, or leak-free.

## Limitations

The data are synthetic, the models are linear, and the perturbation is one
isotropic Gaussian scale. The bootstrap intervals describe sampling variability on
this split, not deployment uncertainty. Fairness metrics are population summaries
and can hide within-group harm. Explanation leakage and adversarial manipulation
are discussed in the module but not measured here.
"""
    (out / "report.md").write_text(report, encoding="utf-8", newline="\n")
    write_json(out / "manifest.json", build_manifest(out, ["metrics.json", "run.json", "report.md"]))

    for name, block in models.items():
        print(
            f"{name}: accuracy={block['overall_accuracy']:.4f} "
            f"dp={block['gaps']['demographic_parity']:.4f} "
            f"eo={block['gaps']['equalized_odds']:.4f}"
        )


if __name__ == "__main__":
    main()
