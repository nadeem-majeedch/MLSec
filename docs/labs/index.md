---
title: Labs
---

# Labs

The labs are the course. Reading makes the labs intelligible; the labs are where you actually learn to measure an attack, defend a system, and prove that your result is real.

There are **21 lab documents totaling 84 hours**, ordered so that each one gives you the tools the next one assumes. Every lab produces an auditable artifact, not a screenshot.

!!! note "Status"
    All twenty-one labs are built and runnable: [LAB-01](lab-01.md), [LAB-01B](lab-01b.md), and [LAB-02](lab-02.md) through [LAB-20](lab-20.md). Their briefs, starter code, reference implementations, and independent checkers are in the repository. Labs are not the whole assessment: the [project catalog](../project-catalog.md) covers six applied projects, RT-01, and the capstone, each with its own rubric.

## How labs work

Every lab must satisfy the same contract before it is published:

| Requirement | Standard |
|---|---|
| Threat model first | Attacker goal, knowledge, capability, budget, and metric are stated before any code |
| Reproducibility | Pinned dependencies, fixed seeds, documented runtime, deterministic where feasible |
| Compute tier | A laptop CPU, B reduced CPU or free Colab, or C optional GPU |
| Data | Public or synthetic; download script, checksum, and a named fallback |
| Artifact | Code, write-up, environment file, manifest, reflection |
| Safety | Local or sandbox targets only; no host credentials; egress disabled where possible |
| Time box | Stated hours, with an explicit stop point at 150% of the estimate |

If a lab cannot be reproduced from a clean environment, it is not finished. That rule applies to the course maintainers and to you.

## Compute tiers

| Tier | Meaning | What to expect |
|---|---|---|
| A | Laptop CPU | Ten minutes or less per run; an 8 GB machine is the reference floor |
| B | CPU 30–60 minutes, or free Colab | A reduced CPU configuration ships with the lab so hardware never blocks you |
| C | GPU recommended | Optional; never required for completion |

You do not need a GPU to finish the course. Every published lab uses scikit-learn and the standard library; none requires PyTorch, a paid service, or an API key.

## The lab sequence

The "Prior lab" column is guidance, not a hard gate. The module links point to prerequisites and outcomes.

| Lab | Title | Module | Tier | Difficulty | Hours | Prior lab | Status |
|---|---|---|---|---:|---:|---:|---|---|
| [LAB-01](lab-01.md) | Reproducible baseline and environment | [M00](../modules/index.md#m00)–[M01](../modules/index.md#m01) | A | 1 | 3 | None | Built |
| [LAB-01B](lab-01b.md) | Evaluation audit and honest baseline | [M02](../modules/index.md#m02) | A | 2 | 4 | LAB-01 | Built |
| [LAB-02](lab-02.md) | Threat model an ML system | [M03](../modules/index.md#m03) | A | 3 | 4 | LAB-01B recommended | Built |
| [LAB-03](lab-03.md) | Evasion versus perturbation budget | [M04](../modules/index.md#m04) | A | 2 | 4 | LAB-01 | Built |
| [LAB-04](lab-04.md) | Targeted evasion and transfer | [M04](../modules/index.md#m04) | A | 3 | 4 | LAB-03 | Built |
| [LAB-05](lab-05.md) | Label-flip poisoning curve | [M05](../modules/index.md#m05) | A | 2 | 4 | LAB-01B recommended | Built |
| [LAB-06](lab-06.md) | Targeted poisoning and reference-set screening | [M05](../modules/index.md#m05) | A | 3 | 4 | LAB-05 recommended | Built |
| [LAB-07](lab-07.md) | Tabular backdoor with a known trigger | [M06](../modules/index.md#m06) | B | 3 | 4 | LAB-05 or LAB-06 | Built |
| [LAB-08](lab-08.md) | Image backdoor and trigger search | [M06](../modules/index.md#m06) | B | 3 | 4 | LAB-07 recommended | Built |
| [LAB-09](lab-09.md) | Model extraction through a local prediction API | [M07](../modules/index.md#m07) | B | 3 | 4 | LAB-01B | Built |
| [LAB-10](lab-10.md) | Membership inference against a local model | [M07](../modules/index.md#m07) | B | 3 | 3 | LAB-01B | Built |
| [LAB-11](lab-11.md) | Defense evaluation: adversarial training, squeezing, adaptive attack | [M08](../modules/index.md#m08) | A | 3 | 6 | LAB-03, LAB-04 | Built |
| [LAB-12](lab-12.md) | Dataset validation and leakage audit | [M09](../modules/index.md#m09) | A | 3 | 4 | LAB-01B; LAB-05 recommended | Built |
| [LAB-13](lab-13.md) | Supply-chain audit of a toy ML project | [M10](../modules/index.md#m10) | A | 3 | 4 | LAB-01 artifact | Built |
| [LAB-14](lab-14.md) | Hardening a local prediction API | [M11](../modules/index.md#m11) | A | 4 | 5 | LAB-13 recommended | Built |
| [LAB-15](lab-15.md) | Monitoring, drift, and incident response | [M11](../modules/index.md#m11) | A | 3 | 3 | LAB-11, LAB-14 recommended | Built |
| [LAB-16](lab-16.md) | Federated learning attack and defense simulation | [M12](../modules/index.md#m12) | A | 4 | 5 | LAB-05 recommended | Built |
| [LAB-17](lab-17.md) | Privacy budget, noisy release, and utility | [M13](../modules/index.md#m13) | A | 4 | 4 | LAB-10 recommended | Built |
| [LAB-18](lab-18.md) | Explanation stability and subgroup audit | [M14](../modules/index.md#m14) | A | 3 | 4 | LAB-11 recommended | Built |
| [LAB-19](lab-19.md) | RAG trust boundary and indirect prompt injection | [M15](../modules/index.md#m15) | A | 3 | 4 | LAB-14 recommended | Built |
| [LAB-20](lab-20.md) | Agent containment and approval boundaries | [M15](../modules/index.md#m15) | A | 4 | 3 | LAB-19 recommended | Built |

**Reading the table.** **Tier** is the compute requirement (A: laptop CPU; B: reduced CPU or free Colab; C: optional GPU). **Difficulty** runs from 1 (foundational) to 4 (advanced) and describes the reasoning and measurement burden, not the length. **Prior lab** is guidance, not a hard gate. Every lab page states its own threat model, prerequisites, environment, task specification, deliverables, hints, troubleshooting, and rubric.

## Standard workflow

| Phase | What to do |
|---|---|
| Before | Read the threat model and metric definitions. Write down your prediction: what accuracy do you expect to lose, at what budget, and why? |
| During | Run the starter top to bottom once without edits. Then change one variable at a time and record the effect. Keep a short error log. |
| After | Score the artifact against the rubric, write the five-line reflection, and confirm that a fresh process reproduces the headline number. |

Predicting before measuring is not a formality. A prediction that turns out wrong is the most useful thing in your lab notebook, because it exposes the mental model that needs fixing.

## What you deliver

Every lab produces the same artifact anatomy:

- **Code** — runs top to bottom, no hidden state, seeds and versions visible.
- **Write-up** — threat model, method, results, limitations, and one claim you can defend.
- **Environment** — a pinned requirements or lock file.
- **Manifest** — SHA-256 hashes of the model, data snapshot, and key outputs.
- **Reflection** — five lines: what worked, what failed, what you would test next, what you misunderstood, what evidence is missing.

For the built labs, the artifact is a folder containing `metrics.json`, `run.json`, `report.md`, and `manifest.json`; see each lab's README for the exact command. Store your own work in a separate folder, for example `work/m04-lab03/`. Never commit datasets or large checkpoints; record their hashes instead.

The eight evidence checks behind every lab are in the [completion checklists](../assessments/rubrics/lab-completion-checklists.md). The scoring dimensions are in the [standard lab rubric](../assessments/rubrics/lab-rubric.md).

## How you are assessed

| Dimension | Weight | Proficient work |
|---|---:|---|
| Technical correctness | 30 | The attack or defense runs as specified and the metrics are correct |
| Security reasoning | 25 | Explicit threat model, budgets, assumptions, and limitations |
| Experimental method | 20 | Controlled comparisons, multiple seeds, ablations, stated uncertainty |
| Reproducibility | 15 | Pinned environment, seeds, commands, manifest; reproduces from a clean checkout |
| Communication and ethics | 10 | Concise report, correct severity, safety and legal constraints addressed |

**Self-assessment protocol**

1. Attempt the lab without looking at a reference solution.
2. Score your own artifact against the rubric before comparing notes with anyone.
3. Write the five-line reflection.
4. Re-run the headline result in a fresh process or environment.
5. Keep the artifact in your portfolio; the capstone reuses it.

**Stop rule.** If a lab takes more than 150% of its stated time, stop and write down the blocker. A well-documented blocker is evidence of debugging skill; an exhausted all-nighter is not.

## Safety rules

- Use local processes, local containers, synthetic services, or explicitly public sandbox datasets. Do not test third-party systems.
- Run anything that deserializes or executes untrusted content in a disposable container with no host credentials and no network egress unless the lab requires it.
- Do not use real personal data. Privacy labs use public benchmarks or synthetic records.
- Keep offensive payloads benign: a marker file, a canary string, a local mock endpoint.
- If you find a real vulnerability, follow coordinated disclosure: private report, reasonable remediation time, no public exploit before a fix.
- If you are unsure whether a target is authorized, it is not.

## Limited hardware

Every Tier B lab ships a reduced configuration. If a run is still too slow:

1. Reduce the test subset and document the size.
2. Reduce attack steps or restarts and state the budget.
3. Switch to the smaller synthetic dataset where the lab allows it.
4. Use a free Colab runtime for the single slow step, then checkpoint the artifact.
5. Record the trade-off in the write-up; do not silently compare against full-scale numbers.

## Solutions and academic integrity

Every built lab includes a reference implementation, a report template (where applicable), and a checking guide inside the lab folder. Work the starter first; open the reference only after you have a result to compare. The checker tells you whether your artifact is structurally consistent and in the expected range. It cannot tell you whether your reasoning is good.

Every built lab includes a reference implementation and an independent checker. Solutions and answer files stay out of the student navigation so that the labs remain useful for practice.

You may use an AI assistant to explain an error, review code, or suggest a test. You may not submit analysis you cannot defend line by line, fabricate results, or copy another learner's report. Disclose material assistance in a short "Tools used" note.

## Where to go next

- [Course roadmap](../modules/index.md) — prerequisites and outcomes for each module.
- [Student guide](../student-guide.md#labs) — setup, workspace layout, and the study loop.
- [Lab catalog](../lab-catalog.md) — full briefs, task lists, and pitfalls.
- [References](../references.md) — the papers and benchmarks behind each lab.
