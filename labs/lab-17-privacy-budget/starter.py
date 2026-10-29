"""LAB-17 starter: a noisy centroid release with accounting.

Run from this directory:
    python starter.py --out artifacts

Three TODO blocks: clip_features, release_centroids, membership_auc. The data
generator, sensitivity formula, utility metrics, and report template are given.
Complete the TODOs, then run check_lab17.py on your artifacts.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

SEED = 42
N_PER_CLASS = 800
RELEASE_PER_CLASS = 500
TEST_PER_CLASS = 150
BOUND = 3.0
EPSILONS = (0.02, 0.1, 0.5, 1.0, 4.0)
AUDIT_EPSILON = 0.5


def make_data():
    """Two Gaussian classes, split into release, test, and nonmember sets."""
    rng = np.random.default_rng(SEED)
    means = np.array([[0.0, 0.0, 0.0, 0.0], [1.2, 1.0, 0.8, 0.6]])
    scales = np.array([1.0, 1.0, 1.0, 1.0])
    release_X, release_y = [], []
    test_X, test_y = [], []
    nonmember_X, nonmember_y = [], []
    for label in (0, 1):
        sample = rng.normal(means[label], scales, size=(N_PER_CLASS, 4))
        release_X.append(sample[:RELEASE_PER_CLASS])
        release_y.append(np.full(RELEASE_PER_CLASS, label))
        test_X.append(sample[RELEASE_PER_CLASS : RELEASE_PER_CLASS + TEST_PER_CLASS])
        test_y.append(np.full(TEST_PER_CLASS, label))
        nonmember_X.append(sample[RELEASE_PER_CLASS + TEST_PER_CLASS :])
        nonmember_y.append(np.full(TEST_PER_CLASS, label))
    return (
        np.vstack(release_X),
        np.concatenate(release_y),
        np.vstack(test_X),
        np.concatenate(test_y),
        np.vstack(nonmember_X),
        np.concatenate(nonmember_y),
    )


def clip_features(X, bound=BOUND):
    """TODO 1: clip every feature to [-bound, bound] without mutating X."""
    raise NotImplementedError("TODO 1: implement clip_features")


def l1_sensitivity(n_per_class, bound=BOUND, dimensions=4):
    """Changing one clipped row moves the centroid vector by at most 2*B*d/n."""
    return 2.0 * bound * dimensions / n_per_class


def release_centroids(X_clipped, y, epsilon, sensitivity, seed=SEED):
    """TODO 2: release two class centroids with the Laplace mechanism.

    For each class, compute the clipped centroid, then add Laplace noise with
    scale `sensitivity / epsilon` independently to each coordinate. Use
    np.random.default_rng(seed + int(round(epsilon * 1000))). Return the 2x4
    centroids and the scale.
    """
    raise NotImplementedError("TODO 2: implement release_centroids")


def predict(centroids, X):
    distances = ((X[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
    return np.argmin(distances, axis=1)


def accuracy(centroids, X, y):
    return float((predict(centroids, X) == y).mean())


def centroid_error(centroids, X_clipped, y):
    errors = []
    for label in (0, 1):
        truth = X_clipped[y == label].mean(axis=0)
        errors.append(float(np.linalg.norm(centroids[label] - truth)))
    return float(np.mean(errors))


def membership_auc(centroids, release_clipped, release_y, nonmember_clipped, nonmember_y):
    """TODO 3: compute a distance-based membership AUC.

    Score each row as the negative Euclidean distance to its class's noisy
    centroid. Stack member scores (label 1) and nonmember scores (label 0), then
    return sklearn.metrics.roc_auc_score.
    """
    raise NotImplementedError("TODO 3: implement membership_auc")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the LAB-17 privacy release.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()

    release_X, release_y, test_X, test_y, nonmember_X, nonmember_y = make_data()
    release_clipped = clip_features(release_X)
    test_clipped = clip_features(test_X)
    nonmember_clipped = clip_features(nonmember_X)
    sensitivity = l1_sensitivity(RELEASE_PER_CLASS)

    baseline_centroids = np.vstack(
        [release_clipped[release_y == label].mean(axis=0) for label in (0, 1)]
    )
    baseline_accuracy = accuracy(baseline_centroids, test_clipped, test_y)

    releases = []
    for epsilon in EPSILONS:
        centroids, scale = release_centroids(
            release_clipped, release_y, epsilon, sensitivity
        )
        releases.append(
            {
                "epsilon": epsilon,
                "delta": 0.0,
                "laplace_scale": round(scale, 6),
                "accuracy": round(accuracy(centroids, test_clipped, test_y), 4),
                "centroid_l2_error": round(
                    centroid_error(centroids, release_clipped, release_y), 4
                ),
                "membership_auc": round(
                    membership_auc(
                        centroids,
                        release_clipped,
                        release_y,
                        nonmember_clipped,
                        nonmember_y,
                    ),
                    4,
                ),
                "centroids": np.round(centroids, 4).tolist(),
            }
        )

    audit = next(item for item in releases if item["epsilon"] == AUDIT_EPSILON)
    metrics = {
        "data": {
            "release_rows": int(len(release_y)),
            "release_per_class": RELEASE_PER_CLASS,
            "test_rows": int(len(test_y)),
            "nonmember_rows": int(len(nonmember_y)),
            "clipped_fraction": round(float(np.mean(np.abs(release_X) > BOUND)), 4),
        },
        "mechanism": {
            "name": "laplace",
            "dimensions": 4,
            "bound": BOUND,
            "l1_sensitivity": round(sensitivity, 6),
            "composition": "parallel over disjoint classes",
            "total_epsilon_equals_class_epsilon": True,
            "delta": 0.0,
        },
        "baseline": {
            "accuracy": round(baseline_accuracy, 4),
            "centroids": np.round(baseline_centroids, 4).tolist(),
        },
        "releases": releases,
        "audit_release": audit,
        "note": (
            "Synthetic data, seed 42. Parallel composition applies because the class "
            "datasets are disjoint and fixed-size. The membership AUC is an empirical "
            "distance test; a value near 0.5 does not prove privacy."
        ),
    }

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "metrics.json", metrics)
    write_json(
        out / "run.json",
        {
            "lab": "LAB-17",
            "seed": SEED,
            "epsilons": list(EPSILONS),
            "audit_epsilon": AUDIT_EPSILON,
            "delta": 0.0,
            "release_per_class": RELEASE_PER_CLASS,
            "sensitivity": round(sensitivity, 6),
            "composition": "parallel",
            "environment": environment(),
        },
    )

    table = "\n".join(
        f"| {item['epsilon']:.2f} | {item['laplace_scale']:.4f} | "
        f"{item['accuracy']:.4f} | {item['centroid_l2_error']:.4f} | "
        f"{item['membership_auc']:.4f} |"
        for item in releases
    )
    report = f"""# LAB-17 report

## Release design

The synthetic dataset has two Gaussian classes and four features. {RELEASE_PER_CLASS}
rows per class are clipped to [-{BOUND:.0f}, {BOUND:.0f}] and summarized by a class
centroid. Laplace noise is added to each coordinate with scale Δ1 / ε, where
Δ1 = 2 · B · d / n = {sensitivity:.3f}. Classes are disjoint and fixed-size, so
parallel composition gives total budget ε, not 2ε.

Baseline nearest-centroid accuracy is {baseline_accuracy:.4f}.

## Results

| ε | Laplace scale | Test accuracy | Mean centroid L2 error | Membership AUC |
|---:|---:|---:|---:|---:|
{table}

Audit claim: Laplace mechanism, L1 sensitivity {sensitivity:.3f}, parallel
composition, ε = {AUDIT_EPSILON}, δ = 0, synthetic data, utility
{audit['accuracy']:.4f}.

## Interpretation

Small ε adds more noise and lowers utility. The membership AUC remains near 0.5:
that is an empirical result from one distance test, not a proof of privacy. The
formal claim rests on sensitivity, the mechanism, and composition.

## Limitations

The release is a centroid, not a trained model. Fixed-size disjoint classes make
parallel composition valid; overlapping users or variable group sizes would need
different accounting. Clipping biases the estimate, and the membership test is
one naive score rather than an adaptive attacker.
"""
    (out / "report.md").write_text(report, encoding="utf-8", newline="\n")
    write_json(out / "manifest.json", build_manifest(out, ["metrics.json", "run.json", "report.md"]))

    print(f"baseline accuracy: {baseline_accuracy:.4f}")
    for item in releases:
        print(
            f"epsilon={item['epsilon']:.2f} scale={item['laplace_scale']:.4f} "
            f"accuracy={item['accuracy']:.4f} error={item['centroid_l2_error']:.4f} "
            f"mia_auc={item['membership_auc']:.4f}"
        )


if __name__ == "__main__":
    main()
