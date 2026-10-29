---
title: Module 14 Exercises
---

# Module 14 Exercises

**Four exercises · about 40 minutes · one scenario**

All exercises use **CivicBridge**, a fictional benefits-screening service. The model and numbers are synthetic. Nothing here involves real applicants, and no exercise should be run against a production explanation endpoint.

---

## Exercise 1 — Three explanations, one prediction (10 minutes)

A logistic model has \(w = (1.0,\ -1.5,\ 0.8)\), \(b = -0.2\), and an applicant has \(x = (2.0,\ 1.0,\ -5.0)\).

1. Compute \(z\), \(p\), and the log-odds contribution of each feature. Rank the features by contribution magnitude.
2. Compute gradient×input attributions. Rank them.
3. Compute occlusion attributions with baseline 0. Rank them.
4. The coefficient ranking is \(x_2, x_1, x_3\). Why do the three rankings differ? Which one would you publish to the applicant, and why?
5. The applicant asks, "If I changed feature 3 from -5 to 0, would I be approved?" Which of these calculations, if any, contains enough information to answer that question? What does the answer not establish?

---

## Exercise 2 — Explanation endpoint threat model (10 minutes)

CivicBridge plans to expose an endpoint that returns the top-5 feature contributions for any application, to any authenticated caseworker.

1. Write the asset, audience, channel, capability, objective, impact, and residual-risk rows of a threat model.
2. The endpoint returns contributions to the log-odds, not probabilities. Show how a caseworker with four features recovers the model's weights. State how many queries are needed.
3. The endpoint is changed to return only the top-2 contributions. Does that stop the procedure? Explain.
4. Propose three controls that reduce the information per response, and one that detects probing.
5. Why is "the caseworker is authenticated" not a sufficient control?

---

## Exercise 3 — Subgroup audit (15 minutes)

CivicBridge evaluates a baseline and a reweighted model on 800 synthetic applicants.

**Baseline**

| Group | n | TP | FN | FP | TN |
|---|---:|---:|---:|---:|---:|
| A | 500 | 105 | 45 | 70 | 280 |
| B | 300 | 78 | 42 | 36 | 144 |

**Reweighted**

| Group | n | TP | FN | FP | TN |
|---|---:|---:|---:|---:|---:|
| A | 500 | 102 | 48 | 70 | 280 |
| B | 300 | 78 | 42 | 36 | 144 |

1. Compute TPR, FPR, selection rate, and accuracy for each group in both models.
2. Compute the DP and equalized-odds gaps for both models.
3. Compute overall accuracy for both. What did the intervention cost?
4. The reweighted model's TPR gap fell because group A's TPR fell, not because group B's rose. Is that an improvement? Argue both sides, then state what you would report.
5. Estimate a 95% interval for group B's TPR in the baseline and compare it with group A's. What does the overlap imply for the comparison?
6. Write one sentence for the audit summary that states the trade-off without choosing a winner.

---

## Exercise 4 — Report critique (5 minutes)

A vendor report says:

> The model is fair: demographic parity is 0.001. Explanations are trustworthy: Spearman stability is 0.99. The endpoint returns full attribution vectors to all authenticated users, which is safe because access is logged. Reweighting improved fairness: the equalized-odds gap fell from 0.12 to 0.09. Accuracy is 0.91. We evaluated on one held-out split. DP-SGD was applied at epsilon 8.

1. Identify six problems or missing pieces of evidence.
2. Rewrite the opening claim as a scoped statement.
3. List four residual risks the report does not address.

---

*Compare your work with the [exercise solutions](exercise-solutions.md).*
