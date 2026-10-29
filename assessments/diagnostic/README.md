# DIA-01 Blueprint — Prerequisite Diagnostic

| Field | Value |
|---|---|
| Student copy | [`docs/assessments/diagnostic/index.md`](../../docs/assessments/diagnostic/index.md) |
| Answer key | [`answer-keys/diagnostic-key.md`](../answer-keys/diagnostic-key.md) |
| Items | 20 |
| Points | 20, one per item |
| Time guide | 30 minutes |
| Pass for course readiness | 14/20 |
| Format | 10 single-answer MCQs, 10 short/numeric items |
| Domains | Python and tooling (5), ML fundamentals (5), statistics and math (5), security fundamentals (5) |

## Design rationale

The diagnostic samples the five baseline rows in the [course blueprint](../../docs/course-blueprint.md#51-required-baseline). It is deliberately smaller than a module quiz: it is a routing decision, not a grade. Each domain has five items so a learner can see which baseline row is weak without a long test.

The diagnostic does not test course-specific attack techniques. A learner who has never seen FGSM can still score 20/20; the course teaches FGSM in M04. What it does test is the material the attack labs assume: arrays, splits, metrics, base rates, norms, gradients, and access-control vocabulary.

## Item distribution

| Domain | Items | Formats | Bloom spread |
|---|---|---|---|
| Python and tooling | 1–5 | 2 MCQ, 3 short | 2, 2, 3, 3, 2 |
| ML fundamentals | 6–10 | 2 MCQ, 3 short | 3, 2, 3, 2, 4 |
| Statistics and math | 11–15 | 2 MCQ, 3 numeric/short | 3, 2, 4, 2, 3 |
| Security fundamentals | 16–20 | 3 MCQ, 2 short | 2, 2, 2, 3, 4 |

## Scoring and routing

| Total | Routing |
|---:|---|
| 18–20 | Start M00; review missed items only |
| 14–17 | Start M00; review each domain below 4/5 before M04 |
| 10–13 | Start the four-week recovery path alongside M00–M01 |
| 0–9 | Complete the recovery path before M02 |

A domain score of 2/5 or below is the first review target regardless of the total. The key contains the item-level rationale and the required elements for written answers.

## Maintenance

- Recompute any numeric item if the underlying definition changes. The current arithmetic is self-contained and does not depend on a lab artifact.
- Do not add an item that requires a framework version newer than the one in [references.md](../../docs/references.md).
- Keep the diagnostic free of attack techniques; it is a prerequisite check, not a preview of M04.
- Run `python scripts/validate_assessments.py` after editing.
