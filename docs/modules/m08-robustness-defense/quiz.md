---
title: Knowledge Check — QZ-08
---

# Knowledge Check — QZ-08

**Module 08 · 10 items · 14 points · about 20 minutes**

Answer without running LAB-11. For calculation items, show the counts and the denominator. The answer key explains the reasoning, not only the final number.

---

**1. (1 point)** Which set of five parts makes a robustness claim testable?

A. Model, adversary, norm and budget, base set, metric  
B. Accuracy, loss, optimizer, learning rate, epochs  
C. Dataset, vendor, price, latency, uptime  
D. Attack name, paper, year, venue, DOI

---

**2. (2 points)** A model has 200 test rows. It classifies 180 correctly before any attack. An untargeted attack changes 45 of those 180 predictions.

Compute clean accuracy, attack success rate (ASR), and robust accuracy. State each denominator.

---

**3. (1 point)** An undefended model has ASR 0.3582 on 522 clean-correct rows. An adversarially trained model has ASR 0.1809 on 481 clean-correct rows. Why is robust accuracy the fairer cross-model comparison?

A. ASR cannot be computed when clean accuracies differ.  
B. ASR uses each model's own base set, while robust accuracy uses the same test rows for both.  
C. Robust accuracy is always larger than ASR.  
D. The two models were evaluated at different budgets.

---

**4. (1 point)** Adversarial training solves which problem?

A. \(\min_\theta \mathbb{E}[L(f_\theta(x), y)]\)  
B. \(\min_\theta \mathbb{E}[\max_{\|\delta\|_\infty \le \epsilon} L(f_\theta(x+\delta), y)]\)  
C. \(\max_\theta \mathbb{E}[L(f_\theta(x), y)]\)  
D. \(\min_\delta \mathbb{E}[L(f_\theta(x+\delta), y)]\)

---

**5. (1 point)** A model is adversarially trained at ε = 0.10 and evaluated at ε = 0.20. What is the expected direction of change, and what does it imply about the claim?

A. ASR decreases; the defense is stronger at larger budgets.  
B. ASR increases; the defense has an operating range and no guarantee beyond it.  
C. ASR is unchanged; adversarial training is budget-independent.  
D. ASR becomes undefined outside the training budget.

---

**6. (1 point)** In BPDA, the attacker:

A. trains a copy of the model and transfers perturbations.  
B. uses the true transform in the forward pass and a differentiable substitute in the backward pass.  
C. removes the transform before querying the model.  
D. maximizes the number of queries until the defense rate-limits.

---

**7. (2 points)** In LAB-11 at ε = 0.10, the naive attack against squeezing reaches ASR 0.1871 and the BPDA adaptive attack reaches 0.1832. At ε = 0.20, the adaptive attack reaches 0.9981. Explain what these three numbers do and do not support. Give two distinct conclusions.

---

**8. (2 points)** A detector has TPR = 0.90 and FPR = 0.05. The deployed base rate of attacked inputs is 1%. Compute the precision of an alert. Show the counts for 10,000 inputs.

---

**9. (1 point)** A lab checker passes. What has been demonstrated?

A. The defense is secure.  
B. The artifacts are consistent with the reference experiment within the stated tolerance.  
C. The attack is the strongest possible.  
D. The result generalizes to other datasets.

---

**10. (2 points)** A report says: "Our defense reduces attack success from 40% to 2%, so the model is robust." Name four missing elements that would make this a scoped claim.

---

*When you have finished, compare your answers with the [answer key](quiz-answers.md).*
