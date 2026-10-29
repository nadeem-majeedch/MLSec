---
title: Module 13 Exercises
---

# Module 13 Exercises

**Four exercises · about 45 minutes · one scenario**

All exercises use the same fictional organization: **Cedar Clinic Network**, a group of six clinics that wants to publish synthetic-data summaries and train a shared triage model. Every number below is invented for practice. Do not run any of this against real patient data, and do not treat the calculations as a compliance determination.

---

## Exercise 1 — Budget ledger (10 minutes)

Cedar plans one quarter of releases under a total budget of \(\varepsilon = 2.0\) with \(\delta = 0\).

| Release | Epsilon each | Count | Notes |
|---|---:|---:|---|
| Cohort counts by clinic | 0.10 | 3 | same underlying cohort table |
| Mean age by clinic | 0.25 | 2 | same cohort table |
| Shared triage model training | 1.20 | 1 | DP-SGD |
| Dashboard refresh | 0.15 | 4 | recomputes the cohort counts |

1. Compute the total epsilon under basic sequential composition.
2. Is the plan within budget? By how much is it over or under?
3. Propose an allocation that stays at or below 2.0 while keeping the model training and at least two dashboard refreshes. Show the ledger.
4. A colleague suggests re-running the cohort counts with a different random seed and calling the second run "parallel" because the seed differs. Is that correct? Explain.
5. Why is a ledger more useful than quoting a per-query epsilon in a data-sharing agreement?

---

## Exercise 2 — Sensitivity and noise (10 minutes)

Cedar releases the mean of 800 rows with 3 features, each clipped to \([-4.0, 4.0]\).

1. Compute the L1 sensitivity of the mean vector.
2. Compute the Laplace scale at \(\varepsilon = 0.5\) and at \(\varepsilon = 0.05\).
3. The cohort shrinks to 400 rows. Recompute sensitivity and the scale at \(\varepsilon = 0.5\). What does this show about the cost of small cohorts?
4. Cedar raises the clipping bound to 6.0 to reduce bias. Recompute sensitivity at \(n = 800\) and the scale at \(\varepsilon = 0.5\). What did the change cost in privacy terms?
5. The observed clipped fraction is 0.02. Explain why the bound must still be treated as public and why the sensitivity uses the bound, not the observed maximum.

---

## Exercise 3 — Designing an honest empirical audit (15 minutes)

A release reports a membership AUC of 0.52 and concludes "no leakage." You are asked to review the audit design.

1. Name three reasons this AUC is weak evidence.
2. Design a **positive control**: a configuration in which the audit should detect membership if the test works. State the configuration, the expected result, and what a failure would mean.
3. Design the repeat structure: how many seeds, what to report, and how to describe the result if the interval straddles 0.5.
4. Design one test that varies the nonmember distribution rather than the mechanism. What confound does it expose?
5. Write a decision rule for the audit that a reviewer could apply without reading the code. The rule must not say "AUC near 0.5 means private."

---

## Exercise 4 — Report critique (10 minutes)

Cedar receives this vendor report:

> We trained the triage model with DP-SGD at \(\varepsilon = 3\), \(\delta = 10^{-5}\). Gradients were clipped at \(C = 1\). We selected \(C\) from \(\{0.5, 1, 2\}\) by maximizing test accuracy. The model is released daily; each release is \(\varepsilon = 3\), and because the releases are independent the total remains \(\varepsilon = 3\). Test accuracy is 0.91. A membership inference test returned AUC 0.51, so there is no membership leakage. The model is therefore private and safe to deploy.

1. Identify at least five problems in the report.
2. For each problem, state the correction or the missing information.
3. Rewrite the final two sentences as a scoped statement.
4. List four items that belong in the documentation record but are absent.

---

*Compare your work with the [exercise solutions](exercise-solutions.md).*
