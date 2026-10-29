---
title: Module 12 Exercises
---

# Module 12 Exercises

**Four exercises · about 45 minutes · one scenario**

All exercises use the same fictional federation: **Northline**, six organizations training a shared readmission model on 2,400 synthetic rows across five classes. The numbers are invented for practice. Do not point any experiment at a real participant or a real clinical dataset.

---

## Exercise 1 — FedAvg arithmetic and influence (10 minutes)

Six clients submit updates for one round.

| Client | Rows | Update \((\Delta_1,\Delta_2)\) |
|---|---:|---|
| C1 | 300 | \((0.2,-0.1)\) |
| C2 | 500 | \((0.4,0.2)\) |
| C3 | 400 | \((-0.2,0.3)\) |
| C4 | 600 | \((0.1,0.0)\) |
| C5 | 200 | \((0.6,-0.4)\) |
| C6 | 400 | \((-0.1,0.2)\) |

1. Compute the sample-weighted mean update.
2. C5 is malicious and scales its update by 6. Recompute the aggregate.
3. Compute C5's effective share of the aggregate direction, accounting for its sample weight and the scale. Compare it with the \(s/(K-1+s)\) figure that assumes equal weights.
4. Name one control that bounds the sample-count influence and one that bounds the update-magnitude influence.
5. Why is it inaccurate to say "one client out of six has one sixth of the vote"?

---

## Exercise 2 — Backdoor design and evaluation (10 minutes)

Northline suspects a backdoor. The hypothesized attack:

- trigger: set two specific features to their maximum;
- target: class 1 (readmitted);
- poison: the malicious client appends triggered copies of its own rows, relabeled 1;
- scale: 4×;
- fraction: one client of six.

1. Explain why the malicious update might still perform well on the clean task.
2. Design three evaluation rows that would distinguish a backdoored model from a clean one. For each, state the metric and the expected difference.
3. Name three monitoring signals that could flag the client before the trigger is known, and one that cannot.
4. The team proposes excluding the client and retraining from scratch. Name two reasons the current global model still needs evaluation.
5. Suppose the trigger is a rare feature value that appears in 0.1% of clean rows. Why is a clean-accuracy gate unlikely to catch the backdoor?

---

## Exercise 3 — Choosing an aggregation rule (15 minutes)

1. For the eight scalar updates \(0.2,\ 0.3,\ 0.5,\ 0.6,\ 0.7,\ 0.8,\ 1.0,\ 4.0\), compute the mean, the 1-trimmed mean, and the median.
2. Krum requires \(K \ge 2m+3\). For \(K=8\), what is the largest \(m\)? For that \(m\), how many nearest neighbors does each score use?
3. Northline has six clients and suspects two are colluding. Can Krum be used with \(m=2\)? Show the inequality.
4. For each scenario, choose a rule and justify it in two sentences. State one residual risk.
   - **A.** One million intermittent mobile clients, weak identity, one round samples 200.
   - **B.** Six hospitals, two possibly colluding, strong contracts and identity.
   - **C.** A 100-client neural-network federation with 50 million weights, one suspected attacker.
   - **D.** An attacker who has read the aggregation paper and can optimize against the rule.
5. Why does a coordinate-wise median not guarantee a good model even when it resists an outlier?

---

## Exercise 4 — Evaluation critique (10 minutes)

A vendor reports:

| Run | Rounds | Clean accuracy | Attack success |
|---|---:|---:|---:|
| Vendor robust aggregator | 40 | 0.88 | 0.02 |
| Plain FedAvg | 10 | 0.90 | 0.40 |
| Benign, no attacker | 10 | 0.92 | 0.01 |

The vendor claims a 95% reduction in attack success and "negligible utility cost."

1. Identify four problems with the comparison.
2. Compute the vendor's relative reduction. Then explain why the number cannot be attributed to the aggregator.
3. What would the vendor need to report for a valid comparison? List at least five fixed factors.
4. The vendor says the 0.02 ASR is "effectively zero." Write a sentence that states the residual risk without overclaiming.
5. Write a scoped assurance statement for the vendor's result, including what it does not establish.

---

*Compare your work with the [exercise solutions](exercise-solutions.md).*
