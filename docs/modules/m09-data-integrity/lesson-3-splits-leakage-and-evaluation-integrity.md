# Lesson 09.3 — Splits, Leakage, and Evaluation Integrity

<a id="m09-l3"></a>

**Module 09 · Lesson 3 of 5 · 1.5 hours · LO-20**

## Scenario

The churn model reports ROC-AUC 0.9584. The team is pleased. Then someone notices that `exit_survey` — a field collected when a customer leaves — is in the training features. The same extract, the same rows, the same split, without that column, scores 0.7507.

The model did not become worse. The first evaluation was answering a different question: "can we predict churn using information we only have after churn?" That question is easy. It is also useless at prediction time.

This lesson is about building splits and ablations that answer the question you meant to ask.

## Objectives

By the end of this lesson you will be able to:

1. Identify target, group, temporal, duplicate, and pipeline leakage in a dataset.
2. Choose a split strategy that matches the prediction task and the entity structure.
3. Design a same-rows ablation that isolates one leaky factor.
4. Distinguish a controlled ablation from a repaired re-evaluation.
5. Audit an evaluation for integrity before trusting its metric.

## 1. Five ways information leaks

Leakage is any information in training or feature construction that would not be available, in the same form, at prediction time. The common forms:

| Type | Mechanism | LAB-12 example |
|---|---|---|
| Target leakage | A feature is caused by or recorded after the label | `exit_survey` exists only after a customer leaves |
| Group leakage | The same entity appears in train and test | 12 customers in both sides of a naive split |
| Duplicate leakage | The same or near-identical row appears on both sides | 8 exact duplicates; near-duplicates survive repair |
| Temporal leakage | Future data is used to predict the past | Not modelled in LAB-12; a random split ignores time |
| Pipeline leakage | Preprocessing is fit on rows that include test data | Not modelled in LAB-12; scalers and imputers can leak |

A feature can be legitimate and still leak. `exit_survey` is a real column with real values. The problem is its **availability time**, not its accuracy.

### Target leakage is a timing question

Ask three questions of every feature:

1. When is the value recorded?
2. Is it recorded before the prediction point for every row?
3. Would it be populated at serving time for a new customer?

If any answer is "after," "no," or "unknown," the feature is suspect. A column that is 95% null at serving time is not a feature; it is a post-hoc label in disguise.

### Duplicate leakage survives cleaning

Exact-duplicate removal catches identical rows. It does not catch:

- the same customer with a new id;
- the same event recorded twice with a timestamp difference;
- near-duplicates with one changed field;
- synthetic copies that preserve the label relationship.

Entity-aware splitting is the structural fix. De-duplication is a complement, not a substitute.

## 2. Splits are a design decision

No split is universally correct. The split must match how the model will be used.

| Split | Use when | Protects against | Does not protect against |
|---|---|---|---|
| Random row | Rows are independent and exchangeable | Nothing structural | Group, temporal, duplicate leakage |
| Stratified random | Class balance matters and rows are independent | Imbalance in small sets | The same structural leaks |
| Grouped | Multiple rows per entity | Entity leakage | Temporal leakage |
| Temporal | Prediction is forward-looking | Future information | Entity leakage across time if not combined |
| Grouped + temporal | Panel data with entities over time | Both | Pipeline leakage |
| Nested (train/val/test) | Hyperparameters are tuned | Tuning leakage into test | Any of the above if the outer split is wrong |

LAB-12 uses two splits for two purposes:

- **Audit split:** a naive random 70/30 split with `random_state=13`, used to *demonstrate* the overlap. It finds 12 customers on both sides.
- **Clean evaluation:** `GroupShuffleSplit` by `customer_id`, same seed, used after repair so that no customer crosses the boundary.

The naive split is not a mistake in the lab; it is the object of study. The mistake would be to report its metric as the model's performance.

### Splitting after repair, not before

If you split first and repair each side separately, imputation statistics differ between train and test. That is a subtle pipeline leak in reverse: the test set influences nothing, but it is processed with different rules, and the comparison is no longer clean. Repair once, version the repaired dataset, then split it.

The stronger rule is: fit every preprocessing step on training rows only. LAB-12 imputes before splitting for simplicity. That is acceptable for a demonstration and is a limitation to state; a production pipeline would fit the imputer inside the training fold.

## 3. The ablation: one factor at a time

LAB-12's central measurement is not "cleaned AUC." It is the same-rows comparison.

| Condition | Rows | Split | Features | ROC-AUC |
|---|---|---|---:|---:|
| Leaky | Naive rows (invalid and missing dropped, exact duplicates removed) | Random, seed 13 | With `exit_survey` | 0.9584 |
| Same rows, no survey | Identical rows and indices | Identical | Without `exit_survey` | 0.7507 |
| Repaired | 581 repaired rows | Grouped by customer, seed 13 | Without `exit_survey` | 0.8485 |

The first two rows differ in exactly one thing: the presence of one column. The difference, \(0.9584 - 0.7507 = 0.2077\), is attributable to that column under this model and split. That is a controlled ablation.

The third row differs in many things: row set, split strategy, imputation, de-duplication, quarantine, and the removed column. The difference from the leaky number, \(0.9584 - 0.8485 = 0.1099\), is the lab's `leak_gap`. It is a useful summary of the total evaluation damage, but it is **not** the effect of the leaky column. Cleaning changed the data and the split at the same time.

| Comparison | What it isolates | What it supports |
|---|---|---|
| 0.9584 vs 0.7507 | The survey column, same rows and split | "This column accounts for 0.2077 AUC here" |
| 0.9584 vs 0.8485 | The whole repair and split change | "The leaky evaluation overstated the repaired result by 0.1099" |
| 0.7507 vs 0.8485 | Repair effects plus split change, without the column | Not a clean estimate; do not attribute to one cause |

The middle row is the one most often misreported. "Cleaning dropped AUC by 0.11, so the leak was worth 0.11" is wrong: the leak was worth 0.2077 on identical rows; cleaning also changed which rows and which split were evaluated.

### Why the repaired number can be higher than the ablated number

0.8485 (repaired, grouped) is higher than 0.7507 (naive rows, no survey, random split). That is plausible: repair removed contradictory labels and duplicate customers, which can improve signal, and the grouped split changes the test population. It does not mean the leak "helped" by 0.10. It means three changes moved the number in different directions.

A report should present the table and resist compressing it into one sentence.

## 4. Auditing an evaluation

Use this checklist before trusting any metric, including your own.

- [ ] **Prediction time.** Is every feature available before the label for every row?
- [ ] **Entity overlap.** Can the same customer, device, patient, or session appear on both sides?
- [ ] **Duplicate check.** Were exact and near-duplicates removed before splitting?
- [ ] **Temporal order.** If time matters, is the test set strictly after the training set?
- [ ] **Preprocessing fit.** Were scalers, imputers, encoders, and feature selectors fit on training rows only?
- [ ] **Target definition.** Is the label window the same for train and test?
- [ ] **Split reproducibility.** Is the split seed or index list saved?
- [ ] **Base rate.** Does the test set have a realistic class balance?
- [ ] **Metric choice.** Is AUC appropriate, or is a precision/recall operating point needed?
- [ ] **Claim scope.** Does the report say which rows and which split produced the number?

A single failed item can invalidate the result. The checklist is ordered by how often the failure occurs in practice, not by severity.

## 5. Adversarial evaluation integrity

An attacker who can influence data collection or the evaluation set has additional options.

| Attack | Mechanism | Control |
|---|---|---|
| Test-set contamination | Insert evaluation-like rows into training | Track row provenance; de-duplicate across splits |
| Duplicate amplification | Duplicate a group to raise its weight | Entity-aware sampling and de-duplication |
| Label flooding | Add many consistent wrong labels below a conflict threshold | Label-source tracking; distribution checks |
| Temporal replay | Reuse old data to make drift look normal | Timestamp integrity; freshness checks |
| Split manipulation | Influence which customers land in test | Pre-registered splits; access control on split files |
| Metric gaming | Choose the split or metric after seeing results | Register the analysis plan before evaluation |

These are integrity attacks on the evaluation, not on the model. They are cheap when nobody owns the split. Assign ownership and make the split an immutable artifact.

## 6. Reporting the result

A defensible paragraph for LAB-12:

> On the naive row set used for the audit, the model reaches ROC-AUC 0.9584 with `exit_survey` and 0.7507 without it, using identical rows and split indices. The difference of 0.2077 isolates the post-outcome column for this model and split. After repair, the dataset has 581 rows and the grouped evaluation reaches 0.8485; that number reflects removal of duplicates, label conflicts, implausible labels, and the leaky column, and is not an estimate of the column's effect. The repaired evaluation is a different dataset and a different split, and no claim about production performance follows without a prospective test.

Notice what the paragraph does not say: it does not call 0.8485 the "true" performance, and it does not call 0.2077 the "value of the leak" in general. Both are conditional on the experiment.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Splitting rows when entities repeat | Random split is the default | Group by entity |
| Removing duplicates after splitting | The pipeline order is convenient | De-duplicate before the split |
| Comparing cleaned and leaky metrics as if one factor changed | Cleaning feels like one action | Use a same-rows ablation for attribution |
| Reporting the repaired AUC as "the real performance" | It is the cleanest number available | Scope it to the repaired dataset and split |
| Fitting a scaler on all rows | It is simpler | Fit inside the training fold |
| Ignoring time | The dataset has no obvious date column | Ask how rows were collected; add temporal splits if needed |
| Keeping post-outcome columns for EDA | Analysts want them | Store them separately from the training frame |
| No saved split indices | The seed seems enough | Save the indices or a split manifest |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Test AUC is implausibly high | A post-outcome feature or duplicate leak | Audit feature availability and duplicates |
| Grouped split errors on `groups` | Null or missing group ids | Drop or repair null ids; verify the group column |
| Ablation differs from the reference | Row set changed between runs | Reuse the same row index and split index arrays |
| Clean AUC does not reproduce | Imputer fit on a different row set | Fix the repair order and seed |
| Class balance changes after repair | Filtering removed one class disproportionately | Report the balance before and after |
| Temporal split has no test rows | Time window too narrow | Widen the window or use a grouped split and state the limit |
| Two reports disagree | Different split seeds or row counts | Compare the saved split manifests |

## Check your understanding

1. Why is `exit_survey` leakage even though its values are accurate?
2. What does the 0.2077 difference isolate, and what does the 0.1099 difference include?
3. Why does LAB-12 use a naive random split at all?
4. Name two leakage types that exact-duplicate removal does not fix.
5. A team reports 0.95 AUC after "cleaning." What five questions do you ask before believing it?

Answers are in the [quiz answer key](quiz-answers.md) and discussed in the exercises.

## Summary

- Leakage is an availability-time problem: information used in training or evaluation that would not be available at prediction time.
- The five common forms are target, group, duplicate, temporal, and pipeline leakage.
- Split strategy follows the prediction task: grouped for entities, temporal for forward-looking problems, nested for tuning.
- LAB-12's audit split is deliberately naive and finds 12 leaked customers; the clean evaluation groups by `customer_id`.
- The same-rows ablation (0.9584 with `exit_survey`, 0.7507 without) isolates one column; the repaired result (0.8485) changes rows, split, and features together.
- Cleaning changes the dataset, so before/after comparisons are confounded unless one factor is held fixed.
- Audit evaluations for availability time, entity overlap, duplicates, temporal order, preprocessing fit, and split reproducibility.
- The split is a security-relevant artifact: own it, version it, and control who can change it.

## Next

Continue to [Lesson 09.4 — Reproducible training and experiment tracking](lesson-4-reproducible-training.md), where the repaired dataset becomes a run record another person can rebuild.
