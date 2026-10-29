# LAB-12 — Dataset Validation and Leakage Audit

**Tier A · 4 hours · Difficulty 3 · Module M09 · Outcomes LO-20, LO-28, LO-30 (supporting)**

## Why this lab exists

Most "the model is broken" incidents are data incidents. A range check would
have caught the negative account age. A duplicate check would have caught the
double-counted customers. A single question — "is this column known before the
label?" — would have caught the leak that made the evaluation look excellent.

This lab builds the pipeline that asks those questions in order, records what it
found, repairs what it can, and measures the evaluation damage that remains. The
central lesson is that cleaning data changes the row set, so only a controlled
ablation can attribute a metric change to one defect.

## The system and the threat model

| Element | Assumption |
|---|---|
| Asset | A customer-churn training extract and its evaluation result |
| Threat | Data integrity failure: corruption, missingness, duplication, label noise, leakage |
| Source | Synthetic generator in `dataset.py`, deterministic at seed 7 |
| Attacker model | Not an active adversary; this is a defective-data scenario with one adversarial-flavoured defect (post-outcome leakage) |
| Detection surface | Schema, value ranges, categories, duplicates, label consistency, customer overlap, column availability timing |
| Metric | ROC-AUC of a logistic regression on a fixed split |
| Lifecycle stage | Data ingestion, dataset versioning, pre-training validation |
| Out of scope | Poisoning attacks (LAB-05/06), privacy attacks (LAB-10), real customer data |

The extract contains 632 rows: 600 base customers plus conflict twins, exact
duplicates, and duplicate-customer records. The generator plants every defect,
so detection has a ground truth.

## What you produce

A folder inside `labs/lab-12-dataset-validation/` containing:

| File | Contents |
|---|---|
| `raw.csv` | The generated extract before repair, for audit |
| `validation.json` | Every defect class, count, and sample id |
| `repaired.csv` | The cleaned dataset |
| `metrics.json` | Issue counts, row counts, leaky/clean AUC, leak gap |
| `run.json` | Lab id, seeds, row counts, environment versions |
| `report.md` | Findings, repair actions, controlled experiment, limitations |
| `manifest.json` | SHA-256 hashes of the six files above |

The reference implementation writes these files to `artifacts/`. Your completed
`starter.py` must write the same schema.

## Prerequisites

- Module 01 Lesson 3 (pandas indexing, groupby, missing data).
- Module 02 Lesson 3 (train/test splits, leakage, AUC).
- Module 09 Lessons 1–3 (provenance, validation gates, leakage).
- LAB-01B recommended (evaluation audit habits).

## Environment

- Python 3.14.7; `numpy==2.5.2`, `pandas==3.0.5`, `scikit-learn==1.9.0`, `joblib==1.5.3`.
- CPU only; the reference run takes seconds.
- No network, no cloud account, no API key.

```bash
cd labs/lab-12-dataset-validation
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab12.py --artifacts artifacts
```

## Data and safety

All records are synthetic and generated locally. Names are sequential ids such as
`C0042`; there are no people behind them. Do not substitute a real customer
extract for this lab. If you adapt the pipeline to a real dataset, do it under an
approved data-handling agreement, not in this repository.

## Task specification

1. **Read the generator.** `dataset.py` defines the schema, the allowed
   categories, and the planted defects. Do not modify it; the checker verifies
   against it.
2. **Validate.** Build a report that counts:
   - missing cells per column and in total;
   - schema violations by rule and in total;
   - exact duplicate rows;
   - label-conflict groups and rows (identical features, opposite labels);
   - implausible labels (`churn=1`, no tickets, account age ≤ 120 days);
   - duplicate customer records;
   - customers present in both sides of a naive 70/30 split (`random_state=13`);
   - columns that are only available after the outcome (`exit_survey`).
3. **Repair.** Drop schema-invalid rows, median-impute `monthly_spend`,
   mode-impute `plan`, drop exact duplicates, quarantine label conflicts and
   implausible labels, keep one record per `customer_id`, and drop `exit_survey`.
   The result must have 581 rows with a fresh index.
4. **Evaluate leakage.** On the naive rows (invalid and missing rows dropped,
   exact duplicates removed), run a random split with the survey column, then the
   same rows and split without it. On the repaired rows, run a customer-grouped
   split without the survey column.
5. **Report the controlled comparison.** The same-rows ablation isolates the
   column. The repaired number is a different dataset and must be labelled as
   such.
6. **Write the report.** Include the issue table, repair actions, the three AUC
   values, a threat-to-control table with residual risks, and at least four
   limitations.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `validate` | Count each defect and the customer split overlap |
| `starter.py` | TODO 2 | `repair` | Drop, impute, quarantine, deduplicate, and remove the post-outcome column |
| `starter.py` | TODO 3 | `evaluate` | Compare the leaky, ablation, and repaired evaluations |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-12-dataset-validation/CHECKING.md`.

## Expected outputs

Reference values (seed 7, deterministic generator):

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

The implausible count is 6, not 5: one natural row also matches the rule. That is
realistic — heuristic rules have false positives — and the report should say so.

Your numbers should match within the checker tolerances (0.02 for the AUCs, 0.03
for the clean AUC). If the row count differs, check the repair order.

## Threat-to-control mapping

| Threat | Control | Evidence | Residual risk |
|---|---|---|---|
| Corrupt values | Schema and range gates | 10 violations blocked | Only known rules enforced |
| Missing fields | Imputation plus missingness report | 18 cells filled | Imputation biases distributions |
| Duplicate rows | Exact de-duplication | 8 removed | Near-duplicates with changed ids survive |
| Contradictory labels | Group quarantine | 8 rows removed | Ground truth unknown; both may be wrong |
| Implausible labels | Domain rule | 5 planted rows plus 1 natural quarantine | Rule can miss subtler label noise |
| Post-outcome leakage | Column drop plus ablation | AUC falls 0.2077 on identical rows | Other proxies may leak |
| Split leakage | Customer grouping | 12 leaked customers found | Temporal leakage not modelled |
| Silent drift | Manifest with SHA-256 | Hash covers raw and repaired files | Hash does not prove correctness |

## Defense-in-depth perspective

Validation is one layer. A production pipeline also records lineage (which
extract, which transformation), versions the dataset, restricts who can modify
it, and monitors label distributions after deployment. This lab gives you the
validation and repair layer plus the evaluation audit that detects a leak after
the fact. It does not give you access control, lineage, or monitoring; those are
the subjects of the next two modules.

Cleaning also has costs. Dropping 51 rows changes the class balance and the
evaluation set. Imputation manufactures values. Quarantining label conflicts
throws away possibly correct data. The report must state which trade-off was
chosen and why.

## Deliverables checklist

- [ ] `artifacts/validation.json`, `raw.csv`, `repaired.csv`, `metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] A named and counted defect inventory, including the customer split overlap.
- [ ] Leaky, same-rows ablation, and repaired metrics reported separately.
- [ ] `report.md` answers every reflection question.
- [ ] `python check_lab12.py --artifacts artifacts` exits 0.

## Success criteria

- [ ] Every defect class is detected and counted, with at least one sample id.
- [ ] `repaired.csv` is schema-valid, complete, duplicate-free, unique by customer, and free of `exit_survey`.
- [ ] The leaky evaluation and the same-rows ablation use identical rows and split indices.
- [ ] The repaired evaluation uses a customer-grouped split.
- [ ] The report distinguishes the controlled ablation from the repaired re-evaluation.
- [ ] The report states that passing validation does not prove the dataset is clean.
- [ ] `python check_lab12.py --artifacts artifacts` exits 0.

## How to check yourself

The checker rebuilds the synthetic data, recomputes every count with its own
rules, inspects `repaired.csv` property by property, and recomputes the clean AUC
from the repaired file. It cannot judge whether your repair choices were wise or
whether your report overstates the result. Use the rubric for that.

## Rubric (20 points)

| Item | Points |
|---|---:|
| Validation detects every planted defect class | 6 |
| Repair produces a schema-valid, unique-customer frame | 5 |
| Leakage experiment with a same-rows ablation | 4 |
| Correct AUC values and honest interpretation | 3 |
| Report with threat mapping, trade-offs, and limitations | 2 |

## Reflection questions

1. Why is "AUC dropped after cleaning" not the same claim as "the survey column leaked"?
2. The implausible-label rule quarantines one natural row. How would you estimate the false-positive cost of the rule?
3. What does the repaired pipeline still not prove about the data?
4. If `exit_survey` were only available for 60% of rows, would dropping it still be the right repair? What else could you do?
5. Which repair step changes the class balance most, and how would you report that?
6. What would you add to the validation report so a reviewer can reproduce the repaired row set exactly?

## Hints

1. Count each defect before repairing it. A validation report that only says `cleaned` cannot be audited.
2. Repair order matters: deduplicate before splitting, and drop the post-outcome column before fitting.
3. The same-rows ablation is the controlled comparison. The repaired dataset is a different dataset, so report it separately.
4. If the repaired AUC is below the leaky one, that is expected. The question is whether the remaining number is honest.

## Time box

| Hour | Work |
|---|---|
| 1 | Read generator, schema, validate counts |
| 2 | Repair pipeline and repaired.csv checks |
| 3 | Leakage ablation and AUC comparison |
| 4 | Report, threat mapping, reflection |

Stop at 6 hours and submit with a note on what is incomplete.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `NotImplementedError` | A TODO block is untouched | Implement validate, repair, or evaluate |
| Repaired rows differ from 581 | Repair order changed which rows survive | Follow the order in the task specification |
| Missing values remain | Categorical imputation skipped | Fill `plan` with its mode |
| `exit_survey` still present | Leaky column list ignored | Drop every column in `LEAKY_COLUMNS` |
| Clean AUC does not reproduce | Group split not used or repaired.csv edited | Use `GroupShuffleSplit` with `random_state=13` |
| Label conflicts survive | Grouping omitted a feature column | Group on all of `FEATURES` with `dropna=False` |
| Checker reports generator drift | `dataset.py` modified | Restore the provided generator |

## Cleanup

```bash
# Windows PowerShell
Remove-Item -Recurse -Force artifacts
# macOS/Linux
rm -rf artifacts
```

Remove the virtual environment if you created one for this lab. Never commit `artifacts/`.

## References

- [Lab catalog](../lab-catalog.md) · [Learning outcomes](../learning-outcomes.md)
- [References](../references.md) — R-06, R-101, R-05
- [Module page](../modules/m09-data-integrity/index.md) — M09 — Data Integrity, Dataset Governance, and Secure Training Pipelines
- Package checking guide: `labs/lab-12-dataset-validation/CHECKING.md`

## What comes next

[LAB-13](lab-13.md) audits the artifacts that come out of training: pinned
dependencies, unsafe serialization, hash and signature verification, and an
SBOM. Module 10 explains the supply-chain threat model before you start.
