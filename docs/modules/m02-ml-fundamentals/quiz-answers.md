# Module 02 Knowledge Check — Answers

**QZ-02 answer key.** Read the explanation for every item, including the ones you answered correctly. The misconception notes describe the reasoning that usually produces the wrong option.

---

## Item 1 — Answer: C

The prediction is about a **customer**, even though the training rows are transactions. The label belongs to the customer and is repeated across their transactions. A group split by `customer_id` keeps all of a customer's sessions on one side; a random row split puts the same customer in both.

- **A and D** confuse the row with the unit. The model scores customers.
- **B** gets the unit right but the split wrong.

**Misconception:** "The model sees rows, so the unit is a row." The model sees rows at training time, but the decision is about an entity. Evaluation must respect that entity.

---

## Item 2 — Answer: B

With 2% positives, predicting the negative class for all rows is correct on the 98% that are negative. It finds none of the 2% that are positive, so recall is 0.

- **C** assumes the 2% positives are found by a model that never predicts positive.
- **A** reverses the definitions.

**Misconception:** "98% accuracy means the model is 98% good." Accuracy weights both classes by their frequency, so the majority class dominates.

---

## Item 3 — Answer: A

$$
\text{precision} = \frac{20}{20+10} = 0.667
\qquad
\text{recall} = \frac{20}{20+30} = 0.400
$$

- **B** swaps the denominators.
- **C** uses the total row count, which is neither metric.
- **D** computes recall as 20/40, which uses predicted positives plus false negatives; the denominator of recall is actual positives (50).

**Misconception:** "Recall is the fraction of predicted positives that are right." That is precision.

---

## Item 4 — Answer: B

Both gradients come from the same loss, but with respect to different variables.

- The parameter gradient $\nabla_\theta J$ is used to **decrease** loss during training.
- The input gradient $\nabla_x J$ is used to **increase** loss on a chosen sample during a white-box attack.

**A** is false because the vectors have different shapes and meanings. **C** is false: input gradients exist for any differentiable model, including neural networks and many tree surrogates. **D** reverses the roles.

---

## Item 5 — Answer: B

Fitting `StandardScaler` on the full `X` exposes every fold's validation rows to the training pipeline. The scaler's mean and variance include information the model should not have at fit time. The CV score is therefore optimistic, and the gap to production is consistent with that.

- **A** is not the cause; more folds do not create leakage.
- **C** is false: `cross_val_score` evaluates on held-out folds.
- **D** is possible in general but does not explain a protocol that leaks by construction.

**Misconception:** "Scaling is unsupervised, so it cannot leak the label." Leakage is not only about labels. Any statistic computed on validation rows violates the evaluation boundary.

---

## Item 6 — Answers: A, B, C, E

- **A** is target leakage: the feature is recorded after the outcome.
- **B** is group leakage: the same entity is on both sides.
- **C** is temporal leakage: a random split trains on the future.
- **E** is pipeline leakage: preprocessing saw the validation data.
- **D** is a design choice, not leakage. An unusual split ratio does not by itself invalidate the result.
- **F** describes a legitimate feature: recorded before the label window and available at prediction time.

**Misconception:** "All data problems are leakage." Leakage specifically means information crossing a boundary it should not cross.

---

## Item 7 — Answer: B

ROC-AUC measures ranking across all thresholds and is computed mostly from true negatives when positives are rare, so it can look high while precision at a usable threshold is low. PR-AUC is anchored by the 2% base rate: 0.18 is much better than random (0.02) but far from perfect (1.0).

- **A** ignores the operating point.
- **C** is false; they measure different things and can be compared with their baselines.
- **D** confuses a low absolute value with a broken model; the baseline is 0.02.

**Misconception:** "A PR-AUC below 0.5 is always bad." Judge PR-AUC against the base rate, not against 0.5.

---

## Item 8 — Answer: B

The rows are sessions, the label is per customer, and the random split puts the same customers on both sides. With four near-duplicate sessions per customer, the model can memorize a customer's label in training and retrieve it in test.

- **A** is a good practice but does not address the dominant flaw.
- **C** is wrong: the seed makes the run reproducible; it does not make the protocol valid.
- **D** is not the main issue; 25% of 2400 rows is 600 sessions.

**Misconception:** "A fixed seed fixes the evaluation." Reproducibility and validity are independent properties.

---

## Item 9 — Answer: C

The observed rate is $80/200 = 0.40$, while the model predicts 0.80. The model is over-confident at this score: it predicts more churn than occurs.

- **A** confuses sample size with calibration.
- **B** reverses the direction; under-confidence would mean the observed rate is higher than predicted.
- **D** is false: calibration is assessed with observed frequencies, not AUC.

**Misconception:** "Calibration is the same as accuracy." A model can be accurate and badly calibrated, or well calibrated and weakly discriminating.

---

## Item 10 — Model answer

> Thanks — before we use the 0.99, I would like to check two things. First, `account_closed_date` looks like it is recorded after churn; I would verify its write time and availability at scoring, then rerun without it. Second, the random split may put the same customers in train and test; I would count customer overlap and rerun with a group split and time-ordered holdout. If both checks confirm a problem, I would report the repaired AUC with a confidence interval, a majority-class baseline, and the feature that was removed. I would add: "The original 0.99 depended on a post-outcome field and a row-level split, so it does not estimate production performance."

### Scoring guide

| Criterion | Points |
|---|---:|
| Two specific checks (provenance of the date field; group/time split or overlap count) | 2 |
| Reports the repaired result with baseline and uncertainty, not just "it is wrong" | 1 |
| Limitation sentence is precise and non-accusatory | 1 |

A response that only says "remove the leaky feature" gets 1 of 4: it names one check but does not address the split or the reporting.

**Misconception:** "The right response is to reject the result." The right response is to replace an invalid measurement with a valid one, and to state what changed.

---

## Score interpretation

| Score | Interpretation |
|---:|---|
| 11–12 | Ready for LAB-01B |
| 9–10 | Review the missed items and the linked lesson sections, then start the lab |
| 6–8 | Re-read Lessons 02.3 and 02.4 before the lab; the exercises will expose the gaps |
| 0–5 | Work through the module again, including the worked examples, before attempting the lab |

Record the items you missed in your study log. If two or more misses are in the same lesson, that lesson is the one to review, not the whole module.
