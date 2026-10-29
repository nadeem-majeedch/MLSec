---
title: Knowledge Check — QZ-18
---

# Knowledge Check — QZ-18

**Module 18 · 10 items · 15 points · about 20 minutes**

Answer without opening the capstone brief. Items 2, 3, 5, 6, and 8 ask you to audit a plan, a result, or a report.

---

**1. (1 point)** Which is the best capstone question?

A. "How can we make machine learning systems more secure?"  
B. "Does a feature-delta detector reduce bounded evasion in a local credit-scoring API without raising false declines above 2%?"  
C. "An investigation of adversarial machine learning."  
D. "Can we improve robustness with adversarial training?"

---

**2. (2 points)** A proposal says:

> "I will investigate LLM security. I will run prompt-injection attacks against a local model, try several defenses, and write a report."

Name three defects that prevent this from being a capstone, and rewrite the objective as one falsifiable question.

---

**3. (2 points)** At week 9, a student reports: "The defense looks great — ASR dropped from 0.61 to 0.09. I overwrote the old baseline when I changed the threshold, but the new baseline is close." Which milestone gate failed, what evidence is missing, and what should happen before the defense claim is reported?

---

**4. (1 point)** Which item must **not** be committed to a public repository?

A. `requirements.txt` with exact versions  
B. The data generator and its seed  
C. A 2 GB model checkpoint and the licensed dataset  
D. `manifest.json` with artifact hashes

---

**5. (2 points)** A defense is evaluated with three seeds: ASR = 0.30, 0.42, 0.55. The undefended baseline is 0.60 from a single seed. State what can and cannot be concluded, and what you would report.

---

**6. (2 points)** A figure is a bar chart with a y-axis from 0.72 to 0.79, no error bars, and the caption "Defense improves robustness." Name three problems and rewrite the claim and caption so they are defensible.

---

**7. (1 point)** Which is the best report of a negative result?

A. "The attack failed, so the model is robust."  
B. "Attack A succeeded 0 of 200 times at ε = 4/255; the 95% upper bound is about 1.5%."  
C. "No effect was observed, proving the defense works."  
D. "The attack is impossible under our threat model."

---

**8. (2 points)** Classify each limitation as construct, internal, external, or statistical.

A. ASR is used as a proxy for customer harm, but the link is not validated.  
B. The defense was trained on a different split from the baseline.  
C. All results come from one synthetic dataset and one model family.  
D. Three seeds produce intervals that overlap with the baseline.

---

**9. (1 point)** Which is a researchable gap rather than a topic?

A. "AI security in healthcare."  
B. "Nobody has studied adversarial examples."  
C. "Detector evaluations report recall at one pacing rate; it is unknown whether recall survives adaptive pacing at a fixed false-positive budget."  
D. "Adversarial examples are a serious problem."

---

**10. (1 point)** Which scope cut destroys the capstone's claim?

A. Reducing three attack families to one and stating the narrower claim  
B. Dropping the evaluation-set hash because it changes when the data is regenerated  
C. Using one dataset instead of two and disclosing the external-validity limit  
D. Running three seeds instead of five and reporting wider intervals

---

*When you have finished, compare your answers with the [answer key](quiz-answers.md).*
