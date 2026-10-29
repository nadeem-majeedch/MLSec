"""Independent checker for LAB-16.

Usage:
    python solution.py --out artifacts
    python check_lab16.py --artifacts artifacts

Exit code 0 means every check passed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

SEED = 42
N_CLIENTS = 8


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


def rebuild_partition() -> list[np.ndarray]:
    X, y = load_digits(return_X_y=True)
    _, _, y_train, _ = train_test_split(
        X.astype(np.float64) / 16.0, y, test_size=0.3, random_state=SEED, stratify=y
    )
    rng = np.random.default_rng(SEED)
    shards: list[list[int]] = [[] for _ in range(N_CLIENTS)]
    for label in range(10):
        indices = np.flatnonzero(y_train == label)
        rng.shuffle(indices)
        cut = int(round(0.7 * len(indices)))
        shards[label % N_CLIENTS].extend(indices[:cut])
        shards[(label + 3) % N_CLIENTS].extend(indices[cut:])
    return [np.sort(np.asarray(shard, dtype=int)) for shard in shards]


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-16 artifacts.")
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
    if run.get("lab") != "LAB-16":
        fail("run.json lab is not LAB-16")
    if int(run.get("clients", 0)) != N_CLIENTS:
        fail("run.json must record eight clients")
    if int(run.get("rounds", 0)) != 12:
        fail("run.json must record twelve rounds")
    if not float(run.get("attack_scale", 0)) > 1.0:
        fail("attack_scale must exceed 1.0")
    if not float(run.get("clip_norm", 0)) > 0.0:
        fail("clip_norm must be positive")
    if int(run.get("malicious_client", -1)) != 0:
        fail("malicious_client must be 0")

    shards = rebuild_partition()
    if len(shards) != N_CLIENTS:
        fail("checker partition rebuild failed")
    if sum(len(shard) for shard in shards) != 1257:
        fail("partition does not cover the 1,257 training rows")
    class_counts = metrics.get("partition", {}).get("class_counts", [])
    if len(class_counts) != N_CLIENTS:
        fail("partition class_counts must describe all eight clients")
    for client_id, counts in enumerate(class_counts):
        if len(counts) > 4:
            fail(f"client {client_id} sees {len(counts)} classes; the partition is not non-IID")
        total = sum(counts.values())
        if total != len(shards[client_id]):
            fail(f"client {client_id} class counts do not match the rebuilt shard")

    runs = metrics.get("runs", {})
    for name in ("benign_mean", "malicious_mean", "trimmed_mean", "clipped_mean"):
        if name not in runs:
            fail(f"missing run {name}")
        for key in ("clean_accuracy", "attack_success_rate"):
            value = float(runs[name][key])
            if not 0.0 <= value <= 1.0:
                fail(f"{name}.{key} outside [0, 1]")
        if len(runs[name].get("history", [])) != 12:
            fail(f"{name} must record twelve round histories")

    benign = runs["benign_mean"]
    malicious = runs["malicious_mean"]
    trimmed = runs["trimmed_mean"]
    clipped = runs["clipped_mean"]

    if float(benign["clean_accuracy"]) < 0.85:
        fail("benign clean accuracy must exceed 0.85")
    if float(benign["attack_success_rate"]) > 0.10:
        fail("benign attack success must stay low (<= 0.10)")
    if float(malicious["clean_accuracy"]) < 0.60:
        fail("malicious mean clean accuracy must remain above 0.60")
    if float(malicious["attack_success_rate"]) < 0.90:
        fail("the malicious mean run must install the backdoor (ASR >= 0.90)")
    if float(trimmed["attack_success_rate"]) > 0.10:
        fail("trimmed mean must reduce ASR to <= 0.10 in this reference setup")
    if float(trimmed["clean_accuracy"]) < 0.80:
        fail("trimmed mean must retain clean accuracy >= 0.80")
    if not 0.30 <= float(clipped["attack_success_rate"]) <= 0.90:
        fail("norm clipping must leave partial attack success (0.30-0.90) in this setup")
    if float(clipped["clean_accuracy"]) < 0.85:
        fail("norm clipping must retain clean accuracy >= 0.85")
    if not float(trimmed["attack_success_rate"]) < float(malicious["attack_success_rate"]):
        fail("trimmed mean must lower ASR relative to mean aggregation")
    if not float(clipped["attack_success_rate"]) < float(malicious["attack_success_rate"]):
        fail("norm clipping must lower ASR relative to mean aggregation")

    text = report.read_text(encoding="utf-8").lower()
    for phrase in ("equal rounds", "residual risk", "limitations", "sybil", "secure aggregation"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print(f"PASS benign mean: clean={benign['clean_accuracy']:.4f} asr={benign['attack_success_rate']:.4f}")
    print(f"PASS malicious mean: clean={malicious['clean_accuracy']:.4f} asr={malicious['attack_success_rate']:.4f}")
    print(f"PASS trimmed mean: clean={trimmed['clean_accuracy']:.4f} asr={trimmed['attack_success_rate']:.4f}")
    print(f"PASS norm clipping: clean={clipped['clean_accuracy']:.4f} asr={clipped['attack_success_rate']:.4f}")
    print("PASS partition is non-IID and covers 1,257 training rows")
    print("PASS report discusses equal rounds, residual risk, Sybil clients, and secure aggregation")
    print("LAB-16 CHECK PASSED")


if __name__ == "__main__":
    main()
