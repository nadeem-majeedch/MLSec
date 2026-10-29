"""LAB-04 starter: complete the targeted and untargeted attacks.

Run from this directory:
    python starter.py --out artifacts

TODO blocks: input gradient, targeted PGD, untargeted FGSM.
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
    """TODO 1: gradient of cross-entropy with respect to X."""
    raise NotImplementedError("TODO 1: implement gradient")


def targeted_pgd(model, X, target, epsilon, alpha=None, steps=50):
    """TODO 2: minimise the target-class loss inside the L-inf ball.

    Descend along the gradient, then project to X +/- epsilon and [0, 1].
    """
    raise NotImplementedError("TODO 2: implement targeted_pgd")


def untargeted_fgsm(model, X, y, epsilon):
    """TODO 3: one-step attack that increases the true-class loss."""
    raise NotImplementedError("TODO 3: implement untargeted_fgsm")


def build_report(metrics):
    lines = [
        "# LAB-04 report — targeted evasion and transfer",
        "",
        f"Clean accuracy: source {metrics['clean_source_accuracy']:.4f}, target {metrics['clean_target_accuracy']:.4f}.",
        "",
        "| epsilon | source targeted | transferred targeted |",
        "|---:|---:|---:|",
    ]
    for row in metrics["targeted"]:
        lines.append(f"| {row['epsilon']:.2f} | {row['source_success']:.4f} | {row['transfer_success']:.4f} |")
    lines += ["", "## Limitations", "", "- Local models only; not evidence about a production service.", ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Starter: targeted evasion and transfer.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    X_train, X_test, y_train, y_test = load_data()
    source = LogisticRegression(max_iter=5000).fit(X_train, y_train)
    target = RandomForestClassifier(n_estimators=300, max_depth=12, random_state=SEED).fit(X_train, y_train)
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
    try:
        for eps in TARGET_EPS:
            X_adv = targeted_pgd(source, X_elig, TARGET_CLASS, eps)
            sp, tp = source.predict(X_adv), target.predict(X_adv)
            metrics["targeted"].append(
                {
                    "epsilon": eps,
                    "source_success": float((sp == TARGET_CLASS).mean()),
                    "transfer_success": float((tp == TARGET_CLASS).mean()),
                    "source_accuracy": float((sp == y_elig).mean()),
                    "target_accuracy": float((tp == y_elig).mean()),
                    "mean_linf": float(np.abs(X_adv - X_elig).max(axis=1).mean()),
                }
            )
        correct = clean_source == y_test
        X_ok, y_ok = X_test[correct], y_test[correct]
        for eps in TRANSFER_EPS:
            X_adv = untargeted_fgsm(source, X_ok, y_ok, eps)
            metrics["transfer"].append(
                {
                    "epsilon": eps,
                    "source_asr": float((source.predict(X_adv) != y_ok).mean()),
                    "target_asr": float((target.predict(X_adv) != y_ok).mean()),
                }
            )
    except NotImplementedError as exc:
        raise SystemExit(f"starter incomplete: {exc}") from exc

    write_json(args.out / "metrics.json", metrics)
    write_json(args.out / "run.json", {"lab": "LAB-04", "seed": SEED, "environment": environment()})
    (args.out / "report.md").write_text(build_report(metrics), encoding="utf-8", newline="\n")
    write_json(args.out / "manifest.json", build_manifest(args.out, ["metrics.json", "run.json", "report.md"]))
    print(f"clean source={metrics['clean_source_accuracy']:.4f} target={metrics['clean_target_accuracy']:.4f}")
    print(f"wrote {args.out / 'metrics.json'}")


if __name__ == "__main__":
    main()
