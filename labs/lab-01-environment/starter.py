"""LAB-01 starter: reproducible baseline on scikit-learn digits.

Complete the three TODO blocks, then run:
    python starter.py --out artifacts

Do not copy the reference solution. If you get stuck, read the lab brief at
docs/labs/lab-01.md and the checking guide in CHECKING.md.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import joblib
import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402


def split_indices(y: np.ndarray, seed: int = 42):
    idx = np.arange(len(y))
    idx_rest, idx_test = train_test_split(
        idx, test_size=0.20, stratify=y, random_state=seed
    )
    idx_train, idx_val = train_test_split(
        idx_rest, test_size=0.25, stratify=y[idx_rest], random_state=seed
    )
    return idx_train, idx_val, idx_test


def build_model(seed: int = 42) -> Pipeline:
    """TODO 1: return a Pipeline with StandardScaler and LogisticRegression.

    Use max_iter=2000 and random_state=seed.
    """
    raise NotImplementedError("TODO 1: build the model pipeline")


def evaluate(model: Pipeline, X: np.ndarray, y: np.ndarray) -> dict:
    pred = model.predict(X)
    return {
        "n": int(len(y)),
        "accuracy": float(accuracy_score(y, pred)),
        "macro_f1": float(f1_score(y, pred, average="macro")),
        "per_class_recall": [float(v) for v in recall_score(y, pred, average=None)],
        "confusion_matrix": confusion_matrix(y, pred).tolist(),
    }


def write_artifacts(
    out: Path,
    model: Pipeline,
    idx_train: np.ndarray,
    idx_val: np.ndarray,
    idx_test: np.ndarray,
    metrics: dict,
    seed: int,
) -> None:
    """TODO 2: write model.joblib, splits.npz, metrics.json, run.json, manifest.json.

    The manifest must cover model.joblib, splits.npz, metrics.json, and run.json.
    Use the helpers imported above.
    """
    raise NotImplementedError("TODO 2: write the artifact set")


def write_report(out: Path, metrics: dict) -> None:
    """TODO 3: write report.md with these headings.

    # LAB-01 Report
    ## Threat model
    ## Setup
    ## Results
    ## Limitations
    ## Reproduction
    """
    raise NotImplementedError("TODO 3: write the report")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the LAB-01 baseline.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    X, y = load_digits(return_X_y=True)
    idx_train, idx_val, idx_test = split_indices(y, args.seed)

    model = build_model(args.seed)
    model.fit(X[idx_train], y[idx_train])

    metrics = {
        "dataset": {
            "name": "sklearn.datasets.load_digits",
            "n_samples": int(len(y)),
            "n_features": int(X.shape[1]),
            "n_classes": int(len(np.unique(y))),
        },
        "split": {
            "train": int(len(idx_train)),
            "val": int(len(idx_val)),
            "test": int(len(idx_test)),
            "seed": args.seed,
            "strategy": "stratified 60/20/20",
        },
        "model": {
            "name": "StandardScaler + LogisticRegression",
            "max_iter": 2000,
            "random_state": args.seed,
        },
        "validation": evaluate(model, X[idx_val], y[idx_val]),
        "test": evaluate(model, X[idx_test], y[idx_test]),
    }

    write_artifacts(
        args.out, model, idx_train, idx_val, idx_test, metrics, args.seed
    )
    write_report(args.out, metrics)
    print(f"accuracy={metrics['test']['accuracy']:.4f} macro_f1={metrics['test']['macro_f1']:.4f}")
    print(f"artifacts written to {args.out}")


if __name__ == "__main__":
    main()
