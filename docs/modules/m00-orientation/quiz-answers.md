# Module 00 Knowledge Check — Answers and Explanations

**QZ-00 · Answer key**

Score one point per item (item 4 and 9 require all correct selections for the point). Pass mark: 8/10.

---

### 1. C — Quality or safety failure

The failure has no adversary. Under-representation is a data-quality and fairness problem. The symptom (a subgroup performs worse) can resemble an attack, which is why intent and provenance matter. Evasion, poisoning, and extraction all require deliberate manipulation.

*Misconception check:* "Any model failure is a security incident." Security requires an adversary and a threat.

### 2. Asset identification

| Attack | Primary asset |
|---|---|
| API queries used to train a copy | Intellectual property: model functionality |
| Triggered misclassification of fraud | Integrity of decisions; financial assets |
| Inputs that maximize compute | Availability and cost of the service |

A secondary asset in the first row is the training data or model weights; in the second, customer trust. Naming a secondary asset is acceptable if you state why the primary one comes first.

### 3. A — Data collection or preparation

The compromise occurs before training, while data is collected or prepared. Training consumes the corrupted data; packaging and inference are later stages. This is poisoning, and the relevant controls are provenance, validation, and label auditing.

### 4. A, B, D

A GPU is not required, and the course is CPU-first. Ownership or permission, scope, and a data-handling and disclosure path are the non-negotiable conditions. Safe handling is also required, although it is not listed as a separate option.

### 5. B — The file changed

A hash mismatch proves that the bytes differ from those recorded. It says nothing about intent, accuracy, or the algorithm. The correct response is to stop, identify what changed, and regenerate the artifact from a known-good source.

### 6. 1%

Calculation: `500 / 50,000 = 0.01 = 1%`. The denominator must be the training set, not the test set or the full dataset. A targeted backdoor can succeed at a much lower rate than indiscriminate label flipping; the rate alone does not determine impact.

### 7. Two flaws

1. **No seed on the split.** `train_test_split` is called without `random_state`, so the rows change between runs.
2. **The seed is set after the split and after fitting.** It has no effect on the operations that matter. It should be set once at the top, and every randomized component should receive it explicitly.

A third issue is that only the estimator is saved, not the preprocessing. If a scaler was fitted earlier, reloading the model without it changes predictions. Any two correct flaws earn the point.

### 8. C — Privacy

The attacker learns whether a record was in the training set. That is membership inference, a privacy goal. Integrity would mean changing predictions; availability would mean degrading service; IP theft would mean copying functionality.

### 9. B and C

A reproducible script with recorded seeds and versions is evidence. A metrics file with the model and evaluated row indices is evidence. A screenshot without code and a copied tutorial number are not.

### 10. Model answer

Decline the engagement until the missing conditions are supplied. Missing items include:

- **Ownership or written permission** — a chat message is not a scoped authorization;
- **Defined scope** — no named endpoints, model version, time window, or excluded actions;
- **Data handling** — no statement about personal or customer data;
- **Disclosure path** — no named contact or remediation window;
- **Stop conditions** — no agreement on rate limits or destructive actions.

Even with permission, the course default is local, synthetic, or explicitly public targets. A production fraud API is out of scope. If the owner wants a legitimate assessment, they should provide written scope, a local replica or sandbox, synthetic data, and a security contact.

*Scoring note:* a response that accepts the key "because they gave permission" does not earn the point. Permission without scope and a disclosure path is not authorization.

---

## Score interpretation

| Score | Interpretation | Next step |
|---:|---|---|
| 9–10 | Strong start | Proceed to the exercises and LAB-01 |
| 8 | Passing with gaps | Re-read the explanations for missed items |
| 6–7 | Not yet | Re-read Lessons 00.1–00.3, then retake |
| 0–5 | Foundation missing | Complete the student guide's recovery path before LAB-01 |

Return to the [quiz](quiz.md) or continue to the [exercises](exercises.md).
