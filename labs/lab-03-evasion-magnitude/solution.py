"""LAB-03 reference solution: measure evasion as a function of L-inf budget.

Run from this directory:
    python solution.py --out artifacts

Artifacts: metrics.json, run.json, report.md, manifest.json.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

EPSILONS = [0.0, 0.02, 0.05, 0.10, 0.20]
SEED = 42


def load_data():
    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    return train_test_split(X, y, test_size=0.3, random_state=SEED, stratify=y)


def fit_model(X_train, y_train) -> LogisticRegression:
    return LogisticRegression(max_iter=5000, C=1.0).fit(X_train, y_train)


def probabilities(model: LogisticRegression, X: np.ndarray) -> np.ndarray:
    scores = X @ model.coef_.T + model.intercept_
    scores -= scores.max(axis=1, keepdims=True)
    exp = np.exp(scores)
    return exp / exp.sum(axis=1, keepdims=True)


def input_gradient(model: LogisticRegression, X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Gradient of mean cross-entropy with respect to the input pixels."""
    p = probabilities(model, X)
    p[np.arange(len(y)), y] -= 1.0
    return p @ model.coef_


def fgsm_attack(model, X, y, epsilon):
    return np.clip(X + epsilon * np.sign(input_gradient(model, X, y)), 0.0, 1.0)


def pgd_attack(model, X, y, epsilon, alpha=None, steps=40, restarts=3, seed=SEED):
    if epsilon == 0.0:
        return X.copy()
    alpha = alpha or max(epsilon / 10.0, 0.005)
    rng = np.random.default_rng(seed)
    best = X.copy()
    best_success = np.zeros(len(y), dtype=bool)
    for restart in range(restarts):
        x_adv = X.copy()
        if restart:
            x_adv = np.clip(X + rng.uniform(-epsilon, epsilon, X.shape), 0.0, 1.0)
        for _ in range(steps):
            grad = input_gradient(model, x_adv, y)
            x_adv = np.clip(x_adv + alpha * np.sign(grad), X - epsilon, X + epsilon)
            x_adv = np.clip(x_adv, 0.0, 1.0)
        success = model.predict(x_adv) != y
        update = success & ~best_success
        best[update] = x_adv[update]
        best_success |= success
    return best


def summarize(model, X, y, X_adv, clean_correct):
    pred = model.predict(X_adv)
    success = pred[clean_correct] != y[clean_correct]
    delta = X_adv - X
    return {
        "asr": float(success.mean()),
        "robust_accuracy": float((pred == y).mean()),
        "mean_linf": float(np.abs(delta).max(axis=1).mean()),
        "max_linf": float(np.abs(delta).max()),
        "mean_l2": float(np.sqrt((delta**2).sum(axis=1)).mean()),
    }


def build_report(metrics):
    lines = [
        "# LAB-03 report — evasion versus perturbation budget",
        "",
        "Model: multinomial logistic regression on 8x8 digits, pixels scaled to [0, 1].",
        "Success is measured only on examples the clean model classified correctly.",
        "",
        "| Method | epsilon | ASR | Robust accuracy | mean L-inf |",
        "|---|---:|---:|---:|---:|",
    ]
    for method in ("fgsm", "pgd"):
        for row in metrics[method]:
            lines.append(
                f"| {method.upper()} | {row['epsilon']:.2f} | {row['asr']:.4f} | "
                f"{row['robust_accuracy']:.4f} | {row['mean_linf']:.4f} |"
            )
    lines += [
        "",
        f"Clean accuracy: {metrics['clean_accuracy']:.4f}; clean-correct examples: "
        f"{metrics['clean_correct']} of {metrics['test_size']}.",
        "",
        "## Limitations",
        "",
        "- Only an L-inf budget is tested, on one linear model and one split.",
        "- A linear model is a deliberately weak baseline; success does not transfer to every model.",
        "- No defense or adaptive evaluation is included; see M08 and LAB-11 for that step.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure evasion versus L-inf budget.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    X_train, X_test, y_train, y_test = load_data()
    model = fit_model(X_train, y_train)
    clean_pred = model.predict(X_test)
    clean_correct = clean_pred == y_test

    metrics = {
        "clean_accuracy": float(clean_correct.mean()),
        "clean_correct": int(clean_correct.sum()),
        "test_size": int(len(y_test)),
        "epsilons": EPSILONS,
        "fgsm": [],
        "pgd": [],
        "dataset": "sklearn.datasets.load_digits (8x8, pixels/16)",
    }
    for eps in EPSILONS:
        metrics["fgsm"].append(
            {"epsilon": eps, **summarize(model, X_test, y_test, fgsm_attack(model, X_test, y_test, eps), clean_correct)}
        )
        metrics["pgd"].append(
            {"epsilon": eps, **summarize(model, X_test, y_test, pgd_attack(model, X_test, y_test, eps), clean_correct)}
        )

    write_json(args.out / "metrics.json", metrics)
    write_json(
        args.out / "run.json",
        {
            "lab": "LAB-03",
            "seed": args.seed,
            "epsilons": EPSILONS,
            "pgd_steps": 40,
            "pgd_restarts": 3,
            "environment": environment(),
        },
    )
    (args.out / "report.md").write_text(build_report(metrics), encoding="utf-8", newline="\n")
    write_json(
        args.out / "manifest.json",
        build_manifest(args.out, ["metrics.json", "run.json", "report.md"]),
    )
    print(f"clean accuracy={metrics['clean_accuracy']:.4f}")
    for row in metrics["fgsm"]:
        print(f"fgsm eps={row['epsilon']:.2f} asr={row['asr']:.4f}")
    for row in metrics["pgd"]:
        print(f"pgd  eps={row['epsilon']:.2f} asr={row['asr']:.4f}")
    print(f"artifacts written to {args.out}")


if __name__ == "__main__":
    main()
