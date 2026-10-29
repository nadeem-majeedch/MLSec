# ML-Sec Project Catalog

| Field | Value |
|---|---|
| Document | Project titles, objectives, prerequisites, deliverables, assessment, dependencies |
| Version | 1.0 (Level 5 projects implemented) |
| Date | 2026-10-28 |
| Status | **PRJ-01…PRJ-06 and RT-01 are written and linked.** No separate starter repositories; projects reuse published labs. |
| Companion documents | [Course blueprint](course-blueprint.md) · [Lab catalog](lab-catalog.md) · [Module map](module-map.md) · [Learning outcomes](learning-outcomes.md) · [Implementation roadmap](implementation-roadmap.md) |

## 1. Design contract

Every project must satisfy the following before publication.

| Requirement | Standard |
|---|---|
| Scope | One system, one decision, two questions, one control; 11 hours of project work |
| Safety | Local, synthetic, or authorized public sandbox; no third-party production target |
| Data | Generated or public licensed data; no personal data; no downloads required |
| Threat model | Assets, boundaries, two adversary profiles with budgets, ≥ 8 scored risks |
| Baseline | Frozen evaluation set, hashed, with seeds, versions, and a zero-effect control |
| Experiments | ≥ 3 attacks with budgets and oracles; ≥ 1 defense replayed; ≥ 1 adaptive variant |
| Artifact | Report, findings, reproducible package, manifest, briefing |
| Assessment | 100-point project rubric; every dimension with descriptors |
| Time box | 11 hours with staged allocation and a 150% stop rule |
| Evaluator reference | Separate guide; not in student navigation |

**Difficulty scale.** 1 = guided · 2 = guided with choices · 3 = independent implementation with a template · 4 = open design within constraints · 5 = research-grade judgment. All projects are 3–4; capstones are 4–5.

## 2. Summary

| ID | Project | Organization | Difficulty | Hours | Primary outcomes | Status |
|---|---|---|---:|---:|---|---|
| PRJ-01 | Fraud scoring under data-quality faults and bounded evasion | Meridian Pay | 4 | 11 | LO-33, LO-08, LO-20 | Written |
| PRJ-02 | Poisoning and backdoors in a visual defect pipeline | Aster Manufacturing | 4 | 11 | LO-33, LO-10, LO-11 | Written |
| PRJ-03 | Privacy and extraction in a prediction API | Helio Health | 4 | 11 | LO-33, LO-12, LO-14, LO-19 | Written |
| PRJ-04 | Secure training and artifact pipeline | Cobalt Models | 3 | 11 | LO-33, LO-21, LO-22 | Written |
| PRJ-05 | RAG assistant with untrusted documents and tools | Harbor Community Services | 4 | 11 | LO-33, LO-25, LO-26, LO-27 | Written |
| PRJ-06 | Comparative robustness defense evaluation | Sentinel Vision | 4 | 11 | LO-33, LO-16, LO-17, LO-18 | Written |
| RT-01 | Bounded red/blue exercise | Pinewood Logistics | 4 | 9 | LO-34, LO-23, LO-28 | Written |
| CAP | Capstone, CAP-A…CAP-F | Learner-selected | 5 | 40 | LO-33, LO-35, LO-28–30 | Written |

Projects are the practical component of Module 16 (16 h = 4 h lessons + 11 h project + 1 h quiz/exercises). RT-01 is the practical component of Module 17 (14 h = 4 h lessons + 9 h RT-01 + 1 h). The capstone is Stage 6 (40 h).

## 3. Prerequisites

| Project | Required prior work | Required knowledge |
|---|---|---|
| PRJ-01 | LAB-03, LAB-05, LAB-12 | Evasion budgets, label noise, leakage, validation |
| PRJ-02 | LAB-05, LAB-06, LAB-07, LAB-08 | Poison budgets, triggers, ASR, screening |
| PRJ-03 | LAB-09, LAB-10, LAB-17 | Query budgets, extraction, low-FPR MIA, DP accounting |
| PRJ-04 | LAB-12, LAB-13 | Validation, hashing, signing, SBOM, fail-closed gates |
| PRJ-05 | LAB-19, LAB-20 | RAG boundaries, indirect injection, tool authority, approval |
| PRJ-06 | LAB-03, LAB-11 | Evasion curves, adversarial training, adaptive attacks, cost |
| RT-01 | M17, LAB-14, LAB-15 | RoE, telemetry, detection calibration, response |
| CAP | One project + M18 | Scoping, milestones, reproducibility, research framing |

## 4. Reuse map

| Project | Published labs reused | New material required |
|---|---|---|
| PRJ-01 | LAB-03, LAB-05, LAB-12 | Segment monitoring, duplicate audit, global-vs-segment comparison |
| PRJ-02 | LAB-05–08 | Screening calibration, adaptive trigger, retraining check |
| PRJ-03 | LAB-09, LAB-10, LAB-17 | Output formats, quota variant, log minimization |
| PRJ-04 | LAB-12, LAB-13 | Local package index, failure-injection matrix, signing and rollback |
| PRJ-05 | LAB-19, LAB-20 | Benign utility set, approval bypass tests, adaptive injections |
| PRJ-06 | LAB-03, LAB-11 | Three-defense matrix, cost table, pre-declared ranking |
| RT-01 | LAB-14, LAB-15 | RoE, quiet baseline, detection calibration, purple synthesis |

No new lab code is shipped with Level 5. Learners adapt the published lab code and write the project-specific harness. This keeps the projects installable offline and avoids a second, divergent codebase.

## 5. Artifact contract

| Artifact | Required | Location |
|---|---|---|
| `scope.md`, `authorization.md` | Yes | project root |
| `system.md`, `data-inventory.csv` | Yes | project root |
| `threat-model.md`, `risk-register.csv` | Yes | project root |
| `test-plan.csv` | Yes | project root |
| `baseline/` with `run.json` | Yes | results |
| `experiments/` | Yes | results |
| `defense/` | Yes | results |
| `findings/`, `report.md` | Yes | report |
| `manifest.json` | Yes | root |
| `briefing.md` | Yes | report |
| Demonstrations | Capstone only | `scripts/` |

## 6. Assessment mapping

| Dimension | Weight | Project evidence | Capstone evidence |
|---|---:|---|---|
| Scope, system, data | 10 | Scope, diagram, inventory | Plus stakeholder and harm analysis |
| Threat model | 15 | Profiles, register, traceability | Plus rejected risks and assumptions |
| Baseline and design | 15 | Frozen set, control, budgets | Plus multiple seeds and confounders |
| Attack and analysis | 20 | ≥ 3 attacks, denominators | Plus an adaptive or new attack |
| Defense and evaluation | 15 | ≥ 1 control, replay, cost | Plus an adaptive variant and residual risk |
| Reproducibility | 10 | Run records, manifest | Plus clean-checkout demonstration |
| Communication | 10 | Report, briefing | Plus 10-minute defense and demonstration |
| Ethics and limitations | 5 | Local/synthetic, limitations | Plus all four validity types and authorized use |

Completion: project ≥ Developing on all dimensions and Proficient on six; capstone ≥ Proficient on all eight.

## 7. Dependencies and sequencing

```text
M03 ─┬─> M04 ─> PRJ-01 ─┐
     ├─> M05 ─> M06 ─> PRJ-02
     ├─> M07 ─> PRJ-03
     ├─> M09 ─> M10 ─> PRJ-04
     ├─> M11 ─> RT-01
     └─> M15 ─> PRJ-05

M08 + PRJ-06 ─> CAP-B
M13 + PRJ-03 ─> CAP-C
M16 + one project ─> M17 ─> M18 ─> CAP
```

A learner may complete a project before all modules are read, provided the prerequisite labs are complete. The capstone assumes the Module 18 lessons.

## 8. Evaluator and solution policy

- The [evaluator guide](projects/evaluator-guide.md) is excluded from student navigation (`not_in_nav`).
- There is no single numeric answer key. Projects generate their own data; the guide describes evidence patterns, expected relationships, and calibration.
- Reference findings are illustrative and must not be cited as measured results.
- Self-study learners are instructed to self-score before opening the guide.

## 9. Build and maintenance notes

| Item | Note |
|---|---|
| New runnable code | None; projects adapt LAB-03…LAB-20 |
| Runtime | CPU-only; each project ≤ 11 h including writing |
| Data | Generated locally; no downloads |
| Links | Project pages link to labs, modules, capstone, and catalog |
| Navigation | Projects section in `mkdocs.yml`; evaluator guide in `not_in_nav` |
| Status text | README, docs index, module map, and lab catalog must agree on counts |

If a lab changes its output schema, update the reuse map and the affected project's evidence section. If a project adds a new dependent lab, add it to §3 and §4 and to the module prerequisites.

## 10. Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-28 | Level 5 projects PRJ-01…PRJ-06 and RT-01 written; capstone and evaluator guide added |
