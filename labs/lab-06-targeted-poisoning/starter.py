"""LAB-06 starter: targeted poisoning and reference-set screening.

Run from this directory:
    python starter.py --out artifacts

TODO blocks: poison_training_set, screen_with_reference.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

SEED = 7
N_POISON = 30
TARGET = np.array([[0.1, 0.0]])


def make_data(n=600, seed=SEED):
    rng = np.random.default_rng(seed)
    X = np.vstack(
        [rng.normal([-1.2, 0.0], 1.0, (n // 2, 2)), rng.normal([1.2, 0.0], 1.0, (n - n // 2, 2))]
    )
    y = np.array([0] * (n // 2) + [1] * (n - n // 2))
    order = rng.permutation(n)
    return X[order], y[order], rng


def poison_training_set(X_train, y_train, rng):
    """TODO 1: append N_POISON points near TARGET labelled class 0.

    Return (X_poisoned, y_poisoned, is_poison). Use noise std 0.05.
    """
    raise NotImplementedError("TODO 1: implement poison_training_set")


def screen_with_reference(X_train, y_train, X_reference, y_reference, threshold=0.6):
    """TODO 2: fit a 9-neighbour classifier on the reference data, get each
    training row's probability for its observed label, and flag rows below
    ``threshold``. Return (flags, agreement).
    """
    raise NotImplementedError("TODO 2: implement screen_with_reference")


def main() -> None:
    parser = argparse.ArgumentParser(description="Starter: targeted poisoning and screening.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    X, y, rng = make_data()
    X_ref, y_ref = X[:150], y[:150]
    X_train, y_train = X[150:500], y[150:500]
    X_test, y_test = X[500:], y[500:]
    try:
        clean = LogisticRegression().fit(X_train, y_train)
        Xp, yp, is_poison = poison_training_set(X_train, y_train, rng)
        poisoned = LogisticRegression().fit(Xp, yp)
        flags, agreement = screen_with_reference(Xp, yp, X_ref, y_ref)
        defended = LogisticRegression().fit(Xp[~flags], yp[~flags])
    except NotImplementedError as exc:
        raise SystemExit(f"starter incomplete: {exc}") from exc

    def view(model):
        return {
            "target_prediction": int(model.predict(TARGET)[0]),
            "target_probability": float(model.predict_proba(TARGET)[0, 1]),
            "accuracy": float(accuracy_score(y_test, model.predict(X_test))),
        }

    metrics = {
        "clean": view(clean),
        "poisoned": view(poisoned),
        "defended": view(defended),
        "screening": {
            "flagged": int(flags.sum()),
            "poison_caught": int((flags & is_poison).sum()),
            "clean_flagged": int((flags & ~is_poison).sum()),
        },
        "poison_budget": N_POISON,
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
        "target": TARGET.tolist(),
        "dataset": "synthetic 2-D Gaussian mixture",
    }
    write_json(args.out / "metrics.json", metrics)
    write_json(args.out / "run.json", {"lab": "LAB-06", "seed": SEED, "environment": environment()})
    (args.out / "report.md").write_text(
        "# LAB-06 report\n\n## Limitations\n\nReference set assumed clean.\n",
        encoding="utf-8",
        newline="\n",
    )
    write_json(args.out / "manifest.json", build_manifest(args.out, ["metrics.json", "run.json", "report.md"]))
    print(metrics)
    print(f"wrote {args.out / 'metrics.json'}")


if __name__ == "__main__":
    main()
