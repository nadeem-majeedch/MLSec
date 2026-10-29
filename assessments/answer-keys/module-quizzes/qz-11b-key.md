# QZ-11B Answer Key — Module 11

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. B — 401

An invalid or badly signed token means the caller's identity is not established. Authentication failed, so the response is 401 Unauthorized. A 403 would say the identity is known but lacks permission; a 400 is a malformed request; 429 is rate limiting.

Tag: M11 · LO-22 · Bloom 2 · D1.

## 2. B — it prevents unauthenticated work

Authentication should be the first gate because inference is the expensive resource. Letting anonymous callers reach the model lets them consume CPU, GPU, quota, and logs before any trust decision. Order also affects the status code: an unauthenticated oversized body should be rejected as 401, not processed far enough to return a validation error.

- **A** is false; auth does not improve accuracy.
- **C** is false; validation is still required for authenticated input.
- **D** is false; rate limiting complements authentication.

Tag: M11 · LO-22 · Bloom 2 · D1.

## 3. False

Detailed validation errors can disclose feature names, ranges, model assumptions, and internal implementation details useful to an attacker. External responses should be generic and carry a request ID; detailed diagnostics belong in internal logs with access control. Safety and debuggability are balanced by correlating the ID, not by exposing the schema to every caller.

Tag: M11 · LO-22 · Bloom 2 · D1.

## 4. False

A distributed attack uses many source addresses, each under the per-IP limit. Per-IP limiting raises the cost but does not stop botnets, cloud rotation, or credential stuffing across accounts. Effective controls include per-account and per-token quotas, global limits, behavioral anomaly detection, and authentication hardening.

Tag: M11 · LO-22 · Bloom 2 · D1.

## 5. Required elements (two signals with benign causes)

Any two pairs, such as:

| Signal | Benign cause |
|---|---|
| A burst of low-confidence or near-boundary predictions | A new client integration with poor preprocessing, or a workload shift |
| A jump in out-of-range or malformed feature values | A schema change or a broken upstream pipeline |
| Repeated 4xx validation failures from one account | A misconfigured client or an outdated SDK |
| A sharp change in input distribution | Seasonal traffic, a new population, or a data-source change |
| Many queries with near-duplicate inputs | A batch job or a caching bug |

The point is that each signal needs a benign explanation and a calibrated threshold; a raw spike is not an attack finding.

Tag: M11 · LO-23 · Bloom 3 · D2.

## 6. 60 requests allowed; fixed-window boundary burst

The first 30 arrive in the 12:00 window and the second 30 in the 12:01 window, so both sets are within their respective limits. Across the two-second span the client gets 60 requests, double the intended per-minute rate.

This is the fixed-window boundary problem: the counter resets on a clock edge, so a client can burst on both sides. Alternatives include a sliding-window log, a sliding-window counter, or a token bucket, each of which smooths the boundary at the cost of more state or different burst behavior.

Tag: M11 · LO-22 · Bloom 3 · D2.

## 7. Required elements (two flaws and why not resolved)

Two of:

- **The rollback criterion is clean accuracy, not attack success.** A model can keep 95% clean accuracy and still be fully evaded. The decision needs a replay of the captured attack batch on current and previous checkpoints, with an explicit threshold.
- **Evidence is not preserved before restoration.** Restoring overwrites or replaces the artifact and may destroy the state needed to explain what happened. Logs, request IDs, checkpoint hashes, and captured inputs must be secured first.
- **"Incident resolved" is declared without verification.** Recovery requires post-rollback monitoring, a clean-accuracy check, and confirmation that the attack no longer succeeds; a restore command is not a closure.
- **No owner, timeline, or communication.** The code has no accountability for the decision or the follow-up.

The incident should stay open until the evidence is preserved, the rollback is validated against the attack, the root cause is identified, and monitoring shows the service is stable. Closing on a single accuracy check hides residual risk.

Tag: M11 · LO-23 · Bloom 4 · D3.

## 8. Required elements (containment, evidence, rollback criterion, residual risk)

A bounded outline:

1. **Validate and scope.** Confirm the alert on the local service; identify the token, time window, endpoints, and model version. Do not touch third-party systems.
2. **Preserve evidence before changing state.** Capture logs, request IDs, token metadata, input batches, model and checkpoint hashes, and deployment configuration in a write-once location. Record who collected what and when.
3. **Contain.** Revoke or suspend the token, apply a tight quota or block at the gateway, isolate the affected instance, and disable the abused endpoint if necessary. Keep the service available to legitimate users where possible.
4. **Assess.** Replay the captured batch on the current and previous checkpoints. Measure attack success and clean accuracy on both. Check whether the inputs indicate evasion, extraction, or abuse, and whether the model or data were altered.
5. **Eradicate and recover.** Fix the validation or quota gap, rotate credentials, and restore the previous checkpoint only if the replay shows attack success below the stated threshold and clean accuracy remains acceptable. State the criterion numerically (for example, previous attack success < 0.5 × current and clean accuracy within 1 point of the approved baseline).
6. **Verify and close.** Monitor for recurrence, confirm the fix with the same replay, document the timeline, and assign follow-up actions with owners.

One residual risk: the attacker may hold other valid tokens or have already extracted information; logs may be incomplete; the previous checkpoint may also be affected; or the fix may not cover a different input pattern. State it with an owner and a monitoring plan.

"Roll back and close" is not an incident response: without preserved evidence and a measured rollback criterion, the team cannot tell recovery from concealment.

Tag: M11 · LO-23 · Bloom 5 · D3.
