---
title: Knowledge Check — QZ-12
---

# Knowledge Check — QZ-12

**Module 12 · 10 items · 14 points · about 20 minutes**

Answer without running LAB-16. For items 2, 5, and 7, show the numbers you use.

---

**1. (1 point)** In a FedAvg round, what does a client send to the coordinator?

A. Its raw training data  
B. A model update or locally trained weights  
C. The coordinator's private key  
D. Only the number of rows it holds

---

**2. (2 points)** Three clients with 200, 300, and 500 rows return updates \((0.2, -0.1)\), \((0.4, 0.2)\), and \((-0.2, 0.3)\). Compute the sample-weighted mean update.

---

**3. (2 points)** Eight equal clients participate. One attacker scales its update by 5 and also doubles its declared sample count. Explain why its effective influence is larger than \(5/12\), and state one control that bounds each source of influence.

---

**4. (1 point)** A coordinate-wise trimmed mean removes \(m\) values from each tail of each coordinate. Which condition must hold?

A. \(m \ge K\)  
B. \(2m < K\)  
C. \(m = K/2\)  
D. \(m\) can be any value

---

**5. (2 points)** For the five scalar updates \(0.5,\ 0.6,\ 0.7,\ 0.8,\ 9.0\), compute the mean, the 1-trimmed mean, and the median.

---

**6. (1 point)** Krum requires \(K \ge 2m + 3\). With \(K = 9\), what is the largest integer \(m\) the condition allows?

A. 2  
B. 3  
C. 4  
D. 9

---

**7. (2 points)** LAB-16 reports clean accuracy 0.8944 and attack success 0.6276 for norm clipping. A colleague says clipping "mostly worked" because accuracy is near the benign 0.9000. Explain what the two numbers show and why the conclusion is wrong.

---

**8. (1 point)** Does secure aggregation prevent a malicious client from poisoning the global model? Explain in one or two sentences.

---

**9. (1 point)** A vendor compares its robust aggregator after 40 rounds with plain FedAvg after 10 rounds and reports a 99.9% reduction in attack success. Name the main flaw in the comparison.

---

**10. (1 point)** Rewrite "the trimmed mean makes federated learning robust to poisoning" as a scoped assurance statement.

---

*When you have finished, compare your answers with the [answer key](quiz-answers.md).*
