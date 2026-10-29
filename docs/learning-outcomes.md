# ML-Sec Learning Outcomes and Assessment Mapping

| Field | Value |
|---|---|
| Document | Measurable outcomes, success criteria, and assessment map |
| Version | 0.7 (assessment layer mapped) |
| Date | 2026-10-28 |
| Status | **All 35 outcomes LO-01–LO-35 have published assessments.** The six projects, RT-01, and the capstone brief with its rubric are published; the self-assessment layer (DIA-01, QZ-00B–QZ-18B, QB-01, LC-1–LC-5, FIN-01) is published and mapped below. Learner work is not included |
| Companion documents | [Course blueprint](course-blueprint.md) · [Module map](module-map.md) · [Lab catalog](lab-catalog.md) · [Project catalog](project-catalog.md) · [Implementation roadmap](implementation-roadmap.md) |

## 1. How outcomes are written

Each outcome uses an observable verb, names the condition (dataset, budget, tool), and states the standard for acceptable performance. An outcome is only "assessed" if a learner artifact provides direct evidence; reading a page is not evidence.

**Bloom levels used:** 1 Remember · 2 Understand · 3 Apply · 4 Analyze · 5 Evaluate · 6 Create.

**Evidence types:** `QZ` knowledge check · `QZB` alternate module quiz · `DIA` prerequisite diagnostic · `QB` tagged question bank · `LC` level check · `FIN` integrated final · `LAB` lab artifact · `MP` mini-project · `PRJ` applied project · `RT` red/blue exercise · `CAP` capstone.

`QZB`, `DIA`, `QB`, `LC`, and `FIN` are **self-assessment instruments**. They show whether a learner can recognize, interpret, and reason about a decision; they do not replace a lab, project, or capstone artifact as evidence that the learner can execute or defend the work.

## 2. Program-level outcomes

| ID | Statement |
|---|---|
| PLO-1 | **Foundations** — Explain ML system architecture, lifecycle, trust boundaries, and adversarial threat models using recognized frameworks. |
| PLO-2 | **Attack analysis** — Implement and evaluate evasion, poisoning, backdoor, extraction, inference, and inversion attacks under explicit budgets. |
| PLO-3 | **Robustness engineering** — Select, implement, and critically evaluate defenses under adaptive attack, distinguishing empirical robustness from certified guarantees. |
| PLO-4 | **Secure engineering** — Harden data pipelines, model artifacts, serving infrastructure, and monitoring/response for ML systems. |
| PLO-5 | **Frontier systems** — Assess and mitigate risks in federated, private, explainable, generative, and agentic AI systems. |
| PLO-6 | **Professional practice** — Communicate findings with reproducible evidence, correct severity, lawful conduct, and responsible disclosure. |
| PLO-7 | **Integrated assessment** — Plan, execute, and defend an authorized end-to-end assessment of an ML system, including red-team/blue-team simulation, costed remediation, and residual risk. |

## 3. Outcome catalog

### 3.1 Foundations and threat modeling

| ID | Outcome | Bloom | Modules | Primary evidence | Success standard |
|---|---|---:|---|---|---|
| LO-01 | Draw an ML system's lifecycle and identify at least five trust boundaries and attack surfaces, justifying each with a concrete failure scenario. | 3 | M01, M02 | LAB-01, LAB-02 | Five boundaries, each with asset, adversary, and consequence |
| LO-02 | Classify a described attack by adversary goal, knowledge, and capability using NIST AI 100-2e2025 terminology. | 3 | M03 | QZ-03, LAB-02 | ≥ 90% agreement with the model answer on 8 scenarios |
| LO-03 | Produce a prioritized threat model that maps at least eight threats to MITRE ATLAS techniques and AI RMF functions and proposes testable controls. | 6 | M03 | LAB-02 | Eight mapped threats; top five scored; each control has a test |
| LO-04 | Select controls using least privilege and defense in depth, and justify residual risk for a given ML service. | 5 | M03, M11 | QZ-03, LAB-14, LAB-15 | Controls are specific; residual risk is stated and owned |

### 3.2 Adversarial examples and evasion

| ID | Outcome | Bloom | Modules | Primary evidence | Success standard |
|---|---|---:|---|---|---|
| LO-05 | Implement FGSM, PGD, and a targeted gradient attack on a local classifier, achieving ASR within 10 percentage points of the reference at the same budget. | 3 | M04 | LAB-03, LAB-04 | Same ε, steps, restarts, and clipping; result within tolerance |
| LO-06 | Execute a transfer attack against a black-box model at three or more perturbation budgets and report source and target success separately. | 3 | M04 | LAB-04 | Identical perturbed inputs; target never differentiated; three budgets reported |
| LO-07 | Assess when an evasion result does and does not generalize to a deployed system, including physical, query, and distribution constraints. | 4–5 | M04 | LAB-04, MP-02 | Constraints named; claim scoped; at least one alternative explanation considered |

### 3.3 Poisoning and backdoors

| ID | Outcome | Bloom | Modules | Primary evidence | Success standard |
|---|---|---:|---|---|---|
| LO-08 | Design and execute a poisoning attack at a controlled rate and report targeted and global effects separately. | 3 | M05 | LAB-05, LAB-06 | Poison denominator explicit; at least five rates or both effects reported |
| LO-09 | Evaluate a data-screening or robust-training defense with catches, false positives, threshold sensitivity, and an explicit trust assumption. | 5 | M05 | LAB-06, MP-01 | Catches and false positives counted; threshold justified; assumption stated |
| LO-10 | Construct a backdoor at a controlled poison rate and report clean accuracy, ASR, and false-trigger rate separately. | 3 | M06 | LAB-07, MP-01 | All three metrics reported; poison budget counted |
| LO-11 | Perform a trigger search on a locally trained model, interpret the anomaly score, and evaluate a mitigation with false positives and an adaptive-attacker caveat. | 4–5 | M06 | LAB-08, MP-01 | Best position identified; score compared with baseline; flagged rows and poisons caught reported |

### 3.4 Extraction and privacy

| ID | Outcome | Bloom | Modules | Primary evidence | Success standard |
|---|---|---:|---|---|---|
| LO-12 | Classify extraction, membership inference, and inversion by attacker goal, required access, and metric, and explain what a prediction API reveals beyond a label. | 2 | M07 | QZ-07, LAB-09, LAB-10 | ≥ 90% agreement on 8 scenarios; information ladder explained |
| LO-13 | Measure extraction fidelity and task accuracy across at least three query budgets, explain cold start, and state what high fidelity does not prove. | 3–4 | M07 | LAB-09, MP-03 | Three budgets; fidelity defined against the teacher; local target only |
| LO-14 | Execute membership inference, report TPR at FPR ≤ 1% and ≤ 5%, compare with a baseline, and explain why a confidence gap is not proof of membership. | 4–5 | M07 | LAB-10, MP-03 | Low-FPR metrics reported; baseline included; explicit not-proof argument |
| LO-15 | Explain model inversion and attribute inference, perform one local demonstration, and assess harm under an ethical constraint. | 4 | M07 | MP-03, LAB-10 (supporting) | Metric appropriate; no real personal data; harm stated; representative vs record distinguished |

### 3.5 Robustness, data integrity, and governance

| ID | Outcome | Bloom | Modules | Primary evidence | Success standard |
|---|---|---:|---|---|---|
| LO-16 | Evaluate robustness with an adaptive attack and identify at least one invalid-evaluation pitfall in a published or self-produced claim. | 5 | M08 | LAB-11, MP-02 | Adaptive attack attempted; pitfall supported by evidence |
| LO-17 | Train an adversarially robust model and quantify the clean-accuracy cost at a stated threat model. | 3 | M08 | LAB-11, MP-02 | Both clean and robust accuracy reported with budget |
| LO-18 | Evaluate an input-processing or detection defense with a static and an adaptive attack, reporting bypass rate, false positives, and the conditions under which the defense fails. | 4–5 | M08 | LAB-11, MP-02 | Static and adaptive results compared; false positives reported; passing one test is not called proof |
| LO-20 | Build a dataset validation pipeline and justify governance controls — provenance, lineage, access, versioning, and audit — by measured defect catches, false positives, and stated trust assumptions. | 5 | M09 | LAB-12 | Planted defects found with counts; false positives measured; assumptions and audit trail documented |

### 3.6 Secure engineering and operations

| ID | Outcome | Bloom | Modules | Primary evidence | Success standard |
|---|---|---:|---|---|---|
| LO-21 | Harden an ML supply chain with scanning, safe serialization, signing, and an SBOM, and verify each control. | 3 | M10 | LAB-13 | Negative test fails the gate; signature verified; SBOM has hashes |
| LO-22 | Threat-model and harden a serving API; demonstrate that authentication, quota, and validation controls work. | 3 | M11 | LAB-14 | Tests for bypass, malformed input, and quota exhaustion pass |
| LO-23 | Design detections for two ML attack scenarios and write an incident-response playbook with rollback and evidence handling. | 6 | M11 | LAB-15 | Detections mapped to techniques; playbook has owners and time bounds |

### 3.7 Distributed, private, explainable, generative, and agentic systems

| ID | Outcome | Bloom | Modules | Primary evidence | Success standard |
|---|---|---:|---|---|---|
| LO-19 | Construct a differentially private release, report ε, δ, sensitivity, and composition, and distinguish the formal guarantee from an empirical leakage signal. | 5 | M13 | LAB-17, MP-03 | All accounting inputs reported; claim auditable; empirical result not called a proof |
| LO-24 | Attack a federated training run and evaluate two defenses under equal rounds, stating residual risk. | 5 | M12 | LAB-16 | Clean accuracy and attack success reported; aggregation assumptions scoped |
| LO-25 | Assess an LLM application against OWASP Top 10 for LLM Applications 2025, MITRE ATLAS, and NIST AI 100-2e2025, mapping at least five risks. | 4 | M15 | LAB-19 | Mappings accurate; at least one risk ruled out with reasoning |
| LO-26 | Evaluate a RAG application's trust boundary with a canary and an indirect injection, and test layered defenses including false positives on benign documents. | 5 | M15 | LAB-19, MP-04 | Success metric defined; benign evaluation included; data-versus-authority behavior shown |
| LO-27 | Threat-model an agentic system, enforce capability and approval constraints in code, and evaluate residual risk with an action log. | 6 | M15 | LAB-20, MP-04 | Controls enforced in code; sandbox evidence; residual risk stated |
| LO-31 | Compare explanation methods and quantify explanation stability under controlled input changes, stating what stability does and does not establish. | 4 | M14 | LAB-18 | At least two methods compared; stability measured; limits stated |
| LO-32 | Measure subgroup performance and at least two fairness metrics, and explain the trade-offs among fairness, robustness, privacy, and explanation. | 5 | M14 | LAB-18 | Subgroup confidence intervals reported; metric conflict explained |

### 3.8 Professional practice

| ID | Outcome | Bloom | Modules | Primary evidence | Success standard |
|---|---|---:|---|---|---|
| LO-28 | Communicate findings in an auditable report with reproducible artifacts, stated budgets, and limitations. | 5 | All | LAB-01…LAB-20, CAP | Another learner can reproduce the headline result |
| LO-29 | Apply authorized-use, data-ethics, and disclosure rules, and sign and follow an ethics statement. | 3 | M00, M15, All | Ethics statement, CAP | Targets authorized; no personal data; disclosure considered |
| LO-30 | Integrate security controls into lifecycle governance using AI RMF, SSDF, and ISO/IEC 42001 concepts. | 5 | M03, M09, M10, M11, M13, CAP | CAP (LAB-02, LAB-12, LAB-13, LAB-14, LAB-17 supporting) | Controls mapped to framework functions with evidence |

### 3.9 Applied assessment and research

| ID | Outcome | Bloom | Modules | Primary evidence | Success standard |
|---|---|---:|---|---|---|
| LO-33 | Plan and execute an end-to-end assessment of one ML system: scope, architecture, data classification, threat model, falsifiable test plan, baseline, bounded attack and defense experiments, costed remediation, and residual risk. | 6 | M16, M18 | One of PRJ-01…PRJ-06; CAP | Every test traces to a risk-register entry; all rubric dimensions at least Proficient; reproduction package runs from a clean checkout |
| LO-34 | Conduct a red-team/blue-team exercise under written rules of engagement: produce a testable attack plan, capture attributable evidence, calibrate detections, and evaluate mitigations against an adaptive variant. | 6 | M17 | RT-01 | Scope and non-goals explicit; every attack within budget; every detection has a measured false-positive cost; adaptive retest reported |
| LO-35 | Convert a completed assessment into a bounded research question with a gap statement, claim–evidence table, controls or ablations, and a pre-registration-style analysis plan. | 6 | M18 | CAP (research extension), PRJ (suggested extension) | Question passes the six tests; every claim has a planned comparison; scope and ethics are stated |

## 4. Assessment map

`P` = primary evidence, `s` = supporting evidence, blank = not assessed.

| LO | QZ | LAB | MP | CAP |
|---|---|---|---|---|
| LO-01 | QZ-01 | LAB-01, LAB-01B, LAB-02 (P) | | P |
| LO-02 | QZ-03 (P) | LAB-02 (s) | | s |
| LO-03 | QZ-03 (s) | LAB-02 (P) | | P |
| LO-04 | QZ-03 (P), QZ-11 (s) | LAB-02 (s), LAB-14 (s), LAB-15 (s) | | P |
| LO-05 | QZ-04 | LAB-03, LAB-04 (P) | | s |
| LO-06 | QZ-04 | LAB-04 (P) | | P |
| LO-07 | QZ-04 | LAB-04 (s) | MP-02 (s) | s |
| LO-08 | QZ-05 | LAB-05 (P), LAB-06 (s) | MP-01 (s) | s |
| LO-09 | QZ-05 | LAB-06 (P) | MP-01 (P) | s |
| LO-10 | QZ-06 | LAB-07 (P) | MP-01 (s) | s |
| LO-11 | QZ-06 | LAB-08 (P) | MP-01 (P) | P |
| LO-12 | QZ-07 | LAB-09, LAB-10 (s) | | s |
| LO-13 | QZ-07 | LAB-09 (P) | MP-03 (s) | s |
| LO-14 | QZ-07 | LAB-10 (P) | MP-03 (s) | P |
| LO-15 | QZ-07 | LAB-10 (s) | MP-03 (P) | s |
| LO-16 | QZ-08 | LAB-11 (P) | MP-02 (P) | P |
| LO-17 | QZ-08 | LAB-11 (P) | MP-02 (s) | s |
| LO-18 | QZ-08 | LAB-11 (P) | MP-02 (s) | s |
| LO-19 | QZ-13 | LAB-17 (P) | MP-03 (P) | P |
| LO-20 | QZ-09 | LAB-12 (P) | | P |
| LO-21 | QZ-10 | LAB-13 (P) | | P |
| LO-22 | QZ-11 | LAB-14 (P) | | P |
| LO-23 | QZ-11 | LAB-15 (P) | | P |
| LO-24 | QZ-12 | LAB-16 (P) | | P (CAP-F) |
| LO-25 | QZ-15 | LAB-19 (P) | MP-04 (s) | s |
| LO-26 | QZ-15 | LAB-19 (P) | MP-04 (P) | P (CAP-E) |
| LO-27 | QZ-15 | LAB-20 (P) | MP-04 (P) | P (CAP-E) |
| LO-28 | | All labs (P) | All MPs (P) | P |
| LO-29 | QZ-00 | LAB-01 (s) | All (s) | P |
| LO-30 | QZ-03, QZ-09, QZ-10, QZ-11, QZ-13 | LAB-02, LAB-12, LAB-13, LAB-14, LAB-17 (s) | | P |
| LO-31 | QZ-14 | LAB-18 (P) | | P |
| LO-32 | QZ-14 | LAB-18 (P) | | P |

### 4.1 Level 5 assessment map

Level 5 evidence is separate because projects combine several labs and cannot be assigned to a single module.

| LO | QZ | Project or exercise | CAP |
|---|---|---|---|
| LO-33 | QZ-16 | PRJ-01…PRJ-06 (P, one required) | P |
| LO-34 | QZ-17 | RT-01 (P) | s |
| LO-35 | QZ-18 | PRJ extension (s) | P |

A completed project also supplies supporting evidence for the LOs whose labs it reuses; the project rubric records which. For example, PRJ-03 reuses LAB-09, LAB-10, and LAB-17, so it supports LO-13, LO-14, and LO-19 without replacing their lab evidence.

### 4.2 Coverage checks

- Every module M00–M18 contributes to at least one LO.
- Every numbered lab LAB-01–LAB-20 is the primary evidence for at least one LO. LAB-01B supports LO-01 and LO-28.
- Every LO has at least one primary evidence source other than a quiz.
- Terminal outcomes (LO-16, LO-27, LO-28, LO-30, LO-33, LO-34, LO-35) are assessed in the capstone or a Level 5 project.
- Published now: LO-01–LO-35. The six project options and RT-01 provide primary evidence for LO-33 and LO-34; the capstone is the primary evidence for LO-35 and for the integrated version of LO-33.

### 4.3 Self-assessment coverage

The alternate quizzes, diagnostic, bank, level checks, and final assessment sample the outcomes below. A `Y` means at least one keyed item in that instrument carries the outcome tag; a number is the module quiz (`04B` = QZ-04B) or level check.

| LO | Quiz B | Level check | Final | Bank | Diagnostic |
|---|---|---|---|---|---|
| LO-01 | 00B, 01B, 02B | LC-1 | — | Y | Y |
| LO-02 | 03B | LC-1 | Y | Y | Y |
| LO-03 | 03B | LC-1 | Y | Y | — |
| LO-04 | 03B | LC-1 | — | Y | Y |
| LO-05 | 04B | LC-2 | Y | Y | Y |
| LO-06 | 04B | LC-2 | — | Y | — |
| LO-07 | 04B | — | — | Y | — |
| LO-08 | 05B | LC-2 | Y | Y | — |
| LO-09 | 05B | — | — | Y | — |
| LO-10 | 06B | LC-2 | Y | Y | — |
| LO-11 | 06B | LC-2 | — | — | — |
| LO-12 | 07B | — | — | Y | — |
| LO-13 | 07B | LC-2 | Y | Y | — |
| LO-14 | 07B | LC-2 | Y | Y | — |
| LO-15 | 07B | — | — | Y | — |
| LO-16 | 08B | LC-3 | Y | Y | — |
| LO-17 | 08B | LC-3 | Y | Y | — |
| LO-18 | 08B | LC-3 | Y | Y | — |
| LO-19 | 13B | LC-4 | Y | Y | — |
| LO-20 | 09B | LC-3 | — | Y | — |
| LO-21 | 10B | LC-3 | Y | Y | — |
| LO-22 | 11B | LC-3 | Y | Y | — |
| LO-23 | 11B | LC-3 | Y | Y | — |
| LO-24 | 12B | LC-4 | Y | Y | — |
| LO-25 | 15B | — | — | — | — |
| LO-26 | 15B | LC-4 | Y | Y | — |
| LO-27 | 15B | LC-4 | Y | Y | — |
| LO-28 | 00B, 01B, 02B | LC-5 | Y | — | — |
| LO-29 | 00B | LC-1, LC-5 | — | Y | Y |
| LO-30 | — | — | — | Y | — |
| LO-31 | 14B | LC-4 | — | Y | — |
| LO-32 | 14B | LC-4 | Y | Y | — |
| LO-33 | 16B | LC-5 | Y | Y | — |
| LO-34 | 17B | LC-5 | Y | Y | — |
| LO-35 | 18B | LC-5 | — | Y | — |

**Reading the table.** Every module has an alternate quiz, and every level has a check. Coverage is deliberately uneven: a 10-item level check cannot sample every outcome in its level, and the final assessment is a 25-item sample, not an exhaustive examination. Three consequences matter:

- LO-25 (OWASP LLM mapping) and LO-30 (lifecycle governance using AI RMF, SSDF, and ISO/IEC 42001) are sampled by only one self-assessment instrument each. Their primary evidence remains LAB-19 and LAB-02, LAB-12, LAB-13, LAB-14, and LAB-17 respectively.
- LO-11 (trigger search) is sampled by QZ-06B and LC-2 only; LAB-08 remains the evidence that the learner can perform it.
- A missing entry is not a claim that the outcome cannot be assessed. It means this particular instrument does not sample it. See the [assessment catalog](assessments/index.md) for the full set.

## 5. Competency levels

| Level | Definition | Evidence required |
|---|---|---|
| **Aware** | Can explain concepts and recognize attacks; can run guided labs. | M00–M03; LAB-01, LAB-01B, LAB-02; QZ ≥ 80% |
| **Practitioner** | Can execute and evaluate attacks/defenses with correct budgets and metrics. | Aware + M04–M11; LAB-03…LAB-15 (13 labs); two of MP-01, MP-02, MP-03 |
| **Specialist** | Can design assessments, handle frontier systems, and defend conclusions under adaptive pressure. | Practitioner + M12–M16; LAB-16–LAB-20; MP-04; one of PRJ-01…PRJ-06 or RT-01; CAP ≥ Proficient |
| **Researcher** | Can critique and extend the literature, design novel evaluations, and produce publishable artifacts. | Specialist + M18; a research-style capstone (CAP-B or CAP-E) with a methodological contribution and external review |

These levels describe capability, not accreditation. No university credit, professional certification, or license is conferred.

## 6. What counts as acceptable evidence

**Acceptable**
- A notebook that runs end-to-end from a clean environment, with seeds and versions.
- Metrics defined in code and reported with the denominator and budget.
- A threat model with explicit assumptions and a rejected alternative.
- A negative result that is correctly measured and explained.
- A mitigation evaluated against an adaptive attempt.

**Not acceptable**
- Screenshots without the code that produced them.
- "Robust" or "secure" without a stated adversary, budget, and metric.
- Results copied from a tutorial without independent execution.
- ASR reported without defining the base set.
- Claims that a defense works because one attack failed.
- Any test against a system the learner does not own or have written permission to test.

## 7. Constructive alignment notes

| Design choice | Alignment |
|---|---|
| Every module has a lab artifact | Outcomes require execution, not recall |
| Quizzes include "find the flaw" items | Targets analysis/evaluation, not just definitions |
| Mini-projects choose two of four | Allows specialization while preserving coverage |
| Every project requires a traceability matrix | Prevents technique-first work with no risk owner |
| RT-01 separates red and blue evidence | Tests both attack execution and defensible detection |
| Capstone requires adaptive evaluation and a clean-checkout run | Prevents "defense demo" projects that never test failure |
| Rubric rewards limitations and negative results | Rewards honesty over impressive-sounding claims |
| LO-35 requires a gap statement and controls | Distinguishes a research question from a topic summary |
| Ethics statement is required for completion | Operationalizes LO-29 |
| Every module has an alternate quiz | Gives a second form without reusing Quiz A items |
| Level checks sample each level cumulatively | Catches cross-module gaps before the next level |
| Half of the final assessment score is scenario work | Tests judgment and design, not recall |
| Answer keys are separate from every student page | Allows attempt-first without leaking answers into the build |
| The sampler withholds feedback until submission | Keeps the practice interaction attempt-first, with source-level limits disclosed |

## 8. Revision policy

Outcomes are versioned with the course. A change to an outcome requires: a rationale, a check that every mapped assessment still provides evidence, and an update to the module map and lab catalog. Framework version changes (ATLAS, OWASP, NIST) do not automatically change outcomes; they change the references and examples used to assess them.
