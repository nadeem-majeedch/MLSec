---
title: Home
description: A self-study, lab-driven course on adversarial machine learning, privacy, and secure ML engineering.
---

<div class="mlsec-hero">
  <p class="mlsec-kicker">Self-study · Lab-driven · CPU-first</p>
  <h1>Machine Learning Security (ML-Sec)</h1>
  <p>Learn how machine-learning systems fail under adversarial pressure — and how to measure, defend, and engineer against that failure.</p>
  <p><strong>Model the adversary, measure the effect, engineer the control, and re-test.</strong></p>
  <div class="mlsec-hero__actions">
    <a class="md-button md-button--primary" href="learning-paths/">Choose your path</a>
    <a class="md-button" href="modules/">Course roadmap</a>
    <a class="md-button" href="labs/">Browse the 21 labs</a>
  </div>
</div>

<div class="mlsec-stats">
  <div class="mlsec-stat"><strong>19</strong><span>modules, M00–M18</span></div>
  <div class="mlsec-stat"><strong>88</strong><span>lessons</span></div>
  <div class="mlsec-stat"><strong>21</strong><span>runnable labs · 84 hours</span></div>
  <div class="mlsec-stat"><strong>276 h</strong><span>full program with capstone</span></div>
  <div class="mlsec-stat"><strong>35</strong><span>measurable outcomes</span></div>
  <div class="mlsec-stat"><strong>0</strong><span>GPUs, API keys, or paid services required</span></div>
</div>

!!! note "Course status (2026-10-28)"
    **Levels 1–5 are published.** Modules [M00](modules/m00-orientation/index.md) through [M18](modules/m18-capstone-and-research/index.md) are complete: 88 lessons, nineteen knowledge checks with separate answer files, 75 exercises, and 21 runnable labs (LAB-01, LAB-01B, LAB-02…LAB-20) with starter code, solutions, and independent checkers. Level 5 adds six 11-hour projects, a 9-hour red/blue exercise, and a 40-hour [capstone](projects/capstone.md) with six options. All project work is local and synthetic.

## Start where you are

<div class="grid cards" markdown>

-   **Complete beginner**

    ---

    Begin with the [student guide](student-guide.md) and [M00](modules/m00-orientation/index.md), then follow M01 and M02. The full spine runs to the capstone.

    [See the beginner path](learning-paths.md#complete-beginner)

-   **ML practitioner new to security**

    ---

    Skim M02, take [M03](modules/m03-threat-modeling/index.md) in full, then start [M04](modules/m04-evasion/index.md). Your modeling skill is an advantage; the threat model is the new part.

    [See the practitioner path](learning-paths.md#ml-practitioner-new-to-security)

-   **Security practitioner new to ML**

    ---

    Take [M01](modules/m01-python-refresher/index.md), then M02 and M03. Your detection and response habits return in M11 with new evidence requirements.

    [See the security path](learning-paths.md#security-practitioner-new-to-ml)

-   **Generative AI and agents**

    ---

    Start with M00–M03, then [M07](modules/m07-extraction-privacy/index.md), [M11](modules/m11-serving-monitoring/index.md), and [M15](modules/m15-genai-llm-agents/index.md). Finish with LAB-19, LAB-20, and [PRJ-05](projects/prj-05-rag-agent.md).

    [See the GenAI path](learning-paths.md#generative-ai-and-agent-security)

-   **Ready to run an assessment**

    ---

    Take [M03](modules/m03-threat-modeling/index.md) and [M16](modules/m16-end-to-end-assessment/index.md), complete one [project](projects/index.md), then scope the [capstone](projects/capstone.md).

    [See the assessment path](learning-paths.md#assessment-and-red-team-specialization)

-   **Research-bound**

    ---

    Follow the full spine, add the [research reading guide](research-reading-guide.md), and extend one project into a capstone question.

    [See the research path](learning-paths.md#research-bound)

</div>

Before the first lab, check the [prerequisites and recovery path](student-guide.md#baseline) and set up your environment with the [setup walkthrough](student-guide.md#setup). The full [learning paths](learning-paths.md) page compares effort, duration, and first artifacts.

## What you will be able to do

- **Explain** an ML system's architecture, lifecycle, trust boundaries, and threat model using recognized frameworks.
- **Implement and evaluate** evasion, poisoning, backdoor, extraction, inference, and inversion attacks under explicit budgets.
- **Select, implement, and critically evaluate** defenses, including adaptive-attack evaluation and certification.
- **Harden** data pipelines, model artifacts, serving infrastructure, and monitoring and response.
- **Assess and mitigate** risks in federated, generative, and agentic systems.
- **Run and defend** an authorized end-to-end assessment, including a red-team/blue-team exercise with bounded attacks, measured defenses, and a stated residual risk.
- **Communicate** findings with reproducible evidence, correct severity, lawful conduct, and responsible disclosure.

These are the seven program-level outcomes. The full catalog of 35 measurable outcomes is in [Learning outcomes](learning-outcomes.md).

## The course in six stages

| Stage | Modules | Question it answers | Gate artifact |
|---|---|---|---|
| [1. Foundations](modules/index.md#stage-1) | [M00](modules/index.md#m00)–[M03](modules/index.md#m03) | What are we protecting, from whom, and how do we describe it? | Threat model (LAB-02) |
| [2. Core attacks](modules/index.md#stage-2) | [M04](modules/index.md#m04)–[M07](modules/index.md#m07) | How are predictions, training data, behavior, and privacy attacked? | Evasion, integrity, and extraction dossiers (LAB-03…LAB-10) |
| [3. Defenses and data integrity](modules/index.md#stage-3) | [M08](modules/index.md#m08)–[M09](modules/index.md#m09) | Does the defense survive an adaptive attack, and can we trust the data? | Robustness audit and validation report (LAB-11…LAB-12) |
| [4. Secure engineering and operations](modules/index.md#stage-4) | [M10](modules/index.md#m10)–[M11](modules/index.md#m11) | How do we build, ship, and operate ML systems securely? | Signed artifact, hardened API, and IR package (LAB-13…LAB-15) |
| [5. Privacy and frontier systems](modules/index.md#stage-5) | [M12](modules/index.md#m12)–[M15](modules/index.md#m15) | What changes with federation, privacy guarantees, explanations, generative models, and agents? | Federated, privacy, subgroup, and red-team reports (LAB-16…LAB-20) |
| [6. Applied projects and synthesis](modules/index.md#stage-6) | [M16](modules/index.md#m16)–[M18](modules/index.md#m18) | Can you run an end-to-end assessment, red-team a system under rules of engagement, and defend the result? | Project dossier (PRJ-01…PRJ-06 or RT-01) and [capstone](projects/capstone.md) (CAP-A to CAP-F) |

The [course roadmap](modules/index.md) gives each module's prerequisites, effort, labs, and outcomes. The dependency graph and lesson inventory are in the [module map](module-map.md).

## How a module works

Every module has the same anatomy:

> **Scenario → objectives → lessons → lab → quiz → reflection → artifact**

You read a failure story, state what you will be able to do, work through a self-contained explanation, run and modify a reproducible experiment, take a self-graded knowledge check, and finish an artifact that another engineer could audit. A module is only published when all of those parts are real.

Each lesson ends with a “Check yourself” section and a next step. Each lab ends with a checker and a reflection. Each assessment page states its attempt rules before the first item. [How to use this site](site-guide.md) explains the page types and navigation.

## Workload

The full program is approximately **276 hours**: 236 hours of guided modules, projects, and the red/blue exercise, plus a 40-hour capstone. The Foundations track is 39 hours, the Core-attacks track is 94 hours, the Practitioner track is 148 hours, and Levels 1–5 together are 236 hours. At 6–10 hours per week, the full program takes roughly 7–11 months.

Detailed tracks, schedules, and a week-by-week plan are in the [student guide](student-guide.md#schedules) and [learning paths](learning-paths.md#pace-and-switching).

## Labs and evidence

The course has 21 lab documents totaling 84 hours, designed CPU-first. Tier A labs target ten minutes or less per run; Tier B labs ship a reduced CPU configuration; GPU work is optional. Every lab produces code, a results write-up, a pinned environment, an artifact manifest, and a reflection.

Level 5 adds six project briefs of about 11 hours each and a 9-hour red-team/blue-team exercise. Each project combines several labs into one assessment dossier: scope, threat model, test plan, baseline, bounded experiments, a defended system, and a report with residual risk. Projects use fictional organizations, synthetic data, and local services; they require no API key and no third-party target. The [project catalog](projects/index.md) explains how to choose one.

You need a laptop, Python 3.14.7, and the pinned requirements in `requirements/labs.txt`. No dataset download is required by any published lab. The [dataset catalog](dataset-catalog.md) records provenance, licenses, and limitations.

## Assessment

Assessment is portfolio-based: knowledge checks 10%, labs and applied projects 40%, mini-projects 20%, capstone 30%. Strong work is reproducible, measured, and honest about limitations. The [assessment layer](assessments/index.md) adds a diagnostic, alternate quizzes, level checks, a final assessment, and rubrics. The [lab guide](labs/index.md) describes the lab sequence, tiers, rubric, and self-assessment protocol.

Track your work with the [progress checklist](assessments/progress-checklist.md) and the [progress record](assessments/progress-and-reflection.md). Tick a box only when the named artifact exists.

## Instructor

**Engr. Dr. Muhammad Nadeem Majeed**
Professor
Department of Data Science (PUCIT)
University of the Punjab, Lahore

ML-Sec is written and maintained by Engr. Dr. Muhammad Nadeem Majeed as a self-study course in the Department of Data Science at PUCIT. Read [About the instructor](about.md) for the course's design principles, scope limits, and corrections policy.

## Reference shelf

- [References](references.md) — frameworks, foundational papers, benchmarks, and reproducibility guidance.
- [Glossary](glossary.md) — plain-language definitions, acronym expansions, and lesson links.
- [Framework mapping](framework-mapping.md) — course topics mapped to NIST, MITRE ATLAS, and OWASP categories.
- [Research reading guide](research-reading-guide.md) — a staged reading path with what to look for in each paper.
- [Dataset catalog](dataset-catalog.md) — provenance, licenses, limitations, and access for every dataset the course mentions.

## Use of the material

The techniques are published research. Apply them only to systems you own or have written permission to test. Labs use local, synthetic, or public sandbox targets. Do not use real personal data, and do not test third-party systems. If you are unsure whether a target is authorized, it is not.

Read the full [responsible-use policy](student-guide.md#safety). It is not legal advice.

## Where to go next

- [Learning paths](learning-paths.md) — beginner-to-advanced routes with effort and first artifacts.
- [Student guide](student-guide.md) — setup, study loop, schedules, labs, assessment, troubleshooting.
- [Course roadmap](modules/index.md) — every module with prerequisites and outcomes.
- [Labs](labs/index.md) — the 21-document lab sequence and the standard artifact.
- [Projects](projects/index.md) — six applied assessment projects and the red/blue exercise.
- [Capstone](projects/capstone.md) — requirements, milestones, rubric, and the route to a research question.
- [Troubleshooting](troubleshooting.md) — site, navigation, and lab-environment problems.
- [Project repository](https://github.com/nadeem-majeedch/MLSec) — source, issues, and corrections.
