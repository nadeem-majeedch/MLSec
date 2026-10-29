# QZ-17B Answer Key — Module 17

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. A — signed authorization

Authorization is the first artifact: it identifies the target, the owner who consented, the time window, the allowed techniques and limits, the stop conditions, and the data-handling rules. Without it, every later action is unauthorized, regardless of how careful the technique is.

- **B** is a plan, not permission.
- **C** is a defender tool, not authorization.
- **D** is model documentation, not consent.

Tag: M17 · LO-34 · Bloom 2 · D1.

## 2. B — recall, base set, query budget, perturbation budget

A red objective states a measurable outcome under stated constraints. "Find weaknesses" and "assess robustness" are activities that cannot fail; any result can be written up as a success.

Tag: M17 · LO-34 · Bloom 2 · D1.

## 3. True

The rules of engagement define the authorized envelope. Staying inside the request, time, and perturbation limits is required even when a larger test would be more informative. If the team believes the envelope is wrong, it stops and renegotiates; it does not expand the test unilaterally.

Tag: M17 · LO-34 · Bloom 2 · D1.

## 4. False

TPR and FPR describe the detector, but precision depends on prevalence. A 1% FPR against a low base rate can produce mostly false alerts even with high recall. The blue team must use the deployment base rate or a stated estimate to compute the analyst queue cost.

Tag: M17 · LO-34 · Bloom 2 · D1.

## 5. Required element

Containment changes the system: logs may rotate, instances may be rebuilt, tokens revoked, and models replaced. If evidence is not captured first, the team cannot establish what happened, validate the detection, or reproduce the finding. Preserve logs, request IDs, hashes, and captured inputs before making changes.

Tag: M17 · LO-34 · Bloom 3 · D2.

## 6. TP = 950; FP = 1,990; alerts = 2,940; precision ≈ 0.323

- Malicious requests: $0.005 \times 200{,}000 = 1{,}000$. True positives: $0.95 \times 1{,}000 = 950$.
- Benign requests: 199,000. False positives: $0.01 \times 199{,}000 = 1{,}990$.
- Alerts: $950 + 1{,}990 = 2{,}940$. Precision: $950/2{,}940 \approx 0.323$, or **32.3%**.

At 20 alerts per hour, 2,940 alerts take about 147 hours of review. Most are false positives, so the queue will bury the analyst unless alerts are aggregated, scored, or enriched before review. A detection that looks strong by TPR alone is expensive at this base rate.

Tag: M17 · LO-34 · Bloom 3 · D2.

## 7. Required elements (two flaws and a corrected design)

Two of:

- **The threshold is not calibrated.** `> 100` per minute is arbitrary; it is not tied to the benign baseline or to account size, so its false-positive rate is unknown.
- **The rule ignores slow-ramp and distributed attacks.** An attacker who stays under 100 per minute, or spreads queries across keys, never triggers it.
- **It is per-request, not per-account or per-tenant.** Extraction is a campaign pattern; the rule has no aggregation window or identity.
- **There is no severity, owner, or response.** An alert with no triage path is not an operational detection.

A corrected design: establish a benign baseline per account, use a sliding window and a threshold set at a stated false-positive budget, combine volume with input-similarity or coverage signals, add a slow-ramp variant, and route alerts with severity and an owner. Then measure false positives on the quiet baseline and recall on the red-team batch.

Tag: M17 · LO-34 · Bloom 4 · D3.

## 8. Required elements (RoE, red objective, blue detection, adaptive retest, residual risk)

Rules of engagement:

- Signed authorization, target and version, owner, time window, allowed techniques, request/time/perturbation budgets, data-handling rules, stop conditions, communications, and an emergency contact.
- Explicit non-goals: no third-party systems, no production data, no denial of service, no social engineering.

Red objective:

- A measurable goal, for example "reduce the target segment's recall by at least 20 percentage points on a frozen 200-row set within 500 queries and an L∞ budget of 8/255," with the baseline and success criterion stated.

Blue detection:

- A rule or monitor tied to an account and a time window, with a threshold calibrated on a quiet baseline.
- Measure false positives on benign traffic, recall on the red batch, and precision at the stated base rate; report the analyst cost.

Adaptive retest:

- Change the attack in a way that targets the control, for example a slower ramp, a second key, or a different input pattern. Report whether the control still holds and what it cost in false positives.

Residual risk:

- The detector can be evaded by a slower or distributed attacker; false positives may be unacceptable at the deployment base rate; logs may be incomplete; the test covers one model and one data distribution. State one with an owner and a monitoring plan.

The exercise stays local and authorized; "we tested the vendor's API" is a safety violation, not a red-team result.

Tag: M17 · LO-34 · Bloom 5 · D3.
