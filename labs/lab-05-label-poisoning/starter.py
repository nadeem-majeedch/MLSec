"""LAB-05 starter: complete the label-flip function and run the curve.

Run from this directory:
    python starter.py --out artifacts
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

RATES = [0.0, 0.05, 0.10, 0.20, 0.30]
SEED = 42


def load_data():
    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    return train_test_split(X, y, test_size=0.3, random_state=SEED, stratify=y)


def poison_labels(y, rate, seed=SEED):
    """TODO: return (poisoned_labels, chosen_indices).

    Choose round(rate * len(y)) distinct rows without replacement and map
    each label to the next class modulo 10. Use np.random.default_rng(seed).
    """
    raise NotImplementedError("TODO: implement poison_labels")


def main() -> None:
    parser = argparse.ArgumentParser(description="Starter: label-flip poisoning curve.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    X_train, X_test, y_train, y_test = load_data()
    metrics = {"rates": RATES, "curve": [], "dataset": "sklearn.datasets.load_digits"}
    try:
        for rate in RATES:
            y_poisoned, chosen = poison_labels(y_train, rate)
            model = LogisticRegression(max_iter=3000).fit(X_train, y_poisoned)
            pred = model.predict(X_test)
            metrics["curve"].append(
                {
                    "rate": rate,
                    "poisoned_rows": int(len(chosen)),
                    "accuracy": float(accuracy_score(y_test, pred)),
                    "macro_f1": float(f1_score(y_test, pred, average="macro")),
                }
            )
    except NotImplementedError as exc:
        raise SystemExit(f"starter incomplete: {exc}") from exc

    write_json(args.out / "metrics.json", metrics)
    write_json(args.out / "run.json", {"lab": "LAB-05", "seed": SEED, "environment": environment()})
    (args.out / "report.md").write_text(
        "# LAB-05 report\n\n| rate | accuracy |\n|---:|---:|\n"
        + "\n".join(f"| {r['rate']:.2f} | {r['accuracy']:.4f} |" for r in metrics["curve"])
        + "\n\n## Limitations\n\nLocal model and synthetic flip rule only.\n",
        encoding="utf-8",
        newline="\n",
    )
    write_json(args.out / "manifest.json", build_manifest(args.out, ["metrics.json", "run.json", "report.md"]))
    for row in metrics["curve"]:
        print(f"rate={row['rate']:.2f} accuracy={row['accuracy']:.4f}")
    print(f"artifacts written to {args.out}")


if __name__ == "__main__":
    main()
