"""LAB-16 reference solution: federated learning attack and defense simulation.

Run from this directory:
    python solution.py --out artifacts

The simulation is deliberately small: eight non-IID digit clients, a NumPy
softmax model, twelve federated rounds, and three aggregation rules. It is a
model of FedAvg, not a federated framework. Nothing touches a network.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

SEED = 42
N_CLIENTS = 8
ROUNDS = 12
LOCAL_EPOCHS = 8
LEARNING_RATE = 0.5
L2 = 1e-3
ATTACK_SCALE = 6.0
CLIP_NORM = 2.0
TRIM = 1
TARGET = 0
TRIGGER_PIXELS = ((0, 0), (0, 1), (1, 0), (1, 1))
MALICIOUS_CLIENT = 0


def load_data():
    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=SEED, stratify=y
    )
    return X_train, X_test, y_train, y_test


def partition_clients(y_train, n_clients=N_CLIENTS):
    """Split each class across two clients so every client sees few classes."""
    rng = np.random.default_rng(SEED)
    shards: list[list[int]] = [[] for _ in range(n_clients)]
    for label in range(10):
        indices = np.flatnonzero(y_train == label)
        rng.shuffle(indices)
        cut = int(round(0.7 * len(indices)))
        shards[label % n_clients].extend(indices[:cut])
        shards[(label + 3) % n_clients].extend(indices[cut:])
    return [np.sort(np.asarray(shard, dtype=int)) for shard in shards]


def softmax(scores):
    scores = scores - scores.max(axis=1, keepdims=True)
    exp = np.exp(scores)
    return exp / exp.sum(axis=1, keepdims=True)


def train_local(X, y, initial):
    """Full-batch softmax regression starting from the current global model."""
    weights, bias = initial
    weights = weights.copy()
    bias = bias.copy()
    one_hot = np.eye(10)[y]
    for _ in range(LOCAL_EPOCHS):
        probabilities = softmax(X @ weights + bias)
        error = (probabilities - one_hot) / len(y)
        weights -= LEARNING_RATE * (X.T @ error + L2 * weights)
        bias -= LEARNING_RATE * error.sum(axis=0)
    return weights, bias


def aggregate_mean(updates, sizes):
    total = float(sum(sizes))
    weights = sum(w * (n / total) for (w, _), n in zip(updates, sizes))
    bias = sum(b * (n / total) for (_, b), n in zip(updates, sizes))
    return weights, bias


def flatten(params):
    weights, bias = params
    return np.concatenate([weights.ravel(), bias.ravel()])


def unflatten(vector, n_features=64):
    weights = vector[: n_features * 10].reshape(n_features, 10)
    bias = vector[n_features * 10 :]
    return weights, bias


def aggregate_trimmed_mean(updates, trim=TRIM):
    stacked = np.stack([flatten(item) for item in updates])
    ordered = np.sort(stacked, axis=0)
    trimmed = ordered[trim : len(updates) - trim].mean(axis=0)
    return unflatten(trimmed)


def aggregate_clipped_mean(updates, global_params, max_norm=CLIP_NORM):
    base = flatten(global_params)
    clipped = []
    for item in updates:
        vector = flatten(item)
        delta = vector - base
        norm = float(np.linalg.norm(delta))
        scale = min(1.0, max_norm / (norm + 1e-12))
        clipped.append(unflatten(base + delta * scale))
    return aggregate_mean(clipped, [1.0] * len(clipped))


def apply_trigger(X):
    triggered = X.copy()
    for row, column in TRIGGER_PIXELS:
        triggered[:, row * 8 + column] = 1.0
    return triggered


def federated_train(X_train, y_train, shards, rule, malicious=False):
    weights = np.zeros((X_train.shape[1], 10))
    bias = np.zeros(10)
    history = []
    for round_index in range(ROUNDS):
        updates = []
        sizes = []
        for client_id, shard in enumerate(shards):
            X_local = X_train[shard]
            y_local = y_train[shard]
            if malicious and client_id == MALICIOUS_CLIENT:
                X_poison = apply_trigger(X_local)
                X_local = np.vstack([X_local, X_poison])
                y_local = np.concatenate(
                    [y_local, np.full(len(X_poison), TARGET, dtype=y_local.dtype)]
                )
            local_weights, local_bias = train_local(X_local, y_local, (weights, bias))
            if malicious and client_id == MALICIOUS_CLIENT:
                local_weights = weights + ATTACK_SCALE * (local_weights - weights)
                local_bias = bias + ATTACK_SCALE * (local_bias - bias)
            updates.append((local_weights, local_bias))
            sizes.append(len(X_local))

        if rule == "mean":
            weights, bias = aggregate_mean(updates, sizes)
        elif rule == "trimmed_mean":
            weights, bias = aggregate_trimmed_mean(updates)
        elif rule == "clipped_mean":
            weights, bias = aggregate_clipped_mean(updates, (weights, bias))
        else:
            raise ValueError(f"unknown aggregation rule: {rule}")

        history.append(
            {
                "round": round_index + 1,
                "weights_l2": float(np.linalg.norm(weights)),
                "bias_l2": float(np.linalg.norm(bias)),
            }
        )
    return weights, bias, history


def evaluate(params, X_test, y_test):
    weights, bias = params
    predictions = np.argmax(X_test @ weights + bias, axis=1)
    clean_accuracy = float((predictions == y_test).mean())
    attack_rows = y_test != TARGET
    triggered = apply_trigger(X_test[attack_rows])
    attack_predictions = np.argmax(triggered @ weights + bias, axis=1)
    attack_success_rate = float((attack_predictions == TARGET).mean())
    return clean_accuracy, attack_success_rate, int(attack_rows.sum())


def summarize(name, params, X_test, y_test):
    clean, asr, attack_rows = evaluate(params, X_test, y_test)
    return {
        "clean_accuracy": round(clean, 4),
        "attack_success_rate": round(asr, 4),
        "attack_rows": attack_rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the LAB-16 federated simulation.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()

    X_train, X_test, y_train, y_test = load_data()
    shards = partition_clients(y_train)
    class_counts = [
        {int(label): int((y_train[shard] == label).sum()) for label in sorted(set(y_train[shard]))}
        for shard in shards
    ]

    benign_params, benign_bias, benign_history = federated_train(
        X_train, y_train, shards, rule="mean", malicious=False
    )
    malicious_params, malicious_bias, malicious_history = federated_train(
        X_train, y_train, shards, rule="mean", malicious=True
    )
    trimmed_params, trimmed_bias, trimmed_history = federated_train(
        X_train, y_train, shards, rule="trimmed_mean", malicious=True
    )
    clipped_params, clipped_bias, clipped_history = federated_train(
        X_train, y_train, shards, rule="clipped_mean", malicious=True
    )

    runs = {
        "benign_mean": summarize("benign_mean", (benign_params, benign_bias), X_test, y_test),
        "malicious_mean": summarize("malicious_mean", (malicious_params, malicious_bias), X_test, y_test),
        "trimmed_mean": summarize("trimmed_mean", (trimmed_params, trimmed_bias), X_test, y_test),
        "clipped_mean": summarize("clipped_mean", (clipped_params, clipped_bias), X_test, y_test),
    }
    runs["benign_mean"]["history"] = benign_history
    runs["malicious_mean"]["history"] = malicious_history
    runs["trimmed_mean"]["history"] = trimmed_history
    runs["clipped_mean"]["history"] = clipped_history

    metrics = {
        "config": {
            "clients": N_CLIENTS,
            "rounds": ROUNDS,
            "local_epochs": LOCAL_EPOCHS,
            "attack_scale": ATTACK_SCALE,
            "clip_norm": CLIP_NORM,
            "trim": TRIM,
            "malicious_client": MALICIOUS_CLIENT,
            "target_label": TARGET,
        },
        "partition": {"sizes": [len(s) for s in shards], "class_counts": class_counts},
        "runs": runs,
        "note": (
            "Seed 42, eight non-IID clients, equal rounds. The malicious client trains on "
            "triggered copies of its own data and scales its update. Trimmed mean and norm "
            "clipping reduce but do not eliminate the backdoor; both are evaluated on one "
            "trigger, one target, and one partition."
        ),
    }

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "metrics.json", metrics)
    write_json(
        out / "run.json",
        {
            "lab": "LAB-16",
            "seed": SEED,
            "rounds": ROUNDS,
            "clients": N_CLIENTS,
            "malicious_client": MALICIOUS_CLIENT,
            "attack_scale": ATTACK_SCALE,
            "clip_norm": CLIP_NORM,
            "trigger_pixels": [list(pixel) for pixel in TRIGGER_PIXELS],
            "target_label": TARGET,
            "environment": environment(),
        },
    )

    report = f"""# LAB-16 report

## Setup

Eight clients receive a deterministic non-IID partition of the digits training
split. Each client trains the same NumPy softmax model for {LOCAL_EPOCHS} local
epochs, and the server averages updates for {ROUNDS} rounds. The test set is
held by the server's evaluator.

The malicious client is client {MALICIOUS_CLIENT}. It appends triggered copies of
its own training rows, relabels them to class {TARGET}, and scales its update by
{ATTACK_SCALE:.1f}. The trigger sets four corner pixels to 1.0. Attack success is
the fraction of triggered test rows whose true label is not {TARGET} that are
classified as {TARGET}.

## Results at equal rounds

| Run | Clean accuracy | Attack success rate |
|---|---:|---:|
| Benign, mean aggregation | {runs['benign_mean']['clean_accuracy']:.4f} | {runs['benign_mean']['attack_success_rate']:.4f} |
| Malicious, mean aggregation | {runs['malicious_mean']['clean_accuracy']:.4f} | {runs['malicious_mean']['attack_success_rate']:.4f} |
| Malicious, trimmed mean | {runs['trimmed_mean']['clean_accuracy']:.4f} | {runs['trimmed_mean']['attack_success_rate']:.4f} |
| Malicious, norm clipping | {runs['clipped_mean']['clean_accuracy']:.4f} | {runs['clipped_mean']['attack_success_rate']:.4f} |

All four runs use the same partition, client order, number of rounds, local
epochs, and target. The comparison is therefore about the aggregation rule, not
about a longer training budget.

## Interpretation

Mean aggregation lets one scaled update move the global model enough to install
the trigger while leaving clean accuracy broadly intact. Trimmed mean removes the
largest and smallest update in each coordinate, and norm clipping limits how far
any client can move the global model in one round. Both reduce the observed attack
success rate in this simulation; neither makes the model trustworthy.

The residual risk is substantial. A Sybil attacker can control several client
identities and defeat trimmed mean by supplying a majority of crafted updates.
Clipping bounds one round but not a patient attacker who spreads the backdoor over
many rounds. The server still sees every update unless secure aggregation is used,
and secure aggregation would hide update contents from the server without
preventing a poisoned aggregate.

## Limitations

This is one trigger, one target class, one non-IID partition, one model family,
and one attack scale. The clients are simulated in one process, so network
failures, stragglers, and client sampling are absent. The numerical result does
not establish that either defense works universally, and no formal guarantee is
claimed. A production decision would need multiple partitions, multiple triggers,
adaptive attackers, and a stated threat model for the coordinator.
"""
    (out / "report.md").write_text(report, encoding="utf-8", newline="\n")

    manifest = build_manifest(out, ["metrics.json", "run.json", "report.md"])
    write_json(out / "manifest.json", manifest)

    for name, result in runs.items():
        print(
            f"{name}: clean={result['clean_accuracy']:.4f} "
            f"asr={result['attack_success_rate']:.4f}"
        )
    print(f"artifacts written to {out.resolve()}")


if __name__ == "__main__":
    main()
