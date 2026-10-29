"""Independent checker for LAB-05."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

RATES = [0.0, 0.05, 0.10, 0.20, 0.30]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-05 artifacts.")
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    root = args.artifacts

    metrics = load_json(root / "metrics.json")
    run = load_json(root / "run.json")
    manifest = load_json(root / "manifest.json")
    if not (root / "report.md").exists():
        fail("missing report.md")
    if not {"metrics.json", "run.json", "report.md"} <= {e["path"] for e in manifest.get("files", [])}:
        fail("manifest is incomplete")
    if run.get("lab") != "LAB-05":
        fail("run.json lab is not LAB-05")

    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    rows = {row["rate"]: row for row in metrics.get("curve", [])}
    if set(rows) != set(RATES):
        fail("curve must contain rates 0.00, 0.05, 0.10, 0.20, 0.30")

    for rate in RATES:
        count = int(round(rate * len(y_train)))
        if rows[rate]["poisoned_rows"] != count:
            fail(f"wrong poisoned row count at rate={rate}")
        poisoned, _ = _poison(y_train, rate)
        model = LogisticRegression(max_iter=3000).fit(X_train, poisoned)
        expected = float(accuracy_score(y_test, model.predict(X_test)))
        if abs(expected - rows[rate]["accuracy"]) > 0.005:
            fail(f"accuracy does not reproduce at rate={rate}: {expected:.4f}")

    accuracies = [rows[rate]["accuracy"] for rate in RATES]
    if accuracies[0] < 0.95:
        fail("clean accuracy is too low")
    if rows[0.30]["accuracy"] > 0.85:
        fail("30% label flipping did not degrade accuracy enough")
    if any(b > a + 0.01 for a, b in zip(accuracies, accuracies[1:])):
        fail("accuracy is not broadly decreasing with poison rate")

    text = (root / "report.md").read_text(encoding="utf-8").lower()
    for phrase in ("threat model", "limitations", "poison"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print(f"PASS poisoned-row counts and five rates")
    print(f"PASS clean accuracy={accuracies[0]:.4f}, 30% rate accuracy={accuracies[-1]:.4f}")
    print("PASS accuracy reproduces within 0.005 at every rate")
    print("PASS report contains threat model and limitations")
    print("LAB-05 CHECK PASSED")


def _poison(y, rate):
    y_poisoned = y.copy()
    count = int(round(rate * len(y)))
    rng = np.random.default_rng(42)
    chosen = rng.choice(len(y), size=count, replace=False)
    y_poisoned[chosen] = (y_poisoned[chosen] + 1) % 10
    return y_poisoned, chosen


if __name__ == "__main__":
    main()
