# LAB-15 — Monitoring, Drift, and Incident Response

**Tier A · 3 hours · Difficulty 3 · Module M11 · Outcomes LO-23, LO-28, LO-30 (supporting)**

## Why this lab exists

A prediction service has no incident feed. It has logs, and someone has to decide
which patterns in those logs deserve an incident number. Two mistakes are common.
The first is treating every alert as an attack, which burns the responder's
attention on a scanner recalibration. The second is treating a quiet dashboard
as safety, which misses a slow evasion campaign entirely.

This lab runs six synthetic scenarios through one local classifier and asks you
to build the detection layer: window statistics, calibrated thresholds, alert
triage, and a written incident response. The interesting result is not that the
attack is detected. It is that the benign change is detected too, with one signal
instead of three, and that the correct response is different.

## The system and the threat model

| Element | Assumption |
|---|---|
| Asset | A digits classifier served through a prediction API, plus its request logs |
| Attacker goal | Integrity: make the model answer incorrectly without touching the model |
| Attacker knowledge | The input format is public; the model version and confidence are not |
| Attacker capability | Send crafted inputs through the normal prediction API, possibly at high volume |
| Monitor capability | Per-request timing, client id, input features, predicted class, confidence, shadow-model class |
| Constraints | Windows of 100 requests; thresholds calibrated on a quiet period only |
| Base set | Calibration traffic, then baseline, drift, evasion, burst, and recovery phases |
| Metric | Alerting windows per phase, episode triage, rollback and mitigation measurements |
| Lifecycle stage | Serving, detection, and response |
| Out of scope | Real traffic, real attackers, distributed rate limiting, alert routing, paging |

The traffic, clients, and incidents are simulated. The attacker in the evasion
phase runs white-box FGSM against the model, which is a stronger attacker than
the monitor can observe; that is deliberate, because detection must work from
telemetry alone.

## What you produce

A folder inside `labs/lab-15-monitoring-incident/` containing:

| File | Contents |
|---|---|
| `metrics.json` | Thresholds, per-phase summaries, window diagnostics, episodes, rollback, mitigation, recovery |
| `logs/predictions.jsonl` | One JSON record per request, including the input features and model outputs |
| `run.json` | Seed, window size, model versions, environment versions |
| `report.md` | Threat model, thresholds, phase table, triage rationale, IR timeline, limitations |
| `manifest.json` | SHA-256 hashes of the four files above |

The reference implementation writes these under `artifacts/`. Your completed
`starter.py` must produce the same structure.

## Prerequisites

- Module 04 Lessons 1–3 (evasion and budgets) and Module 07 (extraction and abuse).
- Module 11 Lessons 4–5 (logging, monitoring, and incident response).
- LAB-11 and LAB-14 recommended: robustness evaluation and the hardened service.

## Environment

- Python 3.14.7; `numpy==2.5.2`, `pandas==3.0.5`, `scikit-learn==1.9.0`, `joblib==1.5.3`, `PyYAML==6.0.3`.
- CPU only; the reference run takes a few seconds and writes about 2.5 MB of logs.
- No network, no cloud account, no API key. The digits dataset ships with scikit-learn.

```bash
cd labs/lab-15-monitoring-incident
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab15.py --artifacts artifacts
```

## Safety rules

- The traffic is generated locally. Do not point the scenario generator at any real service.
- Do not reuse the synthetic client ids or tokens against a real API.
- Do not add real user data to the logs. The lab logs features only to make the statistics reproducible.
- Keep the burst small and local. The scenario is 600 requests, not a load test.

## Task specification

1. **Log the request.** For each request, record window id, scenario, request id,
   timestamp, client, model version, predicted class, shadow class, confidence,
   label, and the 64 input features.
2. **Build the reference.** From calibration traffic only, compute the per-feature
   mean and a floored standard deviation. Never calibrate on monitored windows.
3. **Compute window statistics.** For each 100-request window, compute input shift,
   mean confidence, shadow disagreement, client concentration, and throughput.
4. **Calibrate thresholds.** Use five standard deviations from the calibration
   windows, one-sided in the correct direction, with floors for confidence,
   disagreement, and throughput. Client concentration is a fixed 0.60 policy.
5. **Detect.** Alert on strict threshold crossings. Record the alert set per window.
6. **Triage.** Map signal families to classification and severity. Content signals
   together suggest evasion; volume signals alone suggest abuse; a single content
   signal is a drift candidate.
7. **Group episodes.** Consecutive alerting windows with the same triage become one
   episode. Run the incident playbook for the high-severity episode.
8. **Verify, do not assume.** Test rollback on a captured attack batch, measure the
   squeezing mitigation, and confirm recovery windows return to the calibrated band.
9. **Report.** Explain the threshold choice, the drift-evasion distinction, the
   rollback result, residual risk, trade-offs, and limitations.

## Detection design

| Detector | Statistic | Threshold | Direction |
|---|---|---:|---|
| Input shift | RMS of clipped z-scores of the window mean | 0.1529 | high |
| Low confidence | Mean maximum softmax probability | 0.8232 | low |
| Shadow disagreement | Fraction where deployed and shadow classes differ | 0.0823 | high |
| Client concentration | Largest client share of the window | 0.6000 | high |
| Throughput | Requests per second inside the window | 5.0000 | high |

The threshold values above come from the seed-37 reference run. Yours should match
if you keep the generator, window size, and calibration rules.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `window_statistics` | Compute windowed content and volume statistics |
| `starter.py` | TODO 2 | `detect` | Return the five detector booleans calibrated on the quiet period |
| `starter.py` | TODO 3 | `triage` | Classify the episode, assign severity, and select a playbook |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-15-monitoring-incident/CHECKING.md`.

## Scenarios and expected outcomes

| Scenario | Windows | Expected alerts | Expected triage |
|---|---:|---|---|
| Calibration | 12 | not monitored | source of thresholds |
| Baseline | 6 | 0 | none |
| Benign drift | 6 | input shift ×6 | low: drift under review |
| Evasion attack | 6 | three content signals ×6 | high: probable evasion |
| Query burst | 6 | volume signals ×6 | medium: client abuse |
| Recovery | 3 | 0 | none |

Reference results:

| Metric | Value |
|---|---:|
| Baseline false-positive windows | 0 / 6 |
| Confirmed content incidents | 1 |
| Rollback restored | no |
| ASR current / previous checkpoint | 0.3507 / 0.3299 |
| ASR before / after squeezing | 0.3507 / 0.1979 |
| Clean accuracy before / after squeezing | 0.9600 / 0.9433 |
| Recovery alerting windows | 0 / 3 |

## Threat-to-control mapping

| Threat | Indicator | Control | Residual risk |
|---|---|---|---|
| Evasion with crafted inputs (AML.T0043, AML.T0015) | Shift + confidence + shadow disagreement | Content detectors and incident playbook | Attacker can shape traffic under thresholds |
| Scraping or extraction burst (AML.T0024) | Client concentration + throughput | Volume detectors, rate limits, token review | Distributed abuse across many clients |
| Unannounced data change | Shift alone with stable confidence | Drift review; no automatic rollback | Slow drift may stay under thresholds |
| Bad rollback | ASR unchanged after revert | Verify rollback before closing an incident | A different checkpoint may share the weakness |
| Alert fatigue | Baseline and recovery quiet | Calibrated 5-sigma thresholds | Small calibration sample is optimistic |
| Log privacy | Raw features present | Aggregate or redact in production | Log pipeline needs its own access control |

ATLAS identifiers are used for orientation only. The mapping is not a claim that
these are the only techniques an attacker could use.

## Defense-in-depth perspective

Monitoring is the detective layer. It does not stop requests; authentication,
rate limiting, and validation do that (LAB-14). It does not make the model
robust; adversarial training and honest evaluation do that (LAB-11). It does not
protect the artifact; signatures and dependency controls do that (LAB-13).

The layers fail differently. A content attack can come from valid clients and
slip past rate limits. A burst can look harmless in content. A drift can look
like an attack to a single detector. The lab is designed so that no single
detector is sufficient and no single response closes every incident.

## Deliverables checklist

- [ ] `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] Detector calibration values, episode grouping, and per-scenario outcomes.
- [ ] An incident timeline and playbook for the high-severity episode.
- [ ] `report.md` answers every reflection question and explains why rollback was accepted or rejected.
- [ ] `python check_lab15.py --artifacts artifacts` exits 0.

## Success criteria

- [ ] Thresholds are calibrated on calibration traffic only.
- [ ] Baseline has zero alerting windows; recovery has zero alerting windows.
- [ ] Drift produces one low-severity input-shift episode.
- [ ] Evasion produces one high-severity episode with at least two content signals.
- [ ] The burst produces one medium-severity volume-only episode.
- [ ] Rollback is evaluated and explicitly rejected, not assumed to work.
- [ ] Squeezing is measured, including its clean-accuracy cost and residual bypass risk.
- [ ] The report separates alerts from incidents and states the limitations.
- [ ] `python check_lab15.py --artifacts artifacts` exits 0.

## How to check yourself

The checker reprocesses your prediction log from scratch: it rebuilds the
reference distribution, thresholds, window statistics, alerts, and episodes, then
compares them with `metrics.json`. That is stronger than checking recorded
numbers, but it still cannot tell whether your triage policy is wise or whether
your report is honest. The rubric covers those parts.

## Rubric (20 points)

| Item | Points |
|---|---:|
| Correct window statistics and detector inputs | 5 |
| Correct thresholds, alert semantics, and episode grouping | 4 |
| Signal-family triage with drift/abuse/evasion separation | 4 |
| Reproducible logs, metrics, and manifest | 3 |
| Incident response with rollback, mitigation, and recovery evidence | 2 |
| Threat model, trade-offs, residual risk, and limitations | 2 |

## Reflection questions

1. Why calibrate on a quiet period rather than on the monitored baseline?
2. Drift and evasion both raise an input-shift alert. What evidence separates them, and what would you do if the attacker kept confidence high?
3. The burst is obvious in volume but invisible in content. Why is "abuse" a different response from "model compromise"?
4. The previous checkpoint is just as vulnerable. What would make a rollback a valid containment step?
5. What does the monitor miss if the attacker spreads the same campaign across many clients at low volume?
6. Which detector would you drop first to reduce alert volume, and what would you lose?
7. Why should a production service avoid logging raw input features, and what could it log instead?
8. A quiet baseline and a passing checker are not proof of security. What would you add before trusting this monitor?

## Hints

1. Calibrate on the quiet window only. If you calibrate on attack traffic, the threshold is contaminated.
2. Each detector returns a boolean for one window. Group consecutive alerts into episodes before triage.
3. Triage needs a signal family and a severity rule, not a single alert count.
4. Rollback is a hypothesis. Test it against a captured attack batch; if the old checkpoint is also vulnerable, say so.

## Time box

| Hour | Work |
|---|---|
| 1 | Read the log schema and pipeline; implement window statistics |
| 2 | Implement detect and triage; run the scenarios and inspect episodes |
| 3 | Test rollback and recovery, then write the report and limitations |

Stop at 4.5 hours and submit with a note on what is incomplete.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `NotImplementedError` | A TODO block is untouched | Implement window_statistics, detect, or triage |
| Thresholds do not reproduce | Calibrated over monitored traffic | Filter to `scenario == "calibration"` |
| Input shift explodes | Dividing by a near-zero feature standard deviation | Floor the reference std at 0.05 and clip z-scores at 5 |
| Drift becomes a high incident | Triage escalates any alert | Require two content signals or content plus volume |
| Burst becomes an evasion incident | Comparing predictions with labels instead of the shadow model | Use predicted_class vs shadow_class |
| Recovery alerts | Squeezing applied to recovery traffic, shifting the input distribution | Serve recovery through the normal pipeline |
| Baseline false positives | Too few calibration windows or tighter thresholds | Keep 12 windows and the 5-sigma policy |
| Manifest hash mismatch | Metrics regenerated after the manifest | Rerun `solution.py`, which writes the manifest last |

## Cleanup

```bash
# Windows PowerShell
Remove-Item -Recurse -Force artifacts
# macOS/Linux
rm -rf artifacts
```

Remove the virtual environment if you created one for this lab. Never commit `artifacts/`.

## References

- [Lab catalog](../lab-catalog.md) · [Learning outcomes](../learning-outcomes.md)
- [References](../references.md) — F-20, F-19, R-04
- [Module page](../modules/m11-serving-monitoring/index.md) — M11 — Secure Model Serving, API Security, Monitoring, and Incident Response
- Package checking guide: `labs/lab-15-monitoring-incident/CHECKING.md`

## What comes next

This is the last lab of Level 3. Level 4 begins with Module 12, which turns to
federated learning: clients you do not control, update poisoning, and aggregation
rules whose assumptions an attacker can violate. Module 13 then takes up privacy
— what a model leaks about the people in its training data, how to measure that
leakage, and what differential privacy does and does not promise. The
membership-inference ideas from LAB-10 return there with a stronger evaluation
setup, and the monitoring habits from this lab are what tell you whether a
privacy control is actually working.
