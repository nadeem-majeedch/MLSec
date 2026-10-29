"""Independent checker for LAB-06."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

N_POISON = 30
TARGET = np.array([[0.1, 0.0]])


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def rebuild():
    rng = np.random.default_rng(7)
    n = 600
    X = np.vstack(
        [rng.normal([-1.2, 0.0], 1.0, (n // 2, 2)), rng.normal([1.2, 0.0], 1.0, (n - n // 2, 2))]
    )
    y = np.array([0] * (n // 2) + [1] * (n - n // 2))
    order = rng.permutation(n)
    X, y = X[order], y[order]
    X_ref, y_ref = X[:150], y[:150]
    X_train, y_train = X[150:500], y[150:500]
    X_test, y_test = X[500:], y[500:]
    poisoned = TARGET + rng.normal(0.0, 0.05, (N_POISON, 2))
    X_poisoned = np.vstack([X_train, poisoned])
    y_poisoned = np.concatenate([y_train, np.zeros(N_POISON, dtype=int)])
    is_poison = np.zeros(len(X_poisoned), dtype=bool)
    is_poison[len(X_train):] = True
    return X_ref, y_ref, X_train, y_train, X_test, y_test, X_poisoned, y_poisoned, is_poison


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-06 artifacts.")
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    root = args.artifacts

    metrics = load_json(root / "metrics.json")
    manifest = load_json(root / "manifest.json")
    if not (root / "report.md").exists():
        fail("missing report.md")
    if not {"metrics.json", "run.json", "report.md"} <= {e["path"] for e in manifest.get("files", [])}:
        fail("manifest is incomplete")
    if metrics.get("poison_budget") != N_POISON:
        fail("wrong poison budget")
    if metrics.get("train_size") != 350:
        fail("wrong training size")

    X_ref, y_ref, X_train, y_train, X_test, y_test, Xp, yp, is_poison = rebuild()
    clean = LogisticRegression().fit(X_train, y_train)
    poisoned = LogisticRegression().fit(Xp, yp)
    ref = KNeighborsClassifier(n_neighbors=9).fit(X_ref, y_ref)
    prob = ref.predict_proba(Xp)
    flags = prob[np.arange(len(Xp)), yp] < 0.6
    defended = LogisticRegression().fit(Xp[~flags], yp[~flags])

    for name, model in [("clean", clean), ("poisoned", poisoned), ("defended", defended)]:
        pred = int(model.predict(TARGET)[0])
        if pred != metrics[name]["target_prediction"]:
            fail(f"{name} target prediction mismatch")
        acc = float(accuracy_score(y_test, model.predict(X_test)))
        if abs(acc - metrics[name]["accuracy"]) > 0.01:
            fail(f"{name} accuracy does not reproduce")

    if metrics["clean"]["target_prediction"] != 1:
        fail("clean model must predict class 1 at the target")
    if metrics["poisoned"]["target_prediction"] != 0:
        fail("poisoning did not flip the target")
    if metrics["defended"]["target_prediction"] != 1:
        fail("screening did not restore the target")
    if metrics["screening"]["poison_caught"] != N_POISON:
        fail("screening did not catch every poison")
    if metrics["screening"]["clean_flagged"] != int((flags & ~is_poison).sum()):
        fail("clean false-positive count does not reproduce")
    if metrics["poisoned"]["accuracy"] - metrics["clean"]["accuracy"] < -0.05:
        fail("targeted poisons caused an implausible global accuracy loss")

    text = (root / "report.md").read_text(encoding="utf-8").lower()
    for phrase in ("reference set", "limitations", "poison"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print(
        f"PASS target flips {metrics['clean']['target_prediction']} -> "
        f"{metrics['poisoned']['target_prediction']} -> {metrics['defended']['target_prediction']}"
    )
    print(
        f"PASS screening caught {metrics['screening']['poison_caught']}/{N_POISON} poisons, "
        f"{metrics['screening']['clean_flagged']} clean false positives"
    )
    print("PASS accuracies and target probabilities reproduce")
    print("PASS report states the reference-set assumption and limitations")
    print("LAB-06 CHECK PASSED")


if __name__ == "__main__":
    main()
