# Answer Key — QZ-17

**Module 17 · 15 points**

The model answers below are fuller than a passing response needs. Award partial credit for correct reasoning even when a term differs.

---

**1. (1 point) — B. Non-goals.**

Most RoE templates list the target and the authorization, because those are the visible parts of scope. Non-goals are omitted because they require thinking about what the exercise could drift into. Without them, "the scoring API" expands to whatever the tester can reach, out-of-scope components get touched, and the report's claims no longer match the authorization. Communications and data handling are also frequently thin, but the non-goals omission is the one that produces unsafe tests. Accept A, C, or D with a correct consequence.

---

**2. (1 point)**

Problems (any two):

- "The scoring API" does not name a host, port, route, method, or version, so the tester and the evaluator can disagree about what is in scope.
- "Everything else" is not a non-goal list; it does not identify the specific excluded systems (host filesystem, other ports, network egress, other tenants, real data).
- No data scope: which records may be used, and whether they are synthetic.
- No time window or activity limits.

Rewrite, for example: "In scope: `POST http://127.0.0.1:8080/score`, `GET /health`, and `POST /admin/rollback` on the local mock, using synthetic records from `make_data.py` seed 7, 2026-10-28 to 2026-11-04." The rewrite must be enumerable; exact wording may differ.

---

**3. (1 point)**

Any answer with all three elements:

- **Access assumption:** an authenticated requester with one valid synthetic key and no source, weights, or training-data access.
- **Budget:** e.g., 2,000 requests, 4 hours, at most 3 feature changes per record within observed percentiles.
- **Measurable success:** e.g., a cross-tenant decision, or target-segment block rate below 0.10 at global false-decline ≤ 0.02.

"Test the model for weaknesses" fails because it has no adversary, no bound, and no oracle.

---

**4. (2 points)**

What should happen: the extraction test may run only if it fits within the remaining 350 requests, or the team must stop and record the test as not run at budget. It must not silently borrow from the request budget or exceed 2,000. If the lead authorizes a budget change, it is a logged scope change, not an improvisation.

The report must state:

1. the budget actually available to the test (350 requests), and that the original 500-request hypothesis was **not** tested at its planned budget;
2. the result as "inconclusive at budget" or "not run," not "extraction failed."

A finding from an under-budget test is weaker, and the reader needs the number to interpret it.

---

**5. (2 points)**

- Observed false-positive rate: 40 / 10,000 = **0.004**, or 0.4% of benign requests.
- Observed detection: 18 / 20 = **90%** on the test split.
- Precision **cannot** be concluded from these numbers because the prevalence of attacks in real traffic is not known. The test split is enriched with attacks (20 attacks among a small set), while the baseline is almost all benign. Precision depends on prevalence.
- Also: 20 attacks is a small denominator, so the recall estimate has a wide interval; and if the rule was tuned on some of the same events, the figure is in-sample.

A full-credit answer reports the FP rate and detection rate with denominators and states that precision requires an assumed prevalence.

---

**6. (2 points)**

- Attacks: 100,000 × 0.002 = **200**.
- True positives: 200 × 0.90 = **180**.
- Benign: 99,800. False positives: 99,800 × 0.005 = **499**.
- Alerts: 180 + 499 = **679**.
- Precision: 180 / 679 ≈ **0.265**, or about **26.5%**.

Implication: roughly three of every four alerts are false, so the analyst queue is dominated by benign events even with 90% recall. Reducing the false-positive rate, enriching alerts with additional signals, or automating triage matters more than a small recall gain. State the prevalence assumption with the result.

---

**7. (2 points)**

Problem: changing the seed of the same script is not an adaptive variant. It tests run-to-run variance, not whether the control generalizes to a different attack strategy. A control can block every seed and fail against a different path.

Stronger variants (any two):

- **Identity:** use two keys or two tenants to test whether the control is per-credential or per-actor.
- **Timing:** pace requests below the rate threshold for longer, testing whether the rule uses a window an attacker can avoid.
- **Payload:** move the manipulated field from the body to a header or query parameter, testing whether validation covers all input paths.
- **Objective-preserving change:** use a different feature combination or search strategy within the same perturbation budget.

Each variant keeps the same objective and budget class and is declared with its oracle before running.

---

**8. (1 point)**

- **Time to detect:** from the **first attack request** to the **first correct alert** for that activity. It ends at a correct alert, not at any alert; an unrelated noisy rule firing earlier does not count.
- **Time to triage:** from the **first correct alert** to the moment an analyst assigns a severity and names an owner.

Using the first alert of any kind as the end point understates detection time when an unrelated rule fires early, and overstates it when a correct alert is buried under noise. The metric must attach to the attack being measured.

---

**9. (2 points)**

- **Gap:** the quota control and the detection both key on the credential, while the attacker's unit of action is the actor or tenant. Two keys look like two compliant clients, so neither control sees the aggregate volume.
- **Artifact:** the merged purple-team timeline with a before/after matrix; correlating both keys to tenant `t-04` exposes the aggregate that neither single-team report contains. The gap analysis records that the detection rule's grouping key differs from the control's unit.
- **Control:** a tenant-level or actor-level cumulative quota (and a detection rule that aggregates by tenant/actor, not only by key), plus linking multiple credentials held by the same actor.

A full-credit answer names the grouping mismatch, not just "better monitoring."

---

**10. (1 point) — C.**

C states the adversary, the budget, the remaining measured effect, and the recommended but unimplemented control. A and D assert a level without a number or an adversary. B generalizes from a bounded test to a security claim the test cannot support.

---

## Scoring

| Score | Interpretation |
|---:|---|
| 13–15 | Ready for RT-01; review any missed item before starting |
| 10–12 | Adequate; reread Lessons 17.3–17.4 for the detection and synthesis items missed |
| 6–9 | Reread Lessons 17.1–17.2 and redo the scope and budget items before running the exercise |
| 0–5 | Read the module in order; the exercise depends on the RoE and budget discipline |

Item 6 is the most common failure. If the arithmetic was right but the implication was missing, count it half.
