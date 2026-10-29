---
title: Module 03 Knowledge Check — QZ-03
---

# Module 03 Knowledge Check — QZ-03

**10 items · 12 points · about 20 minutes · Pass 10/12**

Answer without looking at the lesson. Write your answers in `work/m03/quiz-answers.md`, then compare with [the answer key](quiz-answers.md). Each item states its point value.

---

## 1. Asset identification (1 point)

Which of these is the best example of an **asset** in a model-serving system?

A. The HTTPS port number  
B. The training labels and override records  
C. The load balancer's hostname  
D. The firewall rule that allows port 443  

## 2. Trust boundaries (1 point)

A trust boundary is best described as:

A. A network subnet  
B. A line where data or authority crosses between parties with different privilege or assumptions  
C. Any place where encryption is used  
D. The edge of the model's input schema  

## 3. NIST goals (1 point)

Which four are attack goals in the NIST AI 100-2e2025 taxonomy?

A. Integrity  
B. Availability  
C. Privacy  
D. Abuse  
E. Confidentiality  
F. Fairness  

## 4. Attacker knowledge (1 point)

A **black-box** attacker is one who:

A. Has the model weights but not the training data  
B. Can query the model and observe outputs, but does not have the weights  
C. Has no access to the system at all  
D. Can read the source code but not the deployed model  

## 5. Severity arithmetic (1 point)

Using the course bands (1–4 low, 5–9 medium, 10–16 high, 17–25 critical), what is the severity of a threat with **impact 4** and **likelihood 3**?

A. Medium  
B. High  
C. Critical  
D. Low  

## 6. Surfaces and vulnerabilities (1 point)

Which pair correctly separates an **attack surface** from a **vulnerability**?

A. Surface: "the API is unauthenticated"; vulnerability: "the scoring endpoint"  
B. Surface: "the scoring endpoint"; vulnerability: "the endpoint accepts unauthenticated requests"  
C. Surface: "the model is inaccurate"; vulnerability: "the training data"  
D. Surface: "the vendor"; vulnerability: "the contract"  

## 7. ATLAS mapping (1 point)

Which verified MITRE ATLAS technique best fits a threat in which an insider changes training labels?

A. `AML.T0015` Evade AI Model  
B. `AML.T0020` Training Data Poisoning  
C. `AML.T0040` AI Model Inference API Access  
D. `AML.T0051` LLM Prompt Injection  

## 8. AI RMF function (1 point)

Assigning ownership for label provenance, vendor signing, and export approval is primarily which AI RMF function?

A. GOVERN  
B. MAP  
C. MEASURE  
D. MANAGE  

## 9. Find the flaw (2 points)

A draft register contains this row:

> **Threat:** Attackers could poison the model. **Severity:** High.

List at least **four** missing elements that a reviewer would need before accepting this row.

## 10. Scenario: rank three threats (3 points)

A hospital triage system has three accepted threats:

| Threat | Impact | Likelihood | Notes |
|---|---:|---:|---|
| T1 Adversarial image downgrades an urgent finding | 5 | 4 | Direct patient-safety path |
| T2 Insider flips override labels before retraining | 5 | 3 | Affects future model versions |
| T3 Competitor extracts the model through the API | 3 | 4 | IP and contractual harm |

**Tasks:**

1. Compute the score and band for each threat.
2. Rank them.
3. State one tie-break rule you would publish before ranking, and explain why it matters even when there is no tie.
4. Give one reason T3 might still deserve management attention despite its lower score.

---

## Scoring

| Item | Points |
|---|---:|
| 1–8 | 1 each |
| 9 | 2 |
| 10 | 3 |
| **Total** | **12** |

**Pass:** 10/12. If you score below 8, reread Lessons 1–3 before starting LAB-02. If you miss only item 10, reread Lesson 5's scoring and tie-break sections.
