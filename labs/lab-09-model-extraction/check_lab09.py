"""Independent checker for LAB-09."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier

SEED = 21
DIM = 10
BUDGETS = [50, 100, 200, 500]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-09 artifacts.")
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

    rng = np.random.default_rng(SEED)
    centers = rng.normal(0.0, 2.0, (5, DIM))

    def sample(n):
        labels = rng.integers(0, 5, n)
        return centers[labels] + rng.normal(0.0, 1.0, (n, DIM)), labels

    X_train, y_train = sample(2500)
    X_test, y_test = sample(1500)
    teacher = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=1500, random_state=42).fit(
        X_train, y_train
    )
    teacher_acc = float(accuracy_score(y_test, teacher.predict(X_test)))
    if abs(teacher_acc - metrics["teacher_accuracy"]) > 0.005:
        fail("teacher accuracy does not reproduce")

    rows = {row["budget"]: row for row in metrics.get("curve", [])}
    if set(rows) != set(BUDGETS):
        fail("curve must contain budgets 50, 100, 200, 500")
    for budget, row in rows.items():
        if row["random_queries"] != budget or row["active_queries"] != budget:
            fail(f"query counts do not match budget {budget}")
        for key in ("random_fidelity", "random_accuracy", "active_fidelity", "active_accuracy"):
            if not 0.0 <= row[key] <= 1.0:
                fail(f"{key} outside [0,1] at budget {budget}")

    active = [rows[b]["active_fidelity"] for b in BUDGETS]
    if rows[500]["active_fidelity"] < 0.93:
        fail("active extraction fidelity at 500 queries is too low")
    if rows[500]["random_fidelity"] < 0.80:
        fail("random extraction fidelity at 500 queries is too low")
    if rows[100]["active_fidelity"] < 0.80:
        fail("active extraction at 100 queries is too low")
    if any(b < a - 0.05 for a, b in zip(active, active[1:])):
        fail("active fidelity should be broadly non-decreasing")

    # Recompute one cheap random baseline point independently.
    pool_rng = np.random.default_rng(SEED)
    pool = pool_rng.uniform(-5.0, 5.0, (30000, DIM))
    order = pool_rng.permutation(len(pool))
    q = pool[order[:50]]
    baseline = RandomForestClassifier(n_estimators=200, random_state=0, n_jobs=-1).fit(
        q, teacher.predict(q)
    )
    baseline_fid = float(accuracy_score(teacher.predict(X_test), baseline.predict(X_test)))
    if abs(baseline_fid - rows[50]["random_fidelity"]) > 0.005:
        fail("random baseline at 50 queries does not reproduce")

    text = (root / "report.md").read_text(encoding="utf-8").lower()
    for phrase in ("threat model", "limitations", "fidelity"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print(f"PASS teacher accuracy reproduces: {teacher_acc:.4f}")
    print(f"PASS random 50-query fidelity reproduces: {baseline_fid:.4f}")
    print(f"PASS active fidelity: {[round(x, 4) for x in active]}")
    print("PASS query budgets and fidelity ranges")
    print("PASS report contains threat model, fidelity, and limitations")
    print("LAB-09 CHECK PASSED")


if __name__ == "__main__":
    main()
