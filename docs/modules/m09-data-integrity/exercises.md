---
title: Module 09 Exercises
---

# Module 09 Exercises

**Four exercises · about 40 minutes · one scenario**

These exercises test interpretation and governance judgment. You may use a calculator. Keep units and denominators visible in every answer.

---

## Exercise 1 — Lineage and a deletion request (10 minutes)

A support-triage pipeline has these artifacts:

- `vendor_extract_2026_09.csv` — raw ticket export from a vendor;
- `validated_2026_09.parquet` — schema-valid rows only;
- `repaired_2026_09.parquet` — validated rows after imputation, de-duplication, and quarantine;
- `features_v3.parquet` — derived ticket features joined to customer tier;
- `triage_model_a.pkl`, `triage_model_b.pkl`, `triage_model_c.pkl` — three models trained on different months of `features_v3`;
- `metrics_2026_10.json` — evaluation for model C.

A customer requests deletion of all their records.

1. Draw or describe the lineage graph: list the entities and the activities that connect them.
2. Which artifacts are potentially affected by the deletion? Which are definitely affected, and which require investigation?
3. What evidence would you need to prove the deletion propagated to every copy?
4. The models were trained on feature tables that included the customer. Does deleting the rows make the models compliant? State the decision you would escalate and to which role.
5. Name two fields missing from this pipeline's record that would make the impact analysis faster.

---

## Exercise 2 — Counts, units, and false positives (10 minutes)

LAB-12 reports:

| Defect | Count |
|---|---:|
| Missing cells | 18 |
| Schema violations (rows) | 10 |
| Exact duplicate rows | 8 |
| Label-conflict groups | 4 (8 rows) |
| Implausible labels | 6 |
| Duplicate customer records | 28 |
| Customers leaked across naive split | 12 |
| Leaky columns | 1 |

1. Using the group count for conflicts, compute the sum of the eight counts. Explain why it is not the number of affected rows.
2. Repair removes 51 rows (632 → 581). Explain the difference between the sum and 51 using at least two mechanisms.
3. The implausible-label rule flags six rows; five were planted, one is natural. What fraction of the rule's flags are false positives? What fraction of all 632 rows does the rule flag?
4. A reviewer proposes deleting all six rows without inspection. Give one argument for and one against, and state what you would record.
5. A dashboard displays only the total "87 issues." Rewrite the summary line so a reviewer can act on it.

---

## Exercise 3 — Scenario: the triage model that knew the answer (12 minutes)

A support team trains a model to predict whether a ticket will be **escalated**. The extract has 20,000 tickets from 3,000 customers. Features include:

- ticket text;
- customer tier;
- `agent_id`;
- `resolution_code` — recorded when the ticket is closed;
- `satisfaction_score` — collected after closure;
- `created_at` and `closed_at`;
- the label `escalated`.

The team reports ROC-AUC 0.94. A reviewer removes `resolution_code` and `satisfaction_score` and reruns on the same rows and split: 0.78. After repair and a customer-grouped split, the model reaches 0.81.

1. Identify the leakage in the feature list by type. At least two features are post-outcome; name them and explain why they leak.
2. `agent_id` is recorded at assignment, before closure. Is it safe? Give two reasons it might still leak outcome information.
3. Choose a split strategy. The model will score new tickets from existing and new customers. Justify grouped or grouped-plus-temporal, and state one limitation of your choice.
4. Interpret the three numbers. Which comparison isolates the post-outcome features, and what does the 0.94 vs 0.81 difference include?
5. Write a four-sentence scoped claim for the 0.81 model. Include the data, split, metric, and one limitation.
6. Name two residual risks after removing the post-outcome columns.

---

## Exercise 4 — Governance memo for a deletion (8 minutes)

Using the pipeline from Exercise 1, complete a one-page governance record. Use the roles: data owner, data steward, platform custodian, model owner, security reviewer, auditor.

1. For each of these decisions, name the accountable role and the evidence you would file:
   - approve the deletion request;
   - remove rows from the raw and curated zones;
   - decide whether models A, B, and C must be retrained or withdrawn;
   - verify that backups and derived tables are handled;
   - confirm the audit record is complete.
2. Map three of these decisions to NIST AI RMF functions (GOVERN, MAP, MEASURE, MANAGE).
3. State one residual risk that remains after the deletion and who accepts it.
4. Write the review trigger that would reopen this decision before the next annual review.

---

## Self-assessment

| Criterion | Check |
|---|---|
| Lineage names entities and activities, not just files | [ ] |
| Counts state their units and are not added blindly | [ ] |
| False positives are quantified, not hand-waved | [ ] |
| Leakage is identified by availability time | [ ] |
| The ablation is distinguished from the repaired result | [ ] |
| Governance decisions have named roles and evidence | [ ] |
| Residual risk has an owner and a review trigger | [ ] |

Worked answers: [exercise-solutions.md](exercise-solutions.md).
