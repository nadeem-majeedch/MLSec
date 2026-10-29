# Learning Paths

<span class="mlsec-kind">Start here</span>

ML-Sec has one spine — Modules M00 to M18 — and several honest entry points. Choose a path by the evidence you can already produce, not by how confident you feel. Every path keeps the same rule: you finish with artifacts that another person can inspect and reproduce.

If you are unsure where you belong, take the 30-minute [prerequisite diagnostic](assessments/diagnostic/index.md). It measures Python, ML fundamentals, statistics, and security vocabulary. A low score is a routing result, not a rejection.

## Paths at a glance

<div class="grid cards" markdown>

-   **Complete beginner**

    ---

    Start at M00 and follow the spine. The full program is 276 hours: 236 hours of guided modules, projects, and RT-01, plus a 40-hour capstone.

    Best if you have some Python but have not studied ML security.

    [Full path](#complete-beginner)

-   **ML practitioner new to security**

    ---

    Keep the ML you already have, add threat modeling and the attack lifecycle, then specialize in the controls you will actually operate.

    Best if you can train and evaluate a model but have not attacked one.

    [Full path](#ml-practitioner-new-to-security)

-   **Security practitioner new to ML**

    ---

    Learn enough ML to read a model card and a gradient, then apply your existing detection, response, and assurance habits to ML systems.

    Best if you know CIA, authentication, and incident response, but not scikit-learn.

    [Full path](#security-practitioner-new-to-ml)

-   **Generative AI and agent security**

    ---

    Take the 97-hour specialization route through M00–M03 and M15, then extend it with M07 and M11 for privacy and API depth.

    Best if you build with LLMs, retrieval, or tool-using agents.

    [Full path](#generative-ai-and-agent-security)

-   **Assessment and red-team specialization**

    ---

    Build the assessment method first, then run one project and RT-01. The 113-hour specialization ends in a capstone proposal and report.

    Best if you already have security or ML experience and need the audit workflow.

    [Full path](#assessment-and-red-team-specialization)

-   **Research-bound**

    ---

    Follow the full spine and add the [research reading guide](research-reading-guide.md), a reproduction, and a capstone question that extends one project.

    Best if you intend to publish, review, or build on the literature.

    [Full path](#research-bound)

</div>

## Complete beginner

**Effort:** 276 hours · **Typical duration:** 28–46 weeks at 6–15 hours per week · **Start:** M00

| Phase | What you study | Labs and evidence | Milestone |
|---|---|---|---|
| Foundations (39 h) | [M00](modules/m00-orientation/index.md)–[M03](modules/m03-threat-modeling/index.md): orientation, Python and data tooling, ML fundamentals, threat modeling | LAB-01, LAB-01B, LAB-02 | A reproducible baseline and a threat model you can defend |
| Core attacks (to 94 h cumulative) | [M04](modules/m04-evasion/index.md)–[M07](modules/m07-extraction-privacy/index.md): evasion, poisoning, backdoors, extraction and privacy | LAB-03–LAB-10 | Attack dossiers with budgets, base sets, and honest denominators |
| Practical defenses (to 148 h cumulative) | [M08](modules/m08-robustness-defense/index.md)–[M11](modules/m11-serving-monitoring/index.md): robustness, data integrity, supply chain, serving and response | LAB-11–LAB-15 | Robustness audit, validation report, signed artifact, hardened API, IR package |
| Frontier systems (to 202 h cumulative) | [M12](modules/m12-federated-learning/index.md)–[M15](modules/m15-genai-llm-agents/index.md): federation, privacy, explainability, generative and agentic security | LAB-16–LAB-20 | Federated, privacy, subgroup, RAG, and agent-containment reports |
| Synthesis | [M16](modules/m16-end-to-end-assessment/index.md)–[M18](modules/m18-capstone-and-research/index.md), one project, RT-01 | PRJ-01…PRJ-06 or RT-01 | Assessment dossier and red/blue package |
| Capstone (40 h) | [Capstone](projects/capstone.md) M0–M5 | CAP-A…CAP-F | Report, reproduction package, and briefing |

**Do not skip the early labs.** LAB-01 and LAB-01B establish the split, seed, and metric discipline that every later attack assumes. If you are short on time, shorten the reading, not the lab.

## ML practitioner new to security

**Effort:** about 94 hours for the core-attacks track, or 113 hours for the assessment specialization · **Start:** M00, then M03

| Order | Work | Why |
|---:|---|---|
| 1 | [M00](modules/m00-orientation/index.md) | Sets the evidence standard and rules of engagement |
| 2 | [M03](modules/m03-threat-modeling/index.md) | Turns “the model can be fooled” into a testable threat model |
| 3 | [M04](modules/m04-evasion/index.md)–[M07](modules/m07-extraction-privacy/index.md) | Attacks on predictions, data, behavior, and privacy |
| 4 | [M08](modules/m08-robustness-defense/index.md)–[M11](modules/m11-serving-monitoring/index.md) | Defenses, data integrity, supply chain, and operations |
| 5 | [M16](modules/m16-end-to-end-assessment/index.md) plus one project | Proves you can run an assessment, not just an experiment |

Skim M01 and M02 only where the self-check fails. You still need the lab protocol from LAB-01B: grouped splits, leakage removal, threshold selection, and uncertainty. The [student guide](student-guide.md#baseline) lists the exact self-checks.

## Security practitioner new to ML

**Effort:** 148 hours for the practitioner track · **Start:** M00, then M01 and M02

| Order | Work | Why |
|---:|---|---|
| 1 | [M00](modules/m00-orientation/index.md) and [M01](modules/m01-python-refresher/index.md) | Python, NumPy, pandas, and scikit-learn at the depth the labs require |
| 2 | [M02](modules/m02-ml-fundamentals/index.md) | Loss, gradients, evaluation, leakage, and reporting |
| 3 | [M03](modules/m03-threat-modeling/index.md) | Maps your existing security vocabulary onto ML systems |
| 4 | [M04](modules/m04-evasion/index.md)–[M11](modules/m11-serving-monitoring/index.md) | Attacks, defenses, and secure operations |
| 5 | One project and RT-01 | Assessment and red/blue evidence |

Your advantage is detection and response. Use it in M11 and LAB-15, but do not skip the gradient work in M02 and M04: a detection rule you cannot measure against an adaptive attacker is a guess.

## Generative AI and agent security

**Effort:** 97 hours for the core specialization; more if you add M07 and M11 · **Start:** M00

| Order | Work | Why |
|---:|---|---|
| 1 | [M00](modules/m00-orientation/index.md)–[M03](modules/m03-threat-modeling/index.md) | Evidence standard, ML basics, threat modeling |
| 2 | [M07](modules/m07-extraction-privacy/index.md) | Prediction APIs as an attack surface; extraction and membership inference |
| 3 | [M11](modules/m11-serving-monitoring/index.md) | Authentication, request bounds, monitoring, and incident response |
| 4 | [M15](modules/m15-genai-llm-agents/index.md) | Prompt injection, retrieval boundaries, sensitive output, agent authority |
| 5 | LAB-14, LAB-19, LAB-20, then [PRJ-05](projects/prj-05-rag-agent.md) | Hardened API, RAG trust boundary, agent containment, applied dossier |

M07 and M11 are the depth extension named on the landing page; the 97-hour figure covers the core M00–M03 + M15 + capstone route in the [student guide](student-guide.md#schedules). Add time for the extension.

## Assessment and red-team specialization

**Effort:** 113 hours · **Start:** M03, after the diagnostic · **Ends:** capstone proposal and report

| Order | Work | Why |
|---:|---|---|
| 1 | [M00](modules/m00-orientation/index.md)–[M03](modules/m03-threat-modeling/index.md) | Vocabulary, evidence, and threat modeling |
| 2 | [M16](modules/m16-end-to-end-assessment/index.md) | Scoping, test plans, measurement, severity, and remediation |
| 3 | One of [PRJ-01…PRJ-06](projects/index.md) | An 11-hour assessment of one system |
| 4 | [M17](modules/m17-red-team-blue-team/index.md) and [RT-01](projects/rt-01-red-blue.md) | Rules of engagement, red execution, blue detection, purple synthesis |
| 5 | [M18](modules/m18-capstone-and-research/index.md) and [capstone](projects/capstone.md) | Results, limitations, and a research question |

Do not treat the specialization as a shortcut around LAB-03 and LAB-11. The project assumes you can measure an attack and test a defense under an adaptive variant; the briefs name the prerequisite labs.

## Research-bound

**Effort:** 276 hours plus reading time · **Start:** M00 · **Add:** [research reading guide](research-reading-guide.md)

1. Follow the complete spine and keep every manifest. A result you cannot reproduce is not a finding you can extend.
2. Read the foundational papers alongside M04–M08 using the [reading guide](research-reading-guide.md). For each paper, write the claim, the threat model, the budget, the base set, and the limitation before you read the results.
3. In M18, choose a capstone that extends one project along a single axis: a new attack, a new defense, a new population, or a replication with a changed assumption.
4. Report a negative result with a bound. “The attack did not succeed in 200 trials; the 95% upper bound is about 1.5%” is a stronger contribution than an unsupported security claim.

## Pace and switching

| Pace | Foundations (39 h) | Core attacks (94 h) | Practitioner (148 h) | Full program (276 h) |
|---|---:|---:|---:|---:|
| 6 h/week | 7 weeks | 16 weeks | 25 weeks | 46 weeks |
| 8 h/week | 5 weeks | 12 weeks | 19 weeks | 35 weeks |
| 10 h/week | 4 weeks | 10 weeks | 15 weeks | 28 weeks |
| 15 h/week | 3 weeks | 7 weeks | 10 weeks | 19 weeks |

You can switch paths at a module boundary. Finish the lab you started, write the reflection, and record the switch in the [progress record](assessments/progress-and-reflection.md). Do not switch mid-lab to avoid a difficult measurement; a documented blocker is evidence, an abandoned lab is debt.

## Every path shares the same contract

| Requirement | What it means |
|---|---|
| Threat model first | Goal, knowledge, capability, budget, base set, and metric before code |
| Reproducibility | Pinned environment, fixed seeds, documented command, manifest |
| Honest measurement | Denominators, uncertainty, negative results, and limitations |
| Safety | Local, synthetic, or sandbox targets only; benign payloads |
| Reflection | What worked, what failed, what you would test next, what is missing |

Read [How to use this site](site-guide.md) for navigation conventions and [Troubleshooting](troubleshooting.md) when something does not work.

## First week

- [ ] Take the [prerequisite diagnostic](assessments/diagnostic/index.md) or run the [baseline self-checks](student-guide.md#baseline).
- [ ] Set up the environment with the [setup walkthrough](student-guide.md#setup).
- [ ] Read [M00](modules/m00-orientation/index.md) and sign the authorized-use statement.
- [ ] Run [LAB-01](labs/lab-01.md) top to bottom, then run its checker.
- [ ] Open the [progress checklist](assessments/progress-checklist.md) and record the lab artifact, not just the score.
- [ ] Write five lines of reflection. The first week is where the evidence habit starts.
