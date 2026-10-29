# LC-1 Answer Key — Level 1 Foundations

**Scoring:** items 1–6 = 1 point each; items 7–8 = 2 points each; items 9–10 = 5 points each. Total 20. Pass 16/20.

## 1. B — testing an isolated local replica built from synthetic data

The course permits work only on local replicas built from synthetic or appropriately licensed data. That isolates the learner, the data, and any damage.

- **A** is a third-party system; a public demo is still someone else's service, and crafted inputs can affect it or other users.
- **C** is unauthorized reconnaissance of a network the learner does not own.
- **D** uses data the learner has no right to hold, regardless of where it came from.

Tag: M00 · LO-29 · Bloom 1 · D1.

## 2. A — compare row counts before and after, and check key uniqueness on both sides

A merge that multiplies rows is almost always caused by duplicate keys on one or both sides. Counting before and after locates the multiplication, and a uniqueness check names the side that caused it. The check is cheap and runs before any modeling.

- **B** changes memory, not the join semantics.
- **C** can hide the symptom by deleting rows and does not diagnose the key problem.
- **D** changes order, not cardinality.

Tag: M01 · LO-01 · Bloom 2 · D1.

## 3. A — about 15% of flagged rows are true positives

Precision is the share of flagged rows that are true positives, so precision 0.15 means about 15% of flagged rows are correct positives. The flag rate (10%) and recall (0.75) are separate quantities and cannot be combined into accuracy without the base rate.

- **B** confuses the flag rate with recall.
- **C** cannot be derived: precision and recall do not determine accuracy without prevalence.
- **D** is wrong: recall 0.75 means 25% of positives are missed, not most.

Tag: M02 · LO-02 · Bloom 2 · D1.

## 4. B — an anonymous internet caller becomes an authenticated API caller

A trust boundary is a place where the identity, authority, or exposure of data changes. Adding authentication changes who the caller is and what they may do. The other options change representation, volume, or objective, not trust.

- **A** is a type conversion.
- **C** is a data-volume change.
- **D** is a loss-function choice.

Tag: M03 · LO-04 · Bloom 2 · D1.

## 5. True

A threat model that names only in-scope assets and attacks invites the reader to assume everything else is safe. Stating non-goals, excluded adversaries, and excluded interfaces makes the boundary auditable and gives a reopening condition when the system changes.

Tag: M03 · LO-04 · Bloom 1 · D1.

## 6. False

A hash match establishes byte identity with the manifest. It says nothing about whether the bytes are correct, representative, lawfully held, or unbiased. A perfectly hashed dataset can be stale, skewed, or poisoned. Integrity and validity are different properties.

Tag: M01 · LO-02 · Bloom 2 · D1.

## 7. Required elements (two checks and their corrections)

Any two of:

- **Temporal leakage.** Rows or features from the future are used to predict the past. Correct by a time-based split and by removing features recorded after the decision point.
- **Target leakage.** A feature is created after, or is a proxy for, the label (`exit_interview`, a cancellation reason, a post-decision note). Correct by auditing each feature's availability time and dropping post-outcome fields.
- **Entity or duplicate leakage.** The same customer, student, or document appears in train and test. Correct with a grouped split by entity and deduplication before splitting.
- **Preprocessing leakage.** Scaling, imputation, or feature selection is fitted on the full dataset. Correct by fitting only on the training fold, inside a pipeline.
- **Label or annotation leakage.** The test labels were consulted while tuning. Correct with a held-out set or nested selection.

One point for two valid checks; a second point only if both corrective actions are correct. A check without a correction earns at most one point.

Tag: M02 · LO-03 · Bloom 3 · D2.

## 8. Required elements (bounded adversary profile)

- **Goal.** What the adversary wants from the student-risk prediction, such as pushing one student into a lower-risk band, recovering whether a student is in the training set, or degrading the model's usefulness.
- **Knowledge.** Black-box or white-box; whether the adversary knows features, model family, training period, or only the interface. State one assumption and why it is plausible.
- **Access.** What the adversary can reach: submitting a request, editing a record through a normal form, or changing training data. Do not grant access to systems the scenario does not include.
- **Budget.** A number: requests per day, records changed, or attempts per term. The budget is what makes the profile testable and keeps the exercise authorized.

Two points for all four elements with a defensible scope. Deduct one point for a missing element and one for an unbounded capability such as "the adversary can do anything."

Tag: M03 · LO-04 · Bloom 3 · D2.

## 9. Required elements (three errors, direction, corrected protocol)

Three protocol or reasoning errors, each with a direction:

- **Random 70/30 split on 2019–2024 records.** Records from the same student and the same academic year cross the split, and future information can inform past predictions. Effect: the test score is optimistic, not a deployment estimate. Correction: split by time (train on earlier years, test on the latest year) and group by student.
- **`exit_interview` as a feature.** Exit-interview data is recorded after the outcome it predicts. Effect: target leakage inflates ROC-AUC, possibly to the reported 0.96. Correction: drop post-outcome features and document each feature's availability time.
- **"We did not find any threats."** This is not a threat-model result; no assets, adversaries, boundaries, or non-goals are stated. Effect: readiness is asserted without evidence and the risk register is empty. Correction: build a threat model with a bounded adversary and a register, then test the highest-ranked entries.
- **ROC-AUC as a readiness claim.** AUC is threshold-free and does not establish calibration, subgroup performance, or the cost of errors at the deployed operating point. Effect: a high AUC can coexist with unusable decisions. Correction: report calibration, the chosen threshold, and subgroup error rates.

A corrected protocol in four steps:

1. Define the decision, population, and outcome time; state what the model may and may not be used for.
2. Build a time-based, student-grouped split and audit every feature for availability at decision time.
3. Fit all preprocessing on training data only; report calibration, threshold behaviour, and subgroup metrics on the latest period.
4. Build the threat model and risk register, test the top risks on a local replica, and report residual risk instead of a readiness verdict.

Full credit requires three errors, a plausible direction for each, and a protocol that addresses them. A generic "use cross-validation" earns one point at most.

Tag: M02 · LO-03 · Bloom 4 · D3.

## 10. Required elements (register, control classes, RMF mapping, rejected threat)

A complete register has four rows. Each row needs:

- **Threat.** A specific event against a named asset, not a category ("student edits a record to lower predicted risk," not "data issues").
- **Impact and likelihood.** Integers 1–5 with a one-line justification; the score and band must follow from the stated scale.
- **Control.** One control labelled **preventive** or **detective**. Examples: input validation and authorization on the record form (preventive); drift and score-distribution monitoring (detective).
- **AI RMF function.** One of GOVERN, MAP, MEASURE, MANAGE, with a reason the control belongs there. A control mapped to a function it does not serve loses that row's mapping credit.

Plus:

- **One rejected threat** with a reason it is out of scope and a **reopening condition**, such as "physical theft of the server is excluded while the model is hosted in the managed environment; reopen if it is moved on-premises."
- **Synthetic data only.** A register that assumes real student records loses the safety point.

Five points: up to three for four complete rows, one for correct control classification, one for a rejected threat with a reopening condition. A register with no scores or with impact and likelihood swapped is incomplete.

Tag: M03 · LO-04 · Bloom 5 · D4.
