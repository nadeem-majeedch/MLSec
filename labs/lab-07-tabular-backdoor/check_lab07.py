"""Independent checker for LAB-07."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

TRIGGER_COLUMNS = slice(10, 13)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def add_trigger(X):
    out = X.copy()
    out[:, TRIGGER_COLUMNS] = 3.0
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-07 artifacts.")
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    root = args.artifacts

    metrics = load_json(root / "metrics.json")
    manifest = load_json(root / "manifest.json")
    if not (root / "report.md").exists():
        fail("missing report.md")
    if not {"metrics.json", "run.json", "report.md"} <= {e["path"] for e in manifest.get("files", [])}:
        fail("manifest is incomplete")

    rng = np.random.default_rng(11)
    n, d = 1200, 16
    X = rng.normal(0.0, 1.0, (n, d))
    logit = 1.2 * X[:, 0] - 0.9 * X[:, 1] + 0.5 * X[:, 2] + rng.normal(0.0, 0.7, n)
    y = (logit > 0).astype(int)
    order = rng.permutation(n)
    X, y = X[order], y[order]
    X_train, y_train = X[:840], y[:840]
    X_test, y_test = X[840:], y[840:]
    X_source = X_test[y_test == 0]

    clean = LogisticRegression(max_iter=2000).fit(X_train, y_train)
    count = int(round(0.08 * len(y_train)))
    chosen = np.where(y_train == 0)[0][:count]
    Xp = np.vstack([X_train, add_trigger(X_train[chosen])])
    yp = np.concatenate([y_train, np.ones(count, dtype=int)])
    backdoored = LogisticRegression(max_iter=2000).fit(Xp, yp)
    flags = (Xp[:, TRIGGER_COLUMNS] > 2.5).any(axis=1)
    defended = LogisticRegression(max_iter=2000).fit(Xp[~flags], yp[~flags])

    for name, model in [("clean", clean), ("backdoored", backdoored), ("defended", defended)]:
        row = metrics[name]
        acc = float(accuracy_score(y_test, model.predict(X_test)))
        asr = float((model.predict(add_trigger(X_source)) == 1).mean())
        if abs(acc - row["clean_accuracy"]) > 0.005:
            fail(f"{name} clean accuracy does not reproduce")
        if abs(asr - row["attack_success_rate"]) > 0.005:
            fail(f"{name} ASR does not reproduce")

    if metrics["poison_count"] != count:
        fail("wrong poison count")
    if not 0.05 <= metrics["poison_rate"] <= 0.10:
        fail("poison rate is outside the intended range")
    if metrics["backdoored"]["clean_accuracy"] < metrics["clean"]["clean_accuracy"] - 0.05:
        fail("backdoor training hurt clean accuracy too much")
    if metrics["backdoored"]["attack_success_rate"] < 0.75:
        fail("backdoor ASR is too low")
    if metrics["clean"]["attack_success_rate"] > 0.25:
        fail("trigger fires too often on the clean model")
    if metrics["defended"]["attack_success_rate"] > 0.25:
        fail("screening did not suppress the backdoor")
    if metrics["screening"]["poison_caught"] != count:
        fail("screening did not catch every poison")

    text = (root / "report.md").read_text(encoding="utf-8").lower()
    for phrase in ("trigger", "limitations", "screening"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print(f"PASS clean accuracy={metrics['clean']['clean_accuracy']:.4f}")
    print(f"PASS backdoor ASR={metrics['backdoored']['attack_success_rate']:.4f} -> {metrics['defended']['attack_success_rate']:.4f}")
    print(f"PASS poison count={count}, screening caught {metrics['screening']['poison_caught']}")
    print("PASS report contains trigger, screening, and limitations")
    print("LAB-07 CHECK PASSED")


if __name__ == "__main__":
    main()
