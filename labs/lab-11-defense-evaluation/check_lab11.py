"""Independent checker for LAB-11.

Usage:
    python solution.py --out artifacts
    python check_lab11.py --artifacts artifacts

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

TOL = 0.03


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def close(actual: float, expected: float, tol: float = TOL, label: str = "") -> None:
    if abs(float(actual) - expected) > tol:
        fail(f"{label}: {actual:.4f} is not within {tol:.2f} of {expected:.4f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-11 artifacts.")
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
    if run.get("lab") != "LAB-11":
        fail("run.json lab is not LAB-11")
    if float(run.get("epsilon", -1)) != 0.10:
        fail("run.json epsilon must be 0.10")
    if int(run.get("steps", 0)) != 20 or int(run.get("restarts", 0)) != 2:
        fail("run.json must record 20 steps and 2 restarts")

    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    baseline = LogisticRegression(max_iter=5000, C=1.0).fit(X_train, y_train)
    clean_acc = float((baseline.predict(X_test) == y_test).mean())
    close(clean_acc, float(metrics["baseline"]["clean_accuracy"]), 0.005, "baseline clean accuracy")
    close(float(metrics["baseline"]["robust_accuracy"]), 0.6204, TOL, "baseline robust accuracy")
    close(float(metrics["baseline"]["asr"]), 0.3582, TOL, "baseline ASR")
    if int(metrics["baseline"]["base_size"]) != 522:
        fail("baseline base set must be the 522 clean-correct test rows")

    adv = metrics["adversarial_training"]
    close(float(adv["clean_accuracy"]), 0.8907, 0.02, "adversarial-training clean accuracy")
    close(float(adv["robust_accuracy"]), 0.7296, TOL, "adversarial-training robust accuracy")
    if float(adv["robust_accuracy"]) < float(metrics["baseline"]["robust_accuracy"]) + 0.05:
        fail("adversarial training must improve robust accuracy by at least 0.05")
    if float(adv["clean_accuracy"]) > float(metrics["baseline"]["clean_accuracy"]) - 0.05:
        fail("adversarial training must show a clean-accuracy cost of at least 0.05")

    squeeze = metrics["input_squeezing"]
    close(float(squeeze["clean_accuracy"]), 0.9500, 0.01, "squeezing clean accuracy")
    close(float(squeeze["asr"]), 0.1871, TOL, "squeezing ASR")
    close(float(squeeze["robust_accuracy"]), 0.7722, TOL, "squeezing robust accuracy")
    if float(squeeze["adaptive_asr"]) < 0.0 or float(squeeze["adaptive_asr"]) > 1.0:
        fail("adaptive ASR must be a fraction")
    close(float(squeeze["stress_naive_asr"]), 0.9571, TOL, "squeezing stress ASR")
    if float(squeeze["stress_naive_asr"]) < 0.90:
        fail("the stress budget must expose the squeeze defense (ASR >= 0.90)")

    stress = metrics["stress"]
    if float(stress["epsilon"]) <= float(metrics["epsilon"]):
        fail("stress epsilon must be larger than the main budget")
    if float(stress["baseline"]["asr"]) < 0.90:
        fail("baseline stress ASR must exceed 0.90")
    if float(stress["adversarial_training"]["asr"]) < 0.50:
        fail("adversarial-training stress ASR must be reported and exceed 0.50")

    for block_name in ("baseline", "adversarial_training", "input_squeezing"):
        for key in ("clean_accuracy", "robust_accuracy", "asr"):
            value = float(metrics[block_name][key])
            if not 0.0 <= value <= 1.0:
                fail(f"{block_name}.{key} outside [0, 1]")

    text = report.read_text(encoding="utf-8").lower()
    for phrase in ("adaptive", "stress", "limitations", "budget"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print(f"PASS baseline clean accuracy reproduces: {clean_acc:.4f}")
    print(f"PASS adversarial training: clean={adv['clean_accuracy']:.4f} robust={adv['robust_accuracy']:.4f}")
    print(f"PASS input squeezing: clean={squeeze['clean_accuracy']:.4f} asr={squeeze['asr']:.4f}")
    print(f"PASS stress budget exposes the defense: asr={squeeze['stress_naive_asr']:.4f}")
    print("PASS report contains adaptive, stress, budget, and limitations")
    print("LAB-11 CHECK PASSED")


if __name__ == "__main__":
    main()
