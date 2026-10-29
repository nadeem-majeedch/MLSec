# Answer Key — QZ-09

**Module 09 · 10 items · 14 points**

Use this key after attempting the quiz. For calculation items, the reasoning and units matter as much as the final number.

## 1. (1 point) B — Provenance describes origin and context; lineage connects artifacts

Provenance answers who collected the data, how, when, and under what terms. Lineage answers which artifact was produced from which inputs by which activity. They overlap, but neither replaces the other.

## 2. (2 points) Any four of the following

- The **input identity and hash** actually read by the job.
- The **parameters** that affect the output: imputation strategy, thresholds, repair order, dropped columns.
- The **agent**: a job id or a person with a role.
- The **timestamp** and run id.
- The **environment**: library versions and platform.
- The **command** used to invoke the transformation (the question already gives a code reference).

Award half a point per correct field, up to two points. A record with only a code reference and an output hash cannot tell you what data was transformed or with which parameters.

## 3. (2 points) Units and overlap

The four numbers count different things: missing cells, rows with schema violations, duplicate rows, and rows inside conflict groups. Cells are not rows. The schema rows, duplicate rows, and conflict rows can overlap: a row may be both a duplicate and part of a conflict group, or already removed by a schema filter.

Repair removes **51 rows**, from 632 to 581. The difference between 44 and 51 is not an arithmetic error; it is the effect of overlap, additional defect classes (implausible labels, duplicate customers), and the order of repair.

Award 1 point for identifying mixed units and overlap, 1 point for the correct 51 rows and the 632 → 581 change.

## 4. (1 point) C — Target / post-outcome leakage

`exit_survey` is accurate, but it exists only after the outcome, so it is unavailable at prediction time. The mechanism is target leakage, implemented here by a feature's availability time. It is not group leakage; the group issue is separate (12 customers across the naive split).

## 5. (2 points) The same-rows comparison isolates the column

The 0.9584 versus 0.7507 comparison uses identical rows and split indices and changes only the presence of `exit_survey`. The difference, 0.2077, isolates that column for this model and split.

The 0.1099 difference (0.9584 − 0.8485) compares the leaky evaluation with the repaired one. Repair changed the row set (632 → 581 through filtering, imputation, de-duplication, and quarantine), the split strategy (random to grouped), and the feature set. It summarizes total evaluation damage, not the column's effect.

Award 1 point for naming the 0.9584/0.7507 comparison, 1 point for naming at least two changes included in 0.1099.

## 6. (1 point) B — `GroupShuffleSplit` by `customer_id`

A random row split can place two rows for the same customer on opposite sides. Grouping by the entity keeps all of a customer's rows together. A larger test set does not fix the overlap, and stratification balances classes, not entities.

## 7. (2 points) Any four of the following

- **Dataset version and hash** actually read.
- **Split strategy, seed, grouping key, and saved indices.**
- **Code version and command.**
- **Configuration** beyond hyperparameters: imputation, repair order, thresholds, dropped columns.
- **Environment** versions and platform.
- **Output hashes** and a stated tolerance.
- **Agent and run id.**
- **Deviations** from the planned procedure.

Award half a point per correct field, up to two points. The seed alone does not control row order, imputation, library version, or manual steps.

## 8. (1 point) B — Integrity, not correctness

A matching hash proves the bytes are the ones recorded in the manifest. It does not prove the data is accurate, unbiased, licensed, or from a trusted source. It also says nothing about the model's reproducibility.

## 9. (1 point) B — Accountable for lawful and appropriate use

The data owner approves access, purpose, retention, and deletion. The model developer, platform custodian, and auditor are different roles. One person may hold several roles in a small team, but the decision must have a named accountable role.

## 10. (1 point) B — Who, what, when, and why

An audit trail records identity, the object and change, a trusted timestamp, and a reason or approval reference. Cost and accuracy are metrics; source, license, retention, and owner are governance fields, not the four audit questions.
