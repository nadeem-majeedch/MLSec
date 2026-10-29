# Progress and Reflection Record

| Field | Value |
|---|---|
| Purpose | A single record of attempts, evidence, and next actions |
| Scope | 19 modules, 5 level gates, project/RT-01, capstone |
| Scoring | Self-reported; no identity verification or proctoring |
| Companion | [Assessment index](index.md) · [Rubrics](rubrics/index.md) · [Learning outcomes](../learning-outcomes.md) |

Keep this file or a copy of it. Fill it in as you go, not at the end. A record written from memory after the course is a reconstruction, not evidence.

The useful output of an attempt is three things: the item IDs missed, the concept each one tests, and the next action. A score alone is not a record.

## 1. How to use this record

1. After each module, record the Quiz A score, the lab's completion state, and the one concept that was least stable.
2. After each level, record the level-check score and the lab artifact that supports the level.
3. After a project or RT-01, record the rubric levels and the weakest dimension.
4. Before a retake, write what you reviewed and the date of the previous attempt.
5. Every four weeks, review the table and choose one spaced-review target.

Do not record a score you cannot support with an attempt file or a dated note. Do not mark a lab complete because it ran once; use the [completion checklists](rubrics/lab-completion-checklists.md).

## 2. Module record

| Module | Lab(s) | Quiz A | Quiz B | Lab complete | Weakest rubric dimension | Date | Next action |
|---|---|---|---:|---:|---|---|---|---|
| M00 Orientation | LAB-01 | | — | | | | |
| M01 Python and tooling | LAB-01 | | QZ-01B | | | | |
| M02 ML fundamentals | LAB-01B | | QZ-02B | | | | |
| M03 Threat modeling | LAB-02 | | QZ-03B | | | | |
| M04 Evasion | LAB-03, LAB-04 | | QZ-04B | | | | |
| M05 Poisoning | LAB-05, LAB-06 | | QZ-05B | | | | |
| M06 Backdoors | LAB-07, LAB-08 | | QZ-06B | | | | |
| M07 Extraction and privacy | LAB-09, LAB-10 | | QZ-07B | | | | |
| M08 Robustness and defense | LAB-11 | | QZ-08B | | | | |
| M09 Data integrity | LAB-12 | | QZ-09B | | | | |
| M10 Supply chain | LAB-13 | | QZ-10B | | | | |
| M11 Serving and incident response | LAB-14, LAB-15 | | QZ-11B | | | | |
| M12 Federated learning | LAB-16 | | QZ-12B | | | | |
| M13 Privacy-preserving ML | LAB-17 | | QZ-13B | | | | |
| M14 Explainability and fairness | LAB-18 | | QZ-14B | | | | |
| M15 Generative AI and agents | LAB-19, LAB-20 | | QZ-15B | | | | |
| M16 End-to-end assessment | One of PRJ-01…PRJ-06 | | QZ-16B | | | | |
| M17 Red team and blue team | RT-01 | | QZ-17B | | | | |
| M18 Capstone and research | CAP-A…CAP-F | | QZ-18B | | | | |

Quiz A is the module's built-in check. Quiz B is the alternate form in this assessment package. Use the same column for a retake by writing the date and score, for example `8/12 (2026-11-02)`.

## 3. Attempt log

| Date | Assessment | Score | Item IDs missed | Concept to revisit | Reviewed on | Retake date |
|---|---|---|---:|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |

A retake without a review date is not review. If the same item ID appears twice, the concept is still unstable; change the study method, not the number of attempts.

## 4. Level gates

A level gate is complete when the level check passes **and** the level's lab artifact exists. The check alone is knowledge evidence; the artifact is execution evidence.

| Gate | Level check | Score | Date | Supporting lab artifact | Artifact exists? | Weakest area | Next action |
|---|---|---|---:|---|---|---|---|
| G1 Foundations | LC-1 | /20 | | LAB-01, LAB-01B, LAB-02 | ☐ | | |
| G2 Core attacks | LC-2 | /20 | | LAB-03…LAB-10 | ☐ | | |
| G3 Defenses | LC-3 | /20 | | LAB-11…LAB-15 | ☐ | | |
| G4 Advanced | LC-4 | /20 | | LAB-16…LAB-20 | ☐ | | |
| G5 Applied | LC-5 | /20 | | One project or RT-01; capstone proposal | ☐ | | |

If a check passes and the artifact is missing, record the gate as **not complete** and name the artifact you will produce.

## 5. Applied work

### 5.1 Project or RT-01

| Field | Entry |
|---|---|
| Project ID | |
| Title | |
| Rubric total | /100 |
| Lowest dimension and level | |
| Clean-checkout or replay result | |
| Residual-risk statement present | ☐ |
| Ethics/authorization statement present | ☐ |
| Next action | |

### 5.2 Capstone milestones

| Milestone | Due week | Evidence | Status | Date |
|---|---:|---|---|---|
| Proposal frozen (CAP-A) | 0 | `proposal.md`, scope, one question | ☐ | |
| Data and system inventory | 2 | inventory, license/classification | ☐ | |
| Threat model and register | 4 | profiles, scores, controls | ☐ | |
| Baseline frozen | 5 | hash, run record, zero-effect control | ☐ | |
| First attack results | 7 | budgets, denominators, base set | ☐ | |
| Defense and adaptive variant | 9 | replay, cost, residual risk | ☐ | |
| Reproduction package | 10 | manifest, clean-checkout run | ☐ | |
| Report and briefing | 11 | report, briefing, limitations | ☐ | |
| Self-score all eight dimensions | 11 | completed rubric | ☐ | |

The week numbers are a pacing guide. A red baseline or a broken package is a stop-and-fix condition, not a reason to move the date.

## 6. Reflection prompts

Write three to five sentences per level. A reflection that lists topics is a table of contents, not a reflection.

### After Level 1

- Which metric or split mistake would most likely inflate a result in your own work?
- What did the threat model change about how you read the lab?
- Which claim in your report would you now scope more narrowly?

### After Level 2

- Which attack result surprised you, and what baseline explained it?
- Where did a denominator change the conclusion?
- What evidence would make you trust an attack result from someone else?

### After Level 3

- Which defense claim did you have to weaken after an adaptive test?
- What did the clean-accuracy cost change about your recommendation?
- Which control would you test first in a real promotion path, and why?

### After Level 4

- Where did a privacy or fairness metric conflict with another goal?
- Which agent or RAG control is enforced in code, and which is only a prompt?
- What would you refuse to test, and what would you ask for instead?

### After Level 5

- What is the smallest claim your project can support?
- Which limitation would a careful reviewer raise first?
- What would you do differently if you had one more week?

## 7. Ethics and authorized-use statement

Copy this statement into your project or capstone record and complete it. It is a course requirement for applied work, not a quiz item.

> I will test only systems I own or have written authorization to test. I will use synthetic or appropriately licensed data, not real personal data. I will keep credentials and private content out of artifacts. I will report negative results and limitations honestly. I will stop and ask when a target or data source is outside this statement.

| Field | Entry |
|---|---|
| Name or learner identifier | |
| Date | |
| Project or capstone ID | |
| Target scope | |
| Data source and license | |
| Disclosure contact, if any | |
| Signature or typed affirmation | |

## 8. Spaced review schedule

| Interval | What to review | Evidence |
|---|---|---|
| 1 week after a module | Missed Quiz A/B items and the matching lab interpretation question | Retake the alternate quiz |
| 4 weeks after a level | The level check's missed scenario elements | Rewrite one scenario answer |
| 12 weeks after a level | One lab artifact from the level, reproduced from its manifest | Clean run record |
| Before the capstone | The two weakest rubric dimensions across projects | Updated artifact |

A review is complete when you can explain the missed concept without the key and produce the evidence again. Rereading the key is not a review.

## 9. End-of-course reflection

| Prompt | Response |
|---|---|
| Which outcome can you now evidence with an artifact, not just a quiz? | |
| Which outcome is still supported only by quiz scores? | |
| What is the strongest claim your capstone can defend? | |
| What is the first limitation a reviewer will raise? | |
| What will you study next, and why? | |
| What did you refuse to do, and what did you do instead? | |

## 10. Record integrity

- Do not edit a past score after a retake; add a new row with the date.
- Do not mark a gate complete without the artifact checkbox.
- Do not copy another learner's reflection or evidence.
- If you find an error in an assessment or key, report it rather than working around it.
- The record is self-reported. It is evidence of your process, not a certificate.
