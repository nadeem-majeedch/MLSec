---
title: Module 01 Exercises
---

# Module 01 Exercises

**Four exercises · about 60–90 minutes · Complete after the lessons**

Write your work in `work/m01/`. Run the code; do not only read it. Check the [solutions](exercise-solutions.md) after you have a first attempt.

---

## Exercise 1 — A metric that checks its shapes

**Goal.** Implement per-class recall with NumPy and explicit validation.

**Task.** Write a function:

```python
def per_class_recall(y_true, y_pred, n_classes):
    ...
```

Requirements:

- Convert inputs with `np.asarray`.
- Raise `ValueError` if the shapes differ or if either input is not one-dimensional.
- For each class `c`, compute `TP / (TP + FN)`.
- If a class has no true examples, return `nan` for that class and print a warning.
- Do not use scikit-learn for this exercise.

Test it with:

```python
y_true = [0, 1, 1, 2, 2, 2]
y_pred = [0, 1, 2, 2, 0, 2]
print(per_class_recall(y_true, y_pred, 3))
```

**Deliverable.** `work/m01/per_class_recall.py` plus a short note explaining the denominator for each class.

**Success criteria.** Shape validation works; the output is `[1.0, 0.5, 0.6667]` (within rounding); the denominator is the number of true examples for each class, not the total.

---

## Exercise 2 — Audit a messy table

**Goal.** Detect duplicate rows, missing values, and join multiplication before computing a metric.

**Data.**

```python
import pandas as pd

orders = pd.DataFrame({
    "user_id": ["U1", "U2", "U2", "U3", "U4", "U4"],
    "amount": [10, 20, None, 5, 7, 7],
})
sessions = pd.DataFrame({
    "user_id": ["U1", "U1", "U2", "U3"],
    "minutes": [3, 4, 5, 6],
})
```

**Tasks.**

1. Print the shape, dtypes, and missing-value counts of `orders`.
2. Count exact duplicate rows. Identify the duplicated record.
3. Merge `orders` with `sessions` on `user_id` with a left join. Print the shape and the result.
4. Explain why the merged table has more rows than `orders`, and name one metric that would be distorted if the merged table were treated as one row per order.
5. Write the correct aggregation if the question is "average order amount per user."

**Deliverable.** `work/m01/table_audit.md` with the outputs and a five-line explanation.

**Success criteria.** You report 6 orders, 1 missing amount, 1 duplicate row, and a 7-row merge. You explain that U1 has two sessions and U4 has a duplicate order. You state the unit of a row.

---

## Exercise 3 — Leakage demonstration

**Goal.** Measure how much a preprocessing leak inflates a cross-validation score.

**Tasks.**

1. Generate the 500-feature synthetic dataset from Lesson 01.4 with `random_state=42`.
2. Compute 5-fold stratified cross-validation accuracy for a logistic regression trained on the top 10 features selected on the **full** dataset.
3. Repeat with `SelectKBest` inside a `Pipeline`.
4. Report both means and the gap. Use the same folds and the same classifier settings for both.
5. Write two sentences explaining which number you would publish and why.

**Deliverable.** `work/m01/leakage.py` and `work/m01/leakage.md`.

**Success criteria.** Same folds and classifier for both arms; the leaky score is higher; the report states the gap and does not claim the pipeline model is "better" — it is measured more honestly.

---

## Exercise 4 — Scenario: reproduce a 99.2% claim

**Goal.** Apply the module's checks to a colleague's result.

Your colleague sends this notebook summary:

> Churn model, 99.2% accuracy. Loaded `churn.csv` (12,000 rows, 8% churn). Filled missing values with the column mean. Scaled features with `StandardScaler().fit(X)`. Split 80/20 with `train_test_split`. Trained logistic regression. Evaluated once on the test set. Wrote the accuracy in the slide. No random seed was set.

**Tasks.**

1. List at least **five** reproducibility or validity problems.
2. For each, state what the corrected result might change (higher, lower, or unknown) and why.
3. Write a four-step reproduction plan, including one check that would detect each of these: leakage, imbalance, duplicate customers, and an unstable split.
4. Draft the first three sentences of a message to your colleague. Be specific and non-accusatory.

**Deliverable.** `work/m01/reproduction-review.md`.

**Success criteria.**

- Problems include missing seed, scaling before split, mean imputation before split, accuracy-only metric on 8% churn, single split, and possible duplicate customers.
- The plan uses a pipeline, stratified CV, a PR/recall metric, and a duplicate check by customer ID.
- The message asks for the data and code rather than declaring the result false.

---

## Portfolio checklist

- [ ] `per_class_recall.py` with shape validation
- [ ] `table_audit.md` with row counts and units
- [ ] `leakage.py` and `leakage.md` with two comparable scores
- [ ] `reproduction-review.md` with five problems and a plan
- [ ] Five-line reflection

Then run [LAB-01](../../labs/lab-01.md). The lab turns these skills into a complete artifact.
