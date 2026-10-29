# Exercise Solutions — Module 09

**Worked answers and marking guidance.** Accept equivalent reasoning; the units and the distinction between comparisons matter more than wording.

## Exercise 1 — Lineage and a deletion request

**1. Lineage graph.**

Entities: `vendor_extract_2026_09.csv`, `validated_2026_09.parquet`, `repaired_2026_09.parquet`, `features_v3.parquet`, `triage_model_a/b/c.pkl`, `metrics_2026_10.json`.

Activities: ingest the vendor extract; validate; repair; build features; train each model; evaluate model C. Agents: the ingestion job, the data steward, the training job, the model owner.

A correct answer names at least the four data entities, the three models, and the activities that connect them. A list of filenames without activities is not lineage.

**2. Impact.**

- **Definitely affected:** the raw extract (if it contains the customer), validated and repaired versions derived from it, the feature table, and every model trained from that feature table.
- **Requires investigation:** backups and archive copies, notebooks or exports derived from the same extract, the evaluation file if it contains row-level predictions, and any feature table that joined customer aggregates from another source.
- **Not necessarily affected:** models trained on a different month's feature table, unless that table also contains the customer.

**3. Evidence.**

A deletion log listing every location and object, with counts, timestamps, and the operator; registry tombstones or status changes for withdrawn versions; a check of backups and replicas; a query of the lineage graph showing all downstream artifacts; and a verification sample. An attestation without location-level evidence is weak.

**4. Model compliance.**

Deleting the rows removes the direct record but does not remove information the model may have encoded. Whether retraining or withdrawal is required is a risk and legal decision. Escalate to the **data owner** with the **model owner** and legal/privacy counsel: state which models were trained on the affected data, the model's role, the sensitivity of the data, and the feasible options (retrain, withdraw, accept with documented rationale). Do not decide "the model is fine" in the engineering ticket.

**5. Missing fields.**

Accept two:

- the customer id or entity key in each artifact, enabling a direct impact query;
- a dataset version id and hash per model run, so the affected models are identifiable;
- the split id, so evaluation membership is known;
- the license and purpose record, which determines what deletion requires;
- an artifact-level lineage record emitted by the pipeline rather than reconstructed afterward.

## Exercise 2 — Counts, units, and false positives

**1. Sum and units.**

\[
18 + 10 + 8 + 4 + 6 + 28 + 12 + 1 = 87.
\]

The sum mixes cells (18), rows (10, 8, 6), groups (4), extra customer records (28), customers (12), and a column (1). It also double-counts rows that have more than one defect. It is a count of reported issues, not of affected rows.

**2. Why 51 rows are removed.**

- **Overlap:** a row can be a schema violation, a duplicate, and part of a conflict group. It is removed once but counted several times.
- **Units:** missing cells and leaked customers are not rows; the leaky column is not a row at all.
- **Repair policy:** imputation keeps rows that would otherwise be dropped; the implausible and conflict rules remove rows; keeping one record per customer removes extra records, not all records for that customer.

The 632 → 581 change is the net effect of the policy and the order, not the sum of defect counts.

**3. False positives.**

- Share of flags that are false positives: \(1/6 \approx 0.1667\), or 16.7%.
- Share of all rows flagged: \(6/632 \approx 0.00949\), or 0.95%.

Both numbers matter. The first describes the rule's precision when it fires; the second describes its reach across the dataset.

**4. Delete versus inspect.**

- **For deletion:** the rule encodes a domain belief; quarantine is cheap; a wrong row in training is a silent bias.
- **Against:** one flag is a natural row; deleting it removes a legitimate example and shifts the class balance without review.

Record the rule version, the six row ids, the review decision for the natural row, the reviewer, and the reason. The lab's policy quarantines all six; a production policy might release the reviewed natural row and document the exception.

**5. Summary line.**

> "87 reported issues across 8 classes: 18 missing cells (10 rows), 10 schema-violating rows, 8 duplicate rows, 4 label-conflict groups (8 rows), 6 implausible labels (1 likely false positive), 28 extra customer records, 12 customers overlapping the naive split, and 1 post-outcome column. Repair removes 51 rows net (632 → 581)."

The line names units, gives the net row effect, and flags the known false positive.

## Exercise 3 — The triage model that knew the answer

**1. Leakage by type.**

- `resolution_code` is assigned when the ticket closes, after escalation may already have occurred; it can encode the outcome.
- `satisfaction_score` is collected after closure, so it reflects the outcome and the customer's reaction to it.
- Both are **target / post-outcome leakage**: accurate values, unavailable at prediction time.

**2. `agent_id`.**

It is recorded before closure, but it can still leak outcome information because:

- agents differ in escalation propensity, and the model can learn agent-specific base rates;
- assignment may be correlated with ticket difficulty or customer tier, so the id acts as a proxy for the outcome;
- it may be unavailable or changed at serving time for new tickets, creating a distribution shift.

It is not automatically a leak, but it needs an ablation and a serving-availability check.

**3. Split strategy.**

Use a **grouped split by `customer_id`**, and if the model is deployed forward in time, a **temporal split** as well: train on earlier tickets, test on later ones, with groups kept intact. A grouped-plus-temporal split protects against both entity and future leakage. Limitation: a temporal split reduces the test set and may not represent new customers; a grouped random split may still leak future information within a customer's history.

**4. Interpretation.**

- 0.94 with the post-outcome features versus 0.78 on identical rows and split isolates the post-outcome feature set: a difference of 0.16.
- 0.94 versus 0.81 compares the leaky evaluation with the repaired, grouped evaluation. It includes removal of two columns, row repairs, and the split change; it is not the effect of the columns alone.
- 0.78 versus 0.81 is not attributable to one factor either; repair and split both changed.

**5. Scoped claim.**

> On 20,000 synthetic support tickets from 3,000 customers, after removing post-outcome fields and repairing the extract, a model evaluated with a customer-grouped split reaches ROC-AUC 0.81. The result is measured on one repaired dataset and one split, and it does not establish performance for new customers or future time periods.

Add the temporal limitation if the split is not temporal: the evaluation does not test forward-looking deployment.

**6. Residual risks.**

Accept two:

- ticket text may contain resolution language or agent notes written after the outcome;
- near-duplicate tickets from the same customer or incident may cross the grouped boundary if the group key is incomplete;
- unseen customers and temporal drift are outside the evaluation;
- `agent_id` may still act as a proxy for outcome or be unavailable at serving time;
- the repaired dataset may have removed rows non-randomly, changing the class balance.

## Exercise 4 — Governance memo for a deletion

**1. Decisions, roles, evidence.**

| Decision | Accountable role | Evidence |
|---|---|---|
| Approve the deletion request | Data owner | Request record, identity verification, approval, legal basis |
| Remove rows from raw and curated zones | Platform custodian, authorized by the data owner | Deletion log with object ids, counts, timestamps, operator |
| Retrain or withdraw models A, B, C | Model owner, with data owner and legal | Model inventory, dataset versions per model, risk assessment, decision record |
| Verify backups and derived tables | Platform custodian, reviewed by auditor | Backup inventory, restore test or deletion attestation, derived-table lineage |
| Confirm the audit record is complete | Auditor | Sampled events, completeness check, sign-off |

**2. RMF mapping.**

- Approve the request and assign accountability: **GOVERN**; evidence is the policy, roles, and approval record.
- Identify affected artifacts and models: **MAP**; evidence is the lineage and impact list.
- Verify deletion coverage and test controls: **MEASURE**; evidence is the deletion log, sample checks, and audit results.
- Decide retraining or withdrawal and record residual risk: **MANAGE**; evidence is the decision record and risk acceptance.

**3. Residual risk.**

Example: information encoded in a model that is not retrained, or copies in uncontrolled notebooks. The **data owner** accepts it with legal input, with a review date and a condition (for example, retrain at the next scheduled release). "None" is not an acceptable residual.

**4. Review trigger.**

Reopen before the annual review if any of these occurs: a new copy or derived artifact is discovered; a model is retrained on an affected version; the legal basis changes; an audit finds an incomplete deletion; or a related customer request reveals a systemic gap. Calendar review alone is not enough.
