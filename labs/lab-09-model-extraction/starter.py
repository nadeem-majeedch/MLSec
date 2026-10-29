"""LAB-09 starter: model extraction with a query budget.

Run from this directory:
    python starter.py --out artifacts

TODO blocks: PredictionAPI.query and the entropy selection in active_queries.
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
    def __init__(self, model, budget):
        self.model = model
        self.budget = budget
        self.used = 0

    def query(self, X):
        """TODO 1: enforce the budget, count queries, and return hard labels."""
        raise NotImplementedError("TODO 1: implement PredictionAPI.query")


def make_data():
    rng = np.random.default_rng(SEED)
    centers = rng.normal(0.0, 2.0, (5, DIM))

    def sample(n):
        labels = rng.integers(0, 5, n)
        return centers[labels] + rng.normal(0.0, 1.0, (n, DIM)), labels

    return (*sample(2500), *sample(1500))


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
        # TODO 2: rank candidates by predictive entropy (highest first),
        # choose ``take`` of them, query the API, append, and mark them used.
        raise NotImplementedError("TODO 2: implement entropy selection")
    surrogate = RandomForestClassifier(n_estimators=200, random_state=0, n_jobs=-1).fit(
        np.array(queries), np.array(labels)
    )
    return surrogate, api


def main() -> None:
    parser = argparse.ArgumentParser(description="Starter: model extraction.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    X_train, y_train, X_test, y_test = make_data()
    teacher = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=1500, random_state=42).fit(
        X_train, y_train
    )
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
    try:
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
    except NotImplementedError as exc:
        raise SystemExit(f"starter incomplete: {exc}") from exc

    write_json(args.out / "metrics.json", metrics)
    write_json(args.out / "run.json", {"lab": "LAB-09", "seed": SEED, "environment": environment()})
    (args.out / "report.md").write_text(
        "# LAB-09 report\n\n## Threat model\n\nLocal API only.\n\n## Limitations\n\nSynthetic data.\n",
        encoding="utf-8",
        newline="\n",
    )
    write_json(args.out / "manifest.json", build_manifest(args.out, ["metrics.json", "run.json", "report.md"]))
    print(metrics)
    print(f"wrote {args.out / 'metrics.json'}")


if __name__ == "__main__":
    main()
