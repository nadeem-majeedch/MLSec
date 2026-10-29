"""LAB-04 reference solution: targeted evasion and transfer to a black-box model.

Run from this directory:
    python solution.py --out artifacts
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

SEED = 42
TARGET_CLASS = 3
TARGET_EPS = [0.10, 0.20, 0.30]
TRANSFER_EPS = [0.05, 0.10, 0.20, 0.30]


def load_data():
    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    return train_test_split(X, y, test_size=0.3, random_state=SEED, stratify=y)


def probabilities(model, X):
    scores = X @ model.coef_.T + model.intercept_
    scores -= scores.max(axis=1, keepdims=True)
    exp = np.exp(scores)
    return exp / exp.sum(axis=1, keepdims=True)


def gradient(model, X, labels):
    p = probabilities(model, X)
    p[np.arange(len(labels)), labels] -= 1.0
    return p @ model.coef_


def targeted_pgd(model, X, target, epsilon, alpha=None, steps=50):
    """Minimise the loss for ``target`` while staying within an L-inf ball."""
    alpha = alpha or epsilon / 10.0
    x_adv = X.copy()
    labels = np.full(len(X), target, dtype=int)
    for _ in range(steps):
        grad = gradient(model, x_adv, labels)
        x_adv = np.clip(x_adv - alpha * np.sign(grad), X - epsilon, X + epsilon)
        x_adv = np.clip(x_adv, 0.0, 1.0)
    return x_adv


def untargeted_fgsm(model, X, y, epsilon):
    return np.clip(X + epsilon * np.sign(gradient(model, X, y)), 0.0, 1.0)


def build_report(metrics):
    lines = [
        "# LAB-04 report — targeted evasion and transfer",
        "",
        f"Source: logistic regression (white-box). Target: random forest (black-box, used only for evaluation).",
        f"Target class: {TARGET_CLASS}. Clean accuracy: source {metrics['clean_source_accuracy']:.4f}, "
        f"target {metrics['clean_target_accuracy']:.4f}.",
        "",
        "## Targeted attack",
        "",
        "| epsilon | source success | transferred success | source accuracy | target accuracy |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in metrics["targeted"]:
        lines.append(
            f"| {row['epsilon']:.2f} | {row['source_success']:.4f} | {row['transfer_success']:.4f} | "
            f"{row['source_accuracy']:.4f} | {row['target_accuracy']:.4f} |"
        )
    lines += [
        "",
        "## Untargeted transfer",
        "",
        "| epsilon | source ASR | target ASR |",
        "|---:|---:|---:|",
    ]
    for row in metrics["transfer"]:
        lines.append(
            f"| {row['epsilon']:.2f} | {row['source_asr']:.4f} | {row['target_asr']:.4f} |"
        )
    lines += [
        "",
        "## Threat model",
        "",
        "The attacker knows the source architecture, weights, and gradient, but not the target model.",
        "The target is queried only for evaluation; no target queries are used to build the perturbation.",
        "",
        "## Limitations",
        "",
        "- One source and one target architecture; transfer rates are architecture- and data-dependent.",
        "- Transfer success is not evidence that a remote production system is vulnerable.",
        "- The black-box model is a local stand-in, not a real service.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Targeted evasion and transfer.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    X_train, X_test, y_train, y_test = load_data()
    source = LogisticRegression(max_iter=5000).fit(X_train, y_train)
    target = RandomForestClassifier(n_estimators=300, max_depth=12, random_state=SEED, n_jobs=-1).fit(
        X_train, y_train
    )

    clean_source = source.predict(X_test)
    eligible = (y_test != TARGET_CLASS) & (clean_source == y_test)
    X_elig, y_elig = X_test[eligible], y_test[eligible]

    metrics = {
        "clean_source_accuracy": float((clean_source == y_test).mean()),
        "clean_target_accuracy": float((target.predict(X_test) == y_test).mean()),
        "target_class": TARGET_CLASS,
        "targeted_n": int(len(y_elig)),
        "targeted": [],
        "transfer": [],
        "dataset": "sklearn.datasets.load_digits (8x8, pixels/16)",
    }
    for eps in TARGET_EPS:
        X_adv = targeted_pgd(source, X_elig, TARGET_CLASS, eps)
        source_pred = source.predict(X_adv)
        target_pred = target.predict(X_adv)
        metrics["targeted"].append(
            {
                "epsilon": eps,
                "source_success": float((source_pred == TARGET_CLASS).mean()),
                "transfer_success": float((target_pred == TARGET_CLASS).mean()),
                "source_accuracy": float((source_pred == y_elig).mean()),
                "target_accuracy": float((target_pred == y_elig).mean()),
                "mean_linf": float(np.abs(X_adv - X_elig).max(axis=1).mean()),
            }
        )

    source_correct = clean_source == y_test
    X_ok, y_ok = X_test[source_correct], y_test[source_correct]
    for eps in TRANSFER_EPS:
        X_adv = untargeted_fgsm(source, X_ok, y_ok, eps)
        metrics["transfer"].append(
            {
                "epsilon": eps,
                "source_asr": float((source.predict(X_adv) != y_ok).mean()),
                "target_asr": float((target.predict(X_adv) != y_ok).mean()),
            }
        )

    write_json(args.out / "metrics.json", metrics)
    write_json(
        args.out / "run.json",
        {
            "lab": "LAB-04",
            "seed": SEED,
            "target_class": TARGET_CLASS,
            "targeted_epsilons": TARGET_EPS,
            "transfer_epsilons": TRANSFER_EPS,
            "environment": environment(),
        },
    )
    (args.out / "report.md").write_text(build_report(metrics), encoding="utf-8", newline="\n")
    write_json(
        args.out / "manifest.json",
        build_manifest(args.out, ["metrics.json", "run.json", "report.md"]),
    )
    print(f"clean source={metrics['clean_source_accuracy']:.4f} target={metrics['clean_target_accuracy']:.4f}")
    for row in metrics["targeted"]:
        print(
            f"targeted eps={row['epsilon']:.2f} source={row['source_success']:.4f} "
            f"transfer={row['transfer_success']:.4f}"
        )
    for row in metrics["transfer"]:
        print(f"transfer eps={row['epsilon']:.2f} source={row['source_asr']:.4f} target={row['target_asr']:.4f}")
    print(f"artifacts written to {args.out}")


if __name__ == "__main__":
    main()
