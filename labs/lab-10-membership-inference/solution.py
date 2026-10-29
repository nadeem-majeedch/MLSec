"""LAB-10 reference solution: a membership-inference threshold attack.

Run from this directory:
    python solution.py --out artifacts
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

SEED = 31
N_MEMBERS = 500
N_NONMEMBERS = 500


def split_data():
    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    rng = np.random.default_rng(SEED)
    order = rng.permutation(len(X))
    members = order[:N_MEMBERS]
    nonmembers = order[N_MEMBERS : N_MEMBERS + N_NONMEMBERS]
    return X, y, members, nonmembers


def confidence_scores(model, X):
    return model.predict_proba(X).max(axis=1)


def tpr_at_fpr(labels, scores, limit):
    fpr, tpr, _ = roc_curve(labels, scores)
    eligible = fpr <= limit + 1e-12
    return float(tpr[eligible][-1]) if eligible.any() else 0.0


def build_report(metrics):
    lines = [
        "# LAB-10 report — membership inference",
        "",
        "Target: random forest trained on 500 digits examples. Nonmembers come from the same "
        "dataset but were never used for training.",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Member training accuracy | {metrics['member_accuracy']:.4f} |",
        f"| Nonmember accuracy | {metrics['nonmember_accuracy']:.4f} |",
        f"| Mean member confidence | {metrics['mean_member_confidence']:.4f} |",
        f"| Mean nonmember confidence | {metrics['mean_nonmember_confidence']:.4f} |",
        f"| ROC-AUC | {metrics['auc']:.4f} |",
        f"| TPR at FPR ≤ 1% | {metrics['tpr_at_1pct']:.4f} |",
        f"| TPR at FPR ≤ 5% | {metrics['tpr_at_5pct']:.4f} |",
        "",
        "## Interpretation",
        "",
        "Members are more confident on average, but the distributions overlap heavily. A high "
        "confidence is not proof of membership: a nonmember can be easy to classify, and a member "
        "can be atypical. At a 1% false-positive budget, most members are not detected.",
        "",
        "## Limitations",
        "",
        "- Bundled public digits data, not private data about people.",
        "- One model family, one split, and one score (maximum softmax confidence).",
        "- The nonmember set is drawn from the same distribution; distribution shift changes the attack.",
        "- A single threshold is not a privacy guarantee; low-FPR tails matter.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Membership inference threshold attack.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    X, y, members, nonmembers = split_data()
    model = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1).fit(
        X[members], y[members]
    )
    member_scores = confidence_scores(model, X[members])
    nonmember_scores = confidence_scores(model, X[nonmembers])
    labels = np.concatenate([np.ones(len(member_scores)), np.zeros(len(nonmember_scores))])
    scores = np.concatenate([member_scores, nonmember_scores])

    threshold_5 = float(np.quantile(nonmember_scores, 0.95))
    metrics = {
        "n_members": int(len(members)),
        "n_nonmembers": int(len(nonmembers)),
        "member_accuracy": float(accuracy_score(y[members], model.predict(X[members]))),
        "nonmember_accuracy": float(accuracy_score(y[nonmembers], model.predict(X[nonmembers]))),
        "mean_member_confidence": float(member_scores.mean()),
        "mean_nonmember_confidence": float(nonmember_scores.mean()),
        "auc": float(roc_auc_score(labels, scores)),
        "tpr_at_1pct": tpr_at_fpr(labels, scores, 0.01),
        "tpr_at_5pct": tpr_at_fpr(labels, scores, 0.05),
        "threshold_at_5pct": threshold_5,
        "tpr_at_threshold": float((member_scores >= threshold_5).mean()),
        "fpr_at_threshold": float((nonmember_scores >= threshold_5).mean()),
        "score": "maximum predicted class probability",
        "dataset": "sklearn.datasets.load_digits",
    }

    write_json(args.out / "metrics.json", metrics)
    write_json(
        args.out / "run.json",
        {"lab": "LAB-10", "seed": SEED, "model": "RandomForestClassifier(300)", "environment": environment()},
    )
    (args.out / "report.md").write_text(build_report(metrics), encoding="utf-8", newline="\n")
    write_json(
        args.out / "manifest.json",
        build_manifest(args.out, ["metrics.json", "run.json", "report.md"]),
    )
    for key in (
        "member_accuracy",
        "nonmember_accuracy",
        "mean_member_confidence",
        "mean_nonmember_confidence",
        "auc",
        "tpr_at_1pct",
        "tpr_at_5pct",
    ):
        print(f"{key}={metrics[key]:.4f}")
    print(f"threshold@5%={threshold_5:.4f} tpr={metrics['tpr_at_threshold']:.4f} fpr={metrics['fpr_at_threshold']:.4f}")
    print(f"artifacts written to {args.out}")


if __name__ == "__main__":
    main()
