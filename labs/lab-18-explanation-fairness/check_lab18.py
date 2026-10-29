"""Independent checker for LAB-18.

Usage:
    python solution.py --out artifacts
    python check_lab18.py --artifacts artifacts

Exit code 0 means every check passed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

SEED = 42
N_ROWS = 1200


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def close(actual: float, expected: float, tol: float, label: str) -> None:
    if abs(float(actual) - expected) > tol:
        fail(f"{label}: {actual:.4f} is not within {tol:.3f} of {expected:.4f}")


def rebuild_models():
    rng = np.random.default_rng(SEED)
    group = rng.choice([0, 1], size=N_ROWS, p=[0.6, 0.4])
    X = rng.normal(size=(N_ROWS, 6))
    logit = 1.2 * X[:, 0] + 0.9 * X[:, 1] + 0.6 * X[:, 2] + 1.0 * group - 0.7
    probability = 1.0 / (1.0 + np.exp(-logit))
    y = rng.binomial(1, probability)
    X_train, X_test, y_train, y_test, group_train, group_test = train_test_split(
        X, y, group, test_size=0.3, random_state=SEED, stratify=y * 2 + group
    )
    baseline = LogisticRegression(max_iter=2000, random_state=SEED).fit(X_train, y_train)
    counts = {value: int((group_train == value).sum()) for value in (0, 1)}
    weights = np.array([len(group_train) / (2.0 * counts[int(value)]) for value in group_train])
    reweighted = LogisticRegression(max_iter=2000, random_state=SEED).fit(
        X_train, y_train, sample_weight=weights
    )
    return baseline, reweighted, X_test, y_test, group_test


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-18 artifacts.")
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    root = args.artifacts

    metrics = load_json(root / "metrics.json")
    run = load_json(root / "run.json")
    manifest = load_json(root / "manifest.json")
    report = root / "report.md"
    if not report.exists():
        fail("missing report.md")

    required = {"metrics.json", "run.json", "report.md"}
    paths = {entry["path"] for entry in manifest.get("files", [])}
    if not required <= paths:
        fail(f"manifest does not cover {sorted(required - paths)}")
    if run.get("lab") != "LAB-18":
        fail("run.json lab is not LAB-18")
    if float(run.get("noise_sigma", 0)) != 0.25:
        fail("run.json must record noise_sigma 0.25")
    if int(run.get("top_k", 0)) != 2:
        fail("run.json must record top_k 2")

    baseline, reweighted, X_test, y_test, _ = rebuild_models()
    reported_base = metrics["models"]["baseline"]
    reported_reweight = metrics["models"]["reweighted"]
    close(float(reported_base["overall_accuracy"]), float((baseline.predict(X_test) == y_test).mean()), 0.01, "baseline accuracy")
    close(float(reported_reweight["overall_accuracy"]), float((reweighted.predict(X_test) == y_test).mean()), 0.01, "reweighted accuracy")

    for name, block in (("baseline", reported_base), ("reweighted", reported_reweight)):
        for group in ("0", "1"):
            subgroup = block["subgroups"][group]
            for key in ("accuracy", "tpr", "fpr", "selection_rate"):
                if not 0.0 <= float(subgroup[key]) <= 1.0:
                    fail(f"{name}.group{group}.{key} outside [0, 1]")
            if int(subgroup["n"]) <= 0:
                fail(f"{name}.group{group} has no rows")
        dp = abs(
            float(block["subgroups"]["0"]["selection_rate"])
            - float(block["subgroups"]["1"]["selection_rate"])
        )
        eo = max(
            abs(float(block["subgroups"]["0"]["tpr"]) - float(block["subgroups"]["1"]["tpr"])),
            abs(float(block["subgroups"]["0"]["fpr"]) - float(block["subgroups"]["1"]["fpr"])),
        )
        close(float(block["gaps"]["demographic_parity"]), dp, 0.002, f"{name} DP gap")
        close(float(block["gaps"]["equalized_odds"]), eo, 0.002, f"{name} EO gap")
        for key in ("demographic_parity", "equalized_odds"):
            low, high = block["gaps_95ci"][key]
            if not 0.0 <= float(low) <= float(high) <= 1.0:
                fail(f"{name} {key} bootstrap interval is not a valid ordered interval")

    base_dp = float(reported_base["gaps"]["demographic_parity"])
    base_eo = float(reported_base["gaps"]["equalized_odds"])
    re_dp = float(reported_reweight["gaps"]["demographic_parity"])
    re_eo = float(reported_reweight["gaps"]["equalized_odds"])
    if not re_eo < base_eo:
        fail("reweighting must reduce the equalized-odds gap in this setup")
    if not re_dp > base_dp:
        fail("reweighting must increase the demographic-parity gap in this setup (metric conflict)")
    if not float(reported_reweight["overall_accuracy"]) < float(reported_base["overall_accuracy"]) - 0.005:
        fail("reweighting must show an accuracy cost of at least 0.005")

    explanations = metrics["explanation_stability"]
    for name in ("baseline", "reweighted"):
        for method in ("gradient_x_input", "occlusion"):
            block = explanations[name][method]
            if not -1.0 <= float(block["mean_spearman"]) <= 1.0:
                fail(f"{name}/{method} Spearman outside [-1, 1]")
            if not 0.0 <= float(block["mean_top2_overlap"]) <= 1.0:
                fail(f"{name}/{method} top-k overlap outside [0, 1]")
            if int(block["prediction_preserved_rows"]) <= 0:
                fail(f"{name}/{method} has no prediction-preserved rows")
            if not 0.05 <= float(block["top_feature_flip_rate_when_prediction_preserved"]) <= 0.30:
                fail(f"{name}/{method} flip rate must be between 0.05 and 0.30")
            if not 0.80 <= float(block["mean_spearman"]) <= 1.0:
                fail(f"{name}/{method} stability is outside the expected 0.80-1.00 band")

    text = report.read_text(encoding="utf-8").lower()
    for phrase in ("demographic parity", "equalized odds", "stability", "trade-off", "limitations"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print(f"PASS baseline accuracy reproduces: {reported_base['overall_accuracy']:.4f}")
    print(f"PASS reweighted accuracy reproduces: {reported_reweight['overall_accuracy']:.4f}")
    print(f"PASS metric conflict: EO {base_eo:.4f} -> {re_eo:.4f}; DP {base_dp:.4f} -> {re_dp:.4f}")
    print("PASS bootstrap intervals are ordered and inside [0, 1]")
    print(f"PASS explanation stability: Spearman {explanations['baseline']['gradient_x_input']['mean_spearman']:.4f}, flip {explanations['baseline']['gradient_x_input']['top_feature_flip_rate_when_prediction_preserved']:.4f}")
    print("PASS report names both fairness metrics, stability, trade-off, and limitations")
    print("LAB-18 CHECK PASSED")


if __name__ == "__main__":
    main()
