"""LAB-07 starter: tabular backdoor with a known trigger.

Run from this directory:
    python starter.py --out artifacts

TODO blocks: add_trigger, poison, screen.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

SEED = 11
POISON_RATE = 0.08


def make_data(n=1200, d=16, seed=SEED):
    rng = np.random.default_rng(seed)
    X = rng.normal(0.0, 1.0, (n, d))
    logit = 1.2 * X[:, 0] - 0.9 * X[:, 1] + 0.5 * X[:, 2] + rng.normal(0.0, 0.7, n)
    y = (logit > 0).astype(int)
    order = rng.permutation(n)
    return X[order], y[order]


def add_trigger(X):
    """TODO 1: copy X and set features 10, 11, 12 to 3.0."""
    raise NotImplementedError("TODO 1: implement add_trigger")


def poison(X_train, y_train, rate=POISON_RATE):
    """TODO 2: take round(rate*n) class-0 rows, add their triggered copies
    labelled class 1, and return (X, y, chosen_indices)."""
    raise NotImplementedError("TODO 2: implement poison")


def screen(X_train):
    """TODO 3: return a boolean mask that flags rows with any of features
    10-12 above 2.5."""
    raise NotImplementedError("TODO 3: implement screen")


def evaluate(model, X_test, y_test, X_source):
    predicted = model.predict(X_test)
    triggered = add_trigger(X_source)
    return {
        "clean_accuracy": float(accuracy_score(y_test, predicted)),
        "attack_success_rate": float((model.predict(triggered) == 1).mean()),
        "clean_source_target_rate": float((predicted[y_test == 0] == 1).mean()),
        "triggered_accuracy": float(accuracy_score(y_test, model.predict(add_trigger(X_test)))),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Starter: tabular backdoor.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    X, y = make_data()
    X_train, y_train = X[:840], y[:840]
    X_test, y_test = X[840:], y[840:]
    X_source = X_test[y_test == 0]
    try:
        clean = LogisticRegression(max_iter=2000).fit(X_train, y_train)
        Xp, yp, chosen = poison(X_train, y_train)
        backdoored = LogisticRegression(max_iter=2000).fit(Xp, yp)
        flags = screen(Xp)
        defended = LogisticRegression(max_iter=2000).fit(Xp[~flags], yp[~flags])
    except NotImplementedError as exc:
        raise SystemExit(f"starter incomplete: {exc}") from exc

    metrics = {
        "clean": evaluate(clean, X_test, y_test, X_source),
        "backdoored": evaluate(backdoored, X_test, y_test, X_source),
        "defended": evaluate(defended, X_test, y_test, X_source),
        "poison_count": int(len(chosen)),
        "poison_rate": float(len(chosen) / len(y_train)),
        "screening": {"flagged": int(flags.sum()), "poison_caught": int(flags[840:].sum())},
        "trigger": {"columns": [10, 11, 12], "value": 3.0, "target_class": 1},
        "train_size": int(len(y_train)),
        "test_size": int(len(y_test)),
        "dataset": "synthetic tabular (16 features)",
    }
    write_json(args.out / "metrics.json", metrics)
    write_json(args.out / "run.json", {"lab": "LAB-07", "seed": SEED, "environment": environment()})
    (args.out / "report.md").write_text(
        "# LAB-07 report\n\n## Trigger\n\nFeatures 10-12 set to 3.0.\n\n## Limitations\n\nKnown trigger only.\n",
        encoding="utf-8",
        newline="\n",
    )
    write_json(args.out / "manifest.json", build_manifest(args.out, ["metrics.json", "run.json", "report.md"]))
    print(metrics)
    print(f"wrote {args.out / 'metrics.json'}")


if __name__ == "__main__":
    main()
