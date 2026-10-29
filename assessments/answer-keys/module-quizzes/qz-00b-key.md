# QZ-00B Answer Key — Module 00

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. C — data-quality and operational failure

The unit change is a schema and pipeline failure. There is no adversary, no manipulation of training data, and no extraction. It is still a security-relevant failure because integrity controls should have caught it, but calling it an attack would misstate the threat.

- **A** requires an adversary perturbing inference inputs.
- **B** requires corrupted training data or training process.
- **D** requires an adversary copying model behavior through queries.

Tag: M00 · LO-01 · Bloom 3 · D2.

## 2. B — independently verify controls and evidence

The auditor's value is independence: checking that the control exists, that it operates, and that the evidence supports the claim. The auditor does not have to exploit the system, approve deployment, or write the model.

- **A** is a red-team or penetration-test task.
- **C** is an owner or authorizer decision.
- **D** is an engineering task and creates a conflict with independent review.

Tag: M00 · LO-01 · Bloom 2 · D1.

## 3. False

A hash mismatch proves only that the bytes differ from the version recorded in the manifest. That can indicate tampering, but it can also indicate corruption, a rebuild, a partial download, or a manifest generated from the wrong file. Malice requires additional evidence: who changed it, when, with what access, and whether the new artifact behaves differently.

Tag: M00 · LO-01 · Bloom 2 · D1.

## 4. True

Authorization is about the target, not the technology. If the exercise authorizes a local replica that you built, testing it is in scope. The original service remains out of scope. Do not let a replica result become a claim about the production system, and do not test the production system to "confirm" the replica.

Tag: M00 · LO-29 · Bloom 2 · D1.

## 5. Required elements (two)

Award the point for two of:

- A negative result is only meaningful with a stated threat model, budget, base set, and attack strength; an underpowered attack proves little.
- One attack family does not cover other families, data sources, or adaptive adversaries.
- Absence of evidence is not evidence of absence; the correct report is "no success observed at this budget," not "secure."
- There is no upper bound or interval on the failure rate, so a small test cannot rule out a rare but important failure.

Tag: M00 · LO-01 · Bloom 4 · D3.

## 6. Mean 0.230; range 0.050

Mean: $(0.20 + 0.25 + 0.24) / 3 = 0.69 / 3 = 0.230$.

Range: $0.25 - 0.20 = 0.050$.

A three-seed mean is a description, not a confidence interval. With three values, report the individual seeds as well.

Tag: M00 · LO-28 · Bloom 2 · D1.

## 7. Required elements (two flaws with effects)

- **Post-hoc budget selection:** changing the perturbation budget until the curve looks strong turns the experiment into a search for a favorable result. The reported success rate is then the maximum over an undeclared set of budgets, not the success rate at a predeclared budget.
- **Reporting the best run:** selecting the best of several runs and omitting the others inflates the headline and hides variance. Report all seeds or a predeclared aggregation.
- Also acceptable: no baseline, no confidence interval, and no stated threat model.

Tag: M00 · LO-28 · Bloom 3 · D2.

## 8. Required elements

- **Immediate action:** stop testing the real service. The local finding does not authorize production testing.
- **Evidence:** keep the local request and response, timestamps, the minimal reproducer, the model or mock version, and a hash of the artifacts. Do not include secrets or real user data.
- **Disclosure:** notify the course owner and the vendor through a private channel; follow the vendor's coordinated-disclosure process; do not publish an exploit or a step-by-step reproduction before a fix or an agreed deadline.
- Also acceptable: document that the production behavior is inferred, not confirmed; state the limits of the local replica.

A response that says "report it publicly so users know" without a disclosure process is not sufficient. A response that tests the production API "just to confirm" is a safety failure.

Tag: M00 · LO-29 · Bloom 4 · D3.
