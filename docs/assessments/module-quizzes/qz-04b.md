# Module 04 Alternate Quiz (QZ-04B)

| Field | Value |
|---|---|
| Module | M04 — Adversarial Examples and Evasion Attacks |
| Quiz A | [QZ-04](../../modules/m04-evasion/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-05, LO-06, LO-07 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-04b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. Untargeted or targeted?

An attacker perturbs a correctly classified input until the model outputs **any** label other than the true one. Which description fits?

A. A targeted attack toward a chosen class  
B. An untargeted attack  
C. A poisoning attack  
D. A membership inference attack

## 2. Steps and restarts

Two PGD runs use the same L∞ budget and the same number of steps, but one uses three random restarts. What does the three-restart run most directly change?

A. The size of the allowed perturbation  
B. The number of search starting points, and therefore the chance of finding a stronger example  
C. The model's clean accuracy  
D. The definition of the success metric

## 3. Valid input domain

True or false: after each PGD step, the perturbed input must be projected back into the valid input range as well as into the ε-ball around the original input.

## 4. Black-box gradients

True or false: a transfer attack requires the attacker to compute gradients through the target model.

## 5. Why a base set?

In one sentence, explain why untargeted ASR is usually reported on rows the clean model classifies correctly rather than on the whole test set.

## 6. Two denominators

A test set has 400 rows. The clean model classifies 360 of them correctly. Under a stated attack, 90 of those 360 clean-correct rows change to a wrong label. No other row changes.

Compute the untargeted ASR on the base set and the robust accuracy over the full 400-row test set. Show both denominators.

## 7. Find the flaw

The code below is described as "FGSM at ε = 0.10".

```python
asr_hits = 0
for i in range(len(X_test)):
    eps = 0.10
    x_adv = X_test[i].copy()
    while model.predict(x_adv[None, :])[0] == y_test[i] and eps <= 0.50:
        eps += 0.10
        x_adv = np.clip(X_test[i] + eps * np.sign(grad[i]), 0, 1)
    asr_hits += int(model.predict(x_adv[None, :])[0] != y_test[i])
print(asr_hits / len(X_test))
```

Identify two protocol flaws and one consequence for the reported number.

## 8. Scenario: the robustness number

A vendor reports:

> Our classifier is 99.2% robust at ε = 0.01. We evaluated with 5-step PGD, one restart, and a fixed step size. No adversarial example changed a prediction on our 2,000-image test set, so the model is robust for deployment.

You are reviewing the claim for a local deployment decision. Name three questions the report must answer before the number can be interpreted, and rewrite the claim as one the stated evidence could support. Do not propose testing any system you do not own.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can separate a measured attack result from a robustness claim. |
| 10 | Pass. Review the missed item before LAB-11. |
| 8–9 | Reread M04.L5 and the robust-accuracy section, then retake. |
| Below 8 | Reread M04 and rerun LAB-03 and LAB-04 with a written prediction first. |
