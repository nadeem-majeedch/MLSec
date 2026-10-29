# ML-Sec Student Self-Assessment System

| Field | Value |
|---|---|
| Document | Assessment catalog, file map, scoring, and authoring rules |
| Version | 1.0 |
| Date | 2026-10-28 |
| Status | Student assessments and answer keys published in this repository |
| Companion documents | [Course blueprint](../docs/course-blueprint.md) · [Learning outcomes](../docs/learning-outcomes.md) · [Module map](../docs/module-map.md) · [Lab catalog](../docs/lab-catalog.md) |

This package gives a self-study learner a complete assessment path: a prerequisite diagnostic, an alternate quiz for every module, a tagged question bank, a check at the end of each of the five course levels, a cumulative final assessment, lab and capstone rubrics, and a progress and reflection record.

It is a **self-assessment** system. Nothing here is externally validated, accredited, or proctored. A score is evidence about your own understanding, not a qualification. No question is described as validated by NIST, MITRE, OWASP, ISO, or any other body; framework references are used only where the course teaches them.

## 1. Where the files live

The site is built from `docs/`, so student-facing pages must live under `docs/assessments/`. Answer keys must not be built into the site, so they live in this top-level tree. This is the adaptation of the requested layout to the repository's MkDocs architecture.

| Content | Student copy (published) | Answer key (not built) |
|---|---|---|
| Diagnostic | [`docs/assessments/diagnostic/index.md`](../docs/assessments/diagnostic/index.md) | [`answer-keys/diagnostic-key.md`](answer-keys/diagnostic-key.md) |
| Module alternate quizzes | [`docs/assessments/module-quizzes/`](../docs/assessments/module-quizzes/index.md) | [`answer-keys/module-quizzes/`](answer-keys/module-quizzes/) |
| Question bank | [`docs/assessments/question-bank/`](../docs/assessments/question-bank/index.md) | [`answer-keys/question-bank-key.md`](answer-keys/question-bank-key.md) |
| Level checks | [`docs/assessments/level-checks/`](../docs/assessments/level-checks/index.md) | [`answer-keys/level-checks/`](answer-keys/level-checks/) |
| Final assessment | [`docs/assessments/final-assessment/index.md`](../docs/assessments/final-assessment/index.md) | [`answer-keys/final-assessment-key.md`](answer-keys/final-assessment-key.md) |
| Lab and capstone rubrics | [`docs/assessments/rubrics/`](../docs/assessments/rubrics/index.md) | [`rubrics/README.md`](rubrics/README.md) |
| Progress and reflection | [`docs/assessments/progress-and-reflection.md`](../docs/assessments/progress-and-reflection.md) | Self-scored; no key |

The directories in this tree hold blueprints, scoring notes, and answer keys:

```text
assessments/
├─ README.md                      # this file
├─ diagnostic/README.md           # blueprint and administration
├─ module-quizzes/README.md       # coverage matrix for QZ-00B…QZ-18B
├─ level-checks/README.md         # Level 1–5 boundaries and blueprint
├─ final-assessment/README.md     # final blueprint and marking rules
├─ rubrics/README.md              # instructor scoring notes and calibration
└─ answer-keys/
   ├─ diagnostic-key.md
   ├─ question-bank-key.md
   ├─ final-assessment-key.md
   ├─ module-quizzes/qz-00b-key.md … qz-18b-key.md
   └─ level-checks/lc-1-key.md … lc-5-key.md
```

## 2. Assessment catalog

| ID | Assessment | Covers | Items | Points | Time | Pass | Student copy |
|---|---|---|---:|---:|---:|---:|---|
| DIA-01 | Prerequisite diagnostic | Python, ML, statistics/math, security | 20 | 20 | 30 min | 14/20 | [Diagnostic](../docs/assessments/diagnostic/index.md) |
| QZ-00B…QZ-18B | Module alternate quiz (one per module) | M00–M18 | 8 each | 12 each | 20 min | 10/12 | [Module quizzes](../docs/assessments/module-quizzes/index.md) |
| QB-01 | Tagged question bank | All modules | 56 | 92 | Self-paced | — | [Question bank](../docs/assessments/question-bank/index.md) |
| LC-1 | Level 1 check — Foundations | M00–M03 | 10 | 20 | 30 min | 16/20 | [Level 1](../docs/assessments/level-checks/lc-1.md) |
| LC-2 | Level 2 check — Core attacks | M04–M07 | 10 | 20 | 30 min | 16/20 | [Level 2](../docs/assessments/level-checks/lc-2.md) |
| LC-3 | Level 3 check — Practical defenses | M08–M11 | 10 | 20 | 35 min | 16/20 | [Level 3](../docs/assessments/level-checks/lc-3.md) |
| LC-4 | Level 4 check — Advanced and emerging security | M12–M15 | 10 | 20 | 35 min | 16/20 | [Level 4](../docs/assessments/level-checks/lc-4.md) |
| LC-5 | Level 5 check — Applied projects | M16–M18 | 10 | 20 | 40 min | 16/20 | [Level 5](../docs/assessments/level-checks/lc-5.md) |
| FIN-01 | Integrated final assessment | M00–M18 | 25 | 100 | 3 h | 80/100 | [Final assessment](../docs/assessments/final-assessment/index.md) |
| RUB-LAB | Standard lab rubric | LAB-01–LAB-20 | 5 dimensions | 100 | — | all ≥ 3 | [Lab rubric](../docs/assessments/rubrics/lab-rubric.md) |
| CHK-LAB | Practical completion checklists | 21 labs | 8 checks each | Pass/fail | — | all required | [Checklists](../docs/assessments/rubrics/lab-completion-checklists.md) |
| RUB-CAP | Capstone self-scoring rubric | CAP-A–CAP-F | 8 dimensions | 100 | — | all ≥ 3 | [Capstone rubric](../docs/assessments/rubrics/capstone-rubric.md) |
| CHK-PROG | Progress and reflection record | Whole course | 19 modules + 5 gates | — | — | current | [Progress record](../docs/assessments/progress-and-reflection.md) |

### 2.1 Quiz A and Quiz B

The course already publishes one knowledge check per module, `QZ-00`…`QZ-18`, with a separate key in `docs/modules/*/quiz-answers.md`. Those are **Quiz A** and remain the canonical module checks used in the course weighting.

`QZ-00B`…`QZ-18B` in this package are **alternate forms**: same module and outcomes, different questions and numbers. Use Quiz B for a second attempt, for spaced review, or when Quiz A was seen during earlier reading. Quiz B never repeats a Quiz A item verbatim; the validator checks for exact duplicate question stems across both sets.

## 3. Level boundaries

The site groups modules into five levels. The module map also describes six production stages; the assessment levels follow the student-facing navigation, where current Stage 3 (defenses) and Stage 4 (secure engineering) are both inside Level 3.

| Level | Modules | Theme | Check | Main evidence expected alongside |
|---|---|---|---|---|
| 1 | M00–M03 | Foundations | LC-1 | LAB-01, LAB-01B, LAB-02 |
| 2 | M04–M07 | Core attacks | LC-2 | LAB-03…LAB-10 |
| 3 | M08–M11 | Practical defenses | LC-3 | LAB-11…LAB-15 |
| 4 | M12–M15 | Advanced and emerging security | LC-4 | LAB-16…LAB-20 |
| 5 | M16–M18 | Applied projects | LC-5 | One project or RT-01; capstone proposal |

A level check is a knowledge check, not a substitute for the labs. Passing LC-2 without LAB-03…LAB-10 is not evidence that you can execute an attack.

## 4. Scoring and interpretation

| Assessment | Pass | Interpretation |
|---|---:|---|
| DIA-01 | 14/20 | Below 10: take the four-week recovery path before M04. 10–13: review the named domains in parallel with M00–M01. 14–17: ready; review missed domains. 18–20: strong start. |
| QZ-xxB | 10/12 | Below 8: reread the module lessons and redo the lab. 8–9: review the missed lesson sections, then retake. 10–11: pass. 12: strong. |
| LC-n | 16/20 | Below 12: repeat the level's labs before continuing. 12–15: review the remediation map, then retake. 16–17: pass. 18–20: strong. |
| FIN-01 | 80/100 | Below 60: not yet; 60–69: foundations; 70–79: practitioner; 80–89: specialist-ready; 90–100: distinction. Any safety violation is an automatic fail regardless of score. |

All assessments are untimed unless a time is stated; the stated time is a pacing guide, not a proctoring rule. Retakes are unlimited. Record every attempt, including the score and the items missed, in the progress record. A retake without reviewing the missed items is not review.

### 4.1 What a score means

- A high score shows that you can recognize, apply, and reason about the material **on paper**.
- It does not show that you can run the experiment, produce a reproducible artifact, or defend a claim under adaptive pressure.
- Lab and project evidence remain the primary evidence for the outcomes in [learning-outcomes.md](../docs/learning-outcomes.md). Quizzes and checks are supporting evidence.
- A correct letter with incorrect reasoning is a miss on any item that asks for reasoning. The keys state where reasoning is required.

## 5. Attempt-first workflow

1. Read the assessment's instructions and time guide.
2. Answer every item in a separate file or on paper. Do not open the key.
3. Score with the key. For written items, compare against the model answer's **required elements**, not its wording.
4. Record the score, the item IDs missed, and the lesson or lab section to revisit.
5. Re-study only the missed sections, then retake the alternate form or the same check after at least one day.
6. Update [progress-and-reflection.md](../docs/assessments/progress-and-reflection.md).

### 5.1 Access honesty

The answer keys are separate files and are not part of the published site navigation. This repository is public, so the keys are not secret: anyone who knows the path can read them. The design is attempt-first, not access-controlled. Do not describe the keys as hidden or secure.

The optional static practice widget, if enabled, withholds answer text until you submit the attempt and does not call any external service. It is a convenience, not an anti-cheating control.

## 6. Item design rules

Every item in this package follows these rules.

| Rule | Implementation |
|---|---|
| One correct answer | Single-answer MCQs have exactly one defensible option. Multi-select items say "select all that apply" and list the exact count only when it does not give the answer away. |
| Plausible distractors | Each wrong option represents a real misconception, a nearby concept, or a calculation error. Absurd options are not used. |
| Explained errors | The key states why each distractor is wrong, not only why the keyed option is right. |
| Bounded scenarios | Scenario numbers are small enough to compute by hand; systems are fictional or local; no real service, person, or credential appears. |
| Taught material only | A question does not require a paper, tool, or framework version that the module does not teach. |
| Cognitive spread | Each assessment mixes recall, application, analysis, and evaluation; no assessment is all definitions. |
| Tagged | Every item states module, outcome, Bloom level, and difficulty (1–4). |
| Non-duplicative | New items were checked against QZ-00…QZ-18 and against each other. Exact duplicate stems fail validation. |
| No invented authority | The package does not claim external validation, psychometric calibration, or accreditation. |
| Safety | No item asks a learner to attack a third-party system, use personal data, or produce a harmful artifact. |

### 6.1 Difficulty scale

| Level | Meaning |
|---:|---|
| 1 | Recall or direct recognition |
| 2 | Apply a taught procedure with one step |
| 3 | Analyze a result, compare alternatives, or find a flaw |
| 4 | Evaluate a claim, design a bounded test, or integrate two modules |

## 7. Mapping to modules and outcomes

Each student page begins with a metadata table. Each item carries a tag in this form:

```text
[M04 · LO-05 · Bloom 3 · D2]
```

The mapping is also summarized in each assessment's blueprint in this tree. Coverage rules:

- Every module M00–M18 has a Quiz B.
- Every level LC-1…LC-5 covers every module in that level.
- Every outcome LO-01–LO-35 appears in at least one Quiz B, bank item, level check, or final item. LO-28, LO-29, and LO-30 are assessed through embedded professional-practice items and the rubrics, not only through a dedicated question.
- The final assessment samples all five levels; it does not attempt to cover all 35 outcomes with one item each.

## 8. Rubrics and practical evidence

The lab rubric uses the course's five dimensions: technical correctness (30), security reasoning (25), experimental method (20), reproducibility (15), communication and ethics (10). The practical completion checklists name the evidence gate for each of the 21 labs and the failure that most often fakes a pass.

The capstone rubric uses the eight dimensions in the [capstone brief](../docs/projects/capstone.md), with an added self-scoring worksheet and an evidence checklist. The capstone is complete only when every dimension is at Proficient (3) or above and the clean-checkout test reproduces the headline number.

The project and RT-01 rubric is summarized in the [student guide](../docs/student-guide.md) and the [evaluator guide](../docs/projects/evaluator-guide.md). This package does not replace the evaluator guide and does not publish its calibration notes in student navigation.

## 9. Maintenance rules

- Change a question and its key in the same edit. A changed keyed answer with an unchanged explanation is a defect.
- Recompute any number that depends on a lab artifact when the lab's `expected_metrics.json` changes.
- Do not add a question that cites a framework edition not listed in [references.md](../docs/references.md).
- Run `python scripts/validate_assessments.py` after any edit.
- Do not commit, publish, or deploy as part of an assessment edit unless the owner has authorized that action separately.
- Keep the student copy and the key in sync by item ID; the validator checks that every scored item has a key entry and vice versa.

## 10. Known limitations

- The package has not been psychometrically validated. Item difficulty labels are design estimates, not measured parameters.
- Scores are self-reported. There is no identity verification, proctoring, or time enforcement.
- The keys are public in the repository. Attempt-first behavior depends on the learner's discipline.
- The alternate quizzes sample a module; they do not exhaust it. A learner can pass a quiz and still lack lab competence.
- Scenario questions are fictional and simplified. They test judgment, not the ability to assess a real production system.
