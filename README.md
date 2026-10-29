# Machine Learning Security (ML-Sec)

**A self-study, lab-driven course on how machine-learning systems fail under adversarial pressure — and how to measure, defend, and engineer against that failure.**

ML-Sec is written for people studying without a lecturer in the room. Every module is designed to give you a scenario worth caring about, a self-contained explanation, a runnable lab, a knowledge check, and an artifact you can defend to another engineer.

> **Course status (2026-10-28).** **Levels 1–5 are published and runnable**: M00–M18 (88 lessons, nineteen knowledge checks, 75 exercises), LAB-01, LAB-01B, and LAB-02–LAB-20 with starter code, reference solutions, and independent checkers, plus six applied project briefs, a red-team/blue-team exercise, and the 40-hour capstone brief with its rubric. The public site has not been deployed. Start with [Module 00](docs/modules/m00-orientation/index.md), the [student guide](docs/student-guide.md), or the [project catalog](docs/projects/index.md).

---

## 1. Course overview and purpose

Most machine-learning curricula teach models to be accurate. Most security curricula teach networks and applications to be resilient. Neither, on its own, prepares you for systems where the **data distribution is an attack surface**, the **model is an artifact that can be stolen or trojaned**, and the **prediction API is both the product and an oracle**.

ML-Sec closes that gap with one discipline:

> **Model the adversary, measure the effect, engineer the control, and re-test.**

You will not merely read that an attack exists. You will implement it against a local baseline, measure how much accuracy it removes at a stated budget, apply a defense, try to defeat your own defense, and write a report that another person can reproduce.

The course is framework-anchored but implementation-first. [NIST AI 100-2e2025](https://doi.org/10.6028/NIST.AI.100-2e2025) supplies the vocabulary, [MITRE ATLAS](https://atlas.mitre.org/) supplies adversary tactics and techniques, the [NIST AI Risk Management Framework](https://doi.org/10.6028/NIST.AI.100-1) supplies governance structure, and [OWASP](https://genai.owasp.org/) supplies application-facing risk lists. None of these substitutes for running code and measuring outcomes.

**What makes this course different**

- **Threat model before technique.** Every attack starts with an attacker goal, knowledge, capability, access, and success metric.
- **Reproduce, break, defend, re-break.** Static defenses are hypotheses, not conclusions.
- **Measure, don't assert.** "Robust" is not an adjective; it is a curve with a budget, seeds, and uncertainty.
- **Assume an adaptive adversary.** Obfuscated gradients and broken evaluations are a recurring theme.
- **CPU-first.** Core labs are designed for a laptop; a GPU is an optimization, not a requirement.
- **Portfolio over proctored exams.** In self-study there is no credible invigilation. The defensible signal is a reproducible artifact plus an auditable analysis.

---

## 2. Who should take the course

| If you are… | Start at | Your first meaningful artifact |
|---|---|---|
| A beginner with some Python and little ML | M00 → M01 → M02 → M03 | LAB-01 baseline, LAB-01B audit, and LAB-02 threat model |
| An ML practitioner new to security | M00, skim M02, then M03 | LAB-02 threat model plus LAB-03 evasion study |
| A security practitioner new to ML | M00, M01, M02 | LAB-01 baseline, LAB-01B audit, and LAB-02 threat model |
| An ML engineer focused on integrity | M03 → M05 → M06 | LAB-06 targeted poisoning and LAB-08 backdoor dossier |
| An ML platform or MLOps engineer | M03 → M08 → M10 → M11 | LAB-11 robustness audit, LAB-13 supply-chain gate, and LAB-14 hardened API |
| A privacy or platform engineer | M03 → M07 → M13 | LAB-09 extraction curve, LAB-10 membership analysis, and LAB-17 privacy budget |
| A GenAI engineer targeting LLM and agent risk | M00–M03, M07, M11, then M15 | LAB-19 RAG trust-boundary report plus LAB-20 agent containment report, then PRJ-05 |
| A learner ready for an end-to-end assessment | M03 and M16, with M17 for red/blue work | One project dossier from PRJ-01…PRJ-06 or RT-01, then the capstone |
| An instructor or curriculum designer | The planning documents | A complete module slice or project you can teach or adapt |

**This course is probably not for you if** you want a proctored certification, a ready-made offensive toolkit, or a shortcut to attacking systems you do not own. Offensive work here is confined to local, synthetic, or public sandbox targets.

You do **not** need a GPU, a paid cloud account, or a mathematics degree. You do need patience with debugging and a willingness to write down what you measured.

---

## 3. What you will be able to do

The program has seven measurable outcomes. The full catalog of 35 outcomes, success standards, and assessment mappings is in [Learning outcomes](docs/learning-outcomes.md).

| ID | Outcome |
|---|---|
| PLO-1 | **Foundations** — Explain ML system architecture, lifecycle, trust boundaries, and adversarial threat models using recognized frameworks. |
| PLO-2 | **Attack analysis** — Implement and evaluate evasion, poisoning, backdoor, extraction, inference, and inversion attacks under explicit budgets. |
| PLO-3 | **Robustness engineering** — Select, implement, and critically evaluate defenses, including adaptive-attack evaluation and certification. |
| PLO-4 | **Secure engineering** — Harden data pipelines, model artifacts, serving infrastructure, and monitoring/response for ML systems. |
| PLO-5 | **Frontier systems** — Assess and mitigate risks in federated, generative, and agentic AI systems. |
| PLO-6 | **Professional practice** — Communicate findings with reproducible evidence, correct severity, lawful conduct, and responsible disclosure. |
| PLO-7 | **Integrated assessment** — Plan, execute, and defend an authorized end-to-end assessment, including red-team/blue-team simulation, costed remediation, and residual risk. |

Each outcome is assessed by an artifact, not by a page you have read: a lab deliverable, a project dossier, or the capstone. Reading is preparation; evidence is the product.

---

## 4. Prerequisites and a beginner-friendly recovery path

### Baseline

| Area | Minimum | Self-check before you start |
|---|---|---|
| Python | Functions, classes, virtual environments, NumPy arrays | Load a CSV, train a scikit-learn classifier, and plot a confusion matrix without copying a full tutorial |
| ML | Train/test splits, loss, overfitting, precision/recall, ROC-AUC | Explain why 99% accuracy can be useless on imbalanced data |
| Math | Gradients, chain rule, basic probability, norms | Differentiate cross-entropy for a linear layer; explain an L-infinity ball in plain language |
| Tooling | Terminal, Git basics, Jupyter | Clone a repository, create a virtual environment, and run a notebook end to end |
| Security | CIA triad, authentication versus authorization | Explain the difference between a vulnerability and an exploit |

### If you are not there yet: a four-week recovery path

You do **not** need to finish this before reading Module 0. Use it alongside the early modules, and repeat it whenever a lab exposes a gap.

| Week | Focus | Do this | Done when |
|---|---|---|---|
| 1 | Python and NumPy | Write a small script that loads a CSV, splits it, trains a classifier, and prints a confusion matrix. Rewrite one step as a function; move it behind a virtual environment. | You can run your script from a clean shell without a tutorial open. |
| 2 | ML fundamentals | Train the same classifier with a deliberate train/test leak, then fix it. Compare accuracy, precision, recall, F1, and ROC-AUC on an imbalanced split. | You can explain which metric you would monitor and why. |
| 3 | Calculus and probability | Derive the gradient of cross-entropy for a linear layer on paper. Implement one gradient-descent step by hand in NumPy. | You can state what a gradient points toward and what an L-infinity budget constrains. |
| 4 | Tooling and security vocabulary | Create a Git repository, commit a notebook, and write a one-page threat description of a simple login system using confidentiality, integrity, and availability. | You can distinguish a vulnerability, an exploit, and a risk in one sentence each. |

A short diagnostic starts Module 01. Until you reach it, use the self-checks above. If fewer than four of the five baseline rows feel comfortable, take the recovery path seriously rather than skipping ahead.

---

## 5. Tools and installation overview

The course is CPU-first and built around free, open-source tools.

| Layer | Tools | Notes |
|---|---|---|
| Language and environment | Python 3.11–3.14, a virtual environment, `pip` or `uv` | Pin exact versions in a per-lab requirements file; never install into a global environment. Levels 1–5 were verified on Python 3.14.7 |
| Core ML (Levels 1–4) | NumPy, pandas, scikit-learn, joblib, PyYAML | CPU-only and fully offline: LAB-01, LAB-03…LAB-11, and LAB-16 use scikit-learn's bundled digits dataset; LAB-01B, LAB-06, LAB-12, LAB-17, and LAB-18 generate synthetic data; LAB-19 and LAB-20 use local mock corpora and tools |
| Applied projects (Level 5) | The same NumPy, pandas, and scikit-learn stack; Python standard library for mock APIs and services | Projects reuse lab components and add orchestration, reporting, and checkers. No project requires a GPU, paid service, API key, or third-party target |
| Serving and monitoring (M11) | Python standard library, `http.server`, `hmac`, `json`, `logging` | LAB-14 and LAB-15 use no web framework and bind to loopback only; every requirement is already in the shared Level 1 file |
| Supply-chain inspection (M10) | `pickletools`, `hashlib`, `hmac`, `json`, plain files | LAB-13 inspects a benign pickle statically and signs a manifest with a local key; no scanner or registry is installed |
| Discussed, not installed | PyTorch, AutoAttack, RobustBench, ModelScan, safetensors, Sigstore/cosign, CycloneDX, FastAPI, Docker, Trivy | The lessons explain where these tools fit and what they do not prove. No published lab requires them, so the course stays installable offline |
| Discussed, not installed (Level 4) | diffprivlib or Opacus, Flower, LIME/SHAP, garak, PyRIT, promptfoo, NeMo Guardrails or LLM Guard, AgentDojo | M12–M15 explain where these fit and what they do not prove; the published labs implement the same ideas in NumPy and scikit-learn so they stay installable offline |

**Hardware.** An 8 GB laptop is the reference floor. Tier A labs target ten minutes or less per run on CPU; Tier B labs ship a reduced CPU configuration; Tier C labs are optional GPU work. Everything published so far runs offline after `pip install`.

Do not build a large environment up front. Each lab ships its own requirements. The full setup walkthrough, verification checklist, and workspace layout are in the [student guide](docs/student-guide.md#setup).

---

## 6. Course roadmap: beginner to advanced

The course is 18 modules plus a capstone, arranged in six stages. Each module below links to its roadmap entry, which states prerequisites, effort, labs, and outcomes. The full dependency graph and lesson inventory are in the [module map](docs/module-map.md).

### Stage 1 — Foundations (M00–M03)

*What are we protecting, from whom, and how do we describe it?*

| Module | What it covers | Hours | Lab |
|---|---|---:|---|
| [M00 Orientation and Study System](docs/modules/index.md#m00) | Course map, lab setup, evidence habits, rules of engagement | 4 | LAB-01 |
| [M01 Python, NumPy, pandas, and scikit-learn Refresher](docs/modules/index.md#m01) | Validation, arrays and dtypes, pandas joins, leak-free pipelines, reproducibility | 12 | LAB-01 |
| [M02 Machine Learning Fundamentals and Evaluation](docs/modules/index.md#m02) | Problem framing, loss and gradients, metrics, calibration, leakage, reporting | 12 | LAB-01B |
| [M03 Cybersecurity Fundamentals and ML Threat Modeling](docs/modules/index.md#m03) | CIA and privacy, boundaries, NIST AI 100-2e2025, ATLAS, AI RMF, OWASP, risk scoring | 11 | LAB-02 |

### Stage 2 — Core attacks (M04–M07)

*How are predictions, training data, behavior, and privacy attacked?*

| Module | What it covers | Hours | Lab / project |
|---|---|---:|---|
| [M04 Adversarial Examples and Evasion Attacks](docs/modules/index.md#m04) | Lp budgets, FGSM, PGD, restarts, targeted attacks, transfer, honest ASR | 14 | LAB-03, LAB-04 |
| [M05 Training Data Poisoning and Label Manipulation](docs/modules/index.md#m05) | Data supply chain, label-flip curves, targeted poisoning, screening and its costs | 13 | LAB-05, LAB-06 |
| [M06 Backdoor Attacks, Trojan Models, and Trigger-Based Behavior](docs/modules/index.md#m06) | Triggers, poison budget, clean accuracy versus ASR, trigger search, mitigation | 14 | LAB-07, LAB-08, MP-01 |
| [M07 Model Extraction, Membership Inference, and Model Inversion](docs/modules/index.md#m07) | API oracles, fidelity versus accuracy, low-FPR membership metrics, inversion, governance | 14 | LAB-09, LAB-10, MP-03 |

### Stage 3 — Defenses and data integrity (M08–M09)

*Does the defense survive an adaptive attack, and can we trust the data we train on?*

| Module | What it covers | Hours | Lab / project |
|---|---|---:|---|
| [M08 Robustness Evaluation and Adversarial Defense](docs/modules/index.md#m08) | Clean versus robust accuracy, PGD adversarial training, input preprocessing, gradient masking, adaptive attacks, standardized evaluation, scoped reporting | 16 | LAB-11, MP-02 |
| [M09 Data Integrity, Dataset Governance, and Secure Training Pipelines](docs/modules/index.md#m09) | Provenance and lineage, validation rules, label defects, grouped splits, leakage ablations, reproducible runs, dataset governance | 12 | LAB-12 |

### Stage 4 — Secure engineering and operations (M10–M11)

*How do we build, ship, and operate ML systems securely?*

| Module | What it covers | Hours | Lab |
|---|---|---:|---|
| [M10 Model Serialization, Dependencies, and ML Supply-Chain Security](docs/modules/index.md#m10) | Pickle opcode risk, static inspection, safe formats, pinning and hashing, lock files, signing, SBOM, fail-closed promotion | 10 | LAB-13 |
| [M11 Secure Model Serving, API Security, Monitoring, and Incident Response](docs/modules/index.md#m11) | Trust boundaries, authentication and authorization, request bounds, validation, safe output, rate limits, drift and attack indicators, incident response, secrets | 16 | LAB-14, LAB-15 |

### Stage 5 — Privacy and frontier systems (M12–M15)

*What changes with federation, privacy guarantees, explanations, generative models, and agents?*

| Module | What it covers | Hours | Lab / project |
|---|---|---:|---|
| [M12 Federated Learning Security and Distributed ML Threats](docs/modules/index.md#m12) | Federated architecture, client poisoning and backdoors, update scaling, robust aggregation, clipping, monitoring, secure aggregation, Sybil risk | 14 | LAB-16 |
| [M13 Privacy-Preserving Machine Learning](docs/modules/index.md#m13) | Privacy threat models, ε-DP and sensitivity, Laplace and Gaussian mechanisms, composition, DP-SGD, secure computation, privacy–utility evaluation | 12 | LAB-17, MP-03 |
| [M14 Explainability, Fairness, and Security Trade-offs](docs/modules/index.md#m14) | Explanation methods and assumptions, fidelity and stability, explanation leakage and manipulation, subgroup metrics, intervals, audit reporting | 10 | LAB-18 |
| [M15 Generative AI, LLM, RAG, and AI Agent Security](docs/modules/index.md#m15) | Prompt injection and instruction hierarchy, retrieval provenance, sensitive data and output handling, agent authority and tools, layered defense and taxonomies | 18 | LAB-19, LAB-20, MP-04 |

### Stage 6 — Applied projects and synthesis (M16–M18 + CAP)

*Can you run an end-to-end assessment, red-team a system under rules of engagement, and defend the result?*

| Module | What it covers | Hours | Project |
|---|---|---:|---|
| [M16 End-to-End ML Security Assessment](docs/modules/index.md#m16) | Scoping, data classification, threat model to test plan, measurement, attack and defense, costed reporting | 16 | One of PRJ-01…PRJ-06 |
| [M17 ML Red-Team and Blue-Team Simulation](docs/modules/index.md#m17) | Rules of engagement, attack planning under budgets, telemetry and detection calibration, purple-team synthesis, adaptive retest | 14 | RT-01 |
| [M18 Capstone Projects and Research Extensions](docs/modules/index.md#m18) | Scoping, milestones and reproducibility, results and limitations, turning a project into a research question | 4 | CAP-A to CAP-F |
| [CAP Capstone](docs/projects/capstone.md) | End-to-end assessment with adaptive evaluation, reproduction package, and briefing | 40 | CAP-A to CAP-F |

The six applied project briefs are in the [project catalog](docs/projects/index.md). Each is an 11-hour dossier that reuses two or three labs; RT-01 is the 9-hour red/blue exercise.

**Practical guidance.** Stages are sequential for beginners. Experienced learners may enter at Stage 2 or Stage 5, but the capstone assumes the vocabulary from Stages 1–4. M04 requires M02; learners who skip M03 tend to produce attacks without a defensible threat model.

---

## 7. How to study each module

Every module follows the same anatomy:

> **Scenario → objectives → lessons → lab → quiz → reflection → artifact**

For each lesson, use the six-step protocol:

| Step | What you do | Typical time |
|---|---|---|
| 1. Scenario | Read the failure story and name the asset at risk | 10 min |
| 2. Objectives | Turn "I will read about X" into "I will be able to do Y" | 5 min |
| 3. Concept | Read one explanation and restate it in your own words | 30–45 min |
| 4. Guided practice | Run the example, then change one variable and predict the effect | 30–60 min |
| 5. Check | Answer the quiz items before revealing explanations | 15 min |
| 6. Artifact | Finish the lab deliverable and write a five-line reflection | 1–3 h |

A sustainable week looks like this:

| Block | Time | Activity |
|---|---:|---|
| Preview | 20 min | Skim objectives, lab deliverable, and quiz topics; write three questions |
| Read | 60–90 min | One lesson at a time, with notes in your own words |
| Practice | 60–120 min | Run the worked example and alter one parameter |
| Lab | 2–4 h | Complete the artifact and commit it locally |
| Retrieve | 20 min | Closed-book quiz; re-derive the key equation or attack loop |
| Reflect | 15 min | Update the study log; schedule review at 1, 3, 7, and 21 days |

Do not re-read passively. Retrieve: re-derive the attack step, restate the difference between poisoning and a backdoor, or sketch a threat model from memory. The full protocol, including spaced review and a study-log template, is in the [student guide](docs/student-guide.md#study-loop).

---

## 8. Labs, deliverables, and self-assessment

The course has **21 lab documents totaling 84 hours**, all built and runnable. They are the core of the course; the reading exists to make the labs intelligible.

| Tier | Meaning | Typical runtime |
|---|---|---|
| A | Laptop CPU | 10 minutes or less per run |
| B | CPU 30–60 minutes, or free Colab | Reduced CPU configuration shipped |
| C | GPU recommended | Optional; never required for completion |

Every lab produces the same artifact anatomy:

- code that runs top to bottom;
- a `README.md` or `report.md` stating the threat model, results, and limitations;
- a pinned environment file;
- an artifact manifest with hashes;
- a five-line reflection.

You score your own work against the standard rubric before looking at any reference solution:

| Dimension | Weight | What strong work looks like |
|---|---:|---|
| Technical correctness | 30 | The attack or defense runs as specified and the metrics are computed correctly |
| Security reasoning | 25 | Explicit threat model, budgets, assumptions, and limitations |
| Experimental method | 20 | Controlled comparisons, multiple seeds, ablations, uncertainty |
| Reproducibility | 15 | Pinned environment, seeds, commands, and a manifest; reproduces from a clean checkout |
| Communication and ethics | 10 | Concise report, correct severity, safety and legal constraints addressed |

**Self-assessment protocol**

1. Attempt the lab without a reference solution.
2. Score your artifact against the rubric *before* comparing notes.
3. Write five lines: what worked, what failed, what you would test next, what you misunderstood, what evidence is missing.
4. If a claim cannot be reproduced from a clean environment, it is not complete.
5. Keep the artifact in a portfolio folder; the capstone reuses it.

**Current status.** LAB-01, LAB-01B, and LAB-02–LAB-20 ship starter code, a reference solution, pinned requirements, and an independent checker. Reference solutions stay out of student navigation; each lab's checker lets you verify your own artifact. A passing checker confirms structure and expected ranges, not that a defense is secure. The sequence, prerequisites, and time tiers are in the [lab guide](docs/labs/index.md); the full design briefs are in the [lab catalog](docs/lab-catalog.md).

### Applied projects and the capstone

Level 5 does not add more labs. It adds six project briefs of about 11 hours and a 9-hour red/blue exercise, each combining existing labs into one assessment. A project produces a scope statement, architecture and data classification, threat model and risk register, a falsifiable test plan, a baseline table, bounded attack and defense experiments, costed remediation, residual risk, and a reproduction package. The [project catalog](docs/projects/index.md) explains the six options and their lab reuse; the [capstone brief](docs/projects/capstone.md) defines the 40-hour integrated assessment, milestones M0–M5, and the rubric.

Projects are assessed with a 100-point rubric: scope and system understanding 10, threat model 15, baseline and experimental design 15, attack or analysis correctness 20, defense design and evaluation 15, reproducibility and evidence 10, risk communication 10, and ethics and limitations 5. The red/blue exercise uses the same scale with red execution and blue detection weighted separately. An evaluator's reference is kept out of student navigation.

To run a built lab:

```bash
cd labs/lab-03-evasion-magnitude
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab03.py --artifacts artifacts
```

---

## 9. Estimated workload and suggested schedules

Total effort is approximately **276 hours**: 236 hours of guided modules, projects, and the red/blue exercise, plus a 40-hour capstone. Module hours include reading, exercises, the quiz, and the lab or project.

| Track | Modules | Effort | Typical duration |
|---|---|---:|---|
| Foundations | M00–M03 | 39 h | 4–7 weeks |
| Core attacks | M00–M07 | 94 h | 10–16 weeks |
| Practitioner | M00–M11 | 148 h | 15–25 weeks |
| Applied assessment specialization | M00–M03, M16–M18 + one project + CAP | 113 h | 12–19 weeks |
| Full program plus capstone | M00–M18 + CAP | 276 h | 28–46 weeks |
| GenAI and agent specialization | M00–M03, M15 + CAP | 97 h | 10–16 weeks |

| Pace | Foundations | Core attacks | Practitioner | Full program | Assessment specialization | GenAI specialization |
|---|---:|---:|---:|---:|---:|---:|
| 6 h/week | 7 weeks | 16 weeks | 25 weeks | 46 weeks | 19 weeks | 17 weeks |
| 8 h/week | 5 weeks | 12 weeks | 19 weeks | 35 weeks | 15 weeks | 13 weeks |
| 10 h/week | 4 weeks | 10 weeks | 15 weeks | 28 weeks | 12 weeks | 10 weeks |
| 15 h/week | 3 weeks | 7 weeks | 10 weeks | 19 weeks | 8 weeks | 7 weeks |

These are honest estimates for a learner who completes the labs and one project, not for someone skimming the reading. At 10 hours per week, allow 28–30 calendar weeks for the full program once review and slippage are included. A week-by-week plan is in the [student guide](docs/student-guide.md#schedules).

**A note on pace.** Consistency beats intensity. Two focused hours four times a week is more effective than a ten-hour weekend session, because the labs require debugging and reflection rather than passive reading.

---

## 10. Projects, red/blue exercise, and capstone

### Applied projects (11 hours each)

Level 5 offers six project briefs. Choose one; each reuses two or three labs and ends with an auditable dossier and a 100-point rubric. All use fictional organizations and local, synthetic data.

| ID | Organization and system | Core question | Reuses |
|---|---|---|---|
| PRJ-01 | Meridian Pay — card-not-present fraud scoring | Can data-quality faults and bounded feature changes move fraud decisions without breaking the dashboard? | LAB-03, LAB-05, LAB-12 |
| PRJ-02 | Aster Manufacturing — visual defect classification | Can a small poisoned or backdoored fraction survive a realistic pipeline and a screening defense? | LAB-05, LAB-06, LAB-07, LAB-08 |
| PRJ-03 | Helio Health — benefits triage API | What does the prediction interface leak under a fixed query budget, and what does output minimization cost? | LAB-09, LAB-10, LAB-17 |
| PRJ-04 | Cobalt Models — training and artifact pipeline | Do validation, dependency, signing, and reproducibility controls actually fail closed? | LAB-12, LAB-13 |
| PRJ-05 | Harbor — policy assistant with retrieval and tools | Does the application treat untrusted documents as data, and does the agent enforce authority in code? | LAB-19, LAB-20 |
| PRJ-06 | Sentinel Vision — access-badge classifier | Which defense gives the best robustness per unit of clean accuracy, false positives, and runtime? | LAB-03, LAB-11 |

### Red-team/blue-team exercise (9 hours)

RT-01 runs a bounded campaign against Pinewood Logistics' local dispatch-risk service. You first write a one-page rules-of-engagement statement and threat model, then execute attacks A-01…A-07 within fixed budgets, then build detections D-01…D-07 and calibrate them on a quiet baseline, and finally test whether each mitigation survives an adaptive variant. Red and blue evidence are scored separately.

### Mini-projects (8 hours each)

Mini-projects are optional stretch work for the Foundations, Core-attacks, and Defenses tracks and recommended for the Practitioner track. Choose any two.

| ID | Title | After | Core question |
|---|---|---|---|
| MP-01 | Integrity red-team | M05–M06 | Can you poison and backdoor a controlled model within a fixed budget, then detect it and report the residual risk? |
| MP-02 | Robustness audit | M08 | Is the claimed robustness real under an adaptive attack, and what did it cost in clean accuracy? |
| MP-03 | Privacy and extraction assessment | M07, M13 | What does a prediction API leak, at what query or false-positive budget, and what would you change? |
| MP-04 | GenAI and agent red-team | M15 | Which layered defenses survive an adaptive prompt-injection campaign? |

### Capstone (40 hours)

The capstone is a single end-to-end security assessment, published as a brief with milestones M0–M5, a 100-point rubric, and a required reproduction package. You choose one of six options:

| ID | Option | Artifact |
|---|---|---|
| CAP-A | Risk assessment of a public ML service (local replica) | Threat model, red-team results, prioritized controls, report |
| CAP-B | Replication and critique of a robustness benchmark | Reproduced subset, adaptive-attack challenge, methodological critique |
| CAP-C | Privacy attack and DP defense study | MIA and inversion pipeline, DP-SGD comparison, accounting, harm analysis |
| CAP-D | Secure ML supply-chain blueprint | Signed artifacts, SBOM/ML-BOM, CI gates, registry policy, demo |
| CAP-E | Agentic AI security evaluation harness | Test suite, attack scenarios, defense evaluation, disclosure plan |
| CAP-F | Federated learning threat model and robust aggregation study | FL simulation, attacks, robust aggregation and DP, residual-risk report |

Every capstone must include an **authorized-use statement** naming the systems tested (local, synthetic, or public sandbox only), a **reproducibility package**, and a **limitations** section. CAP-A and CAP-E must not target third-party production systems.

Module assessments together carry 70% of the notional score (knowledge checks 10%, labs and applied projects 40%, mini-projects 20%); the capstone carries 30%. The plan defines a self-study completion record at 80% overall with a proficient project, a proficient capstone, and a signed ethics statement. **No certificate is issued at this stage**, and no formal credit or accreditation is implied.

---

## 11. Responsible use and lab safety

The techniques in this course are published research. Learning them is legitimate. Using them against systems you do not own is not.

- **Authorized targets only.** Labs use local processes, local containers, synthetic services, or explicitly public sandbox datasets. Attacking third-party systems is prohibited.
- **No real personal data.** Privacy labs use public benchmarks or synthetic records. Do not attempt to identify individuals.
- **No real-model extraction.** Extraction labs query a model you trained yourself behind a local mock API; do not probe a commercial service.
- **Contain offensive code.** Artifact and agent labs run in a disposable container or VM with no host credentials and no network egress unless the lab requires it.
- **Responsible disclosure.** If you find a real vulnerability in a public model or library, report it privately to the maintainer, allow reasonable remediation time, and do not publish an exploit before a fix.
- **Law and policy.** Follow applicable law, institutional policy, and terms of service. This course does not provide legal advice, and cross-border rules differ.
- **Harm minimization.** Do not generate targeted disinformation, impersonation, or content harmful to real people, even as an exercise.

> If you are unsure whether a target is authorized, it is not. Stop and ask.

The full policy, including the AI-assistant rules and the authorized-use statement required for the capstone, is in the [student guide](docs/student-guide.md#safety).

---

## 12. Troubleshooting and FAQ

| Symptom | Likely cause | First fix |
|---|---|---|
| `ModuleNotFoundError` | Wrong environment | Activate the lab virtual environment and reinstall from its pinned file |
| `torch` install is huge or slow | Default CUDA wheels | Install the CPU-only wheel index instead |
| CUDA error or no GPU | Driver and wheel mismatch | Use the CPU requirements and set the device explicitly to CPU |
| Dataset download fails | Network or proxy | Use the bundled-dataset lab path, or download manually and verify the checksum |
| Results differ between runs | Non-determinism | Set seeds, enable deterministic algorithms, set `num_workers=0` |
| Attack "succeeds" at zero perturbation | Metric or label bug | Check the perturbation norm and confirm predictions actually changed |
| Zero attack success | Underpowered attack or gradient masking | Increase steps and restarts; try a gradient-free attack |
| Checker says "does not reproduce" | Different split, seed, or model settings | Use the exact protocol in the lab README |
| Server returns `401` for a demo token | Missing or malformed `Authorization` header | Send `Authorization: Bearer <token>`; confirm the token belongs to the role you intended |
| Every request returns `429` | The fixed-window limiter is exhausted for that role | Wait for the window to reset; the lab uses 10 requests per 60 seconds per role |
| Artifact gate rejects an unchanged file | Hash covers different bytes than you expect | Recompute the digest over the exact file the manifest names; do not hash a directory listing |
| Notebook behaves inconsistently | Out-of-order execution | Restart the kernel and run all cells |

**FAQ**

**Do I need a GPU?** No. Tier A labs run on a laptop CPU. Tier B labs ship reduced configurations. GPU is optional.

**Is there a certificate?** Not at this stage. The design includes a self-study completion record, but no certificate is issued and no accreditation is implied.

**Are solutions available?** Built labs ship reference solutions inside their own folders, outside student navigation. The owner has not set a public solutions policy.

**Can I use an AI assistant?** Yes, for explanations, debugging, code review, and test suggestions. Disclose material assistance and never submit analysis you cannot defend line by line. Do not paste private data into a third-party assistant.

**Can I skip modules?** Yes, via the entry paths in section 2. The capstone still assumes foundational vocabulary.

**Does this work on Windows?** Yes. Levels 1–5 were verified on Windows 10, CPU only. A few container labs are easier under WSL2, and legacy path-length limits can affect deep virtual environments.

**Why do labs use digits instead of CIFAR-10 or MNIST?** scikit-learn's digits dataset ships with the package, so the labs run offline, deterministically, and in seconds on a laptop. LAB-12 and LAB-15 generate their own synthetic data, and LAB-14 binds a server to loopback with no external service. The lessons state what each choice does and does not establish.

The complete troubleshooting protocol and a longer FAQ are in the [student guide](docs/student-guide.md#troubleshooting).

---

## 13. Curated references and further learning

Start with the frameworks; they define the vocabulary the course uses. Versions are dated because they change faster than courses.

| Reference | Why it matters |
|---|---|
| [NIST AI 100-2e2025](https://doi.org/10.6028/NIST.AI.100-2e2025) | Adversarial ML taxonomy: goals, knowledge, capabilities, attack classes |
| [MITRE ATLAS](https://atlas.mitre.org/) | Adversary tactics and techniques, with case studies |
| [NIST AI RMF 1.0](https://doi.org/10.6028/NIST.AI.100-1) and [Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1) | Governance structure and generative-AI risk |
| [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) | Application-facing LLM risks |
| [OWASP Machine Learning Security Top 10](https://owasp.org/projects/machine-learning-security-top-ten) | ML-specific application risks |
| [OWASP API Security Top 10 (2023)](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) | Serving and API risk taxonomy used in M11 |
| [NIST SP 800-61r3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | Incident-response lifecycle used in LAB-15 |
| [CISA and UK NCSC secure AI guidelines](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development) | Secure development across the AI lifecycle |
| [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html) and [ISO/IEC 23894:2023](https://www.iso.org/standard/77304.html) | AI management systems and risk guidance |

**Foundational reading**

- Biggio and Roli, *Wild Patterns: Ten Years After the Rise of Adversarial Machine Learning* — [arXiv:1712.03141](https://arxiv.org/abs/1712.03141)
- Szegedy et al., *Intriguing properties of neural networks* — [arXiv:1312.6199](https://arxiv.org/abs/1312.6199)
- Goodfellow, Shlens, and Szegedy, *Explaining and Harnessing Adversarial Examples* — [arXiv:1412.6572](https://arxiv.org/abs/1412.6572)
- Madry et al., *Towards Deep Learning Models Resistant to Adversarial Attacks* — [arXiv:1706.06083](https://arxiv.org/abs/1706.06083)
- Carlini and Wagner, *Towards Evaluating the Robustness of Neural Networks* — [arXiv:1608.04644](https://arxiv.org/abs/1608.04644)
- Biggio, Nelson, and Laskov, *Poisoning Attacks against Support Vector Machines* — [arXiv:1206.6389](https://arxiv.org/abs/1206.6389)
- Gu, Dolan-Gavitt, and Garg, *BadNets* — [arXiv:1708.06733](https://arxiv.org/abs/1708.06733)
- Tramèr et al., *Stealing Machine Learning Models via Prediction APIs* — [arXiv:1609.02943](https://arxiv.org/abs/1609.02943)
- Shokri et al., *Membership Inference Attacks against Machine Learning Models* — [arXiv:1610.05820](https://arxiv.org/abs/1610.05820)
- Greshake et al., *Indirect Prompt Injection* — [arXiv:2302.12173](https://arxiv.org/abs/2302.12173)

**Benchmarks and evaluation resources**

- [RobustBench](https://robustbench.github.io/) for standardized robustness comparison
- [BackdoorBench](https://github.com/SCLBD/BackdoorBench) and [TrojAI](https://www.trojandetection.ai/) for backdoor evaluation
- [HarmBench](https://www.harmbench.org/) and [JailbreakBench](https://jailbreakbench.github.io/) for LLM safety evaluation
- [AgentDojo](https://github.com/ethz-spylab/agentdojo) for agent prompt-injection evaluation

The annotated, category-organized list — including evasion, poisoning, extraction, privacy, federated, and agentic literature — is in [References](docs/references.md). All links were checked on 2026-10-28. Publisher sites may block automated checks while resolving normally in a browser.

---

## 14. Instructor

**Engr. Dr. Muhammad Nadeem Majeed**
Professor
Department of Data Science (PUCIT)
University of the Punjab, Lahore

Dr. Majeed is the author and instructor of record for ML-Sec.

---

## 15. Contact and contribution

**Contact.** No public contact address has been supplied for this course, so none is published here. To report an error, propose a correction, or ask a course question, open an issue in the [repository](https://github.com/nadeem-majeedch/MLSec). A dedicated contact address will be added only if the instructor supplies and verifies one.

**Contribution.** Levels 1–5 are implemented; the capstone brief and rubric are published, but no learner work is included. Licenses for content and code, the solutions policy, and the contribution workflow are still owner decisions. Until those are settled, please do not send large content contributions. Small corrections and reproducibility reports are welcome as issues. Maintainers should read the [maintainer guide](docs/maintainer-guide.md).

**Do not include** personal data, credentials, or details of an unpatched vulnerability in a public issue. For a security report, contact the repository owner privately through the channel they publish; if none is published, do not disclose publicly.

---

## Repository map

| Path | Purpose |
|---|---|
| [docs/index.md](docs/index.md) | Student landing page for the published site |
| [docs/student-guide.md](docs/student-guide.md) | Full self-study guide: setup, workflow, labs, assessment, troubleshooting |
| [docs/modules/index.md](docs/modules/index.md) | Course roadmap with every module, prerequisite, and lab |
| [docs/labs/index.md](docs/labs/index.md) | Lab system, tiers, sequence, and deliverables |
| [docs/projects/index.md](docs/projects/index.md) | Six applied projects, RT-01, and the capstone route |
| [docs/projects/capstone.md](docs/projects/capstone.md) | Capstone requirements, milestones, rubric, and research extension |
| [docs/assessments/index.md](docs/assessments/index.md) | Diagnostic, module quizzes, level checks, final, question bank, rubrics, progress record |
| [assessments/answer-keys/](assessments/answer-keys/) | Answer keys and scoring notes; kept outside the published site |
| [labs/](labs/README.md) | Runnable lab packages: starter, solution, checker, expected metrics |
| [scripts/validate_labs.py](scripts/validate_labs.py) · [check_links.py](scripts/check_links.py) · [validate_assessments.py](scripts/validate_assessments.py) | Structural lab, link, and assessment validation |
| [tests/test_validation.py](tests/test_validation.py) | Unit tests for the validation tooling |
| [requirements/](requirements/README.md) | Supported interpreter and pinned install path |
| [datasets/](datasets/README.md) | Data policy and per-lab dataset registry |
| [docs/references.md](docs/references.md) | Annotated references by topic |
| [docs/course-blueprint.md](docs/course-blueprint.md) | Master design document |
| [docs/module-map.md](docs/module-map.md) | Lesson inventory and dependency graph |
| [docs/lab-catalog.md](docs/lab-catalog.md) | Full lab briefs |
| [docs/project-catalog.md](docs/project-catalog.md) | Project briefs, reuse map, and evaluator policy |
| [docs/learning-outcomes.md](docs/learning-outcomes.md) | 35 outcomes and assessment mapping |
| [docs/implementation-roadmap.md](docs/implementation-roadmap.md) | Build plan and milestones |
| [docs/maintainer-guide.md](docs/maintainer-guide.md) | Build, QA, and release process |
| [docs/projects/evaluator-guide.md](docs/projects/evaluator-guide.md) | Evaluator reference; excluded from student navigation |
| [mkdocs.yml](mkdocs.yml) | Site configuration for local builds |

The course is built in vertical slices: a module is published only when its lessons, lab, quiz, and artifact are complete. No page in this repository is an empty placeholder.
