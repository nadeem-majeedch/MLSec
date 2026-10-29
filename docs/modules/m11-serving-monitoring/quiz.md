---
title: Knowledge Check — QZ-11
---

# Knowledge Check — QZ-11

**Module 11 · 10 items · 14 points · about 20 minutes**

Answer without running LAB-14 or LAB-15. For items 4, 7, and 8, show the numbers you use.

---

**1. (1 point)** A caller presents a valid token that lacks the `stats` scope and calls `GET /stats`. Which status code is correct?

A. 400  
B. 401  
C. 403  
D. 429

---

**2. (2 points)** LAB-14 checks body size before authentication. An oversized body arrives with no `Authorization` header. Which status code should it receive, and what does the order protect? What would change if authentication ran first?

---

**3. (2 points)** A validator rejects a feature only when it is not numeric or when `x < 0 or x > 1`. Give two different dangerous values that can still pass this check, and state the additional check that rejects each.

---

**4. (2 points)** The limiter allows 10 requests per role per 60-second fixed window. A fresh role sends 12 requests. How many are allowed and how many receive 429? Name two limitations of this limiter in a production service.

---

**5. (1 point)** In LAB-15, which scenario produces only volume signals and is triaged as medium-severity abuse?

A. Benign drift  
B. Evasion attack  
C. Query burst  
D. Recovery

---

**6. (1 point)** Thresholds in LAB-15 are calibrated on which traffic?

A. The monitored baseline  
B. All monitored windows, pooled  
C. The quiet calibration period only  
D. The recovery windows

---

**7. (2 points)** LAB-15 replays a captured attack batch on the current and previous checkpoints. Attack success is 0.3507 on the current model and 0.3299 on the previous one. The criterion is `previous < 0.5 * current`. Is the rollback counted as restored? Explain the decision and name one condition that would make rollback a valid containment step.

---

**8. (1 point)** Edge squeezing changes attack success from 0.3507 to 0.1979 and clean accuracy from 0.9600 to 0.9433 on the replay batch. State one reason this is a limited mitigation rather than a fix.

---

**9. (1 point)** Name three places a credential must not be stored or emitted, and one production mechanism for supplying it instead.

---

**10. (1 point)** A report says: "All 18 security tests pass and no tokens appear in 28 log records, so the service is secure." Rewrite the claim as a scoped assurance statement.

---

*When you have finished, compare your answers with the [answer key](quiz-answers.md).*
