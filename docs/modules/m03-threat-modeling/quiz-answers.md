# Module 03 Knowledge Check — Answers and Explanations

**QZ-03 · 12 points · Pass 10/12**

Do not read this file before attempting the quiz.

---

## 1. Asset identification — **B** (1 point)

Training labels and override records are assets: they control future model behavior and carry integrity and privacy value. A port number, hostname, and firewall rule are configuration details, not assets in the sense used here. They may be *controls* or *surface attributes*.

## 2. Trust boundaries — **B** (1 point)

A trust boundary is a change in privilege or trust, not a network subnet. Encryption may implement a control at a boundary, but it is not the boundary itself. The input schema is a contract, not a trust change.

## 3. NIST goals — **A, B, C, D** (1 point)

Integrity, availability, privacy, and abuse. Confidentiality is a CIA property, but the NIST adversarial-ML taxonomy groups confidentiality harms under privacy. Fairness is a trustworthiness characteristic in the AI RMF, not an attack goal in this taxonomy.

## 4. Attacker knowledge — **B** (1 point)

Black-box means query access without weights or gradients. "No access at all" is not an attacker. "Weights but not data" is closer to white-box on the model.

## 5. Severity arithmetic — **B** (1 point)

4 × 3 = 12, which falls in the 10–16 high band. Medium is 5–9; critical is 17–25.

## 6. Surfaces and vulnerabilities — **B** (1 point)

The scoring endpoint is a reachable point (surface); accepting unauthenticated requests is a weakness (vulnerability). Option A reverses the two. Options C and D confuse model quality and contractual relationships with the surface/vulnerability distinction.

## 7. ATLAS mapping — **B** (1 point)

`AML.T0020` is Training Data Poisoning. `AML.T0015` is evasion at inference, `AML.T0040` is API access, and `AML.T0051` is LLM prompt injection. Only use IDs you have verified; an empty mapping is acceptable when none fits.

## 8. AI RMF function — **A** (1 point)

Assigning ownership and setting rules is GOVERN. MAP frames the system and risks; MEASURE evaluates them; MANAGE prioritizes and responds. GOVERN runs throughout and is the correct primary function for accountability.

## 9. Find the flaw — **2 points**

A strong answer lists at least four of:

- The **asset** being harmed (labels, model behavior, patient safety).
- The **actor** and their **knowledge** and **capability** (who can change labels, with what authority).
- The **attack surface** and **trust boundary** used.
- The **assumptions** that make the path feasible (for example, no dual approval).
- An **impact statement** naming the harm and who bears it.
- A **likelihood** justification, not just a severity label.
- A **detection hypothesis** and **controls**.
- The **lifecycle stage** and **NIST goal**.

A score of 2 requires four or more substantive elements; 1 point for two or three; 0 for a restatement of the row.

## 10. Scenario — **3 points**

**Scores and bands:**

| Threat | Score | Band |
|---|---:|---|
| T1 | 5 × 4 = 20 | Critical |
| T2 | 5 × 3 = 15 | High |
| T3 | 3 × 4 = 12 | High |

**Ranking:** T1, then T2, then T3.

**Tie-break rule (example):** patient safety first, then privacy, then availability, then financial and reputational harm. It matters even without a tie because it forces the team to agree on what "worse" means before a tie appears. A rule invented after a tie is a preference, not a policy.

**Why T3 still matters:** a lower score is not "ignore." Extraction can trigger contractual, IP, and regulatory consequences that the impact anchor may underweight; it may also be a precursor to other abuse. Record it with an owner and monitor query patterns.

**Scoring:** 1 point for correct scores/bands, 1 for the ranking, 1 for a defensible tie-break plus a reason for T3. A ranking without a stated rule earns at most 2 of 3.

---

## Score interpretation

| Score | Interpretation |
|---:|---|
| 12 | Ready for LAB-02; check that you can apply the same reasoning to a new system |
| 10–11 | Ready; review the item you missed |
| 8–9 | Reread Lessons 3 and 5 before the lab |
| Below 8 | Reread Lessons 1–3 and retake the quiz before the lab |
