# Lesson 11.4 — Monitoring, Drift, and Attack Indicators

<a id="m11-l4"></a>

**Module 11 · Lesson 4 of 6 · 1.5 hours · LO-23**

## Scenario

The prediction API from LAB-14 has been running for a month. There is no incident feed, no analyst, and no alarm. There are logs. Someone notices that average confidence is lower this week and asks whether the model is under attack, whether a scanner changed, or whether the traffic is simply different.

The logs cannot answer that question directly. They can answer a narrower one: which windows of traffic differ from a quiet reference period, in which measured way, and how those differences co-occur. That is what a detection layer does. It converts telemetry into alerts, and alerts into a triage decision that a human can review.

This lesson builds that layer on LAB-15's synthetic traffic and examines where it fails.

## Objectives

By the end of this lesson you will be able to:

1. Define the telemetry a prediction service needs for detection and the privacy limits on it.
2. Distinguish data drift, concept drift, evasion, and volume abuse by their observable signatures.
3. Compute window statistics and calibrate one-sided thresholds on a quiet reference period.
4. Group consecutive alerting windows into episodes and triage them by signal family.
5. Interpret false positives, missed detections, and threshold sensitivity.
6. State why detection is not prevention and why a quiet dashboard is not evidence of safety.

## 1. What the service can observe

| Field | Detection value | Privacy or operational concern |
|---|---|---|
| Request id | Correlation across logs and incidents | Low |
| Timestamp | Throughput, window boundaries, timing | Reveals traffic patterns |
| Client id | Concentration, per-client rate, abuse | Pseudonymous, but linkable |
| Model version | Change correlation, rollback verification | Version disclosure |
| Predicted class | Distribution shift, class imbalance | May reveal sensitive inferences |
| Confidence | Evasion, distribution change | Can support extraction |
| Shadow-model class | Disagreement signal | Extra compute; shadow model governance |
| Input features | Distribution shift, drift | Often personal or sensitive; high risk |
| Label | Accuracy, delayed ground truth | Often unavailable in real time |
| Latency and status | Availability, errors, abuse | Low |

LAB-15 logs the full feature vector to make the statistics reproducible, and its report says explicitly that a production service should aggregate or redact it. That is not a contradiction. The lab is a measurement environment; production is a data-protection environment.

A practical production compromise is to log per-window aggregates (means, variances, quantiles, hashes) rather than raw rows, and to keep raw rows only for a short, access-controlled forensic window when policy allows.

## 2. Four phenomena, four signatures

| Phenomenon | Definition | Input distribution | Confidence | Shadow disagreement | Volume |
|---|---|---|---|---|---|
| Data drift | Inputs change while the input-output relationship holds | Shifts | Usually stable | Low | Normal |
| Concept drift | The relationship between inputs and labels changes | May be stable | May fall | May rise | Normal |
| Evasion | Crafted inputs cause wrong predictions | Shifts in a targeted way | Falls | Rises | Normal or high |
| Volume abuse | A client sends many requests, often benign | Normal | Normal | Low | High and concentrated |

These are tendencies, not laws. A slow drift can lower confidence. A clever evasion can keep confidence high. A scraper can distribute across clients. The signatures are evidence, not proof.

### LAB-15's three alerting scenarios

| Scenario | What happens | Signals | Triage |
|---|---|---|---|
| Benign drift | A scanner recalibrates: darker, noisier images, same classes | `input_shift` only | Low: drift under review |
| Evasion | White-box FGSM at ε = 0.10 through the normal API | `input_shift`, `low_confidence`, `shadow_disagreement` | High: probable evasion |
| Query burst | One client sends at machine speed | `client_concentration`, `throughput` | Medium: client abuse |

The drift episode is the important one for calibration. It is a real change that operators must know about, but it is not an attack. A detector that cannot separate it from evasion will either cry wolf or hide a scanner change. The separation comes from the other signals, not from the input shift alone.

## 3. The reference distribution

Detection starts with a reference. LAB-15 uses 12 calibration windows of 100 requests each: 1,200 quiet requests.

For each feature \(j\):

\[
z_{j} = \operatorname{clip}\left(\frac{\bar{x}_{j} - \mu_{j}}{\max(\sigma_{j}, 0.05)}, -5, 5\right)
\]

\[
\text{input shift} = \sqrt{\frac{1}{d}\sum_{j=1}^{d} z_{j}^{2}}
\]

- \(\mu_j\) and \(\sigma_j\) come from calibration rows only.
- The standard deviation is floored at 0.05 so a nearly constant pixel does not create enormous z-scores.
- Each z-score is clipped at ±5 so one extreme feature does not dominate the window.
- The root mean square summarizes the window's average deviation in standard-deviation units.

Calibrating on monitored traffic would absorb the attack into the reference and make the attack look normal. That is the most common way a detector is quietly defeated.

### The other four statistics

| Statistic | Definition | Direction that matters |
|---|---|---|
| Mean confidence | Mean maximum predicted probability in the window | Low |
| Shadow disagreement | Fraction of rows where deployed and shadow classes differ | High |
| Client concentration | Largest client's share of the window | High |
| Throughput | Requests divided by the window's time span | High |

The shadow model is trained on a 60% subset of the training data with a different regularization setting. It is a comparison signal, not an oracle. Its disagreement can rise because the input distribution changed, because the deployed model is wrong, or because the shadow model is wrong.

## 4. Thresholds

LAB-15 uses five standard deviations from the calibration windows, one-sided in the harmful direction, with floors:

| Detector | Threshold | Direction | Floor or policy |
|---|---:|---|---|
| Input shift | 0.1529 | High | Mean + 5σ, minimum 0.01 |
| Low confidence | 0.8232 | Low | Mean − 5σ, floor 0.80 |
| Shadow disagreement | 0.0823 | High | Mean + 5σ, floor 0.05 |
| Client concentration | 0.6000 | High | Fixed policy value |
| Throughput | 5.0 req/s | High | Mean + 5σ, floor 5.0 |

Two design choices deserve scrutiny.

**One-sided thresholds.** Confidence is only alarming when it is low. Throughput is only alarming when it is high. A two-sided threshold would alert on unusually good confidence, which is noise.

**Floors and policy values.** A 5σ threshold derived from 12 windows can be too tight or too loose. The floor keeps a detector from firing on a tiny absolute change. The concentration threshold is a policy choice, not a statistical estimate: one client taking more than 60% of a window is worth reviewing regardless of the calibration mean.

### Threshold sensitivity

The report from LAB-15 notes that the lowest drift-window confidence stays above 0.8232, but not by a large margin. A slightly stricter confidence threshold would escalate the benign drift into a content incident. A slightly looser one might hide the evasion's confidence drop.

That is the central trade-off of threshold design:

| Threshold | Effect |
|---|---|
| Tighter | More detections, more false positives, faster alert fatigue |
| Looser | Fewer false positives, later or missed detections |
| More calibration data | More stable estimate, slower to adapt |
| Shorter windows | Faster detection, noisier statistics |
| Longer windows | Steadier statistics, slower detection |

There is no universal setting. The choice belongs in the report, with the data that produced it.

## 5. Detection and triage

LAB-15 compares each window's statistic with its threshold using a strict crossing:

```python
def detect(stats, thresholds):
    return {
        "input_shift": stats["input_shift"] > thresholds["input_shift"],
        "low_confidence": stats["mean_confidence"] < thresholds["low_confidence"],
        "shadow_disagreement": stats["shadow_disagreement"] > thresholds["shadow_disagreement"],
        "client_concentration": stats["client_concentration"] > thresholds["client_concentration"],
        "throughput": stats["throughput"] > thresholds["throughput"],
    }
```

Then it triages by signal family:

| Active signals | Classification | Severity | Playbook |
|---|---|---|---|
| Two or more content signals, or content plus volume | Probable evasion or model-targeted abuse | High | Content incident |
| Volume signals only | Client abuse or scraping | Medium | Volume abuse |
| One content signal only | Distribution drift under review | Low | Drift review |
| None | None | None | None |

The rule encodes a judgment: a single content signal is not enough to call an incident. It could be a scanner change, a data-pipeline change, or a model deployment. Two independent content signals, or content plus volume, are harder to explain benignly.

### Episodes

Consecutive alerting windows with the same triage become one episode. LAB-15 produces three:

| Episode | Windows | Classification | Severity | Signals |
|---|---|---|---:|---|
| EP-01 | 18–23 | Distribution drift under review | Low | `input_shift` |
| EP-02 | 24–29 | Probable evasion or model-targeted abuse | High | all three content signals |
| EP-03 | 30–35 | Client abuse or scraping | Medium | `client_concentration`, `throughput` |

Eighteen alerting windows become three episodes and one confirmed incident. That compression is the point of triage: responders work on incidents, not on every threshold crossing.

### The phase results

| Scenario | Windows | Alerting | Mean confidence | Accuracy | Signals |
|---|---:|---:|---:|---:|---|
| Baseline | 6 | 0 | 0.8956 | 0.9733 | none |
| Benign drift | 6 | 6 | 0.8622 | 0.9600 | `input_shift` |
| Evasion | 6 | 6 | 0.6840 | 0.6300 | three content signals |
| Query burst | 6 | 6 | 0.8921 | 0.9600 | two volume signals |
| Recovery | 3 | 0 | 0.8926 | 0.9667 | none |

The baseline false-positive rate is 0/6 windows. That is encouraging and statistically weak: six windows is a small sample, and a threshold calibrated on 12 windows has wide uncertainty. A quiet week is not a guarantee for the next week.

Accuracy is shown because the synthetic labels are available immediately. In production, labels usually arrive late or never. A monitor that depends on real-time accuracy is a monitor that does not run.

## 6. What the monitor misses

| Blind spot | Why it matters | Mitigation |
|---|---|---|
| Adaptive attacker | Shapes traffic to stay under thresholds | Red-team the monitor; vary thresholds; correlate with auth and business signals |
| Distributed abuse | Spreads volume across many clients | Per-account aggregates, graph analysis, slower windows |
| Slow drift | Each window looks normal | Longer-horizon trend detection and change correlation |
| Label lag | Accuracy is unavailable | Use proxy signals; backfill labels later |
| Shadow model bias | Disagreement is not ground truth | Validate the shadow model; use multiple references |
| Log tampering | Evidence can be altered | Append-only storage, hashes, access control |
| Privacy exposure | Features are sensitive | Aggregate, redact, restrict, retain briefly |
| Alert fatigue | Too many low-value alerts | Triage, suppression, ownership, review |

The monitor is a detective control. It does not reject a request, revoke a token, or make the model robust. Those are preventive controls in LAB-14, LAB-11, and LAB-13. The monitor tells you when they were insufficient.

### Detection metrics

For a detector, four counts matter:

| | Actually an incident | Actually benign |
|---|---:|---:|
| Alert | True positive | False positive |
| No alert | False negative | True negative |

Precision is \(TP/(TP+FP)\): of the windows you alerted on, how many mattered? Recall is \(TP/(TP+FN)\): of the incident windows, how many did you catch? A detector with perfect recall and many false positives may still be unusable if responders stop reading alerts.

LAB-15's three episodes give a small, concrete example: one high-severity incident, one low-severity drift, one medium-severity abuse episode. The low and medium episodes are not failures of detection; they are successes of triage. They are alerts that did not become incidents.

## 7. Privacy and access

Monitoring data is sensitive even when the model is not.

- Prefer aggregates over raw features.
- If raw features are necessary, define retention, access, and deletion.
- Do not log credentials, authorization headers, or full request bodies.
- Protect the log pipeline with its own authentication and authorization.
- Hash or pseudonymize client identifiers where correlation is enough.
- Record who accessed the logs and why.

A log store with raw inputs and open access is a data breach waiting to be indexed. Lesson 5 treats logs as evidence; evidence still needs custody.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Calibrating on monitored traffic | It is the data at hand | Calibrate on a quiet period; document it |
| Using a two-sided threshold for confidence | Symmetry feels scientific | Alert only on the harmful direction |
| Treating every alert as an incident | Alerts look urgent | Triage by signal family and severity |
| Using one detector for everything | It is simpler to explain | Combine content and volume signals |
| Calling drift an attack | Both shift the input | Check confidence, shadow disagreement, and change tickets |
| Ignoring label lag | The lab has labels | Use proxies; backfill later |
| Logging raw features by default | It is useful for debugging | Aggregate; restrict raw retention |
| Reporting 0/6 false positives as proof | The number is clean | State the sample size and uncertainty |
| Assuming the shadow model is correct | It is another model | Validate it; treat disagreement as a signal |
| Forgetting the monitor's own security | It is "just logs" | Authenticate, authorize, and retain deliberately |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Thresholds do not reproduce | Calibration includes monitored windows | Filter to `scenario == "calibration"` |
| Input shift explodes | Near-zero feature standard deviation | Floor the reference std at 0.05; clip z-scores at 5 |
| Drift becomes high severity | Triage escalates any alert | Require two content signals or content plus volume |
| Burst becomes evasion | Using labels instead of the shadow model | Compare `predicted_class` with `shadow_class` |
| Recovery alerts | A mitigation is still applied to recovery traffic | Remove temporary controls before recovery checks |
| Baseline false positives | Too few calibration windows or thresholds too tight | Keep 12 windows and the 5σ policy |
| Every window alerts | Threshold direction or comparison reversed | Check `>` versus `<` per detector |
| No alerts at all | Thresholds computed from the wrong rows | Inspect the reference distribution and calibration summary |

## Check your understanding

1. Why calibrate on a quiet period rather than the monitored baseline?
2. Drift and evasion both raise an input-shift alert. Which two signals separate them in LAB-15?
3. Why is the confidence threshold one-sided low while throughput is one-sided high?
4. A detector alerts on 6 of 6 evasion windows and 2 of 6 baseline windows. What are its precision and recall on this sample?
5. Why is a 0/6 baseline false-positive result weak evidence?
6. What does the monitor not do, even when it works perfectly?

Answers are discussed in the [answer key](quiz-answers.md) and the exercises.

## Summary

- Telemetry turns requests into evidence, but raw features are sensitive; aggregate or redact in production.
- Drift, concept drift, evasion, and volume abuse have different signatures and different responses.
- LAB-15 calibrates five detectors on 12 quiet windows: input shift 0.1529, low confidence 0.8232, shadow disagreement 0.0823, client concentration 0.60, throughput 5.0 req/s.
- Baseline and recovery produce 0 alerting windows. Drift fires one signal and stays low. Evasion fires three content signals and becomes the single high-severity incident. The burst fires volume signals only and is handled as abuse.
- Eighteen alerting windows compress into three episodes and one confirmed incident.
- Thresholds are a trade-off, not a law. A small calibration sample makes the estimate uncertain.
- Detection is not prevention. An adaptive attacker can stay under thresholds, and a quiet dashboard is not proof of safety.

## Next

Continue to [Lesson 11.5 — Incident response, rollback, and evidence](lesson-5-incident-response-rollback-and-evidence.md), where an alert becomes an incident with a timeline, a containment decision, and a record.
