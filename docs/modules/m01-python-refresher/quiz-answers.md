# Module 01 Knowledge Check — Answers and Explanations

**QZ-01 · Answer key**

One point per item; items 9 requires all correct selections.

---

### 1. `['a']` then `['a', 'b']`

The default list is created once at function definition and reused. The second call sees the list from the first. Fix it with `bucket=None` and create a new list inside the function.

*Misconception:* "Default arguments are re-evaluated on every call." They are not.

### 2. Yes, the endpoint is enabled

A non-empty string is truthy in Python, including `"False"`. Parse booleans explicitly:

```python
enabled = config["enabled"].strip().lower() in {"true", "1", "yes"}
```

This is a real configuration vulnerability pattern: a feature intended to be off is on.

### 3. `[44] uint8`

`uint8` wraps modulo 256: 300 - 256 = 44. The dtype stays `uint8`. Cast to a wider integer or float before arithmetic. No exception is raised, which is why this is dangerous in metrics and feature pipelines.

### 4. Shape `(500, 20)`

Broadcasting aligns the trailing dimension: each column is centered by its own mean. The result is the column-centered matrix, one mean per feature. It does **not** standardize; you still need to divide by the standard deviation, and both statistics should be fitted on training data only.

### 5. Not necessarily a bug

Four sessions per user on average can produce 4,000 rows from 1,000 users if the unit of the result is a session. The bug is not the row count; it is using a per-session table as if it were per-user. Before computing a per-user metric, state the unit and aggregate to one row per user (or use a weighted metric). Record rows before and after the join.

### 6. Leakage: the scaler was fitted on all rows

`StandardScaler().fit(X, y)` sees every row before cross-validation. Each training fold therefore uses statistics influenced by its validation fold. Fix:

```python
pipe = Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression())])
scores = cross_val_score(pipe, X, y, cv=5)
```

The pipeline fits the scaler inside each training fold. The same rule applies to feature selection, imputation, and target encoding.

### 7. B

A 94.7% accuracy with 0 recall is the signature of a majority-class predictor on an imbalanced dataset. Accuracy is dominated by the negative class. Report precision, recall, F1 at a stated threshold, and PR-AUC (more informative than ROC-AUC when positives are rare). Deployment depends on the cost of false negatives and false positives, not accuracy alone.

### 8. Same sequence for two new generators; different sequence for one reused generator

`default_rng(7)` creates a new generator with the same initial state, so two separate calls produce identical sequences. A single generator advances its state on every draw, so the second experiment continues the sequence rather than restarting it. Create a fresh generator per experiment, or record and restore its state.

### 9. A, B, D

Re-running cells in any order is a source of hidden state, not a reproducibility practice. Saving indices, recording versions, and seeding randomized components are all necessary. A fourth practice is pinning versions in a lockfile.

### 10. Model answer

1. **Split before scaling.** Refit the scaler on the training rows only, or move it into a pipeline. The reported accuracy may drop; the difference is the leakage effect.
2. **Check for duplicate or near-duplicate rows across the split.** Duplicates can inflate test accuracy. Deduplicate by a stable key before splitting, or group by customer.
3. **Check the class balance and the metric.** 99.2% may be the majority-class rate. Compute precision, recall, and PR-AUC; compare against a `DummyClassifier`.
4. **Check the split seed and size.** A single small test set has wide uncertainty. Use stratified cross-validation and report mean and spread.
5. **Check the target definition and timing.** A feature recorded after the outcome (for example, a cancellation reason) is target leakage. Confirm that every feature would be available at prediction time.

Any four with a correct explanation earn the point. The best answers say what could change, not just what to inspect.

---

## Score interpretation

| Score | Next step |
|---:|---|
| 9–10 | Start LAB-01 |
| 8 | Review the missed explanations, then LAB-01 |
| 6–7 | Re-read Lessons 01.2–01.5 and retake |
| 0–5 | Work through the lessons with the examples; do not skip to the lab |

Return to the [quiz](quiz.md) or continue to the [exercises](exercises.md).
