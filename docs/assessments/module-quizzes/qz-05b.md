# Module 05 Alternate Quiz (QZ-05B)

| Field | Value |
|---|---|
| Module | M05 — Training Data Poisoning and Label Manipulation |
| Quiz A | [QZ-05](../../modules/m05-poisoning/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-08, LO-09 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-05b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. Access without labels

Which attacker position lets an adversary change how training rows are joined or deduplicated **without** submitting a single labelled row?

A. Label-only submission through the public intake form  
B. Access to the preprocessing or pipeline code  
C. Query access to the deployed prediction API  
D. Read access to the model's published evaluation report

## 2. Availability effect

Which outcome is the characteristic goal of an **availability** poisoning attack?

A. One chosen input class is redirected while overall accuracy stays stable  
B. Broad degradation of accuracy across many classes  
C. Extraction of the model's weights from the API  
D. Inference about whether a record was in the training set

## 3. Unchanged accuracy

True or false: a poisoning attack that leaves test accuracy unchanged has failed.

## 4. Screening and clean labels

True or false: reference-set screening is equally effective against a clean-label attack that places correctly labelled rows near the target boundary.

## 5. Corrupted test set

A team finds that 40 test labels were altered. Explain in one sentence why this is not a poisoning attack, and name the correct way to report it.

## 6. Two poison rates

A clean training set has 2,000 rows. The attacker appends 50 poisoned rows.

Compute the poison rate against the clean training set and against the augmented set. State which denominator the course requires and why the difference matters for comparing results.

## 7. Find the flaw

The code below is meant to evaluate a label screen.

```python
scores = screen(X_train)
threshold = scores[poison_idx].min()
flagged = scores <= threshold
caught = flagged[poison_idx].sum()
print(f"caught {caught}/{len(poison_idx)}, false positives 0")
```

Identify two flaws and explain why the reported catch rate is not evidence about future data.

## 8. Scenario: the signed feed

A data vendor says:

> Our feed is deduplicated and cryptographically signed. An attacker cannot insert rows, so poisoning is not in our threat model.

You are assessing the feed for a local model you own. Identify three gaps in the argument and outline a bounded verification plan using synthetic or licensed data. Do not test the vendor's production systems.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can separate data integrity from data correctness. |
| 10 | Pass. Review the missed item before LAB-06. |
| 8–9 | Reread M05.L1 and L4, especially denominators and screening assumptions. |
| Below 8 | Reread all four lessons and rerun LAB-05 with a prediction recorded first. |
