"""LAB-05 reference solution: indiscriminate label-flip poisoning curve.

Run from this directory:
    python solution.py --out artifacts
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

RATES = [0.0, 0.05, 0.10, 0.20, 0.30]
SEED = 42


def load_data():
    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    return train_test_split(X, y, test_size=0.3, random_state=SEED, stratify=y)


def poison_labels(y, rate, seed=SEED):
    """Flip a random subset to the next class (cyclically)."""
    y_poisoned = y.copy()
    count = int(round(rate * len(y)))
    rng = np.random.default_rng(seed)
    chosen = rng.choice(len(y), size=count, replace=False)
    y_poisoned[chosen] = (y_poisoned[chosen] + 1) % 10
    return y_poisoned, chosen


def build_report(metrics):
    lines = [
        "# LAB-05 report — label-flip poisoning",
        "",
        "Poisoned rows are training rows whose label is changed to the next class.",
        "Clean test labels are never modified.",
        "",
        "| poison rate | poisoned rows | clean accuracy | macro F1 |",
        "|---:|---:|---:|---:|",
    ]
    for row in metrics["curve"]:
        lines.append(
            f"| {row['rate']:.2f} | {row['poisoned_rows']} | {row['accuracy']:.4f} | {row['macro_f1']:.4f} |"
        )
    lines += [
        "",
        "## Threat model",
        "",
        "The attacker can modify labels in the training pipeline but not features or test data.",
        "The attacker does not know the exact test set; the goal is a broad accuracy loss.",
        "",
        "## Limitations",
        "",
        "- One dataset, one linear model, one flip rule.",
        "- A 30% flip budget is large; smaller budgets are the realistic case.",
        "- The curve measures availability, not a targeted misclassification.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Label-flip poisoning curve.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    X_train, X_test, y_train, y_test = load_data()
    metrics = {"rates": RATES, "curve": [], "dataset": "sklearn.datasets.load_digits"}
    for rate in RATES:
        y_poisoned, chosen = poison_labels(y_train, rate)
        model = LogisticRegression(max_iter=3000).fit(X_train, y_poisoned)
        pred = model.predict(X_test)
        metrics["curve"].append(
            {
                "rate": rate,
                "poisoned_rows": int(len(chosen)),
                "accuracy": float(accuracy_score(y_test, pred)),
                "macro_f1": float(f1_score(y_test, pred, average="macro")),
            }
        )

    write_json(args.out / "metrics.json", metrics)
    write_json(
        args.out / "run.json",
        {"lab": "LAB-05", "seed": SEED, "flip_rule": "next class modulo 10", "environment": environment()},
    )
    (args.out / "report.md").write_text(build_report(metrics), encoding="utf-8", newline="\n")
    write_json(
        args.out / "manifest.json",
        build_manifest(args.out, ["metrics.json", "run.json", "report.md"]),
    )
    for row in metrics["curve"]:
        print(
            f"rate={row['rate']:.2f} poisoned={row['poisoned_rows']} "
            f"accuracy={row['accuracy']:.4f} macro_f1={row['macro_f1']:.4f}"
        )
    print(f"artifacts written to {args.out}")


if __name__ == "__main__":
    main()
