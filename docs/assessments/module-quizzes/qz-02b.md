# Module 02 Alternate Quiz (QZ-02B)

| Field | Value |
|---|---|
| Module | M02 — Machine Learning Fundamentals and Evaluation |
| Quiz A | [QZ-02](../../modules/m02-ml-fundamentals/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-01, LO-28 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-02b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. Time-ordered data

You have five years of login events and a label that depends on future behavior. Which evaluation split is appropriate?

A. A random 80/20 row split  
B. A split by user ID only  
C. A chronological split: train on earlier events, test on later events  
D. A split that puts the largest users in the test set

## 2. Threshold selection

A team tries 50 thresholds on the test set, picks the one with the best F1, and reports that F1 as the test result. What is the main problem?

A. F1 cannot be computed for binary classifiers.  
B. The reported score is optimistic because the test set influenced the choice.  
C. The threshold must always be 0.5.  
D. The test set is too large to evaluate.

## 3. Accuracy and recall

True or false: a model can have 95% accuracy and 0% recall on the minority class.

## 4. Rare positives

True or false: when positives are rare, PR-AUC is usually more informative than ROC-AUC about performance at realistic operating points.

## 5. One split

Give two reasons a single train/test split can give a misleading estimate of model performance.

## 6. Confusion matrix

A model produces: TP = 30, FN = 10, FP = 20, TN = 140. Compute precision, recall, and F1. Show the formula for each.

## 7. Find the flaw

```python
model.fit(X, y)
accuracy = model.score(X, y)
print("test accuracy:", accuracy)
```

Identify the flaw, explain what the number actually measures, and state the minimum correction.

## 8. Scenario: the vendor number

A vendor reports ROC-AUC 0.92 and accuracy 0.85 for a fraud model. The positive rate is 2%, the threshold is 0.5, and no baseline or interval is given. Write three questions you would ask before recommending a pilot, and say why each matters.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can separate discrimination, calibration, and decision cost. |
| 10 | Pass. Review the missed item before LAB-01B. |
| 8–9 | Reread M02.L3–L4, especially thresholds, calibration, and leakage. |
| Below 8 | Reread M02 and rerun LAB-01B before continuing. |
