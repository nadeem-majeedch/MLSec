"""Independent checker for LAB-01B.

Usage:
    python solution.py --out artifacts
    python check_lab01b.py --artifacts artifacts

Exit code 0 means every check passed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

import sys

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.data import make_churn_dataset  # noqa: E402


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def check_manifest(root: Path, manifest: dict) -> None:
    entries = manifest.get("files", [])
    paths = {entry.get("path") for entry in entries}
    required = {"data.csv", "model.joblib", "splits.npz", "metrics.json", "run.json"}
    if required - paths:
        fail(f"manifest does not cover: {sorted(required - paths)}")
    for entry in entries:
        path = root / entry["path"]
        if not path.exists():
            fail(f"manifest entry missing: {entry['path']}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
            fail(f"hash mismatch for {entry['path']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-01B artifacts.")
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()

    root = args.artifacts
    report_path = args.report or root / "report.md"
    metrics = load_json(root / "metrics.json")
    run = load_json(root / "run.json")
    manifest = load_json(root / "manifest.json")
    check_manifest(root, manifest)

    # Rebuild the dataset from the generator and verify the snapshot hash.
    fresh = make_churn_dataset(seed=42)
    with tempfile.TemporaryDirectory() as tmp:
        fresh_path = Path(tmp) / "churn.csv"
        fresh.to_csv(fresh_path, index=False)
        fresh_hash = hashlib.sha256(fresh_path.read_bytes()).hexdigest()
    data_hash = hashlib.sha256((root / "data.csv").read_bytes()).hexdigest()
    if data_hash != fresh_hash:
        fail("data.csv does not match the deterministic generator output")
    if metrics.get("dataset", {}).get("sha256") != data_hash:
        fail("metrics.json dataset hash does not match data.csv")

    df = fresh
    clean = df.drop_duplicates().reset_index(drop=True)
    splits = np.load(root / "splits.npz")
    train_rows, val_rows, test_rows = splits["train_rows"], splits["val_rows"], splits["test_rows"]

    for name, idx in [("train", train_rows), ("val", val_rows), ("test", test_rows)]:
        if idx.min() < 0 or idx.max() >= len(clean):
            fail(f"{name} row index out of range")
        if len(np.unique(idx)) != len(idx):
            fail(f"{name} has duplicate row indices")
    if set(train_rows) & set(test_rows) or set(train_rows) & set(val_rows) or set(val_rows) & set(test_rows):
        fail("row indices overlap across splits")

    train_c = set(splits["train_customers"])
    val_c = set(splits["val_customers"])
    test_c = set(splits["test_customers"])
    if train_c & val_c or train_c & test_c or val_c & test_c:
        fail("customer IDs overlap across splits")
    if set(clean["customer_id"].iloc[test_rows]) - test_c:
        fail("test rows contain customers not listed in the test split")

    # Audit values
    audit = metrics.get("audit", {})
    if not 30 <= audit.get("duplicate_rows", -1) <= 50:
        fail("duplicate_rows outside the expected 30-50 band")
    if audit.get("missing_monthly_spend") != 80:
        fail("missing_monthly_spend should be 80")
    if not 0.85 <= audit.get("late_fee_univariate_auc", -1) <= 0.95:
        fail("late_fee univariate AUC outside 0.85-0.95")
    if audit.get("random_split_customer_overlap", 0) < 80:
        fail("random-split customer overlap is unexpectedly low")

    # Repaired model consistency
    repaired = metrics.get("repaired", {})
    features = repaired.get("features", [])
    if "late_fee_flag" in features:
        fail("late_fee_flag is still in the repaired feature list")
    model = joblib.load(root / "model.joblib")
    test_frame = clean.iloc[test_rows]
    encoded = test_frame.copy()
    encoded["plan_tier"] = encoded["plan_tier"].map({"A": 0, "B": 1, "C": 2})
    encoded["region"] = encoded["region"].map({"N": 0, "S": 1, "E": 2, "W": 3})
    proba = model.predict_proba(encoded[features])[:, 1]
    threshold = float(repaired.get("threshold", -1))
    pred = (proba >= threshold).astype(int)
    y = test_frame["churned"].to_numpy()

    recomputed = {
        "accuracy": accuracy_score(y, pred),
        "precision": precision_score(y, pred, zero_division=0),
        "recall": recall_score(y, pred, zero_division=0),
        "f1": f1_score(y, pred, zero_division=0),
        "roc_auc": roc_auc_score(y, proba),
        "pr_auc": average_precision_score(y, proba),
    }
    saved = repaired.get("test", {})
    for key, value in recomputed.items():
        if abs(value - saved.get(key, -1)) > 1e-6:
            fail(f"repaired {key} mismatch: saved {saved.get(key)} vs recomputed {value}")

    # Validation threshold should be the 80th percentile of validation scores.
    val_frame = clean.iloc[val_rows].copy()
    val_frame["plan_tier"] = val_frame["plan_tier"].map({"A": 0, "B": 1, "C": 2})
    val_frame["region"] = val_frame["region"].map({"N": 0, "S": 1, "E": 2, "W": 3})
    val_proba = model.predict_proba(val_frame[features])[:, 1]
    if abs(np.quantile(val_proba, 0.80) - threshold) > 1e-9:
        fail("threshold is not the 80th percentile of validation scores")

    if not 0.65 <= recomputed["roc_auc"] <= 0.76:
        fail(f"repaired ROC-AUC {recomputed['roc_auc']:.3f} outside 0.65-0.76")
    if not 0.35 <= recomputed["pr_auc"] <= 0.46:
        fail(f"repaired PR-AUC {recomputed['pr_auc']:.3f} outside 0.35-0.46")
    if not 0.40 <= recomputed["recall"] <= 0.52:
        fail(f"repaired recall {recomputed['recall']:.3f} outside 0.40-0.52")

    leaky_auc = metrics.get("leaky_baseline", {}).get("at_0_5", {}).get("roc_auc", 0)
    if leaky_auc < 0.92:
        fail("leaky baseline AUC is lower than expected; check that the leak and preprocessing leak are reproduced")
    if leaky_auc - recomputed["roc_auc"] < 0.15:
        fail("leaky and repaired AUCs are too close; the leak may not have been reproduced")

    cv = repaired.get("group_cv_pr_auc", {})
    if not 0.30 <= cv.get("mean", -1) <= 0.55:
        fail("grouped CV PR-AUC outside 0.30-0.55")

    if run.get("environment", {}).get("python") is None:
        fail("run.json does not record the Python version")

    if not report_path.exists():
        fail(f"missing report {report_path}")
    report = report_path.read_text(encoding="utf-8")
    for heading in ["## Threat model", "## Data audit", "## Results", "## Limitations", "## Reproduction"]:
        if heading not in report:
            fail(f"report is missing heading: {heading}")

    print("PASS manifest hashes and deterministic dataset")
    print("PASS grouped splits have no customer overlap")
    print("PASS leaky baseline reproduces the inflation")
    print(f"PASS repaired model reproduces metrics: AUC={recomputed['roc_auc']:.4f}, PR-AUC={recomputed['pr_auc']:.4f}")
    print(f"PASS threshold equals validation 80th percentile: {threshold:.4f}")
    print("PASS report is complete")
    print("LAB-01B CHECK PASSED")


if __name__ == "__main__":
    main()
