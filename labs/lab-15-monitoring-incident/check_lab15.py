"""Independent checker for LAB-15.

Usage:
    python solution.py --out artifacts
    python check_lab15.py --artifacts artifacts

The checker rebuilds the detector pipeline from the prediction logs, recomputes
thresholds, window alerts, and episodes, and compares them with metrics.json.
Exit code 0 means every check passed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

WINDOW = 100
SIGMAS = 5.0
FEATURE_FLOOR = 0.05
Z_CLIP = 5.0
CONCENTRATION_THRESHOLD = 0.60
CONTENT = ("input_shift", "low_confidence", "shadow_disagreement")
VOLUME = ("client_concentration", "throughput")
SIGNALS = CONTENT + VOLUME
SCENARIOS = {
    "calibration": 12,
    "baseline": 6,
    "benign_drift": 6,
    "evasion_attack": 6,
    "query_burst": 6,
    "recovery": 3,
}
LOG_FIELDS = {
    "window", "scenario", "request_id", "ts", "client", "model_version",
    "predicted_class", "shadow_class", "confidence", "label", "features",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def close(left: float, right: float, tolerance: float, label: str) -> None:
    if not math.isfinite(left) or abs(left - right) > tolerance:
        fail(f"{label}: recomputed {left:.6f}, recorded {right:.6f}")


def read_logs(path: Path) -> list[dict]:
    if not path.exists():
        fail(f"missing {path}")
    records = []
    with open(path, encoding="utf-8") as handle:
        for number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                fail(f"log line {number} is not JSON")
            if set(record) != LOG_FIELDS:
                fail(f"log line {number} fields are {sorted(record)}")
            features = record["features"]
            if len(features) != 64 or any(not (0.0 <= float(v) <= 1.0) for v in features):
                fail(f"log line {number} features are not 64 values in [0, 1]")
            if not 0 <= int(record["label"]) <= 9:
                fail(f"log line {number} label is out of range")
            if not 0 <= int(record["predicted_class"]) <= 9:
                fail(f"log line {number} predicted_class is out of range")
            if not 0 <= int(record["shadow_class"]) <= 9:
                fail(f"log line {number} shadow_class is out of range")
            if not 0.0 < float(record["confidence"]) <= 1.0:
                fail(f"log line {number} confidence is not a probability")
            records.append(record)
    return records


def triage(alerts: dict) -> tuple[str, str]:
    content = [name for name in CONTENT if alerts.get(name)]
    volume = [name for name in VOLUME if alerts.get(name)]
    if len(content) >= 2 or (content and volume):
        return "probable evasion or model-targeted abuse", "high"
    if volume:
        return "client abuse or scraping", "medium"
    if content:
        return "distribution drift under review", "low"
    return "none", "none"


def stats_for(records: list[dict], reference: dict) -> dict:
    features = np.array([r["features"] for r in records], dtype=np.float64)
    mean = np.array(reference["mean"])
    std = np.array(reference["std"])
    z = np.clip((features.mean(axis=0) - mean) / std, -Z_CLIP, Z_CLIP)
    timestamps = np.array([r["ts"] for r in records], dtype=np.float64)
    span = max(float(timestamps.max() - timestamps.min()), 1e-6)
    clients = Counter(r["client"] for r in records)
    predicted = np.array([r["predicted_class"] for r in records])
    shadow = np.array([r["shadow_class"] for r in records])
    confidence = np.array([r["confidence"] for r in records])
    labels = np.array([r["label"] for r in records])
    return {
        "requests": len(records),
        "input_shift": float(np.sqrt(np.mean(z**2))),
        "mean_confidence": float(confidence.mean()),
        "shadow_disagreement": float((predicted != shadow).mean()),
        "client_concentration": float(clients.most_common(1)[0][1] / len(records)),
        "throughput": float(len(records) / span),
        "accuracy": float((predicted == labels).mean()),
        "start_ts": float(timestamps.min()),
        "end_ts": float(timestamps.max()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-15 artifacts.")
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    root = args.artifacts

    metrics = load_json(root / "metrics.json")
    run = load_json(root / "run.json")
    manifest = load_json(root / "manifest.json")
    report = root / "report.md"
    log_path = root / "logs" / "predictions.jsonl"
    if not report.exists():
        fail("missing report.md")

    evidence = {
        "metrics.json": root / "metrics.json",
        "run.json": root / "run.json",
        "report.md": report,
        "logs/predictions.jsonl": log_path,
    }
    listed = {entry["path"]: entry for entry in manifest.get("files", [])}
    if set(listed) != set(evidence):
        fail(f"manifest covers {sorted(listed)}, expected {sorted(evidence)}")
    for name, path in evidence.items():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if listed[name]["sha256"] != digest:
            fail(f"manifest hash for {name} does not match the file")
        if listed[name]["bytes"] != path.stat().st_size:
            fail(f"manifest size for {name} does not match the file")

    if run.get("lab") != "LAB-15":
        fail("run.json lab is not LAB-15")
    if run.get("seed") != 37 or run.get("window_size") != WINDOW:
        fail("run.json seed or window size does not match the reference")
    if abs(float(run.get("epsilon", 0.0)) - 0.10) > 1e-9:
        fail("run.json epsilon must be 0.10")

    records = read_logs(log_path)
    if len(records) != sum(SCENARIOS.values()) * WINDOW:
        fail(f"log holds {len(records)} records, expected {sum(SCENARIOS.values()) * WINDOW}")
    seen_ids = set()
    grouped: dict[tuple[str, int], list[dict]] = {}
    for record in records:
        if record["request_id"] in seen_ids:
            fail(f"duplicate request_id {record['request_id']}")
        seen_ids.add(record["request_id"])
        grouped.setdefault((record["scenario"], record["window"]), []).append(record)
    for scenario, expected in SCENARIOS.items():
        windows = sorted(window for name, window in grouped if name == scenario)
        if len(windows) != expected:
            fail(f"{scenario} has {len(windows)} windows, expected {expected}")
        for window in windows:
            if len(grouped[(scenario, window)]) != WINDOW:
                fail(f"{scenario} window {window} does not hold {WINDOW} requests")
            timestamps = [row["ts"] for row in grouped[(scenario, window)]]
            if timestamps != sorted(timestamps):
                fail(f"{scenario} window {window} timestamps are not ordered")

    calibration = [r for r in records if r["scenario"] == "calibration"]
    features = np.array([r["features"] for r in calibration], dtype=np.float64)
    reference = {
        "mean": features.mean(axis=0),
        "std": np.maximum(features.std(axis=0), FEATURE_FLOOR),
    }
    calibration_stats = [
        stats_for(calibration[i : i + WINDOW], reference)
        for i in range(0, len(calibration), WINDOW)
    ]

    def mean_std(key):
        values = [entry[key] for entry in calibration_stats]
        return float(np.mean(values)), float(np.std(values))

    shift_mean, shift_std = mean_std("input_shift")
    conf_mean, conf_std = mean_std("mean_confidence")
    dis_mean, dis_std = mean_std("shadow_disagreement")
    rate_mean, rate_std = mean_std("throughput")
    recomputed_thresholds = {
        "input_shift": max(0.01, shift_mean + SIGMAS * shift_std),
        "low_confidence": max(0.80, conf_mean - SIGMAS * conf_std),
        "shadow_disagreement": max(0.05, dis_mean + SIGMAS * dis_std),
        "client_concentration": CONCENTRATION_THRESHOLD,
        "throughput": max(5.0, rate_mean + SIGMAS * rate_std),
    }
    recorded = metrics["thresholds"]
    for name in SIGNALS:
        close(recorded[name], recomputed_thresholds[name], 0.01, f"threshold {name}")
    if metrics["calibration"]["windows"] != 12 or metrics["calibration"]["rows"] != 1200:
        fail("calibration must use 12 windows and 1200 rows")

    diagnostics = []
    for scenario, window in sorted(grouped, key=lambda key: key[1]):
        if scenario == "calibration":
            continue
        rows = grouped[(scenario, window)]
        stats = stats_for(rows, reference)
        alerts = {
            "input_shift": stats["input_shift"] > recomputed_thresholds["input_shift"],
            "low_confidence": stats["mean_confidence"] < recomputed_thresholds["low_confidence"],
            "shadow_disagreement": stats["shadow_disagreement"] > recomputed_thresholds["shadow_disagreement"],
            "client_concentration": stats["client_concentration"] > recomputed_thresholds["client_concentration"],
            "throughput": stats["throughput"] > recomputed_thresholds["throughput"],
        }
        classification, severity = triage(alerts)
        diagnostics.append(
            {
                "scenario": scenario,
                "window": window,
                "stats": stats,
                "alerts": alerts,
                "classification": classification,
                "severity": severity,
            }
        )

    recorded_windows = metrics.get("window_diagnostics", [])
    if [entry["window"] for entry in recorded_windows] != [entry["window"] for entry in diagnostics]:
        fail("window_diagnostics does not cover every monitored window in order")
    for recorded_entry, entry in zip(recorded_windows, diagnostics):
        if recorded_entry["scenario"] != entry["scenario"]:
            fail(f"window {entry['window']} scenario does not match the log")
        if recorded_entry["alerts"] != entry["alerts"]:
            fail(f"window {entry['window']} alerts do not reproduce")
        if recorded_entry["classification"] != entry["classification"]:
            fail(f"window {entry['window']} classification does not reproduce")
        if recorded_entry["severity"] != entry["severity"]:
            fail(f"window {entry['window']} severity does not reproduce")
        for key, tolerance in (
            ("input_shift", 0.01),
            ("mean_confidence", 0.005),
            ("shadow_disagreement", 0.005),
            ("client_concentration", 0.005),
            ("throughput", 0.5),
        ):
            close(recorded_entry["stats"][key], entry["stats"][key], tolerance,
                  f"window {entry['window']} {key}")

    by_scenario: dict[str, list[dict]] = {}
    for entry in diagnostics:
        by_scenario.setdefault(entry["scenario"], []).append(entry)
    for scenario, expected in (
        ("baseline", 0),
        ("benign_drift", 6),
        ("evasion_attack", 6),
        ("query_burst", 6),
        ("recovery", 0),
    ):
        active = sum(1 for entry in by_scenario.get(scenario, []) if any(entry["alerts"].values()))
        if active != expected:
            fail(f"{scenario} has {active} alerting windows, expected {expected}")
        if metrics["phases"][scenario]["alerting_windows"] != active:
            fail(f"phase summary for {scenario} does not match the windows")
    if metrics["false_positive"]["alerting_windows"] != 0:
        fail("baseline false positives must be 0 for the reference run")

    episodes = []
    current = None
    for entry in diagnostics:
        active = any(entry["alerts"].values())
        if not active:
            current = None
            continue
        if (
            current is not None
            and entry["window"] == current["windows"][-1] + 1
            and entry["classification"] == current["classification"]
        ):
            current["windows"].append(entry["window"])
            current["signals"].update(name for name in SIGNALS if entry["alerts"][name])
            current["scenarios"].add(entry["scenario"])
            continue
        current = {
            "windows": [entry["window"]],
            "signals": {name for name in SIGNALS if entry["alerts"][name]},
            "classification": entry["classification"],
            "severity": entry["severity"],
            "scenarios": {entry["scenario"]},
        }
        episodes.append(current)
    if len(episodes) != len(metrics["episodes"]):
        fail(f"recomputed {len(episodes)} episodes, recorded {len(metrics['episodes'])}")
    for index, (episode, recorded_episode) in enumerate(zip(episodes, metrics["episodes"]), start=1):
        if recorded_episode["windows"] != episode["windows"]:
            fail(f"episode {index} windows do not reproduce")
        if sorted(recorded_episode["signals"]) != sorted(episode["signals"]):
            fail(f"episode {index} signals do not reproduce")
        if recorded_episode["classification"] != episode["classification"]:
            fail(f"episode {index} classification does not reproduce")
        if recorded_episode["severity"] != episode["severity"]:
            fail(f"episode {index} severity does not reproduce")

    by_playbook = {episode["playbook"]: episode for episode in metrics["episodes"]}
    drift = by_playbook.get("drift_review")
    attack = by_playbook.get("content_incident")
    abuse = by_playbook.get("volume_abuse")
    if drift is None or drift["signals"] != ["input_shift"] or drift["severity"] != "low":
        fail("benign drift must produce one low-severity input-shift episode")
    if attack is None or attack["severity"] != "high":
        fail("the evasion phase must produce a high-severity incident")
    if len([name for name in attack["signals"] if name in CONTENT]) < 2:
        fail("the evasion incident needs at least two content signals")
    if abuse is None or abuse["severity"] != "medium":
        fail("the query burst must be triaged as medium-severity abuse")
    if set(abuse["signals"]) - set(VOLUME):
        fail("the query burst should trigger volume signals only")
    if metrics["confirmed_incidents"] != 1:
        fail("exactly one confirmed content incident is expected")

    rollback = metrics["rollback"]
    if rollback["restored"] is not False:
        fail("rollback must not be recorded as restored")
    if "rejected" not in rollback["decision"]:
        fail("the rollback decision must state that it was rejected")
    if rollback["base_size"] != 288:
        fail("rollback base set must be 288 rows")
    for key in ("attack_success_current", "attack_success_previous"):
        if not 0.0 <= rollback[key] <= 1.0:
            fail(f"{key} is not a success rate")
    if rollback["attack_success_previous"] < 0.20:
        fail("the previous checkpoint should share the same weakness")
    if rollback["attack_success_current"] - rollback["attack_success_previous"] > 0.15:
        fail("the checkpoint gap is too large for the reference story")

    mitigation = metrics["mitigation"]
    if not mitigation["attack_success_after"] < mitigation["attack_success_before"]:
        fail("input squeezing did not reduce attack success")
    if mitigation["clean_accuracy_after"] < 0.90:
        fail("squeezing cost too much clean accuracy for this lab")
    recovery = metrics["recovery"]
    if recovery["alerting_windows"] != 0 or recovery["within_band"] is not True:
        fail("recovery windows must return to the calibrated band")
    if recovery["mean_confidence"] < recorded["low_confidence"]:
        fail("recovery confidence is below the calibrated threshold")

    text = report.read_text(encoding="utf-8").lower()
    for phrase in (
        "monitoring", "drift", "incident", "false positive",
        "rollback", "residual", "limitations",
    ):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print("PASS manifest hashes and sizes cover metrics, run, report, and prediction logs")
    print("PASS 3900 logged requests across calibration, baseline, drift, evasion, burst, recovery")
    print("PASS thresholds, window statistics, alerts, and triage reproduce from the logs")
    print("PASS baseline has 0 false-positive windows and recovery returns to the band")
    print("PASS drift is low severity, evasion is a high incident, burst is medium abuse")
    print("PASS rollback rejected, squeezing measured, residual risk recorded")
    print("PASS report covers monitoring, drift, incidents, false positives, rollback, limitations")
    print("LAB-15 CHECK PASSED")


if __name__ == "__main__":
    main()
