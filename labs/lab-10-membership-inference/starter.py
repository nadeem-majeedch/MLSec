"""LAB-10 starter: membership inference by confidence thresholding.

Fill in the TODO blocks. Run the same command the solution uses:

    python starter.py --out artifacts
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
    """Return X, y, member indices, nonmember indices. This part is given."""
    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    rng = np.random.default_rng(SEED)
    order = rng.permutation(len(X))
    members = order[:N_MEMBERS]
    nonmembers = order[N_MEMBERS : N_MEMBERS + N_NONMEMBERS]
    return X, y, members, nonmembers


def confidence_scores(model, X):
    # TODO 1: return one membership score per row, using the model's predicted
    # probabilities. A larger score should mean "more likely a member".
    # Hint: model.predict_proba(X) returns one row per sample.
    raise NotImplementedError("TODO 1: implement confidence_scores")


def tpr_at_fpr(labels, scores, limit):
    # TODO 2: compute the true-positive rate at a false-positive-rate budget.
    # Use sklearn.metrics.roc_curve, keep the points where fpr <= limit,
    # and return the largest tpr among them.
    raise NotImplementedError("TODO 2: implement tpr_at_fpr")


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
    (args.out / "report.md").write_text(
        "# LAB-10 report\n\n"
        "TODO 3: write at least five sentences. Report the AUC, the TPR at a 1% "
        "false-positive budget, and the mean confidence gap. State explicitly that "
        "confidence is not proof of membership, and list your limitations.\n",
        encoding="utf-8",
        newline="\n",
    )
    write_json(
        args.out / "manifest.json",
        build_manifest(args.out, ["metrics.json", "run.json", "report.md"]),
    )
    print(f"AUC={metrics['auc']:.4f} TPR@1%={metrics['tpr_at_1pct']:.4f}")
    print(f"artifacts written to {args.out}")


if __name__ == "__main__":
    main()
