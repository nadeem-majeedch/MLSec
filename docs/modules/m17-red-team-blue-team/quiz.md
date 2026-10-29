---
title: Knowledge Check — QZ-17
---

# Knowledge Check — QZ-17

**Module 17 · 10 items · 15 points · about 20 minutes**

Answer without opening the RT-01 brief. Items 2, 5, 7, and 9 ask you to audit a design or a claim.

---

**1. (1 point)** Which section of a rules-of-engagement document is most often missing, and what does its absence usually cause?

A. Authorization  
B. Non-goals  
C. Communications  
D. Data handling

---

**2. (1 point)** Audit this scope statement:

> "In scope: the scoring API. Out of scope: everything else."

Name two concrete problems and rewrite the in-scope line so an evaluator could enumerate it.

---

**3. (1 point)** Rewrite "test the model for weaknesses" as a red objective with an access assumption, a budget, and a measurable success criterion.

---

**4. (2 points)** A red-team plan allocates 900 of 2,000 requests to one evasion test. After that test, the team wants to run an extraction test with a 500-request hypothesis. The session has used 1,650 requests. What should happen, and what two things must the report state about the extraction test?

---

**5. (2 points)** A detection rule for extraction querying fires on 40 benign requests out of 10,000 during the quiet baseline, and on 18 of 20 red-team queries in the test split. Compute the observed false-positive rate, state what precision you can and cannot conclude, and explain why.

---

**6. (2 points)** Assume 0.2% of requests are malicious. A detector has 90% recall and a 0.5% false-positive rate. Over 100,000 requests, compute the number of true positives, false positives, and the precision of an alert. State one implication for the analyst queue.

---

**7. (2 points)** A mitigation is described as follows:

> "M-07 blocks the attack: the original script now receives 403. We also tested a variant, which was the same script with a different seed. Both were blocked, so the control generalizes."

Identify the problem with the variant and propose two stronger variants.

---

**8. (1 point)** Define time to detect and time to triage, including the start and end events of each, and explain why the first alert of any kind is not the right end point for time to detect.

---

**9. (2 points)** Red reports a quota bypass using a second API key. Blue reports 100% detection of quota abuse on the first key. Neither report mentions the other. What is the gap, what artifact exposes it, and what control would address it?

---

**10. (1 point)** Which is the best residual-risk statement?

A. "Residual risk is low after the fixes."  
B. "No attacks succeeded after mitigation, so the system is secure."  
C. "Under RD-01 with 2,000 requests, a two-key slow-ramp variant still lowers the target segment block rate to 0.09; tenant-level quotas are recommended but not implemented."  
D. "The remaining risk is accepted by the team."

---

*When you have finished, compare your answers with the [answer key](quiz-answers.md).*
