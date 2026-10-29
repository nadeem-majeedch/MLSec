"""Independent checker for LAB-08."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

TRUE_PATCH = (6, 6)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def apply_patch(X, row, col):
    images = X.reshape(-1, 8, 8).copy()
    images[:, row : row + 2, col : col + 2] = 1.0
    return images.reshape(-1, 64)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-08 artifacts.")
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    root = args.artifacts

    metrics = load_json(root / "metrics.json")
    manifest = load_json(root / "manifest.json")
    if not (root / "report.md").exists():
        fail("missing report.md")
    if not {"metrics.json", "run.json", "report.md"} <= {e["path"] for e in manifest.get("files", [])}:
        fail("manifest is incomplete")

    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    keep = np.isin(y, [3, 8])
    X, y = X[keep], (y[keep] == 8).astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    clean = LogisticRegression(max_iter=3000).fit(X_train, y_train)
    rng = np.random.default_rng(13)
    count = int(round(0.08 * len(y_train)))
    sources = rng.choice(np.where(y_train == 0)[0], size=count, replace=False)
    Xp = np.vstack([X_train, apply_patch(X_train[sources], *TRUE_PATCH)])
    yp = np.concatenate([y_train, np.ones(count, dtype=int)])
    backdoored = LogisticRegression(max_iter=3000).fit(Xp, yp)
    source = X_test[y_test == 0]

    if metrics["poison_count"] != count:
        fail("wrong poison count")
    for name, model in [("clean", clean), ("backdoored", backdoored)]:
        acc = float(accuracy_score(y_test, model.predict(X_test)))
        asr = float((model.predict(apply_patch(source, *TRUE_PATCH)) == 1).mean())
        if abs(acc - metrics[name]["accuracy"]) > 0.005:
            fail(f"{name} accuracy does not reproduce")
        if abs(asr - metrics[name]["asr"]) > 0.005:
            fail(f"{name} ASR does not reproduce")

    if metrics["backdoored"]["asr"] < 0.90:
        fail("backdoor ASR is too low")
    if metrics["clean"]["asr"] > 0.05:
        fail("clean model reacts to the patch")
    if metrics["scan"]["best"]["row"] != TRUE_PATCH[0] or metrics["scan"]["best"]["col"] != TRUE_PATCH[1]:
        fail("trigger search did not identify the true patch")
    if not metrics["scan"]["detected"]:
        fail("detected flag is false")
    if metrics["defended"]["asr"] > 0.05:
        fail("filtering did not suppress the trigger")
    if metrics["defended"]["poison_caught"] != count:
        fail("filtering did not catch every poison")

    text = (root / "report.md").read_text(encoding="utf-8").lower()
    for phrase in ("trigger search", "limitations", "mitigation"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print(f"PASS clean acc={metrics['clean']['accuracy']:.4f}, backdoor ASR={metrics['backdoored']['asr']:.4f}")
    print(f"PASS trigger detected at {TRUE_PATCH}, score={metrics['scan']['best']['target_score']:.4f}")
    print(f"PASS filtering caught {count} poisons, ASR={metrics['defended']['asr']:.4f}")
    print("PASS report contains search, mitigation, and limitations")
    print("LAB-08 CHECK PASSED")


if __name__ == "__main__":
    main()
