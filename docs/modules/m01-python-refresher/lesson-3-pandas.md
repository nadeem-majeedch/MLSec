# Lesson 01.3 — pandas: Cleaning Without Lying

**Module 01 · 1.5 hours · Complete Lesson 01.2 first**

## Scenario

A security team joins a model's predictions to a table of user sessions so it can measure false positives. The session table has several rows per user. The join multiplies prediction rows, so users with many sessions appear many times. The reported false-positive rate changes from 3% to 11% without a single model prediction changing. The dashboard is not lying on purpose. It is reporting a join cardinality problem.

pandas makes joins, filling, and grouping look simple. Each operation also changes the **unit of a row**. If you do not track that unit, every metric downstream is suspect.

## Learning objectives

By the end of this lesson you will be able to:

1. Inspect a `DataFrame`'s shape, dtypes, and missing values before transforming it.
2. Select rows and columns with `.loc` and `.iloc` and explain the difference.
3. Fill or drop missing values with a documented, reproducible rule.
4. Detect row multiplication and index misalignment in joins.
5. Produce a small audit trail that states what changed and how many rows were affected.

## The two objects

A `Series` is a labeled one-dimensional array. A `DataFrame` is a collection of `Series` with a shared row index.

```python
import pandas as pd

df = pd.DataFrame({
    "student_id": ["S1", "S2", "S3", "S4"],
    "score": [88, 92, None, 79],
    "group": ["A", "A", "B", "B"],
})
print(df.to_string(index=False))
print("shape:", df.shape)
print("missing:")
print(df.isna().sum().to_string())
```

Expected output:

```text
student_id  score group
        S1   88.0     A
        S2   92.0     A
        S3    NaN     B
        S4   79.0     B
shape: (4, 3)
missing:
student_id    0
score         1
group         0
```

The integer score column became `float64` because `None` forces a missing-value representation. That is a type change, and it is visible in the output. Always print `dtypes` as well as `shape`:

```python
print(df.dtypes.to_string())
```

Expected output:

```text
student_id     object
score         float64
group          object
```

In pandas 3.x, string columns may use a dedicated string dtype depending on construction and options; record what you observe rather than assuming. The point is to look.

## Selection: `.loc` and `.iloc`

- `.loc` selects by **label**: `df.loc[row_label, column_name]`.
- `.iloc` selects by **position**: `df.iloc[row_position, column_position]`.

```python
print(df.loc[df["score"] > 80, ["student_id", "score"]].to_string(index=False))
```

Expected output:

```text
student_id  score
        S1   88.0
        S2   92.0
```

`df["score"] > 80` produces a boolean `Series`. Rows with `NaN` compare as false and are excluded. That is usually what you want, but it changes the denominator. State it: "passing rate among rows with a non-missing score."

`iloc` is useful when the index is not meaningful:

```python
print(df.iloc[0:2, 0:2].to_string(index=False))
```

Expected output:

```text
student_id  score
        S1   88.0
        S2   92.0
```

Do not mix the two. `df.loc[0]` means "the row whose label is 0," which may not be the first row after filtering.

## Missing data

There is no universal correct fill. There is only a rule you can defend.

| Rule | When it is defensible | Risk |
|---|---|---|
| Drop the row | Missingness is rare and unrelated to the outcome | Selection bias if missingness is informative |
| Fill with the column mean | Numeric, roughly symmetric, missing at random | Distorts variance; leaks test statistics if fitted on all data |
| Fill with a group mean | Groups differ substantially | Leakage if the group statistic uses future or test rows |
| Fill with a sentinel (`-1`, `"unknown"`) | Missingness itself is meaningful | The model may learn the sentinel as a shortcut |
| Model-based imputation | You can validate it inside the pipeline | More complexity; still needs leakage control |

```python
df["score_filled"] = df.groupby("group")["score"].transform(
    lambda series: series.fillna(series.mean())
)
print(df.to_string(index=False))
```

Expected output:

```text
student_id  score group  score_filled
        S1   88.0     A          88.0
        S2   92.0     A          92.0
        S3    NaN     B          79.0
        S4   79.0     B          79.0
```

Group B's mean is 79.0 because S3 is missing and S4 is 79. This is a simple rule, but it is fitted on the same rows it fills. In a real pipeline, compute the fill value on the training fold only. scikit-learn's `SimpleImputer` inside a `Pipeline` does this for you; see Lesson 01.4.

## Joins and row multiplication

A join combines rows from two tables on a key. The number of output rows depends on the **cardinality** of the key on each side.

```python
visits = pd.DataFrame({
    "student_id": ["S1", "S1", "S2"],
    "minutes": [10, 20, 30],
})
merged = df.merge(visits, on="student_id", how="left")
print("merged shape:", merged.shape)
print(merged.to_string(index=False))
```

Expected output:

```text
merged shape: (5, 5)
student_id  score group  score_filled  minutes
        S1   88.0     A          88.0     10.0
        S1   88.0     A          88.0     20.0
        S2   92.0     A          92.0     30.0
        S3    NaN     B          79.0      NaN
        S4   79.0     B          79.0      NaN
```

Four rows became five because `S1` appears twice in `visits`. The score for S1 is duplicated. If you now compute a mean score, S1 has twice the weight. The fix depends on the question:

- If you want one row per student, aggregate `visits` first (`groupby("student_id")["minutes"].sum()`), then join.
- If you want one row per visit, keep the multiplication and state that the unit is a visit.
- If you expected a one-to-one join, validate it with `validate="one_to_one"` and let pandas raise on a mismatch.

Always record the before and after row counts:

```python
audit = {
    "rows_before": len(df),
    "rows_after": len(merged),
    "extra_rows": len(merged) - df["student_id"].nunique(),
}
print(audit)
```

Expected output:

```text
{'rows_before': 4, 'rows_after': 5, 'extra_rows': 1}
```

## Index alignment

pandas aligns on labels, not positions. This is a feature and a trap.

```python
left = pd.DataFrame({"id": [1, 2], "score": [0.2, 0.8]})
right = pd.DataFrame({"id": [2, 1], "weight": [5, 10]})
print(left.merge(right, on="id").to_string(index=False))
```

Expected output:

```text
 id  score  weight
  1    0.2      10
  2    0.8       5
```

The merge matches on `id`, not on row order. If you instead assign `left["weight"] = right["weight"]`, pandas aligns the **index**; row 0 of `right` has weight 5 for id 2, so id 1 would receive the wrong weight. Use an explicit merge on the key, or reset the index deliberately.

## An audit trail for every transform

For each step that changes rows or values, record:

| Field | Example |
|---|---|
| Step | `fill_missing_score_by_group` |
| Input rows | 4 |
| Output rows | 4 |
| Rows changed | 1 (S3) |
| Rule | group mean, fitted on all rows |
| Risk | statistic includes the row being filled; move inside CV |

This is not bureaucracy. It is the difference between "I cleaned the data" and "I can tell you exactly what changed and which conclusions it affects."

## Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Joining without checking cardinality | Duplicated rows; wrong denominators | Aggregate first; use `validate=` |
| Filling with a statistic computed on all data | Leakage into validation and test | Fit imputation inside a pipeline |
| Using `inplace=True` everywhere | Hard to audit; chained-assignment surprises | Prefer explicit assignment |
| Treating `-1` as a real value | Model learns a missingness shortcut | Use `NaN` or a separate indicator column |
| Assuming row order is stable after filtering | Labels attach to wrong rows | Reset or align by key |
| Ignoring dtype changes | IDs lose leading zeros; scores become objects | Specify `dtype=` on read |

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `SettingWithCopyWarning` | Chained assignment on a slice | Use `.loc` on the original frame or `.copy()` |
| Join produces more rows than expected | Many-to-many key | Aggregate or validate cardinality |
| `NaN` appears after a merge | No match on the key | Check key dtypes and whitespace |
| Numeric column is `object` | Mixed types or sentinel strings | Clean and cast explicitly |
| Groupby drops rows | `dropna=True` default on keys | Use `dropna=False` if missing keys matter |

## Key terms

**Series**, **DataFrame**, **index**, **`.loc`**, **`.iloc`**, **boolean mask**, **imputation**, **join cardinality**, **many-to-one**, **alignment**, **audit trail**.

## Summary

- Inspect shape, dtypes, and missingness before transforming.
- `.loc` selects by label, `.iloc` by position; do not mix them.
- Every fill rule has a risk; fit imputation on training data only.
- Joins change the unit of a row; validate cardinality and record row counts.
- pandas aligns on labels; use explicit key merges to avoid misalignment.

## References

| Reference | Use |
|---|---|
| [pandas user guide](https://pandas.pydata.org/docs/user_guide/) | Indexing, merging, missing data |
| [pandas `merge`](https://pandas.pydata.org/docs/reference/api/pandas.merge.html) | Join types and validation |
| [pandas `groupby`](https://pandas.pydata.org/docs/user_guide/groupby.html) | Split-apply-combine |
| [pandas copy-on-write](https://pandas.pydata.org/docs/user_guide/copy_on_write.html) | Assignment and view semantics |

Next: [Lesson 01.4 — scikit-learn](lesson-4-scikit-learn.md).
