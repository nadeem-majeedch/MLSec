"""LAB-17 reference solution: a noisy centroid release with accounting.

Run from this directory:
    python solution.py --out artifacts

The lab uses synthetic two-class tabular data. Each class is clipped, summarized
as a centroid, and released with Laplace noise. Classes are disjoint, so
parallel composition lets the total budget equal the per-class epsilon. The
membership test is an empirical check, not a proof of privacy.
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
    return np.clip(X, -bound, bound)


def l1_sensitivity(n_per_class, bound=BOUND, dimensions=4):
    """Changing one clipped row moves the centroid vector by at most 2*B*d/n."""
    return 2.0 * bound * dimensions / n_per_class


def release_centroids(X_clipped, y, epsilon, sensitivity, seed=SEED):
    """Laplace mechanism on each class centroid; returns centroids and scales."""
    rng = np.random.default_rng(seed + int(round(epsilon * 1000)))
    scale = sensitivity / epsilon
    centroids = []
    for label in (0, 1):
        centroid = X_clipped[y == label].mean(axis=0)
        noisy = centroid + rng.laplace(0.0, scale, size=centroid.shape)
        centroids.append(noisy)
    return np.vstack(centroids), scale


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
    """Distance-based membership score; AUC 0.5 means no measured signal."""
    member_scores = -np.linalg.norm(
        release_clipped - centroids[release_y], axis=1
    )
    nonmember_scores = -np.linalg.norm(
        nonmember_clipped - centroids[nonmember_y], axis=1
    )
    labels = np.concatenate([np.ones(len(member_scores)), np.zeros(len(nonmember_scores))])
    scores = np.concatenate([member_scores, nonmember_scores])
    return float(roc_auc_score(labels, scores))


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
    clipped_fraction = float(np.mean(np.abs(release_X) > BOUND))
    metrics = {
        "data": {
            "release_rows": int(len(release_y)),
            "release_per_class": RELEASE_PER_CLASS,
            "test_rows": int(len(test_y)),
            "nonmember_rows": int(len(nonmember_y)),
            "clipped_fraction": round(clipped_fraction, 4),
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
            "distance test; a value near 0.5 does not prove privacy, and a value above "
            "0.5 would not by itself prove a formal violation."
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

The synthetic dataset has two Gaussian classes and four continuous features.
{RELEASE_PER_CLASS} rows per class are clipped to [-{BOUND:.0f}, {BOUND:.0f}] and
summarized by a class centroid. Laplace noise is added independently to each
centroid coordinate. The vector L1 sensitivity is

    Δ1 = 2 · B · d / n = 2 · {BOUND:.0f} · 4 / {RELEASE_PER_CLASS} = {sensitivity:.3f}

so each coordinate gets Laplace(scale = Δ1 / ε). The class datasets are disjoint
and have fixed size, so parallel composition gives a total budget of ε per
release, not 2ε.

Baseline nearest-centroid accuracy is {baseline_accuracy:.4f}. The clipped
fraction of release rows is {clipped_fraction:.4f}.

## Results

| ε | Laplace scale | Test accuracy | Mean centroid L2 error | Membership AUC |
|---:|---:|---:|---:|---:|
{table}

The audit configuration is ε = {AUDIT_EPSILON}, δ = 0. The complete claim is:
Laplace mechanism on two clipped class centroids, L1 sensitivity {sensitivity:.3f},
parallel composition, ε = {AUDIT_EPSILON}, δ = 0, synthetic data, nearest-centroid
utility {audit['accuracy']:.4f}.

## Interpretation

Small ε means more noise, larger centroid error, and lower utility. At ε = 0.02
the release is close to useless for this task; at ε = 4.0 utility is close to the
non-private baseline. That is the privacy-utility trade-off in this design, not a
universal curve.

The membership AUC stays near 0.5 across the sweep. That is an empirical result:
this particular distance test did not detect a membership signal. It is not a proof
that the release is private, and it cannot validate the formal guarantee.
Conversely, an AUC above 0.5 would be evidence worth investigating, not a formal
violation by itself. The formal claim comes from sensitivity, the mechanism, and
composition; the empirical test is a sanity check on one attack.

## Limitations

The data is synthetic and the release is a centroid, not a trained model. The
fixed-size disjoint-class assumption makes parallel composition valid; a real
system with overlapping users or variable group sizes would need a different
accounting argument. Clipping bounds the contribution but also biases the
estimate. The membership test is one naive distance score, not an adaptive
attacker. No claim is made about DP-SGD, deep models, or deployment-time inputs.
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
    print(f"artifacts written to {out.resolve()}")


if __name__ == "__main__":
    main()
