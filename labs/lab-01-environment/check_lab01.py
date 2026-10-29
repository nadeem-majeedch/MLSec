"""Independent checker for LAB-01.

Usage:
    python solution.py --out artifacts
    python check_lab01.py --artifacts artifacts

Exit code 0 means every check passed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def check_manifest(root: Path, manifest: dict) -> None:
    import hashlib

    files = manifest.get("files", [])
    paths = {entry.get("path") for entry in files}
    required = {"model.joblib", "splits.npz", "metrics.json", "run.json"}
    missing = required - paths
    if missing:
        fail(f"manifest does not cover: {sorted(missing)}")
    for entry in files:
        path = root / entry["path"]
        if not path.exists():
            fail(f"manifest entry missing on disk: {entry['path']}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != entry["sha256"]:
            fail(f"hash mismatch for {entry['path']}")
        if path.stat().st_size != entry["bytes"]:
            fail(f"size mismatch for {entry['path']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-01 artifacts.")
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()

    root = args.artifacts
    report_path = args.report or root / "report.md"
    metrics = load_json(root / "metrics.json")
    run = load_json(root / "run.json")
    manifest = load_json(root / "manifest.json")

    check_manifest(root, manifest)

    X, y = load_digits(return_X_y=True)
    splits = np.load(root / "splits.npz")
    idx_train, idx_val, idx_test = splits["train"], splits["val"], splits["test"]

    for name, idx in [("train", idx_train), ("val", idx_val), ("test", idx_test)]:
        if len(idx) == 0:
            fail(f"{name} split is empty")
        if len(np.unique(idx)) != len(idx):
            fail(f"{name} split has duplicate indices")

    if set(idx_train) & set(idx_val) or set(idx_train) & set(idx_test) or set(idx_val) & set(idx_test):
        fail("split indices overlap")
    if len(idx_train) + len(idx_val) + len(idx_test) != len(y):
        fail("splits do not cover every row exactly once")

    expected_sizes = {"train": 1077, "val": 360, "test": 360}
    actual_sizes = {"train": len(idx_train), "val": len(idx_val), "test": len(idx_test)}
    if actual_sizes != expected_sizes:
        fail(f"split sizes {actual_sizes} != {expected_sizes}")

    model = joblib.load(root / "model.joblib")
    pred = model.predict(X[idx_test])
    re_acc = float(accuracy_score(y[idx_test], pred))
    re_f1 = float(f1_score(y[idx_test], pred, average="macro"))
    saved = metrics.get("test", {})

    if abs(re_acc - saved.get("accuracy", -1)) > 1e-9:
        fail(f"test accuracy mismatch: saved {saved.get('accuracy')} vs recomputed {re_acc}")
    if abs(re_f1 - saved.get("macro_f1", -1)) > 1e-9:
        fail(f"test macro F1 mismatch: saved {saved.get('macro_f1')} vs recomputed {re_f1}")
    if confusion_matrix(y[idx_test], pred).tolist() != saved.get("confusion_matrix"):
        fail("confusion matrix does not match the saved model")

    if not 0.94 <= re_acc <= 0.975:
        fail(f"test accuracy {re_acc:.4f} outside the expected 0.94-0.975 band")
    if not 0.94 <= re_f1 <= 0.975:
        fail(f"test macro F1 {re_f1:.4f} outside the expected 0.94-0.975 band")
    if metrics.get("split", {}).get("seed") != 42:
        fail("split seed is not 42")
    if run.get("environment", {}).get("python") is None:
        fail("run.json does not record the Python version")

    if not report_path.exists():
        fail(f"missing report {report_path}")
    report = report_path.read_text(encoding="utf-8")
    for heading in ["## Threat model", "## Setup", "## Results", "## Limitations", "## Reproduction"]:
        if heading not in report:
            fail(f"report is missing heading: {heading}")

    print("PASS manifest hashes and sizes")
    print("PASS splits cover every row once with no overlap")
    print("PASS model reproduces saved test metrics")
    print(f"PASS metrics in range: accuracy={re_acc:.4f}, macro_f1={re_f1:.4f}")
    print("PASS report is complete")
    print("LAB-01 CHECK PASSED")


if __name__ == "__main__":
    main()
