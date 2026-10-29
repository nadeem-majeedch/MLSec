# Checking Guide — LAB-12

## What the checker verifies

1. `metrics.json`, `validation.json`, `repaired.csv`, `run.json`, `report.md`, and `manifest.json` exist; the manifest covers the five required outputs.
2. `run.json` records LAB-12.
3. The checker rebuilds the synthetic data and recomputes every defect count with its own rules: missing cells, schema violations, exact duplicates, label-conflict groups, implausible labels, duplicate customer records, cross-split customers, and leaky columns.
4. Those counts match both the reference values and `validation.json`.
5. `validation.json` records 18 missing cells, 10 schema violations, 8 label-conflict rows, and `exit_survey` as the leaky column.
6. `repaired.csv` has 581 rows, exactly the expected columns, no missing values, no duplicates, unique customer ids, no schema violations, no label conflicts, no implausible labels, binary labels, and no `exit_survey`.
7. Leaky AUC reproduces within 0.02 (0.9584); same-rows survey-free AUC within 0.02 (0.7507); clean AUC within 0.03 (0.8485).
8. The reported gap equals leaky minus clean within 0.005 and is at least 0.08; leaky AUC is at least 0.93; clean AUC is at most 0.90.
9. The clean AUC recomputes from `repaired.csv` within 0.01.
10. The report contains "schema", "missing", "duplicate", "label", "leak", "auc", and "limitations".

## Reference results (seed 7)

| Metric | Value |
|---|---:|
| Raw rows | 632 |
| Repaired rows | 581 |
| Missing cells | 18 |
| Schema violations | 10 |
| Exact duplicate rows | 8 |
| Label-conflict groups / rows | 4 / 8 |
| Implausible labels | 6 |
| Duplicate customer records | 28 |
| Customers leaked across the naive split | 12 |
| Leaky AUC | 0.9584 |
| Same rows, survey removed | 0.7507 |
| Repaired AUC | 0.8485 |
| Leak gap | 0.1099 |

## Why these numbers matter

The leaky number is not a model-quality result. `exit_survey` is observed after
the customer churns, so any deployment that uses it is predicting the past. The
same-rows ablation drops AUC by 0.2077 when that one column is removed, which is
the cleanest evidence that the evaluation was contaminated.

The repaired AUC is higher than the same-rows ablation because repair also
removes contradictory labels and duplicate customers and changes the split. That
is not a defense of leakage; it is a reminder that changing the row set changes
the metric. Report both, and never compare them as if they were one experiment.

A checker pass means the pipeline detects the planted defects. It does not mean
the validation rules are complete. A new defect class outside the rules would
pass silently.

## Threat-to-control mapping

| Threat | Control tested | Evidence | Residual risk |
|---|---|---|---|
| Corrupt or out-of-range values | Schema gates | Counts and repaired frame | Rules cover known ranges only |
| Missing data | Median/mode imputation | No nulls after repair | Imputation can distort distributions |
| Duplicated records | Exact and customer-level de-duplication | Unique customer ids | Near-duplicates with changed ids survive |
| Contradictory labels | Group conflict quarantine | No conflict groups after repair | Quarantining both rows loses data |
| Post-outcome leakage | Column drop and same-rows ablation | AUC drop of 0.2077 | Other proxies may still leak |
| Split leakage | Customer-grouped split | Overlap count before, zero after | Temporal leakage not modelled |

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| `NotImplementedError` | A TODO block is untouched | Implement validate, repair, or evaluate |
| Repaired rows differ from 581 | Rows dropped in a different order | Drop invalid, impute, dedupe, quarantine conflicts, quarantine implausible, then keep one record per customer |
| Missing values remain | Imputation skipped for a categorical column | Fill `plan` with its mode and `monthly_spend` with its median |
| `exit_survey` still present | Leaky column list ignored | Drop every column in `LEAKY_COLUMNS` |
| Clean AUC is compared directly to the naive AUC | Different row sets | Report the same-rows ablation as the controlled comparison |
| Checker says generator drift | `dataset.py` changed | Restore the provided generator; the defects are part of the task contract |

## Rubric (20 points)

| Item | Points |
|---|---:|
| Validation detects every planted defect class | 6 |
| Repair produces a schema-valid, unique-customer frame | 5 |
| Leakage experiment with a same-rows ablation | 4 |
| Correct AUC values and honest interpretation | 3 |
| Report with threat mapping, trade-offs, and limitations | 2 |

## Reflection questions

1. Why is "AUC dropped after cleaning" not the same statement as "the survey column leaked"?
2. Which defect would you fix first if you could fix only one, and what evidence supports that choice?
3. What does quarantining a contradictory row cost, and what does keeping it cost?
4. Why does a customer-grouped split matter even after de-duplication?
5. The checker passes on the planted defects. Name two defect classes it would miss.
6. What would you log so that a later reviewer can reproduce the repaired row set exactly?
