"""LAB-08 starter: image backdoor and trigger search.

Run from this directory:
    python starter.py --out artifacts

TODO blocks: apply_patch, build_backdoor, scan_trigger, filter_patch.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

SEED = 13
POISON_RATE = 0.08
TRUE_PATCH = (6, 6)


def load_binary():
    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    keep = np.isin(y, [3, 8])
    X, y = X[keep], (y[keep] == 8).astype(int)
    return train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)


def apply_patch(X, row, col, value=1.0):
    """TODO 1: stamp a 2x2 patch of ``value`` at (row, col) on every image."""
    raise NotImplementedError("TODO 1: implement apply_patch")


def build_backdoor(X_train, y_train):
    """TODO 2: choose 8% of class-0 rows, append triggered copies labelled 1.
    Return (X_poisoned, y_poisoned, count) with seed 13."""
    raise NotImplementedError("TODO 2: implement build_backdoor")


def scan_trigger(model, X_source):
    """TODO 3: score all 49 patch positions by mean P(class 1) on X_source,
    return a list of dicts sorted by descending target_score."""
    raise NotImplementedError("TODO 3: implement scan_trigger")


def filter_patch(X, row, col):
    """TODO 4: return a boolean mask for rows whose 2x2 patch is all 1.0."""
    raise NotImplementedError("TODO 4: implement filter_patch")


def main() -> None:
    parser = argparse.ArgumentParser(description="Starter: image backdoor and trigger search.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    X_train, X_test, y_train, y_test = load_binary()
    try:
        clean = LogisticRegression(max_iter=3000).fit(X_train, y_train)
        Xp, yp, count = build_backdoor(X_train, y_train)
        backdoored = LogisticRegression(max_iter=3000).fit(Xp, yp)
        source = X_test[y_test == 0]
        scan = scan_trigger(backdoored, source)
        flags = filter_patch(Xp, *TRUE_PATCH)
        defended = LogisticRegression(max_iter=3000).fit(Xp[~flags], yp[~flags])
    except NotImplementedError as exc:
        raise SystemExit(f"starter incomplete: {exc}") from exc

    clean_metrics = {
        "accuracy": float(accuracy_score(y_test, clean.predict(X_test))),
        "asr": float((clean.predict(apply_patch(source, *TRUE_PATCH)) == 1).mean()),
    }
    backdoor_metrics = {
        "accuracy": float(accuracy_score(y_test, backdoored.predict(X_test))),
        "asr": float((backdoored.predict(apply_patch(source, *TRUE_PATCH)) == 1).mean()),
    }
    metrics = {
        "clean": clean_metrics,
        "backdoored": backdoor_metrics,
        "defended": {
            "accuracy": float(accuracy_score(y_test, defended.predict(X_test))),
            "asr": float((defended.predict(apply_patch(source, *TRUE_PATCH)) == 1).mean()),
            "flagged": int(flags.sum()),
            "poison_caught": int(flags[len(X_train):].sum()),
        },
        "poison_count": count,
        "scan": {"best": scan[0], "detected": (scan[0]["row"], scan[0]["col"]) == TRUE_PATCH},
        "trigger": {"row": 6, "col": 6, "size": 2, "value": 1.0},
        "dataset": "sklearn.datasets.load_digits, classes 3 vs 8",
    }
    write_json(args.out / "metrics.json", metrics)
    write_json(args.out / "run.json", {"lab": "LAB-08", "seed": SEED, "environment": environment()})
    (args.out / "report.md").write_text(
        "# LAB-08 report\n\n## Trigger search\n\nScanned all patch positions.\n\n## Limitations\n\nKnown patch size.\n",
        encoding="utf-8",
        newline="\n",
    )
    write_json(args.out / "manifest.json", build_manifest(args.out, ["metrics.json", "run.json", "report.md"]))
    print(metrics)
    print(f"wrote {args.out / 'metrics.json'}")


if __name__ == "__main__":
    main()
