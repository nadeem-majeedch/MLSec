# Machine Learning Security (ML-Sec) — Master Course Blueprint

| Field | Value |
|---|---|
| Document | Master course design |
| Version | 0.6 (Level 5 implemented) |
| Date | 2026-10-28 |
| Status | **Levels 1–5 implemented** (M00–M18, LAB-01…LAB-20, PRJ-01…PRJ-06, RT-01, capstone brief) |
| Repository | `nadeem-majeedch/MLSec` |
| Intended site | `https://nadeem-majeedch.github.io/MLSec/` (planned; not yet published) |
| Instructor | Engr. Dr. Muhammad Nadeem Majeed, Professor, Department of Data Science (PUCIT), University of the Punjab, Lahore |
| Audience | Independent learners, beginner → advanced |
| Related documents | [Module map](module-map.md) · [Lab catalog](lab-catalog.md) · [Project catalog](project-catalog.md) · [Learning outcomes](learning-outcomes.md) · [Implementation roadmap](implementation-roadmap.md) |

> **Status note.** This document is the design contract. Module, lab, project, and assessment identifiers used here are the canonical IDs that all lesson material must follow. Levels 1–5 are built and verified: M00–M18, LAB-01…LAB-20, six applied project briefs, RT-01, and the capstone brief with milestones and rubric. Where the implementation changed a title, scope, or hour estimate, the change is recorded in the changelog and in the module map.

---

## 1. Course identity

**Machine Learning Security (ML-Sec)** is a self-study, lab-driven course about how machine-learning systems fail under adversarial pressure, how to measure that failure honestly, and how to engineer systems that resist it. It covers classical adversarial ML (evasion, poisoning, backdoors, extraction, inference and inversion), privacy engineering, ML supply-chain and deployment security, monitoring and incident response, federated learning, and the security of generative and agentic AI systems.

The course is written for people studying without a lecturer in the room. Every module therefore includes: a why-it-matters scenario, explicit objectives, self-contained explanations, a runnable lab with a reproducible artifact, a self-graded knowledge check, and a short reflective task. Assessment is portfolio-based and self-assessed against published rubrics.

### 1.1 Instructor profile

**Engr. Dr. Muhammad Nadeem Majeed** is a Professor in the Department of Data Science (PUCIT), University of the Punjab, Lahore. He is the author and instructor of record for ML-Sec.

Only the details supplied for this project appear here. A full biography page (`docs/about/instructor.md`) will be added when the instructor provides a short bio, research interests, teaching philosophy, public contact policy, and an optional photograph. No credentials, publications, awards, or contact details are invented in this blueprint.

### 1.2 Course at a glance

| | |
|---|---|
| Level | Beginner to advanced, with three entry tracks |
| Format | Reading + guided notebooks + self-graded quizzes + projects |
| Total effort (full program) | ≈ 276 hours (236 guided + 40 capstone) |
| Typical duration | 7–11 months at 6–10 h/week |
| Delivery | Static site (MkDocs Material) + runnable lab repository |
| Language | English; identifiers are ASCII (`M04`, `LAB-07`, `LO-12`); mathematical symbols appear only in prose |
| Hardware | CPU-first (8 GB RAM); GPU/Colab optional for selected labs |
| Prerequisites | Python, basic ML, basic command line (details in §5) |
| Assessment | Knowledge checks 10%, labs and applied projects 40%, mini-projects 20%, capstone 30% |
| Licensing | **TBD by owner** — content and code licenses must be chosen before publication |

---

## 2. The problem this course solves

Most ML curricula teach models to be accurate. Most security curricula teach networks and applications to be resilient. Neither, on its own, prepares a practitioner for systems where the *data distribution is an attack surface*, the *model is an artifact that can be stolen or trojaned*, and the *API is both the product and the oracle*.

ML-Sec closes that gap with a single discipline: **model the adversary, measure the effect, engineer the control, and re-test**. Learners do not merely read that FGSM exists; they implement it, break a baseline, evaluate a defense, discover why the defense fails under an adaptive attack, and write a defensible report.

The course is deliberately **framework-anchored but implementation-first**. NIST AI 100-2e2025 supplies the vocabulary, MITRE ATLAS supplies adversary tactics and techniques, the NIST AI Risk Management Framework supplies governance structure, and OWASP supplies application-facing risk lists. None of these substitutes for running code and measuring outcomes.

---

## 3. Design principles

1. **Threat model before technique.** Every attack is introduced with attacker goal, knowledge, capability, access, and success metric. A technique without a threat model is a demo, not security work.
2. **Reproduce → break → defend → re-break.** Learners first reproduce a known result, then attack a system, then apply a defense, then attempt an adaptive attack that defeats or qualifies the defense.
3. **Measure, don't assert.** Claims require numbers with budgets, seeds, and uncertainty: attack success rate at a stated perturbation budget, fidelity at a stated query budget, TPR at a stated FPR. "Robust" is not an adjective; it is a curve.
4. **Assume an adaptive adversary.** Static defenses are treated as hypotheses. Obfuscated gradients and broken evaluations are a recurring theme, not a footnote.
5. **CPU-first reproducibility.** Core labs run on a laptop; GPU is an optimization, not a requirement. Every lab pins versions and seeds.
6. **Safety by construction.** Offensive work is confined to local, synthetic, or public sandbox targets. No lab instructs or permits attacks on third-party systems.
7. **Constructive alignment.** Each outcome maps to a quiz item set, a lab artifact, and (for terminal outcomes) a project or capstone.
8. **Portfolio over proctored exams.** In self-study there is no credible invigilation; the defensible signal is a reproducible artifact plus a written analysis that another person can audit.

---

## 4. Learning outcomes (summary)

The full, measurable outcome set is in [learning-outcomes.md](learning-outcomes.md). Program-level outcomes:

- **PLO-1 Foundations** — Explain ML system architecture, lifecycle, trust boundaries, and adversarial threat models using recognized frameworks.
- **PLO-2 Attack analysis** — Implement and evaluate evasion, poisoning, backdoor, extraction, inference, and inversion attacks under explicit budgets.
- **PLO-3 Robustness engineering** — Select, implement, and critically evaluate defenses under adaptive attack, distinguishing empirical robustness from certified guarantees.
- **PLO-4 Secure engineering** — Harden data pipelines, model artifacts, serving infrastructure, and monitoring/response for ML systems.
- **PLO-5 Frontier systems** — Assess and mitigate risks in federated, generative, and agentic AI systems.
- **PLO-6 Professional practice** — Communicate findings with reproducible evidence, correct severity, lawful conduct, and responsible disclosure.
- **PLO-7 Integrated assessment** — Plan, execute, and defend an authorized end-to-end assessment, including red-team/blue-team simulation, costed remediation, and residual risk.

---

## 5. Prerequisites and entry paths

### 5.1 Required baseline

| Area | Minimum | Diagnostic (self-check) |
|---|---|---|
| Python | Functions, classes, virtual environments, NumPy arrays | Load a CSV, train a scikit-learn classifier, plot a confusion matrix without copying a full tutorial |
| ML | Train/test splits, loss, overfitting, precision/recall, ROC-AUC | Explain why 99% accuracy can be useless on imbalanced data |
| Math | Gradients, chain rule, basic probability, norms | Compute the gradient of cross-entropy for a linear layer; explain an L∞ ball |
| Tooling | Terminal, Git basics, Jupyter | Clone a repo, create a venv, run a notebook end-to-end |
| Security | CIA triad, authentication vs authorization | Explain the difference between a vulnerability and an exploit |

### 5.2 Entry paths

| Learner | Start at | Skip / skim | First meaningful artifact |
|---|---|---|---|
| Beginner (some Python, little ML) | M00, then M01 | M02 §§1–3 if security-literate | LAB-01 baseline + LAB-02 threat model |
| ML practitioner, new to security | M00, M02, M03 | M01 (review only) | LAB-02 + LAB-03 |
| Security practitioner, new to ML | M00, M01 | M02 (review only) | LAB-01 + LAB-02 |
| GenAI engineer targeting LLM/agent risk | M00–M03, M07, M11, then M15 | M04–M06, M08–M10, and M12–M14 optional | LAB-19 + LAB-20, then PRJ-05 |
| Learner ready for assessment work | M03, then M16; add M17 for red/blue | M08–M11 for control vocabulary | One of PRJ-01…PRJ-06 or RT-01 |

A 20-item diagnostic and its answer key are published at [DIA-01](assessments/diagnostic/index.md), with the key in the repository at `assessments/answer-keys/diagnostic-key.md`. Learners who score below 14/20 should complete the M01 refresher and the Python/NumPy warm-up exercises before M04.

---

## 6. Progression model

| Stage | Modules | Question answered | Gate artifact |
|---|---|---|---|
| 1. Foundations | M00–M03 | What are we protecting, from whom, and how do we describe it? | Threat model (LAB-02) |
| 2. Core attacks | M04–M07 | How do inputs, training data, and prediction APIs fail under attack? | Evasion report (LAB-04), poisoning dossier (LAB-06), backdoor dossier (LAB-08), privacy memo (LAB-10) |
| 3. Defenses and data integrity | M08–M09 | Does the defense survive an adaptive attack, and can we trust the data we train on? | Robustness audit (LAB-11 + MP-02), dataset validation and governance memo (LAB-12) |
| 4. Secure engineering and operations | M10–M11 | How do we build, ship, and operate ML systems securely? | Supply-chain record (LAB-13), hardened service and IR playbook (LAB-14/15) |
| 5. Distributed, private, and frontier systems | M12–M15 | What changes with federation, privacy guarantees, explanation and fairness, generative models, and agents? | FL attack/defense report (LAB-16), DP accounting (LAB-17), explanation audit (LAB-18), red-team report (LAB-19/20 + MP-04) |
| 6. Applied projects and synthesis | M16–M18 + CAP | Can you run an assessment, red-team under rules of engagement, and defend the result? | Project dossier (PRJ-01…PRJ-06 or RT-01) and capstone (CAP-A…CAP-F) |

Stages are sequential for beginners. Experienced learners may enter at Stage 2 or Stage 5, but the capstone assumes Stage 1–4 vocabulary and one completed project.

---

## 7. Tracks and workload

Module effort below is **total learner effort** (reading, exercises, quiz, and lab), not lecture hours.

| Track | Modules | Effort | Suggested pace |
|---|---|---|---|
| Foundations | M00–M03 | ≈ 39 h | 6 h/week → 7 weeks |
| Core attacks | M00–M07 | ≈ 94 h | 8 h/week → 12 weeks |
| Practitioner | M00–M11 | ≈ 148 h | 8 h/week → 19 weeks |
| Applied assessment specialization | M00–M03, M16–M18 + one project + CAP | ≈ 113 h | 8 h/week → 15 weeks |
| Full program + capstone | M00–M18 + CAP | ≈ 276 h | 10 h/week → 28 weeks |
| GenAI/Agent specialization | M00–M03, M15 + CAP | ≈ 97 h | 8 h/week → 12 weeks |

Mini-projects (MP-01…MP-04, 8 h each) are optional stretch work for the Foundations/Practitioner tracks and recommended for the Full track. They are not double-counted in the module totals. The six applied projects are 11 h each and the red/blue exercise is 9 h; those hours are inside M16 and M17.

### 7.1 Module budget

| Module | Title | Hours | Difficulty (1–5) | Prerequisites |
|---|---|---:|---:|---|
| M00 | How to Use This Self-Study Course | 4 | 1 | None |
| M01 | Python, NumPy, pandas, and scikit-learn Refresher | 12 | 2 | Python basics |
| M02 | Machine Learning Fundamentals and Evaluation | 12 | 3 | M01 or equivalent |
| M03 | Cybersecurity Fundamentals and ML Threat Modeling | 11 | 3 | M00–M02 |
| M04 | Adversarial Examples and Evasion Attacks | 14 | 4 | M02, M03 recommended |
| M05 | Training Data Poisoning and Label Manipulation | 13 | 3 | M02, M03 recommended |
| M06 | Backdoor Attacks, Trojan Models, and Trigger-Based Behavior | 14 | 4 | M05 |
| M07 | Model Extraction, Membership Inference, and Model Inversion | 14 | 4 | M02, M03 |
| M08 | Robustness Evaluation and Adversarial Defense | 16 | 5 | M04, M05, M06 |
| M09 | Data Integrity, Dataset Governance, and Secure Training Pipelines | 12 | 3 | M01, M02; M05 recommended |
| M10 | Model Serialization, Dependencies, and ML Supply-Chain Security | 10 | 3 | M01, M03 |
| M11 | Secure Model Serving, API Security, Monitoring, and Incident Response | 16 | 4 | M02, M03, M10 |
| M12 | Federated Learning Security and Distributed ML Threats | 14 | 5 | M05, M07 |
| M13 | Privacy-Preserving Machine Learning | 12 | 5 | M07; M12 recommended |
| M14 | Explainability, Fairness, and Security Trade-offs | 10 | 4 | M02, M07 |
| M15 | Generative AI, LLM, RAG, and AI Agent Security | 18 | 6 | M03, M07, M11 |
| M16 | End-to-End ML Security Assessment | 16 | 5 | M03; M08–M11 recommended |
| M17 | ML Red-Team and Blue-Team Simulation | 14 | 5 | M03, M11; M15 recommended |
| M18 | Capstone Projects and Research Extensions | 4 | 4 | M16 or M17 recommended |
| CAP | Capstone | 40 | 5 | M00–M18 (or track equivalent plus M16) |
| **Total** | | **276** | | |

---

## 8. Module catalog

Each module follows the standard lesson pattern defined in §19. "Deliverable" is the evidence a learner keeps in the portfolio.

### M00 — How to Use This Self-Study Course (4 h)
**Objectives.** Explain what ML security covers and how it differs from application security and AI safety; set up a reproducible lab environment; apply the course's safety, ethics, and legal rules; build a personal study plan.
**Subtopics.** Attacker/defender/auditor mindsets; the ML lifecycle as attack surface; course map and study loop; evidence portfolio; notebook and Git hygiene; authorized-use rules; responsible disclosure; how to use AI assistants without outsourcing understanding; self-assessment and spaced review.
**Lab.** LAB-01 (environment and baseline artifact, shared with M01). **Deliverable.** Environment verification report, ethics statement, and 12-week study plan. **Assessment.** QZ-00; LAB-01.

### M01 — Python, NumPy, pandas, and scikit-learn Refresher (12 h)
**Objectives.** Write small, testable Python with explicit input validation; use NumPy arrays with deliberate shapes and dtypes; clean tabular data without losing the audit trail; build a leak-free scikit-learn `Pipeline`; and make a run reproducible.
**Subtopics.** Types and silent coercion; mutable defaults; validation as a control; exceptions and script structure; array shape and axis discipline; dtype overflow; broadcasting; seeded randomness; pandas selection, missing data, duplicates, joins and row multiplication, index alignment; estimators, pipelines, cross-validation, metrics and thresholds; seeds, determinism, pinned versions, saved splits, manifests.
**Lab.** LAB-01. **Deliverable.** Reproducible baseline with metrics, audit trail, and artifact manifest. **Assessment.** QZ-01; LAB-01 checker.

### M02 — Machine Learning Fundamentals and Evaluation (12 h)
**Objectives.** Frame a supervised problem; explain and compute a gradient step; evaluate a classifier with metrics that survive imbalance; diagnose and repair leakage; report results with uncertainty and a reproduction command.
**Subtopics.** Unit of prediction, label definition and window, inference-time features; lifecycle stages; cross-entropy and gradient descent; learning rate, epochs, batch size; confusion matrix, precision/recall/F1, ROC-AUC vs PR-AUC, calibration, majority-class baseline; bootstrap intervals; group and temporal splits; pipeline, target, duplicate/group, and temporal leakage; slices and error analysis; trustworthy reporting.
**Lab.** LAB-01B. **Deliverable.** Evaluation audit comparing a leaky and a repaired baseline, with intervals and a report. **Assessment.** QZ-02; LAB-01B checker.

### M03 — Cybersecurity Fundamentals and ML Threat Modeling (11 h)
**Objectives.** Classify assets, trust boundaries, attack surfaces, and controls; describe adversaries with NIST AI 100-2e2025 terms; build a data-flow diagram; map threats to MITRE ATLAS, the NIST AI RMF, and OWASP; produce a prioritized, testable threat model.
**Subtopics.** Confidentiality, integrity, availability, privacy; least privilege; defense in depth; trust-boundary tests; attack surface across data, model, artifact, serving, and monitoring; adversary goals, knowledge, capability, and budget; impact dimensions; lifecycle stages; DFD rules; MITRE ATLAS techniques; NIST AI RMF functions; OWASP ML and LLM lists; ISO/IEC 42001 and 23894 concepts; risk scoring anchors; attack trees; preventive/detective/corrective controls; detection hypotheses; residual risk and reasoned rejection.
**Lab.** LAB-02. **Deliverable.** Threat model (YAML), 12-section report with DFD, ranked register, controls, and detection hypotheses. **Assessment.** QZ-03; LAB-02 checker and rubric.

### M04 — Adversarial Examples and Evasion Attacks (14 h)
**Objectives.** Implement FGSM, PGD, and a targeted gradient attack; execute a transfer attack against a black-box model; measure and report evasion with explicit budgets, base sets, and limitations.
**Subtopics.** Adversarial example and evasion definitions; Lp norms and budgets; five-part evasion claim; FGSM derivation and sign step; PGD iteration, projection, step size, and restarts; targeted vs untargeted; transfer and surrogate models; source vs target success; clipping and valid-domain checks; ASR vs robust accuracy; zero-budget tests; why a toy result does not generalize to a deployed system; physical and query constraints.
**Labs.** LAB-03, LAB-04. **Deliverable.** ε-sweep report and targeted/transfer report with threat-model justification. **Assessment.** QZ-04; LAB-03/04.

### M05 — Training Data Poisoning and Label Manipulation (13 h)
**Objectives.** Construct an indiscriminate label-flip attack at controlled rates; construct a targeted feature-space poisoning attack; evaluate a screening defense with catches, false positives, and an explicit trust assumption.
**Subtopics.** Poisoning threat models and data-control channels; poison-rate denominators; label flipping and fresh sampling per rate; the low-rate plateau; targeted placement and one-decision flips; why global accuracy hides local harm; reference-set screening with k-NN; threshold sensitivity; false-positive cost; robust training and provenance; limits of "just clean the data."
**Labs.** LAB-05, LAB-06. **Deliverable.** Poisoning curve and targeted-poisoning defense report. **Assessment.** QZ-05; LAB-05/06; MP-01.

### M06 — Backdoor Attacks, Trojan Models, and Trigger-Based Behavior (14 h)
**Objectives.** Construct a backdoor at a controlled poison rate; measure clean accuracy, ASR, and false-trigger rate separately; perform a trigger search; evaluate a mitigation with false positives and an adaptive-attacker caveat.
**Subtopics.** Trigger design (patch, blended, tabular); poison budget and target behavior; BadNets and conditional failure; stealth and false-trigger rate; tabular and image triggers; positional trigger search; anomaly scores and baselines; STRIP and input filtering; spectral signatures and activation clustering; fine-pruning and unlearning; adaptive attackers; reporting a defense dossier.
**Labs.** LAB-07, LAB-08. **Deliverable.** Backdoor red-team and defense dossier. **Assessment.** QZ-06; LAB-07/08; MP-01.

### M07 — Model Extraction, Membership Inference, and Model Inversion (14 h)
**Objectives.** Classify extraction, membership inference, and inversion by goal, access, and metric; measure extraction fidelity and accuracy across query budgets; compute membership TPR at low FPR; explain inversion and attribute inference; report privacy risk with base rates and limits.
**Subtopics.** Prediction APIs as oracles; hard labels, top-k, probabilities, logits, explanations; surrogate training; random vs active queries and cold start; fidelity vs task accuracy; shadow models, thresholds, and LiRA; TPR at FPR ≤ 1%; why confidence is not proof; optimization-based inversion and priors; representative vs recovered record; attribute inference; precision at realistic base rates; interface defenses (rounding, top-k, rate limits, monitoring, watermarking); DP overview; risk memos.
**Labs.** LAB-09, LAB-10. **Deliverable.** Extraction study and privacy risk memo. **Assessment.** QZ-07; LAB-09/10; MP-03.

### M08 — Robustness Evaluation and Adversarial Defense (16 h)
**Objectives.** State a robustness claim with its threat model; train an adversarially robust model and quantify the clean cost; evaluate input-processing and detection defenses against static and adaptive attacks; recognize invalid evaluations.
**Subtopics.** Clean vs robust accuracy and base sets; PGD adversarial training; overfitting to a fixed attack; input squeezing, quantization, feature transforms, and detectors; utility and false-positive costs; gradient masking, shattered gradients, and BPDA; adaptive attack design; AutoAttack, RobustBench, restarts, seeds, and confidence intervals; robustness reporting checklists; negative results and residual risk.
**Lab.** LAB-11. **Deliverable.** Robustness audit comparing an undefended model, an adversarially trained model, and a preprocessing defense, including a stress budget and an adaptive attack. **Assessment.** QZ-08; LAB-11; MP-02.

### M09 — Data Integrity, Dataset Governance, and Secure Training Pipelines (12 h)
**Objectives.** Establish provenance and lineage for training data; build validation and quarantine gates for schema, quality, and label defects; prevent split and target leakage; make training reproducible and auditable.
**Subtopics.** Source registration and collection context; lineage graphs and manifests; schema, range, missing-value, duplicate, and contradiction checks; label quality and quarantine; grouped and temporal splits; target and pipeline leakage; versioned datasets; seeds, configuration capture, and experiment tracking; access control, retention, licensing, and audit trails; AI RMF GOVERN and MAP.
**Lab.** LAB-12. **Deliverable.** Validation and quarantine pipeline with defect counts, controlled leakage ablation, and a governance memo. **Assessment.** QZ-09; LAB-12.

### M10 — Model Serialization, Dependencies, and ML Supply-Chain Security (10 h)
**Objectives.** Threat-model an ML artifact supply chain; explain unsafe deserialization and safe formats; scan dependencies and artifacts in CI; implement hashing, signing, provenance, SBOM, and a fail-closed promotion gate.
**Subtopics.** Pipeline stages and trust boundaries; dependency confusion and typosquatting; pickle opcode risk and static inspection; safetensors and ONNX caveats; pinning and hashes; vulnerability audit; scanner limits; Sigstore/cosign, in-toto, and SLSA concepts; CycloneDX ML-BOM and SPDX; registry promotion and third-party model review; license risk; residual risk of integrity versus publisher identity.
**Lab.** LAB-13. **Deliverable.** Audit findings, hardened artifact pipeline, verified hash and signature, SBOM, and a gate that fails on a negative test. **Assessment.** QZ-10; LAB-13.

### M11 — Secure Model Serving, API Security, Monitoring, and Incident Response (16 h)
**Objectives.** Threat-model a prediction API; implement authentication, authorization, request bounds, validation, and safe errors; design calibrated detections; write and exercise an incident-response playbook with rollback and evidence handling.
**Subtopics.** Serving architecture and trust boundaries; API keys, OIDC, mTLS, RBAC/ABAC, object-level authorization, tenancy; body and batch caps; type, shape, range, and finiteness checks; quotas and fixed-window rate limits; output handling and generic errors; redacted telemetry; drift versus attack; windowed detectors and threshold calibration; alert fatigue and false positives; signal-family triage; episodes and severity; containment, rollback verification, evidence preservation, postmortems; secrets, configuration, least privilege, and safe failure.
**Labs.** LAB-14, LAB-15. **Deliverable.** Hardened loopback service with an 18-case security suite, plus a detection and IR package with a tested rollback and measured mitigation. **Assessment.** QZ-11; LAB-14/15.

### M12 — Federated Learning Security and Distributed ML Threats (14 h)
**Objectives.** Threat-model a federated training deployment; simulate malicious-client poisoning and backdoors; compare aggregation, clipping, and validation controls under equal budgets; state residual risk.
**Subtopics.** FL architecture and roles; cross-device versus cross-silo; FedAvg and aggregation rounds; trust assumptions for clients, coordinator, and network; non-IID data and client drift; malicious-client update poisoning; backdoors and scaling attacks; Sybil clients; update inspection and client validation; norm clipping, trimmed mean, coordinate median, and Krum; assumptions and failure modes of robust aggregation; secure aggregation and DP-FL at a conceptual level; monitoring and provenance; residual risk in distributed training.
**Lab.** LAB-16. **Deliverable.** Federated simulation with benign, malicious, and defended runs, plus an equal-round comparison and residual-risk memo. **Assessment.** QZ-12; LAB-16.

### M13 — Privacy-Preserving Machine Learning (12 h)
**Objectives.** Explain differential privacy precisely enough to audit a claim; compute sensitivity and simple composition; build a noisy release; measure utility and an empirical privacy signal; distinguish formal guarantees from empirical measurements.
**Subtopics.** Privacy threat models and the limits of anonymization; neighboring datasets, sensitivity, epsilon/delta; Laplace and Gaussian mechanisms; parallel and sequential composition; privacy budgets; per-example clipping and noise; DP-SGD at a conceptual level; local versus central DP; secure aggregation and cryptographic approaches conceptually; synthetic data limits; membership-inference evaluation and its caveats; privacy-utility trade-offs; documentation and governance obligations.
**Lab.** LAB-17. **Deliverable.** DP release experiment with accounting inputs, utility comparison, empirical membership-inference signal, and a limitations statement. **Assessment.** QZ-13; LAB-17; MP-03.

### M14 — Explainability, Fairness, and Security Trade-offs (10 h)
**Objectives.** Compare explanation methods and their assumptions; test explanation stability under controlled input changes; identify leakage through explanations; measure subgroup performance and fairness gaps; reason about how explanation, fairness, privacy, and robustness trade off.
**Subtopics.** Global versus local explanations; coefficients, gradient×input, occlusion, surrogate explanations; fidelity versus plausibility; explanation stability and sensitivity to perturbation; explanation leakage of training data or model internals; adversarial manipulation of explanations; fairness definitions and their incompatibilities; subgroup evaluation, confidence intervals, and small-sample risk; demographic parity, equalized odds, and calibration; fairness-aware training and its costs; security trade-offs and documentation.
**Lab.** LAB-18. **Deliverable.** Explanation and subgroup audit comparing a baseline and a reweighted model, including stability and trade-off analysis. **Assessment.** QZ-14; LAB-18.

### M15 — Generative AI, LLM, RAG, and AI Agent Security (18 h)
**Objectives.** Distinguish classical predictive-ML security from LLM application security; assess an LLM application against recognized risk taxonomies; test direct and indirect prompt injection; secure a RAG boundary; evaluate output handling and tool use; constrain an agent's authority and prove the constraint in code.
**Subtopics.** LLM application attack surface; model versus application versus agent trust boundaries; prompt injection, direct and indirect; retrieval poisoning and RAG trust boundaries; instruction hierarchy; sensitive-information disclosure; insecure output handling; excessive agency; tool misuse and delegated authority; untrusted tool outputs; model and dataset provenance; access control and tenant isolation; OWASP Top 10 for LLM Applications and Agentic AI guidance; MITRE ATLAS and NIST AI 100-2 terminology; why prompt filtering alone is not a complete defense; layered controls, monitoring, and incident response.
**Labs.** LAB-19, LAB-20. **Deliverable.** A RAG-boundary evaluation with canary and injection tests, plus a mock agent with enforced capability, approval, and egress controls and an action log. **Assessment.** QZ-15; LAB-19/20; MP-04.

### M16 — End-to-End ML Security Assessment (16 h)
**Objectives.** Scope an ML system and its business decision; classify assets and data; convert a threat model into falsifiable tests; establish baselines and negative controls; run bounded attack and defense experiments; report findings with severity, cost, owner, retest, and residual risk.
**Subtopics.** Assessment versus technique demo; scope, non-goals, and authorization; architecture and data-flow diagrams; data classification; adversary profiles; risk anchors and dispositions; test matrices with oracle, budget, metric, and denominator; baselines and zero-budget controls; uncertainty and evidence integrity; attack and defense measurement; costed remediation; residual-risk statements; report and briefing structure. Six project scenarios: fraud scoring, image poisoning/backdoor, prediction-API privacy, secure pipeline, RAG/agent, robustness comparison.
**Projects.** One of PRJ-01…PRJ-06. **Deliverable.** A project dossier with scope, threat model, test plan, baseline, experiment evidence, defended system, report, briefing, and reproduction package. **Assessment.** QZ-16; one project.

### M17 — ML Red-Team and Blue-Team Simulation (14 h)
**Objectives.** Write rules of engagement; plan attacks as falsifiable hypotheses under fixed budgets; execute a bounded campaign against a local service; build and calibrate detections on a quiet baseline; reconstruct a timeline; evaluate mitigations against an adaptive variant.
**Subtopics.** Authorization, scope, non-goals, constraints, data handling, roles, communications, and stop conditions; red objectives tied to business objectives; ML API kill chain; request, time, feature, concurrency, and attempt budgets; evidence capture and redaction; telemetry schema; detection hypotheses and bounded features; threshold calibration, base rates, and false positives; triage, containment, eradication, recovery, and verification; TTD, TTC, and TTR; purple-team outputs; fair adaptive retest; residual risk.
**Exercise.** RT-01 (9 h), against a local dispatch-risk service. **Deliverable.** Red plan and evidence log, blue detection and response package, purple synthesis, and adaptive-retest report. **Assessment.** QZ-17; RT-01.

### M18 — Capstone Projects and Research Extensions (4 h)
**Objectives.** Turn a broad interest into a scoped capstone; manage milestones and a reproducibility contract; present results and limitations honestly; convert a completed assessment into a bounded research question.
**Subtopics.** Capstone versus lab; scope scoring; one system, one decision, two questions, one control; proposal template; milestone gates M0–M5; clean-checkout reproduction; run records and hashes; claim-first results; table and figure selection; uncertainty and small samples; negative results; construct, internal, external, and statistical validity; topic versus question versus gap; contribution types; claim–evidence tables; controls and ablations; pre-registration-lite; supervision, ethics, and timeline for an MPhil-level extension.
**Capstone.** CAP-A…CAP-F. **Deliverable.** Proposal, milestone record, reproduction package, technical report, briefing, and optional research-question canvas. **Assessment.** QZ-18; CAP.

### CAP — Capstone (40 h)
**Objectives.** Conduct an end-to-end security assessment of an ML system; integrate threat modeling, attack, defense, engineering, and communication; produce an auditable artifact.
**Options.** CAP-A through CAP-F in §12.4. **Deliverable.** Proposal, weekly log, technical artifact, 8–12 page report, 10-minute recorded briefing, reproducibility package. **Assessment.** Capstone rubric (§10.2).

---

## 9. Assessment architecture

### 9.1 Weights

| Component | Weight | Notes |
|---|---:|---|
| Knowledge checks (QZ-00…QZ-18) | 10% | Highest 16 of 19 scores; pass mark 80% per quiz; unlimited retakes |
| Labs and applied project (LAB-01…LAB-20; one of PRJ-01…PRJ-06 or RT-01) | 40% | 16 labs required by track; one project required for the applied track; rubric-scored; lowest two lab scores may be dropped |
| Mini-projects (MP-01…MP-04) | 20% | Choose any two; 8 h each |
| Capstone (CAP) | 30% | Required for Full track; rubric-scored |
| **Total** | **100%** | |

**Completion criteria (self-study certificate).** Overall ≥ 80%, all required labs submitted, one applied project at Proficient or above, capstone ≥ "Proficient" (3/4) on every dimension, and a signed ethics/authorized-use statement. No formal credit is implied; the certificate is a course-completion record, not an accredited qualification.

### 9.2 Self-assessment protocol

1. Attempt the lab without reading the reference solution.
2. Score your own artifact against the rubric *before* viewing the solution.
3. Record a 5-line reflection: what worked, what failed, what you would test next, what you misunderstood, what evidence is missing.
4. If a claim cannot be reproduced from a clean environment, it is not complete.
5. Optionally request peer review using the review checklist in `maintainers/review-checklist.md` (planned).

### 9.3 Academic integrity and AI-assistant policy

- **Allowed:** asking an assistant to explain a concept, debug an error, review code, or suggest a test.
- **Not allowed for graded artifacts:** submitting assistant-generated analysis you cannot defend line by line; fabricating results; copying another learner's report.
- **Required:** disclose material AI assistance in a short "Tools used" note (tool, purpose, what you verified).
- **Never:** paste private, proprietary, or restricted data into a third-party assistant; use assistants to generate attacks against systems you do not own.

### 9.4 Optional cohort mode

The same materials support a facilitated cohort: weekly 60-minute discussion, peer review pairs, and a showcase. Cohort mode changes logistics, not the artifacts or rubrics. No cohort features are required for self-study.

---

## 10. Rubrics

### 10.1 Standard lab rubric (100 points)

| Dimension | Weight | Exemplary (4) | Proficient (3) | Developing (2) | Insufficient (1) |
|---|---:|---|---|---|---|
| Technical correctness | 30 | Attack/defense runs as specified; metrics computed correctly; edge cases handled | Runs correctly with minor omissions | Partially works; metric errors | Does not run or results invalid |
| Security reasoning | 25 | Explicit threat model, budgets, assumptions, and limitations; distinguishes capability from claim | Clear threat model with minor gaps | Vague threat model; overclaims | No threat model or misleading claims |
| Experimental method | 20 | Controlled comparisons, multiple seeds, uncertainty, ablations | Sound comparison, limited uncertainty | Single run or confounded comparison | Anecdotal |
| Reproducibility | 15 | Pinned environment, seeds, commands, artifact manifest; reproduces from clean checkout | Reproduces with small fixes | Missing steps | Not reproducible |
| Communication and ethics | 10 | Concise report; correct severity; safety and legal constraints addressed | Clear with minor issues | Disorganized or overlong | Unsafe or unprofessional |

### 10.2 Capstone rubric (100 points)

| Dimension | Weight | What "Proficient" looks like |
|---|---:|---|
| Problem framing and scope | 15 | System, assets, adversary, and success criteria are explicit; out-of-scope is stated |
| Technical depth | 25 | At least two attack/defense families applied correctly; implementation is non-trivial and verified |
| Evaluation rigor | 20 | Budgets, seeds, baselines, uncertainty, and adaptive attacks addressed; negative results reported |
| Mitigations and engineering | 15 | Controls are specific, prioritized, costed, and mapped to frameworks; residual risk stated |
| Communication | 15 | Report is auditable, well structured, and free of overclaiming; briefing is clear |
| Ethics, legality, reproducibility | 10 | Authorized targets only; disclosure considered; clean-environment reproduction demonstrated |

### 10.3 Applied project and RT-01 rubric (100 points)

| Dimension | Weight | What "Proficient" looks like |
|---|---:|---|
| Scope, system, and data understanding | 10 | One decision, explicit non-goals, correct asset classification, current architecture |
| Threat model | 15 | Testable adversary profiles, anchored scores, a disposition for every register entry |
| Baseline and experimental design | 15 | Frozen evaluation set, negative controls, falsifiable oracle, uncertainty |
| Attack or analysis correctness | 20 | Correct budgets, denominators, and metrics; no zero-budget artifact; results reproducible |
| Defense design and evaluation | 15 | Control tested statically and adaptively, with benign cost and residual success |
| Reproducibility and evidence | 10 | Pinned environment, clean-checkout run, hashed manifest, attributable evidence |
| Risk communication | 10 | Severity tied to exposure; costed remediation; clear residual risk and owner |
| Ethics, safety, and limitations | 5 | Authorized local target, no personal data, honest scope of claim |

RT-01 uses the same 100-point scale with red execution and blue detection scored separately: RoE and scope 10, threat model 15, red execution and evidence 20, blue detection and response 20, mitigation and adaptive retest 15, reproducibility 10, communication 5, safety and ethics 5.

### 10.4 Mini-project rubric

Reuse the lab rubric with the "Experimental method" weight increased to 25 and "Communication" to 15 (technical 30, security 20, method 25, reproducibility 10, communication 15). Mini-projects require a one-page executive summary in addition to the notebook.

---

## 11. Knowledge checks and quizzes

### 11.1 Blueprint

| Property | Design |
|---|---|
| Items per module | 10 (M00: 8) |
| Item mix | 20% recall, 40% apply, 30% analyze, 10% evaluate/create |
| Formats | Single-choice, multi-select, numeric, short answer, "find the flaw" code snippet |
| Pass mark | 80%, unlimited retakes, no time limit |
| Feedback | Explanation for every option; misconception tags |
| Anti-gaming | Randomized order in the site build; no answers in page source until "reveal" is clicked |

### 11.2 Sample items (with answers)

**Q (M04, apply).** For a model with loss $J(\theta,x,y)$ and $L_\infty$ budget $\epsilon$, the one-step FGSM perturbation is:
A. $x' = x - \epsilon\,\mathrm{sign}(\nabla_x J)$
B. $x' = x + \epsilon\,\mathrm{sign}(\nabla_x J)$
C. $x' = x + \epsilon\,\nabla_x J$
D. $x' = x + \epsilon\,\mathrm{sign}(\nabla_\theta J)$
**Answer: B.** The sign maximizes the first-order increase in loss under an L∞ constraint. C is an unnormalized gradient step; D differentiates with respect to parameters, not input.

**Q (M08, analyze).** A paper reports 0% attack success using PGD with a fixed step size and no restarts. Give two reasons this is not evidence of robustness.
**Model answer.** (1) The attack may be underpowered (step size, iterations, restarts), so failure to find an example is not a guarantee. (2) The defense may cause gradient masking or shattered gradients, which defeats a gradient-based attack without removing the vulnerability; an adaptive or gradient-free attack is required. Bonus: no certified bound, and the evaluation may not cover the threat model.

**Q (M05, apply).** A dataset has 50,000 training examples and an attacker can flip 500 labels. What poisoning rate is this, and why does the answer depend on the attack type?
**Model answer.** 1%. Indiscriminate label flipping often needs a much higher rate to move test accuracy, while a targeted backdoor can succeed at well under 1% because it exploits trigger-specific features; the relevant denominator and success metric differ.

**Q (M14, recall/apply).** Which OWASP Top 10 for LLM Applications item covers an agent that can delete production records because its tools were over-permissioned?
**Answer.** LLM06:2025 Excessive Agency. The control is least-privilege tool scoping plus human confirmation for destructive actions, not a better system prompt alone. The 2026 edition of the list renumbers this category to LLM03, so state the edition whenever you cite the ID.

**Q (M12, evaluate).** Two systems report "differential privacy, ε = 1." Why is that statement insufficient to compare privacy risk?
**Model answer.** ε is meaningless without δ, the neighboring-relation definition, the mechanism and its composition across queries, the sensitivity assumptions, and the number of releases. ε = 1 for a single release differs from ε = 1 after thousands of training steps under composition.

### 11.3 Quiz-to-module map

QZ-00 → M00, QZ-01 → M01, …, QZ-18 → M18. Each quiz page links back to the lab or project and forward to the next module. No quiz is published before its module's lessons are complete.

---

## 12. Practical work

### 12.1 Challenge exercises

Each module M00–M15 has one optional **challenge exercise** (`CH-00`…`CH-15`): a 30–90 minute open task with no step-by-step guide. M16–M18 use the project briefs and research canvas as their extension work. Challenges are not weighted in the final score; they are for retrieval practice, portfolio depth, and interview preparation. Solutions are discussed in the module's "What good looks like" note, not published as a walkthrough.

| ID | Module | Challenge | Evidence |
|---|---|---|---|
| CH-00 | M00 | Classify three real incidents as ML security, application security, or neither; justify with assets and adversaries | 1-page analysis |
| CH-01 | M01 | Show a case where accuracy and macro-F1 disagree under class imbalance; explain which metric a defender should monitor | Notebook cell + note |
| CH-02 | M02 | Given a data-flow diagram, mark five trust boundaries and one missing control | Annotated diagram |
| CH-03 | M03 | Map ten ATLAS techniques to AI 100-2e2025 categories; identify one ambiguous mapping | Mapping table |
| CH-04 | M04 | Find a step-size/ε combination where your PGD collapses, then explain and fix it | Ablation table |
| CH-05 | M05 | Design a screening rule that catches the LAB-06 poisons while flagging fewer than ten clean rows; report the trade-off | Threshold table + memo |
| CH-06 | M06 | Design a tabular trigger that survives 20% feature dropout; measure the ASR drop | Robustness-of-trigger table |
| CH-07 | M07 | Extract a model with label-only queries; compare cost with confidence-based extraction | Fidelity/query table |
| CH-08 | M08 | Reproduce a preprocessing defense and defeat it with an adaptive attack; report the clean-accuracy cost | Attack log + comparison table |
| CH-09 | M09 | Design a validation gate that catches the LAB-12 schema, duplicate, and label defects while flagging fewer than ten clean rows; report the trade-off | Threshold table + memo |
| CH-10 | M10 | Find an unsigned-artifact path in a sample CI pipeline and patch it | Diff + negative test |
| CH-11 | M11 | Write five authorization and request-bound tests for a model API, including one object-level case, plus a detection that fires on a query burst but not a legitimate spike | Test suite + detection rule |
| CH-12 | M12 | Simulate one malicious client among eight; test whether trimmed mean and norm clipping help without collapsing clean accuracy | FL result table |
| CH-13 | M13 | Compute the budget for three sequential releases; implement one release and explain composition and a mitigation | Accounting worksheet + release |
| CH-14 | M14 | Perturb inputs until an explanation changes while the prediction does not; measure the rate and subgroup gaps | Stability table |
| CH-15 | M15 | Embed an indirect injection in an untrusted document, then harden the RAG-to-agent boundary and re-test | Attack/defense log + tool trace |

Challenge rules: local/sandbox targets only; no new dependencies if a standard one suffices; report negative results; if a challenge takes more than 90 minutes, stop and write down the blocker — that is itself useful evidence.

### 12.2 Mini-projects

| ID | Title | After | Effort | Core question |
|---|---|---|---:|---|
| MP-01 | Integrity red-team: poisoning and backdoor | M05–M06 | 8 h | Can you implant a conditional failure, measure it, and evaluate a defense under a fixed data budget? |
| MP-02 | Robustness audit of a local model | M08 | 8 h | Is the claimed robustness real under an adaptive attack? |
| MP-03 | Privacy and extraction assessment | M07, M13 | 8 h | How much does the model leak, and what does a defense cost in utility? |
| MP-04 | GenAI/agent red-team | M15 | 8 h | Which layered defenses survive an adaptive prompt-injection campaign? |

### 12.3 Applied projects and RT-01

Six project briefs and one red/blue exercise accompany M16–M17. Each is a complete assessment scenario with a fictional organization, a local synthetic system, data classification, threat model, staged tasks, required experiments, controls, deliverables, and a 100-point rubric. They are not extra labs and do not add to the lab-hours total.

| ID | Scenario | Core question | Reuses |
|---|---|---|---|
| PRJ-01 | Meridian Pay — card-not-present fraud scoring | Can data-quality faults and bounded feature changes move fraud decisions without breaking the dashboard? | LAB-03, LAB-05, LAB-12 |
| PRJ-02 | Aster Manufacturing — visual defect classification | Can a small poisoned or backdoored fraction survive a realistic pipeline and a screening defense? | LAB-05, LAB-06, LAB-07, LAB-08 |
| PRJ-03 | Helio Health — benefits triage API | What does the prediction interface leak under a fixed query budget, and what does output minimization cost? | LAB-09, LAB-10, LAB-17 |
| PRJ-04 | Cobalt Models — training and artifact pipeline | Do validation, dependency, signing, and reproducibility controls fail closed? | LAB-12, LAB-13 |
| PRJ-05 | Harbor — policy assistant with retrieval and tools | Does the application treat untrusted documents as data, and does the agent enforce authority in code? | LAB-19, LAB-20 |
| PRJ-06 | Sentinel Vision — access-badge classifier | Which defense gives the best robustness per unit of clean accuracy, false positives, and runtime? | LAB-03, LAB-11 |
| RT-01 | Pinewood Logistics — dispatch-risk service | Can a bounded red campaign evade detection, and do the blue detections and mitigations survive adaptation? | LAB-03, LAB-11, LAB-14, LAB-15 |

Each project is about 11 hours; RT-01 is 9 hours. All are local and CPU-first, and none requires an API key or a third-party target. The [project catalog](projects/index.md) is the student entry point; the [project-catalog](project-catalog.md) planning document holds the reuse map, artifact contract, and evaluator policy.

### 12.4 Capstone options

| ID | Title | Artifact | Difficulty |
|---|---|---|---|
| CAP-A | End-to-end risk assessment of a public ML service (local replica) | Threat model, red-team results, prioritized controls, report | 5 |
| CAP-B | Replication and critique of a robustness benchmark | Reproduced subset, adaptive-attack challenge, methodological critique | 5 |
| CAP-C | Privacy attack and DP defense study | MIA/inversion pipeline, DP-SGD comparison, accounting, harm analysis | 5 |
| CAP-D | Secure ML supply chain blueprint | Signed artifacts, SBOM/ML-BOM, CI gates, registry policy, demo | 4 |
| CAP-E | Agentic AI security evaluation harness | Test suite, attack scenarios, defense evaluation, responsible-disclosure plan | 5 |
| CAP-F | Federated learning threat model and robust aggregation study | FL simulation, attacks, robust aggregation/DP, residual-risk report | 5 |

Every capstone must include an **authorized-use statement** naming the systems tested (local/synthetic/public sandbox only), a **reproducibility package**, and a **limitations** section. CAP-A and CAP-E must not target third-party production systems.

---

## 13. Datasets and tooling

### 13.1 Data principles

- Do not vendor datasets into the repository. Use download scripts with checksums and document licenses.
- Prefer small, public, well-understood datasets; cap runtime so labs stay laptop-friendly.
- Do not use personal or sensitive data. For privacy labs, use public benchmarks or synthetic data; never attempt to identify individuals.
- Record dataset version/hash in the artifact manifest.

### 13.2 Dataset shortlist

| Dataset | Used in | Role | Access note |
|---|---|---|---|
| scikit-learn digits | M01–M12 | Fast baselines, evasion, backdoors, extraction, privacy, FL, robustness | Ships with scikit-learn; no download |
| MNIST / Fashion-MNIST | M08, M11, M15 (optional) | Robustness, monitoring, inversion | Via `torchvision`; verify license at source |
| CIFAR-10 | M08 (optional) | Larger vision benchmark | [cs.toronto.edu/~kriz/cifar.html](https://www.cs.toronto.edu/~kriz/cifar.html) |
| UCI Adult | M07, M11 (optional) | Tabular classification, extraction, monitoring | [UCI dataset 2](https://archive.ics.uci.edu/dataset/2/adult) |
| SMS Spam Collection | M15 (optional) | Text classification examples | [UCI dataset 228](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) |
| NSL-KDD / CICIDS2017 | M11 (optional) | Network intrusion detection context | [NSL-KDD](https://www.unb.ca/cic/datasets/nsl.html) · [CICIDS2017](https://www.unb.ca/cic/datasets/ids-2017.html) |
| EMBER | M11 (optional) | Malware static features | [github.com/elastic/ember](https://github.com/elastic/ember) |
| FEMNIST (LEAF) | M12 | Federated non-IID partitions | [leaf.cmu.edu](https://leaf.cmu.edu/) |
| Credit card fraud (ULB) | M11 (optional) | Imbalanced tabular monitoring | [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) (account required) |
| BackdoorBench / TDC | M06 (optional) | Backdoor benchmark comparisons | [BackdoorBench](https://github.com/SCLBD/BackdoorBench) · [TDC](https://www.trojandetection.ai/) |
| RobustBench | M08 | Standardized robustness leaderboard | [robustbench.github.io](https://robustbench.github.io/) |
| HarmBench / JailbreakBench | M15 (optional) | LLM safety/jailbreak evaluation | [harmbench.org](https://www.harmbench.org/) · [JailbreakBench](https://jailbreakbench.github.io/) |
| AgentDojo | M15 (optional) | Prompt-injection evaluation for agents | [github.com/ethz-spylab/agentdojo](https://github.com/ethz-spylab/agentdojo) |

**Purchase-100** (Kaggle) is a common membership-inference benchmark; it is not required by LAB-10, which uses digits. Any optional extension that uses it must have a local synthetic fallback. Dataset availability changes; every lab needs a fallback path.

### 13.3 Tool shortlist

| Tool | Purpose | Used in |
|---|---|---|
| NumPy, scikit-learn, pandas | Models, attacks, evaluation | All published labs |
| PyTorch (CPU) | Differentiable models for robustness and DP labs | LAB-11, LAB-17 (optional) |
| IBM Adversarial Robustness Toolbox (ART) | Library cross-checks for evasion and poisoning | LAB-03–LAB-08 (optional) |
| Foolbox | Gradient and decision-based attacks | LAB-04 (optional) |
| SecML | Secure ML research toolkit | Optional |
| TextAttack | NLP adversarial attacks | M15 (optional) |
| AutoAttack (`fra31/auto-attack`) | Robustness evaluation | LAB-11 (optional; the published lab implements PGD by hand) |
| RobustBench | Benchmark models/leaderboard | LAB-11 (optional) |
| BackdoorBench | Backdoor implementations | LAB-07/08 (optional) |
| ModelScan, picklescan | Artifact scanning | LAB-13 |
| safetensors, ONNX | Safe serialization/interchange | LAB-13 |
| Sigstore/cosign, in-toto, SLSA | Signing/provenance | LAB-13 (concepts; the published lab uses HMAC-SHA256 locally) |
| CycloneDX, SPDX | SBOM/ML-BOM | LAB-13 |
| FastAPI, Uvicorn | Serving | LAB-14 (optional; the published lab uses the standard library `http.server`) |
| Docker, Trivy | Containerization/scanning | LAB-14 (optional) |
| Evidently, Alibi-Detect | Drift/outlier detection | LAB-15 (optional; the published lab implements windowed detectors) |
| Flower | Federated learning simulation | LAB-16 (optional) |
| diffprivlib, Opacus | DP mechanisms and DP-SGD | LAB-17 (optional; the published lab implements Laplace releases directly) |
| LIME, SHAP | Post-hoc local explanations | LAB-18 (optional; the published lab implements gradient×input and occlusion directly) |
| garak, PyRIT, promptfoo | LLM red teaming | LAB-19 (optional) |
| NeMo Guardrails, LLM Guard | Layered LLM defenses | LAB-19 (optional) |
| Inspect (UK AISI) | Evaluation harness | LAB-19/20 (optional) |
| AgentDojo | Agent injection evaluation | LAB-20 (optional) |

Version policy: pin exact versions in `labs/shared/requirements-*.txt` at implementation time; test on Linux and Windows; document GPU alternatives. CleverHans is listed only as historical context — it is not a maintained dependency.

---

## 14. Self-study operating system

### 14.1 Weekly loop (recommended 6–10 h)

| Block | Time | Activity |
|---|---:|---|
| Preview | 20 min | Skim objectives, lab deliverable, and quiz topics; write 3 questions |
| Read | 60–90 min | One lesson at a time; take notes in your own words |
| Practice | 60–120 min | Run the guided notebook; change one variable; record results |
| Lab | 2–4 h | Complete the lab artifact; commit code locally with a meaningful message |
| Retrieve | 20 min | Closed-book quiz; re-derive the key equation or attack loop |
| Reflect | 15 min | Update the study log; schedule a 1-3-7-21 day review |

### 14.2 Lesson protocol (six steps)

1. **Scenario** — read the failure story and identify the asset at risk.
2. **Objectives** — state what you will be able to do, not what you will read.
3. **Concept** — worked explanation with a minimal example.
4. **Guided practice** — a notebook cell you run and modify.
5. **Check** — quiz items with explanations.
6. **Artifact** — a lab deliverable plus a short written analysis.

### 14.3 Spaced review

Review each module at 1, 3, 7, and 21 days. Use only retrieval: re-derive FGSM, restate the difference between poisoning and backdoors, sketch a threat model, explain ε to a peer. Do not re-read passively.

### 14.4 Evidence portfolio

Each module contributes one folder containing: notebook, `README.md` with threat model and results, `requirements.txt` or lockfile, artifact manifest (hashes), and a 5-line reflection. The capstone reuses these artifacts; a portfolio with broken reproduction steps is not complete.

### 14.5 Study log template

```
Date:
Module / lab:
Time spent:
What I predicted:
What happened:
Metric(s):
Surprise / failure:
Next test:
Question for review:
```

### 14.6 Getting unstuck

1. Reproduce the smallest failing case.
2. Check shapes, dtypes, ranges, device, and seeds.
3. Compare against the reference implementation on one batch.
4. Reduce to a subset and one iteration.
5. Search the error text plus library version.
6. Ask a precise question with the minimal reproducer.
7. If blocked for more than 90 minutes, move to the theory and return with fresh eyes.

### 14.7 Using AI assistants responsibly

Assistants are useful for explaining an error, proposing a test, or reviewing a threat model. They are unreliable for exact API signatures, dataset availability, and citations. Verify every factual claim and every line of attack code. Never let an assistant's confidence substitute for a measured result.

---

## 15. Troubleshooting guide (seed content for `docs/start/troubleshooting.md`)

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError` | Wrong environment | Activate the lab venv; reinstall from the pinned file |
| CUDA error / no GPU | Driver or wheel mismatch | Use the CPU requirements; set the device explicitly to CPU |
| `torch` install is huge/slow | Default CUDA wheels | Install the CPU-only wheel index |
| CIFAR download fails | Network/proxy | Download manually, verify checksum, point the loader at the local path |
| Kaggle 401/403 | Missing API token or unaccepted rules | Configure the token; accept the dataset terms |
| Out of memory | Batch/model too large | Reduce batch size, use a subset, enable mixed precision |
| Results differ between runs | Non-determinism | Set seeds; deterministic algorithms; `num_workers=0`; pin versions |
| Attack "succeeds" at ε=0 | Metric or label bug | Verify perturbation norm and that predictions changed |
| 0% attack success | Underpowered attack or gradient masking | Increase restarts/steps; try a gradient-free attack |
| Notebook state confusing | Out-of-order execution | Restart kernel and run all |
| Colab disconnects | Session limit | Checkpoint artifacts to mounted storage |
| AutoAttack takes hours | Full test set | Use a fixed subset and document it |
| Flower version errors | API drift | Pin the version used in the lab |
| Opacus unsupported layer | Unsupported module | Replace with supported layers or use per-sample gradients manually |
| `pip` resolver conflict | Mixed environments | Create a fresh venv; install from lockfile |
| Windows path too long | Legacy limit | Enable long paths or use WSL |
| Slow PGD on CPU | Compute bound | Use MNIST/Fashion-MNIST, a subset, and fewer steps; document the trade-off |

---

## 16. Safety, ethics, and law

- **Authorized targets only.** Labs use local processes, local containers, synthetic services, or explicitly public sandbox datasets. Attacking third-party systems is prohibited.
- **No real personal data.** Privacy labs use public benchmarks or synthetic records; do not attempt re-identification.
- **Contain offensive code.** Run artifact and agent labs in a disposable container/VM with no host credentials and no network egress unless required.
- **Responsible disclosure.** If a learner finds a real vulnerability in a public model or library, follow coordinated disclosure norms: private report to the maintainer, reasonable remediation time, no public exploit before a fix.
- **Law and policy.** Learners must comply with applicable law, institutional policy, and terms of service. The course does not provide legal advice. Cross-border rules differ; when in doubt, do not test.
- **Dual-use awareness.** Techniques taught here are published research. The course emphasizes measurement, defense, and documentation, and it does not provide operational tooling for attacking production systems.
- **Harm minimization in examples.** Avoid exercises that generate targeted disinformation, impersonation, or content harmful to real people.

---

## 17. Reference architecture

All links were checked on 2026-10-28 unless marked otherwise. Publisher sites (ACM, ISO, some DOI resolvers) block automated requests and may return 403 to a link checker while resolving normally in a browser; DOI targets were verified through Crossref or DOI resolution where possible. Re-verify before publication; framework versions change faster than courses.

### 17.1 Frameworks, standards, and guidance

| ID | Reference |
|---|---|
| F-01 | Vassilev, A., Oprea, A., Fordyce, A., Anderson, H., Davies, X., & Hamin, M. *Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations.* NIST AI 100-2 E2025, March 2025. DOI [10.6028/NIST.AI.100-2e2025](https://doi.org/10.6028/NIST.AI.100-2e2025) · [CSRC](https://csrc.nist.gov/pubs/ai/100/2/e2025/final) |
| F-02 | MITRE ATLAS knowledge base, data release v2026.09 (published 2026-09-15; 16 tactics, 120 techniques, 88 sub-techniques, 40 mitigations, 73 case studies). [atlas.mitre.org](https://atlas.mitre.org/) · [atlas-data](https://github.com/mitre-atlas/atlas-data) |
| F-03 | NIST. *Artificial Intelligence Risk Management Framework (AI RMF 1.0).* NIST AI 100-1, January 2023. DOI [10.6028/NIST.AI.100-1](https://doi.org/10.6028/NIST.AI.100-1) |
| F-04 | NIST. *AI RMF: Generative Artificial Intelligence Profile.* NIST AI 600-1, July 2024. DOI [10.6028/NIST.AI.600-1](https://doi.org/10.6028/NIST.AI.600-1) |
| F-05 | NIST. *Secure Software Development Framework (SSDF) Version 1.1.* NIST SP 800-218, February 2022. DOI [10.6028/NIST.SP.800-218](https://doi.org/10.6028/NIST.SP.800-218) |
| F-06 | NIST. *Secure Software Development Practices for Generative AI and Dual-Use Foundation Models: An SSDF Community Profile.* NIST SP 800-218A, July 2024. [PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218A.pdf) |
| F-07 | OWASP GenAI Security Project. *OWASP Top 10 for LLM Applications 2025* (LLM01–LLM10). [Resource](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) |
| F-07A | OWASP GenAI Security Project. *OWASP GenAI LLM Top 10 2026*, v1.0, published 2026-08-04. [Resource](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) · DOI [10.5281/zenodo.22109015](https://doi.org/10.5281/zenodo.22109015) |
| F-08 | OWASP GenAI Security Project. *Agentic AI — Threats and Mitigations*, v1.1 (December 2025). [Resource](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) |
| F-09 | OWASP. *Machine Learning Security Top 10* (incubator project). [Project](https://owasp.org/projects/machine-learning-security-top-ten) · [Repository](https://github.com/OWASP/www-project-machine-learning-security-top-10) |
| F-10 | OWASP. *AI Exchange* (AI security and privacy guide). [owaspai.org](https://owaspai.org/) |
| F-11 | CISA & UK NCSC et al. *Guidelines for Secure AI System Development*, November 2023. [CISA alert](https://www.cisa.gov/news-events/alerts/2023/11/26/cisa-and-uk-ncsc-unveil-joint-guidelines-secure-ai-system-development) · [NCSC collection](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development) |
| F-12 | ISO/IEC 42001:2023, *Information technology — Artificial intelligence — Management system.* [ISO catalogue](https://www.iso.org/standard/81230.html) |
| F-13 | ISO/IEC 23894:2023, *Information technology — Artificial intelligence — Guidance on risk management.* [ISO catalogue](https://www.iso.org/standard/77304.html) |
| F-14 | Regulation (EU) 2024/1689 (Artificial Intelligence Act). [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) |
| F-15 | Cloud Security Alliance. *Agentic AI Threat Modeling Framework (MAESTRO)*, 2025. [CSA](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro) |
| F-16 | Google. *Secure AI Framework (SAIF).* [saif.google](https://saif.google/) |
| F-17 | OpenSSF. *SLSA* · *Sigstore* · CycloneDX *ML-BOM* · SPDX 3.0. [slsa.dev](https://slsa.dev/) · [sigstore.dev](https://www.sigstore.dev/) · [CycloneDX ML-BOM](https://cyclonedx.org/capabilities/mlbom/) · [spdx.dev](https://spdx.dev/) |
| F-22 | NIST. *Technical Guide to Information Security Testing and Assessment.* NIST SP 800-115, September 2008. [CSRC](https://csrc.nist.gov/pubs/sp/800/115/final) |
| F-23 | OWASP. *Web Security Testing Guide (WSTG)*, v4.2. [Project](https://owasp.org/www-project-web-security-testing-guide/) |

### 17.2 Surveys and foundational reading

| ID | Reference |
|---|---|
| R-01 | Biggio, B., & Roli, F. *Wild Patterns: Ten Years After the Rise of Adversarial Machine Learning.* arXiv:1712.03141, 2017. [arXiv](https://arxiv.org/abs/1712.03141) |
| R-02 | Biggio, B., Corona, I., Maiorca, D., et al. *Evasion Attacks against Machine Learning at Test Time.* arXiv:1708.06131, 2017. [arXiv](https://arxiv.org/abs/1708.06131) |
| R-03 | Kairouz, P., McMahan, H. B., Avent, B., et al. *Advances and Open Problems in Federated Learning.* arXiv:1912.04977, 2019. [arXiv](https://arxiv.org/abs/1912.04977) |
| R-04 | Gama, J., Žliobaitė, I., Bifet, A., Pechenizkiy, M., & Bouchachia, A. *A Survey on Concept Drift Adaptation.* ACM Computing Surveys, 2014. DOI [10.1145/2523813](https://doi.org/10.1145/2523813) |

### 17.3 Evasion and robustness

| ID | Reference |
|---|---|
| R-10 | Szegedy, C., Zaremba, W., Sutskever, I., et al. *Intriguing properties of neural networks.* arXiv:1312.6199, 2013. [arXiv](https://arxiv.org/abs/1312.6199) |
| R-11 | Goodfellow, I. J., Shlens, J., & Szegedy, C. *Explaining and Harnessing Adversarial Examples.* arXiv:1412.6572, 2014. [arXiv](https://arxiv.org/abs/1412.6572) |
| R-12 | Papernot, N., McDaniel, P., Jha, S., et al. *The Limitations of Deep Learning in Adversarial Settings.* arXiv:1511.07528, 2015. [arXiv](https://arxiv.org/abs/1511.07528) |
| R-13 | Kurakin, A., Goodfellow, I., & Bengio, S. *Adversarial examples in the physical world.* arXiv:1607.02533, 2016. [arXiv](https://arxiv.org/abs/1607.02533) |
| R-14 | Carlini, N., & Wagner, D. *Towards Evaluating the Robustness of Neural Networks.* arXiv:1608.04644, 2016. [arXiv](https://arxiv.org/abs/1608.04644) |
| R-15 | Moosavi-Dezfooli, S.-M., Fawzi, A., & Frossard, P. *DeepFool: a simple and accurate method to fool deep neural networks.* arXiv:1511.04599, 2015. [arXiv](https://arxiv.org/abs/1511.04599) |
| R-16 | Moosavi-Dezfooli, S.-M., Fawzi, A., Fawzi, O., & Frossard, P. *Universal adversarial perturbations.* arXiv:1610.08401, 2016. [arXiv](https://arxiv.org/abs/1610.08401) |
| R-17 | Brown, T. B., Mané, D., Roy, A., et al. *Adversarial Patch.* arXiv:1712.09665, 2017. [arXiv](https://arxiv.org/abs/1712.09665) |
| R-18 | Madry, A., Makelov, A., Schmidt, L., et al. *Towards Deep Learning Models Resistant to Adversarial Attacks.* arXiv:1706.06083, 2017. [arXiv](https://arxiv.org/abs/1706.06083) |
| R-19 | Athalye, A., Carlini, N., & Wagner, D. *Obfuscated Gradients Give a False Sense of Security.* arXiv:1802.00420, 2018. [arXiv](https://arxiv.org/abs/1802.00420) |
| R-20 | Andriushchenko, M., Croce, F., Flammarion, N., & Hein, M. *Square Attack: a query-efficient black-box adversarial attack via random search.* arXiv:1912.00049, 2019. [arXiv](https://arxiv.org/abs/1912.00049) |
| R-21 | Chen, J., Jordan, M. I., & Wainwright, M. J. *HopSkipJumpAttack: A Query-Efficient Decision-Based Attack.* arXiv:1904.02144, 2019. [arXiv](https://arxiv.org/abs/1904.02144) |
| R-22 | Croce, F., & Hein, M. *Reliable evaluation of adversarial robustness with an ensemble of diverse parameter-free attacks.* arXiv:2003.01690, 2020. [arXiv](https://arxiv.org/abs/2003.01690) |
| R-23 | Croce, F., Andriushchenko, M., Sehwag, V., et al. *RobustBench: a standardized adversarial robustness benchmark.* arXiv:2010.09670, 2020. [arXiv](https://arxiv.org/abs/2010.09670) |
| R-24 | Carlini, N., Athalye, A., Papernot, N., et al. *On Evaluating Adversarial Robustness.* arXiv:1902.06705, 2019. [arXiv](https://arxiv.org/abs/1902.06705) |
| R-25 | Cohen, J. M., Rosenfeld, E., & Kolter, J. Z. *Certified Adversarial Robustness via Randomized Smoothing.* arXiv:1902.02918, 2019. [arXiv](https://arxiv.org/abs/1902.02918) |
| R-26 | Wong, E., & Kolter, J. Z. *Provable defenses against adversarial examples via the convex outer adversarial polytope.* arXiv:1711.00851, 2017. [arXiv](https://arxiv.org/abs/1711.00851) |
| R-27 | Zhang, H., Yu, Y., Jiao, J., et al. *Theoretically Principled Trade-off between Robustness and Accuracy (TRADES).* arXiv:1901.08573, 2019. [arXiv](https://arxiv.org/abs/1901.08573) |

### 17.4 Poisoning and backdoors

| ID | Reference |
|---|---|
| R-30 | Biggio, B., Nelson, B., & Laskov, P. *Poisoning Attacks against Support Vector Machines.* arXiv:1206.6389, 2012. [arXiv](https://arxiv.org/abs/1206.6389) |
| R-31 | Gu, T., Dolan-Gavitt, B., & Garg, S. *BadNets: Identifying Vulnerabilities in the Machine Learning Model Supply Chain.* arXiv:1708.06733, 2017. [arXiv](https://arxiv.org/abs/1708.06733) |
| R-32 | Chen, X., Liu, C., Li, B., et al. *Targeted Backdoor Attacks on Deep Learning Systems Using Data Poisoning.* arXiv:1712.05526, 2017. [arXiv](https://arxiv.org/abs/1712.05526) |
| R-33 | Liu, Y., Ma, S., Aafer, Y., et al. *Trojaning Attack on Neural Networks.* NDSS 2018. (Venue citation; no DOI asserted.) |
| R-34 | Wang, B., Yao, Y., Shan, S., et al. *Neural Cleanse: Identifying and Mitigating Backdoor Attacks in Neural Networks.* IEEE S&P 2019. DOI [10.1109/SP.2019.00031](https://doi.org/10.1109/SP.2019.00031) |
| R-35 | Gao, Y., Xu, C., Wang, D., et al. *STRIP: A Defence Against Trojan Attacks on Deep Neural Networks.* arXiv:1902.06531, 2019. [arXiv](https://arxiv.org/abs/1902.06531) |
| R-36 | Liu, K., Dolan-Gavitt, B., & Garg, S. *Fine-Pruning: Defending Against Backdooring Attacks on Deep Neural Networks.* arXiv:1805.12185, 2018. [arXiv](https://arxiv.org/abs/1805.12185) |
| R-37 | Tran, B., Li, J., & Madry, A. *Spectral Signatures in Backdoor Attacks.* arXiv:1811.00636, 2018. [arXiv](https://arxiv.org/abs/1811.00636) |
| R-38 | Schwarzschild, A., Goldblum, M., Gupta, A., et al. *Just How Toxic is Data Poisoning? A Unified Benchmark for Backdoor and Data Poisoning Attacks.* arXiv:2006.12557, 2020. [arXiv](https://arxiv.org/abs/2006.12557) |
| R-39 | Carlini, N., & Terzis, A. *Poisoning and Backdooring Contrastive Learning.* arXiv:2106.09667, 2021. [arXiv](https://arxiv.org/abs/2106.09667) |
| R-40 | Tramèr, F., Shokri, R., San Joaquin, A., et al. *Truth Serum: Poisoning Machine Learning Models to Reveal Their Secrets.* arXiv:2204.00032, 2022. [arXiv](https://arxiv.org/abs/2204.00032) |
| R-41 | Shumailov, I., Zhao, Y., Bates, D., et al. *Sponge Examples: Energy-Latency Attacks on Neural Networks.* arXiv:2006.03463, 2020. [arXiv](https://arxiv.org/abs/2006.03463) |

### 17.5 Extraction, inference, and privacy

| ID | Reference |
|---|---|
| R-50 | Tramèr, F., Zhang, F., Juels, A., et al. *Stealing Machine Learning Models via Prediction APIs.* arXiv:1609.02943, 2016. [arXiv](https://arxiv.org/abs/1609.02943) |
| R-51 | Orekondy, T., Schiele, B., & Fritz, M. *Knockoff Nets: Stealing Functionality of Black-Box Models.* arXiv:1812.02766, 2018. [arXiv](https://arxiv.org/abs/1812.02766) |
| R-52 | Jagielski, M., Carlini, N., Berthelot, D., et al. *High Accuracy and High Fidelity Extraction of Neural Networks.* arXiv:1909.01838, 2019. [arXiv](https://arxiv.org/abs/1909.01838) |
| R-53 | Carlini, N., Jagielski, M., Mironov, I., et al. *Cryptanalytic Extraction of Neural Network Models.* arXiv:2003.04884, 2020. [arXiv](https://arxiv.org/abs/2003.04884) |
| R-54 | Adi, Y., Baum, C., Cisse, M., et al. *Turning Your Weakness Into a Strength: Watermarking Deep Neural Networks by Backdooring.* arXiv:1802.04633, 2018. [arXiv](https://arxiv.org/abs/1802.04633) |
| R-55 | Uchida, Y., Nagai, Y., Sakazawa, S., & Satoh, S. *Embedding Watermarks into Deep Neural Networks.* arXiv:1701.04082, 2017. [arXiv](https://arxiv.org/abs/1701.04082) |
| R-56 | Shokri, R., Stronati, M., Song, C., & Shmatikov, V. *Membership Inference Attacks against Machine Learning Models.* arXiv:1610.05820, 2016. [arXiv](https://arxiv.org/abs/1610.05820) |
| R-57 | Carlini, N., Chien, S., Nasr, M., et al. *Membership Inference Attacks From First Principles (LiRA).* arXiv:2112.03570, 2021. [arXiv](https://arxiv.org/abs/2112.03570) |
| R-58 | Fredrikson, M., Jha, S., & Ristenpart, T. *Model Inversion Attacks that Exploit Confidence Information and Basic Countermeasures.* ACM CCS 2015. DOI [10.1145/2810103.2813677](https://doi.org/10.1145/2810103.2813677) |
| R-59 | Zhang, Y., Jia, R., Pei, H., et al. *The Secret Revealer: Generative Model-Inversion Attacks Against Deep Neural Networks.* arXiv:1911.07135, 2019. [arXiv](https://arxiv.org/abs/1911.07135) |
| R-60 | Abadi, M., Chu, A., Goodfellow, I., et al. *Deep Learning with Differential Privacy.* arXiv:1607.00133, 2016. [arXiv](https://arxiv.org/abs/1607.00133) |
| R-61 | Papernot, N., Abadi, M., Erlingsson, Ú., et al. *Semi-supervised Knowledge Transfer for Deep Learning from Private Training Data (PATE).* arXiv:1610.05755, 2016. [arXiv](https://arxiv.org/abs/1610.05755) |
| R-62 | Dwork, C., & Roth, A. *The Algorithmic Foundations of Differential Privacy.* Foundations and Trends in Theoretical Computer Science, 2014. DOI [10.1561/0400000042](https://doi.org/10.1561/0400000042) |
| R-63 | Carlini, N., Tramèr, F., Wallace, E., et al. *Extracting Training Data from Large Language Models.* arXiv:2012.07805, 2020. [arXiv](https://arxiv.org/abs/2012.07805) |
| R-64 | Carlini, N., Hayes, J., Nasr, M., et al. *Extracting Training Data from Diffusion Models.* arXiv:2301.13188, 2023. [arXiv](https://arxiv.org/abs/2301.13188) |

### 17.6 Federated, generative, and agentic systems

| ID | Reference |
|---|---|
| R-70 | McMahan, H. B., Moore, E., Ramage, D., et al. *Communication-Efficient Learning of Deep Networks from Decentralized Data.* arXiv:1602.05629, 2016. [arXiv](https://arxiv.org/abs/1602.05629) |
| R-71 | Bagdasaryan, E., Veit, A., Hua, Y., et al. *How To Backdoor Federated Learning.* arXiv:1807.00459, 2018. [arXiv](https://arxiv.org/abs/1807.00459) |
| R-72 | Blanchard, P., El Mhamdi, E. M., Guerraoui, R., & Stainer, J. *Machine Learning with Adversaries: Byzantine Tolerant Gradient Descent (Krum).* NeurIPS 2017. (Venue citation.) |
| R-73 | Yin, D., Chen, Y., Ramchandran, K., & Bartlett, P. *Byzantine-Robust Distributed Learning: Towards Optimal Statistical Rates.* arXiv:1803.01498, 2018. [arXiv](https://arxiv.org/abs/1803.01498) |
| R-74 | Bonawitz, K., Ivanov, V., Kreuter, B., et al. *Practical Secure Aggregation for Privacy-Preserving Machine Learning.* ACM CCS 2017. DOI [10.1145/3133956.3133982](https://doi.org/10.1145/3133956.3133982) |
| R-80 | Greshake, K., Abdelnabi, S., Mishra, S., et al. *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection.* arXiv:2302.12173, 2023. [arXiv](https://arxiv.org/abs/2302.12173) |
| R-81 | Zou, A., Wang, Z., Carlini, N., et al. *Universal and Transferable Adversarial Attacks on Aligned Language Models.* arXiv:2307.15043, 2023. [arXiv](https://arxiv.org/abs/2307.15043) |
| R-82 | Wei, A., Haghtalab, N., & Steinhardt, J. *Jailbroken: How Does LLM Safety Training Fail?* arXiv:2307.02483, 2023. [arXiv](https://arxiv.org/abs/2307.02483) |
| R-83 | Carlini, N., Nasr, M., Choquette-Choo, C. A., et al. *Are aligned neural networks adversarially aligned?* arXiv:2306.15447, 2023. [arXiv](https://arxiv.org/abs/2306.15447) |
| R-84 | Wallace, E., Xiao, K., Leike, R., et al. *The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions.* arXiv:2404.13208, 2024. [arXiv](https://arxiv.org/abs/2404.13208) |
| R-85 | Debenedetti, E., Zhang, J., Balunović, M., et al. *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents.* arXiv:2406.13352, 2024. [arXiv](https://arxiv.org/abs/2406.13352) |
| R-86 | Debenedetti, E., Shumailov, I., Fan, T., et al. *Defeating Prompt Injections by Design (CaMeL).* arXiv:2503.18813, 2025. [arXiv](https://arxiv.org/abs/2503.18813) |

### 17.7 Research practice, reproducibility, and evaluation

| ID | Reference |
|---|---|
| R-100 | Pineau, J., Vincent-Lamarre, P., Sinha, K., et al. *Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program).* arXiv:2003.12206, 2020; JMLR 22(164), 2021. [arXiv](https://arxiv.org/abs/2003.12206) |
| R-101 | Kapoor, S., & Narayanan, A. *Leakage and the Reproducibility Crisis in ML-based Science.* arXiv:2207.07048, 2022. [arXiv](https://arxiv.org/abs/2207.07048) |
| R-102 | Ganguli, D., Hernandez, D., Lovitt, L., et al. *Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned.* arXiv:2209.07858, 2022. [arXiv](https://arxiv.org/abs/2209.07858) |
| R-103 | Brundage, M., Avin, S., Clark, J., et al. *The Malicious Use of Artificial Intelligence: Forecasting, Prevention, and Mitigation.* arXiv:1802.07228, 2018. [arXiv](https://arxiv.org/abs/1802.07228) |
| R-104 | Brundage, M., Avin, S., Wang, J., et al. *Toward Trustworthy AI Development: Mechanisms for Supporting Verifiable Claims.* arXiv:2004.07213, 2020. [arXiv](https://arxiv.org/abs/2004.07213) |
| R-105 | Ganguli, D., Hernandez, D., Lovitt, L., et al. *Predictability and Surprise in Large Generative Models.* arXiv:2202.07785, 2022. [arXiv](https://arxiv.org/abs/2202.07785) |

---

## 18. Proposed repository and site structure

The tree below reflects the repository as built through Level 5. Directories marked *(planned)* do not exist yet, and empty placeholders remain disallowed.

```
MLSec/
├─ README.md                      # student entry point
├─ mkdocs.yml                     # site config, nav, not_in_nav
├─ docs/                          # learner-facing site source
│  ├─ index.md
│  ├─ student-guide.md
│  ├─ references.md
│  ├─ maintainer-guide.md         # not in nav
│  ├─ course-blueprint.md         # planning (not in nav)
│  ├─ module-map.md               # planning (not in nav)
│  ├─ lab-catalog.md              # planning (not in nav)
│  ├─ project-catalog.md          # planning (not in nav)
│  ├─ learning-outcomes.md        # planning (not in nav)
│  ├─ implementation-roadmap.md   # planning (not in nav)
│  ├─ modules/
│  │  ├─ index.md
│  │  ├─ m00-orientation/         # published
│  │  ├─ m01-python-refresher/    # published
│  │  ├─ m02-ml-fundamentals/     # published
│  │  ├─ m03-threat-modeling/     # published
│  │  ├─ m04-evasion/             # published
│  │  ├─ m05-poisoning/           # published
│  │  ├─ m06-backdoors/           # published
│  │  ├─ m07-extraction-privacy/  # published
│  │  ├─ m08-robustness-defense/  # published
│  │  ├─ m09-data-integrity/      # published
│  │  ├─ m10-supply-chain/        # published
│  │  ├─ m11-serving-monitoring/  # published
│  │  ├─ m12-federated-learning/  # published
│  │  ├─ m13-privacy-preserving-ml/ # published
│  │  ├─ m14-explainability-fairness/ # published
│  │  ├─ m15-genai-llm-agents/    # published
│  │  ├─ m16-end-to-end-assessment/ # published
│  │  ├─ m17-red-team-blue-team/  # published
│  │  └─ m18-capstone-and-research/ # published
│  ├─ labs/
│  │  ├─ index.md
│  │  └─ lab-01.md … lab-20.md    # one brief per built lab
│  └─ projects/
│     ├─ index.md                 # student project catalog
│     ├─ prj-01-fraud-detection.md … prj-06-robustness-comparison.md
│     ├─ rt-01-red-blue.md
│     ├─ capstone.md
│     └─ evaluator-guide.md       # not in nav
├─ labs/                          # runnable code, not published as pages
│  ├─ shared/
│  │  ├─ mlsec_labs/{__init__.py, artifacts.py, data.py, environment.py}
│  │  └─ requirements-level1.txt
│  ├─ lab-01-environment/
│  ├─ lab-01b-evaluation-audit/
│  ├─ lab-02-threat-model/
│  ├─ lab-03-evasion-magnitude/
│  ├─ lab-04-targeted-transfer/
│  ├─ lab-05-label-poisoning/
│  ├─ lab-06-targeted-poisoning/
│  ├─ lab-07-tabular-backdoor/
│  ├─ lab-08-image-backdoor-detection/
│  ├─ lab-09-model-extraction/
│  ├─ lab-10-membership-inference/
│  ├─ lab-11-defense-evaluation/
│  ├─ lab-12-dataset-validation/
│  ├─ lab-13-supply-chain-audit/
│  ├─ lab-14-secure-serving/
│  ├─ lab-15-monitoring-incident/
│  ├─ lab-16-federated-learning/
│  ├─ lab-17-privacy-budget/
│  ├─ lab-18-explanation-fairness/
│  ├─ lab-19-rag-boundary/
│  └─ lab-20-agent-containment/
├─ maintainers/                   # planned; owner-only operations docs
└─ .github/workflows/             # planned; owner-enabled CI/Pages (see §18.2)
```

### 18.1 Site decisions

| Decision | Choice | Rationale |
|---|---|---|
| Generator | MkDocs + Material | Markdown-native, fast search, admonitions, offline build, no Node required |
| Pages deployment | GitHub Actions artifact | `docs/` Markdown is not a Jekyll site; Actions gives reproducible builds |
| Planning docs | `docs/*.md` with `not_in_nav` | Honours the requested paths without cluttering learner navigation |
| Maintainer docs | `maintainers/` (outside `docs/`) | Keeps deployment/ops out of student content |
| Search | Client-side (Material) | No third-party service or data leakage |
| Analytics | None by default | Learner privacy; revisit with consent |
| Code execution | Local / Colab | Static site cannot run notebooks; labs are downloaded from `labs/` |
| Solutions | Not published in nav | Assessment integrity; lab solutions and the project evaluator guide are excluded |

### 18.2 CI outline

1. `ci.yml` — on pull request: `mkdocs build --strict`, markdown lint, link check (internal + external with allowlist), spell check on changed files, YAML validation.
2. `pages.yml` — on push to `main`: build with pinned Python, upload artifact, deploy via `actions/deploy-pages` with least-privilege permissions.
3. `labs.yml` — weekly/manual: CPU smoke tests for LAB-01, LAB-03, LAB-11, LAB-14 in a container; no secrets; time-boxed.

The repository currently has `mkdocs.yml` but no workflows and no Pages deployment. Enabling Pages (source: GitHub Actions) is an **owner action** that this project cannot and must not perform automatically.

---

## 19. Content quality bar (definition of done)

A lesson is publishable only when all of the following hold:

- [ ] It states 2–4 measurable objectives aligned to a LO ID.
- [ ] Every claim about an attack or defense has a citation (framework, paper, or documented tool behavior) or a reproduced result.
- [ ] Code runs from a clean environment with pinned dependencies; outputs are shown.
- [ ] The threat model (goal, knowledge, capability, budget, metric) is explicit.
- [ ] Limitations and failure modes are stated; no "solved" claims.
- [ ] At least one knowledge-check item targets a common misconception.
- [ ] Safety, legality, and data-handling notes are present where relevant.
- [ ] Links resolve; images have alt text; no color-only encoding.
- [ ] A second reviewer (ML or security) has checked technical accuracy.
- [ ] The page is linked from the module map and nav (or intentionally excluded).

For labs, add: reproducible artifact, checksum/manifest, runtime estimate, CPU fallback, and rubric mapping.

---

## 20. Risks and open decisions

| Risk / decision | Impact | Mitigation / owner |
|---|---|---|
| GitHub Pages not enabled (site returns 404) | Cannot verify deployment | Owner enables Pages → GitHub Actions; verify after Phase 1 |
| No license selected | Cannot safely publish/reuse | Owner chooses content (e.g., CC BY-SA) and code (e.g., Apache-2.0) licenses |
| Framework drift (ATLAS monthly, OWASP 2026, NIST updates) | Content becomes stale | Pin versions in a "frameworks as of" note; quarterly review |
| Dataset access changes (Kaggle, CICIDS, Purchase-100) | Labs break | Every lab needs a fallback dataset and a download check |
| Compute limits | Slow labs, drop-off | CPU-first design, subsets, Colab alternatives, time boxes |
| Offensive content misuse | Ethical/legal harm | Sandbox-only targets, authorized-use statement, no production tooling |
| Breadth vs depth (276 h) | Learners stall | Tracks, explicit minimum paths, cap at 21 lab documents (84 lab hours) plus one 11-hour project |
| Solution leakage | Assessment integrity | Solutions excluded from nav; policy TBD |
| AI-generated content errors | Credibility | Citation checks, reproduction, two-reviewer rule |
| Maintenance burden | Rot | Shared lab package, CI smoke tests, deprecation policy |
| Accessibility/i18n | Exclusion | Alt text, contrast, plain language; translation is out of scope for v1 |
| Instructor bio details absent | Incomplete about page | Add only instructor-supplied facts; no invention |

**Open decisions for the owner:** licenses; whether solutions are public; whether to offer a cohort/certificate; hosting of large artifacts; analytics; localization; official contact channel.

---

## 21. Change log

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-10-28 | Initial design baseline: 18 modules, 21 labs, 4 mini-projects, 6 capstones, 30 outcomes, references verified |
| 0.2 | 2026-10-28 | Level 1 implemented: M00–M03 published (17 lessons), LAB-01/LAB-01B/LAB-02 built; blueprint at that time planned 22 labs / 116 lab hours in ≈265 h |
| 0.3 | 2026-10-28 | Level 2 implemented: M04–M07 published (M04 5, M05 4, M06 4, M07 5 lessons), LAB-03…LAB-10 built and checker-verified; structure recast as 15 modules + capstone (78 lessons) with 20 lab documents (LAB-01…LAB-19 plus LAB-01B, 96 lab hours) and 242 h total (202 guided + 40 capstone); outcomes, lab catalog, module map, assessment weights, datasets, tools, quizzes and mini-projects renumbered to match |
| 0.4 | 2026-10-28 | Level 3 implemented: M08–M11 published (M08 6, M09 5, M10 4, M11 6 lessons) and LAB-11…LAB-15 built and checker-verified. M08 recast around defense evaluation (adversarial training, preprocessing, adaptive attacks) with LO-18 re-scoped from certified smoothing; M09 recast as data integrity and governance with LO-20 re-scoped; M10 reduced to 10 h and M11 widened to 16 h to include monitoring and incident response; privacy/DP and its outcome LO-19 moved to planned M12/LAB-16. Stage totals and tracks updated (Practitioner M00–M11 ≈ 148 h); challenge, mini-project, dataset, and tool mappings realigned. Lab hours unchanged at 96 |
| 0.5 | 2026-10-28 | Level 4 implemented: M12–M15 published in the requested order — federated learning (M12, 14 h), privacy-preserving ML (M13, 12 h), explainability/fairness (M14, 10 h), and generative AI/RAG/agents (M15, 18 h) — with 20 lessons, LAB-16…LAB-20 built and checker-verified, and new outcomes LO-31/LO-32 for explanation stability and fairness trade-offs. Course now has 76 lessons, 21 lab documents (20 numbered labs plus LAB-01B), 16 quizzes, 4 mini-projects, 32 outcomes, and 242 h; lab time is 84 h. Added RAG-boundary and agent-containment labs, OWASP LLM/agent and MITRE ATLAS mappings, and a 97 h LLM/agent specialization track |
| 0.6 | 2026-10-28 | Level 5 implemented: M16 (end-to-end assessment, 16 h), M17 (red/blue simulation, 14 h), and M18 (capstone and research, 4 h + 40 h capstone) published with 12 lessons, QZ-16…QZ-18, 12 exercises, six 11-hour project briefs (PRJ-01…PRJ-06), RT-01 (9 h), and a capstone brief with milestones M0–M5 and a 100-point rubric. Added outcomes LO-33 (integrated assessment), LO-34 (red/blue), and LO-35 (research question); PLO-7; project and evaluator catalogs; and the 236 guided hours. Total is now 276 h (236 + 40), 88 lessons, 19 quizzes, 75 exercises, 21 labs, and 35 outcomes |

---

*End of blueprint. Companion documents: [module-map.md](module-map.md), [lab-catalog.md](lab-catalog.md), [learning-outcomes.md](learning-outcomes.md), [implementation-roadmap.md](implementation-roadmap.md).*
