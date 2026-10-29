"""LAB-15 starter: monitoring and incident response for a prediction service.

Fill in the three TODO blocks, then run:
    python starter.py --out artifacts

Artifacts: metrics.json, run.json, report.md, logs/predictions.jsonl, manifest.json.

All traffic is synthetic and drawn from sklearn's bundled digits dataset. The
service, clients, and incidents are simulated in memory; nothing here contacts
a real system. Logged features are stored for reproducibility only; see the
report's limitations for why a deployed system should not keep raw inputs.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

SEED = 37
WINDOW = 100
EPSILON = 0.10
SQUEEZE_LEVELS = 4
DEPLOYED_VERSION = "digits-logreg-v2"
PREVIOUS_VERSION = "digits-logreg-v1"
CONTENT_SIGNALS = ("input_shift", "low_confidence", "shadow_disagreement")
VOLUME_SIGNALS = ("client_concentration", "throughput")
SIGNALS = CONTENT_SIGNALS + VOLUME_SIGNALS
CLIENTS = ("c-101", "c-102", "c-103", "c-104")
ABUSE_CLIENT = "c-900"
THRESHOLD_SIGMAS = 5.0
CONCENTRATION_THRESHOLD = 0.60
FEATURE_FLOOR = 0.05
Z_CLIP = 5.0


def load_split():
    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    return train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)


def train_models(X_train, y_train):
    deployed = LogisticRegression(max_iter=5000, C=1.0).fit(X_train, y_train)
    previous = LogisticRegression(max_iter=5000, C=0.5).fit(X_train, y_train)
    rng = np.random.default_rng(7)
    subset = rng.choice(len(X_train), size=int(0.6 * len(X_train)), replace=False)
    shadow = LogisticRegression(max_iter=5000, C=0.5, random_state=7).fit(
        X_train[subset], y_train[subset]
    )
    return deployed, previous, shadow


def probabilities(model, X):
    scores = X @ model.coef_.T + model.intercept_
    scores -= scores.max(axis=1, keepdims=True)
    exp = np.exp(scores)
    return exp / exp.sum(axis=1, keepdims=True)


def fgsm(model, X, y, epsilon=EPSILON):
    p = probabilities(model, X)
    p[np.arange(len(y)), y] -= 1.0
    gradient = p @ model.coef_
    return np.clip(X + epsilon * np.sign(gradient), 0.0, 1.0)


def squeeze(X, levels=SQUEEZE_LEVELS):
    """Edge preprocessing: snap pixels to a coarse grid. Mitigates naive evasion."""
    return np.clip(np.round(X * (levels - 1)) / (levels - 1), 0.0, 1.0)


def scanner_drift(X, gain, offset, noise, rng):
    """Simulate a scanner recalibration: darker, noisier images, same classes."""
    return np.clip(gain * X + offset + rng.normal(0.0, noise, X.shape), 0.0, 1.0)


def emit_window(
    scenario,
    window_index,
    rows,
    clients,
    model,
    shadow,
    clock,
    step,
    jitter,
    rng,
    squeeze_applied=False,
):
    """Turn one batch of inputs into request records and advance the clock."""
    X, y = rows
    served = squeeze(X) if squeeze_applied else X
    p = probabilities(model, served)
    predicted = p.argmax(axis=1)
    confidence = p.max(axis=1)
    shadow_pred = shadow.predict(served)
    records = []
    for row in range(len(X)):
        clock += step + rng.uniform(0.0, jitter)
        records.append(
            {
                "window": window_index,
                "scenario": scenario,
                "request_id": f"r-{scenario[:3]}-{window_index:02d}-{row:03d}",
                "ts": round(float(clock), 3),
                "client": clients[row % len(clients)],
                "model_version": DEPLOYED_VERSION + ("+squeeze" if squeeze_applied else ""),
                "predicted_class": int(predicted[row]),
                "shadow_class": int(shadow_pred[row]),
                "confidence": round(float(confidence[row]), 4),
                "label": int(y[row]),
                "features": [round(float(value), 4) for value in X[row]],
            }
        )
    return records, clock


def build_traffic(model, shadow, X_test, y_test):
    """Generate calibration and monitored traffic with deterministic phases."""
    rng = np.random.default_rng(SEED)
    drift_rng = np.random.default_rng(SEED + 1)
    clock = 0.0
    records: list[dict] = []
    window_index = 0

    def rows(count=WINDOW):
        idx = rng.integers(0, len(X_test), size=count)
        return X_test[idx], y_test[idx]

    # Calibration: quiet period used to derive thresholds. Not monitored.
    for _ in range(12):
        batch, clock = emit_window(
            "calibration", window_index, rows(), CLIENTS, model, shadow,
            clock, 0.5, 0.2, rng,
        )
        records.extend(batch)
        window_index += 1

    # Baseline: normal production traffic.
    for _ in range(6):
        batch, clock = emit_window(
            "baseline", window_index, rows(), CLIENTS, model, shadow,
            clock, 0.5, 0.2, rng,
        )
        records.extend(batch)
        window_index += 1

    # Benign drift: a scanner recalibration nobody announced.
    for _ in range(6):
        X, y = rows()
        shifted = scanner_drift(X, 0.88, 0.02, 0.015, drift_rng)
        batch, clock = emit_window(
            "benign_drift", window_index, (shifted, y), CLIENTS, model, shadow,
            clock, 0.5, 0.2, rng,
        )
        records.extend(batch)
        window_index += 1

    # Evasion attack: white-box FGSM against the deployed model.
    for _ in range(6):
        X, y = rows()
        batch, clock = emit_window(
            "evasion_attack", window_index, (fgsm(model, X, y), y), CLIENTS, model, shadow,
            clock, 0.5, 0.2, rng,
        )
        records.extend(batch)
        window_index += 1

    # Query burst: one client scrapes the API at machine speed.
    for _ in range(6):
        batch, clock = emit_window(
            "query_burst", window_index, rows(), (ABUSE_CLIENT,), model, shadow,
            clock, 0.05, 0.01, rng,
        )
        records.extend(batch)
        window_index += 1

    # Recovery: clean traffic after containment. Edge squeezing was removed,
    # and the deployed model is unchanged.
    for _ in range(3):
        batch, clock = emit_window(
            "recovery", window_index, rows(), CLIENTS, model, shadow,
            clock, 0.5, 0.2, rng,
        )
        records.extend(batch)
        window_index += 1

    return records


def reference_distribution(records):
    """Per-feature mean and floored standard deviation from calibration rows."""
    features = np.array([r["features"] for r in records if r["scenario"] == "calibration"])
    mean = features.mean(axis=0)
    std = np.maximum(features.std(axis=0), FEATURE_FLOOR)
    return {"mean": mean.tolist(), "std": std.tolist(), "rows": int(len(features))}


def window_statistics(records, reference):
    """Compute the five detector inputs for one window of request records.

    TODO 1: return a dict with these keys.

    - input_shift: standardize the window's per-feature mean against
      reference["mean"] and reference["std"], clip each z-score to [-5, 5],
      then take the root mean square. This is one number summarising how far
      the batch has moved from calibration.
    - mean_confidence: mean of record["confidence"].
    - shadow_disagreement: fraction of rows where predicted_class differs
      from shadow_class.
    - client_concentration: largest client count divided by the number of rows.
    - throughput: rows divided by (max ts - min ts), with the span floored at
      1e-6 to avoid division by zero.
    - accuracy, start_ts, end_ts: evaluation helpers, not detectors.

    Use numpy. A full window always has records, so no empty-window handling
    is required.
    """
    raise NotImplementedError("TODO 1: implement window_statistics")


def calibrate(records, reference):
    """Derive detector thresholds from calibration windows only."""
    calibration = [r for r in records if r["scenario"] == "calibration"]
    windows = [calibration[i : i + WINDOW] for i in range(0, len(calibration), WINDOW)]
    stats = [window_statistics(window, reference) for window in windows]
    thresholds = {
        "input_shift": max(0.01, float(np.mean([s["input_shift"] for s in stats]))
                           + THRESHOLD_SIGMAS * float(np.std([s["input_shift"] for s in stats]))),
        "low_confidence": max(0.80, float(np.mean([s["mean_confidence"] for s in stats]))
                              - THRESHOLD_SIGMAS * float(np.std([s["mean_confidence"] for s in stats]))),
        "shadow_disagreement": max(0.05, float(np.mean([s["shadow_disagreement"] for s in stats]))
                                   + THRESHOLD_SIGMAS * float(np.std([s["shadow_disagreement"] for s in stats]))),
        "client_concentration": CONCENTRATION_THRESHOLD,
        "throughput": max(5.0, float(np.mean([s["throughput"] for s in stats]))
                          + THRESHOLD_SIGMAS * float(np.std([s["throughput"] for s in stats]))),
    }
    summary = {
        "windows": len(windows),
        "rows": int(len(calibration)),
        "input_shift": {"mean": float(np.mean([s["input_shift"] for s in stats])),
                        "std": float(np.std([s["input_shift"] for s in stats]))},
        "mean_confidence": {"mean": float(np.mean([s["mean_confidence"] for s in stats])),
                            "std": float(np.std([s["mean_confidence"] for s in stats]))},
        "shadow_disagreement": {"mean": float(np.mean([s["shadow_disagreement"] for s in stats])),
                                "std": float(np.std([s["shadow_disagreement"] for s in stats]))},
        "throughput": {"mean": float(np.mean([s["throughput"] for s in stats])),
                       "std": float(np.std([s["throughput"] for s in stats]))},
    }
    return thresholds, summary


def detect(stats, thresholds):
    """Compare one window's statistics against the calibrated thresholds.

    TODO 2: return a dict of five booleans keyed by the signal names.
    input_shift, shadow_disagreement, client_concentration, and throughput
    alert when the statistic is strictly greater than its threshold;
    low_confidence alerts when mean_confidence is strictly less than its
    threshold.
    """
    raise NotImplementedError("TODO 2: implement detect")


def triage(alerts):
    """Map active signals to a classification, severity, and playbook entry.

    TODO 3: return {"classification", "severity", "playbook"} using:
    - two or more content signals (input_shift, low_confidence,
      shadow_disagreement), or content plus volume signals:
      "probable evasion or model-targeted abuse", "high", "content_incident";
    - volume signals only (client_concentration, throughput):
      "client abuse or scraping", "medium", "volume_abuse";
    - exactly one content signal: "distribution drift under review",
      "low", "drift_review";
    - no signals: "none", "none", "none".
    """
    raise NotImplementedError("TODO 3: implement triage")


def window_diagnostics(records, reference, thresholds):
    """Window-level statistics, alerts, and triage for all monitored scenarios."""
    grouped: dict[tuple[str, int], list[dict]] = {}
    for record in records:
        if record["scenario"] == "calibration":
            continue
        grouped.setdefault((record["scenario"], record["window"]), []).append(record)
    diagnostics = []
    for (scenario, window), rows in sorted(grouped.items(), key=lambda item: item[0][1]):
        stats = window_statistics(rows, reference)
        alerts = detect(stats, thresholds)
        decision = triage(alerts)
        diagnostics.append(
            {
                "scenario": scenario,
                "window": int(window),
                "stats": stats,
                "alerts": alerts,
                "classification": decision["classification"],
                "severity": decision["severity"],
                "playbook": decision["playbook"],
            }
        )
    return diagnostics


def build_episodes(diagnostics):
    """Group consecutive alerting windows with the same triage into episodes."""
    episodes = []
    current = None
    for entry in diagnostics:
        active = any(entry["alerts"].values())
        if not active:
            current = None
            continue
        if (
            current is not None
            and entry["window"] == current["end_window"] + 1
            and entry["classification"] == current["classification"]
        ):
            current["end_window"] = entry["window"]
            current["windows"].append(entry["window"])
            for name in SIGNALS:
                if entry["alerts"][name]:
                    current["signals"].add(name)
            current["scenarios"].add(entry["scenario"])
            continue
        current = {
            "start_window": entry["window"],
            "end_window": entry["window"],
            "windows": [entry["window"]],
            "signals": {name for name in SIGNALS if entry["alerts"][name]},
            "classification": entry["classification"],
            "severity": entry["severity"],
            "playbook": entry["playbook"],
            "scenarios": {entry["scenario"]},
        }
        episodes.append(current)
    result = []
    for index, episode in enumerate(episodes, start=1):
        result.append(
            {
                "episode_id": f"EP-{index:02d}",
                "start_window": episode["start_window"],
                "end_window": episode["end_window"],
                "windows": episode["windows"],
                "signals": sorted(episode["signals"]),
                "classification": episode["classification"],
                "severity": episode["severity"],
                "playbook": episode["playbook"],
                "scenarios": sorted(episode["scenarios"]),
            }
        )
    return result


def phase_summary(diagnostics):
    phases = {}
    for entry in diagnostics:
        scenario = entry["scenario"]
        block = phases.setdefault(
            scenario,
            {
                "windows": 0,
                "alerting_windows": 0,
                "signals": {name: 0 for name in SIGNALS},
                "confidence": [],
                "accuracy": [],
                "input_shift": [],
            },
        )
        block["windows"] += 1
        block["alerting_windows"] += int(any(entry["alerts"].values()))
        for name in SIGNALS:
            block["signals"][name] += int(entry["alerts"][name])
        block["confidence"].append(entry["stats"]["mean_confidence"])
        block["accuracy"].append(entry["stats"]["accuracy"])
        block["input_shift"].append(entry["stats"]["input_shift"])
    summary = {}
    for scenario, block in phases.items():
        summary[scenario] = {
            "windows": block["windows"],
            "alerting_windows": block["alerting_windows"],
            "signal_counts": block["signals"],
            "mean_confidence": float(np.mean(block["confidence"])),
            "accuracy": float(np.mean(block["accuracy"])),
            "max_input_shift": float(np.max(block["input_shift"])),
        }
    return summary


def attack_measurements(deployed, previous, X_test, y_test):
    """Replay one captured attack batch through the current and previous models."""
    rng = np.random.default_rng(SEED + 11)
    idx = rng.integers(0, len(X_test), size=300)
    X, y = X_test[idx], y_test[idx]
    adversarial = fgsm(deployed, X, y)
    clean_correct = deployed.predict(X) == y
    base = int(clean_correct.sum())
    current_success = float((deployed.predict(adversarial)[clean_correct] != y[clean_correct]).mean())
    previous_success = float((previous.predict(adversarial)[clean_correct] != y[clean_correct]).mean())
    squeeze_pred = deployed.predict(squeeze(adversarial))
    squeezed_success = float((squeeze_pred[clean_correct] != y[clean_correct]).mean())
    clean_accuracy = float(clean_correct.mean())
    squeezed_clean_accuracy = float((deployed.predict(squeeze(X)) == y).mean())
    return {
        "batch_size": int(len(y)),
        "base_size": base,
        "epsilon": EPSILON,
        "attack_success_current": current_success,
        "attack_success_previous": previous_success,
        "rollback_restored": bool(previous_success < 0.5 * current_success),
        "clean_accuracy_current": clean_accuracy,
        "squeezed_attack_success": squeezed_success,
        "squeezed_clean_accuracy": squeezed_clean_accuracy,
    }


def build_metrics(diagnostics, thresholds, calibration, reference, measurements):
    phases = phase_summary(diagnostics)
    episodes = build_episodes(diagnostics)
    high = [episode for episode in episodes if episode["severity"] == "high"]
    baseline = phases["baseline"]
    recovery = phases["recovery"]
    return {
        "lab": "LAB-15",
        "dataset": "sklearn.datasets.load_digits (8x8, pixels/16)",
        "window_size": WINDOW,
        "epsilon": EPSILON,
        "squeeze_levels": SQUEEZE_LEVELS,
        "deployed_model": DEPLOYED_VERSION,
        "reference_rows": reference["rows"],
        "threshold_policy": {
            "sigmas": THRESHOLD_SIGMAS,
            "confidence_floor": 0.80,
            "disagreement_floor": 0.05,
            "throughput_floor": 5.0,
            "concentration_threshold": CONCENTRATION_THRESHOLD,
        },
        "calibration": calibration,
        "thresholds": thresholds,
        "phases": phases,
        "window_diagnostics": diagnostics,
        "false_positive": {
            "scenario": "baseline",
            "windows": baseline["windows"],
            "alerting_windows": baseline["alerting_windows"],
            "rate": float(baseline["alerting_windows"] / baseline["windows"]),
        },
        "episodes": episodes,
        "confirmed_incidents": len(high),
        "rollback": {
            "previous_checkpoint": PREVIOUS_VERSION,
            "base_size": measurements["base_size"],
            "attack_success_current": measurements["attack_success_current"],
            "attack_success_previous": measurements["attack_success_previous"],
            "restored": measurements["rollback_restored"],
            "decision": "rollback rejected: the previous checkpoint shares the same weakness",
            "evaluated_on": "captured FGSM batch replayed from the same traffic distribution",
        },
        "mitigation": {
            "control": "4-level edge input squeezing",
            "attack_success_before": measurements["attack_success_current"],
            "attack_success_after": measurements["squeezed_attack_success"],
            "clean_accuracy_before": measurements["clean_accuracy_current"],
            "clean_accuracy_after": measurements["squeezed_clean_accuracy"],
            "residual_risk": "adaptive attacks can approximate the quantizer and bypass it",
        },
        "recovery": {
            "scenario": "recovery",
            "windows": recovery["windows"],
            "alerting_windows": recovery["alerting_windows"],
            "mean_confidence": recovery["mean_confidence"],
            "confidence_threshold": thresholds["low_confidence"],
            "within_band": bool(recovery["alerting_windows"] == 0),
            "note": "edge squeezing was removed after the attack window because of its clean-accuracy cost",
        },
        "deployment": {
            "deployed": DEPLOYED_VERSION,
            "previous": PREVIOUS_VERSION,
            "shadow": "digits-logreg-shadow",
        },
        "limitations": [
            "synthetic traffic from one bundled dataset and one linear model",
            "thresholds come from 12 calibration windows and are optimistic",
            "labels arrive immediately here; production label feedback is delayed",
            "detectors were not tuned against an adaptive attacker",
            "raw features are logged for reproducibility; production logs should aggregate or redact them",
            "detection is not prevention and a passing monitor is not proof of security",
        ],
    }


def playbooks():
    return {
        "content_incident": [
            "Confirm: require two or more content signals across consecutive windows.",
            "Contain: enable edge input squeezing for digit traffic and raise authentication for suspect clients.",
            "Verify: replay captured rows through the previous checkpoint; roll back only if it restores accuracy.",
            "Eradicate: fix the underlying model weakness or schedule retraining; squeezing is temporary.",
            "Recover: remove temporary controls, then verify clean windows stay inside the confidence band.",
            "Learn: add a robustness evaluation to the release gate and review threshold calibration.",
        ],
        "volume_abuse": [
            "Contain: apply per-client rate limits and revoke the abusive token if policy allows.",
            "Verify: confirm normal clients are unaffected and that request volume returns to baseline.",
            "Document: update issuance rules and keep the client on a watch list.",
        ],
        "drift_review": [
            "Confirm: check change tickets and upstream data sources before opening an incident.",
            "Monitor: recalibrate thresholds only after the change is understood.",
            "Document: record the distribution change and its effect on confidence.",
        ],
    }


def build_incident_response(metrics):
    episodes = metrics["episodes"]
    high = next((episode for episode in episodes if episode["severity"] == "high"), None)
    abuse = next(
        (episode for episode in episodes if episode["playbook"] == "volume_abuse"), None
    )
    if high is None:
        return {"status": "no content incident detected"}
    playbook = playbooks()["content_incident"]
    return {
        "incident_id": "INC-001",
        "signals": high["signals"],
        "severity": "high",
        "detected_window": high["start_window"],
        "detected_windows": len(high["windows"]),
        "playbook": playbook,
        "timeline": [
            {"step": "detect", "detail": f"content signals {', '.join(high['signals'])} in windows {high['start_window']}-{high['end_window']}"},
            {"step": "triage", "detail": "two or more content signals; treated as a model-targeted incident"},
            {"step": "contain", "detail": "edge squeezing enabled; client rate limits unchanged because the attack is distributed"},
            {"step": "rollback_check", "detail": f"previous checkpoint ASR {metrics['rollback']['attack_success_previous']:.4f} vs current {metrics['rollback']['attack_success_current']:.4f}; rollback rejected"},
            {"step": "recover", "detail": "attack traffic stopped; squeezing removed after measuring its clean-accuracy cost"},
            {"step": "learn", "detail": "robustness gate added to the release checklist; monitoring thresholds reviewed"},
        ],
        "rollback": metrics["rollback"],
        "mitigation": metrics["mitigation"],
        "abuse_episode": abuse["episode_id"] if abuse else None,
        "status": "contained, residual risk accepted",
    }


def build_report(metrics, incident, reference_rows):
    phases = metrics["phases"]
    diagnostics = metrics["window_diagnostics"]
    drift_conf = min(
        entry["stats"]["mean_confidence"]
        for entry in diagnostics
        if entry["scenario"] == "benign_drift"
    )
    baseline_shift = max(
        entry["stats"]["input_shift"]
        for entry in diagnostics
        if entry["scenario"] == "baseline"
    )
    lines = [
        "# LAB-15 report — monitoring and incident response",
        "",
        "All traffic is synthetic. A logistic-regression digit classifier is served "
        "from memory, and six simulated scenarios produce prediction logs. Detectors "
        "are calibrated on a quiet period and then run on monitored windows of "
        f"{metrics['window_size']} requests. The attacker is assumed to send crafted "
        "inputs through the normal prediction API; the monitor sees only telemetry.",
        "",
        "## Threat model and telemetry",
        "",
        "The monitor observes request timing, client identity, raw input features, "
        "the predicted class, confidence, and a shadow-model prediction. It does not "
        "see attacker intent, and labels shown in this lab are synthetic evaluation "
        "labels that arrive immediately; a real service rarely has them on time.",
        "",
        "## Calibration and thresholds",
        "",
        f"Thresholds use {metrics['threshold_policy']['sigmas']:g} standard deviations from "
        f"{metrics['calibration']['windows']} calibration windows ({reference_rows} requests). "
        "Confidence is one-sided low, disagreement and throughput are one-sided high, "
        "and client concentration is a fixed policy value.",
        "",
        "| Detector | Threshold | Interpretation |",
        "|---|---:|---|",
        f"| Input shift | {metrics['thresholds']['input_shift']:.4f} | window mean drifts from the calibration reference |",
        f"| Low confidence | {metrics['thresholds']['low_confidence']:.4f} | mean maximum probability falls below the band |",
        f"| Shadow disagreement | {metrics['thresholds']['shadow_disagreement']:.4f} | deployed and shadow models disagree more often |",
        f"| Client concentration | {metrics['thresholds']['client_concentration']:.4f} | one client dominates the window |",
        f"| Throughput | {metrics['thresholds']['throughput']:.4f} req/s | request rate exceeds calibration |",
        "",
        "## Scenario results",
        "",
        "| Scenario | Windows | Alerting | Mean confidence | Accuracy | Signals |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for name in ("baseline", "benign_drift", "evasion_attack", "query_burst", "recovery"):
        block = phases[name]
        active = ", ".join(
            f"{signal} x{count}" for signal, count in block["signal_counts"].items() if count
        ) or "none"
        lines.append(
            f"| {name} | {block['windows']} | {block['alerting_windows']} | "
            f"{block['mean_confidence']:.4f} | {block['accuracy']:.4f} | {active} |"
        )
    lines += [
        "",
        f"Baseline false positives: {metrics['false_positive']['alerting_windows']} of "
        f"{metrics['false_positive']['windows']} windows (rate "
        f"{metrics['false_positive']['rate']:.4f}). A clean baseline is encouraging, "
        "not proof that the thresholds are safe for all traffic. The widest baseline "
        f"input shift was {baseline_shift:.4f} against a threshold of "
        f"{metrics['thresholds']['input_shift']:.4f}; the margin is not large, and it "
        "would shrink on a different day.",
        "",
        "## Control coverage",
        "",
        "| Stage | Observable | Control |",
        "|---|---|---|",
        "| Volume abuse | one client dominates the window and request rate spikes | client concentration and throughput detectors, then rate limits and token review |",
        "| Input manipulation | feature shift, confidence drop, and shadow disagreement together | content detectors, then an incident, edge preprocessing, and a robustness review |",
        "| Benign change | feature shift with stable confidence and shadow agreement | drift review; no incident and no rollback |",
        "| Post-incident | clean windows return to the calibrated band | recovery verification before closing the incident |",
        "",
        "Monitoring is detective. It does not stop a request, and it cannot compensate "
        "for missing authentication, rate limits, or a weak model. It belongs alongside "
        "the serving controls from LAB-14, the robustness evaluation from LAB-11, and "
        "the supply-chain checks from LAB-13.",
        "",
        "## Episodes and triage",
        "",
        "| Episode | Windows | Classification | Severity | Signals |",
        "|---|---:|---|---|---|",
    ]
    for episode in metrics["episodes"]:
        lines.append(
            f"| {episode['episode_id']} | {episode['start_window']}-{episode['end_window']} | "
            f"{episode['classification']} | {episode['severity']} | "
            f"{', '.join(episode['signals'])} |"
        )
    lines += [
        "",
        "The benign drift fires only the input-shift detector. Confidence and shadow "
        "agreement stay inside their bands, so triage keeps it at low severity: an "
        "alert is not automatically an incident. The evasion phase fires all three "
        "content signals and becomes a high-severity incident. The query burst fires "
        "only volume signals and is handled as abuse, not as model compromise. This "
        f"separation is the point: {metrics['confirmed_incidents']} confirmed content "
        "incident emerged from three alerting episodes.",
        "",
        "Threshold sensitivity matters. During the drift episode the lowest window "
        f"confidence was {drift_conf:.4f} against a threshold of "
        f"{metrics['thresholds']['low_confidence']:.4f}. A slightly stricter threshold "
        "would have escalated the drift to a content incident, and a slightly looser one "
        "would have hidden the attack's confidence drop. The 5-sigma policy is a choice, "
        "not a law, and it should be reviewed against real traffic.",
        "",
        "## Trade-offs",
        "",
        "- Window size: 100 requests detects quickly but makes each statistic noisy; a larger window is steadier and slower to alert.",
        "- Threshold width: 5 sigma suppresses false positives but delays detection of subtle attacks.",
        "- Preprocessing: edge squeezing lowers attack success here but costs clean accuracy, and an adaptive attacker can approximate the quantizer.",
        "- Log detail: storing raw features makes the exercise reproducible, but a production service should aggregate or redact them and protect the log pipeline itself.",
        "",
        "## Incident response",
        "",
        f"The content incident is {incident['incident_id']} (severity {incident['severity']}). "
        f"The playbook begins with detection at window {incident['detected_window']} and "
        "runs confirm, contain, verify, eradicate, recover, and learn.",
        "",
        f"Rollback was evaluated, not assumed. Replaying a captured FGSM batch "
        f"(epsilon={metrics['epsilon']:.2f}, base set {metrics['rollback']['base_size']}) "
        f"gives attack success {metrics['rollback']['attack_success_current']:.4f} on the "
        f"current checkpoint and {metrics['rollback']['attack_success_previous']:.4f} on the "
        f"previous one. Restored: {metrics['rollback']['restored']}. A rollback between two "
        "checkpoints with the same weakness is not containment, and the report records "
        "that decision instead of claiming a fix.",
        "",
        f"Edge input squeezing reduced attack success from "
        f"{metrics['mitigation']['attack_success_before']:.4f} to "
        f"{metrics['mitigation']['attack_success_after']:.4f} on the replay batch, at a "
        f"clean-accuracy cost from {metrics['mitigation']['clean_accuracy_before']:.4f} to "
        f"{metrics['mitigation']['clean_accuracy_after']:.4f}. Squeezing is a temporary "
        "brake: an adaptive attacker can approximate the quantizer, so the residual risk "
        "stays open and is tracked rather than declared closed.",
        "",
        "## Recovery and residual risk",
        "",
        f"Recovery windows alert {metrics['recovery']['alerting_windows']} times; mean "
        f"confidence {metrics['recovery']['mean_confidence']:.4f} stays above the "
        f"{metrics['recovery']['confidence_threshold']:.4f} threshold. Squeezing was removed "
        "after the attack stopped because of its accuracy cost; rate limits and elevated "
        "monitoring remain. Residual risk is accepted with an owner and a review date in a "
        "real deployment; here it is recorded as an open limitation.",
        "",
        "## Limitations",
        "",
        "- Synthetic traffic, one dataset, one linear model, and one attack family.",
        "- Thresholds are calibrated on 12 quiet windows; more history would change them.",
        "- Immediate labels are unrealistic; production monitoring must tolerate label lag.",
        "- An adaptive attacker can shape traffic to stay under these thresholds.",
        "- Raw features are logged here for reproducibility; production logs should aggregate or redact them.",
        "- A passing test or a quiet baseline is not proof that the service is secure.",
        "",
        "## Reproducibility",
        "",
        "Run `python solution.py --out artifacts` and then "
        "`python check_lab15.py --artifacts artifacts` from this directory. The seed, "
        "window size, model versions, and thresholds are recorded in `metrics.json` and "
        "`run.json`; the manifest hashes all evidence files.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor synthetic prediction traffic and triage incidents.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "logs").mkdir(parents=True, exist_ok=True)

    X_train, X_test, y_train, y_test = load_split()
    deployed, previous, shadow = train_models(X_train, y_train)

    records = build_traffic(deployed, shadow, X_test, y_test)
    reference = reference_distribution(records)
    thresholds, calibration = calibrate(records, reference)
    diagnostics = window_diagnostics(records, reference, thresholds)
    measurements = attack_measurements(deployed, previous, X_test, y_test)
    metrics = build_metrics(diagnostics, thresholds, calibration, reference, measurements)
    incident = build_incident_response(metrics)

    log_path = args.out / "logs" / "predictions.jsonl"
    with open(log_path, "w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    write_json(args.out / "metrics.json", metrics)
    write_json(
        args.out / "run.json",
        {
            "lab": "LAB-15",
            "seed": SEED,
            "window_size": WINDOW,
            "epsilon": EPSILON,
            "squeeze_levels": SQUEEZE_LEVELS,
            "deployed_model": DEPLOYED_VERSION,
            "previous_model": PREVIOUS_VERSION,
            "threshold_sigmas": THRESHOLD_SIGMAS,
            "environment": environment(),
        },
    )
    (args.out / "report.md").write_text(
        build_report(metrics, incident, reference["rows"]), encoding="utf-8", newline="\n"
    )
    write_json(
        args.out / "manifest.json",
        build_manifest(
            args.out,
            ["metrics.json", "run.json", "report.md", "logs/predictions.jsonl"],
        ),
    )

    baseline = metrics["phases"]["baseline"]
    print(f"baseline false positives: {baseline['alerting_windows']}/{baseline['windows']} windows")
    for episode in metrics["episodes"]:
        print(
            f"{episode['episode_id']} {episode['classification']} "
            f"({episode['severity']}) windows {episode['start_window']}-{episode['end_window']}"
        )
    print(
        f"rollback restored={metrics['rollback']['restored']} "
        f"asr_current={metrics['rollback']['attack_success_current']:.4f} "
        f"asr_previous={metrics['rollback']['attack_success_previous']:.4f}"
    )
    print(
        f"mitigation asr {metrics['mitigation']['attack_success_before']:.4f} -> "
        f"{metrics['mitigation']['attack_success_after']:.4f}"
    )
    print(f"artifacts written to {args.out}")


if __name__ == "__main__":
    main()
