# Lesson 09.5 — Dataset Governance and Audit

<a id="m09-l5"></a>

**Module 09 · Lesson 5 of 5 · 1.5 hours · LO-20, LO-30**

## Scenario

A customer asks for deletion of their records. The engineering team can find the rows in the current extract. They cannot find every model trained on an earlier version, every copy in a notebook, or the derived feature table that still contains the customer's aggregate spend.

The deletion is technically possible and operationally incomplete. This lesson is about designing the controls that make the question answerable: who owns the data, who may use it, how long it is kept, and what evidence remains after a change.

## Objectives

By the end of this lesson you will be able to:

1. Assign governance roles and responsibilities for a dataset and its derived artifacts.
2. Design access, retention, deletion, and licensing controls proportionate to the data's sensitivity.
3. Specify an audit trail that answers who, what, when, and why.
4. Map data controls to NIST AI RMF functions and ISO/IEC 42001 concepts.
5. Write a governance memo with owners, evidence, residual risk, and review dates.

## 1. Governance is decisions plus evidence

A technical control enforces a rule. Governance decides which rules apply, who owns them, and what evidence proves they ran.

| Question | Governance artifact | Technical evidence |
|---|---|---|
| Who may read this dataset? | Access policy with roles | IAM logs, row-level policy tests |
| What may it be used for? | Purpose statement and license | Project registration, review approval |
| How long is it kept? | Retention schedule | Deletion job logs, tombstones |
| Who changed it? | Change policy | Append-only audit log |
| How do we know it is correct? | Validation policy | Validation report and hashes |
| Who approved the model? | Release policy | Signed approval record |

A policy without evidence is a statement of intent. Evidence without a policy is a pile of logs. Governance is the link between them.

### Roles, not job titles

Use roles so the structure survives staff changes.

| Role | Accountable for | Typical decisions |
|---|---|---|
| Data owner | The dataset's lawful and appropriate use | Approve access, purpose, retention, deletion |
| Data steward | Quality and semantics | Rule thresholds, quarantine review, schema changes |
| Platform custodian | Storage, access enforcement, backups | IAM, encryption, availability |
| Model owner | The model built from the data | Training use, evaluation claims, retraining |
| Security reviewer | Threats and controls | Access review, incident escalation |
| Auditor | Independent evidence | Sample checks, control testing |

One person may hold several roles in a small team. The important property is that each decision has a named role, not that six people exist.

## 2. Access control

Access control for datasets has three dimensions: who, what, and why.

| Dimension | Control | Example |
|---|---|---|
| Who | Identity and role | `analyst` may read de-identified columns; `trainer` may read the training view |
| What | Scope | Row filters by region; column masks for identifiers; separate raw and curated zones |
| Why | Purpose binding | Access granted to a registered project with a stated use |

Least privilege applies at each dimension. A common failure is granting a broad "data science" role read access to raw identifiers because fine-grained roles are inconvenient.

### Separate the zones

A workable pattern:

- **Raw zone:** immutable source extracts, restricted to the ingestion service and a small set of custodians.
- **Curated zone:** validated and repaired versions, readable by registered projects.
- **Feature zone:** derived tables, owned by the model team, with lineage back to the curated version.
- **Quarantine zone:** rejected rows, restricted to stewards and reviewers.
- **Archive zone:** retention-managed copies, encrypted and access-logged.

Each zone has its own access policy and its own retention. Mixing them is how a quarantine file ends up in a notebook.

### Column-level controls

Identifiers, quasi-identifiers, and sensitive attributes need different treatment. Options include:

- removing direct identifiers from the training view;
- generalizing or bucketing quasi-identifiers;
- restricting sensitive columns to a separate, audited join;
- storing the mapping table under stricter access than the de-identified data.

De-identification is not anonymization. Module 07 showed that membership and attribute inference can recover information from models; a de-identified dataset can still support re-identification when combined with auxiliary data.

## 3. Retention and deletion

Retention is a schedule, not a default of "forever." Deletion is a process, not a `rm`.

| Stage | Question | Evidence |
|---|---|---|
| Retention | How long is each zone kept, and why? | Policy with legal or operational justification |
| Expiry | What happens when the period ends? | Scheduled job, exception process |
| Deletion request | Who is authorized to request and approve? | Request record and approval |
| Propagation | Which copies, features, and models are affected? | Lineage query and impact list |
| Execution | Were all copies removed or tombstoned? | Deletion log with counts and locations |
| Verification | How do we know it worked? | Sample check or attestation |
| Model impact | Must a model be retrained or withdrawn? | Decision record |

The hardest part is propagation. A model trained on a deleted record does not contain the row in a readable form, but it may encode information about it. Whether retraining is required is a legal and risk decision, not a purely technical one. The governance artifact should state the decision and its rationale rather than assume "the model is fine."

### Tombstones and immutability

If dataset versions are immutable, deletion cannot mean editing `repaired-7`. It means:

1. recording a tombstone that marks the version as withdrawn or restricted;
2. preventing new reads;
3. deleting or restricting the underlying objects according to policy;
4. updating the registry so lineage consumers see the status.

A tombstone preserves the audit trail while removing access. Deleting the metadata as well destroys the evidence that the data ever existed, which may itself be a compliance problem.

## 4. Licensing and purpose

A license is a governance control with legal force.

| Source type | Typical constraint | Practical control |
|---|---|---|
| Public research dataset | Citation, non-commercial, or share-alike terms | License registry; usage review |
| Vendor data | Contractual scope and redistribution limits | Contract metadata; access restriction |
| Customer data | Purpose limitation, consent, retention | Purpose registry; deletion process |
| Synthetic data | Generator license; no real people | Document the generator and seed |
| Web-scraped data | Terms of service, copyright, personal data | Legal review; provenance record |

Record the license in the dataset record and check it at project registration. "We did not know" is not a control.

FAIR principles — findable, accessible, interoperable, reusable — are a useful checklist for research data. They do not replace legal review, and "accessible" does not mean "public."

## 5. The audit trail

An audit trail answers four questions for every material action:

- **Who** performed it (identity or service)?
- **What** changed (object, before/after reference)?
- **When** did it happen (trusted timestamp)?
- **Why** was it done (ticket, approval, or reason code)?

| Event | Recorded fields | Retention |
|---|---|---|
| Access to raw data | identity, role, project, timestamp, rows/columns | Per policy, often longer than the data |
| Dataset version published | version id, hash, pipeline run, approver | Life of the dataset |
| Rule or threshold change | old/new value, approver, reason | Life of the model |
| Quarantine review | reviewer, decision, rule version | Audit period |
| Deletion | request, approval, locations, verification | Per legal requirement |
| Model release | model id, dataset versions, approval | Life of the model |

The audit log must be append-only and separated from the systems it audits. If an administrator can edit both the data and the log, the log is not evidence.

### Logging without leaking

Audit logs often contain identifiers and query text. Apply the same classification as the data:

- log identifiers, not full row contents;
- hash or redact sensitive values;
- restrict log access to auditors and security;
- set a retention period that satisfies audit needs without keeping personal data indefinitely.

## 6. Framework mapping

NIST AI RMF 1.0 organizes risk work into four functions. Data governance touches all four.

| Function | Data governance question | Evidence |
|---|---|---|
| GOVERN | Who owns the data, and what policies apply? | Roles, policies, access reviews |
| MAP | What data is used, where does it come from, and what are the risks? | Dataset record, lineage, threat model |
| MEASURE | Are the controls working? | Validation counts, false positives, access test results |
| MANAGE | What happens when something goes wrong? | Incident record, deletion propagation, retraining decision |

ISO/IEC 42001 addresses an AI management system, including documented responsibilities, data resources, and continual improvement. This course discusses its concepts; the standard itself is paid, and no clause text is reproduced here.

A governance memo that maps each control to a function and supplies evidence is auditable. A memo that says "we follow best practices" is not.

## 7. A governance memo structure

Use this for LAB-12's dataset and adapt it to your own project.

```text
1. Dataset and scope (version, purpose, population)
2. Owner and roles (names or role holders, review cadence)
3. Classification and license (sensitivity, permitted use, restrictions)
4. Access policy (zones, roles, column controls, purpose binding)
5. Retention and deletion (schedule, propagation, model impact)
6. Integrity controls (validation rules, quarantine SLA, manifest)
7. Audit trail (events, storage, retention, access)
8. Framework mapping (GOVERN/MAP/MEASURE/MANAGE)
9. Residual risk (unknown defects, re-identification, vendor trust)
10. Review date and change log
```

### A worked residual-risk row

| Risk | Likelihood | Impact | Control | Residual | Owner |
|---|---|---|---|---|---|
| De-identified data re-identified by linkage | Medium | High | Column restriction, access review, aggregation | Residual risk accepted for internal research; no external release | Data owner |

The residual column is not "none." If a control removed all risk, the risk would not be on the list.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Assigning controls to "the team" | Accountability feels bureaucratic | Name a role for every decision |
| Treating de-identification as anonymization | The terms are conflated | State linkage risk and access controls |
| Retaining everything "for reproducibility" | Deletion is hard | Separate a minimal audit record from the data itself |
| Deleting metadata with the data | It seems thorough | Keep a tombstone and the approval record |
| An audit log the admin can edit | It is stored with the system | Append-only, separated, access-controlled |
| License recorded in a wiki page | It is easy | Store it in the dataset registry and check it |
| Governance memo with no evidence | It reads well | Attach counts, test results, and review records |
| Annual review with no trigger events | Calendar-driven only | Add triggers: schema change, incident, new use, deletion request |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Cannot answer "which models used this row?" | No artifact-level lineage | Add lineage from dataset version to model |
| Deletion leaves copies in notebooks | No zone control | Restrict raw access; scan shared storage |
| Access review finds stale accounts | No periodic review | Quarterly review with owner sign-off |
| Audit log has gaps | Manual actions outside the pipeline | Route changes through the pipeline; log exceptions |
| Retention job deletes too much | Schedule applied to the wrong zone | Scope by zone and verify on a sample |
| License unclear | Not recorded at ingestion | Require a license field at registration |
| Quarantine queue never reviewed | No SLA or owner | Assign a steward and a review cadence |
| Memo rejected by legal | Claims exceed evidence | Separate technical evidence from legal conclusions |

## Check your understanding

1. What is the difference between a governance policy and a technical control, and why do you need both?
2. Name three dimensions of dataset access control and give an example of each.
3. Why can deletion not simply edit an immutable dataset version?
4. What four questions must an audit trail answer?
5. Map two data controls to NIST AI RMF functions and name the evidence for each.

Answers are in the [quiz answer key](quiz-answers.md) and discussed in the exercises.

## Summary

- Governance is decisions plus evidence: roles, policies, and proof that controls ran.
- Access control has who, what, and why dimensions; zone separation and column controls reduce exposure.
- Retention is a schedule; deletion is a process with propagation, verification, and a model-impact decision.
- Immutable versions require tombstones and registry status changes, not silent edits.
- Licenses and purpose limits are governance controls with legal force; record them at ingestion.
- An audit trail is append-only, separated from the audited system, and answers who, what, when, and why.
- Map controls to GOVERN, MAP, MEASURE, and MANAGE with evidence, and state residual risk with an owner.
- Governance does not make data safe; it makes decisions explicit and checkable.

## Next

Complete [LAB-12](../../labs/lab-12.md), then the [knowledge check](quiz.md) and [exercises](exercises.md). The lab supplies the validation counts, the ablation, and the material for the governance memo this module has built toward.
