---
title: Assessments and Self-Checks
---

# Assessments and Self-Checks

This section is the course's assessment layer. It tells you what to attempt, when to attempt it, how to score it, and what to do with a missed item. It does not replace the labs: a quiz can show that you recognize a mistake; only an artifact shows that you can avoid it.

The module knowledge checks `QZ-00`…`QZ-18` remain inside each module. This section adds:

- a prerequisite diagnostic before M04;
- an alternate quiz for every module (`QZ-00B`…`QZ-18B`) for retakes and spaced review;
- a tagged question bank for targeted practice;
- a check at the end of each of the five levels;
- a cumulative final assessment;
- lab, project, and capstone scoring tools;
- a printable [progress checklist](progress-checklist.md) and a fuller progress and reflection record.

## 1. Start here

| If you are… | Do this first | Then |
|---|---|---|
| Beginning the course | [Prerequisite diagnostic](diagnostic/index.md) (30 min, closed-book) | Use the result to choose the recovery path or start M00 |
| Finishing a module | The module's `QZ-xx` knowledge check, then the [alternate quiz](module-quizzes/index.md) at least one day later | Record misses and revisit the named lesson |
| Finishing a level | The matching [level check](level-checks/index.md) | Compare the result with your lab evidence before starting the next level |
| Tracking what is left | The [progress checklist](progress-checklist.md) | Record each date only when the named artifact exists |
| Preparing for the capstone | The [final assessment](final-assessment/index.md) and the [capstone rubric](rubrics/capstone-rubric.md) | Score your proposal against the rubric before M0 |
| Reviewing after a break | The [question bank](question-bank/index.md), filtered by module | Retake only the modules you miss |

## 2. Attempt-first rules

1. Answer without notes, the lesson pages, or an AI assistant. The diagnostic and checks are retrieval practice; open notes turn them into copying.
2. Write reasoning for every item that asks for it. A correct letter with a wrong reason is a miss.
3. Score only after the attempt is complete. Keys are separate files in the course repository under `assessments/answer-keys/`; they are not linked from this page.
4. For written answers, compare against the key's **required elements**, not its exact wording. If your answer reaches the same decision with different evidence, it can still earn the point.
5. Record the attempt in the [progress and reflection record](progress-and-reflection.md), including the score, the item IDs missed, and the section you will revisit.
6. Wait at least one day before a retake. A retake immediately after reading the key measures recognition, not retention.

The repository is public. The keys are separate and out of the site navigation, but they are not secret. The workflow is attempt-first by design, not by enforcement.

## 3. Assessment map

### 3.1 Diagnostic

| ID | Items | Points | Time | Pass | Covers |
|---|---:|---:|---:|---:|---|
| DIA-01 | 20 | 20 | 30 min | 14/20 | Python, ML fundamentals, statistics and math, basic security |

A score below 14 is not a rejection. It tells you which of the four domains to strengthen before M04, where the attacks begin to assume fluency with arrays, gradients, metrics, and threat vocabulary.

### 3.2 Module alternate quizzes

Each quiz has 8 items, 12 points, and a 20-minute guide. Pass is 10/12. Every module M00–M18 has one.

| Quiz | Module | Quiz | Module |
|---|---|---|---|
| [QZ-00B](module-quizzes/qz-00b.md) | M00 Orientation | [QZ-10B](module-quizzes/qz-10b.md) | M10 Supply chain |
| [QZ-01B](module-quizzes/qz-01b.md) | M01 Python and tooling | [QZ-11B](module-quizzes/qz-11b.md) | M11 Serving and incident response |
| [QZ-02B](module-quizzes/qz-02b.md) | M02 ML fundamentals | [QZ-12B](module-quizzes/qz-12b.md) | M12 Federated learning |
| [QZ-03B](module-quizzes/qz-03b.md) | M03 Threat modeling | [QZ-13B](module-quizzes/qz-13b.md) | M13 Privacy-preserving ML |
| [QZ-04B](module-quizzes/qz-04b.md) | M04 Evasion | [QZ-14B](module-quizzes/qz-14b.md) | M14 Explainability and fairness |
| [QZ-05B](module-quizzes/qz-05b.md) | M05 Poisoning | [QZ-15B](module-quizzes/qz-15b.md) | M15 Generative AI and agents |
| [QZ-06B](module-quizzes/qz-06b.md) | M06 Backdoors | [QZ-16B](module-quizzes/qz-16b.md) | M16 End-to-end assessment |
| [QZ-07B](module-quizzes/qz-07b.md) | M07 Extraction and privacy | [QZ-17B](module-quizzes/qz-17b.md) | M17 Red team and blue team |
| [QZ-08B](module-quizzes/qz-08b.md) | M08 Robustness and defense | [QZ-18B](module-quizzes/qz-18b.md) | M18 Capstone and research |
| [QZ-09B](module-quizzes/qz-09b.md) | M09 Data integrity | | |

Quiz B is an alternate form, not a harder version of Quiz A. Use it for a clean second attempt after reviewing Quiz A, or for spaced review three to four weeks after the module. Do not use it to replace the module lab.

### 3.3 Level checks

| ID | Level | Modules | Items | Points | Pass |
|---|---|---|---:|---:|---:|
| [LC-1](level-checks/lc-1.md) | Foundations | M00–M03 | 10 | 20 | 16/20 |
| [LC-2](level-checks/lc-2.md) | Core attacks | M04–M07 | 10 | 20 | 16/20 |
| [LC-3](level-checks/lc-3.md) | Practical defenses | M08–M11 | 10 | 20 | 16/20 |
| [LC-4](level-checks/lc-4.md) | Advanced and emerging security | M12–M15 | 10 | 20 | 16/20 |
| [LC-5](level-checks/lc-5.md) | Applied projects | M16–M18 | 10 | 20 | 16/20 |

A level check is cumulative within its level. It assumes you have completed the labs, but it does not test lab execution. If you pass a level check and cannot produce the level's lab artifacts, the check is not evidence of competence.

### 3.4 Final assessment

The [integrated final assessment](final-assessment/index.md) is 25 items, 100 points, and about three hours. It samples all five levels and includes one integrative design question. The pass standard for course completion is 80/100, but a score is not a certificate and does not replace the capstone.

### 3.5 Question bank

The [question bank](question-bank/index.md) contains 56 additional items: multiple-choice, true/false, short-answer, and scenario questions. Every item is tagged with module, outcome, Bloom level, and difficulty. Use it for targeted review, not as a third full quiz.

### 3.6 Rubrics and records

- [Standard lab rubric](rubrics/lab-rubric.md) — the five dimensions used for every lab.
- [Practical completion checklists](rubrics/lab-completion-checklists.md) — the evidence gate for each of the 21 labs.
- [Capstone self-scoring rubric](rubrics/capstone-rubric.md) — the eight capstone dimensions, automatic fails, and evidence checklist.
- [Project and RT-01 scoring](rubrics/project-rubric.md) — how applied projects and the red/blue exercise are scored.
- [Progress and reflection record](progress-and-reflection.md) — the module-by-module record you keep.

## 4. How to interpret a score

| Result | What it means | What to do |
|---|---|---|
| Below the pass mark on one domain | A local gap, not a failure of the whole course | Review the named lesson and retake after a day |
| Below the pass mark on most domains | The module's lab was completed without the underlying model | Reread the lessons, rerun the lab with predictions, then retake |
| Pass with a weak scenario answer | Recognition is present; judgment is not yet | Rewrite the scenario answer against the key's required elements |
| High score, weak lab | Test-taking skill, not execution | Treat the lab as incomplete until the artifact reproduces |
| High score and strong lab | The outcome is supported by two kinds of evidence | Move on; schedule a spaced review |

A score is diagnostic, not moral. The useful output of any attempt is a short list: which item IDs you missed, which concept each one tests, and the next action.

## 5. What is not assessed here

- Your ability to run code, reproduce a number, or debug an environment. The labs and their checkers assess that.
- Your ability to design and defend an end-to-end assessment. The project, RT-01, and capstone assess that.
- Your conduct. The ethics statement and authorized-use rules are pass/fail conditions in the rubrics, not quiz items.

## 6. Professional practice in assessments

Every assessment in this section follows the course's rules:

- No question asks you to test a system you do not own or have written permission to test.
- No scenario uses real personal data, real credentials, or a real third-party service.
- Framework mappings are used only where the course teaches them, and they are not presented as certification or coverage.
- A failed or negative result is a legitimate answer when it is measured and reported honestly.

If an assessment item appears to require an unsafe action, stop and report it as an issue. The correct response to an out-of-scope request is refusal, not a workaround.
