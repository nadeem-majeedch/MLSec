---
title: Knowledge Check — QZ-07
---

# Knowledge Check — QZ-07

**Module 07 · 10 items · 12 points · about 20 minutes**

Answer without running the labs. Write down your reasoning for the calculation and short-answer items; the answer key explains the expected reasoning, not just the final number.

---

**1. (1 point)** Which attack answers the question "was this record used to train the model?"

A. Model extraction  
B. Membership inference  
C. Model inversion  
D. Label flipping

---

**2. (1 point)** A surrogate agrees with its teacher on 90% of a test set but matches the true labels on 60%. Which statement is correct?

A. Fidelity is 0.90 and task accuracy is 0.60.  
B. Fidelity is 0.60 and task accuracy is 0.90.  
C. Both are 0.90 because the teacher is the reference.  
D. The numbers are inconsistent; fidelity cannot exceed accuracy.

---

**3. (1 point)** In LAB-09, active selection reaches fidelity 0.4793 at 50 queries while random sampling reaches 0.7620. What is the best explanation?

A. The entropy calculation is inverted.  
B. The temporary surrogate is too weak after 20 seed queries, so its uncertainty estimates are uninformative.  
C. The random forest cannot be trained on fewer than 100 points.  
D. Active learning always loses at small budgets by definition.

---

**4. (2 points)** A membership attack has TPR = 0.228 at FPR = 0.05. The candidate pool is 10% members. Compute precision at this operating point. Show the numerator and denominator.

---

**5. (1 point)** A report says "ROC-AUC is 0.82, so the attack identifies members 82% of the time." What is wrong with that sentence?

A. AUC cannot be computed for membership inference.  
B. AUC is a threshold-free ranking measure; it is not the detection rate at a chosen operating point.  
C. 0.82 is below the accepted threshold for a privacy attack.  
D. The sentence is correct if the model returns probabilities.

---

**6. (2 points)** Give three distinct reasons why a high predicted confidence is not proof that a record was in the training set.

---

**7. (1 point)** In the inversion objective

$$
x^{*} = \arg\max_{x} \; \log f_y(x) - \lambda R(x),
$$

what role does $R(x)$ play?

A. It measures the model's accuracy on the training set.  
B. It selects a plausible input among the many that produce a high score.  
C. It guarantees that the recovered input is a training record.  
D. It converts the model's probabilities into hard labels.

---

**8. (1 point)** A team replaces a probability API with a hard-label API to reduce membership inference and inversion risk. Which statement is most accurate?

A. Both attacks are eliminated because confidence is no longer exposed.  
B. The signal is reduced, but label-only extraction and repeated-query attacks can remain; the residual risk must be measured.  
C. Membership inference becomes impossible but extraction becomes easier.  
D. Hard labels improve membership inference because they are less noisy.

---

**9. (1 point)** Which statement accurately describes a limitation of LAB-10?

A. It measures a deployed production model.  
B. It uses private patient records.  
C. It tests one score, one split, and same-distribution nonmembers.  
D. It includes shadow models and a likelihood-ratio attack.

---

**10. (1 point)** A vendor reports "AUC 0.90, so the privacy risk is high; our defense reduces it by 60%." Name two things the report is missing before you could act on it.

---

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Ready for the exercises and a written risk memo |
| 8–10 | Review the missed lesson sections, then retake |
| 5–7 | Reread Lessons 07.2–07.4 and redo the calculations |
| 0–4 | Work through the module in order; do not skip the labs |

Answers and explanations: [quiz-answers.md](quiz-answers.md).
