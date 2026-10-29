# Exercise Solutions — Module 17

**Evaluator reference.** These are model answers for the four Pinewood exercises. They are not the only acceptable answers; score the reasoning and the evidence, not the wording.

---

## Exercise 1 — Audit and repair the RoE

### Defects (any five)

| # | Section | Defect | Consequence |
|---|---|---|---|
| 1 | Authorization | "The security team approved" names no person, role, date, or duration | No accountable authorization; exercise cannot be defended later |
| 2 | Target | "The dispatch risk service" is not enumerable | Tester and owner disagree about what is in scope |
| 3 | Non-goals | "None" | Any out-of-scope discovery becomes an excuse to continue |
| 4 | Constraints | "Do not break anything" has no budget or definition | No request, time, concurrency, or perturbation limit |
| 5 | Data | "The shipment data" does not say synthetic, seed, or handling | Risk of real data and of unreproducible records |
| 6 | Roles | "The team will coordinate" has no separation | Blue may see the red plan; detection result is meaningless |
| 7 | Communications | "Report at the end" has no channel or escalation | Out-of-scope access is not reported promptly |
| 8 | Stop | "If something goes wrong" has no trigger, action, or authority | Nobody can decide to stop |

### Rewritten sections

```text
2. Target: http://127.0.0.1:8090 only; POST /risk, GET /health,
   POST /admin/reload; synthetic shipments from make_shipments.py seed 21;
   dispatcher keys d-01…d-06 and admin key a-01; window 2026-10-28 to
   2026-11-02.

3. Non-goals: any host or port other than 127.0.0.1:8090; the host
   filesystem outside exercises/pinewood/; the OS, interpreter, and
   network stack; denial of service beyond 20 concurrent requests; social
   engineering; real shipment, customer, or employee data; any admin
   action other than /admin/reload with a-01.

8. Stop conditions:
   - any request would leave 127.0.0.1 -> abort, record URL -> lead
   - host CPU/memory > 90% for 60 s -> stop load -> lead
   - access to host files or environment variables -> stop, preserve -> lead
   - real data discovered -> stop, quarantine, delete -> lead + data owner
   - 150% of time or request budget -> stop, record partial -> lead
   Only the exercise lead may stop or resume.
```

### Exercise risk (example)

| ID | Risk | Control |
|---|---|---|
| X-01 | Quiet baseline is generated after the red plan is read, so it contains attack-like traffic | Generate and hash the baseline before reading the red plan; record the order |

Other acceptable answers: contaminated synthetic data, host instability, scope creep into `/admin/reload` without the admin key, results not reproducible.

---

## Exercise 2 — Adversary profiles and a variant

### RD-01 — External dispatcher

```text
Goal:       Integrity — obtain a low-risk recommendation for shipments
            that should be high risk, or obtain a decision for a shipment
            outside the dispatcher's assigned lane.
Knowledge:  /risk schema and documented quota; no weights, thresholds,
            source, or training data.
Capability: Submit shipments; choose feature values within observed
            ranges; hold one dispatcher key.
Access:     POST /risk through the mock API; logs not visible.
Budget:     600 requests; 2 hours; ≤ 3 feature changes per record;
            values within the 1st–99th percentile.
Success:    Target-lane high-risk rate < 0.10 at global false-high ≤ 0.02,
            or a decision for an out-of-lane shipment.
Out of scope: host compromise, admin key theft, network attacks.
```

### RD-02 — Insider dispatcher with two keys

```text
Goal:       Availability/integrity — exceed the documented per-key quota
            without triggering 429s, and sustain the higher volume.
Knowledge:  Documented quota, shift patterns, and the fact that keys are
            issued per dispatcher; no source access.
Capability: Hold two valid dispatcher keys; pace requests; choose timing.
Access:     /risk and /health from the internal network mock.
Budget:     1,200 requests; 2 hours; two keys; ≤ 240 requests/min total.
Success:    More than 120 decisions per minute at tenant level with no
            429 for either key.
Out of scope: creating keys outside /keys, admin actions, code changes.
```

### Variant V-01

```text
Objective:  Same as RD-02: exceed the tenant-level decision rate.
Change:     One dimension — two keys at 60 requests/min each for 10 min,
            instead of one key at 400 requests/min for 60 s.
Oracle:     Tenant decisions > 120/min, or D-04 silent while tenant volume
            exceeds 2× quota.
Budget:     1,200 requests; 10 minutes; 2 keys; ≤ 20 concurrent.
```

### What success would not prove

That a production tenant-level control is absent, or that an attacker with many keys and a longer ramp would also succeed. It shows that the tested per-key control and per-key detection do not aggregate across two credentials within this budget. The claim is bounded by the two-key, ten-minute design.

---

## Exercise 3 — Calibration

### False-positive rates

| Threshold | Benign alerts / 10,000 | FP rate | Meets 0.5%? | Recall (held-out) |
|---:|---:|---:|---|---:|
| 5 | 210 | 2.10% | No | 96% |
| 10 | 85 | 0.85% | No | 92% |
| 20 | 38 | 0.38% | Yes | 80% |
| 40 | 9 | 0.09% | Yes | 56% |
| 80 | 1 | 0.01% | Yes | 24% |

### Choice

Two defensible choices:

- **T = 20:** highest recall that meets the budget (20/25 = 0.80).
- **T = 40:** lower recall (14/25 = 0.56) but far fewer alerts (0.09%), which may be right if analyst capacity is the constraint.

A model answer states the choice and the reason. Choosing T = 10 because it has better recall ignores the budget; choosing T = 80 because it is quiet ignores the missed attacks.

### Precision at 0.1% prevalence, 100,000 requests

For **T = 20**:

- attacks: 100; TP = 100 × 0.80 = 80;
- benign: 99,900; FP = 99,900 × 0.0038 = 380 (approximately);
- alerts: 460; precision = 80 / 460 ≈ **17.4%**.

For **T = 40**:

- TP = 100 × 0.56 = 56;
- FP = 99,900 × 0.0009 ≈ 90;
- precision = 56 / 146 ≈ **38.4%**.

So the quieter rule has better precision but detects 24 fewer attacks per 100,000 requests. The trade-off is the answer, not a single number.

### What the calculation cannot tell you

Any of:

- whether 0.1% is the real prevalence (it was assumed);
- whether 25 held-out attacks represent the attack population (small denominator, narrow family);
- whether the rule survives an adaptive variant that paces below the threshold;
- the per-day analyst load, which depends on traffic volume, not only rate;
- the uncertainty of the FP estimate from a 10,000-request baseline.

---

## Exercise 4 — Before/after matrix and residual risk

### Matrix

| Attack | Before: outcome | Before: detection | Before: containment | After: outcome | After: detection | After: containment | Benign cost |
|---|---|---|---|---|---|---|---|
| A-02 | cross-tenant decision | D-02, 0 s | 4 min | blocked at validation | D-02, 0 s | n/a | not measured |
| A-04 | 410 decisions | D-04, 70 s | 9 min | 120 decisions | D-04, 20 s | 3 min | not measured |
| A-05 | segment 0.07 | none | — | segment 0.09 | D-05, 35 s | 6 min | not measured |
| A-06 | agreement 0.94 | none | — | agreement 0.72 | D-06, 3 min | 4 min | not measured |

"Not measured" is itself a finding: the exercise cannot say what the controls cost legitimate dispatchers. That belongs in the limitations and in the next exercise's plan.

### Generalization

- **M-01 validation generalizes** across the body and header paths: the variant is blocked by the same control.
- **M-02 per-key quota does not generalize:** the two-key variant obtains 230 decisions, nearly double the per-key limit, and D-04 fires only after 3 minutes. The control is per credential; the attacker's unit is the actor.
- **M-05 detection generalizes in detection but not in prevention:** the slow-ramp variant is still detected (2 min), but the segment block rate remains 0.085 and containment takes 4 minutes.
- **M-06 output bucketing reduces but does not prevent extraction:** agreement falls from 0.94 to 0.72, and the boundary-only variant recovers to 0.79.

### Residual-risk statement

```text
Under RD-02 (two dispatcher keys, 1,200 requests, 2 hours), after M-01
validation, M-02 per-key quota, M-05 near-duplicate detection, and M-06
output bucketing, a two-key slow-ramp variant still obtains 230 decisions
in a 10-minute window (documented tenant quota: 120/min), with detection
at 3 minutes and containment at 5. Under RD-01, the evasion variant still
lowers the target segment block rate to 0.085, and the extraction variant
still reaches 0.79 surrogate agreement. These residual risks are accepted
for the exercise; a production deployment would need tenant-level
cumulative quotas, faster containment, and query-diversity limits.
```

Accept a statement with the same four parts even if the wording or the chosen numbers differ; the numbers must come from the table.

### Remediation order

1. **Tenant-level cumulative quota.** It closes the two-key bypass, needs no model change, and its cost is configuration plus a counter. Largest residual reduction per unit cost.
2. **Faster containment for D-05** (pre-approved automatic throttle at alert) because the evasion variant remains effective for 4–6 minutes.
3. **Query-diversity limit plus bucketing** for extraction; bucketing alone leaves 0.79 agreement.
4. **Measure benign cost** of M-05 and M-06 before production; without it, items 2 and 3 cannot be justified.

A different order is acceptable if the justification uses risk reduction, benign cost, and operational effort.
