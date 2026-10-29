---
title: Module 02 Exercises
---

# Module 02 Exercises

**Four exercises · about 75–105 minutes · Complete after the lessons**

Write your work in `work/m02/`. Run every calculation; do not only read it. Compare with the [solutions](exercise-solutions.md) after a first attempt.

---

## Exercise 1 — Compute the operating point

**Goal.** Turn a threshold table into a decision under a capacity constraint.

**Data.** A fraud model was evaluated on 500 transactions with 56 positives. At three thresholds:

| Threshold | Flagged | True positives | False positives | False negatives |
|---:|---:|---:|---:|---:|
| 0.20 | 63 | 29 | 34 | 27 |
| 0.30 | 28 | 17 | 11 | 39 |
| 0.50 | 8 | 7 | 1 | 49 |

**Tasks.**

1. Compute precision, recall, and F1 for each threshold. Show the formulas and round to three decimals.
2. The review team can handle **75 alerts per 500 transactions**. A missed fraud costs about 10 times a manual review. Which threshold do you recommend, and why?
3. What would change if the team could handle only **25** alerts per 500?
4. State one reason the highest-precision threshold might still be the wrong operating point.

**Deliverable.** `work/m02/operating_point.md` with the table and a short recommendation.

**Success criteria.** Precision and recall match the definitions; the recommendation is tied to capacity and cost, not to F1 alone; the capacity-25 case is answered with a different trade-off.

---

## Exercise 2 — Screen a new feature for leakage

**Goal.** Use univariate AUC and provenance reasoning to decide whether a feature is usable.

**Code.**

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.metrics import roc_auc_score

X, y = make_classification(
    n_samples=1500, n_features=8, n_informative=3, n_redundant=1,
    weights=[0.85, 0.15], class_sep=0.9, flip_y=0.03, random_state=21,
)
rng = np.random.default_rng(21)
flip = rng.random(len(y)) < 0.08
late_fee_flag = np.where(flip, 1 - y, y)
```

**Tasks.**

1. Report the number of positives, the positive rate, the agreement between `late_fee_flag` and `y`, and the univariate ROC-AUC.
2. The feature is written by the billing system when an account is closed. Would you include it in a churn model scored **before** renewal? Justify with the feature's timestamp, not only its AUC.
3. Suppose a different feature, `support_calls_30d`, has univariate AUC 0.62 and is recorded daily before renewal. Would you treat it the same way? Explain the difference in reasoning.
4. Name two additional checks you would run before accepting either feature.

**Deliverable.** `work/m02/leak_screen.py` and `work/m02/leak_screen.md`.

**Success criteria.** The AUC is computed on the full dataset and matches the solution; the decision distinguishes a strong feature from a leaky one; the checks include provenance plus at least one empirical test.

---

## Exercise 3 — Calibration by hand

**Goal.** Compute a Brier score and a reliability table, and explain why ranking and calibration are different.

**Data.**

```python
import numpy as np

y = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
p = np.array([0.90, 0.20, 0.80, 0.40, 0.70, 0.10, 0.60, 0.30, 0.75, 0.25])
```

**Tasks.**

1. Compute the Brier score by hand and with NumPy.
2. Build a reliability table with bins 0.0–0.2, 0.2–0.4, 0.4–0.6, 0.6–0.8, and 0.8–1.0. For each bin, report the count, mean predicted probability, and observed positive rate.
3. Compute ROC-AUC. Explain how the model can have a perfect AUC and still be imperfectly calibrated.
4. The mean predicted probability is 0.5 and the observed rate is 0.5. Does that mean the model is calibrated? Use the table to justify your answer.

**Deliverable.** `work/m02/calibration.md` with the arithmetic and the table.

**Success criteria.** Brier score is correct to four decimals; the bins are correct and sum to 10; the explanation separates ranking from calibration; the mean-vs-local calibration distinction is explicit.

---

## Exercise 4 — Scenario: audit the 0.993

**Goal.** Apply the module's checks to a result that is about to be used in a security review.

A colleague sends this summary:

> Churn model for the retention system. ROC-AUC 0.993, accuracy 0.97. Data: 12,000 customers, 8% churn. Top feature: `late_fee_flag`, followed by `account_closed_date`. Random 80/20 split. No cross-validation. Threshold 0.5. No seed was set because the result was stable across two runs.

**Tasks.**

1. List at least **five** validity problems. For each, state whether the reported metric is likely too high, too low, or unknown, and why.
2. Write a four-step repair plan. Each step must name the check it performs and the metric it reports.
3. Draft the claim you would put in the report after the repair, using the reporting template from Lesson 02.4. You may invent plausible repaired numbers, but label them clearly as illustrative.
4. Write the first three sentences of a message to your colleague. Be specific and non-accusatory.

**Deliverable.** `work/m02/audit.md`.

**Success criteria.**

- Problems include at least: target leakage from the two date/fee fields, group/duplicate leakage from customers, missing cross-validation, accuracy on 8% churn, and no baseline or uncertainty.
- The plan uses provenance checks, a group or time-ordered split, a pipeline, PR-AUC/recall, and a confidence interval.
- The rewritten claim names the protocol, metric, baseline, and a limitation.
- The message asks for evidence and offers a shared rerun.

---

## Portfolio checklist

- [ ] `operating_point.md` with three thresholds and a capacity-based recommendation
- [ ] `leak_screen.py` and `leak_screen.md` with the AUC and a provenance decision
- [ ] `calibration.md` with the Brier score, bins, and an AUC-versus-calibration explanation
- [ ] `audit.md` with five problems, a repair plan, a rewritten claim, and a message
- [ ] Five-line reflection

Then run [LAB-01B](../../labs/lab-01b.md). The lab applies the same checks to a complete, runnable baseline and produces the artifact your portfolio needs.
