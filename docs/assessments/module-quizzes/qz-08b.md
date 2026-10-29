# Module 08 Alternate Quiz (QZ-08B)

| Field | Value |
|---|---|
| Module | M08 — Robustness Evaluation and Adversarial Defense |
| Quiz A | [QZ-08](../../modules/m08-robustness-defense/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-16, LO-17, LO-18 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-08b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. Empirical or certified?

Which statement is an **empirical** robustness result rather than a certified guarantee?

A. For every perturbation with $\|\delta\|_\infty \le 0.03$, accuracy is at least 0.80  
B. Under 40-step PGD at ε = 0.03 on this test set, accuracy was 0.82  
C. No input within the stated L2 ball can change the prediction  
D. The model is provably stable for all inputs in the declared region

## 2. The cost of adversarial training

What is the most common trade-off reported for adversarial training?

A. Lower clean accuracy in exchange for higher robust accuracy  
B. Higher clean accuracy with no change in robustness  
C. Elimination of the need for attack evaluation  
D. A guarantee against all future attacks

## 3. One failed attack

True or false: a defense that reports 0% attack success under a single gradient-based attack is proven robust.

## 4. Differentiability

True or false: input squeezing, as implemented in the lab, is differentiable, so a standard PGD attack evaluates the defended model fairly.

## 5. Gradient masking

Explain in one or two sentences what gradient masking is and why it can make a defense look stronger than it is.

## 6. Detector precision

A detector has TPR = 0.90 and FPR = 0.01. In a stream of 10,000 inputs, 2% are attacked.

Compute the number of true positives, false positives, and the precision of an alert. Show the counts.

## 7. Find the flaw

The code below is meant to measure robust accuracy for a model that applies a squeezing preprocessing step.

```python
X_adv = pgd_attack(model, X_test, y_test, eps=0.10, steps=40)
X_def = squeeze(X_adv)
robust_accuracy = (model.predict(X_def) == y_test).mean()
print("robust accuracy", robust_accuracy)
```

Identify two flaws and explain what the reported number overstates.

## 8. Scenario: the improvement claim

A vendor reports:

> Our defense improves robustness by 98%. We measured with FGSM at a fixed budget and saw attack success fall from 42% to 0.8%. No adaptive attack was necessary.

You are deciding whether to rely on this for a local deployment. Name three questions the report must answer, and rewrite the claim as one the evidence could support. Do not test the vendor's systems.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can distinguish a measured defense from a robustness claim. |
| 10 | Pass. Review the missed item before LAB-11. |
| 8–9 | Reread M08.L1, L4, and L6, especially adaptive evaluation. |
| Below 8 | Reread M08 and rerun LAB-11 with the adaptive attack enabled. |
