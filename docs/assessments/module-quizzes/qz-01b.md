# Module 01 Alternate Quiz (QZ-01B)

| Field | Value |
|---|---|
| Module | M01 — Python, NumPy, pandas, and scikit-learn Refresher |
| Quiz A | [QZ-01](../../modules/m01-python-refresher/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-01, LO-28 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-01b-key.md` |

Answer without running the code unless an item says otherwise. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. Index alignment

```python
import pandas as pd
s1 = pd.Series([10, 20, 30], index=[0, 1, 2])
s2 = pd.Series([1, 2, 3], index=[1, 2, 3])
print((s1 + s2).tolist())
```

What is printed?

A. `[11, 22, 33]`  
B. `[nan, 21.0, 32.0, nan]`  
C. `[nan, 21, 32, nan]` as a Series with index `[0, 1, 2, 3]`  
D. It raises a `ValueError` because the indices differ.

## 2. Stratification

What is the purpose of `train_test_split(..., stratify=y)`?

A. It sorts the rows by label before splitting.  
B. It preserves the label proportions in each split.  
C. It guarantees that the test set is larger than the training set.  
D. It removes duplicate rows before splitting.

## 3. Duplicate rows

True or false: `df.drop_duplicates()` with no arguments removes rows that are identical across **all** columns, keeping the first occurrence by default.

## 4. Pipeline placement

True or false: fitting a preprocessing `Pipeline` on the training rows and then calling `predict` on the test rows prevents the preprocessing from learning from the test set.

## 5. Saved splits

Why is it better to save the train/validation/test row indices than to call `train_test_split` again whenever you need the split? Give two reasons.

## 6. Stratified split arithmetic

A dataset has 2,000 rows and 10% positives. You make a stratified 80/20 train/test split. How many positive rows are in the training set and in the test set? How many rows total are in each split?

## 7. Find the flaw

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
scaler = StandardScaler().fit(X_test)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

Identify the flaw, explain the consequence, and give the corrected line.

## 8. Scenario: the perfect notebook

A colleague sends a notebook that reports 0.999 accuracy on a 10,000-row tabular dataset. You notice that the label column is still present in `X`, and the notebook uses a random row split. Name three checks you would run before trusting the number, and say what each could reveal.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can audit data handling, not only write it. |
| 10 | Pass. Review the missed item before LAB-01. |
| 8–9 | Reread M01.L3–L5, especially index alignment, splits, and reproducibility. |
| Below 8 | Reread M01 and rerun LAB-01 from a clean environment. |
