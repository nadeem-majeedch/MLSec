---
title: Module 01 Knowledge Check (QZ-01)
---

# Module 01 Knowledge Check (QZ-01)

**10 items · 20 minutes · Pass mark 80%**

Write your answers before opening the [answer key](quiz-answers.md). For code items, predict the output first, then run it.

---

**1. (Predict)** What does this print, and why?

```python
def add(item, bucket=[]):
    bucket.append(item)
    return bucket

print(add("a"))
print(add("b"))
```

---

**2. (Evaluate)** A configuration file contains the string `"False"`. The code is:

```python
if config["enabled"]:
    enable_debug_endpoint()
```

Does the endpoint get enabled? Explain.

---

**3. (Predict)** What is printed?

```python
import numpy as np
a = np.array([200], dtype=np.uint8)
b = np.array([100], dtype=np.uint8)
print(a + b, (a + b).dtype)
```

---

**4. (Apply)** `X` has shape `(500, 20)` and `col_mean` has shape `(20,)`. What is the shape of `(X - col_mean)`? What does the result represent?

---

**5. (Analyze)** A `DataFrame` has 1,000 rows. It is merged with a session table that has 4,000 rows and an average of 4 sessions per user. The result has 4,000 rows. Is this necessarily a bug? What must you state before computing a per-user metric?

---

**6. (Find the flaw)** The following code reports a cross-validation score. Identify the leakage and fix it.

```python
scaler = StandardScaler().fit(X, y)
X_scaled = scaler.transform(X)
scores = cross_val_score(LogisticRegression(), X_scaled, y, cv=5)
```

---

**7. (Interpret)** A model reports accuracy 0.947 and recall 0.0 on a fraud dataset. What is the most likely explanation, and which metric would you report instead?

A. The model is 94.7% correct and should be deployed
B. The model predicts the majority class; report precision, recall, PR-AUC, and a threshold
C. Recall is always zero when accuracy is high
D. The dataset is balanced

---

**8. (Apply)** You call `np.random.default_rng(7)` twice in two separate experiments. Do you get the same sequence? What if you use the same generator object for both experiments without resetting it?

---

**9. (Multi-select)** Which practices improve reproducibility? Select all that apply.

A. Saving the train/test row indices
B. Recording package versions in a manifest
C. Re-running cells in any order
D. Passing a seed to every randomized component

---

**10. (Scenario)** A colleague reports 99.2% accuracy on a customer-churn model. The notebook fits a `StandardScaler` on the full dataset, splits it, and evaluates once. They ask you to reproduce it. List the first four checks you would run, and explain what each could change.

---

Open the [answer key](quiz-answers.md) when you are ready, then complete the [exercises](exercises.md).
