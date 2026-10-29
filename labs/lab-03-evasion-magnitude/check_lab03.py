"""Independent checker for LAB-03.

Usage:
    python solution.py --out artifacts
    python check_lab03.py --artifacts artifacts

Exit code 0 means every check passed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-03 artifacts.")
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    root = args.artifacts

    metrics = load_json(root / "metrics.json")
    run = load_json(root / "run.json")
    manifest = load_json(root / "manifest.json")
    report = root / "report.md"
    if not report.exists():
        fail("missing report.md")

    required = {"metrics.json", "run.json", "report.md"}
    paths = {entry["path"] for entry in manifest.get("files", [])}
    if not required <= paths:
        fail(f"manifest does not cover {sorted(required - paths)}")
    if run.get("lab") != "LAB-03":
        fail("run.json lab is not LAB-03")

    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    model = LogisticRegression(max_iter=5000, C=1.0).fit(X_train, y_train)
    clean_acc = float((model.predict(X_test) == y_test).mean())
    if abs(clean_acc - metrics["clean_accuracy"]) > 0.005:
        fail(f"clean accuracy mismatch: {clean_acc:.4f} vs {metrics['clean_accuracy']:.4f}")
    if metrics["test_size"] != len(y_test):
        fail("test_size does not match the deterministic split")

    for method in ("fgsm", "pgd"):
        rows = metrics.get(method, [])
        if len(rows) != 5:
            fail(f"{method} must contain five epsilon rows")
        previous = -1.0
        for row in rows:
            eps = float(row["epsilon"])
            if row["asr"] < previous - 0.02:
                fail(f"{method} ASR is not monotone at epsilon={eps}")
            previous = row["asr"]
            if row["mean_linf"] > eps + 1e-6:
                fail(f"{method} exceeds the L-inf budget at epsilon={eps}")
            if row["max_linf"] > eps + 1e-6:
                fail(f"{method} max perturbation exceeds epsilon={eps}")
            if not 0.0 <= row["asr"] <= 1.0 or not 0.0 <= row["robust_accuracy"] <= 1.0:
                fail(f"{method} metric outside [0,1] at epsilon={eps}")

    fgsm = {row["epsilon"]: row for row in metrics["fgsm"]}
    pgd = {row["epsilon"]: row for row in metrics["pgd"]}
    if fgsm[0.20]["asr"] < 0.85:
        fail(f"FGSM at epsilon=0.20 is too weak: {fgsm[0.20]['asr']:.4f}")
    if pgd[0.20]["asr"] < 0.93:
        fail(f"PGD at epsilon=0.20 is too weak: {pgd[0.20]['asr']:.4f}")
    if pgd[0.10]["asr"] + 0.02 < fgsm[0.10]["asr"]:
        fail("PGD should not be materially weaker than FGSM at the same budget")

    text = report.read_text(encoding="utf-8").lower()
    for phrase in ("limitations", "clean accuracy", "asr"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print(f"PASS clean accuracy reproduces: {clean_acc:.4f}")
    print("PASS five budgets, monotone ASR, and L-inf bounds")
    print(f"PASS FGSM epsilon=0.20 ASR={fgsm[0.20]['asr']:.4f}")
    print(f"PASS PGD epsilon=0.20 ASR={pgd[0.20]['asr']:.4f}")
    print("PASS report contains the required sections")
    print("LAB-03 CHECK PASSED")


if __name__ == "__main__":
    main()
