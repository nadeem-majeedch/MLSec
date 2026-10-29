---
title: Knowledge Check — QZ-09
---

# Knowledge Check — QZ-09

**Module 09 · 10 items · 14 points · about 20 minutes**

Answer without running LAB-12. For calculation items, show the units and the denominator.

---

**1. (1 point)** Which pair is correct?

A. Provenance is the graph of transformations; lineage is the legal terms.  
B. Provenance describes origin and context; lineage connects artifacts through activities.  
C. Provenance and lineage are synonyms.  
D. Lineage is only possible for neural networks.

---

**2. (2 points)** A transformation record contains the code reference and the output hash. Name four other fields needed to reproduce the transformation.

---

**3. (2 points)** LAB-12 reports 18 missing cells, 10 schema violations, 8 exact duplicate rows, and 4 label-conflict groups containing 8 rows. Explain why \(18+10+8+8=44\) is not the number of rows removed by repair, and state the actual number.

---

**4. (1 point)** `exit_survey` is recorded only after a customer leaves. The model uses it as a feature and reaches ROC-AUC 0.9584. Which leakage type is this?

A. Group leakage  
B. Temporal leakage only  
C. Target / post-outcome leakage  
D. Pipeline leakage

---

**5. (2 points)** LAB-12 reports 0.9584 with `exit_survey`, 0.7507 on identical rows without it, and 0.8485 after repair with a grouped split. Which comparison isolates the effect of the column, and what does the 0.1099 difference include?

---

**6. (1 point)** A dataset has multiple rows per customer. Which split protects the evaluation from entity leakage?

A. `train_test_split` with `random_state=13`  
B. `GroupShuffleSplit` grouped by `customer_id`  
C. A larger test set  
D. Stratification by the label

---

**7. (2 points)** A run record lists the model hyperparameters and the random seed. Name four additional fields needed for another person to reproduce the result.

---

**8. (1 point)** A dataset file's SHA-256 hash matches the manifest. What does this prove?

A. The data is correct and unbiased.  
B. The bytes match the recorded version; it does not prove the content is correct.  
C. The dataset came from a trusted source.  
D. The model trained on it is reproducible.

---

**9. (1 point)** Which statement best describes the data owner role?

A. The person who writes the training code.  
B. The role accountable for lawful and appropriate use, access, retention, and deletion decisions.  
C. The cloud administrator who manages storage.  
D. The auditor who samples controls.

---

**10. (1 point)** An audit trail must answer which four questions for a material action?

A. Cost, latency, accuracy, and version  
B. Who, what, when, and why  
C. Which model, which GPU, which epoch, and which metric  
D. Source, license, retention, and owner

---

*When you have finished, compare your answers with the [answer key](quiz-answers.md).*
