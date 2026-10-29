---
title: Module 00 Knowledge Check (QZ-00)
---

# Module 00 Knowledge Check (QZ-00)

**10 items · 20 minutes · Pass mark 80% · No time limit**

Answer every item before opening the [answer key](quiz-answers.md). Write your reasoning, not just the letter: the explanations are where most of the learning happens.

---

**1. (Classify)** A retail site's recommendation model performs poorly for a demographic group because that group was under-represented in the training data. Which label fits best?

A. Evasion
B. Poisoning
C. Quality or safety failure, not a deliberate security incident
D. Model extraction

---

**2. (Identify)** For each attack, name the primary asset at risk.

| Attack | Asset |
|---|---|
| A competitor queries your prediction API to train a copy | ? |
| An attacker adds a trigger that forces a fraud model to approve transactions | ? |
| An attacker floods the API with inputs that maximize compute | ? |

---

**3. (Apply)** An attacker alters the labels in a third-party dataset before it is used to train a model. Which lifecycle stage is the primary point of compromise?

A. Data collection or preparation
B. Packaging
C. Inference
D. Monitoring

---

**4. (Multi-select)** Which conditions are required before testing a system in this course? Select all that apply.

A. Ownership or explicit written permission
B. A defined scope and time window
C. A GPU
D. A safe data-handling and disclosure path

---

**5. (Interpret)** A manifest records `sha256(model.joblib) = a1b2...`. Later the hash is `9f8e...`. What does the mismatch prove?

A. The model is malicious
B. The file changed since the manifest was written
C. The model's accuracy decreased
D. The hash algorithm is broken

---

**6. (Numeric)** A training set has 50,000 examples. An attacker controls 500 labels. What is the poisoning rate as a percentage of the training set? Show the calculation.

---

**7. (Find the flaw)** The following code is meant to be reproducible. Identify **two** flaws.

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LogisticRegression()
model.fit(X_train, y_train)
joblib.dump(model, "model.joblib")
random.seed(42)
```

---

**8. (Classify)** An attacker uses the confidence values returned by an API to decide whether a specific patient record was used in training. Which adversary goal is this?

A. Availability
B. Integrity
C. Privacy
D. Intellectual property

---

**9. (Evaluate)** Which of the following is acceptable evidence for a lab claim? Select all that apply.

A. A screenshot of an accuracy number with no code
B. A script that runs from a clean environment with seeds and versions recorded
C. A metrics file plus the saved model and the indices of the evaluated rows
D. A result copied from a tutorial without running it

---

**10. (Scenario)** A stranger offers you an API key and asks you to "try to break" their company's fraud model over the weekend. They say written scope is unnecessary because "we trust you." What do you do, and why? Name at least three missing conditions from the authorization test.

---

When you have written your answers, open the [answer key](quiz-answers.md). Then complete the [exercises](exercises.md).
