# Course Roadmap and Module Guide

The course has **18 modules plus a capstone**, arranged in six stages. This page is the navigation target for every module and the place to check prerequisites before you start one.

Each entry states the stage, effort, prerequisite, lesson count, lab, and outcomes, followed by why the module matters and what you will produce. Module effort is total learner time: reading, exercises, quiz, and lab or project.

!!! note "Status"
    **Levels 1–5 (M00–M18) are published and runnable.** Their lessons, knowledge checks, exercises, answer files, labs (LAB-01…LAB-20), six project briefs, and the red/blue exercise are complete. The capstone brief, milestones, and rubric are published; no learner capstone work is included. The lesson-by-lesson inventory is in the [module map](../module-map.md); the design rationale is in the [course blueprint](../course-blueprint.md); the projects are in the [project catalog](../projects/index.md).

## How to read an entry

| Field | Meaning |
|---|---|
| Stage | The progression stage the module belongs to |
| Effort | Total learner hours, including the lab |
| Prerequisite | What you should be able to do first |
| Lessons | Published lesson count |
| Lab | The lab that produces the module artifact |
| Outcomes | The learning outcomes the module primarily serves |

## At a glance

| Stage | Modules | Effort | Question it answers | Gate artifact |
|---|---|---:|---|---|
| [1. Foundations](#stage-1) | M00–M03 | 39 h | What are we protecting, from whom, and how do we describe it? | Threat model (LAB-02) |
| [2. Core attacks](#stage-2) | M04–M07 | 55 h | How are predictions, training data, behavior, and privacy attacked? | Evasion, integrity, and extraction dossiers |
| [3. Defenses and data integrity](#stage-3) | M08–M09 | 28 h | Does the defense survive an adaptive attack, and can we trust the data we train on? | Robustness audit and dataset validation |
| [4. Secure engineering and operations](#stage-4) | M10–M11 | 26 h | How do we build, ship, and operate ML systems securely? | Supply-chain record and hardened service |
| [5. Privacy and frontier systems](#stage-5) | M12–M15 | 54 h | What changes with federation, privacy guarantees, explanations, generative models, and agents? | Federated study, privacy release, subgroup audit, and red-team reports |
| [6. Applied projects and synthesis](#stage-6) | M16–M18 + Capstone | 74 h (34 guided + 40 capstone) | Can you run an end-to-end assessment, red-team a system under rules of engagement, and defend the result? | Project dossier (PRJ-01…PRJ-06 or RT-01) and capstone (CAP-A to CAP-F) |

---

<a id="stage-1"></a>

## Stage 1 — Foundations (M00–M03)

*What are we protecting, from whom, and how do we describe it?*

This stage builds the vocabulary and the evidence habit. You learn how an ML system is assembled, how security principles apply to it, and how to write a threat model that justifies every attack you will later run.

<a id="m00"></a>

### M00 — How to Use This Self-Study Course

| | |
|---|---|
| Stage | 1 — Foundations |
| Effort | 4 hours |
| Prerequisite | None |
| Lessons | 3 published |
| Lab | LAB-01 (shared with M01) |
| Outcomes | LO-01, LO-28, LO-29 |

**Why it matters.** Most learners begin with attack code and never learn to justify it, reproduce it, or keep themselves inside the law. This module sets the study system, the evidence standard, and the rules of engagement for everything that follows.

**What you will do.** Distinguish adversarial ML from application security and AI safety; set up a reproducible lab; learn notebook, Git, and artifact hygiene; write a personal study plan; and sign an authorized-use and ethics statement.

**What you keep.** An environment verification report, a 12-week study plan, and a completed ethics statement.

[Open Module 00](m00-orientation/index.md){ .md-button }

<a id="m01"></a>

### M01 — Python, NumPy, pandas, and scikit-learn Refresher

| | |
|---|---|
| Stage | 1 — Foundations |
| Effort | 12 hours |
| Prerequisite | Python basics, or the recovery path |
| Lessons | 5 published |
| Lab | LAB-01 |
| Outcomes | LO-01, LO-28 |

**Why it matters.** Most "security bugs" in ML code are ordinary data bugs in disguise: a scaler fitted before the split, a silent dtype cast, a join that duplicates rows. If the baseline is untrustworthy, every attack and defense measured against it is meaningless.

**What you will do.** Write small testable functions and validate inputs; use NumPy arrays with deliberate shapes and dtypes; clean tabular data while preserving an audit trail; build a scikit-learn `Pipeline` that keeps preprocessing inside cross-validation; and make a run reproducible from seeds, pinned versions, saved splits, and a manifest.

**What you keep.** A tested validation function, a leak-free baseline pipeline, an audit trail, and a rerun proof.

[Open Module 01](m01-python-refresher/index.md){ .md-button }

<a id="m02"></a>

### M02 — Machine Learning Fundamentals and Evaluation

| | |
|---|---|
| Stage | 1 — Foundations |
| Effort | 12 hours |
| Prerequisite | M01 or equivalent |
| Lessons | 4 published |
| Lab | LAB-01B |
| Outcomes | LO-01, LO-28 |

**Why it matters.** Every security claim about a model is a claim about measurement. A 90%-accurate churn model on an 11%-positive dataset can beat the majority-class baseline while catching one in eight real positives. If you cannot state the unit of prediction, the metric, and the evaluation protocol, an attack result means nothing.

**What you will do.** Frame a supervised problem; compute a gradient step by hand and in NumPy; evaluate with a confusion matrix, precision, recall, F1, ROC-AUC, PR-AUC, calibration, and cross-validation; diagnose pipeline, target, duplicate/group, and temporal leakage; and report results with slices, confidence intervals, and a reproduction command.

**What you keep.** A metric table with a stated baseline and threshold, a written gradient step, and a complete evaluation audit of a leaky baseline.

[Open Module 02](m02-ml-fundamentals/index.md){ .md-button }

<a id="m03"></a>

### M03 — Cybersecurity Fundamentals and ML Threat Modeling

| | |
|---|---|
| Stage | 1 — Foundations |
| Effort | 11 hours |
| Prerequisite | M00–M02 |
| Lessons | 5 published |
| Lab | LAB-02 |
| Outcomes | LO-02, LO-03, LO-04, LO-30 |

**Why it matters.** Technique-first thinking produces demos. A threat model decides which technique is relevant, what access it assumes, and what evidence would prove it happened. This is the module that keeps the rest of the course honest.

**What you will do.** Classify assets, trust boundaries, attack surfaces, and controls; describe adversaries by goal, knowledge, capability, assumptions, and impact using NIST AI 100-2e2025; draw a data-flow diagram; map threats to MITRE ATLAS, the NIST AI RMF, and OWASP lists; build attack trees; score likelihood and impact; and write detection hypotheses and one reasoned rejection.

**What you keep.** A prioritized threat model with a risk register, testable controls, and one detection hypothesis per top threat.

[Open Module 03](m03-threat-modeling/index.md){ .md-button }

---

<a id="stage-2"></a>

## Stage 2 — Core Attacks (M04–M07)

*How are predictions, training data, behavior, and privacy attacked?*

This stage is the technical center of the course. You begin with crafted inputs, then move into the training process, the model artifact, and finally the prediction interface and the privacy of the people represented in the data.

<a id="m04"></a>

### M04 — Adversarial Examples and Evasion Attacks

| | |
|---|---|
| Stage | 2 — Core attacks |
| Effort | 14 hours |
| Prerequisite | M01; M03 recommended |
| Lessons | 5 published |
| Labs | LAB-03, LAB-04 |
| Outcomes | LO-05, LO-06, LO-07, LO-28 |

**Why it matters.** Gradient-based attacks define the vocabulary of perturbation budgets and success metrics. Understanding them at the level of a loop you can debug is the prerequisite for evaluating every defense.

**What you will do.** Derive FGSM; implement PGD with projection and restarts; run targeted and untargeted attacks; measure accuracy as a function of ε; separate source-model success from transfer success; and apply sanity checks such as zero perturbation, valid input ranges, and an explicit base set.

**What you keep.** An ε-sweep report and a targeted/transfer report, each with a written threat-model justification.

[Open Module 04](m04-evasion/index.md){ .md-button }

<a id="m05"></a>

### M05 — Training Data Poisoning and Label Manipulation

| | |
|---|---|
| Stage | 2 — Core attacks |
| Effort | 13 hours |
| Prerequisite | M02; M03 recommended |
| Lessons | 4 published |
| Labs | LAB-05, LAB-06 |
| Outcomes | LO-08, LO-09, LO-28 |

**Why it matters.** Every supervised model is an argument built from examples. Poisoning attacks the argument at its source. Its effects are quiet: a small label-flip rate can cost almost nothing in test accuracy, and a targeted attack can flip one decision while the global dashboard stays green.

**What you will do.** State a data-access threat model; measure a label-flip poisoning curve at controlled rates with an explicit denominator; build a targeted poisoning attack that changes one prediction; and evaluate a reference-set screen by its catches, false positives, threshold, and trust assumption.

**What you keep.** A poisoning curve and a targeted-poisoning defense report that reports attack and clean-data effects separately.

[Open Module 05](m05-poisoning/index.md){ .md-button }

<a id="m06"></a>

### M06 — Backdoor Attacks, Trojan Models, and Trigger-Based Behavior

| | |
|---|---|
| Stage | 2 — Core attacks |
| Effort | 14 hours |
| Prerequisite | M05; M03 recommended |
| Lessons | 4 published |
| Labs | LAB-07, LAB-08 |
| Outcomes | LO-10, LO-11, LO-28 |

**Why it matters.** A backdoor is a conditional failure: normal on ordinary inputs, wrong when a trigger appears. Clean accuracy can stay almost unchanged, so a model can pass every clean test and still carry behavior its publisher never intended.

**What you will do.** Define a trigger and target behavior; implant a backdoor at a fixed poison budget in tabular data; measure clean accuracy, attack success rate, and false-trigger behavior separately; scan an image model for a candidate trigger; and evaluate filtering and mitigation with false positives and an adaptive-attacker caveat.

**What you keep.** A backdoor red-team and defense dossier that includes a clean-model baseline and mitigation results.

[Open Module 06](m06-backdoors/index.md){ .md-button }

<a id="m07"></a>

### M07 — Model Extraction, Membership Inference, and Model Inversion

| | |
|---|---|
| Stage | 2 — Core attacks |
| Effort | 14 hours |
| Prerequisite | M06; M03 recommended |
| Lessons | 5 published |
| Labs | LAB-09, LAB-10 |
| Outcomes | LO-12, LO-13, LO-14, LO-15, LO-28 |

**Why it matters.** Every deployed model answers questions, and those answers reveal information about the model and the data it learned from. Extraction copies function, membership inference tests a record, and inversion reconstructs a representative input. They share an interface, not a metric.

**What you will do.** Build a local prediction API with a hard query budget; extract a surrogate with random and active queries; measure fidelity and task accuracy at several budgets; train a membership-inference attack and report TPR at low false-positive rates; explain inversion and attribute inference; and write a decision-ready privacy memo that states the base rate and the limits.

**What you keep.** An extraction curve and a privacy risk memo, including an explicit argument for why confidence is not proof of membership.

[Open Module 07](m07-extraction-privacy/index.md){ .md-button }

---

<a id="stage-3"></a>

## Stage 3 — Defenses and Data Integrity (M08–M09)

*Does the defense survive an adaptive attack, and can we trust the data we train on?*

A defense that has not faced an adaptive attacker is a hypothesis. This stage teaches you to test robustness claims, report the cost of a defense, validate training data, detect leakage, and govern the pipeline that produces a model.

<a id="m08"></a>

### M08 — Robustness Evaluation and Adversarial Defense

| | |
|---|---|
| Stage | 3 — Defenses and data integrity |
| Effort | 16 hours |
| Prerequisite | M04; M05 and M06 recommended |
| Lessons | 6 published |
| Lab | LAB-11 |
| Outcomes | LO-16, LO-17, LO-18, LO-28 |

**Why it matters.** "The model is robust" is not a testable statement. Robustness is a property of a model, an adversary, a norm, a budget, and a base set. Change one and the number changes. Adversarial training buys robustness by spending clean accuracy, and preprocessing defenses can look excellent at one budget and collapse at another.

**What you will do.** Write a five-part robustness claim; implement PGD adversarial training; evaluate input squeezing against a static and an adaptive attack; measure clean and robust accuracy at ε = 0.10 and a stress budget of ε = 0.20; recognize gradient masking; reproduce a comparison with fixed seeds; and report a scoped claim with residual risk.

**What you keep.** A three-model comparison table, an adaptive-attack log, and a robustness report that states what the evidence does not cover.

<a id="m09"></a>

### M09 — Data Integrity, Dataset Governance, and Secure Training Pipelines

| | |
|---|---|
| Stage | 3 — Defenses and data integrity |
| Effort | 12 hours |
| Prerequisite | M01, M02; M05 recommended |
| Lessons | 5 published |
| Lab | LAB-12 |
| Outcomes | LO-20, LO-30, LO-28 |

**Why it matters.** A model is only as trustworthy as the data and pipeline behind it. Missing values, duplicate records, contradictory labels, and post-outcome columns can inflate a metric or hide a defect. Leakage is not a modeling error; it is an evaluation integrity failure.

**What you will do.** Register source and lineage for a dataset; build validation rules for schema, missing values, duplicates, label conflicts, and implausible labels; repair in a documented order; audit a naive split against a grouped split; measure a leakage ablation; capture a reproducible run record; and write a governance memo with access, retention, and audit evidence.

**What you keep.** A validation report with defect counts, repaired data, a leakage ablation table, and a governance memo.

---

<a id="stage-4"></a>

## Stage 4 — Secure Engineering and Operations (M10–M11)

*How do we build, ship, and operate ML systems securely?*

Attacks are only half the job. This stage treats models as supply-chain artifacts and serving infrastructure as an attack surface. The controls are layered, and the evidence includes what the controls do not cover.

<a id="m10"></a>

### M10 — Model Serialization, Dependencies, and ML Supply-Chain Security

| | |
|---|---|
| Stage | 4 — Secure engineering and operations |
| Effort | 10 hours |
| Prerequisite | M01, M03 |
| Lessons | 4 published |
| Lab | LAB-13 |
| Outcomes | LO-21, LO-30 |

**Why it matters.** A model artifact may contain weights, a class definition, or an instruction to import and call something. If the loader can execute what the file describes, downloading a model is closer to running a stranger's program than opening a CSV. Dependencies and build steps carry the same risk.

**What you will do.** Map an ML supply chain and its trust boundaries; inspect a pickle statically with `pickletools.genops`; replace unsafe loading with a safe format; pin and hash dependencies; sign a manifest; generate an SBOM; build a fail-closed promotion gate; and prove it rejects a tampered artifact.

**What you keep.** A six-finding audit, a hardened project, a verified signature and SBOM, and a gate that passes the hardened copy and fails the vulnerable one.

<a id="m11"></a>

### M11 — Secure Model Serving, API Security, Monitoring, and Incident Response

| | |
|---|---|
| Stage | 4 — Secure engineering and operations |
| Effort | 16 hours |
| Prerequisite | M02, M03, M10 |
| Lessons | 6 published |
| Labs | LAB-14, LAB-15 |
| Outcomes | LO-22, LO-23, LO-04, LO-30 |

**Why it matters.** A model behind an API has users, network exposure, resource limits, logs, and an incident surface. Authentication does not bound work; rate limiting does not validate content; validation does not make the model robust; and monitoring does not stop a request. Each layer answers a different question.

**What you will do.** Build a loopback prediction API with bearer authentication, scopes, body and batch caps, feature validation, rate limiting, safe errors, and redacted logs; test 18 security cases; calibrate five detectors on quiet traffic; triage drift, evasion, and abuse episodes; test a rollback rather than assuming it works; measure a mitigation's utility cost; and write an incident playbook with evidence and recovery criteria.

**What you keep.** A hardened service with a passing 18-case suite and security report, plus a monitoring and incident-response package with thresholds, episodes, rollback evidence, and a manifest.

---

<a id="stage-5"></a>

## Stage 5 — Privacy and Frontier Systems (M12–M15)

*What changes with privacy guarantees, federation, generative models, and agents?*

The next-to-last stage extends the same discipline to systems where the trust boundary moves: data subjects with privacy rights, clients you do not control, context that arrives at inference time, and agents that can take actions.

<a id="m12"></a>

### M12 — Federated Learning Security and Distributed ML Threats

| | |
|---|---|
| Stage | 5 — Privacy and frontier systems |
| Effort | 14 hours |
| Prerequisite | M05, M07 |
| Lessons | 5 |
| Lab | LAB-16 |
| Outcomes | LO-24; supports LO-19, LO-28 |

**Why it matters.** Federation changes the topology, not the adversary. A malicious client can scale a poisoning update, persist a backdoor, or multiply itself through Sybil identities, and the coordinator's aggregation rule may average the damage rather than remove it.

**What you will do.** Diagram a training round and its trust assumptions; build a controlled malicious local update; compare the mean, coordinate-wise trimmed mean, coordinate median, and Krum by assumption and breakdown point; add norm clipping, update inspection, monitoring, and secure aggregation; and evaluate each mitigation at equal rounds with clean accuracy and attack success.

**What you keep.** A federated attack and defense report with equal-round comparisons and a residual-risk statement covering Sybil clients, free-riding, coordinator trust, and what secure aggregation does not protect.

<a id="m13"></a>

### M13 — Privacy-Preserving Machine Learning

| | |
|---|---|
| Stage | 5 — Privacy and frontier systems |
| Effort | 12 hours |
| Prerequisite | M07 (M12 recommended) |
| Lessons | 5 |
| Lab | LAB-17 |
| Outcomes | LO-19; supports LO-28 |

**Why it matters.** Privacy claims need formal guarantees, not assurances. Differential privacy gives a measurable budget, but only if you report ε, δ, composition, sensitivity, and the assumptions behind the accounting honestly. A number without those inputs cannot be compared or audited.

**What you will do.** Analyze membership, reconstruction, linkage, and attribute-inference risk; derive ε-DP, sensitivity, and the Laplace and Gaussian mechanisms; compute noise scale and compose budgets; compare central, local, and distributed DP, DP-SGD, secure aggregation, and secure computation; and evaluate a noisy release with utility metrics and an empirical membership test.

**What you keep.** A privacy–utility experiment with an accounting trail and an explicit statement of what the empirical measurement does and does not establish.

<a id="m14"></a>

### M14 — Explainability, Fairness, and Security Trade-offs

| | |
|---|---|
| Stage | 5 — Privacy and frontier systems |
| Effort | 10 hours |
| Prerequisite | M02, M07, M08 |
| Lessons | 4 |
| Lab | LAB-18 |
| Outcomes | LO-31, LO-32; supports LO-28 |

**Why it matters.** An explanation is an output: it can be unfaithful, leak more than intended, or be steered by an attacker while the prediction stays fixed. Fairness has the same structure — a subgroup metric is a measurement under uncertainty, not a verdict, and two reasonable definitions can conflict.

**What you will do.** Compare coefficient, gradient×input, occlusion, surrogate, and Shapley-style explanations by assumption and cost; test fidelity with deletion and model randomization; measure stability under bounded input change; identify leakage and manipulation paths; and compute demographic parity, equalized odds, and calibration gaps with subgroup sizes and intervals.

**What you keep.** A subgroup audit and explanation-stability report that separates stability from faithfulness and states the trade-offs it measured.

<a id="m15"></a>

### M15 — Generative AI, LLM, RAG, and AI Agent Security

| | |
|---|---|
| Stage | 5 — Privacy and frontier systems |
| Effort | 18 hours |
| Prerequisite | M03, M07, M11 |
| Lessons | 6 |
| Labs | LAB-19, LAB-20 |
| Outcomes | LO-25, LO-26, LO-27; supports LO-28 |

**Why it matters.** In an LLM application, the prompt, retrieved context, tool descriptions, and output are all inputs. Nothing enforces the boundary between instruction and data, so a retrieved document can carry an instruction, an output can become executable content elsewhere, and an agent's tool can convert a text-level bug into a real action.

**What you will do.** Distinguish predictive-ML from LLM application security; test direct and indirect prompt injection against a local mock application; build a RAG corpus with labeled trusted and untrusted documents and a canary; add instruction hierarchy, trust labels, retrieval boundaries, and output validation; then build a mock agent with harmless tools and enforce capability scoping, recipient and host allowlists, approval gates, untrusted-output handling, and a hash-chained action log.

**What you keep.** A RAG trust-boundary evaluation and an agent containment report, each with a defense comparison, residual success, false positives on benign tasks, and a mapping to OWASP LLM 2026, OWASP Agentic AI, MITRE ATLAS, and NIST AI 100-2e2025.

---

<a id="stage-6"></a>

## Stage 6 — Applied Projects and Synthesis (M16–M18 + Capstone)

*Can you run an end-to-end assessment, red-team a system under rules of engagement, and defend the result?*

The last stage removes the scaffolding. Each module hands you a system, a budget, and an evidence standard, then asks you to produce the kind of dossier an engineering owner can act on. The work is local and synthetic, but the reasoning is the reasoning used in production assessments.

<a id="m16"></a>

### M16 — End-to-End ML Security Assessment

| | |
|---|---|
| Stage | 6 — Applied projects and synthesis |
| Effort | 16 hours (4 lessons + 11-hour project + 1-hour quiz/exercises) |
| Prerequisite | M03; M08–M11 recommended |
| Lessons | 4 published |
| Project | One of PRJ-01…PRJ-06 |
| Outcomes | LO-33; supports LO-28, LO-30 |

**Why it matters.** A collection of successful attacks is not an assessment. An assessment starts from a business decision, names what is in scope, traces every test to a risk, establishes a baseline, measures within a budget, and ends with a costed remediation and a residual risk the owner accepts.

**What you will do.** Scope a system and classify its assets; turn a threat model into falsifiable tests; establish baselines and negative controls; run bounded attack and defense experiments; and write findings with severity, owners, costs, retests, and limitations. Then apply the method to one of six project scenarios, from fraud scoring to a RAG assistant.

**What you keep.** A complete project dossier: architecture and data classification, risk register, test matrix, baseline table, experiment evidence, defended system, report, briefing, and reproduction package.

[Open Module 16](m16-end-to-end-assessment/index.md){ .md-button }

<a id="m17"></a>

### M17 — ML Red-Team and Blue-Team Simulation

| | |
|---|---|
| Stage | 6 — Applied projects and synthesis |
| Effort | 14 hours (4 lessons + 9-hour exercise + 1-hour quiz/exercises) |
| Prerequisite | M03, M11; M15 recommended |
| Lessons | 4 published |
| Project | RT-01 |
| Outcomes | LO-34; supports LO-23, LO-28, LO-29 |

**Why it matters.** An attack that leaves no usable evidence is a stunt. A detection that has never seen a real attack is a guess. Red/blue work is the discipline that connects an action to a log, a log to a decision, and a mitigation to a measured cost on both attacker and defender.

**What you will do.** Write rules of engagement with scope, non-goals, budgets, roles, communications, and stop conditions; plan attacks as falsifiable hypotheses; execute A-01…A-07 against a local service; build and calibrate detections D-01…D-07 on a quiet baseline; reconstruct a UTC timeline; test mitigations against an adaptive variant; and report before/after results with residual risk.

**What you keep.** A red-team plan and evidence log, a blue-team detection and response package, a purple-team synthesis, and an adaptive-retest report.

[Open Module 17](m17-red-team-blue-team/index.md){ .md-button }

<a id="m18"></a>

### M18 — Capstone Projects and Research Extensions

| | |
|---|---|
| Stage | 6 — Applied projects and synthesis |
| Effort | 4 lesson hours + 40-hour capstone |
| Prerequisite | M16 or M17 recommended |
| Lessons | 4 published |
| Project | CAP-A to CAP-F |
| Outcomes | LO-33, LO-35; supports LO-28, LO-29, LO-30 |

**Why it matters.** The difference between a course project and a research contribution is not ambition; it is whether the question is bounded, the gap is stated, the comparison is controlled, and the claim matches the evidence. This module makes that difference explicit before you start the capstone.

**What you will do.** Turn a broad interest into a one-system, one-decision scope; set milestone gates and a reproducibility contract; choose tables and figures that answer a claim; write limitations that a reviewer would accept; and convert the work into a research question with a gap statement, claim–evidence table, and pre-registration-style plan.

**What you keep.** A scoped capstone proposal, a milestone and reproducibility plan, a results and limitations draft, and a research-question canvas.

[Open Module 18](m18-capstone-and-research/index.md){ .md-button }

<a id="cap"></a>

### Capstone

| | |
|---|---|
| Stage | 6 — Applied projects and synthesis |
| Effort | 40 hours |
| Prerequisite | M00–M18, or a track equivalent plus M16 |
| Lessons | 1 brief plus six option briefs |
| Project | CAP-A to CAP-F |
| Outcomes | LO-33, LO-35; LO-28, LO-29, LO-30 |

**Why it matters.** A capstone is where the loop becomes a habit: scope a system, model the adversary, measure an effect, engineer a control, re-test under adaptation, and communicate the result without overclaiming.

**What you will do.** Choose one of six options, from an end-to-end risk assessment to a federated robustness study. Write a proposal and an authorized-use statement; pass milestones M0–M5; build and evaluate; attempt an adaptive attack on your own mitigation; and produce a reproduction package, report, and briefing.

**What you keep.** A complete, auditable assessment that names its limitations and can be reproduced by another learner.

[Open the capstone brief](../projects/capstone.md){ .md-button }

---

<a id="entry-paths"></a>

## Entry paths

The same routes in more detail, with effort, duration, and first artifacts, are on [Learning paths](../learning-paths.md). The [progress checklist](../assessments/progress-checklist.md) turns each route into dated evidence.

| Learner | Start at | Skim | First artifact |
|---|---|---|---|
| Beginner with some Python | M00 → M01 → M02 → M03 | Nothing; the sequence is the course | LAB-01, LAB-01B, LAB-02 |
| ML practitioner new to security | M00, then M03 | M01 and M02 (review only) | LAB-02, LAB-03 |
| Security practitioner new to ML | M00 → M01 → M02, then M03 | M01 §§4–5 if comfortable with Python | LAB-01, LAB-01B, LAB-02 |
| GenAI engineer | M00–M03, M07, M11, then M15 | M04–M06, M08–M10, and M12–M14 optional | LAB-19 and LAB-20, then PRJ-05 |
| Privacy or federated specialist | M02, M07, then M12–M13 | M14–M15 optional | LAB-16 and LAB-17 |
| Learner ready for assessment work | M03, then M16; add M17 for red/blue | Skim M08–M11 for control vocabulary | PRJ-01…PRJ-06 or RT-01, then the capstone |

The capstone assumes the vocabulary of Stages 1–4 even for specialist entry paths. If you skip a prerequisite, read its threat-model sections before starting the lab or project.

## Publication status and planned work

Levels 1–5 are complete: lessons, labs, quizzes, exercises, answer files, project briefs, the red/blue exercise, and the capstone brief with its rubric. There are no empty placeholder modules. The maintainer-facing evaluator reference is published but excluded from student navigation.

The remaining work is maintenance rather than content: deploy the site when the owner approves, re-check external links and framework versions, and add learner work or worked examples only if they can be published without weakening the projects. The build order and quality gates are in the [implementation roadmap](../implementation-roadmap.md).
