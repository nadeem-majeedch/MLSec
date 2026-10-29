# Module 06 Alternate Quiz (QZ-06B)

| Field | Value |
|---|---|
| Module | M06 — Backdoor Attacks, Trojan Models, and Trigger-Based Behavior |
| Quiz A | [QZ-06](../../modules/m06-backdoors/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-10, LO-11 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-06b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. Separating the two behaviors

Which pair of measurements best separates a backdoor's conditional behavior from its ordinary performance?

A. Test-set size and training time  
B. Clean accuracy on untriggered inputs and ASR on triggered inputs  
C. Training loss and number of epochs  
D. Precision and recall on untriggered inputs

## 2. What counts as a trigger?

Which item is a trigger in the sense used in this module?

A. A fixed 3×3 patch added to the corner of an input  
B. A different random noise vector for every input  
C. A corrected label in the training set  
D. A change to the train/test split ratio

## 3. Clean accuracy

True or false: high clean accuracy on a held-out test set rules out a backdoor.

## 4. Scan thresholds

True or false: lowering a trigger-scan threshold so that more positions are flagged will generally increase the number of false positives.

## 5. The clean-source baseline

Why must a backdoor report include the clean model's target-class rate on the same triggered source rows? Answer in one or two sentences.

## 6. Appended rows

A clean training set has 1,500 rows. The attacker appends triggered rows equal to 6% of the clean set.

Compute the number of poisoned rows, the poison rate against the clean set, and the poison rate against the augmented set. State which denominator the course requires.

## 7. Find the flaw

The code below is meant to decide whether a local model is backdoored.

```python
patched = add_patch(X_test, position=(0, 0))
score = model.predict_proba(patched)[:, 1].mean()
print("backdoor" if score > 0.5 else "no backdoor")
```

Identify two flaws and explain why a "no backdoor" result from this code is not evidence of absence.

## 8. Scenario: the opaque checkpoint

A vendor supplies a compiled classifier and a clean-accuracy figure, but no training data and no training code. You may run it locally on synthetic or licensed inputs.

Design a bounded black-box test plan for a possible backdoor. Name the measurements, the baseline each needs, and two limits of what the result can establish. Do not attempt to access the vendor's systems.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can test conditional behavior without overclaiming. |
| 10 | Pass. Review the missed item before LAB-08. |
| 8–9 | Reread M06.L1 and L3, especially baselines and scan assumptions. |
| Below 8 | Reread all four lessons and rerun LAB-07 with a recorded prediction. |
