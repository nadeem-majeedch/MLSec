# Module Alternate Quizzes — Blueprint and Coverage

This directory holds the authoring record for `QZ-00B`…`QZ-18B`. The student copies are under [`docs/assessments/module-quizzes/`](../../docs/assessments/module-quizzes/index.md); the keys are under [`../answer-keys/module-quizzes/`](../answer-keys/module-quizzes/).

## 1. Contract

| Field | Value |
|---|---|
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Item 1–5 | 1 point each |
| Item 6–7 | 2 points each |
| Item 8 | 3 points (scenario or multi-part) |
| Formats | MCQ, true/false, short answer, scenario |
| Tags | `[Mxx · LO-xx · Bloom n · Dn]` in each key entry |

Each Quiz B is an alternate form of the module's built-in Quiz A. It covers the same module and outcomes with different stems, numbers, and scenarios. Exact duplicate stems across Quiz A and Quiz B fail validation.

## 2. Coverage

| Module | Quiz | Key | Primary outcomes |
|---|---|---|---|
| M00 Orientation | [QZ-00B](../../docs/assessments/module-quizzes/qz-00b.md) | `qz-00b-key.md` | LO-01, LO-28, LO-29 |
| M01 Python and tooling | [QZ-01B](../../docs/assessments/module-quizzes/qz-01b.md) | `qz-01b-key.md` | LO-01, LO-02 |
| M02 ML fundamentals | [QZ-02B](../../docs/assessments/module-quizzes/qz-02b.md) | `qz-02b-key.md` | LO-02, LO-03 |
| M03 Threat modeling | [QZ-03B](../../docs/assessments/module-quizzes/qz-03b.md) | `qz-03b-key.md` | LO-04, LO-30 |
| M04 Evasion | [QZ-04B](../../docs/assessments/module-quizzes/qz-04b.md) | `qz-04b-key.md` | LO-05, LO-06, LO-07 |
| M05 Poisoning | [QZ-05B](../../docs/assessments/module-quizzes/qz-05b.md) | `qz-05b-key.md` | LO-08, LO-09 |
| M06 Backdoors | [QZ-06B](../../docs/assessments/module-quizzes/qz-06b.md) | `qz-06b-key.md` | LO-10, LO-11 |
| M07 Extraction and privacy | [QZ-07B](../../docs/assessments/module-quizzes/qz-07b.md) | `qz-07b-key.md` | LO-12, LO-13, LO-14, LO-15 |
| M08 Robustness and defense | [QZ-08B](../../docs/assessments/module-quizzes/qz-08b.md) | `qz-08b-key.md` | LO-16, LO-17, LO-18 |
| M09 Data integrity | [QZ-09B](../../docs/assessments/module-quizzes/qz-09b.md) | `qz-09b-key.md` | LO-20 |
| M10 Supply chain | [QZ-10B](../../docs/assessments/module-quizzes/qz-10b.md) | `qz-10b-key.md` | LO-21 |
| M11 Serving and incident response | [QZ-11B](../../docs/assessments/module-quizzes/qz-11b.md) | `qz-11b-key.md` | LO-22, LO-23 |
| M12 Federated learning | [QZ-12B](../../docs/assessments/module-quizzes/qz-12b.md) | `qz-12b-key.md` | LO-24 |
| M13 Privacy-preserving ML | [QZ-13B](../../docs/assessments/module-quizzes/qz-13b.md) | `qz-13b-key.md` | LO-19 |
| M14 Explainability and fairness | [QZ-14B](../../docs/assessments/module-quizzes/qz-14b.md) | `qz-14b-key.md` | LO-31, LO-32 |
| M15 Generative AI and agents | [QZ-15B](../../docs/assessments/module-quizzes/qz-15b.md) | `qz-15b-key.md` | LO-25, LO-26, LO-27 |
| M16 End-to-end assessment | [QZ-16B](../../docs/assessments/module-quizzes/qz-16b.md) | `qz-16b-key.md` | LO-33 |
| M17 Red team and blue team | [QZ-17B](../../docs/assessments/module-quizzes/qz-17b.md) | `qz-17b-key.md` | LO-34 |
| M18 Capstone and research | [QZ-18B](../../docs/assessments/module-quizzes/qz-18b.md) | `qz-18b-key.md` | LO-35 |

LO-28, LO-29, and LO-30 are embedded professional-practice outcomes. They are assessed through items inside the module quizzes and through the rubrics, not only through a dedicated question.

## 3. Marking and review

1. Attempt all eight items closed-book.
2. Score with the key; written items are marked against required elements.
3. Record the score and missed item numbers.
4. Read both the keyed explanation and the distractor explanations.
5. Revisit only the missed lesson sections, then retake after at least one day.

A score below 8 means reread the module and redo the lab. 8–9 means review the missed sections, then retake. 10–11 is a pass. 12 is strong. Score is diagnostic, not a grade.

## 4. Maintenance

- Change a question and its key together.
- Keep the point distribution and item count fixed.
- Recompute any calculation when a referenced lab metric changes.
- Do not reuse a Quiz A stem verbatim.
- Run `python scripts/validate_assessments.py` after edits.
