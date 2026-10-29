"""Independent checker for LAB-17.

Usage:
    python solution.py --out artifacts
    python check_lab17.py --artifacts artifacts

Exit code 0 means every check passed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

SEED = 42
N_PER_CLASS = 800
RELEASE_PER_CLASS = 500
TEST_PER_CLASS = 150
BOUND = 3.0
EPSILONS = (0.02, 0.1, 0.5, 1.0, 4.0)


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


def rebuild_baseline() -> float:
    rng = np.random.default_rng(SEED)
    means = np.array([[0.0, 0.0, 0.0, 0.0], [1.2, 1.0, 0.8, 0.6]])
    release, test = [], []
    for label in (0, 1):
        sample = rng.normal(means[label], 1.0, size=(N_PER_CLASS, 4))
        release.append((sample[:RELEASE_PER_CLASS], np.full(RELEASE_PER_CLASS, label)))
        test.append(
            (
                sample[RELEASE_PER_CLASS : RELEASE_PER_CLASS + TEST_PER_CLASS],
                np.full(TEST_PER_CLASS, label),
            )
        )
    release_X = np.clip(np.vstack([item[0] for item in release]), -BOUND, BOUND)
    release_y = np.concatenate([item[1] for item in release])
    test_X = np.clip(np.vstack([item[0] for item in test]), -BOUND, BOUND)
    test_y = np.concatenate([item[1] for item in test])
    centroids = np.vstack([release_X[release_y == label].mean(axis=0) for label in (0, 1)])
    distances = ((test_X[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
    return float((np.argmin(distances, axis=1) == test_y).mean())


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-17 artifacts.")
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
    if run.get("lab") != "LAB-17":
        fail("run.json lab is not LAB-17")
    if tuple(float(value) for value in run.get("epsilons", [])) != EPSILONS:
        fail("run.json must record the five epsilon values")
    if float(run.get("delta", -1)) != 0.0:
        fail("run.json delta must be 0.0")
    if run.get("composition") != "parallel":
        fail("run.json must record parallel composition")

    sensitivity = 2.0 * BOUND * 4 / RELEASE_PER_CLASS
    close(float(metrics["mechanism"]["l1_sensitivity"]), sensitivity, 1e-6, "L1 sensitivity")
    if float(metrics["data"]["release_rows"]) != 1000:
        fail("release must contain 1,000 rows")
    if float(metrics["data"]["release_per_class"]) != RELEASE_PER_CLASS:
        fail("release must contain 500 rows per class")

    baseline = rebuild_baseline()
    close(float(metrics["baseline"]["accuracy"]), baseline, 0.01, "baseline accuracy")
    if baseline < 0.75:
        fail("baseline nearest-centroid accuracy must exceed 0.75")

    releases = metrics.get("releases", [])
    if len(releases) != len(EPSILONS):
        fail("metrics must contain one release per epsilon")
    for item in releases:
        epsilon = float(item["epsilon"])
        expected_scale = sensitivity / epsilon
        close(float(item["laplace_scale"]), expected_scale, 1e-4, f"scale at epsilon={epsilon}")
        close(float(item["delta"]), 0.0, 1e-9, f"delta at epsilon={epsilon}")
        if not 0.0 <= float(item["accuracy"]) <= 1.0:
            fail("accuracy outside [0, 1]")
        if not 0.0 <= float(item["membership_auc"]) <= 1.0:
            fail("membership AUC outside [0, 1]")
        if not 0.45 <= float(item["membership_auc"]) <= 0.60:
            fail("membership AUC is outside the near-chance band 0.45-0.60")

    by_epsilon = {float(item["epsilon"]): item for item in releases}
    if float(by_epsilon[0.02]["accuracy"]) > float(by_epsilon[0.5]["accuracy"]):
        fail("low-budget accuracy must not exceed mid-budget accuracy")
    if float(by_epsilon[0.02]["centroid_l2_error"]) < float(by_epsilon[0.5]["centroid_l2_error"]):
        fail("low-budget centroid error must be larger than mid-budget error")
    if float(by_epsilon[4.0]["accuracy"]) < float(by_epsilon[0.5]["accuracy"]):
        fail("high-budget accuracy must be at least mid-budget accuracy")
    if float(by_epsilon[4.0]["centroid_l2_error"]) > float(by_epsilon[0.5]["centroid_l2_error"]):
        fail("high-budget centroid error must be at most mid-budget error")

    audit = metrics["audit_release"]
    if float(audit["epsilon"]) != 0.5:
        fail("audit release must use epsilon=0.5")
    if abs(float(audit["accuracy"]) - float(by_epsilon[0.5]["accuracy"])) > 1e-9:
        fail("audit release must match the epsilon=0.5 row")

    text = report.read_text(encoding="utf-8").lower()
    for phrase in ("sensitivity", "parallel composition", "not a proof", "limitations"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print(f"PASS baseline accuracy reproduces: {baseline:.4f}")
    print(f"PASS L1 sensitivity: {sensitivity:.4f} for 4 dimensions, B=3, n=500")
    print(f"PASS epsilon=0.02 accuracy={by_epsilon[0.02]['accuracy']:.4f} error={by_epsilon[0.02]['centroid_l2_error']:.4f}")
    print(f"PASS epsilon=0.50 accuracy={by_epsilon[0.5]['accuracy']:.4f} error={by_epsilon[0.5]['centroid_l2_error']:.4f}")
    print(f"PASS epsilon=4.00 accuracy={by_epsilon[4.0]['accuracy']:.4f} error={by_epsilon[4.0]['centroid_l2_error']:.4f}")
    print("PASS membership AUC stays near chance and the report calls it empirical, not proof")
    print("LAB-17 CHECK PASSED")


if __name__ == "__main__":
    main()
