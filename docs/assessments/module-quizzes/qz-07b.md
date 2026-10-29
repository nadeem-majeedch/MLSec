# Module 07 Alternate Quiz (QZ-07B)

| Field | Value |
|---|---|
| Module | M07 — Model Extraction, Membership Inference, and Model Inversion |
| Quiz A | [QZ-07](../../modules/m07-extraction-privacy/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-12, LO-13, LO-14, LO-15 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-07b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. The information ladder

Which prediction-API response generally reveals the most about the model per query?

A. The predicted class name only  
B. A ranked list of three class names with no scores  
C. The full probability vector over all classes  
D. The model's version string

## 2. What inversion produces

What does a model inversion attack most directly produce?

A. A representative input that scores highly for a chosen class  
B. Proof that a specific record was in the training set  
C. A copy of the model's weights  
D. The complete set of training labels

## 3. Fidelity and data theft

True or false: a surrogate with high fidelity to the teacher proves the attacker obtained the training data.

## 4. Low-FPR reporting

True or false: for privacy harm, TPR at FPR ≤ 1% is usually more informative than the overall accuracy of the membership classifier.

## 5. Extraction defenses

Name two defenses against model extraction. For each, state one benign cost the defense imposes.

## 6. Membership arithmetic

A candidate pool has 1,000 records, 10% of which are members. A membership test has TPR = 0.30 at FPR = 0.02.

Compute the number of true positives, the number of false positives, and the precision at this operating point. Then explain in one sentence why precision would fall if the member prevalence were 1% instead of 10%, with TPR and FPR unchanged.

## 7. Find the flaw

The code below is meant to report TPR at FPR ≤ 1% for a membership attack.

```python
fpr, tpr, thresholds = roc_curve(y_member, scores)
i = np.argmax(tpr)
print(f"TPR={tpr[i]:.3f} at FPR={fpr[i]:.3f}")
```

Identify two flaws and state the corrected selection rule.

## 8. Scenario: the health-risk API

A clinic runs a local prediction API that returns a probability for a health-risk class. You have synthetic records and written permission to test a local replica only.

Outline a bounded privacy assessment covering extraction, membership inference, and inversion. Name one metric and one baseline for each, plus two limits of the assessment. Do not use real patient data or test the production service.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can measure privacy risk without overstating it. |
| 10 | Pass. Review the missed item before LAB-10. |
| 8–9 | Reread M07.L1 and L3, especially low-FPR metrics and prevalence. |
| Below 8 | Reread all five lessons and rerun LAB-09 and LAB-10. |
