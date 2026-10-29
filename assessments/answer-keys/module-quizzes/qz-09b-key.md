# QZ-09B Answer Key — Module 09

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. B — a SHA-256 hash in a manifest

A content hash identifies the exact bytes. If the bytes change, the hash changes, so a run record can name the same content later. A file name can be reused, a row count is insensitive to substitutions, and a timestamp does not identify content.

- **A** is a label, not an identity.
- **C** does not detect row replacement or reordering with the same count.
- **D** records when a file was written, not what it contains.

Tag: M09 · LO-20 · Bloom 2 · D1.

## 2. B — entity or key conflict

The same entity appears twice with different labels. That is an entity/key conflict, not a schema error: both rows can satisfy the column types and ranges. It matters because the model receives contradictory supervision and because a customer-level split can still leak if the conflict is not resolved first.

- **A** is a type, range, or column violation.
- **C** is an absent value.
- **D** is a time-based leakage pattern, not a duplicate-key conflict.

Tag: M09 · LO-20 · Bloom 2 · D1.

## 3. False

Schema validation checks types, required fields, and often ranges. It does not know whether a label is correct, whether two rows describe the same entity, whether a feature is recorded after the outcome, or whether the data are representative. Those are semantic and governance defects and need separate checks.

Tag: M09 · LO-20 · Bloom 2 · D1.

## 4. False

A seed controls pseudorandom streams, but reproduction also depends on the code version, library and hardware versions, data hash, preprocessing order, thread or GPU nondeterminism, and configuration. A run record with only a seed can produce a different model on a different stack. The manifest and environment must be recorded with it.

Tag: M09 · LO-20 · Bloom 2 · D1.

## 5. Required element

A row count is unchanged when one row is replaced by another, when duplicates are merged, or when rows are reordered, so it cannot establish uniqueness or content identity. Detecting those defects needs key-level uniqueness checks and content hashes, not only a total.

Tag: M09 · LO-20 · Bloom 2 · D1.

## 6. 120 unique rows removed; 1,880 remain

The two defect sets overlap in 10 rows, so adding 90 and 40 double-counts those 10:

$$90 + 40 - 10 = 120.$$

Remaining rows: $2000 - 120 = 1880$.

The overlap matters because a repair pipeline that removes both sets sequentially may remove the same row twice in its accounting, or may remove a conflict row that was already removed as a duplicate. The union, not the sum, is the correct removal count.

Tag: M09 · LO-20 · Bloom 3 · D2.

## 7. Required elements (two flaws and the consequence)

Two of:

- **The split happens before deduplication.** Duplicate rows for the same customer can be assigned to different sides before the duplicate is removed. Deduplicating afterward cannot undo the leakage that already occurred.
- **Deduplication changes the evaluation set after the split.** Removing rows from `test_idx` changes its size and composition; the reported score is computed on a set that no longer matches the declared split.
- **Index intersection is not a group split.** Even with duplicates removed, multiple rows per customer can remain, and the split is still by row, not by entity.
- **The resulting split is not reproducible from the stated rule.** The effective test size depends on how many rows survive deduplication.

Consequence: the test score is inflated by entity leakage and is not reproducible from the declared protocol. The fix is to deduplicate or group by `customer_id` first and to use a grouped split (`GroupShuffleSplit` by customer), then record the resulting indices and counts.

Tag: M09 · LO-20 · Bloom 4 · D3.

## 8. Required elements (three controls, evidence, one residual risk)

Controls and evidence such as:

| Control | Evidence |
|---|---|
| Named data owner and purpose/retention policy | Registry entry with owner, permitted use, retention period, and access list |
| Provenance and lineage manifest | Source extract, query or code reference, timestamps, row counts, and SHA-256 of the dataset |
| Validation gates before training | Counts of missing values, schema violations, duplicate keys, label conflicts, and quarantined rows; false-positive counts for any automated rule |
| Access control and audit logging | Role assignments and an append-only log of reads, exports, and changes |
| Versioning and change control | Dataset hash and version tag; a diff or change note for each new extract |

One residual risk, for example: de-identification can still permit re-identification through linkage; schema and duplicate checks do not detect historical label bias; an authorized insider can misuse data within policy; or the extract may not represent the current patient population. The residual risk must be stated with an owner, not hand-waved as "governance handles it."

The plan must use de-identified or synthetic data and stay local. "Follow HIPAA" without naming a control, an evidence artifact, or an owner earns little credit.

Tag: M09 · LO-20 · Bloom 5 · D3.
