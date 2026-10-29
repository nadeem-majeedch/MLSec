"""LAB-18 reference solution: explanation stability and subgroup audit.

Run from this directory:
    python solution.py --out artifacts

The lab compares a baseline logistic model with a group-reweighted model on
synthetic tabular data. It measures subgroup performance, two fairness gaps, the
stability of two explanation methods under bounded input noise, and the rate at
which the top explanation feature changes while the prediction does not.
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
    baseline = LogisticRegression(max_iter=2000, random_state=SEED).fit(X_train, y_train)
    group_counts = {value: int((group_train == value).sum()) for value in (0, 1)}
    total = len(group_train)
    sample_weight = np.array(
        [total / (2.0 * group_counts[int(value)]) for value in group_train]
    )
    reweighted = LogisticRegression(max_iter=2000, random_state=SEED).fit(
        X_train, y_train, sample_weight=sample_weight
    )
    return baseline, reweighted


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
        metrics = subgroup_metrics(y_true[indices], y_pred[indices], group[indices])
        current = gaps(metrics)
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
    original = probabilities(model, X)
    attributions = np.zeros_like(X)
    for feature in range(X.shape[1]):
        occluded = X.copy()
        occluded[:, feature] = baseline
        attributions[:, feature] = original - probabilities(model, occluded)
    return attributions


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
    rng = np.random.default_rng(seed)
    original_scores = gradient_x_input(model, X) if method == "gradient_x_input" else occlusion(model, X)
    original_prediction = model.predict(X)
    correlations = []
    overlaps = []
    preserved = 0
    explanation_flips = 0
    for row in range(len(X)):
        perturbed = X[row] + rng.normal(0.0, NOISE_SIGMA, size=X.shape[1])
        perturbed_scores = (
            gradient_x_input(model, perturbed[None, :])[0]
            if method == "gradient_x_input"
            else occlusion(model, perturbed[None, :])[0]
        )
        correlations.append(spearman(original_scores[row], perturbed_scores))
        top_original = set(np.argsort(-np.abs(original_scores[row]))[:TOP_K])
        top_perturbed = set(np.argsort(-np.abs(perturbed_scores))[:TOP_K])
        overlaps.append(len(top_original & top_perturbed) / TOP_K)
        if model.predict(perturbed[None, :])[0] == original_prediction[row]:
            preserved += 1
            if np.argmax(np.abs(original_scores[row])) != np.argmax(np.abs(perturbed_scores)):
                explanation_flips += 1
    return {
        "mean_spearman": round(float(np.mean(correlations)), 4),
        "mean_top2_overlap": round(float(np.mean(overlaps)), 4),
        "prediction_preserved_rows": int(preserved),
        "top_feature_flip_rate_when_prediction_preserved": round(
            explanation_flips / preserved, 4
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the LAB-18 explanation and fairness audit.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()

    X, y, group = make_data()
    stratify = y * 2 + group
    X_train, X_test, y_train, y_test, group_train, group_test = train_test_split(
        X, y, group, test_size=0.3, random_state=SEED, stratify=stratify
    )
    baseline, reweighted = fit_models(X_train, y_train, group_train)

    models = {
        "baseline": evaluate_model(baseline, X_test, y_test, group_test),
        "reweighted": evaluate_model(reweighted, X_test, y_test, group_test),
    }

    explanations = {}
    for name, model in (("baseline", baseline), ("reweighted", reweighted)):
        explanations[name] = {
            method: stability(model, X_test, method)
            for method in ("gradient_x_input", "occlusion")
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
40%; the label depends on the features and on group membership. The test split has
{len(y_test)} rows ({int((group_test == 0).sum())} group 0, {int((group_test == 1).sum())} group 1).

The baseline is logistic regression with no sample weights. The reweighted model
uses sample weights inversely proportional to group frequency, so each group
contributes equally to the training objective. Neither model is trained on the
test rows.

## Subgroup performance

| Model | Accuracy | TPR group 0 | TPR group 1 | FPR group 0 | FPR group 1 | DP gap | EO gap |
|---|---:|---:|---:|---:|---:|---:|---:|
{row('Baseline', base)}
{row('Reweighted', reweight)}

Bootstrap 95% intervals for the gaps (baseline): demographic parity
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

The baseline has a demographic-parity gap of {base['gaps']['demographic_parity']:.4f}
and an equalized-odds gap of {base['gaps']['equalized_odds']:.4f}. Reweighting
changes both, but it does not set either gap to zero: group weighting is a
training-time intervention, not a guarantee of equal error rates. Equalized odds
improves while demographic parity worsens, and accuracy falls. That is a concrete
trade-off between fairness metrics, not a defect in the arithmetic: the metrics
encode different goals and cannot generally be minimized at once.

Explanation stability is method-dependent. Gradient × input and occlusion produce
different attribution patterns, and the two methods need not agree on the top
feature. The flip rate counts rows where the prediction is unchanged but the
top-ranked explanation feature changes under noise. That is a warning about
reading a single explanation as a stable fact about the model, not evidence that
the model is wrong.

## Limitations

The data are synthetic, the models are linear, and the perturbation is isotropic
Gaussian noise at one scale. The bootstrap intervals describe sampling variability
on this split, not deployment uncertainty. Fairness metrics are population
summaries and can hide within-group harm. No claim is made that the reweighted
model is fair, that either explanation is faithful, or that stable explanations
are secure. Explanation leakage and adversarial explanation manipulation are
discussed in the module but not measured here.
"""
    (out / "report.md").write_text(report, encoding="utf-8", newline="\n")
    write_json(out / "manifest.json", build_manifest(out, ["metrics.json", "run.json", "report.md"]))

    for name, block in models.items():
        print(
            f"{name}: accuracy={block['overall_accuracy']:.4f} "
            f"dp={block['gaps']['demographic_parity']:.4f} "
            f"eo={block['gaps']['equalized_odds']:.4f}"
        )
    for name, methods in explanations.items():
        for method, values in methods.items():
            print(
                f"{name}/{method}: spearman={values['mean_spearman']:.4f} "
                f"top2={values['mean_top2_overlap']:.4f} "
                f"flip={values['top_feature_flip_rate_when_prediction_preserved']:.4f}"
            )
    print(f"artifacts written to {out.resolve()}")


if __name__ == "__main__":
    main()
