# Framework mapping

This page connects the course to the public vocabularies that security teams, auditors, and researchers actually use. It answers a practical question: when you write up a finding from LAB-06, which NIST attack class and which MITRE ATLAS technique are you describing?

The mapping is a translation aid, not a claim of coverage. See [what this mapping does not mean](#what-this-mapping-does-not-mean) before you reuse any row in an assessment.

!!! warning "No compliance or certification claim"
    Completing this course, a lab, a project, or the capstone does **not** certify compliance with NIST AI 100-2, the NIST AI Risk Management Framework, MITRE ATLAS, any OWASP publication, ISO/IEC 42001 or 23894, the EU AI Act, or any other standard. The course teaches concepts and evidence habits that overlap with those documents. Compliance is a property of an organization's system and its audit record, established by qualified assessors against the current official text. Nothing here is legal advice.

## Editions used on this page

Framework identifiers change between releases, and two editions of the same OWASP list can number the same risk differently. Every mapping below names the edition it was checked against on **2026-10-28**.

| Vocabulary | Edition used here | Where it is introduced |
|---|---|---|
| NIST adversarial ML taxonomy | NIST AI 100-2 E2025, March 2025 ([F-01](references.md#frameworks-standards-and-guidance)) | [M03.2](modules/m03-threat-modeling/lesson-2-adversaries-and-taxonomy.md) |
| MITRE ATLAS | Data release v2026.09, modified 2026-09-15 ([F-02](references.md#frameworks-standards-and-guidance)) | [M03.3](modules/m03-threat-modeling/lesson-3-surfaces-lifecycle-atlas.md) |
| OWASP Top 10 for LLM Applications | **2025** edition for taught IDs; 2026 edition crosswalked below ([F-07, F-07A](references.md#frameworks-standards-and-guidance)) | [M15.1](modules/m15-genai-llm-agents/lesson-1-from-predictive-ml-to-llm-security.md) |
| OWASP API Security Top 10 | 2023 edition ([F-18](references.md#frameworks-standards-and-guidance)) | [M11.2](modules/m11-serving-monitoring/lesson-2-authentication-and-authorization.md) |
| NIST AI RMF | AI 100-1, January 2023, with the Generative AI Profile AI 600-1, July 2024 ([F-03, F-04](references.md#frameworks-standards-and-guidance)) | [M03.4](modules/m03-threat-modeling/lesson-4-frameworks-and-crosswalks.md) |
| NIST SSDF | SP 800-218 v1.1 plus SP 800-218A ([F-05, F-06](references.md#frameworks-standards-and-guidance)) | [M09.4](modules/m09-data-integrity/lesson-4-reproducible-training.md), [M10.4](modules/m10-supply-chain/lesson-4-provenance-signing-and-promotion.md) |

**Coverage legend.** ● practised in a lab with a measured artifact · ◐ discussed and applied in a lesson exercise · ○ out of scope for this course.

## 1. NIST AI 100-2 E2025 attack classes

NIST organizes adversarial ML by the **impact** the attacker wants: availability, integrity, privacy, misuse, or supply-chain compromise. The identifier is a stable handle for the attack type. The same identifier can appear under more than one impact class — model poisoning, for example, can deny service and corrupt behavior.

### Predictive AI

| ID | Published name | In plain language | Coverage | Where |
|---|---|---|---|---|
| NISTAML.01 | Availability Violations | The attacker makes the model slow, expensive, or unavailable | ◐ | [M11.3](modules/m11-serving-monitoring/lesson-3-request-bounds-validation-and-safe-output.md) |
| NISTAML.011 | Model Poisoning | Corrupting the trained model itself, including in federated settings | ● | [M12.2](modules/m12-federated-learning/lesson-2-malicious-clients-and-update-poisoning.md), [LAB-16](labs/lab-16.md) |
| NISTAML.012 | Clean-label Poisoning | Poisoning features while leaving labels correct | ◐ | [M05.3](modules/m05-poisoning/lesson-3-targeted-poisoning.md) |
| NISTAML.013 | Data Poisoning | Manipulating training data so the learned behavior is wrong | ● | [M05.2](modules/m05-poisoning/lesson-2-label-flipping.md), [LAB-05](labs/lab-05.md), [LAB-06](labs/lab-06.md) |
| NISTAML.014 | Energy-latency | Inputs crafted to maximize computation, not to change the label | ◐ | [M11.3](modules/m11-serving-monitoring/lesson-3-request-bounds-validation-and-safe-output.md) |
| NISTAML.02 | Integrity Violations | The attacker changes what the model outputs or how it behaves | ● | [M04](modules/m04-evasion/index.md), [M05](modules/m05-poisoning/index.md), [M06](modules/m06-backdoors/index.md) |
| NISTAML.021 | Clean-label Backdoor | A trigger works without relabeling the poisoned examples | ◐ | [M06.1](modules/m06-backdoors/lesson-1-backdoor-anatomy.md) |
| NISTAML.022 | Evasion | Perturbing an input at test time to flip a prediction | ● | [M04.2](modules/m04-evasion/lesson-2-fgsm.md), [M04.3](modules/m04-evasion/lesson-3-pgd.md), [LAB-03](labs/lab-03.md) |
| NISTAML.023 | Backdoor Poisoning | Implanting trigger-conditioned behavior during training | ● | [M06.2](modules/m06-backdoors/lesson-2-tabular-backdoor.md), [LAB-07](labs/lab-07.md), [LAB-08](labs/lab-08.md) |
| NISTAML.024 | Targeted Poisoning | Causing a specific input to receive a chosen label | ● | [M05.3](modules/m05-poisoning/lesson-3-targeted-poisoning.md), [LAB-06](labs/lab-06.md) |
| NISTAML.025 | Black-box Evasion | Evasion with only query or label access | ● | [M04.4](modules/m04-evasion/lesson-4-black-box-and-transfer.md), [LAB-04](labs/lab-04.md) |
| NISTAML.026 | Model Poisoning | Directly modifying model parameters or updates | ● | [M12.2](modules/m12-federated-learning/lesson-2-malicious-clients-and-update-poisoning.md), [LAB-16](labs/lab-16.md) |
| NISTAML.03 | Privacy Compromises | The attacker learns something about training data or the model | ● | [M07](modules/m07-extraction-privacy/index.md), [M13](modules/m13-privacy-preserving-ml/index.md) |
| NISTAML.031 | Model Extraction | Reconstructing a functionally similar model through queries | ● | [M07.2](modules/m07-extraction-privacy/lesson-2-model-extraction.md), [LAB-09](labs/lab-09.md) |
| NISTAML.032 | Reconstruction | Recovering training records from released outputs | ◐ | [M07.4](modules/m07-extraction-privacy/lesson-4-inversion-and-attribute-inference.md), [M13.1](modules/m13-privacy-preserving-ml/lesson-1-privacy-threat-models.md) |
| NISTAML.033 | Membership Inference | Deciding whether a record was in the training set | ● | [M07.3](modules/m07-extraction-privacy/lesson-3-membership-inference.md), [LAB-10](labs/lab-10.md), [LAB-17](labs/lab-17.md) |
| NISTAML.034 | Property Inference | Inferring a dataset-level property the model was not meant to reveal | ◐ | [M07.4](modules/m07-extraction-privacy/lesson-4-inversion-and-attribute-inference.md) |
| NISTAML.05 | Supply Chain Attacks | Compromise arrives through a model, dataset, package, or tool supplier | ● | [M10](modules/m10-supply-chain/index.md), [LAB-13](labs/lab-13.md) |
| NISTAML.051 | Model Poisoning (supply chain) | A supplied model or checkpoint already carries malicious behavior | ● | [M10.1](modules/m10-supply-chain/lesson-1-ml-supply-chain-and-artifact-trust.md), [LAB-13](labs/lab-13.md) |

### Generative AI

NIST's generative matrix reuses identifiers for attack types that also affect predictive systems, and adds identifiers for prompt- and tool-mediated attacks.

| ID | Published name | In plain language | Coverage | Where |
|---|---|---|---|---|
| NISTAML.013 | Data Poisoning | Corrupting pre-training or fine-tuning data | ● | [M15.3](modules/m15-genai-llm-agents/lesson-3-retrieval-provenance-and-rag-boundaries.md), [LAB-19](labs/lab-19.md) |
| NISTAML.015 | Indirect Prompt Injection | Instructions arrive inside retrieved or tool content | ● | [M15.2](modules/m15-genai-llm-agents/lesson-2-prompt-injection-and-instruction-hierarchy.md), [LAB-19](labs/lab-19.md) |
| NISTAML.017 | Time-consuming background tasks | Injected instructions make the system do expensive work | ◐ | [M15.6](modules/m15-genai-llm-agents/lesson-6-layered-defense-taxonomies-and-evaluation.md) |
| NISTAML.018 | Prompt Injection | The user's own input overrides intended instructions | ● | [M15.2](modules/m15-genai-llm-agents/lesson-2-prompt-injection-and-instruction-hierarchy.md), [LAB-19](labs/lab-19.md) |
| NISTAML.023 | Backdoor Poisoning | Trigger-conditioned behavior in a generative model | ◐ | [M06.1](modules/m06-backdoors/lesson-1-backdoor-anatomy.md), [M15.3](modules/m15-genai-llm-agents/lesson-3-retrieval-provenance-and-rag-boundaries.md) |
| NISTAML.024 | Targeted Poisoning | Steering outputs toward an attacker-chosen target | ◐ | [M05.3](modules/m05-poisoning/lesson-3-targeted-poisoning.md) |
| NISTAML.027 | Misaligned Outputs | Output that violates the intended behavior or policy | ◐ | [M15.4](modules/m15-genai-llm-agents/lesson-4-sensitive-data-and-insecure-output.md), [M15.6](modules/m15-genai-llm-agents/lesson-6-layered-defense-taxonomies-and-evaluation.md) |
| NISTAML.033 | Membership Inference | Detecting whether text or an image was in training data | ● | [M07.3](modules/m07-extraction-privacy/lesson-3-membership-inference.md), [LAB-10](labs/lab-10.md) |
| NISTAML.035 | Prompt Extraction | Recovering the system prompt | ◐ | [M15.4](modules/m15-genai-llm-agents/lesson-4-sensitive-data-and-insecure-output.md) |
| NISTAML.036 | Leaking information from user interactions | One user's data appears in another user's session or output | ◐ | [M15.4](modules/m15-genai-llm-agents/lesson-4-sensitive-data-and-insecure-output.md) |
| NISTAML.037 | Training Data Attacks | Memorization and extraction of training content | ◐ | [M15.1](modules/m15-genai-llm-agents/lesson-1-from-predictive-ml-to-llm-security.md), [M15.4](modules/m15-genai-llm-agents/lesson-4-sensitive-data-and-insecure-output.md) |
| NISTAML.038 | Data Extraction | Pulling sensitive data out through model outputs | ◐ | [M07.5](modules/m07-extraction-privacy/lesson-5-privacy-risk-and-governance.md), [M15.4](modules/m15-genai-llm-agents/lesson-4-sensitive-data-and-insecure-output.md) |
| NISTAML.039 | Compromising connected resources | Using the model to reach systems or data it can access | ● | [M15.5](modules/m15-genai-llm-agents/lesson-5-agent-authority-tools-and-delegated-trust.md), [LAB-20](labs/lab-20.md) |
| NISTAML.04 | Misuse Violations | Legitimate capability turned to a harmful purpose | ◐ | [M15.6](modules/m15-genai-llm-agents/lesson-6-layered-defense-taxonomies-and-evaluation.md) |
| NISTAML.05 / .051 | Supply Chain Attacks / Model Poisoning | A third-party model or component arrives compromised | ● | [M10.1](modules/m10-supply-chain/lesson-1-ml-supply-chain-and-artifact-trust.md), [LAB-13](labs/lab-13.md) |

Two practical cautions. First, **impact class and attack type are different axes**: "poisoning" is a technique, "availability" or "integrity" is the harm. Second, NIST's document is a taxonomy and terminology report, not a control catalog; it describes attacks and mitigations but does not tell you that a specific product configuration is compliant.

## 2. MITRE ATLAS

ATLAS is the adversarial-ML counterpart to ATT&CK: tactics describe *why* an adversary acts, techniques describe *how*. ATLAS data release v2026.09 lists 16 tactics, 120 techniques, 88 sub-techniques, 40 mitigations, and 73 case studies.

### Tactics touched by the course

| Tactic ID | Tactic | Course anchor |
|---|---|---|
| AML.TA0000 | AI Model Access | [M07.1](modules/m07-extraction-privacy/lesson-1-prediction-apis-as-attack-surface.md) — query access is the precondition for extraction |
| AML.TA0001 | AI Attack Adaptation | [M08.4](modules/m08-robustness-defense/lesson-4-adaptive-attacks-and-pitfalls.md) — the adversary adjusts to the defense |
| AML.TA0002 | Reconnaissance | [M03.3](modules/m03-threat-modeling/lesson-3-surfaces-lifecycle-atlas.md) |
| AML.TA0003 | Resource Development | [M03.3](modules/m03-threat-modeling/lesson-3-surfaces-lifecycle-atlas.md) — proxy models and tooling |
| AML.TA0004 | Initial Access | [M10](modules/m10-supply-chain/index.md), [M15.2](modules/m15-genai-llm-agents/lesson-2-prompt-injection-and-instruction-hierarchy.md) |
| AML.TA0005 | Execution | [M10.2](modules/m10-supply-chain/lesson-2-unsafe-serialization-and-safe-formats.md) — deserialization executes code |
| AML.TA0006 | Persistence | [M06](modules/m06-backdoors/index.md) — a backdoor persists across benign inputs |
| AML.TA0007 | Defense Evasion | [M04.4](modules/m04-evasion/lesson-4-black-box-and-transfer.md), [M08.4](modules/m08-robustness-defense/lesson-4-adaptive-attacks-and-pitfalls.md) |
| AML.TA0008 | Discovery | [M07.1](modules/m07-extraction-privacy/lesson-1-prediction-apis-as-attack-surface.md) |
| AML.TA0009 | Collection | [M07.3](modules/m07-extraction-privacy/lesson-3-membership-inference.md), [M15.4](modules/m15-genai-llm-agents/lesson-4-sensitive-data-and-insecure-output.md) |
| AML.TA0010 | Exfiltration | [M07.2](modules/m07-extraction-privacy/lesson-2-model-extraction.md), [M15.5](modules/m15-genai-llm-agents/lesson-5-agent-authority-tools-and-delegated-trust.md) |
| AML.TA0011 | Impact | [M11.5](modules/m11-serving-monitoring/lesson-5-incident-response-rollback-and-evidence.md) |
| AML.TA0012 | Privilege Escalation | [M11.2](modules/m11-serving-monitoring/lesson-2-authentication-and-authorization.md) |
| AML.TA0013 | Credential Access | [M10.4](modules/m10-supply-chain/lesson-4-provenance-signing-and-promotion.md), [M11.6](modules/m11-serving-monitoring/lesson-6-secure-configuration-secrets-and-least-privilege.md) |
| AML.TA0014 | Command and Control | [M15.5](modules/m15-genai-llm-agents/lesson-5-agent-authority-tools-and-delegated-trust.md) — tool-mediated egress |
| AML.TA0015 | Lateral Movement | [M15.5](modules/m15-genai-llm-agents/lesson-5-agent-authority-tools-and-delegated-trust.md) — connected resources |

### Techniques practised or discussed

| Technique ID | Technique | Coverage | Where |
|---|---|---|---|
| AML.T0010 | AI Supply Chain Compromise | ● | [M10](modules/m10-supply-chain/index.md), [LAB-13](labs/lab-13.md) |
| AML.T0010.001 | AI Software (supply chain) | ● | [M10.3](modules/m10-supply-chain/lesson-3-dependency-and-artifact-scanning.md), [LAB-13](labs/lab-13.md) |
| AML.T0010.002 | Data (supply chain) | ◐ | [M09.1](modules/m09-data-integrity/lesson-1-provenance-and-lineage.md) |
| AML.T0010.003 | Model (supply chain) | ● | [M10.1](modules/m10-supply-chain/lesson-1-ml-supply-chain-and-artifact-trust.md), [LAB-13](labs/lab-13.md) |
| AML.T0011.001 | Malicious Package | ● | [M10.3](modules/m10-supply-chain/lesson-3-dependency-and-artifact-scanning.md), [LAB-13](labs/lab-13.md) |
| AML.T0015 | Evade AI Model | ● | [M04](modules/m04-evasion/index.md), [LAB-03](labs/lab-03.md) |
| AML.T0018 | Manipulate AI Model | ● | [M06](modules/m06-backdoors/index.md), [M12.2](modules/m12-federated-learning/lesson-2-malicious-clients-and-update-poisoning.md) |
| AML.T0018.000 | Poison AI Model | ● | [LAB-07](labs/lab-07.md), [LAB-16](labs/lab-16.md) |
| AML.T0018.002 | Embed Malware | ◐ | [M10.2](modules/m10-supply-chain/lesson-2-unsafe-serialization-and-safe-formats.md) |
| AML.T0020 | Training Data Poisoning | ● | [M05](modules/m05-poisoning/index.md), [LAB-05](labs/lab-05.md), [LAB-06](labs/lab-06.md) |
| AML.T0024 | Exfiltration via AI Inference API | ● | [M07](modules/m07-extraction-privacy/index.md) |
| AML.T0024.000 | Infer Training Data Membership | ● | [LAB-10](labs/lab-10.md) |
| AML.T0024.001 | Invert AI Model | ◐ | [M07.4](modules/m07-extraction-privacy/lesson-4-inversion-and-attribute-inference.md) |
| AML.T0024.002 | Extract AI Model | ● | [LAB-09](labs/lab-09.md) |
| AML.T0029 | Denial of AI Service | ◐ | [M11.3](modules/m11-serving-monitoring/lesson-3-request-bounds-validation-and-safe-output.md) |
| AML.T0034 | Cost Harvesting | ● | [M11.3](modules/m11-serving-monitoring/lesson-3-request-bounds-validation-and-safe-output.md), [LAB-14](labs/lab-14.md) — rate limiting bounds cost, not only throughput |
| AML.T0040 | AI Model Inference API Access | ● | [M07.1](modules/m07-extraction-privacy/lesson-1-prediction-apis-as-attack-surface.md), [LAB-09](labs/lab-09.md) |
| AML.T0043 | Craft Adversarial Data | ● | [M04](modules/m04-evasion/index.md) |
| AML.T0043.000 | White-Box Optimization | ● | [LAB-03](labs/lab-03.md) |
| AML.T0043.001 | Black-Box Optimization | ● | [LAB-04](labs/lab-04.md) |
| AML.T0043.002 | Black-Box Transfer | ● | [LAB-04](labs/lab-04.md) |
| AML.T0043.004 | Insert Backdoor Trigger | ● | [LAB-08](labs/lab-08.md) |
| AML.T0051 | LLM Prompt Injection | ● | [M15.2](modules/m15-genai-llm-agents/lesson-2-prompt-injection-and-instruction-hierarchy.md), [LAB-19](labs/lab-19.md) |
| AML.T0051.000 | Direct (prompt injection) | ● | [LAB-19](labs/lab-19.md) |
| AML.T0051.001 | Indirect (prompt injection) | ● | [LAB-19](labs/lab-19.md) |
| AML.T0053 | AI Agent Tool Invocation | ● | [M15.5](modules/m15-genai-llm-agents/lesson-5-agent-authority-tools-and-delegated-trust.md), [LAB-20](labs/lab-20.md) |
| AML.T0054 | LLM Jailbreak | ◐ | [M15.2](modules/m15-genai-llm-agents/lesson-2-prompt-injection-and-instruction-hierarchy.md) |
| AML.T0056 | Extract LLM System Prompt | ◐ | [M15.4](modules/m15-genai-llm-agents/lesson-4-sensitive-data-and-insecure-output.md) |
| AML.T0057 | LLM Data Leakage | ◐ | [M15.4](modules/m15-genai-llm-agents/lesson-4-sensitive-data-and-insecure-output.md) |
| AML.T0070 | RAG Poisoning | ● | [M15.3](modules/m15-genai-llm-agents/lesson-3-retrieval-provenance-and-rag-boundaries.md), [LAB-19](labs/lab-19.md) |
| AML.T0071 | False RAG Entry Injection | ● | [LAB-19](labs/lab-19.md) |
| AML.T0080 | AI Agent Context Poisoning | ● | [M15.5](modules/m15-genai-llm-agents/lesson-5-agent-authority-tools-and-delegated-trust.md), [LAB-20](labs/lab-20.md) |
| AML.T0086 | Exfiltration via AI Agent Tool Invocation | ● | [LAB-20](labs/lab-20.md) |
| AML.T0101 | Data Destruction via AI Agent Tool Invocation | ● | [LAB-20](labs/lab-20.md) |
| AML.T0110 | AI Agent Tool Poisoning | ◐ | [M15.5](modules/m15-genai-llm-agents/lesson-5-agent-authority-tools-and-delegated-trust.md) |

ATLAS technique pages also list mitigations. When you cite an ATLAS mitigation in a report, cite the mitigation ID from the same data release, not the technique ID, and say which release you used.

## 3. OWASP guidance

### 3.1 LLM application risks: 2025 taught IDs and 2026 crosswalk

The lessons, quizzes, LAB-19, and LAB-20 use the **2025** edition's identifiers. The **2026** edition renumbers several categories. Both are legitimate; mixing IDs across editions is not. State the edition in every citation.

| 2025 ID and name | Taught in | 2026 ID and name |
|---|---|---|
| LLM01:2025 Prompt Injection | [M15.2](modules/m15-genai-llm-agents/lesson-2-prompt-injection-and-instruction-hierarchy.md), [LAB-19](labs/lab-19.md) | LLM01:2026 Prompt Injection |
| LLM02:2025 Sensitive Information Disclosure | [M15.4](modules/m15-genai-llm-agents/lesson-4-sensitive-data-and-insecure-output.md), [LAB-19](labs/lab-19.md) | LLM02:2026 Sensitive Information Disclosure |
| LLM03:2025 Supply Chain | [M10](modules/m10-supply-chain/index.md), [M15.6](modules/m15-genai-llm-agents/lesson-6-layered-defense-taxonomies-and-evaluation.md) | LLM04:2026 Supply Chain |
| LLM04:2025 Data and Model Poisoning | [M05](modules/m05-poisoning/index.md), [M15.3](modules/m15-genai-llm-agents/lesson-3-retrieval-provenance-and-rag-boundaries.md), [LAB-19](labs/lab-19.md) | LLM05:2026 Data and Model Poisoning |
| LLM05:2025 Improper Output Handling | [M15.4](modules/m15-genai-llm-agents/lesson-4-sensitive-data-and-insecure-output.md) | LLM10:2026 Improper Output Handling |
| LLM06:2025 Excessive Agency | [M15.5](modules/m15-genai-llm-agents/lesson-5-agent-authority-tools-and-delegated-trust.md), [LAB-20](labs/lab-20.md) | LLM03:2026 Excessive Agency |
| LLM07:2025 System Prompt Leakage | [M15.4](modules/m15-genai-llm-agents/lesson-4-sensitive-data-and-insecure-output.md) | LLM08:2026 Hidden Context Exposure (closest successor; check the scope in the 2026 text) |
| LLM08:2025 Vector and Embedding Weaknesses | [M15.3](modules/m15-genai-llm-agents/lesson-3-retrieval-provenance-and-rag-boundaries.md) | LLM09:2026 Vector and Embedding Weaknesses |
| LLM09:2025 Misinformation | [M15.4](modules/m15-genai-llm-agents/lesson-4-sensitive-data-and-insecure-output.md), [M15.6](modules/m15-genai-llm-agents/lesson-6-layered-defense-taxonomies-and-evaluation.md) | LLM07:2026 Misinformation |
| LLM10:2025 Unbounded Consumption | [M11.3](modules/m11-serving-monitoring/lesson-3-request-bounds-validation-and-safe-output.md), [M15.6](modules/m15-genai-llm-agents/lesson-6-layered-defense-taxonomies-and-evaluation.md) | LLM06:2026 Unbounded Consumption |

The crosswalk is a reading aid, not an equivalence claim. Category scope and wording changed between editions, and "Hidden Context Exposure" covers more than system prompts. When you need an authoritative mapping, use the crosswalk tables published in the 2026 report itself.

### 3.2 API Security Top 10 2023

The serving module and LAB-14 are about prediction APIs, so the API list matters as much as the LLM list.

| ID | Category | Coverage | Where |
|---|---|---|---|
| API1:2023 | Broken Object Level Authorization | ● | [M11.2](modules/m11-serving-monitoring/lesson-2-authentication-and-authorization.md), [LAB-14](labs/lab-14.md) |
| API2:2023 | Broken Authentication | ● | [M11.2](modules/m11-serving-monitoring/lesson-2-authentication-and-authorization.md), [LAB-14](labs/lab-14.md) |
| API3:2023 | Broken Object Property Level Authorization | ◐ | [M11.3](modules/m11-serving-monitoring/lesson-3-request-bounds-validation-and-safe-output.md) |
| API4:2023 | Unrestricted Resource Consumption | ● | [M11.3](modules/m11-serving-monitoring/lesson-3-request-bounds-validation-and-safe-output.md), [LAB-14](labs/lab-14.md) |
| API5:2023 | Broken Function Level Authorization | ◐ | [M11.2](modules/m11-serving-monitoring/lesson-2-authentication-and-authorization.md) |
| API6:2023 | Unrestricted Access to Sensitive Business Flows | ◐ | [M11.4](modules/m11-serving-monitoring/lesson-4-monitoring-drift-and-attack-indicators.md) — scraping and automated abuse |
| API7:2023 | Server Side Request Forgery | ◐ | [M15.5](modules/m15-genai-llm-agents/lesson-5-agent-authority-tools-and-delegated-trust.md) — agent fetch tools |
| API8:2023 | Security Misconfiguration | ● | [M11.6](modules/m11-serving-monitoring/lesson-6-secure-configuration-secrets-and-least-privilege.md), [LAB-14](labs/lab-14.md) |
| API9:2023 | Improper Inventory Management | ◐ | [M11.1](modules/m11-serving-monitoring/lesson-1-serving-architecture-and-attack-surface.md) |
| API10:2023 | Unsafe Consumption of APIs | ◐ | [M15.5](modules/m15-genai-llm-agents/lesson-5-agent-authority-tools-and-delegated-trust.md) — tool output is untrusted input |

The ML Security Top 10 ([F-09](references.md#frameworks-standards-and-guidance)) is a useful cross-check, but it is an incubator project with a different structure. The course does not use its identifiers in assessments.

## 4. NIST AI RMF and SSDF

The AI RMF describes *what an organization does*: GOVERN, MAP, MEASURE, MANAGE. The course rehearses the evidence each function needs, at the scale of one system.

| AI RMF function | What it asks for | Course evidence |
|---|---|---|
| GOVERN | Policies, roles, accountability, and risk tolerance | [M03.4](modules/m03-threat-modeling/lesson-4-frameworks-and-crosswalks.md), [M09.5](modules/m09-data-integrity/lesson-5-dataset-governance-and-audit.md), [M14.4](modules/m14-explainability-fairness/lesson-4-security-trade-offs-and-audit-reporting.md), project reports |
| MAP | Context, intended use, threat model, and affected parties | [M03.5](modules/m03-threat-modeling/lesson-5-building-the-model.md), [M16.1](modules/m16-end-to-end-assessment/lesson-1-scoping-and-system-documentation.md), [LAB-02](labs/lab-02.md) |
| MEASURE | Metrics, testing, uncertainty, and tracked risk | [M04.5](modules/m04-evasion/lesson-5-measuring-honestly.md), [M08.5](modules/m08-robustness-defense/lesson-5-standardized-evaluation.md), [M16.3](modules/m16-end-to-end-assessment/lesson-3-measurement-baselines-and-evidence.md), every lab's `metrics.json` |
| MANAGE | Prioritize, respond, recover, and monitor | [M11.5](modules/m11-serving-monitoring/lesson-5-incident-response-rollback-and-evidence.md), [M16.4](modules/m16-end-to-end-assessment/lesson-4-findings-severity-and-remediation.md), [M17.3](modules/m17-red-team-blue-team/lesson-3-blue-team-detection-and-response.md), [LAB-15](labs/lab-15.md) |

The Generative AI Profile (NIST AI 600-1) adds risks that the base framework names less explicitly, including confabulation, information integrity, and information security. [M15.6](modules/m15-genai-llm-agents/lesson-6-layered-defense-taxonomies-and-evaluation.md) uses that framing when it separates content risk from security risk.

The SSDF has four practice groups. The course touches all four but implements none completely.

| SSDF group | Course anchor | Honest limitation |
|---|---|---|
| PO — Prepare the Organization | [M09.5](modules/m09-data-integrity/lesson-5-dataset-governance-and-audit.md), [M14.4](modules/m14-explainability-fairness/lesson-4-security-trade-offs-and-audit-reporting.md) | You practise a policy for one project, not an organizational program |
| PS — Protect the Software | [M10.1](modules/m10-supply-chain/lesson-1-ml-supply-chain-and-artifact-trust.md), [M10.4](modules/m10-supply-chain/lesson-4-provenance-signing-and-promotion.md) | You verify hashes and provenance locally; you do not run a signing service |
| PW — Produce Well-Secured Software | [M09.4](modules/m09-data-integrity/lesson-4-reproducible-training.md), [M10.2](modules/m10-supply-chain/lesson-2-unsafe-serialization-and-safe-formats.md), [M11.6](modules/m11-serving-monitoring/lesson-6-secure-configuration-secrets-and-least-privilege.md) | Secure coding is exercised on small services, not a full SDLC |
| RV — Respond to Vulnerabilities | [M11.5](modules/m11-serving-monitoring/lesson-5-incident-response-rollback-and-evidence.md), [M17.3](modules/m17-red-team-blue-team/lesson-3-blue-team-detection-and-response.md) | Incident response is a tabletop and a lab, not a live incident |

NIST SP 800-218A adapts SSDF practices to generative AI and dual-use foundation models. The course discusses model provenance and supplier trust in [M10.4](modules/m10-supply-chain/lesson-4-provenance-signing-and-promotion.md) but does not implement the full profile.

## 5. Governance frameworks used only for context

| Framework | How the course uses it | What the course does not do |
|---|---|---|
| ISO/IEC 42001:2023 | Vocabulary for an AI management system when you write governance evidence | No audit, no management-system implementation, no certification |
| ISO/IEC 23894:2023 | Risk-management process language that overlaps with the AI RMF | No formal risk register or organizational process |
| Regulation (EU) 2024/1689 (AI Act) | Regulatory context for risk classification and documentation | No legal analysis, no conformity assessment, no advice |
| NIST CSF 2.0 | A general security vocabulary for govern, identify, protect, detect, respond, recover | Not used to structure the course |

[F-14](references.md#frameworks-standards-and-guidance) is included so you can see how regulatory obligations differ from technical controls. Reading it does not make you qualified to advise on the regulation.

## 6. Combining frameworks without confusing them

A worked example. LAB-19 tests a RAG assistant that reads untrusted documents. A defensible sentence in your report is:

> The indirect-injection test (NISTAML.015; ATLAS AML.T0051.001) achieved 4 of 12 successful instruction overrides. In OWASP LLM01:2025 terms this is prompt injection through retrieved content; the relevant control is provenance and instruction hierarchy, implemented as document trust labels plus a retrieval filter. Residual risk: a poisoned document that passes the filter.

That sentence uses three vocabularies correctly because it names each edition and gives the measured result separately from the classification. What it must not say is "the system is OWASP-compliant" or "NIST-certified".

| Do | Do not |
|---|---|
| Cite the edition and version with the ID | Cite "OWASP LLM Top 10" with no year |
| Map at the technique or category level | Claim a control satisfies an entire framework |
| Report measurements separately from classification | Turn a passing lab into a compliance statement |
| Say "supports", "aligns with", "provides evidence for" | Say "certified", "compliant", "approved" |
| Note the framework's own scope limits | Assume one framework's IDs transfer to another |

## 7. Coverage gaps

These are deliberate. Knowing what the course leaves out is part of using the mapping honestly.

- **Certified robustness.** The course teaches PGD evaluation and adversarial training, and discusses randomized smoothing and convex relaxations as reading. It does not implement a certifier.
- **Watermarking and ownership.** Discussed as a research area in [M07.5](modules/m07-extraction-privacy/lesson-5-privacy-risk-and-governance.md); not implemented.
- **Production federated learning.** LAB-16 is a simulation with eight clients. It does not cover secure aggregation protocols, client sampling at scale, or cross-device deployment.
- **Physical-world attacks.** The reading covers adversarial patches and physical examples; the labs stay digital.
- **Hardware and side channels.** Out of scope.
- **Agentic autonomy at scale.** LAB-20 models approval and capability boundaries in a mock environment, not a real agent platform.
- **Organizational compliance.** No management-system audit, no legal analysis, no regulatory filing.

## What this mapping does not mean

Completing this course does not certify compliance with any framework, standard, or regulation named on this page. The mapping shows where course activities touch published concepts so you can read the primary documents and write precise reports. It does not establish that a system, a lab artifact, or a learner meets any external requirement. For compliance work, use the current official text and a qualified assessor.

## Where to go next

- [References](references.md) — the primary sources behind every ID on this page.
- [Glossary](glossary.md) — plain-language definitions and acronym expansions.
- [Research reading guide](research-reading-guide.md) — how to read the original papers behind these categories.
- [M03.4 — Frameworks and crosswalks](modules/m03-threat-modeling/lesson-4-frameworks-and-crosswalks.md) — the lesson that introduces cross-framework reasoning.
