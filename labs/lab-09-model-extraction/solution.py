"""LAB-09 reference solution: model extraction through a local prediction API.

Run from this directory:
    python solution.py --out artifacts
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

SEED = 21
BUDGETS = [50, 100, 200, 500]
DIM = 10
ACTIVE_BATCH = 20
INITIAL_RANDOM = 20


class PredictionAPI:
    """A local stand-in for a remote classifier with a hard query budget."""

    def __init__(self, model, budget):
        self.model = model
        self.budget = budget
        self.used = 0

    def query(self, X):
        X = np.asarray(X, dtype=float)
        if self.used + len(X) > self.budget:
            raise RuntimeError("query budget exceeded")
        self.used += len(X)
        return self.model.predict(X)


def make_data():
    rng = np.random.default_rng(SEED)
    centers = rng.normal(0.0, 2.0, (5, DIM))

    def sample(n):
        labels = rng.integers(0, 5, n)
        return centers[labels] + rng.normal(0.0, 1.0, (n, DIM)), labels

    X_train, y_train = sample(2500)
    X_test, y_test = sample(1500)
    return X_train, y_train, X_test, y_test


def fit_teacher(X_train, y_train):
    return MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=1500, random_state=42).fit(
        X_train, y_train
    )


def fidelity(surrogate, teacher, X_test):
    return float(accuracy_score(teacher.predict(X_test), surrogate.predict(X_test)))


def random_queries(teacher, pool, budget):
    api = PredictionAPI(teacher, budget)
    queries = pool[:budget]
    labels = api.query(queries)
    surrogate = RandomForestClassifier(n_estimators=200, random_state=0, n_jobs=-1).fit(
        queries, labels
    )
    return surrogate, api


def active_queries(teacher, pool, budget, extra_pool):
    api = PredictionAPI(teacher, budget)
    queries = list(pool[:INITIAL_RANDOM])
    labels = list(api.query(np.array(queries)))
    remaining = np.ones(len(extra_pool), dtype=bool)
    while len(queries) < budget:
        surrogate = RandomForestClassifier(n_estimators=100, random_state=0, n_jobs=-1).fit(
            np.array(queries), np.array(labels)
        )
        take = min(ACTIVE_BATCH, budget - len(queries))
        candidates = np.where(remaining)[0]
        probabilities = surrogate.predict_proba(extra_pool[candidates])
        entropy = -(probabilities * np.log(probabilities + 1e-12)).sum(axis=1)
        chosen = candidates[np.argsort(entropy)[-take:]]
        queries.extend(extra_pool[chosen])
        labels.extend(api.query(extra_pool[chosen]))
        remaining[chosen] = False
    surrogate = RandomForestClassifier(n_estimators=200, random_state=0, n_jobs=-1).fit(
        np.array(queries), np.array(labels)
    )
    return surrogate, api


def build_report(metrics):
    lines = [
        "# LAB-09 report — model extraction",
        "",
        f"Teacher: MLP on a 10-dimensional synthetic 5-class problem; teacher test accuracy "
        f"{metrics['teacher_accuracy']:.4f}.",
        "Surrogate: random forest trained only on API labels.",
        "",
        "| Budget | Random fidelity | Random task accuracy | Active fidelity | Active task accuracy |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in metrics["curve"]:
        lines.append(
            f"| {row['budget']} | {row['random_fidelity']:.4f} | {row['random_accuracy']:.4f} | "
            f"{row['active_fidelity']:.4f} | {row['active_accuracy']:.4f} |"
        )
    lines += [
        "",
        "Fidelity is agreement with the teacher on 1,500 held-out points; task accuracy uses the true labels.",
        "",
        "## Threat model",
        "",
        "The attacker can query a local prediction endpoint with a hard budget and receives hard labels.",
        "The target model, training data, and gradients are not available.",
        "",
        "## Limitations",
        "",
        "- The attacker knows the input domain and can sample it uniformly.",
        "- A low-dimensional synthetic teacher is easier to extract than a real service.",
        "- No rate limiting, query monitoring, or output rounding is applied.",
        "- Fidelity is not the same as stolen intellectual property or task equivalence.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Model extraction with a query budget.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    X_train, y_train, X_test, y_test = make_data()
    teacher = fit_teacher(X_train, y_train)
    rng = np.random.default_rng(SEED)
    pool = rng.uniform(-5.0, 5.0, (30000, DIM))
    order = rng.permutation(len(pool))
    random_pool = pool[order]
    active_pool = pool[rng.permutation(len(pool))]

    metrics = {
        "teacher_accuracy": float(accuracy_score(y_test, teacher.predict(X_test))),
        "budgets": BUDGETS,
        "curve": [],
        "dataset": "synthetic 10-D Gaussian mixture, 5 classes",
    }
    for budget in BUDGETS:
        random_surrogate, random_api = random_queries(teacher, random_pool, budget)
        active_surrogate, active_api = active_queries(teacher, random_pool, budget, active_pool)
        metrics["curve"].append(
            {
                "budget": budget,
                "random_queries": random_api.used,
                "active_queries": active_api.used,
                "random_fidelity": fidelity(random_surrogate, teacher, X_test),
                "random_accuracy": float(accuracy_score(y_test, random_surrogate.predict(X_test))),
                "active_fidelity": fidelity(active_surrogate, teacher, X_test),
                "active_accuracy": float(accuracy_score(y_test, active_surrogate.predict(X_test))),
            }
        )

    write_json(args.out / "metrics.json", metrics)
    write_json(
        args.out / "run.json",
        {
            "lab": "LAB-09",
            "seed": SEED,
            "budgets": BUDGETS,
            "teacher": "MLPClassifier(64, 32)",
            "surrogate": "RandomForestClassifier(200)",
            "environment": environment(),
        },
    )
    (args.out / "report.md").write_text(build_report(metrics), encoding="utf-8", newline="\n")
    write_json(
        args.out / "manifest.json",
        build_manifest(args.out, ["metrics.json", "run.json", "report.md"]),
    )
    print(f"teacher accuracy={metrics['teacher_accuracy']:.4f}")
    for row in metrics["curve"]:
        print(
            f"budget={row['budget']} random_fid={row['random_fidelity']:.4f} "
            f"active_fid={row['active_fidelity']:.4f} active_acc={row['active_accuracy']:.4f}"
        )
    print(f"artifacts written to {args.out}")


if __name__ == "__main__":
    main()
