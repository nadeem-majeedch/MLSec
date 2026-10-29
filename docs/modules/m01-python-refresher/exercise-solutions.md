# Module 01 Exercise Solutions

**Read this after a first attempt.** These are model answers, not the only correct answers. If your number differs, check the shape, dtype, index, and seed before assuming your reasoning is wrong.

All outputs below were produced on Python 3.14.7 with NumPy 2.5.2, pandas 3.0.5, and scikit-learn 1.9.0.

---

## Exercise 1 — A metric that checks its shapes

### Solution

```python
import numpy as np


def per_class_recall(y_true, y_pred, n_classes):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    if y_true.shape != y_pred.shape:
        raise ValueError(
            f"shape mismatch: y_true {y_true.shape} vs y_pred {y_pred.shape}"
        )
    if y_true.ndim != 1:
        raise ValueError("inputs must be one-dimensional")

    recalls = np.empty(n_classes, dtype=float)
    for c in range(n_classes):
        true_c = y_true == c
        n_true = int(true_c.sum())
        if n_true == 0:
            print(f"warning: class {c} has no true examples")
            recalls[c] = np.nan
            continue
        tp = int((true_c & (y_pred == c)).sum())
        recalls[c] = tp / n_true
    return recalls
```

### Expected output

```python
y_true = [0, 1, 1, 2, 2, 2]
y_pred = [0, 1, 2, 2, 0, 2]
print(per_class_recall(y_true, y_pred, 3))
```

```text
[1.  0.5 0.66666667]
```

### Why the denominators differ

| Class | True examples | Correct predictions | Recall | Denominator |
|---|---:|---:|---:|---|
| 0 | 1 (index 0) | 1 | 1.0000 | 1 |
| 1 | 2 (indices 1, 2) | 1 (index 1) | 0.5000 | 2 |
| 2 | 3 (indices 3, 4, 5) | 2 (indices 3, 5) | 0.6667 | 3 |

Recall asks: *of the rows that truly belong to this class, what fraction did we find?* The denominator is therefore the number of **true** examples for that class. Dividing by the total number of rows (6) would produce `[0.1667, 0.1667, 0.3333]`, which is not recall.

### Common errors

| Error | What happens | Fix |
|---|---|---|
| `y_pred == c` used as the denominator | Measures precision, not recall | Denominator is `y_true == c` |
| Integer division | `1 // 2` gives `0` | Cast to `float` or divide with `/` |
| Silent broadcasting | A `(n, 1)` input compares against `(n,)` and yields `(n, n)` | Reject `ndim != 1` |
| Returning `0.0` for an absent class | Hides a class that was never tested | Return `nan` and warn |

### Self-check

- Does `per_class_recall([0, 0], [0, 1], 2)` warn about class 1 and return `[1.0, nan]`?
- Does a `(6, 1)` input raise `ValueError`?
- Does `np.mean` of the output ignore `nan`? It does not — use `np.nanmean` and say so in your note.

---

## Exercise 2 — Audit a messy table

### Solution

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

print("shape:", orders.shape)
print(orders.dtypes)
print("missing:\n", orders.isna().sum())
print("exact duplicates:", orders.duplicated().sum())
print(orders[orders.duplicated(keep=False)])

merged = orders.merge(sessions, on="user_id", how="left")
print("merged shape:", merged.shape)
print(merged)

print("mean amount, merged:", round(merged["amount"].mean(), 4))
print("mean amount, orders:", round(orders["amount"].mean(), 4))
print(orders.groupby("user_id", dropna=False)["amount"].mean())
```

### Expected output

```text
shape: (6, 2)
user_id        str
amount     float64
dtype: object
missing:
 user_id    0
amount     1
dtype: int64
exact duplicates: 1
  user_id  amount
4      U4     7.0
5      U4     7.0
merged shape: (7, 3)
  user_id  amount  minutes
0      U1    10.0      3.0
1      U1    10.0      4.0
2      U2    20.0      5.0
3      U2     NaN      5.0
4      U3     5.0      6.0
5      U4     7.0      NaN
6      U4     7.0      NaN
mean amount, merged: 9.8333
mean amount, orders: 9.8
user_id
U1    10.0
U2    20.0
U3     5.0
U4     7.0
Name: amount, dtype: float64
```

On pandas 2.x the `user_id` dtype prints as `object` instead of `str`. The values are the same; pandas 3 introduced a dedicated string dtype. Do not make a test depend on the printed dtype label.

### Why the merge grew

The count went from 6 to 7 because the right table is not unique on the join key:

- `U1` has **two sessions** (3 and 4 minutes), so the `U1` order appears twice.
- `U4` has **two identical orders** (a duplicate in the left table), so both duplicate rows survive.
- `U4` has no session; the left join still keeps it and fills `minutes` with `NaN`.
- `U2` has two orders and one session, so each of those two orders gets the same 5 minutes.

The row count of a join is not `len(left) + len(right)`; it is the sum of matching combinations. Neither table was unique, and both problems compounded.

### What gets distorted

If the merged table is treated as one row per order:

| Question | True answer | Merged answer | Direction |
|---|---|---|---|
| Number of orders | 6 | 7 | Overcount by 1 |
| Mean order amount | 9.8 | 9.8333 | Slightly higher |
| Total session minutes | 18 | 26 | Overcount by 8 |
| Mean minutes per order | 4.5 (18/4) | 3.714 (26/7) | Lower |

The mean amount moves only slightly here, which is exactly why this bug survives review: the number looks fine. The count and the session totals are badly wrong.

### Correct aggregation

The unit of a row must be stated before any metric. For "average order amount per user", aggregate orders at the order grain first:

```python
per_user = (
    orders.groupby("user_id", dropna=False)["amount"]
    .mean()
    .rename("avg_order_amount")
    .reset_index()
)
```

```text
  user_id  avg_order_amount
0      U1              10.0
1      U2              20.0
2      U3               5.0
3      U4               7.0
```

`U2` has a missing amount. `groupby.mean()` skips it by default, so `U2` is the mean of one value, not of two. That is a decision, not a fact: write it down, and if missingness matters, use `.agg(["mean", "count"])` so the reader can see that `U2` is based on one order.

If the question is "average session minutes per user", aggregate `sessions` separately and join the two summaries once, after each is unique on `user_id`. Joining raw event tables to each other is how row counts quietly multiply.

### Self-check

- Did you state the unit of a row before computing anything?
- Did you report the duplicate as `U4`, not just "1"?
- Did you notice that `U4` has no session, and decide whether that is expected?
- Did you avoid using the merged mean as the order mean?

---

## Exercise 3 — Leakage demonstration

### Solution

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline

X_syn, y_syn = make_classification(
    n_samples=200, n_features=500, n_informative=5,
    n_redundant=0, n_classes=2, random_state=42,
)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

selector = SelectKBest(f_classif, k=10).fit(X_syn, y_syn)
X_selected = selector.transform(X_syn)

leaky = cross_val_score(
    LogisticRegression(max_iter=2000, random_state=42),
    X_selected, y_syn, cv=cv,
)
clean = cross_val_score(
    Pipeline([
        ("select", SelectKBest(f_classif, k=10)),
        ("clf", LogisticRegression(max_iter=2000, random_state=42)),
    ]),
    X_syn, y_syn, cv=cv,
)

print("leaky folds:", np.round(leaky, 3), "mean:", round(leaky.mean(), 4))
print("clean folds:", np.round(clean, 3), "mean:", round(clean.mean(), 4))
print("gap:", round(leaky.mean() - clean.mean(), 4))
```

### Expected output

```text
leaky folds: [0.6   0.8   0.7   0.675 0.75 ] mean: 0.705
clean folds: [0.525 0.575 0.7   0.675 0.65 ] mean: 0.625
gap: 0.08
```

The leaky protocol scores **8 percentage points** higher. Both arms use the same 5 folds, the same classifier, and the same regularization. The only difference is *when* feature selection saw the labels.

Notice that the highest fold is identical (0.70 vs 0.675 is close) while the low folds diverge. Leakage does not add a constant; it adds an optimistic bias whose size depends on the fold. That is another reason a single split is a weak claim.

### Which number to publish

Publish **0.625**, and describe it as "5-fold stratified cross-validation accuracy of a pipeline in which feature selection is fitted inside each training fold". Do not describe the pipeline model as "better" than the leaky one. It is the same model family measured under a protocol that does not let the validation rows influence feature choice. The 0.705 is an artifact of the protocol, not evidence of a stronger model.

Also state the limitation: 200 samples and 500 features is a deliberately hard, high-variance setting. The fold spread is wide, and the mean alone hides that.

### Self-check

- Are the folds the same object (`cv`) in both arms?
- Is the classifier identical in both arms?
- Did you avoid re-running `make_classification` with a different seed between arms?
- Did you report the gap and the fold spread, not just two means?

---

## Exercise 4 — Scenario: reproduce a 99.2% claim

### Model answer, part 1: problems

| # | Problem in the report | Likely effect on 99.2% | Why |
|---|---|---|---|
| 1 | No random seed | Unknown | The split, the model fit, and any sampling change between runs; the number is not reproducible |
| 2 | `StandardScaler().fit(X)` before the split | Higher | The scaler saw test rows, so test statistics leaked into training |
| 3 | Mean imputation before the split | Higher | The imputation values were computed with test rows included |
| 4 | Accuracy only, on 8% churn | Misleading, probably higher | A model that predicts "no churn" for everyone scores about 92% accuracy and finds zero churners |
| 5 | One 80/20 split, evaluated once | Unknown, unstable | With ~960 positives in the test set, one split can be several points from the mean; no uncertainty is reported |
| 6 | Possible duplicate customers | Higher | If the same customer appears in train and test, the model can memorize them; rows are not independent |
| 7 | No baseline | Unknown | Without a majority-class or logistic-regression baseline, 99.2% has no reference point |
| 8 | No feature or target definition | Unknown | A post-outcome field (e.g. "cancellation reason") would explain a near-perfect score |

Any five of these satisfy the exercise. Problems 1–4 are the core set; 5–8 show deeper review.

### Model answer, part 2: planned reproduction

1. **Obtain the data and code, then freeze the split.** Set a seed, save the train/test indices, and record the row count and positive rate in both parts. Run twice and confirm identical indices. This detects the unstable split and the missing seed.
2. **Rebuild the model as a pipeline.** Put imputation, scaling, and the classifier inside one `Pipeline`, and evaluate with 5-fold `StratifiedKFold(shuffle=True, random_state=...)`. This removes the scaling and imputation leaks. Compare the pipeline score with the reported 99.2%; a large drop is evidence of leakage, not proof of it.
3. **Switch the headline metric.** Report accuracy, precision, recall, F1, and PR-AUC, plus the confusion matrix at a stated threshold. Include the majority-class baseline. On 8% churn, recall and PR-AUC are the numbers a reader needs. This detects the imbalance problem.
4. **Check duplicates by customer, not by row.** Count customers with more than one row, and check how many appear in both train and test. If overlap exists, re-split by customer ID (`GroupShuffleSplit`) and report both results. This detects the duplicate-customer problem.

Add one more check: univariate AUC of each feature against the target, and the top feature importances. A single feature with AUC above roughly 0.95 on a churn problem is a target-leak signal worth investigating before believing any score.

### Model answer, part 3: message draft

> Hi — thanks for sharing the churn result. I would like to reproduce the 99.2% before we put it in the slide, and I have a few questions about the setup. Could you send the dataset snapshot and the notebook, including the seed and the exact train/test split? I also noticed the scaler and the mean imputation are fitted on the full data before the split, which can inflate the score; I would like to rerun it with those steps inside a pipeline and with stratified cross-validation. On an 8% churn rate I would also report recall and PR-AUC alongside accuracy, since accuracy can look high while missing most churners.

The message asks for evidence, names the specific mechanism, and proposes a shared rerun. It does not say "your result is wrong" and it does not accuse anyone of misconduct. Most leakage is an honest mistake made under deadline.

### Self-check

- Did you list at least five distinct problems, not five restatements of "no seed"?
- Did you state a direction (higher, lower, unknown) for each, with a reason?
- Does each of the four planned checks map to a named problem?
- Would you be comfortable if your colleague read your message?

---

## Self-assessment rubric

Score each row 0–2, where 2 is "complete and defensible".

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Correctness of outputs | Numbers do not match and no explanation | One output differs but is explained | Outputs match, or differences are explained by version or seed |
| Shape and dtype awareness | No validation | Some checks | Explicit validation with clear errors |
| Audit trail | Results only | Some intermediate counts | Row counts, unit of a row, and decisions recorded |
| Leakage reasoning | "Pipeline is better" | Identifies the leak | Explains the protocol difference and refuses the "better" framing |
| Communication | Accusatory or vague | Specific but incomplete | Specific, non-accusatory, asks for evidence |
| Reproducibility | No seed or command | Partial | Seed, saved split, versions, and a rerun command |

A total of 10–12 is ready for LAB-01. Below 8, revisit the matching lesson before starting the lab; the lab assumes these skills and will be slow otherwise.

## Next step

Complete the [portfolio checklist](exercises.md#portfolio-checklist), then start [LAB-01](../../labs/lab-01.md). The lab combines all four exercises into one reproducible artifact and adds a manifest and a written threat-model justification.
