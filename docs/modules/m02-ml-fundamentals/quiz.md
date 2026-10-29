---
title: Module 02 Knowledge Check
---

# Module 02 Knowledge Check

**QZ-02 · 10 items · 20 minutes · Pass mark 80%**

Answer without looking at the [answer key](quiz-answers.md). Write your reasoning for items 3, 5, 8, and 10; a correct letter with wrong reasoning is a miss.

---

## Item 1 — Unit of prediction

A bank trains a model on one row per card transaction to predict whether a **customer** will default within 90 days. Each customer has many transactions, and the default label is copied onto every transaction.

What is the unit of prediction, and what split strategy is appropriate?

A. Transaction; random row split
B. Customer; random row split
C. Customer; group split by customer
D. Transaction; group split by transaction

---

## Item 2 — Majority baseline

A fraud dataset has 2% positives. A classifier predicts "not fraud" for every row.

What is its accuracy, and what is its recall for the fraud class?

A. 2% accuracy, 100% recall
B. 98% accuracy, 0% recall
C. 98% accuracy, 2% recall
D. 50% accuracy, 50% recall

---

## Item 3 — Compute precision and recall

A model produces this confusion matrix on 1,000 transactions:

| | Predicted fraud | Predicted not fraud |
|---|---:|---:|
| **Actual fraud** | 20 | 30 |
| **Actual not fraud** | 10 | 940 |

Which pair is correct?

A. Precision 0.667, recall 0.400
B. Precision 0.400, recall 0.667
C. Precision 0.020, recall 0.500
D. Precision 0.667, recall 0.500

---

## Item 4 — Two gradients

In a white-box attack, the attacker computes the gradient of the loss with respect to the **input**. In training, the optimizer computes the gradient with respect to the **parameters**.

Which statement is correct?

A. They are the same vector because the loss is the same.
B. The input gradient says how to change the sample to increase loss; the parameter gradient says how to change the model to decrease loss.
C. The input gradient is only available for linear models.
D. The parameter gradient is the attack surface; the input gradient is only for training.

---

## Item 5 — Leakage by pipeline

A colleague writes:

```python
scaler = StandardScaler().fit(X)
X_scaled = scaler.transform(X)
scores = cross_val_score(model, X_scaled, y, cv=5)
```

The cross-validation score is 0.94, and the production score is 0.81.

What is the most likely explanation?

A. The model overfitted because 5 folds are too many.
B. The scaler was fitted on all rows, including each fold's validation data, so the CV score is optimistic.
C. `cross_val_score` always returns the training score.
D. The production data has a different class balance, so the two scores are not comparable.

---

## Item 6 — Leakage families

Which of the following are leakage problems? Select **all** that apply.

A. A `cancellation_reason` field recorded after the customer churned is used as a feature.
B. The same customer appears in both the training and test sets.
C. A random split is used on five years of time-ordered login events.
D. The training set is smaller than the test set.
E. `StandardScaler` is fitted on the full dataset before splitting.
F. The model uses a feature that is available at prediction time and was recorded before the label window.

---

## Item 7 — ROC-AUC versus PR-AUC

A rare-event classifier has ROC-AUC 0.90 and PR-AUC 0.18. The positive rate is 2%.

Which interpretation is most defensible?

A. The model is excellent because ROC-AUC is 0.90.
B. The model ranks reasonably well but its precision at realistic thresholds is poor relative to the 2% base rate.
C. PR-AUC is always lower than ROC-AUC, so the comparison is meaningless.
D. The model is broken because PR-AUC is below 0.5.

---

## Item 8 — Find the flaw

```python
sessions = pd.read_csv("sessions.csv")       # customer_id, minutes, churned
X = sessions[["minutes"]]
y = sessions["churned"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
```

The dataset has four sessions per customer, and `churned` is constant per customer.

Which flaw matters most for the reported score?

A. `minutes` should be standardized before the split.
B. The random split puts the same customers in train and test, so the score measures memorization.
C. `random_state=42` makes the result reproducible but not valid.
D. The test set is too small to compute any metric.

---

## Item 9 — Calibration

A model predicts a churn probability of 0.80 for 200 customers. In that group, 80 customers actually churn.

Which statement is correct?

A. The model is well calibrated because 80 is a large number.
B. The model is under-confident; the observed rate is lower than predicted.
C. The model is over-confident at this score; the observed rate is 0.40 versus a predicted 0.80.
D. Calibration cannot be assessed without ROC-AUC.

---

## Item 10 — Scenario: the 0.99 AUC

A colleague reports:

> Churn model, ROC-AUC 0.99. Top feature: `account_closed_date`. Trained on 12,000 rows with a random 80/20 split. No cross-validation. Threshold 0.5.

Write a short response that includes:

1. Two specific checks you would run before accepting the result.
2. What you would report if both checks confirm a problem.
3. One sentence you would add to the report's limitations section.

Aim for 80–120 words. Do not accuse your colleague of misconduct.

---

## Scoring

| Section | Items | Points |
|---|---|---:|
| Recall and apply | 1–4 | 4 |
| Analyze | 5–9 | 5 |
| Scenario reasoning | 10 | 3 |
| **Total** | | **12** |

A score of 10/12 (about 83%) passes. For any miss, read the explanation and the linked lesson section before moving to LAB-01B.
