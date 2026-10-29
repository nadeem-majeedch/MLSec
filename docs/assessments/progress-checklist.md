# Course Progress Checklist

<span class="mlsec-kind">Assessment</span>

This is the printable, one-page-per-level view of the course. Use it with the [progress record](progress-and-reflection.md), which holds scores, missed item IDs, and retake dates. This page asks a simpler question: is the evidence there?

Write the completion date only when you can point to the artifact. A blank cell is honest; a date without evidence is not.

## How to use it

1. Work one level at a time. Complete the module's lessons, exercises, quiz, and lab before moving to the next module.
2. Record the date in the last column only after the lab checker passes and the report answers its reflection questions.
3. Take the level check after the level's labs, not instead of them. A pass without artifacts is a paper result.
4. Keep the artifact folder. The project and capstone reuse lab evidence.
5. If a lab exceeds 150% of its stated time, write the blocker in the record and stop. Do not skip the evidence to keep the schedule.

## Level 1 — Foundations

**Effort:** 39 hours · **Level check:** [LC-1](level-checks/index.md) · **Gate artifact:** LAB-01, LAB-01B, and LAB-02

| Module | Lab(s) | Knowledge checks | Evidence to keep | Date completed |
|---|---|---|---|---|
| M00 Orientation | LAB-01 | QZ-00 | Environment report, study plan, signed ethics statement | |
| M01 Python and tooling | LAB-01 | QZ-01, QZ-01B | Model, split indices, metrics, manifest, report | |
| M02 ML fundamentals | LAB-01B | QZ-02, QZ-02B | Leaky and repaired estimates side by side, with intervals | |
| M03 Threat modeling | LAB-02 | QZ-03, QZ-03B | Threat model, attack trees, framework crosswalk, checker output | |

**Level gate:** LC-1 score recorded · [ ] All three artifacts complete and reproducible

## Level 2 — Core attacks

**Effort:** 55 hours · **Level check:** [LC-2](level-checks/index.md) · **Gate artifact:** LAB-03 through LAB-10

| Module | Lab(s) | Knowledge checks | Evidence to keep | Date completed |
|---|---|---|---|---|
| M04 Evasion | LAB-03, LAB-04 | QZ-04, QZ-04B | ASR curves, targeted and transfer results, budget checks | |
| M05 Poisoning | LAB-05, LAB-06 | QZ-05, QZ-05B | Poisoning curve, targeted flip, screening results | |
| M06 Backdoors | LAB-07, LAB-08 | QZ-06, QZ-06B | Trigger design, attack success, false-trigger cost, detection | |
| M07 Extraction and privacy | LAB-09, LAB-10 | QZ-07, QZ-07B | Extraction fidelity/query budget, membership AUC and baseline | |

**Level gate:** LC-2 score recorded · [ ] All eight artifacts complete and reproducible

## Level 3 — Practical defenses and secure engineering

**Effort:** 54 hours · **Level check:** [LC-3](level-checks/index.md) · **Gate artifact:** LAB-11 through LAB-15

| Module | Lab(s) | Knowledge checks | Evidence to keep | Date completed |
|---|---|---|---|---|
| M08 Robustness and defense | LAB-11 | QZ-08, QZ-08B | Clean/robust accuracy, adaptive-attack result, defense costs | |
| M09 Data integrity | LAB-12 | QZ-09, QZ-09B | Validation report, leakage audit, hashes and split checks | |
| M10 Supply chain | LAB-13 | QZ-10, QZ-10B | Dependency and artifact audit, provenance record, findings | |
| M11 Serving and response | LAB-14, LAB-15 | QZ-11, QZ-11B | Hardened API evidence, detection rules, incident timeline and rollback | |

**Level gate:** LC-3 score recorded · [ ] All five artifacts complete and reproducible

## Level 4 — Advanced and emerging security

**Effort:** 54 hours · **Level check:** [LC-4](level-checks/index.md) · **Gate artifact:** LAB-16 through LAB-20

| Module | Lab(s) | Knowledge checks | Evidence to keep | Date completed |
|---|---|---|---|---|
| M12 Federated learning | LAB-16 | QZ-12, QZ-12B | Update-poisoning result, aggregation comparison, client validation | |
| M13 Privacy-preserving ML | LAB-17 | QZ-13, QZ-13B | Privacy-utility curve, epsilon accounting, membership signal | |
| M14 Explainability and fairness | LAB-18 | QZ-14, QZ-14B | Explanation stability, subgroup audit, trade-off report | |
| M15 Generative AI and agents | LAB-19, LAB-20 | QZ-15, QZ-15B | Injection test, provenance boundary, tool-authority evidence | |

**Level gate:** LC-4 score recorded · [ ] All five artifacts complete and reproducible

## Level 5 — Applied projects

**Effort:** 34 guided hours plus a 40-hour capstone · **Level check:** [LC-5](level-checks/index.md)

| Module | Work | Knowledge checks | Evidence to keep | Date completed |
|---|---|---|---|---|
| M16 End-to-end assessment | One of [PRJ-01…PRJ-06](../projects/index.md) | QZ-16, QZ-16B | Scope, threat model, test plan, baseline, experiments, defense, findings, briefing | |
| M17 Red team and blue team | [RT-01](../projects/rt-01-red-blue.md) | QZ-17, QZ-17B | Rules of engagement, red evidence, detections, adaptive retest, purple synthesis | |
| M18 Capstone and research | [Capstone](../projects/capstone.md) CAP-A…CAP-F | QZ-18, QZ-18B | Proposal, report, reproduction package, briefing | |

**Level gate:** LC-5 score recorded · [Final assessment](final-assessment/index.md) attempted · [ ] Project, RT-01, and capstone artifacts complete

## Project and capstone evidence

| Stage | Evidence | Done |
|---|---|---|
| Project scope and authorization | `scope.md`, `authorization.md`, system description, data inventory | [ ] |
| Project threat model | Adversary profiles, scored risks, dispositions, test plan | [ ] |
| Project baseline | Frozen clean measurement, seeds, versions, `run.json` | [ ] |
| Project experiments | Attack results with denominators, budgets, and uncertainty | [ ] |
| Project defense | Control evaluation, cost, adaptive retest, residual risk | [ ] |
| Project report and briefing | Findings, severity, owner, retest, ten-minute briefing | [ ] |
| Capstone M0 — Proposal (2 h) | Scoped question, option, success criterion, stop condition | [ ] |
| Capstone M1 — Threat model (4 h) | System, boundaries, adversaries, risks, ethics | [ ] |
| Capstone M2 — Baseline (6 h) | Reproducible clean measurement with manifest | [ ] |
| Capstone M3 — Attacks (12 h) | Bounded experiments and negative results with bounds | [ ] |
| Capstone M4 — Defense (10 h) | Control, cost, adaptive retest, residual risk | [ ] |
| Capstone M5 — Report and briefing (6 h) | Report, reproduction package, briefing | [ ] |

The exact milestone requirements and scoring are in the [capstone brief](../projects/capstone.md).

## The evidence standard

A box is earned by an artifact, not by an attempt.

| Check | Pass condition |
|---|---|
| Artifact exists | The named files open and match the brief's schema |
| Checker passes | The lab's checker exits 0 on the documented folder |
| Manifest is real | SHA-256 hashes match the files and sizes |
| Report is complete | Threat model, method, results, limitations, and one defensible claim |
| Reproduction works | A fresh process reproduces the headline number from the documented command |
| Reflection exists | Five lines: worked, failed, next test, misunderstanding, missing evidence |
| Safety is stated | Local or synthetic targets only; no credentials or personal data |

## Before you call the course complete

- [ ] All 19 modules read, with the module knowledge check attempted.
- [ ] All 21 labs complete, checker-passing, and stored with their manifests.
- [ ] Five level checks attempted; scores recorded with missed item IDs.
- [ ] The final assessment attempted after the capstone proposal.
- [ ] One applied project or RT-01 complete, scored against its rubric.
- [ ] Any mini-projects (MP-01…MP-04) assigned by your program are recorded with their artifacts.
- [ ] The capstone report, reproduction package, and briefing complete.
- [ ] The progress record filled in, including at least one documented blocker and how you resolved it.
- [ ] A portfolio folder a second person can open without asking you where anything is.

A track is complete when its modules and labs are complete. The full program adds a project, RT-01, and the capstone, plus any mini-projects your program assigns. Optional challenge exercises are depth, not completion requirements.

## Print or copy

Use your browser's print command to make a paper copy; the navigation and header are hidden in print. If you keep a digital copy, duplicate this page into your own `work/` folder and fill in the dates there. The site stores nothing.

## Related pages

- [Progress and reflection record](progress-and-reflection.md) — scores, missed items, retakes, and next actions.
- [Lab completion checklists](rubrics/lab-completion-checklists.md) — the eight checks behind every lab.
- [Rubrics](rubrics/index.md) — lab, project, and capstone scoring.
- [Learning paths](../learning-paths.md) — choose or change a route.
