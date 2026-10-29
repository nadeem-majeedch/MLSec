# Module 09 Alternate Quiz (QZ-09B)

| Field | Value |
|---|---|
| Module | M09 — Data Integrity, Dataset Governance, and Secure Training Pipelines |
| Quiz A | [QZ-09](../../modules/m09-data-integrity/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-20 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-09b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. Pinning a dataset version

Which identifier best pins the exact dataset content used by a training run?

A. The file name, such as `dataset.csv`  
B. A SHA-256 hash recorded in a manifest  
C. The row count  
D. The creation date shown by the operating system

## 2. Conflicting customer rows

A table has two rows for the same `customer_id` with different labels and otherwise identical features. Which defect class is this?

A. Schema violation  
B. Entity or key conflict  
C. Missing value  
D. Temporal leakage

## 3. Schema validation

True or false: a schema validation pass with zero errors proves the dataset has no semantic defects.

## 4. Reproducibility factors

True or false: recording the random seed is sufficient for another person to reproduce a training run; library versions and hardware do not need to be recorded.

## 5. Duplicate detection

Explain in one sentence why a row-count check alone cannot detect every duplicate or replacement defect.

## 6. Repair arithmetic

A dataset has 2,000 rows. It contains 90 excess duplicate rows and 40 rows in label-conflict groups. Ten of the 40 conflict rows are also among the 90 excess duplicates.

How many unique rows are removed if both defects are repaired, and how many rows remain? Show the inclusion–exclusion step.

## 7. Find the flaw

The code below is meant to prevent the same customer appearing in both training and test data.

```python
train_idx, test_idx = train_test_split(
    df.index, test_size=0.3, random_state=7
)
df = df.drop_duplicates(subset="customer_id", keep="first")
X_train = df.loc[df.index.intersection(train_idx)]
X_test = df.loc[df.index.intersection(test_idx)]
```

Identify two flaws and explain the consequence for the reported test score.

## 8. Scenario: the readmission dataset

A hospital wants to train a readmission model on a historical extract. You are defining the dataset controls before any modeling.

Name three controls, the evidence each produces, and one residual risk that remains after all three. Use only de-identified or synthetic data in your plan, and keep the work local.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can connect data controls to measured evidence. |
| 10 | Pass. Review the missed item before LAB-12. |
| 8–9 | Reread M09.L2, L3, and L5. |
| Below 8 | Reread M09 and rerun LAB-12 from a clean state. |
