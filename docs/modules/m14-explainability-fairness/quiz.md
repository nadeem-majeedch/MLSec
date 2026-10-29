---
title: Knowledge Check — QZ-14
---

# Knowledge Check — QZ-14

**Module 14 · 10 items · 14 points · about 20 minutes**

Answer without running LAB-18. For items 2, 3, 4, and 6, show the arithmetic.

---

**1. (1 point)** A logistic model has \(w = (1.5,\ -2.0,\ 0.5)\) and \(b = 0.1\). For \(x = (2.0,\ 1.0,\ -2.0)\), compute \(z\), the log-odds contribution of each feature, and state which feature contributes most.

---

**2. (2 points)** For the same model and input, compute \(p\), \(p(1-p)\), and the gradient×input attributions. Do the attributions sum to \(z\)? What does that tell you about the method?

---

**3. (1 point)** Using baseline 0, compute the occlusion attribution for each feature in the same example. Which feature has the largest absolute occlusion value?

---

**4. (2 points)** A model review reports a demographic-parity gap of 0.001 and an equalized-odds gap of 0.12. Explain how both can be true, and which group is affected by the larger error-rate difference if the FPRs are 0.26 and 0.14.

---

**5. (1 point)** A colleague says: "The explanations barely change under noise, so they are faithful." Identify the error.

---

**6. (2 points)** Group A has 200 rows: 60 TP, 40 FN, 30 FP, 70 TN. Group B has 100 rows: 30 TP, 20 FN, 10 FP, 40 TN. Compute each group's TPR, FPR, and selection rate, then the DP and equalized-odds gaps.

---

**7. (1 point)** Why can calibration, equal false-positive rate, and equal false-negative rate not all hold when group base rates differ?

---

**8. (1 point)** An explanation endpoint returns per-feature log-odds contributions and accepts arbitrary inputs. Describe the extraction procedure for a linear model with four features.

---

**9. (1 point)** What optimization does an explanation-manipulation attacker solve, and which constraint keeps the decision unchanged?

---

**10. (2 points)** Rewrite as a scoped statement: "Our model is fair and its explanations are stable, so it is safe to deploy."

---

*When you have finished, compare your answers with the [answer key](quiz-answers.md).*
