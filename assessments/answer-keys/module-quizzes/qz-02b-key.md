# QZ-02B Answer Key — Module 02

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. C — chronological split

When the label depends on future behavior, a random split lets the model train on future events and test on past ones. A chronological split (train on earlier events, test on later events) mimics deployment and prevents temporal leakage. Grouping by user is useful only if the unit of prediction is the user; it does not solve time order.

- **A** mixes time and is the classic temporal-leakage error.
- **B** addresses entity leakage, not temporal order.
- **D** is a biased split with no methodological justification.

Tag: M02 · LO-01 · Bloom 2 · D1.

## 2. B — optimistic because the test set influenced the choice

Choosing among 50 thresholds on the test set uses the test labels to select the model. The winning F1 is the maximum of 50 noisy estimates, so it is biased upward. Select the threshold on validation data or with cross-validation, then report once on the untouched test set.

- **A** is false; F1 is defined for binary classification.
- **C** is false; 0.5 is a default, not a requirement.
- **D** is unrelated.

Tag: M02 · LO-01 · Bloom 3 · D2.

## 3. True

A majority-class predictor on a 5% positive dataset has 95% accuracy and 0% recall on the positive class. Accuracy measures overall correctness; recall measures coverage of actual positives. High accuracy and zero minority recall are compatible.

Tag: M02 · LO-01 · Bloom 2 · D1.

## 4. True, with a caveat

ROC-AUC is computed over all thresholds and can look strong when there are many true negatives. PR-AUC concentrates on the positive class and is usually more sensitive to performance at the precision levels a rare-event deployment can tolerate. It is not a universal law: the operating cost and the chosen threshold still decide what matters.

Tag: M02 · LO-01 · Bloom 2 · D1.

## 5. Required elements (two)

- **Sampling variance:** one split gives one estimate; a different split can move the metric, especially with a small test set.
- **Class imbalance:** a single split can put too few positives in test, making recall and PR-AUC unstable.
- **Distribution shift:** one split may not represent the deployment population; a random split can hide temporal or group shift.
- **No uncertainty:** a point estimate without an interval overstates precision.
- Also acceptable: the split may leak groups or duplicates.

Tag: M02 · LO-01 · Bloom 3 · D2.

## 6. Precision 0.60; recall 0.75; F1 ≈ 0.667

- Precision $= TP / (TP + FP) = 30 / (30 + 20) = 0.60$.
- Recall $= TP / (TP + FN) = 30 / (30 + 10) = 0.75$.
- F1 $= 2 \cdot (0.60 \cdot 0.75) / (0.60 + 0.75) = 0.90 / 1.35 \approx 0.667$.

Each formula must be shown for full credit; a correct F1 with no denominators earns half credit at most.

Tag: M02 · LO-01 · Bloom 3 · D2.

## 7. Flaw: the model is scored on the data it trained on

`model.score(X, y)` after `fit(X, y)` measures training-set fit, not generalization. A flexible model can memorize the training rows and report a high number that says nothing about unseen data. The minimum correction is a held-out test set (or cross-validation) that the model never saw during fitting or tuning.

Tag: M02 · LO-01 · Bloom 3 · D2.

## 8. Required elements (three questions with why)

- **What are precision and recall at the operating threshold, given the 2% base rate?** Accuracy and AUC do not state the cost of false positives and false negatives at the threshold the vendor will deploy.
- **Is the model calibrated?** A score of 0.8 should correspond to roughly an 80% observed rate; otherwise the threshold and the risk communication are misleading.
- **How was the split constructed, and were duplicates, groups, or time order handled?** A random split on repeated entities or time-ordered events can inflate all the reported numbers.
- **What is the confidence interval, and on how many positives?** With a 2% base rate, the positive count may be small and the estimate unstable.
- **What is the baseline, and what threshold was used?** A model must beat a trivial or existing rule, and the threshold must be chosen for the deployment cost.

Three questions with a clear "why" earn the 3 points. Generic questions such as "Is the data good?" do not.

Tag: M02 · LO-28 · Bloom 4 · D3.
