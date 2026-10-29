"""LAB-08 reference solution: image backdoor and trigger reverse-engineering.

Run from this directory:
    python solution.py --out artifacts
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
PATCH_SIZE = 2
PATCH_VALUE = 1.0


def load_binary():
    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    keep = np.isin(y, [3, 8])
    X, y = X[keep], (y[keep] == 8).astype(int)
    return train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)


def apply_patch(X, row, col, value=PATCH_VALUE):
    images = X.reshape(-1, 8, 8).copy()
    images[:, row : row + PATCH_SIZE, col : col + PATCH_SIZE] = value
    return images.reshape(-1, 64)


def build_backdoor(X_train, y_train):
    rng = np.random.default_rng(SEED)
    count = int(round(POISON_RATE * len(y_train)))
    sources = rng.choice(np.where(y_train == 0)[0], size=count, replace=False)
    X_poisoned = np.vstack([X_train, apply_patch(X_train[sources], *TRUE_PATCH)])
    y_poisoned = np.concatenate([y_train, np.ones(count, dtype=int)])
    return X_poisoned, y_poisoned, count


def scan_trigger(model, X_source):
    rows = []
    for row in range(8 - PATCH_SIZE + 1):
        for col in range(8 - PATCH_SIZE + 1):
            score = float(model.predict_proba(apply_patch(X_source, row, col))[:, 1].mean())
            rows.append({"row": row, "col": col, "target_score": score})
    rows.sort(key=lambda item: item["target_score"], reverse=True)
    return rows


def build_report(metrics):
    scan = metrics["scan"]
    lines = [
        "# LAB-08 report — image backdoor and trigger search",
        "",
        "Binary digits 3 vs 8. The attacker stamps a white 2x2 patch and relabels class-0 sources as class 1.",
        "",
        "| Model | Clean accuracy | ASR |",
        "|---|---:|---:|",
        f"| Clean | {metrics['clean']['accuracy']:.4f} | {metrics['clean']['asr']:.4f} |",
        f"| Backdoored | {metrics['backdoored']['accuracy']:.4f} | {metrics['backdoored']['asr']:.4f} |",
        f"| After filtering | {metrics['defended']['accuracy']:.4f} | {metrics['defended']['asr']:.4f} |",
        "",
        "## Trigger search",
        "",
        f"Top candidate: row {scan['best']['row']}, col {scan['best']['col']} "
        f"(score {scan['best']['target_score']:.4f}); true patch score "
        f"{scan['true_patch']['target_score']:.4f}; clean-model score at the true patch "
        f"{scan['clean_model_true_patch_score']:.4f}.",
        f"Detection succeeded: {scan['detected']}.",
        "",
        "## Mitigation",
        "",
        f"Filtered {metrics['defended']['flagged']} rows containing a solid white patch at the "
        f"discovered location; {metrics['defended']['poison_caught']} were poisons.",
        "",
        "## Limitations",
        "",
        "- The defender knows the patch size and value; a broader search space is harder.",
        "- A linear model on an easy binary subset makes the backdoor unusually clean.",
        "- Removing rows by trigger presence is not a general repair and can delete benign images.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Image backdoor and trigger search.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    X_train, X_test, y_train, y_test = load_binary()
    clean = LogisticRegression(max_iter=3000).fit(X_train, y_train)
    X_poisoned, y_poisoned, count = build_backdoor(X_train, y_train)
    backdoored = LogisticRegression(max_iter=3000).fit(X_poisoned, y_poisoned)

    source = X_test[y_test == 0]
    clean_metrics = {
        "accuracy": float(accuracy_score(y_test, clean.predict(X_test))),
        "asr": float((clean.predict(apply_patch(source, *TRUE_PATCH)) == 1).mean()),
    }
    backdoor_metrics = {
        "accuracy": float(accuracy_score(y_test, backdoored.predict(X_test))),
        "asr": float((backdoored.predict(apply_patch(source, *TRUE_PATCH)) == 1).mean()),
    }

    scan = scan_trigger(backdoored, source)
    best = scan[0]
    true_row, true_col = TRUE_PATCH
    true_score = next(r["target_score"] for r in scan if (r["row"], r["col"]) == TRUE_PATCH)
    clean_true_score = float(clean.predict_proba(apply_patch(source, true_row, true_col))[:, 1].mean())
    detected = (best["row"], best["col"]) == TRUE_PATCH

    images = X_poisoned.reshape(-1, 8, 8)
    flags = (images[:, true_row : true_row + PATCH_SIZE, true_col : true_col + PATCH_SIZE] == PATCH_VALUE).all(
        axis=(1, 2)
    )
    defended = LogisticRegression(max_iter=3000).fit(X_poisoned[~flags], y_poisoned[~flags])
    defended_metrics = {
        "accuracy": float(accuracy_score(y_test, defended.predict(X_test))),
        "asr": float((defended.predict(apply_patch(source, *TRUE_PATCH)) == 1).mean()),
        "flagged": int(flags.sum()),
        "poison_caught": int(flags[len(X_train):].sum()),
    }

    metrics = {
        "clean": clean_metrics,
        "backdoored": backdoor_metrics,
        "defended": defended_metrics,
        "poison_count": count,
        "poison_rate": float(count / len(y_train)),
        "scan": {
            "best": best,
            "true_patch": {"row": true_row, "col": true_col, "target_score": true_score},
            "clean_model_true_patch_score": clean_true_score,
            "detected": bool(detected),
        },
        "trigger": {"row": true_row, "col": true_col, "size": PATCH_SIZE, "value": PATCH_VALUE},
        "train_size": int(len(y_train)),
        "test_size": int(len(y_test)),
        "dataset": "sklearn.datasets.load_digits, classes 3 vs 8",
    }

    write_json(args.out / "metrics.json", metrics)
    write_json(
        args.out / "run.json",
        {"lab": "LAB-08", "seed": SEED, "poison_rate": POISON_RATE, "environment": environment()},
    )
    (args.out / "report.md").write_text(build_report(metrics), encoding="utf-8", newline="\n")
    write_json(
        args.out / "manifest.json",
        build_manifest(args.out, ["metrics.json", "run.json", "report.md"]),
    )
    print(f"clean acc={clean_metrics['accuracy']:.4f} asr={clean_metrics['asr']:.4f}")
    print(f"backdoor acc={backdoor_metrics['accuracy']:.4f} asr={backdoor_metrics['asr']:.4f}")
    print(f"best patch={best['row'],best['col']} score={best['target_score']:.4f} detected={detected}")
    print(f"filtered={defended_metrics['flagged']} caught={defended_metrics['poison_caught']} "
          f"asr={defended_metrics['asr']:.4f}")
    print(f"artifacts written to {args.out}")


if __name__ == "__main__":
    main()
