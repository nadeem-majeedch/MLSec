---
title: Module 16 Exercises
---

# Module 16 Exercises

**Four exercises · about 45 minutes · one assessment scenario**

All exercises use **Northwind Claims**, a fictional insurer that uses a gradient-boosted model to triage property-damage claims for manual review. The model, the data, and the incidents are synthetic. Do not test a real insurer, a real claims system, or real policyholder data.

---

## Exercise 1 — Audit a scope statement (10 minutes)

The engagement note says:

```text
Project: Northwind Claims model security review
System: the claims triage model
Goal: check the model for security issues
Timeline: two weeks
Environment: production-like
Data: claims records
Out of scope: none
Authorization: requested
```

1. Identify six missing or unusable fields.
2. Rewrite the scope as an eight-field table: system, components, versions, environment, decision, non-goals, constraints, authority.
3. The business decision is whether to expand the model from property claims to auto claims. State two evidence items that decision needs and one that it does not.
4. "Out of scope: none" is a red flag. Give two reasons.
5. Name one asset that a model-only scope would omit, and explain the harm.

---

## Exercise 2 — Turn threats into tests (12 minutes)

The register contains these entries:

| ID | Threat | Asset |
|---|---|---|
| R-01 | A claimant submits duplicate photos of the same damage | Claim evidence |
| R-02 | A body shop inflates estimate text to trigger manual review | Decision |
| R-03 | A stale contractor-fee table skews repair-cost features | Feature store |
| R-04 | A model artifact is replaced without approval | Model |
| R-05 | Reviewer overrides are not recorded | Evidence |
| R-06 | An attacker with physical access photographs the screen | Model IP |

1. For R-01, R-02, R-03, and R-04, write a test case with hypothesis, procedure, budget, oracle, metric and denominator, and evidence.
2. Assign one disposition to R-05 and one to R-06: test, accept, reject, or defer. Justify each in two sentences.
3. Which of your tests is a negative control, and what would a failure reveal?
4. Rewrite R-02 as a falsifiable hypothesis with a numeric success criterion.
5. Identify one test that cannot be run in a local synthetic environment and explain why.

---

## Exercise 3 — Audit the evidence (12 minutes)

A team reports:

> **Result.** The poisoning attack reduced model accuracy from 91% to 84%. We poisoned 2% of the training data. The defense restored accuracy to 90%, so the defense works. We ran one seed because the result was stable. The evaluation used a random 80/20 split. The threshold was chosen after seeing the defense results. The raw outputs are in a screenshot in the appendix.

1. List at least six methodological problems.
2. Which problem most directly prevents reproduction, and why?
3. Rewrite the result as a table row with n, baseline, result, difference, interval, and a note.
4. The claim "the defense works" is unsupported. Write a scoped claim that the evidence could support after the problems are fixed.
5. Name two negative controls this experiment should include.
6. Why is a random split potentially wrong for a claims dataset with multiple claims per policyholder?

---

## Exercise 4 — Severity and remediation (11 minutes)

Findings:

| ID | Finding | Impact | Likelihood | Exposure | Control gap |
|---|---|---|---|---|---|
| F-01 | Duplicate claims inflate recall by 8 points | 4 | 4 | 2 | 3 |
| F-02 | Body-shop text can trigger review without fraud | 3 | 3 | 3 | 3 |
| F-03 | Stale fee table affects 6% of estimates | 3 | 3 | 3 | 2 |
| F-04 | Overrides are unlogged | 2 | 3 | 3 | 3 |
| F-05 | Artifact gate rejects unsigned models | 2 | 1 | 1 | 1 |

Use the rubric from Lesson 16.4: score each dimension 1–4, sum, then map 4–6 Low, 7–9 Medium, 10–12 High, 13–16 Critical.

1. Score all five findings and assign a band.
2. Order remediation by risk reduction per unit of effort, given: deduplication 2 days; text-feature cap 5 days; fee-table freshness monitor 2 days; override logging 1 day; no action for F-05.
3. Which finding would you fix first if the owner has one day? Justify with evidence, not only the band.
4. Write a residual-risk statement for F-01 after deduplication and a data-quality gate.
5. F-05 scores Low. Should it appear in the report? Explain.
6. The owner asks for a single number for "overall risk." Give one sentence explaining why a single number hides the decision.

---

*Compare your work with the [exercise solutions](exercise-solutions.md).*
