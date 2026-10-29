# Level 1 Check — Foundations (LC-1)

| Field | Value |
|---|---|
| Level | 1 — Foundations |
| Modules | M00–M03 |
| Items | 10 |
| Points | 20 |
| Time guide | 30 minutes |
| Pass | 16/20 |
| Outcomes | LO-01, LO-02, LO-03, LO-04, LO-29 |
| Answer key | Separate file: `assessments/answer-keys/level-checks/lc-1-key.md` |

Answer without notes. Items 1–6 are worth 1 point, items 7–8 are worth 2 points, and items 9–10 are worth 5 points. For scenarios, use headings so the key can be compared element by element.

## 1. Authorized work (1 point)

Which activity is permitted in this course?

A. Testing a public demo API with crafted inputs  
B. Testing an isolated local replica built from synthetic data  
C. Scanning the campus network for model endpoints  
D. Using a leaked dataset from a former employer

## 2. Join cardinality (1 point)

A pandas merge returns far more rows than either input. Which check best detects the cause?

A. Compare row counts before and after, and check key uniqueness on both sides  
B. Increase the dataframe memory limit  
C. Drop all null values and merge again  
D. Sort the index before merging

## 3. Precision (1 point)

A model flags 10% of rows. Precision is 0.15 and recall is 0.75. Which statement is correct?

A. About 15% of flagged rows are true positives  
B. About 75% of all rows are flagged  
C. Accuracy is at least 0.90  
D. The model misses most positive rows

## 4. Trust boundary (1 point)

Which pair names a trust boundary and the change in authority it represents?

A. A float column becomes an integer column  
B. An anonymous internet caller becomes an authenticated API caller  
C. The training set grows from 10,000 to 20,000 rows  
D. The loss changes from cross-entropy to hinge loss

## 5. Scope (1 point)

True or false: a threat model should state what is out of scope, not only what is in scope.

## 6. Hash match (1 point)

True or false: if a dataset's SHA-256 matches the manifest, the data are correct and unbiased.

## 7. Leakage checks (2 points)

Name two checks that can reveal leakage before training, and state the corrective action for each.

## 8. Adversary profile (2 points)

Write a bounded adversary profile for a local student-risk predictor. Include goal, knowledge, access, and budget.

## 9. Scenario: the ready-model claim (5 points)

A report says:

> We trained on student records from 2019–2024 with a random 70/30 split, used `exit_interview` as a feature, and reached ROC-AUC 0.96. The model is ready for deployment. We did not find any threats.

Identify three protocol or reasoning errors, state the likely direction of each effect on the reported score or claim, and give a corrected protocol in four steps.

## 10. Scenario: the student-risk register (5 points)

Build a four-row threat register for a local student-risk model. For each row give the threat, impact (1–5), likelihood (1–5), score/band, one control classified as preventive or detective, and the AI RMF function it supports. Add one rejected threat with a reason and a reopening condition. Use only synthetic data.

## Scoring

| Score | Interpretation |
|---:|---|
| 18–20 | Strong. You can connect data handling, metrics, and threat reasoning. |
| 16–17 | Pass. Review the missed item and the linked lesson. |
| 12–15 | Not yet. Repeat LAB-01B and LAB-02, then retake. |
| Below 12 | Reread M00–M03 before continuing to Level 2. |
