# Module 14 Alternate Quiz (QZ-14B)

| Field | Value |
|---|---|
| Module | M14 — Explainability, Fairness, and Their Trade-offs |
| Quiz A | [QZ-14](../../modules/m14-explainability-fairness/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-31, LO-32 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-14b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. What an attribution is

A feature-attribution method reports that a feature contributed +0.3 to a prediction. What does this establish?

A. The feature causes the outcome for every input  
B. The model's local behavior under that method and baseline, not a causal effect  
C. The feature is fair to use  
D. The explanation is stable under all input changes

## 2. Stability

An explanation method is **stable** when:

A. It produces exactly the same attribution for every input  
B. Small changes to the input produce small changes in the attribution under a stated metric  
C. Its attributions sum to the prediction  
D. A human agrees with the ranking

## 3. Fairness metrics

True or false: a model with equal selection rates across two groups necessarily has equal true-positive and false-positive rates.

## 4. Explanation access

True or false: an explanation endpoint that accepts arbitrary inputs can disclose information about a model even when predictions are not returned.

## 5. Metric trade-off

Name two group-fairness metrics and explain in one sentence why they can conflict when group base rates differ.

## 6. Group arithmetic

Group A has 200 rows: 60 TP, 20 FN, 20 FP, 100 TN. Group B has 100 rows: 20 TP, 20 FN, 5 FP, 55 TN.

Compute each group's TPR, FPR, precision, and selection rate. Then compute the demographic-parity gap and the equalized-odds gaps for TPR and FPR.

## 7. Find the flaw

A reviewer compares two explanation methods and concludes:

```python
attr_a = shap_values(model, X)
attr_b = gradient_x_input(model, X)
print("method A is better because its mean |attribution| is larger")
```

Identify two flaws in the comparison and explain what the magnitude does not show.

## 8. Scenario: the loan review

A local lending model is being reviewed for subgroup performance and explanation stability. You have a de-identified synthetic dataset and may run only local experiments.

Outline the review: the groups and metrics, how you will report uncertainty, one stability test, one mitigation, and two limits of the conclusion. Do not use real applicant data.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can separate explanation, stability, fairness, and causation. |
| 10 | Pass. Review the missed item before LAB-18. |
| 8–9 | Reread M14.L3–L5, especially metric conflicts and stability limits. |
| Below 8 | Reread M14 and rerun LAB-18 with the subgroup table completed. |
