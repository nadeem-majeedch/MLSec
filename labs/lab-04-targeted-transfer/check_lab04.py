"""Independent checker for LAB-04.

Usage:
    python solution.py --out artifacts
    python check_lab04.py --artifacts artifacts
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

TARGET_CLASS = 3


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-04 artifacts.")
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    root = args.artifacts

    metrics = load_json(root / "metrics.json")
    run = load_json(root / "run.json")
    manifest = load_json(root / "manifest.json")
    if not (root / "report.md").exists():
        fail("missing report.md")
    required = {"metrics.json", "run.json", "report.md"}
    covered = {entry["path"] for entry in manifest.get("files", [])}
    if not required <= covered:
        fail(f"manifest does not cover {sorted(required - covered)}")

    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    source = LogisticRegression(max_iter=5000).fit(X_train, y_train)
    target = RandomForestClassifier(n_estimators=300, max_depth=12, random_state=42, n_jobs=-1).fit(
        X_train, y_train
    )
    source_acc = float((source.predict(X_test) == y_test).mean())
    target_acc = float((target.predict(X_test) == y_test).mean())
    if abs(source_acc - metrics["clean_source_accuracy"]) > 0.005:
        fail("clean source accuracy does not reproduce")
    if abs(target_acc - metrics["clean_target_accuracy"]) > 0.005:
        fail("clean target accuracy does not reproduce")
    if metrics.get("target_class") != TARGET_CLASS:
        fail("wrong target class")

    targeted = {row["epsilon"]: row for row in metrics.get("targeted", [])}
    if set(targeted) != {0.1, 0.2, 0.3}:
        fail("targeted results must cover epsilon 0.1, 0.2, 0.3")
    for eps, row in targeted.items():
        if row["mean_linf"] > eps + 1e-6:
            fail(f"targeted perturbation exceeds budget at eps={eps}")
        if row["source_success"] < 0.95 and eps == 0.3:
            fail("targeted attack on the source is too weak at eps=0.3")
        if row["transfer_success"] < 0.55 and eps == 0.3:
            fail("targeted transfer is too weak at eps=0.3")
        if row["source_success"] < row["transfer_success"] - 1e-9:
            fail("source success should not be below transfer success")

    transfer = {row["epsilon"]: row for row in metrics.get("transfer", [])}
    if set(transfer) != {0.05, 0.1, 0.2, 0.3}:
        fail("transfer results must cover epsilon 0.05, 0.1, 0.2, 0.3")
    if transfer[0.2]["target_asr"] < 0.7:
        fail("untargeted transfer at eps=0.2 is too weak")
    previous = -1.0
    for eps in sorted(transfer):
        row = transfer[eps]
        if row["target_asr"] < previous - 0.03:
            fail("transfer ASR is not broadly monotone")
        previous = row["target_asr"]

    text = (root / "report.md").read_text(encoding="utf-8").lower()
    for phrase in ("threat model", "limitations", "transfer"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print(f"PASS clean accuracies reproduce: source={source_acc:.4f} target={target_acc:.4f}")
    print(f"PASS targeted source success at eps=0.3: {targeted[0.3]['source_success']:.4f}")
    print(f"PASS targeted transfer at eps=0.3: {targeted[0.3]['transfer_success']:.4f}")
    print(f"PASS untargeted transfer at eps=0.2: {transfer[0.2]['target_asr']:.4f}")
    print("PASS report contains threat model and limitations")
    print("LAB-04 CHECK PASSED")


if __name__ == "__main__":
    main()
