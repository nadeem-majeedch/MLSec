# Module 00 Alternate Quiz (QZ-00B)

| Field | Value |
|---|---|
| Module | M00 — How to Use This Self-Study Course |
| Quiz A | [QZ-00](../../modules/m00-orientation/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-01, LO-28, LO-29 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-00b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points. Write your reasoning for items 5, 7, and 8.

## 1. Classify the failure

A retail model's accuracy falls sharply after a vendor changes a featured column from dollars to cents. No attacker is involved, and the schema check was never updated. Which label fits best?

A. Evasion  
B. Data poisoning  
C. A data-quality and operational failure, not a deliberate security incident  
D. Model extraction

## 2. The auditor role

Which task belongs most directly to an **auditor** rather than to a red team or a model owner?

A. Exploit the model to demonstrate a vulnerability  
B. Independently verify that controls exist and that the evidence supports the claim  
C. Approve the model for deployment  
D. Write the model's training code

## 3. Hash mismatch

True or false: if a file's SHA-256 hash no longer matches the manifest, the file is proven to be malicious.

## 4. Local replica

True or false: testing a locally built replica of a service is acceptable when the exercise's authorization covers the replica, even if the original service belongs to someone else.

## 5. Negative evidence

A colleague says: "We tried an attack and nothing happened, so the system is secure." Give two reasons this is weak security evidence.

## 6. Seed spread

An attack is run with three seeds and succeeds on 0.20, 0.25, and 0.24 of the base set. Compute the mean and the range. State the result to three decimal places.

## 7. Find the flaw

An experiment log says:

> We ran the attack and saw about 80% success. We then changed the perturbation budget until the curve looked strong and reported the best run.

Identify two flaws and explain how each affects the reported number.

## 8. Scenario: the local finding

While testing a local mock that copies a vendor's production API, you find a behavior that would probably work against the vendor's real service. You have no authorization for the real service. What do you do? Name the immediate action, the evidence you keep, and the disclosure path.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You separate evidence from assertion. |
| 10 | Pass. Review the missed item before M01. |
| 8–9 | Reread M00.L1–L3, especially the evidence standard and rules of engagement. |
| Below 8 | Reread M00 and rewrite the authorized-use statement before continuing. |
