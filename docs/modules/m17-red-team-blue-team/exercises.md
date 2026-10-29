---
title: Exercises — Module 17
---

# Exercises — Module 17

**Four exercises on one scenario · 40 minutes · portfolio evidence**

These exercises use a fictional target so you can practise the artifacts without running a full exercise. RT-01 remains the practical assessment; these are the drills.

## Scenario — Pinewood Logistics dispatch-risk service

Pinewood Logistics operates a local mock service that scores shipment records for dispatch risk. Dispatchers submit a shipment and receive a risk band (`low`, `medium`, `high`) and a recommended action. The mock is used for training; no real shipments or customer data are involved.

```text
Target:     http://127.0.0.1:8090
Routes:     POST /risk      score one shipment (dispatcher key required)
            GET  /health    liveness
            POST /admin/reload  reload model (admin key required)
Data:       synthetic shipments from make_shipments.py, seed 21
Identities: 6 dispatcher keys (d-01…d-06), 1 admin key (a-01)
Quota:      120 decisions per minute per key (documented)
Model:      gradient-boosted classifier, version 3.1, threshold 0.55
Logs:       request, auth, decision, admin, model events; banded features
```

The system owner has asked for a bounded red/blue exercise. The exercises below produce the artifacts the owner needs to approve it.

---

## Exercise 1 — Audit and repair the RoE (10 minutes)

The owner supplied this draft. It has at least five defects.

```text
RULES OF ENGAGEMENT — Pinewood dispatch risk (draft)
1. Authorization: the security team approved this exercise.
2. Target: the dispatch risk service.
3. Non-goals: none.
4. Constraints: do not break anything.
5. Data: use the shipment data.
6. Roles: the team will coordinate.
7. Communications: report at the end.
8. Stop: stop if something goes wrong.
```

**Tasks**

1. List five defects, naming the RoE section each belongs to.
2. Rewrite sections 2, 3, and 8 so they are enumerable and testable.
3. Add one exercise risk that is not a target risk, with a control.

**Deliverable:** `ex1_roe_review.md` with the defect table and the rewritten sections.

**Check:** a reader can list every allowed route and every excluded host without asking a question; the stop section names a trigger, an action, and a decision-maker.

---

## Exercise 2 — Adversary profiles and a variant (10 minutes)

The red team's first session produced this result:

> A-04 (quota): one dispatcher key sent 400 requests in 60 s. The service returned 120 decisions and 280 `429` responses. Detection D-04 alerted after 64 s; containment throttled the key after 7 minutes. The team then used a second dispatcher key and obtained another 120 decisions in the same minute.

**Tasks**

1. Write two adversary profiles: RD-01 (external dispatcher) and RD-02 (insider dispatcher with two keys). Include goal, knowledge, capability, access, budget, and success criterion.
2. Write one adaptive variant hypothesis for the second-key observation. State the objective, the change, the oracle, and the budget.
3. State one thing the variant does **not** prove even if it succeeds.

**Deliverable:** `ex2_profiles.md`.

**Check:** each profile could be handed to a different tester and produce the same test; the variant preserves the original objective and budget class.

---

## Exercise 3 — Calibrate a detection (10 minutes)

The blue team scored a candidate rule, D-05 (repeated near-identical shipment scoring), on 10,000 benign requests and on 25 held-out attack events.

| Threshold (near-dupes / 10 min) | Benign alerts / 10,000 | Attacks detected / 25 |
|---:|---:|---:|
| 5 | 210 | 24 |
| 10 | 85 | 23 |
| 20 | 38 | 20 |
| 40 | 9 | 14 |
| 80 | 1 | 6 |

**Tasks**

1. Compute the false-positive rate at each threshold.
2. The team's budget is 0.5% of benign requests. Which thresholds satisfy it?
3. Choose a threshold and state its recall on the held-out set.
4. Assume malicious requests are 0.1% of traffic. Estimate precision at your chosen threshold over 100,000 requests.
5. State one thing this calculation cannot tell you.

**Deliverable:** `ex3_calibration.md` with the table, the chosen threshold, and the calculation.

**Check:** the FP rate is computed per 10,000 (not per alert), the chosen threshold meets the budget, and the precision calculation states its prevalence assumption.

---

## Exercise 4 — Before/after matrix and residual risk (10 minutes)

The team reran the attacks after three mitigations.

| Attack | Before | After | Variant result |
|---|---|---|---|
| A-02 cross-tenant | cross-tenant decision; D-02 at 0 s; contained 4 min | blocked at validation; D-02 at 0 s | header-tenant variant also blocked |
| A-04 quota | 410 decisions; D-04 at 70 s; contained 9 min | 120 decisions; D-04 at 20 s; contained 3 min | two-key variant: 230 decisions; D-04 at 3 min; contained 5 min |
| A-05 evasion | segment block rate 0.07; not detected | 0.09; D-05 at 35 s; contained 6 min | slow-ramp variant 0.085; D-05 at 2 min; contained 4 min |
| A-06 extraction | surrogate agreement 0.94; not detected | 0.72; D-06 at 3 min; contained 4 min | boundary-only variant 0.79; D-06 at 4 min |

**Tasks**

1. Build the before/after matrix with columns for outcome, detection, containment, and benign cost (state "not measured" where the table gives none).
2. Identify which mitigation generalizes to its variant and which does not.
3. Write a residual-risk statement with the four required parts.
4. Recommend a remediation order and justify the first item by risk reduction per unit cost.

**Deliverable:** `ex4_purple.md`.

**Check:** every claim is tied to a row, the residual statement names the adversary and a number, and the recommendation is ordered.

---

## Submission

Keep the four files in `exercises/` with a short `README.md` naming the seed, the date, and the course module. The [exercise solutions](exercise-solutions.md) contain model answers; attempt all four before reading them.
