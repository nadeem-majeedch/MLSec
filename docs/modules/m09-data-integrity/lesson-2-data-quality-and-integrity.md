# Lesson 09.2 — Data Quality and Integrity Controls

<a id="m09-l2"></a>

**Module 09 · Lesson 2 of 5 · 1.5 hours · LO-20**

## Scenario

The validation report for a customer extract arrives with a summary line: "58 issues." The extract has 632 rows. A reviewer asks whether 58 rows are bad. The answer is no: the count mixes cells, rows, groups, and columns, and several defects overlap on the same row. The number is not wrong; the interpretation is.

This lesson is about building validation rules that produce counts a reviewer can act on, and about the repair decisions those counts force. It uses LAB-12's measured results throughout.

## Objectives

By the end of this lesson you will be able to:

1. Choose validation rules for schema, ranges, categories, missingness, uniqueness, cross-field consistency, and label plausibility.
2. Distinguish counts of cells, rows, groups, and columns, and avoid double-counting overlaps.
3. Decide between blocking, quarantining, imputing, and dropping a defective row, and state the trade-off.
4. Measure a rule's false positives and explain why a clean pass is not proof of cleanliness.
5. Map data-integrity threats to controls and name the residual risk.

## 1. Quality dimensions, security lens

Classical data quality names dimensions such as completeness, accuracy, consistency, timeliness, and uniqueness. Security adds intent.

| Dimension | Benign failure | Adversarial version |
|---|---|---|
| Completeness | Missing fields from a broken export | Withholding records to bias a class |
| Accuracy | Typos, unit errors | Carefully placed wrong labels |
| Consistency | Two systems disagree | Contradictory records that poison a group |
| Timeliness | Stale extract | Replaying old data to evade drift detection |
| Uniqueness | Duplicate rows | Duplicating a group to amplify its influence |
| Validity | Out-of-range values | Values just inside the range that shift a boundary |
| Provenance | Lost source record | Forged source metadata |

The control is often the same check. The threat model determines how hard you look and what you do when a check fails.

### Rules are hypotheses

A rule encodes a belief about the data: `age` is between 18 and 100; `plan` is one of four values; identical feature rows have one label. Each belief can be wrong.

- If the rule is too tight, legitimate rows are flagged (**false positives**), and the repair discards real signal.
- If the rule is too loose, bad rows pass (**false negatives**), and the evaluation inherits them.

A validation report without false-positive analysis is a count of rule firings, not a measurement of data quality.

## 2. The rule families LAB-12 uses

LAB-12's `validate` function implements eight checks. Each answers a different question.

| Check | Rule | LAB-12 count | Unit |
|---|---|---:|---|
| Missing cells | Any null in a required field | 18 | cells, per column |
| Schema range | `age` < 18 or > 100; `account_age_days` < 0; `monthly_spend` > 500 | 10 | rows |
| Unknown category | `plan` or `region` outside the allowed set | included in the 10 schema violations | rows |
| Exact duplicate | Every column identical | 8 | rows |
| Label conflict | Identical features, different `churn` | 4 groups / 8 rows | groups and rows |
| Implausible label | `churn=1`, 0 tickets, account age ≤ 120 days | 6 | rows |
| Duplicate customer | Repeated `customer_id` | 28 | extra records |
| Split overlap | Same customer in train and test of a naive split | 12 | customers |
| Leaky column | Column observed only after the outcome | 1 (`exit_survey`) | column |

Read the units before adding them. Eighteen missing cells may sit in ten rows; eight duplicate rows may include rows already dropped for a schema violation; the 28 duplicate customer records count extra occurrences, not unique customers; the 12 leaked customers are entities, not rows. Summing the column produces a number larger than the number of affected rows, which is exactly what happens in the lab.

### Why the schema total is ten, not more

The validator reports range violations, negative account ages, spend over the cap, and unknown categories separately, then sums them. A row can violate more than one rule. The total counts violations, not distinct rows. If a report needs distinct affected rows, compute a boolean mask across all rules and count it separately. Label whichever number you report.

### The implausible-label rule has a false positive

The rule `churn=1 and support_tickets=0 and account_age_days <= 120` fires on five planted rows and **one natural row**. That is realistic. A short-tenure customer with no tickets can churn for reasons the rule does not model.

The lab quarantines all six. A reviewer should inspect the natural row before deciding. The false-positive cost is not zero: a legitimate example is removed, and the class balance shifts. Report the count and the review decision.

## 3. Repair: four actions, four trade-offs

Validation finds; repair decides. LAB-12 uses four actions.

| Action | Used for | What it preserves | What it costs |
|---|---|---|---|
| Drop | Schema violations | A schema-valid dataset | Loses rows and possibly signal |
| Impute | Missing `monthly_spend`, `plan` | Row count and other fields | Manufactures values; biases distributions |
| Quarantine | Label conflicts, implausible labels | Evidence and a review queue | Removes rows from training until resolved |
| De-duplicate | Exact duplicates, repeated customers | One record per entity | Choice of which record to keep is a judgment |

The order matters. LAB-12 drops schema-invalid rows first, then imputes, then drops exact duplicates, then quarantines conflicts and implausible labels, then keeps one record per customer, then drops the leaky column. A different order can leave missing values in rows that would have been dropped, or change which duplicate survives.

**Measured result:** 632 raw rows become 581 repaired rows, a removal of 51. That is less than the sum of the row-level defect counts because defects overlap and because imputation preserves rows. If your pipeline removes 60 or 40, the order or the rules differ. The row count is a fingerprint of the repair policy.

### Imputation is a modeling decision

`monthly_spend` is imputed with the median, `plan` with the mode. Both choices assume the missingness is not informative. If customers with missing spend churn differently, the imputation hides that signal and biases the model. A missing-indicator column is an alternative; it preserves the information that the value was absent, at the cost of an extra feature.

LAB-12 does not test missingness by label. That is a limitation to report, not a defect to hide.

## 4. Gates: block, quarantine, warn

A validation rule can have three outcomes.

| Outcome | When | Example |
|---|---|---|
| Block | The dataset cannot be used at all | Schema missing a required column; label column absent |
| Quarantine | Rows are isolated for review | Label conflicts; implausible labels |
| Warn | The issue is recorded but does not stop the run | A small number of duplicate customers within tolerance |

The choice is a policy, not a technical default. Blocking on every rule makes the pipeline unusable; warning on every rule makes it decorative. A workable policy assigns:

- **Severity:** critical, high, medium, low.
- **Threshold:** zero tolerance, a rate, or a count.
- **Owner:** who resolves a quarantine or approves an override.
- **Expiry:** an override must expire and be re-reviewed.

Fail closed on the checks that protect the evaluation. If `exit_survey` is present in a training frame, stop. If the split overlaps customers, stop. These are not stylistic issues; they invalidate the result.

## 5. False positives, false negatives, and adversarial limits

Validation is a detector. It has the same properties as the adversarial-example detectors in Module 08: a true-positive rate, a false-positive rate, and an adaptive attacker.

| Limitation | Example | Consequence |
|---|---|---|
| Known rules only | A new unit error passes | Unknown defects are invisible |
| Threshold mimicry | Poison values sit just inside the range | The attack survives validation |
| Label noise below the rule | Subtle label corruption | The conflict check does not fire |
| Duplicate evasion | Near-duplicates with changed ids | Exact-match de-duplication misses them |
| Rule collision | Two legitimate categories look identical | False positives |
| Stale rules | The schema changed upstream | New valid values are flagged |

A poisoned dataset can pass every rule in LAB-12. The validator checks form, not intent. Module 05's poisoning attacks and Module 06's backdoors are designed to look valid. The data-integrity pipeline raises the cost of a crude attack and preserves evidence; it does not replace model-level defenses.

### Measuring a rule's cost

To estimate false positives, sample flagged rows and review them against the intended semantics. Record:

- how many flags were reviewed;
- how many were genuinely bad;
- how many were legitimate;
- what the reviewer changed (rule, threshold, or data).

Without this, "6 implausible labels" could be six true defects or one defect and five false alarms. The count alone does not tell you which.

## 6. Threat-to-control mapping

| Threat | Control | Evidence in LAB-12 | Residual risk |
|---|---|---|---|
| Corrupt values | Schema and range gates | 10 violations blocked | Only known rules enforced |
| Missing fields | Imputation plus missingness report | 18 cells filled | Imputation biases distributions |
| Duplicate rows | Exact de-duplication | 8 removed | Near-duplicates with new ids survive |
| Contradictory labels | Group quarantine | 8 rows removed | Ground truth unknown; both may be wrong |
| Implausible labels | Domain rule | 6 quarantined, including 1 natural row | Subtler label noise remains |
| Duplicate customers | Entity de-duplication | 28 extra records removed | Which record to keep is a judgment |
| Split leakage | Customer grouping | 12 leaked customers found | Temporal leakage not modelled |
| Post-outcome column | Column drop plus ablation | AUC falls 0.2077 on identical rows | Other proxies may leak |
| Silent modification | Manifest with SHA-256 | Hashes cover raw and repaired files | A hash proves integrity, not correctness |

The last row is the bridge to the next lesson: validation is a control, and the manifest is evidence about the control's input and output.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Adding counts with different units | The summary looks tidy | Report cells, rows, groups, and columns separately |
| Reporting rule firings as affected rows | The distinction is invisible in code | Compute a distinct-row mask when needed |
| Silent deletion | Simplicity | Quarantine with a reason and a rule version |
| Imputing without a missingness report | The column must be complete | Report missingness by column and by label |
| Trusting a pass | The green check is satisfying | State which rules ran and what they cannot catch |
| Tuning thresholds on the evaluation set | It improves the number | Tune on a reviewed validation sample |
| Keeping the leaky column "for analysis" | Analysts want it | Store it separately, outside the training frame |
| No owner for quarantine | Everyone assumes someone else reviews | Assign a role and a review date |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Repaired rows differ from 581 | Repair order or rule differs | Follow the documented order; compare issue counts |
| Missing values remain | Imputation applied before filtering or skipped | Impute after schema drops; check both columns |
| Label-conflict count is zero | Grouping dropped nulls or omitted features | Use `dropna=False` and group on all features |
| Duplicate count is lower than expected | Exact matching ignores whitespace or case | Normalize before comparing, and document it |
| Imputation shifts the target rate | Missingness is informative | Add a missing indicator; report the shift |
| A rule fires on most rows | Threshold is wrong or units changed | Review a sample; recalibrate against semantics |
| Quarantine file grows without review | No owner or SLA | Assign an owner and an expiry |
| Validation passes but the model is bad | The defect is outside the rule set | Add checks; do not relax the ones that passed |

## Check your understanding

1. Why can the sum of LAB-12's issue counts exceed the number of affected rows?
2. The implausible-label rule quarantines six rows, but only five were planted. What does that tell you about the rule?
3. Give one defect that LAB-12's validator cannot detect and explain why.
4. When would you block a dataset instead of quarantining rows?
5. Why is a missing-indicator column sometimes better than median imputation?

Answers are in the [quiz answer key](quiz-answers.md) and discussed in the exercises.

## Summary

- Quality dimensions have benign and adversarial failure modes; the check may be shared, the intent is not.
- LAB-12 reports 18 missing cells, 10 schema violations, 8 duplicate rows, 4 conflict groups (8 rows), 6 implausible labels, 28 duplicate customer records, 12 leaked customers, and 1 leaky column.
- Counts have units. Cells, rows, groups, and columns are not additive.
- Repair has four actions — drop, impute, quarantine, de-duplicate — each with a cost and a policy.
- The order of repair determines which rows survive; 632 → 581 is a fingerprint, not an accident.
- Rules have false positives. The implausible-label rule catches one natural row, and the report must say so.
- Gates need severity, threshold, owner, and expiry; protective checks should fail closed.
- Validation checks form, not intent. A poisoned dataset can pass every rule.

## Next

Continue to [Lesson 09.3 — Splits, leakage, and evaluation integrity](lesson-3-splits-leakage-and-evaluation-integrity.md), where the repaired dataset meets the evaluation and the leak gap becomes measurable.
