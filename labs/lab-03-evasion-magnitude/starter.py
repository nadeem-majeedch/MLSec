"""LAB-03 starter: complete the attack functions, then run the experiment.

Run from this directory:
    python starter.py --out artifacts

Three TODO blocks: input_gradient, fgsm_attack, pgd_attack. Do not change the
metric definitions; they are part of the task contract.
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


def fit_model(X_train, y_train):
    return LogisticRegression(max_iter=5000, C=1.0).fit(X_train, y_train)


def probabilities(model, X):
    scores = X @ model.coef_.T + model.intercept_
    scores -= scores.max(axis=1, keepdims=True)
    exp = np.exp(scores)
    return exp / exp.sum(axis=1, keepdims=True)


def input_gradient(model, X, y):
    """TODO 1: return d(mean cross-entropy)/dX, shape (n_samples, n_features).

    Hint: start from probabilities(model, X), subtract 1 from the true-class
    column, then multiply by the model coefficients.
    """
    raise NotImplementedError("TODO 1: implement input_gradient")


def fgsm_attack(model, X, y, epsilon):
    """TODO 2: one-step sign attack with pixel clipping to [0, 1]."""
    raise NotImplementedError("TODO 2: implement fgsm_attack")


def pgd_attack(model, X, y, epsilon, alpha=None, steps=40, restarts=3, seed=SEED):
    """TODO 3: iterative sign attack projected into the epsilon ball.

    Start from X (and optional random starts), step by alpha, clip to
    [X - epsilon, X + epsilon] and to [0, 1]. Keep the most successful restart.
    """
    raise NotImplementedError("TODO 3: implement pgd_attack")


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Starter: evasion versus L-inf budget.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    X_train, X_test, y_train, y_test = load_data()
    model = fit_model(X_train, y_train)
    clean_correct = model.predict(X_test) == y_test

    metrics = {
        "clean_accuracy": float(clean_correct.mean()),
        "clean_correct": int(clean_correct.sum()),
        "test_size": int(len(y_test)),
        "epsilons": EPSILONS,
        "fgsm": [],
        "pgd": [],
        "dataset": "sklearn.datasets.load_digits (8x8, pixels/16)",
    }
    try:
        for eps in EPSILONS:
            metrics["fgsm"].append(
                {
                    "epsilon": eps,
                    **summarize(model, X_test, y_test, fgsm_attack(model, X_test, y_test, eps), clean_correct),
                }
            )
            metrics["pgd"].append(
                {
                    "epsilon": eps,
                    **summarize(model, X_test, y_test, pgd_attack(model, X_test, y_test, eps), clean_correct),
                }
            )
    except NotImplementedError as exc:
        raise SystemExit(f"starter incomplete: {exc}") from exc

    write_json(args.out / "metrics.json", metrics)
    write_json(
        args.out / "run.json",
        {
            "lab": "LAB-03",
            "seed": SEED,
            "environment": environment(),
            "note": "starter completed by learner",
        },
    )
    write_json(
        args.out / "manifest.json",
        build_manifest(args.out, ["metrics.json", "run.json"]),
    )
    print(f"clean accuracy={metrics['clean_accuracy']:.4f}")
    print(f"wrote {args.out / 'metrics.json'}")


if __name__ == "__main__":
    main()
