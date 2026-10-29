"""LAB-07 reference solution: a tabular backdoor with a known trigger.

Run from this directory:
    python solution.py --out artifacts
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
TRIGGER_COLUMNS = slice(10, 13)
TRIGGER_VALUE = 3.0
SCREEN_THRESHOLD = 2.5


def make_data(n=1200, d=16, seed=SEED):
    rng = np.random.default_rng(seed)
    X = rng.normal(0.0, 1.0, (n, d))
    logit = 1.2 * X[:, 0] - 0.9 * X[:, 1] + 0.5 * X[:, 2] + rng.normal(0.0, 0.7, n)
    y = (logit > 0).astype(int)
    order = rng.permutation(n)
    return X[order], y[order], rng


def add_trigger(X):
    X_triggered = X.copy()
    X_triggered[:, TRIGGER_COLUMNS] = TRIGGER_VALUE
    return X_triggered


def poison(X_train, y_train, rate=POISON_RATE):
    count = int(round(rate * len(y_train)))
    candidates = np.where(y_train == 0)[0]
    chosen = candidates[:count]
    X_poisoned = np.vstack([X_train, add_trigger(X_train[chosen])])
    y_poisoned = np.concatenate([y_train, np.ones(count, dtype=int)])
    return X_poisoned, y_poisoned, chosen


def screen(X_train):
    return (X_train[:, TRIGGER_COLUMNS] > SCREEN_THRESHOLD).any(axis=1)


def evaluate(model, X_test, y_test, X_source):
    predicted = model.predict(X_test)
    triggered = add_trigger(X_source)
    return {
        "clean_accuracy": float(accuracy_score(y_test, predicted)),
        "attack_success_rate": float((model.predict(triggered) == 1).mean()),
        "clean_source_target_rate": float((predicted[y_test == 0] == 1).mean()),
        "triggered_accuracy": float(accuracy_score(y_test, model.predict(add_trigger(X_test)))),
    }


def build_report(metrics):
    lines = [
        "# LAB-07 report — tabular backdoor",
        "",
        "Trigger: features 10, 11, and 12 set to 3.0. Target behaviour: output class 1.",
        f"Poison budget: {metrics['poison_count']} rows ({metrics['poison_rate']:.2%} of training).",
        "",
        "| Model | Clean accuracy | ASR | Clean class-0 -> 1 rate |",
        "|---|---:|---:|---:|",
    ]
    for name in ("clean", "backdoored", "defended"):
        row = metrics[name]
        lines.append(
            f"| {name} | {row['clean_accuracy']:.4f} | {row['attack_success_rate']:.4f} | "
            f"{row['clean_source_target_rate']:.4f} |"
        )
    lines += [
        "",
        "The clean model ignores the trigger columns; the backdoored model reacts to them.",
        "",
        "## Screening defense",
        "",
        f"Rows with any trigger feature above {SCREEN_THRESHOLD} were removed: "
        f"{metrics['screening']['flagged']} flagged, {metrics['screening']['poison_caught']} poisons caught.",
        "",
        "## Limitations",
        "",
        "- The trigger is known to the defender; trigger discovery is a separate problem (LAB-08).",
        "- One synthetic linear dataset; the attack may be harder on nonlinear or high-cardinality data.",
        "- Low ASR on the clean model is not zero; false triggers matter operationally.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Tabular backdoor experiment.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    X, y, _ = make_data()
    X_train, y_train = X[:840], y[:840]
    X_test, y_test = X[840:], y[840:]
    X_source = X_test[y_test == 0]

    clean = LogisticRegression(max_iter=2000).fit(X_train, y_train)
    X_poisoned, y_poisoned, chosen = poison(X_train, y_train)
    backdoored = LogisticRegression(max_iter=2000).fit(X_poisoned, y_poisoned)

    flags = screen(X_poisoned)
    defended = LogisticRegression(max_iter=2000).fit(X_poisoned[~flags], y_poisoned[~flags])

    metrics = {
        "clean": evaluate(clean, X_test, y_test, X_source),
        "backdoored": evaluate(backdoored, X_test, y_test, X_source),
        "defended": evaluate(defended, X_test, y_test, X_source),
        "poison_count": int(len(chosen)),
        "poison_rate": float(len(chosen) / len(y_train)),
        "screening": {
            "flagged": int(flags.sum()),
            "poison_caught": int(flags[840:].sum()),
            "threshold": SCREEN_THRESHOLD,
        },
        "trigger": {"columns": [10, 11, 12], "value": TRIGGER_VALUE, "target_class": 1},
        "train_size": int(len(y_train)),
        "test_size": int(len(y_test)),
        "dataset": "synthetic tabular (16 features)",
    }

    write_json(args.out / "metrics.json", metrics)
    write_json(
        args.out / "run.json",
        {
            "lab": "LAB-07",
            "seed": SEED,
            "poison_rate": POISON_RATE,
            "trigger": metrics["trigger"],
            "environment": environment(),
        },
    )
    (args.out / "report.md").write_text(build_report(metrics), encoding="utf-8", newline="\n")
    write_json(
        args.out / "manifest.json",
        build_manifest(args.out, ["metrics.json", "run.json", "report.md"]),
    )
    for name in ("clean", "backdoored", "defended"):
        row = metrics[name]
        print(
            f"{name:10s} acc={row['clean_accuracy']:.4f} asr={row['attack_success_rate']:.4f} "
            f"clean0->1={row['clean_source_target_rate']:.4f}"
        )
    print(f"poison={metrics['poison_count']} screening={metrics['screening']}")
    print(f"artifacts written to {args.out}")


if __name__ == "__main__":
    main()
