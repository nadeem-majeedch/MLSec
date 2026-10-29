# Lesson 17.3 — Blue-Team Detection and Response

<a id="m17-l3"></a>

**Module 17 · Lesson 3 of 4 · 1 hour · LO-23, LO-34**

## Scenario

A blue team is asked to detect the attacks from last week's exercise. It reads the attack log, writes five rules that match those events, and reruns them. All five attacks are detected. The report says "100% detection, zero false positives."

Both numbers are artifacts of the method. The rules were fitted to the events they were scored on, and the only traffic in the test set was attack traffic. A detector that alerts on everything would also have scored 100%.

A real detection measurement needs three things this exercise skipped: quiet baseline traffic to estimate false positives, a rule written from a hypothesis rather than from the answer key, and a held-out set of attack events the rule was not tuned on.

## Objectives

By the end of this lesson you will be able to:

1. Specify telemetry for an ML service that supports detection without storing secrets or personal data.
2. Write detection hypotheses that connect a signal to an attack family and a response.
3. Calibrate thresholds against quiet baseline traffic at a stated false-positive budget.
4. Run a response from triage through containment, eradication, recovery, and verification.
5. Measure time to detect and time to contain with defined start and end points.

## 1. What the blue team owns

| Artifact | Purpose | Owner |
|---|---|---|
| Telemetry schema | What is logged, at what granularity, with what retention | Blue team with platform |
| Quiet baseline | Benign traffic distribution for calibration | Blue team, before attacks |
| Detection hypotheses | Signal → attack family → response | Blue team |
| Rule set with thresholds | Executable detection logic | Blue team |
| Triage guide | Severity, ownership, escalation | Blue team |
| Response runbook | Containment, eradication, recovery, verification | Blue team with system owner |
| Detection metrics | Precision, recall, time to detect, time to contain | Blue team |
| Evidence of response | Timeline, actions, logs | Blue team |

The blue team does not need the red team's plan. It needs the system's normal behavior and a hypothesis about how an attack would look.

## 2. Telemetry design

Log events, not prose. One JSON object per event, appended, with a stable schema.

```json
{
  "ts": "2026-10-28T09:14:03.221Z",
  "event": "decision",
  "request_id": "req-7f3a",
  "actor": {"key_id": "key-12", "tenant_id": "t-04"},
  "route": "/score",
  "status": 200,
  "latency_ms": 41,
  "decision": {"label": "block", "score_bucket": "0.80-0.90"},
  "features": {"amount_band": "B3", "hour_band": "H22", "velocity_band": "V1"},
  "flags": []
}
```

| Event type | Required fields | Do not log |
|---|---|---|
| `auth` | key_id (hashed), tenant, result, reason code | Raw key, token |
| `request` | route, method, status, size, latency, request_id | Full body with personal data |
| `decision` | label, score bucket, model version, threshold version | Raw score if it enables extraction |
| `feature` | banded or hashed feature summary, out-of-range flags | Exact values that identify a person |
| `admin` | actor, action, target, result | Credentials |
| `model` | version, artifact hash, promotion event | Weights |
| `data` | batch ID, row count, validation result, hash | Row contents |

### Banding is a control

Exact feature values in logs help an attacker who can read logs and help a regulator who wants minimization. Band them (`B3`, `H22`) and keep exact values only where a response requires them, with a retention limit. The detection question is usually "did the value leave the normal band," not "what was the value."

### What detection needs that logging usually lacks

- a **request ID** shared by request, decision, and error events;
- an **actor identifier** that is stable per key and per tenant;
- a **decision** and the model/threshold version that produced it;
- **status and latency**, so availability attacks are visible;
- **out-of-range flags** computed at the boundary, not reconstructed later.

If these are missing, add them before the exercise. Detection cannot be bolted on after the fact without changing what the service records.

## 3. Detection hypotheses

A detection hypothesis has the same shape as an attack hypothesis, read from the other side.

| Field | Question |
|---|---|
| ID | Which detection is this? |
| Attack family | What behavior does it target? |
| Signal | Which logged fields carry the evidence? |
| Rule | What predicate fires? |
| Threshold | What value separates attack from benign? |
| Baseline expectation | How often does benign traffic fire? |
| Response | What should an analyst do when it fires? |
| False-positive risk | Which legitimate behavior could trigger it? |

### Seven hypotheses for RT-01

| ID | Attack family | Signal and rule | Response |
|---|---|---|---|
| D-01 | Auth probing (A-01) | ≥ 5 `auth` failures from one key_id or source in 60 s | Rate-limit source; review keys |
| D-02 | Cross-tenant access (A-02) | Any request where body tenant ≠ authenticated tenant | Block request; page owner; audit key |
| D-03 | Malformed input (A-03) | ≥ 3 validation failures from one key in 5 min, or one payload over limit | Block key briefly; review payload class |
| D-04 | Quota abuse (A-04) | Requests per key per minute > 2× documented quota | Throttle; notify tenant |
| D-05 | Evasion probing (A-05) | Repeated decisions for near-identical records with feature deltas ≤ 1 band, ≥ 20 in 10 min | Flag for review; sample records |
| D-06 | Extraction querying (A-06) | High query volume with boundary-adjacent features and low feature diversity | Throttle; require justification |
| D-07 | Unauthorized admin (A-07) | `admin` event with result=denied, or success without admin role | Page on-call; freeze admin path |

D-02 and D-07 are deterministic: a single event is enough. D-01, D-03, D-04, D-05, and D-06 are statistical: they need a threshold and a baseline.

## 4. Baseline before threshold

A threshold without a baseline is a guess. Build quiet traffic first.

### Designing the quiet baseline

| Property | Requirement | RT-01 example |
|---|---|---|
| Volume | Comparable to the attack window | 2,000 benign requests over 4 hours |
| Mix | Representative routes and outcomes | 90% `/score`, 8% `/health`, 2% admin reads |
| Actors | Several keys and tenants | 20 keys across 4 tenants |
| Feature distribution | Matches the evaluation set | Sampled from the frozen eval set |
| Label mix | Realistic block rate | 6% block, matching the mock's calibration |
| Timing | Realistic inter-arrival | Poisson, mean 7 s, with a business-hours peak |
| Noise | Includes legitimate oddities | Retries, duplicate submissions, a bulk upload |

Generate it with a script and a seed, and hash the output. The quiet baseline is an artifact like any other.

### Calibrating a threshold

Pick a false-positive budget first, then choose the threshold that meets it.

| Step | Action | Output |
|---|---|---|
| 1 | Score every quiet-baseline event with the candidate rule | Benign alert count |
| 2 | Compute alerts per 1,000 requests at each threshold | FP curve |
| 3 | Choose the strictest threshold at or below the FP budget | Threshold |
| 4 | Measure alert volume per day at that threshold | Analyst load |
| 5 | Freeze the rule and threshold before seeing attack events | Signed config |

Example, for D-05 (near-duplicate probing):

| Threshold (near-dupes per 10 min) | Benign alerts / 1,000 req | Alerts/day | Decision |
|---:|---:|---:|---|
| 10 | 14.2 | ~340 | Too noisy |
| 20 | 3.1 | ~74 | At budget (0.5%) |
| 40 | 0.4 | ~10 | Below budget, higher miss risk |
| 80 | 0.0 | ~0 | Silent; untestable |

The numbers above are illustrative for the mock, not measured results. In your exercise, compute them from your own baseline and report the curve.

### The base-rate problem

Attacks are rare. If 0.1% of requests are malicious and a detector has 1% false positives, then among alerts, benign events outnumber attacks roughly 10:1 even with perfect recall. Precision depends on prevalence, not only on the rule.

Consequences:

- report precision **at the prevalence you assume**, and state the assumption;
- prefer rules with very low false-positive rates for high-volume signals;
- use deterministic rules (D-02, D-07) where the event itself is the evidence;
- do not promise "zero false positives" from a small baseline; report the observed count and its uncertainty.

## 5. Writing the rule

Start with the simplest rule that tests the hypothesis.

| Complexity | Example | When to use |
|---|---|---|
| Deterministic | body tenant ≠ auth tenant | The invariant is exact |
| Threshold | ≥ 5 auth failures / 60 s / key | Rate-based behavior |
| Ratio | near-duplicate decisions / total decisions > 0.6 | Composition, not volume |
| Sequence | auth failure → success → admin within 60 s | Multi-stage behavior |
| Model-based | anomaly score on banded features | Last resort; harder to explain |

Prefer the top of the table. A rule an analyst can explain in one sentence is easier to tune, defend, and retire.

### Hold out attack events

Split the red-team events into a **tuning set** and a **test set** before writing rules. Tune on the first; report on the second. If you cannot split because the attack set is small, say so and report the result as in-sample.

| Split | Use | Reported as |
|---|---|---|
| Tuning | Choose rule and threshold | Development result |
| Test | Measure precision and recall | Headline result |
| Adaptive | Variant designed after the rule | Robustness check (Lesson 17.4) |

## 6. Triage and response

Detection without response is a log entry. Write the runbook before the exercise.

| Phase | Question | RT-01 action | Time bound |
|---|---|---|---|
| Triage | Is the alert real, and how bad? | Check request IDs, actor, scope; assign severity | 15 min |
| Containment | How do we stop the effect? | Revoke key; throttle source; disable admin path | 30 min |
| Eradication | What caused it? | Identify the defect; patch or reconfigure | 2 h |
| Recovery | How do we restore service? | Re-enable path; roll back model if needed; verify | 1 h |
| Verification | Is the fix effective? | Replay the attack; check benign traffic | 30 min |
| Learning | What changes? | Update rule, runbook, or design | Next session |

### Severity for exercise purposes

Use the same four-dimension rubric as Module 16 (exploitability, impact, exposure, detectability), but add one exercise-specific question: **was it detected?**

| Situation | Severity adjustment |
|---|---|
| Detected and contained within bounds | Report as detected; severity from impact |
| Detected but not contained | Escalate one level |
| Not detected, contained by luck | Escalate one level; fix detection |
| Not detected, not contained | Highest severity in its impact band |

### Containment options, cheapest first

1. Throttle the actor (rate limit, temporary block).
2. Revoke the credential.
3. Disable the route or the admin path.
4. Roll back the model or threshold.
5. Take the service offline (last resort; record why).

Each option has a benign-traffic cost. Measure it: after containment, replay a slice of the quiet baseline and confirm benign users are not blocked. A containment that stops the attack by stopping all traffic is an availability incident.

## 7. Measuring detection and response

Define the clocks before the exercise; otherwise every team measures from a different start.

| Metric | Start | End | Notes |
|---|---|---|---|
| Time to detect (TTD) | First attack request | First correct alert | Not the first alert of any kind |
| Time to triage | First correct alert | Severity assigned and owner named | |
| Time to contain (TTC) | First correct alert | Attack effect stopped | Not when the ticket was opened |
| Time to recover (TTR) | Containment | Benign traffic verified normal | |
| Precision | — | TP / (TP + FP) at stated prevalence | Report the prevalence |
| Recall | — | Detected attacks / attacks in test set | Report the test set size |

### Detection coverage matrix

| Attack | Detected? | Rule | TTD | Contained? | TTC | Benign cost |
|---|---|---|---|---|---|---|
| A-01 | | D-01 | | | | |
| A-02 | | D-02 | | | | |
| … | | | | | | |

An empty cell is a finding. "No detection hypothesis exists for this attack family" is more useful than a fabricated rule.

## 8. Worked example — blue-team plan

```text
BLUE PLAN (frozen before red plan is read)
Telemetry: request, auth, decision, admin, model events; banded features;
           key_id hashed; retention 14 days.
Baseline:  2,000 benign requests, seed 11, 20 keys, 4 tenants; hash 9c1e…
Rules:     D-01 auth failures ≥5/60s/key
           D-02 body tenant ≠ auth tenant (deterministic)
           D-03 ≥3 validation failures/5min/key or payload > limit
           D-04 >2× quota/min/key
           D-05 ≥20 near-duplicate decisions/10min/key
           D-06 query volume > 500/h with feature diversity < 0.2
           D-07 admin denied, or success without admin role (deterministic)
FP budget: ≤ 0.5% of benign requests per rule; measured on baseline.
Response:  triage 15 min; contain 30 min; recover 1 h; verify 30 min.
Evidence:  alerts.jsonl, timeline.md, containment log, benign replay.
Limitations: small baseline; no real identity provider; no network telemetry.
```

The plan is frozen before the red plan is opened. That sentence is the difference between a measurement and a story.

## 9. Detection theater

| Anti-pattern | Why it looks good | Fix |
|---|---|---|
| Rule fitted to the scored events | Perfect recall | Hold out attack events |
| No benign traffic | Zero false positives | Build a quiet baseline |
| Alert on every 4xx | Catches all malformed input | Measure precision; benign clients send 4xx |
| Threshold chosen after results | Best of both worlds | Freeze threshold before scoring |
| "Detected" means a log exists | Coverage looks complete | Require a correct alert and a response |
| Containment untested | Runbook is prose | Execute containment and verify benign traffic |
| One combined score | Simple to report | Report precision, recall, TTD, TTC separately |
| No limitations | Confident report | State baseline size, prevalence, and missing telemetry |

## 10. Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Logging bodies with personal data | Privacy incident | Band or hash; log metadata |
| Logging raw API keys | Credential leak | Hash key IDs |
| No request ID | Events cannot be joined | Add a correlation ID |
| Threshold without baseline | Arbitrary alerts | Calibrate at a stated FP budget |
| Tuning on test attacks | Inflated recall | Tune/test split |
| Ignoring prevalence | Precision overestimated | Report precision at assumed prevalence |
| Containment blocks all traffic | Availability incident | Measure benign replay after containment |
| Clocks undefined | TTD not comparable | Define start and end per metric |
| No coverage matrix | Gaps invisible | One row per attack family |
| Response never rehearsed | Playbook fails live | Execute it in the exercise |

## 11. Check your understanding

1. Why is 100% detection with zero false positives suspicious in a small exercise?
2. Name five event types and one field each that detection needs.
3. What is the base-rate problem, and how does it affect the precision you report?
4. How do you choose a threshold at a false-positive budget?
5. What is the difference between time to detect and time to triage?
6. Why must containment be followed by a benign-traffic replay?

## 12. What you keep

A telemetry schema, seven detection hypotheses, a quiet baseline with a hash, a calibrated threshold table, a frozen rule set, a response runbook with time bounds, a coverage matrix, and detection metrics with stated denominators. Lesson 17.4 merges this with the red-team evidence.

## 13. Next

Lesson 17.4 covers the purple-team review: merging timelines, before/after comparison, adaptive variants, and a residual-risk statement that survives scrutiny.
