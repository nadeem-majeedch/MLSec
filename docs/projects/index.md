---
title: Applied Projects — Catalog
---

# Applied Projects — Catalog

**Level 5 · Six assessment projects and one red/blue exercise · Local and synthetic only**

This catalog lists the practical work for Modules 16–18. Each project is an 11-hour assessment of one ML system; each produces a report, a reproducible artifact, and a briefing. The red/blue exercise is 9 hours and produces a different artifact: a measured contest between attack and defense.

Complete **one project** for Module 16 and **RT-01** for Module 17. The capstone extends one project along a single axis; it is not a seventh project.

The [assessment and red-team specialization](../learning-paths.md#assessment-and-red-team-specialization) shows how M16–M18, one project, RT-01, and the capstone fit into a 113-hour route.

## Choose by what you want to prove

| ID | Organization and system | Core question | Prerequisites | Outcome |
|---|---|---|---|---|
| [PRJ-01](prj-01-fraud-detection.md) | Meridian Pay — card-not-present fraud scoring | Can data-quality faults and bounded feature changes move fraud decisions without the dashboard noticing? | LAB-03, LAB-05, LAB-12 | LO-33, LO-08, LO-20 |
| [PRJ-02](prj-02-image-poisoning.md) | Aster Manufacturing — visual defect classification | Can a small poisoned or backdoored fraction survive a realistic pipeline and a screening defense? | LAB-05, LAB-06, LAB-07, LAB-08 | LO-33, LO-10, LO-11 |
| [PRJ-03](prj-03-prediction-api-privacy.md) | Helio Health — benefits triage API | What does the prediction interface leak under a fixed query budget, and what does output minimization cost? | LAB-09, LAB-10, LAB-17 | LO-33, LO-12, LO-14, LO-19 |
| [PRJ-04](prj-04-secure-pipeline.md) | Cobalt Models — training and artifact pipeline | Do validation, dependency, signing, and reproducibility controls actually fail closed? | LAB-12, LAB-13 | LO-33, LO-21, LO-22 |
| [PRJ-05](prj-05-rag-agent.md) | Harbor — policy assistant with retrieval and tools | Does the application treat untrusted documents as data, and does the agent enforce authority in code? | LAB-19, LAB-20 | LO-33, LO-25, LO-26, LO-27 |
| [PRJ-06](prj-06-robustness-comparison.md) | Sentinel Vision — access-badge classifier | Which defense gives the best robustness per unit of clean accuracy, false positives, and runtime? | LAB-03, LAB-11 | LO-33, LO-16, LO-17, LO-18 |
| [RT-01](rt-01-red-blue.md) | Pinewood Logistics — dispatch-risk service | Can a bounded red team be detected and contained without blocking benign users? | M17, LAB-14, LAB-15 | LO-34, LO-23, LO-28 |

The capstone options CAP-A…CAP-F are described in the [capstone brief](capstone.md).

## Which project should I choose?

| If you want to practise… | Choose |
|---|---|
| Data integrity, labels, and segment-level monitoring | PRJ-01 |
| Poisoning, backdoors, and screening | PRJ-02 |
| Privacy attacks, extraction, and output minimization | PRJ-03 |
| Supply-chain integrity and fail-closed engineering | PRJ-04 |
| Prompt injection, provenance, and agent authority | PRJ-05 |
| Benchmarking defenses with cost and adaptive attacks | PRJ-06 |
| Detection, response, and purple-team synthesis | RT-01 |

Score each option from 1 to 5 on skill fit, data access, compute, measurement clarity, risk/ethics, and interest; multiply by the weights in [Lesson 18.1](../modules/m18-capstone-and-research/lesson-1-choosing-and-scoping-a-capstone.md). Data access of 4 or 5 is close to mandatory.

## What every project produces

| Artifact | Purpose |
|---|---|
| `scope.md` and `authorization.md` | System, decision, data, non-goals, stop conditions |
| `system.md` and `data-inventory.csv` | Architecture, boundaries, classification, owners |
| `threat-model.md` and `risk-register.csv` | Adversary profiles, scored risks, dispositions |
| `test-plan.csv` | Hypothesis, procedure, budget, oracle, metric, evidence |
| `baseline/` and `run.json` | Frozen clean measurement with seeds and versions |
| `experiments/` | Attack results with denominators and budgets |
| `defense/` | Control evaluation, costs, adaptive retest |
| `findings/` and `report.md` | Severity, evidence, owner, cost, retest |
| `manifest.json` | Hashes and versions for reproduction |
| `briefing.md` | Ten-minute decision-oriented summary |

The project rubric is in each brief. It weights scope and data (10), threat model (15), baseline and design (15), attack and analysis (20), defense and evaluation (15), reproducibility (10), communication (10), and ethics and limitations (5).

## Time and rhythm

| Week | Work | Hours |
|---|---|---:|
| 1 | Scope, system, data inventory | 2.5 |
| 1–2 | Threat model and test plan | 1.5 |
| 2 | Baseline and data audit | 3 |
| 3 | Attack experiments | 3 |
| 3–4 | Defense, adaptive retest, report | 2 |

The hours are a budget, not a target. If a stage runs past 150% of its allocation, stop, record the partial result, and cut a later experiment rather than the baseline or the report.

## Assessment

- **Module 16 project:** scored against the project rubric; every dimension at Developing or above, with at least six at Proficient.
- **Module 17 RT-01:** scored against the RT-01 rubric; red and blue results reported separately, then synthesized.
- **Capstone:** scored against the capstone rubric; every dimension at Proficient or above for completion.

Self-score before reading the [evaluator guide](evaluator-guide.md). The guide is written for instructors and self-reviewers and contains reference findings and calibration notes; reading it before attempting the work defeats the assessment.

## Safety rules for every project

- Local, synthetic, or authorized public sandbox targets only.
- No real personal, payment, health, or employee data.
- No third-party production system, even read-only.
- No real credentials; create local mock keys.
- No malicious model files distributed outside the exercise directory.
- Services bind to `127.0.0.1`; no network egress.
- Stop conditions are written before the first experiment and honored.

A project that violates a safety rule is not assessed on its technical merit. The rule is the first acceptance criterion.

## Relationship to the capstone

| Project | Capstone route | What the capstone adds |
|---|---|---|
| PRJ-01 | CAP-A | A second segment, a monitoring control, an adaptive variant, a costed remediation plan |
| PRJ-02 | CAP-A or CAP-B | Two defenses under an adaptive trigger; a poison-budget curve; a benchmark critique |
| PRJ-03 | CAP-C | A DP defense or release with accounting; a utility–privacy curve |
| PRJ-04 | CAP-D | A second environment, key rotation, a compromised-build-host scenario |
| PRJ-05 | CAP-E | A test harness with adaptive injections and a containment test |
| PRJ-06 | CAP-B | A published-style replication plus a methodological critique |
| RT-01 | CAP-A or CAP-E | A full assessment or an agentic evaluation harness |

A capstone must add at least one of: a new adversary, a new measurement, a new control, or a replication with a critique. Re-running a project with more seeds is not a capstone.

## Frequently asked questions

**Can I do more than one project?** Yes, but one is required and depth beats breadth. A second project is useful only if it supplies a skill the capstone needs.

**Can I use a real dataset?** Only if it is public, appropriately licensed, and contains no personal data. The default is synthetic. Record the source, license, and checksum.

**Can I use a real LLM API?** No. The course is offline and key-free. PRJ-05 uses a local mock model because the trust-boundary controls, not model sophistication, are the subject.

**What if my attack fails?** Report it with the budget, attempts, baseline, and interval. A measured negative result is a result. Do not raise the budget silently or tune until it succeeds.

**What if my defense fails?** Report the failure and the residual risk. A defense that is bypassed by an adaptive variant is a finding, not a failed project.

**How much code is expected?** Enough to reproduce the headline result from a clean checkout. The project is an assessment, not a software product; tests and a manifest matter more than features.

**Can I work in a pair?** The course is designed for individual work. If you collaborate, record who did what and ensure each person can reproduce the result and defend every claim.

## Next step

Read [Module 16](../modules/m16-end-to-end-assessment/index.md) before starting a project, [Module 17](../modules/m17-red-team-blue-team/index.md) before RT-01, and the [capstone brief](capstone.md) before extending either into CAP-A…CAP-F.
