# Module 03 Alternate Quiz (QZ-03B)

| Field | Value |
|---|---|
| Module | M03 — Cybersecurity Fundamentals and ML Threat Modeling |
| Quiz A | [QZ-03](../../modules/m03-threat-modeling/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-02, LO-03, LO-04 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-03b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. Goal or capability?

Which item is an adversary **capability** rather than a goal?

A. Steal the model's weights  
B. Cause a targeted misclassification  
C. Send 1,000 queries to the prediction endpoint  
D. Read a patient's record

## 2. Boundary and privilege

Which pair correctly names a trust boundary and the privilege change it represents?

A. The model's input schema; a change from float to integer  
B. The public internet to an authenticated API; anonymous caller to authenticated caller  
C. The training set; a change from 10,000 to 20,000 rows  
D. The loss function; a change from cross-entropy to hinge loss

## 3. Rejected threats

True or false: a threat model should record rejected threats and the reason each was rejected.

## 4. Severity band

True or false: under the course bands (1–4 low, 5–9 medium, 10–16 high, 17–25 critical), a threat with impact 4 and likelihood 3 is **high**.

## 5. Controls

Name two controls for a high-severity threat to training-label integrity, and classify each as preventive or detective.

## 6. Residual risk

A threat has impact 5 and likelihood 4. A control reduces the likelihood to 2 without changing the impact. Compute the inherent score, the residual score, the band for each, and the percentage reduction in the score.

## 7. Find the flaw

An attack tree contains one node:

> Hack the model.

Identify three properties that make this unusable as an attack tree, and state what a usable first branch would contain.

## 8. Scenario: the downgraded scan

A clinical triage assistant ingests scan images and suggests urgency. One accepted threat is: "An adversary modifies a scan so that an urgent finding is downgraded."

Write an adversary profile with goal, knowledge, access, and budget, then propose one testable detection hypothesis. Keep the profile bounded to a local or authorized setting.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can turn a threat into a test. |
| 10 | Pass. Review the missed item before LAB-02. |
| 8–9 | Reread M03.L2–L5, especially adversary profiles and residual risk. |
| Below 8 | Reread M03 and rebuild the LAB-02 register. |
