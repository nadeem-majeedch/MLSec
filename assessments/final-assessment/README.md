# FIN-01 Blueprint — Integrated Final Assessment

| Field | Value |
|---|---|
| Assessment | FIN-01 |
| Student copy | [`docs/assessments/final-assessment/index.md`](../../docs/assessments/final-assessment/index.md) |
| Answer key | [`../answer-keys/final-assessment-key.md`](../answer-keys/final-assessment-key.md) |
| Items | 25 |
| Points | 100 |
| Time guide | 3 hours |
| Pass | 80/100 |
| Safety | Automatic fail for a third-party target, real personal data, real credentials, or a harmful artifact |

## 1. Construction

The final has five parts, one per site level. Each part uses the same shape: two multiple-choice items at 2 points, one true/false item at 2 points, one short-answer item at 4 points, and one scenario at 10 points. Every part therefore contributes 20 points and cannot be passed by recall alone.

| Part | Level | Modules | Items | Points |
|---|---|---|---:|---:|
| A | Foundations | M00–M03 | 1–5 | 20 |
| B | Core attacks | M04–M07 | 6–10 | 20 |
| C | Defenses and secure engineering | M08–M11 | 11–15 | 20 |
| D | Advanced and emerging | M12–M15 | 16–20 | 20 |
| E | Applied assessment and research | M16–M18 | 21–25 | 20 |

## 2. Item map

| Item | Part | Module | Outcome | Bloom | Difficulty | Points | Format |
|---:|---|---|---|---:|---:|---:|---|
| 1 | A | M00/M01 | LO-28 | 3 | 2 | 2 | MCQ |
| 2 | A | M02 | LO-02 | 2 | 1 | 2 | MCQ |
| 3 | A | M02 | LO-02 | 2 | 1 | 2 | TF |
| 4 | A | M02 | LO-02, LO-03 | 4 | 3 | 4 | Short |
| 5 | A | M00/M01 | LO-28 | 5 | 3 | 10 | Scenario |
| 6 | B | M04 | LO-05 | 3 | 2 | 2 | MCQ |
| 7 | B | M05 | LO-08 | 3 | 2 | 2 | MCQ |
| 8 | B | M07 | LO-14 | 3 | 2 | 2 | TF |
| 9 | B | M07 | LO-13 | 4 | 3 | 4 | Short |
| 10 | B | M05/M06 | LO-08, LO-10 | 5 | 4 | 10 | Scenario |
| 11 | C | M08 | LO-16 | 3 | 2 | 2 | MCQ |
| 12 | C | M10 | LO-21 | 3 | 2 | 2 | MCQ |
| 13 | C | M11 | LO-22 | 3 | 2 | 2 | TF |
| 14 | C | M11 | LO-22, LO-23 | 4 | 3 | 4 | Short |
| 15 | C | M08 | LO-16, LO-17, LO-18 | 5 | 4 | 10 | Scenario |
| 16 | D | M13 | LO-19 | 2 | 1 | 2 | MCQ |
| 17 | D | M15 | LO-27 | 3 | 2 | 2 | MCQ |
| 18 | D | M14 | LO-32 | 3 | 2 | 2 | TF |
| 19 | D | M12/M13 | LO-24, LO-19 | 4 | 3 | 4 | Short |
| 20 | D | M15 | LO-26, LO-27 | 5 | 4 | 10 | Scenario |
| 21 | E | M16/M18 | LO-28, LO-33 | 3 | 2 | 2 | MCQ |
| 22 | E | M16 | LO-33 | 3 | 2 | 2 | MCQ |
| 23 | E | M18 | LO-28 | 3 | 2 | 2 | TF |
| 24 | E | M17 | LO-34 | 4 | 3 | 4 | Short |
| 25 | E | M16/M17/M18 | LO-28, LO-33, LO-34 | 5 | 4 | 10 | Scenario |

Outcomes sampled: LO-02, LO-03, LO-05, LO-08, LO-10, LO-13, LO-14, LO-16, LO-17, LO-18, LO-19, LO-21, LO-22, LO-23, LO-24, LO-26, LO-27, LO-28, LO-32, LO-33, LO-34. The final samples the five levels; it does not attempt one item per outcome. Outcomes not sampled here are covered by the module quizzes, the question bank, the level checks, or the project and capstone rubrics.

## 3. Marking rules

- Multiple-choice and true/false: full credit only for the keyed answer with no contradicting note.
- Short answer: award the stated elements in the key, not the wording. A correct claim with a missing required element loses that element's point.
- Scenario: compare against the element breakdown in the key. A scenario that names a third-party target, real personal data, or a harmful artifact is scored zero for that item and triggers the safety review.
- A correct letter with an incorrect reason is a miss on any item that asks for reasoning.
- Do not award partial credit for volume. Additional unrequested content neither earns nor loses points unless it contradicts the answer.

## 4. Interpretation

| Score | Band | Action |
|---:|---|---|
| 90–100 | Distinction | Proceed to the capstone; use misses as review targets. |
| 80–89 | Pass | Proceed; repair any part below 14/20. |
| 70–79 | Practitioner, not passing | Rework the weakest two parts and retake. |
| 60–69 | Foundations | Revisit the level checks and labs for weak parts. |
| Below 60 | Not yet | Rebuild the underlying level checks and labs. |

The final is a self-assessment. It is not proctored, not psychometrically calibrated, and not a certificate. Lab, project, RT-01, and capstone artifacts remain the primary evidence for the course outcomes.

## 5. Maintenance

- Change an item and its key in the same edit.
- Recompute any number in an item when the referenced lab artifact changes.
- Run `python scripts/validate_assessments.py` after any edit.
- Keep the item count and point total: 25 items, 100 points, 20 per part.
- Do not add a claim of external validation, accreditation, or proctoring.
