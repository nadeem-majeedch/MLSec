# Lesson 09.4 — Reproducible Training and Experiment Tracking

<a id="m09-l4"></a>

**Module 09 · Lesson 4 of 5 · 1.5 hours · LO-20, LO-28**

## Scenario

Two engineers run the same notebook on the same extract. One gets ROC-AUC 0.8485, the other 0.8312. The hyperparameters are identical. The difference is that one installed a newer scikit-learn, one used a different repair order, and neither saved the split indices.

Neither result is necessarily wrong. The experiment is simply not specified tightly enough to be repeated. This lesson is about closing that gap.

## Objectives

By the end of this lesson you will be able to:

1. Define what "reproducible" means for a training run and state its scope.
2. Identify the main sources of run-to-run variation in a small ML pipeline.
3. Write a run record with code, data, configuration, environment, seeds, and outputs.
4. Version a dataset immutably and bind a run to the version it actually read.
5. Audit a tracking setup for tampering, secret leakage, and missing lineage.

## 1. Three levels of reproducibility

The words are often used interchangeably. They are not.

| Level | Question | Who can do it |
|---|---|---|
| Repeat | Can I run the same code on the same machine and get the same result? | The original author |
| Reproduce | Can another person, from the artifacts and instructions, get the same result? | A colleague |
| Replicate | Can an independent team, with new data or code, reach the same conclusion? | An external reviewer |

This lesson targets the second level. LAB-12's checker is a reproduction tool: it rebuilds the synthetic data, recomputes every count with its own rules, and checks the cleaned file's properties. It does not prove the conclusion replicates.

A claim of reproducibility should name its level and its tolerance: "same metrics within 0.02 AUC on the pinned environment," not "fully reproducible."

### Bitwise versus statistical reproducibility

Bitwise identity is achievable for some deterministic pipelines and not for others. Floating-point summation order, parallel reductions, and library versions can change the last digits. Statistical reproducibility asks whether the result is the same within a stated tolerance. For a lab metric, a tolerance is the honest target; for a hash manifest, bitwise identity is the target.

Do not mix them. A metric that differs in the fourth decimal is not a hash mismatch, and a hash mismatch is not a small numerical difference.

## 2. Where variation enters

| Source | Example | Control |
|---|---|---|
| Data content | A regenerated extract with a different seed | Version and hash the dataset |
| Row order | Shuffle before split | Save split indices; sort deterministically |
| Split | Different `random_state` | Record the seed and the indices |
| Imputation | Median computed on a different row set | Fit on the same rows; record the value |
| Model | Solver, tolerance, iteration cap | Pin the library; record hyperparameters |
| Environment | NumPy/scikit-learn version, BLAS threads | Pin versions; record the environment |
| Code | A cell edited after the run | Record the commit or file hash |
| Hardware | Floating-point behavior across CPUs | Document the platform; use tolerances |
| Human | A manual step outside the pipeline | Move it into code or record it |

The first four are the usual culprits in a data pipeline. The last one is the most dangerous, because it leaves no trace at all.

### The reproducibility test

A practical test: hand a colleague the run record and the repository, with no conversation. If they cannot rebuild the metrics within the tolerance, the record is incomplete. This is uncomfortable and it is the point.

## 3. The run record

A run record is the minimum unit of experiment tracking. LAB-12 writes a small one:

```json
{
  "lab": "LAB-12",
  "seed": 7,
  "split_seed": 13,
  "raw_rows": 632,
  "repaired_rows": 581,
  "environment": { "python": "...", "numpy": "...", "pandas": "...", "scikit-learn": "..." }
}
```

A production record needs more. The fields below are a checklist, not a schema to copy blindly.

| Field | Why it matters | Example |
|---|---|---|
| Run id | Unique reference for discussion | `run-20261028-001` |
| Code version | What executed | commit `abc123` or file hashes |
| Command | How it was invoked | `python solution.py --out artifacts` |
| Dataset id and hash | What was read | `churn-synthetic/repaired-7`, sha256 |
| Split id and indices | Which rows were in each fold | `split-13-grouped`, file hash |
| Configuration | All parameters that affect the result | seeds, imputer strategy, model `C` |
| Environment | Versions and platform | Python, libraries, OS, CPU |
| Outputs | What was produced | metrics, model, reports, hashes |
| Runtime | Cost and feasibility | seconds or minutes, hardware |
| Agent | Who or what ran it | job id, person, role |
| Status | Completed, failed, aborted | `completed` |
| Notes | Deviations from the plan | "ran with threads=1" |

The **command** and **code version** are the two fields most often missing. Without them, a record describes a result but cannot recreate it.

### Configuration is not only hyperparameters

In a data pipeline, the configuration includes:

- repair order and rule thresholds;
- imputation strategy and the rows used to compute it;
- the list of dropped columns;
- the split strategy, seed, and grouping key;
- the metric definition and the positive class.

Changing any of these changes the result. If it is not in the record, it is not reproducible.

## 4. Dataset versioning

A version is an immutable name for a content state. `repaired-7` must always mean the same bytes. A correction creates `repaired-8`.

| Practice | Why |
|---|---|
| Content-addressed ids | The id changes when the content changes |
| Immutable storage | Overwrites are impossible or audited |
| Manifest per version | Lists files, sizes, and hashes |
| Changelog per version | Explains what changed and why |
| Access control | Only the pipeline writes; people propose changes |
| Retention policy | Old versions expire on a schedule, not by accident |

LAB-12's `manifest.json` hashes `raw.csv`, `validation.json`, `repaired.csv`, `metrics.json`, `run.json`, and `report.md`. That is a version manifest for one run. It does not include the code or the environment; `run.json` covers the environment, and the repository covers the code. The combination is the record.

### Bind the run to what it read

Record the hash of the file the job opened, computed at read time. A hash typed into a config proves only that someone typed a hash. If the job reads a mutable path, the hash must be captured from the bytes actually consumed.

This is the same principle as the provenance lesson: **attestation must be generated by the activity, not written beside it.**

## 5. Experiment tracking as a security surface

A tracking server stores parameters, metrics, artifacts, and sometimes source code. That makes it a target.

| Risk | Example | Control |
|---|---|---|
| Secret leakage | A token logged as a parameter | Redact known secret patterns; never log environment dumps |
| Personal data | A sample row logged as an artifact | Classify artifacts; restrict sample logging |
| Metric tampering | An edited result in the dashboard | Append-only records; hash outputs; restrict write access |
| Artifact substitution | A different model under the same run id | Content-addressed artifacts; verify on load |
| Over-broad access | Every engineer can read every project | Project-level roles; least privilege |
| Retention drift | Runs kept forever with sensitive data | Retention policy and deletion jobs |
| Untrusted code | A logged notebook executes on view | Disable execution; render statically |

A tracking system is part of the ML supply chain. Module 10 extends this to models and dependencies; the access and integrity questions are the same.

### What to log, what not to log

Log:

- configuration, seeds, versions, metrics, artifact hashes;
- the dataset version and split id;
- the command and code reference;
- a short note on deviations.

Do not log:

- credentials, tokens, connection strings;
- full data samples unless classified and approved;
- personal data in metric names or tags;
- free-text fields that may contain either.

If a field is useful for debugging and risky to store, store a hash or a reference instead.

## 6. Auditing a run record

Before accepting a result, check:

1. **Can the dataset be rebuilt?** Version, hash, and generator or source.
2. **Can the split be rebuilt?** Strategy, seed, grouping key, saved indices.
3. **Can the code be identified?** Commit or file hash, plus the command.
4. **Can the environment be rebuilt?** Pinned versions and platform.
5. **Are the outputs hashed?** Metrics, model, report.
6. **Is the agent recorded?** A job id or a person with a role.
7. **Is the tolerance stated?** What counts as "the same result"?
8. **Was anything manual?** If yes, it is a gap.

A record that passes all eight is reproducible in the sense this lesson uses. It still may not replicate.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Recording hyperparameters only | They are the visible knobs | Record data, split, rules, and environment |
| Saving a seed but not the split indices | The seed feels sufficient | Save the indices or the split manifest |
| Hashing a mutable path | The path is convenient | Hash the bytes read at run time |
| Claiming bitwise reproducibility for a parallel job | It sounds rigorous | State a tolerance and the platform |
| Logging the environment as free text | It is quick | Capture structured versions |
| Storing secrets in parameters | Debugging is easier | Redact; use a secret store |
| Editing a metric in the dashboard | Fixing a typo | Append a correction; never overwrite |
| No run id | Runs are discussed by timestamp | Assign an id and use it everywhere |
| One successful rerun as proof | It worked once | Repeat on a fresh environment and record differences |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Metrics differ on rerun | Different library version or split | Compare `run.json`; pin versions; save indices |
| Repaired rows differ | Rule or order changed | Record rule versions and repair order |
| Hash mismatch after transfer | Encoding or line endings | Copy bytes; verify after transfer |
| Model loads but predictions differ | Preprocessing version mismatch | Version the preprocessing with the model |
| Tracking run has no artifacts | Upload failed silently | Fail the run if an expected artifact is missing |
| Run id collides | Timestamp-based ids | Use a UUID or a monotonic counter |
| Cannot delete a dataset version | Immutability enforced | That is intended; use retention policy and tombstone records |
| Reviewer cannot follow the record | Missing command or code link | Add both; test with an independent rerun |

## Check your understanding

1. Distinguish repeat, reproduce, and replicate.
2. Name four sources of variation in a data pipeline that a seed alone does not control.
3. Why should a run record include the command and the code version?
4. What does a dataset manifest prove, and what does it not prove?
5. Give two security risks of an experiment-tracking server and one control for each.

Answers are in the [quiz answer key](quiz-answers.md) and discussed in the exercises.

## Summary

- Reproducibility has levels: repeat, reproduce, replicate. State which one you claim and at what tolerance.
- Variation enters through data, row order, splits, imputation, model, environment, code, hardware, and manual steps.
- A run record includes id, code, command, dataset and split ids, configuration, environment, outputs, runtime, agent, and status.
- Dataset versions are immutable and content-addressed; manifests list hashes; the run binds to what it actually read.
- A hash proves integrity, not correctness; a metric tolerance is not a hash.
- Tracking systems are a security surface: secrets, personal data, tampering, substitution, and access all matter.
- The test of a record is whether a colleague can rebuild the result without asking you.

## Next

Continue to [Lesson 09.5 — Dataset governance and audit](lesson-5-dataset-governance-and-audit.md), where technical controls become owners, access rules, retention, and review.
