"""LAB-01 reference solution: reproducible baseline on scikit-learn digits.

Run from this directory:
    python solution.py --out artifacts

Artifacts: model.joblib, splits.npz, metrics.json, run.json, manifest.json, report.md.
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


def evaluate(model: Pipeline, X: np.ndarray, y: np.ndarray) -> dict:
    pred = model.predict(X)
    return {
        "n": int(len(y)),
        "accuracy": float(accuracy_score(y, pred)),
        "macro_f1": float(f1_score(y, pred, average="macro")),
        "per_class_recall": [float(v) for v in recall_score(y, pred, average=None)],
        "confusion_matrix": confusion_matrix(y, pred).tolist(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the LAB-01 baseline.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    X, y = load_digits(return_X_y=True)
    idx_train, idx_val, idx_test = split_indices(y, args.seed)
    X_train, y_train = X[idx_train], y[idx_train]
    X_val, y_val = X[idx_val], y[idx_val]
    X_test, y_test = X[idx_test], y[idx_test]

    model = Pipeline(
        [
            ("scale", StandardScaler()),
            ("clf", LogisticRegression(max_iter=2000, random_state=args.seed)),
        ]
    )
    model.fit(X_train, y_train)

    metrics = {
        "dataset": {
            "name": "sklearn.datasets.load_digits",
            "n_samples": int(len(y)),
            "n_features": int(X.shape[1]),
            "n_classes": int(len(np.unique(y))),
        },
        "split": {
            "train": int(len(y_train)),
            "val": int(len(y_val)),
            "test": int(len(y_test)),
            "seed": args.seed,
            "strategy": "stratified 60/20/20",
        },
        "model": {
            "name": "StandardScaler + LogisticRegression",
            "max_iter": 2000,
            "random_state": args.seed,
        },
        "validation": evaluate(model, X_val, y_val),
        "test": evaluate(model, X_test, y_test),
    }

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out / "model.joblib")
    np.savez_compressed(
        out / "splits.npz",
        train=idx_train,
        val=idx_val,
        test=idx_test,
    )
    write_json(out / "metrics.json", metrics)
    write_json(
        out / "run.json",
        {
            "command": "python solution.py",
            "seed": args.seed,
            "environment": environment(),
            "dataset": metrics["dataset"],
            "split": metrics["split"],
            "model": metrics["model"],
        },
    )
    write_json(
        out / "manifest.json",
        build_manifest(out, ["model.joblib", "splits.npz", "metrics.json", "run.json"]),
    )

    test = metrics["test"]
    report = f"""# LAB-01 Report

## Threat model
This baseline is not an attack target. It establishes a reproducible reference for later evasion and poisoning labs. The asset is the integrity of the reported metric; the adversary is any source of unreproducible or leaky evaluation.

## Setup
- Data: scikit-learn `load_digits` ({metrics["dataset"]["n_samples"]} samples, {metrics["dataset"]["n_features"]} features, {metrics["dataset"]["n_classes"]} classes).
- Split: stratified 60/20/20, seed {args.seed} ({metrics["split"]["train"]}/{metrics["split"]["val"]}/{metrics["split"]["test"]}).
- Model: StandardScaler followed by logistic regression (`max_iter=2000`).

## Results
- Validation accuracy: {metrics["validation"]["accuracy"]:.4f}; macro F1: {metrics["validation"]["macro_f1"]:.4f}.
- Test accuracy: {test["accuracy"]:.4f}; macro F1: {test["macro_f1"]:.4f}.
- Test per-class recall: {", ".join(f"{v:.3f}" for v in test["per_class_recall"])}.

## Limitations
The split is random, so it does not test temporal or group generalization. The dataset is small and clean; it does not represent production noise. Results are conditional on the pinned environment.

## Reproduction
Run `python solution.py --out artifacts`, then `python check_lab01.py --artifacts artifacts`. Compare `metrics.json` and verify `manifest.json` hashes.
"""
    (out / "report.md").write_text(report, encoding="utf-8", newline="\n")

    print(f"accuracy={test['accuracy']:.4f} macro_f1={test['macro_f1']:.4f}")
    print(f"artifacts written to {out}")


if __name__ == "__main__":
    main()
