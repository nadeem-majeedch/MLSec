# Module 17 Alternate Quiz (QZ-17B)

| Field | Value |
|---|---|
| Module | M17 — Red Team / Blue Team Exercise |
| Quiz A | [QZ-17](../../modules/m17-red-team-blue-team/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-34 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-17b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. Before testing

Which artifact must exist before any red-team action begins?

A. A signed authorization naming the target, time window, limits, and stop conditions  
B. A list of every technique the team might try  
C. A blue-team detection dashboard  
D. A model card with accuracy numbers

## 2. A measurable objective

Which red objective is measurable?

A. "Find weaknesses in the target."  
B. "Lower the target class's recall below 0.50 on a frozen 200-row set within 500 queries and an L∞ budget of 8/255."  
C. "Test the model for evasion."  
D. "Assess whether robustness is adequate."

## 3. Budget discipline

True or false: a red action that stays within the written request, time, and perturbation budget is acceptable even if a larger test would produce a more interesting result.

## 4. Detection precision

True or false: a blue team can compute alert precision from TPR and FPR alone, without knowing the base rate of malicious traffic.

## 5. Evidence handling

Why should evidence be preserved before containment changes the system? Answer in one or two sentences.

## 6. Alert-queue arithmetic

A detector has 95% recall and a 1% false-positive rate. Of 200,000 requests, 0.5% are malicious.

Compute the true positives, false positives, total alerts, and precision. Then state one implication for an analyst who can review 20 alerts per hour.

## 7. Find the flaw

A blue-team detection rule is presented as ready for deployment:

```python
if requests_per_minute > 100:
    alert("possible extraction")
```

Identify two flaws and propose a corrected design. Keep the proposal measurable.

## 8. Scenario: the local exercise

Design a bounded red/blue exercise for a local model API that you own. Include the rules-of-engagement elements, one red objective with a budget, one blue detection with a false-positive measurement, an adaptive retest, and one residual risk. Do not target any third-party system.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can run an exercise that produces attributable evidence. |
| 10 | Pass. Review the missed item before RT-01. |
| 8–9 | Reread M17.L2 and L5, especially budgets and detection cost. |
| Below 8 | Reread M17 and rebuild the RoE and test plan. |
