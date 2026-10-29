"""LAB-06 reference solution: targeted poisoning and reference-set screening.

Run from this directory:
    python solution.py --out artifacts
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

SEED = 7
N_POISON = 30
TARGET = np.array([[0.1, 0.0]])
REFERENCE_SIZE = 150
TRAIN_START = 150
TRAIN_STOP = 500


def make_data(n=600, seed=SEED):
    rng = np.random.default_rng(seed)
    X = np.vstack(
        [rng.normal([-1.2, 0.0], 1.0, (n // 2, 2)), rng.normal([1.2, 0.0], 1.0, (n - n // 2, 2))]
    )
    y = np.array([0] * (n // 2) + [1] * (n - n // 2))
    order = rng.permutation(n)
    return X[order], y[order], rng


def poison_training_set(X_train, y_train, rng):
    poisoned = TARGET + rng.normal(0.0, 0.05, (N_POISON, 2))
    X_poisoned = np.vstack([X_train, poisoned])
    y_poisoned = np.concatenate([y_train, np.zeros(N_POISON, dtype=int)])
    is_poison = np.zeros(len(X_poisoned), dtype=bool)
    is_poison[len(X_train):] = True
    return X_poisoned, y_poisoned, is_poison


def screen_with_reference(X_train, y_train, X_reference, y_reference, threshold=0.6):
    """Flag rows whose label disagrees with a k-NN model fit on trusted data."""
    reference_model = KNeighborsClassifier(n_neighbors=9).fit(X_reference, y_reference)
    probability = reference_model.predict_proba(X_train)
    agreement = probability[np.arange(len(X_train)), y_train]
    return agreement < threshold, agreement


def build_report(metrics):
    lines = [
        "# LAB-06 report — targeted poisoning and screening",
        "",
        "Goal: flip one chosen test prediction by adding a small cluster of mislabelled rows.",
        "The reference set is assumed to be clean; that assumption is the defense's main limit.",
        "",
        "| Quantity | Clean | Poisoned | After screening |",
        "|---|---:|---:|---:|",
        f"| Target prediction | {metrics['clean']['target_prediction']} | "
        f"{metrics['poisoned']['target_prediction']} | {metrics['defended']['target_prediction']} |",
        f"| Target P(class 1) | {metrics['clean']['target_probability']:.4f} | "
        f"{metrics['poisoned']['target_probability']:.4f} | {metrics['defended']['target_probability']:.4f} |",
        f"| Test accuracy | {metrics['clean']['accuracy']:.4f} | "
        f"{metrics['poisoned']['accuracy']:.4f} | {metrics['defended']['accuracy']:.4f} |",
        "",
        "## Screening",
        "",
        f"Flagged {metrics['screening']['flagged']} rows, catching "
        f"{metrics['screening']['poison_caught']} of {N_POISON} poisons; "
        f"{metrics['screening']['clean_flagged']} clean rows were also removed.",
        "",
        "## Limitations",
        "",
        "- The clean reference set is a strong assumption; an attacker who can poison it breaks the defense.",
        "- Removing flagged rows changes the training distribution and can hurt boundary cases.",
        "- One synthetic dataset and one target point do not establish general effectiveness.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Targeted poisoning and screening.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    X, y, rng = make_data()
    X_ref, y_ref = X[:REFERENCE_SIZE], y[:REFERENCE_SIZE]
    X_train, y_train = X[TRAIN_START:TRAIN_STOP], y[TRAIN_START:TRAIN_STOP]
    X_test, y_test = X[TRAIN_STOP:], y[TRAIN_STOP:]

    clean_model = LogisticRegression().fit(X_train, y_train)
    X_poisoned, y_poisoned, is_poison = poison_training_set(X_train, y_train, rng)
    poisoned_model = LogisticRegression().fit(X_poisoned, y_poisoned)

    flags, agreement = screen_with_reference(X_poisoned, y_poisoned, X_ref, y_ref)
    defended_model = LogisticRegression().fit(X_poisoned[~flags], y_poisoned[~flags])

    def view(model):
        return {
            "target_prediction": int(model.predict(TARGET)[0]),
            "target_probability": float(model.predict_proba(TARGET)[0, 1]),
            "accuracy": float(accuracy_score(y_test, model.predict(X_test))),
        }

    metrics = {
        "clean": view(clean_model),
        "poisoned": view(poisoned_model),
        "defended": view(defended_model),
        "screening": {
            "flagged": int(flags.sum()),
            "poison_caught": int((flags & is_poison).sum()),
            "clean_flagged": int((flags & ~is_poison).sum()),
            "threshold": 0.6,
            "reference_size": REFERENCE_SIZE,
        },
        "poison_budget": N_POISON,
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
        "target": TARGET.tolist(),
        "dataset": "synthetic 2-D Gaussian mixture",
    }

    write_json(args.out / "metrics.json", metrics)
    write_json(
        args.out / "run.json",
        {
            "lab": "LAB-06",
            "seed": SEED,
            "poison_budget": N_POISON,
            "reference_size": REFERENCE_SIZE,
            "environment": environment(),
        },
    )
    (args.out / "report.md").write_text(build_report(metrics), encoding="utf-8", newline="\n")
    write_json(
        args.out / "manifest.json",
        build_manifest(args.out, ["metrics.json", "run.json", "report.md"]),
    )
    print(
        f"clean target={metrics['clean']['target_prediction']} "
        f"({metrics['clean']['target_probability']:.4f}), acc={metrics['clean']['accuracy']:.4f}"
    )
    print(
        f"poisoned target={metrics['poisoned']['target_prediction']} "
        f"({metrics['poisoned']['target_probability']:.4f}), acc={metrics['poisoned']['accuracy']:.4f}"
    )
    print(
        f"screening flagged={metrics['screening']['flagged']} "
        f"caught={metrics['screening']['poison_caught']} clean_flagged={metrics['screening']['clean_flagged']}"
    )
    print(
        f"defended target={metrics['defended']['target_prediction']} "
        f"({metrics['defended']['target_probability']:.4f}), acc={metrics['defended']['accuracy']:.4f}"
    )
    print(f"artifacts written to {args.out}")


if __name__ == "__main__":
    main()
