"""Independent checker for LAB-10."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-10 artifacts.")
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
    rng = np.random.default_rng(31)
    order = rng.permutation(len(X))
    members, nonmembers = order[:500], order[500:1000]
    model = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1).fit(
        X[members], y[members]
    )
    member_scores = model.predict_proba(X[members]).max(axis=1)
    nonmember_scores = model.predict_proba(X[nonmembers]).max(axis=1)
    labels = np.concatenate([np.ones(500), np.zeros(500)])
    scores = np.concatenate([member_scores, nonmember_scores])
    auc = float(roc_auc_score(labels, scores))
    fpr, tpr, _ = roc_curve(labels, scores)

    if abs(auc - metrics["auc"]) > 0.005:
        fail("AUC does not reproduce")
    if abs(float((member_scores >= np.quantile(nonmember_scores, 0.95)).mean()) - metrics["tpr_at_threshold"]) > 0.005:
        fail("threshold TPR does not reproduce")
    if abs(float(member_scores.mean()) - metrics["mean_member_confidence"]) > 0.005:
        fail("mean member confidence does not reproduce")
    if abs(float(nonmember_scores.mean()) - metrics["mean_nonmember_confidence"]) > 0.005:
        fail("mean nonmember confidence does not reproduce")
    if abs(accuracy_score(y[members], model.predict(X[members])) - metrics["member_accuracy"]) > 0.005:
        fail("member accuracy does not reproduce")
    if abs(accuracy_score(y[nonmembers], model.predict(X[nonmembers])) - metrics["nonmember_accuracy"]) > 0.005:
        fail("nonmember accuracy does not reproduce")

    if metrics["mean_member_confidence"] <= metrics["mean_nonmember_confidence"]:
        fail("members should be more confident on average")
    if metrics["auc"] < 0.75:
        fail("membership signal is too weak for the reference setup")
    if metrics["tpr_at_1pct"] > 0.20:
        fail("TPR at 1% FPR is implausibly high")
    if not metrics["tpr_at_1pct"] < metrics["tpr_at_5pct"]:
        fail("TPR should increase with the FPR budget")
    if abs(metrics["tpr_at_threshold"] - metrics["tpr_at_5pct"]) > 0.01:
        fail("threshold TPR and TPR at 5% FPR should agree")

    text = (root / "report.md").read_text(encoding="utf-8").lower()
    for phrase in ("not proof", "limitations", "confidence"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print(f"PASS AUC reproduces: {auc:.4f}")
    print(
        f"PASS mean confidence member={member_scores.mean():.4f} "
        f"nonmember={nonmember_scores.mean():.4f}"
    )
    print(f"PASS TPR@1%={metrics['tpr_at_1pct']:.4f}, TPR@5%={metrics['tpr_at_5pct']:.4f}")
    print("PASS report explains that confidence is not proof of membership")
    print("LAB-10 CHECK PASSED")


if __name__ == "__main__":
    main()
