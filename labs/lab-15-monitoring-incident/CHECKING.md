# Checking Guide — LAB-15

## What the checker verifies

1. The manifest covers `metrics.json`, `run.json`, `report.md`, and `logs/predictions.jsonl`, and every hash and size matches the file.
2. `run.json` records LAB-15 with seed 37, window 100, and epsilon 0.10.
3. The log holds 3,900 requests: 1,200 calibration, 600 baseline, 600 drift, 600 evasion, 600 burst, and 300 recovery.
4. Every record has the exact expected fields, 64 features in [0, 1], valid classes, a probability confidence, a unique request ID, and ordered timestamps.
5. The calibration reference and all five thresholds recompute from the logs within tolerance.
6. Every window statistic, alert flag, classification, and severity recomputes from the logs.
7. Baseline has zero alerting windows; recovery has zero alerting windows and its mean confidence is above the threshold.
8. Drift produces exactly one low-severity input-shift episode; evasion produces a high-severity episode with at least two content signals; the burst produces a medium-severity volume-only episode.
9. Exactly one confirmed content incident is recorded.
10. Rollback is not recorded as restored, the previous checkpoint remains vulnerable, and the base set is 288 rows.
11. Squeezing reduces attack success and keeps clean accuracy at or above 0.90.
12. The report contains "monitoring", "drift", "incident", "false positive", "rollback", "residual", and "limitations".

## Reference results (seed 37)

| Check | Result |
|---|---|
| Calibration windows / requests | 12 / 1,200 |
| Input-shift threshold | 0.1529 |
| Low-confidence threshold | 0.8232 |
| Shadow-disagreement threshold | 0.0823 |
| Baseline alerting windows | 0 / 6 |
| Drift alerting windows | 6 / 6 (input shift only) |
| Evasion alerting windows | 6 / 6 (all three content signals) |
| Burst alerting windows | 6 / 6 (both volume signals) |
| Recovery alerting windows | 0 / 3 |
| Confirmed incidents | 1 |
| Rollback restored | no |
| ASR current / previous checkpoint | 0.3507 / 0.3299 |
| ASR with squeezing | 0.1979 |
| Clean accuracy current / squeezed | 0.9600 / 0.9433 |

## Why these numbers matter

The three alerting episodes are deliberately different. Drift changes the input
distribution but leaves confidence and shadow agreement inside their bands, so a
single-signal alert stays low severity. Evasion changes all three content
signals at once, which is what raises it to an incident. The burst is obvious in
volume but invisible in content; treating it as model compromise would send the
responder down the wrong path.

The rollback result is the honesty check. Reverting to the previous checkpoint
still leaves a 0.33 attack success rate, so rollback is rejected as containment
rather than reported as a fix. Squeezing helps on this batch but costs clean
accuracy, and an adaptive attacker can approximate the quantizer (LAB-11).
Detection is not prevention, and a quiet baseline is not proof of safety.

The drift episode also comes close to the confidence threshold: the lowest drift
window sits at 0.830 against 0.823. A stricter threshold would have escalated a
benign change. That sensitivity is part of the lesson, not a defect to hide.

## Threat-to-control mapping

| Threat | Indicator | Control | Evidence | Residual risk |
|---|---|---|---|---|
| Model evasion with crafted inputs | Input shift plus confidence drop plus shadow disagreement | Content detectors, triage, incident playbook | One high-severity episode, 6/6 windows | Attackers can shape traffic under thresholds |
| Scraping or extraction burst | One client dominates and throughput spikes | Volume detectors, rate limits, token review | Medium-severity volume-only episode | Distributed abuse from many clients is harder |
| Unannounced data or sensor change | Input shift alone | Drift review, no automatic rollback | Low-severity episode with stable confidence | Real drift can be slow and below thresholds |
| Bad deployment rollback | Attack success unchanged after revert | Verify before declaring containment | Rollback rejected on replay batch | A different checkpoint may hide the same weakness |
| Alert fatigue | Baseline and recovery quiet | Calibrated 5-sigma thresholds | 0/6 and 0/3 alerting windows | Small calibration sample is optimistic |
| Sensitive data in logs | Raw features present in this lab | Restrict and aggregate logs in production | Documented limitation | Log pipeline itself needs access control |

ATLAS references: AML.T0043 (craft adversarial data), AML.T0015 (evade ML
model), AML.T0024 (exfiltration via ML inference API). The mapping is
illustrative; the lab does not claim these techniques are exhaustive.

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| `NotImplementedError` | A TODO block is untouched | Implement window_statistics, detect, or triage |
| Thresholds do not reproduce | Calibration computed over monitored windows or all traffic | Calibrate on `scenario == "calibration"` only |
| Input shift is huge or unstable | Dividing by a zero feature standard deviation | Floor the reference standard deviation at 0.05 and clip z-scores at 5 |
| Drift escalates to an incident | Triage treats any alert as high severity | Use the signal-family rules |
| Burst classified as evasion | Content signals computed on the wrong fields | Compare predicted_class with shadow_class, not label |
| Recovery still alerts | Edge squeezing applied during recovery, or thresholds not recalibrated | Serve recovery traffic through the normal pipeline |
| Baseline false positives | Too few calibration windows or thresholds too tight | Keep 12 calibration windows and the 5-sigma policy |
| Checker hash mismatch | Metrics regenerated after the manifest | Rerun `solution.py`, which writes the manifest last |

## Rubric (20 points)

| Item | Points |
|---|---:|
| Correct window statistics and detector inputs | 5 |
| Correct threshold comparison and alert semantics | 4 |
| Signal-family triage and episode grouping | 4 |
| Reproducible logs, thresholds, and metrics | 3 |
| Incident response with rollback and mitigation evidence | 2 |
| Honest report with trade-offs, residual risk, and limitations | 2 |

## Reflection questions

1. Why calibrate on a quiet period instead of the monitored baseline?
2. Drift and evasion both raise an input-shift alert. What evidence separates them?
3. Why is a single high-severity alert not enough to open an incident?
4. The rollback check rejects the previous checkpoint. What would make a rollback a valid containment step?
5. Which detector would you remove first if you had to reduce alert volume, and what would you lose?
6. What does the monitor still miss if the attacker spreads the same attack across many clients?
7. Why should production logs avoid storing raw input features, and what would you log instead?
