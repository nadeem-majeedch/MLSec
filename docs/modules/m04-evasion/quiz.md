---
title: Module 04 Knowledge Check — QZ-04
---

# Module 04 Knowledge Check — QZ-04

**10 items · 12 points · about 20 minutes · Pass 10/12**

Answer without looking at the lessons. Write your answers in `work/m04/quiz-answers.md`, then compare with [the answer key](quiz-answers.md). Each item states its point value.

---

## 1. Parts of an evasion claim (1 point)

Which set contains the five parts of a testable evasion claim?

A. Model, accuracy, dataset, paper, author  
B. Goal, knowledge, capability, budget, metric  
C. Loss, optimizer, learning rate, epoch, batch size  
D. Asset, boundary, surface, threat, control  

## 2. The L∞ norm (1 point)

For a perturbation vector δ, $\|\delta\|_\infty$ is:

A. The sum of the absolute changes  
B. The largest absolute change to any single coordinate  
C. The number of changed coordinates  
D. The square root of the sum of squares  

## 3. FGSM update (1 point)

For loss $J(x,y)$, budget ε, and pixels in [0, 1], the untargeted FGSM update is:

A. $x' = x - \epsilon \cdot \mathrm{sign}(\nabla_x J)$  
B. $x' = x + \epsilon \cdot \mathrm{sign}(\nabla_x J)$  
C. $x' = x + \epsilon \cdot \nabla_x J$  
D. $x' = x + \epsilon \cdot \mathrm{sign}(\nabla_\theta J)$  

## 4. The ε = 0 test (1 point)

Why must an evasion implementation return exactly zero perturbation and zero ASR at ε = 0?

A. Because the model is robust at small budgets  
B. Because it catches sign, projection, and restart bugs before they contaminate the curve  
C. Because the test set is empty  
D. Because ASR is undefined at ε = 0  

## 5. Base set (1 point)

An untargeted ASR is normally measured on:

A. Every row in the dataset  
B. Rows the clean model classifies correctly  
C. Only rows the clean model misclassifies  
D. Only the first 100 rows  

## 6. Targeted accuracy (1 point)

A test set has 1,000 rows, 120 of which truly have label 3. You run a targeted attack toward class 3. Which denominator is appropriate for targeted success?

A. 1,000  
B. 120  
C. The rows with label 3 that the clean model classifies correctly, excluded from the base  
D. The rows whose true label is not 3 and that the clean model classifies correctly  

## 7. PGD projection (1 point)

After each PGD step, the update must be projected onto:

A. The unit sphere  
B. The intersection of the ε-ball around the original input and the valid input range  
C. The set of integer pixel values  
D. The training distribution  

## 8. Transfer reasoning (1 point)

A perturbation changes the source model's prediction on 40% of a base set and the target model's prediction on 45%. Which statement is best?

A. The result is impossible  
B. The target is definitely more vulnerable than the source  
C. Transfer success depends on both models' boundaries and can exceed source success  
D. The target must share training data with the source  

## 9. Find the flaw (2 points)

The following code is meant to report white-box FGSM ASR at ε = 0.1.

```python
X_adv = np.clip(X_test - 0.1 * np.sign(grad), 0, 1)
asr = (model.predict(X_adv) != y_test).mean()
print(asr)
```

Name two flaws in the protocol and one likely consequence. (Assume `grad` is computed correctly for `X_test` and `y_test`.)

## 10. Evaluate the claim (2 points)

A blog post says: "We attacked an image classifier with PGD and got 99% success, so all image classifiers are insecure."

Give two reasons the conclusion does not follow from the experiment, and rewrite the claim so that it is supportable.
