# Level Checks — Blueprint and Boundaries

This directory holds the authoring record for `LC-1`…`LC-5`. Student copies are under [`docs/assessments/level-checks/`](../../docs/assessments/level-checks/index.md); keys are under [`../answer-keys/level-checks/`](../answer-keys/level-checks/).

## 1. Boundaries

| Level | Check | Modules | Theme | Items | Points | Time | Pass | Key |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | [LC-1](../../docs/assessments/level-checks/lc-1.md) | M00–M03 | Foundations | 10 | 20 | 30 min | 16/20 | `lc-1-key.md` |
| 2 | [LC-2](../../docs/assessments/level-checks/lc-2.md) | M04–M07 | Core attacks | 10 | 20 | 30 min | 16/20 | `lc-2-key.md` |
| 3 | [LC-3](../../docs/assessments/level-checks/lc-3.md) | M08–M11 | Practical defenses and secure engineering | 10 | 20 | 35 min | 16/20 | `lc-3-key.md` |
| 4 | [LC-4](../../docs/assessments/level-checks/lc-4.md) | M12–M15 | Advanced and emerging security | 10 | 20 | 35 min | 16/20 | `lc-4-key.md` |
| 5 | [LC-5](../../docs/assessments/level-checks/lc-5.md) | M16–M18 | Applied projects | 10 | 20 | 40 min | 16/20 | `lc-5-key.md` |

The site's Level 3 combines the module map's production stages 3 and 4. The checks follow the student-facing navigation, not the six-stage production grouping.

## 2. Blueprint

Every check uses the same shape:

| Items | Format | Points each | Total |
|---|---|---:|---:|
| 1–4 | Multiple choice | 1 | 4 |
| 5–6 | True/false | 1 | 2 |
| 7–8 | Short answer | 2 | 4 |
| 9–10 | Scenario | 5 | 10 |
| | | **20** | |

Each check mixes Bloom levels. Scenario items carry half the points; recall alone cannot pass a level.

## 3. Outcome coverage

| Check | Outcomes |
|---|---|
| LC-1 | LO-01, LO-02, LO-03, LO-04, LO-29, LO-30 |
| LC-2 | LO-05, LO-06, LO-08, LO-10, LO-12, LO-13, LO-14, LO-15 |
| LC-3 | LO-16, LO-17, LO-18, LO-20, LO-21, LO-22, LO-23 |
| LC-4 | LO-19, LO-24, LO-25, LO-26, LO-27, LO-31, LO-32 |
| LC-5 | LO-28, LO-29, LO-30, LO-33, LO-34, LO-35 |

LO-28, LO-29, and LO-30 are professional-practice outcomes embedded in several checks and in the rubrics.

## 4. Marking

- MCQ/TF: full credit only for the keyed answer.
- Short answer: award each stated element; compare required elements, not wording.
- Scenario: use the element breakdown in the key. A scenario that violates the safety boundary earns zero for that item.
- Do not award points for unrequested extra content that contradicts the key.

## 5. Interpretation

| Score | Interpretation | Action |
|---:|---|---|
| 18–20 | Strong | Next level; spaced review |
| 16–17 | Pass | Review the missed item and linked lab |
| 12–15 | Not yet | Reread the named lessons and repeat the level's labs |
| Below 12 | Not yet | Rebuild the level's metrics and labs before retaking |

A level check is knowledge evidence only. Passing without the level's lab artifacts is a paper result.

## 6. Maintenance

- Keep 10 items and 20 points.
- Change an item and its key together and update the tag.
- Run `python scripts/validate_assessments.py` after edits.
- Do not describe the check as externally validated, proctored, or accredited.
