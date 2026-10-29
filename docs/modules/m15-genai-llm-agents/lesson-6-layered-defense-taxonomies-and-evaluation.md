# Lesson 15.6 — Layered Defense, Taxonomies, and Evaluation

<a id="m15-l6"></a>

**Module 15 · Lesson 6 of 6 · 1.5 hours · LO-25, LO-27, LO-28**

## Scenario

A release review has two results. LAB-19's combined policy blocks all three scripted RAG attacks. LAB-20's layered policy blocks all five scripted agent attacks. The slide says "8/8 attacks blocked; 7/7 benign tasks preserved." Someone asks whether the system is secure.

The honest answer is: the system passed a small, deterministic, scripted suite. That is useful evidence. It is not a security property, and it does not tell the team what an adaptive attacker would do.

This lesson builds the evaluation and reporting discipline that keeps that distinction visible.

## Objectives

By the end of this lesson you will be able to:

1. Map LLM application risks to OWASP LLM categories, MITRE ATLAS techniques, and NIST terminology.
2. Design a layered defense that assigns each control to a failure it can actually stop.
3. Evaluate a defense with benign utility, attack success, false positives, and adaptive cases.
4. Report the result with scope, model version, sample size, and residual risk.
5. Write an incident-response outline for an LLM or agent compromise.
6. State what a taxonomy mapping does and does not establish.

## 1. Defense in depth for LLM applications

| Layer | Controls | Stops | Does not stop |
|---|---|---|---|
| Input | Size, rate, auth, provenance, encoding checks | Obvious abuse, resource exhaustion | Semantic injection |
| Context | Role separation, trust labels, spotlighting, dual LLM | Authority confusion | A model that ignores the labels |
| Model | Alignment, instruction hierarchy training, refusal behavior | Some harmful requests | Adaptive jailbreaks, indirect injection |
| Retrieval | Tenant/ACL filtering, trust-aware ranking, ingestion control | Cross-tenant and poisoned content | A well-ranked allowed document |
| Output | Schema, allowlist, encoding, redaction, canary | Known leaks, downstream injection | Unlisted content, semantic leaks |
| Action | Tool scope, approval, egress allowlist, sandbox | Unauthorized actions | An allowed action used maliciously |
| Runtime | Least privilege, network policy, secrets isolation | Privilege escalation, lateral movement | Bugs in allowed code |
| Monitoring | Logs, traces, anomaly detection, tripwires | Prolonged or repeated abuse | A single low-and-slow event |
| Governance | Review, model cards, incident response, training | Recurring process failures | A novel technical attack |

The table is a design checklist, not a score. A layer that does not address a specific failure is decoration. The question for each row is: *which test would fail if this control were removed?*

### Defense in depth is not defense by checklist

Adding controls can create new costs:

- More filters mean more false positives and more user workarounds.
- More approvals mean approval fatigue.
- More logging means more sensitive data at rest.
- More model-side instructions mean a longer prompt and more places to leak.

A layered design should state the failure each layer addresses and the cost it adds. "We have eight controls" is not an argument.

## 2. Mapping to OWASP

The OWASP Top 10 for LLM Applications 2025 names ten risk families. The mapping below links each to a concrete failure, a primary control, and the lab that exercises it. "Lab" means the lab contains a related test, not that the category is fully covered.

| OWASP 2025 | Failure in this module | Primary controls | Lab touchpoint |
|---|---|---|---|
| LLM01 Prompt Injection | Retrieved note or user text becomes an instruction | Provenance, hierarchy, tool authorization | LAB-19; LAB-20 |
| LLM02 Sensitive Information Disclosure | Canary, prompt, or customer data in output | Data minimization, output policy, redaction | LAB-19 canary |
| LLM03 Supply Chain | Model, tokenizer, prompt, vector store, tool dependency | Inventory, version pinning, provenance | Not tested |
| LLM04 Data and Model Poisoning | Poisoned corpus or fine-tune | Ingestion ACL, validation, monitoring | LAB-19 untrusted docs (partial) |
| LLM05 Improper Output Handling | Markup, SQL, shell, URL rendered or executed | Encoding, parameterization, allowlists | Not tested |
| LLM06 Excessive Agency | Broad tools, scope, or autonomy | Capability scoping, approval, budgets | LAB-20 |
| LLM07 System Prompt Leakage | Prompt repeated or paraphrased | Remove secrets; canary; output policy | Not tested |
| LLM08 Vector and Embedding Weaknesses | Cross-tenant retrieval, poisoning, inversion | Tenant filters, access control, provenance | Not tested |
| LLM09 Misinformation | Confident wrong answer | Grounding, citations, uncertainty, review | LAB-19 benign only |
| LLM10 Unbounded Consumption | Token, loop, or cost exhaustion | Quotas, timeouts, iteration caps | Not tested |

Five of the ten categories are not exercised by the labs. That is a coverage gap to report, not a reason to rename the tests.

### Mapping is not coverage

A mapping says "this test is relevant to this category." It does not say "this category is covered." Coverage requires a test that would fail if the control were absent, plus a statement of what the test does not include. A category with no test is a known unknown; a category with one test is a known test, not a solved problem.

## 3. Mapping to MITRE ATLAS and NIST

MITRE ATLAS catalogues adversary techniques. Representative entries relevant to this module:

| ATLAS technique | What it describes | Where it appears here |
|---|---|---|
| AML.T0051 LLM Prompt Injection | Crafted input changes model behavior | LAB-19; Lesson 15.2 |
| AML.T0054 LLM Jailbreak | Input bypasses model safety policy | Lesson 15.2 (concept) |
| AML.T0057 LLM Data Leakage | Prompts induce disclosure | Lesson 15.4; LAB-19 canary |
| AML.T0020 Poison Training Data | Adversary corrupts training data | Lesson 15.3 (corpus analogue) |
| AML.T0018 Backdoor ML Model | Triggered behavior implanted in a model | Module 06; LLM analogue |
| AML.T0024 Exfiltration via AI Inference API | Extraction through query access | Lesson 15.2 extraction discussion |

The IDs and names are from the ATLAS entries consulted on 2026-10-28. ATLAS evolves; cite the version or date when a mapping matters.

NIST AI 100-2e2025 organizes adversarial ML threats into broad families: evasion, poisoning, privacy, and abuse. LLM-specific material extends these to prompt injection, jailbreaks, and data extraction. NIST AI RMF 1.0 provides the governance functions — GOVERN, MAP, MEASURE, MANAGE — that turn a technical finding into a managed risk. A lab result is a MEASURE input; it is not a GOVERN decision.

| Framework | Use in this module | Limit |
|---|---|---|
| OWASP LLM Top 10 | Risk vocabulary and mitigation checklist | Not a test suite; categories overlap |
| MITRE ATLAS | Technique catalogue and detection mapping | Not exhaustive; evolves |
| NIST AI 100-2e2025 | Adversarial-ML taxonomy | Research taxonomy, not a compliance standard |
| NIST AI RMF | Governance and risk lifecycle | Does not prescribe specific controls |
| ISO/IEC 42001 | AI management-system requirements | Organizational, not a technical test |

A report can cite several frameworks without claiming that any of them certifies the system.

## 4. Evaluation design

A defensible LLM evaluation has seven parts.

### 1. Scope and version

Name the model, version, decoding settings, prompt version, retrieval corpus version, tool set, and policy version. An LLM result without a version is not reproducible.

### 2. Benign utility

Measure whether the application still does its job. Include:

- task success on representative benign requests;
- refusal rate on benign requests;
- latency and cost;
- answer quality or citation accuracy where measurable.

A defense that blocks attacks by breaking the product is not a defense.

### 3. Attack suite

Include direct, indirect, encoded, multilingual, multi-turn, and tool-output cases. For RAG, include poisoned documents, cross-tenant queries, and citation spoofing. For agents, include path traversal, SSRF, recipient abuse, unauthorized tools, and origin spoofing.

### 4. Adaptive cases

After the first result, change the attack in response to the defense. This is the step most suites skip. Examples:

- paraphrase the instruction;
- encode it in base64 or HTML entities;
- place it in a different document role;
- split it across chunks;
- use an allowed recipient with a different subject;
- ask the model to translate or summarize the payload first.

Adaptive tests are not a proof of security either. They are evidence that the defense is not trivially bypassed.

### 5. False positives

Run the same controls on benign traffic. Report the block rate and inspect a sample of blocks. A control with a high false-positive rate will be disabled or worked around.

### 6. Reproducibility

Fix seeds where possible, record temperature, and repeat stochastic tests. Report a rate with a denominator, not a single pass.

### 7. Residual risk

List the attacks not tested, the assumptions (trusted model provider, static allowlists, no compromised account), and the monitoring and response plan.

## 5. Metrics

| Metric | Definition | Report as |
|---|---|---|
| Attack success rate | Successful attacks / attempted attacks | \(k/n\) with a rate and interval |
| Benign task success | Successful benign tasks / benign tasks | \(k/n\) |
| False-positive rate | Benign requests blocked / benign requests | \(k/n\) |
| Leakage rate | Responses containing the canary / attempts | \(k/n\) |
| Containment rate | Actions blocked / unauthorized actions attempted | \(k/n\) |
| Time to detect | Time from event to alert | Median and range |
| Cost per request | Tokens and infrastructure | Currency or tokens |
| Refusal rate | Benign requests refused | \(k/n\) |

A proportion from a small suite has a wide interval. With 8 attacks and 0 successes, the upper bound of a 95% rule-of-three interval is about \(3/8 = 0.375\). "0/8" does not mean the true success rate is zero; it means the suite did not observe one.

### The lab totals

| Configuration | Benign | Scripted attacks | Result |
|---|---:|---:|---|
| LAB-19 baseline | 3/3 | 3/3 succeeded | No boundary |
| LAB-19 trust labels | 3/3 | 1/3 succeeded | Indirect blocked; direct remains |
| LAB-19 output validation | 3/3 | 1/3 succeeded | Canary blocked; action marker succeeds |
| LAB-19 combined | 3/3 | 0/3 | All three blocked in the mock |
| LAB-20 baseline | 4/4 | 5/5 succeeded | No containment |
| LAB-20 scoped | 4/4 | 1/5 succeeded | Allowed-channel injection remains |
| LAB-20 approval | 4/4 | 2/5 succeeded | Reads and fetches remain |
| LAB-20 layered | 4/4 | 0/5 | All five blocked in the mock |

The two layered configurations together: 0/8 scripted attacks and 7/7 benign tasks. The correct statement is "0/8 on this suite," not "0% attack success in production." The suite is deterministic, the attacks are scripted, and the benign set is tiny.

## 6. Human factors

LLM defenses are used by people, and people are part of the attack surface.

- **Approval fatigue.** A reviewer who approves hundreds of actions per day will eventually approve a bad one. Use risk-based thresholds, not blanket approvals.
- **Automation bias.** A cited, confident answer is trusted more than an uncited one, even when the citation is wrong. Validate citations and show uncertainty.
- **Explanation trust.** A model's rationale can be plausible and unfaithful. Lesson 14.1 applies directly.
- **Workarounds.** If a filter blocks legitimate work, users will find another channel. Measure false positives and provide an escalation path.
- **Insider risk.** A legitimate account can still exfiltrate. Authorization and monitoring are not only for external attackers.

## 7. Incident response

An LLM or agent incident follows the same lifecycle as Module 11, with LLM-specific steps.

| Phase | Actions |
|---|---|
| Detect | Tripwire, canary, anomaly, user report, log alert |
| Triage | Which model, prompt, corpus, tool, tenant, and data? Is the action reversible? |
| Contain | Disable the tool or endpoint, revoke credentials, stop the agent, quarantine the document, block the recipient/host |
| Eradicate | Remove the poisoned content, patch the prompt or policy, rotate secrets |
| Recover | Verify with the test suite and a clean corpus; monitor for recurrence |
| Learn | Update the threat model, controls, tests, and monitoring; record the residual |

Two LLM-specific cautions:

- **Do not "fix" an incident by editing the system prompt alone.** If the action was authorized by a tool with broad scope, the scope is still broad.
- **Preserve the action log before rotating credentials.** The log is evidence; rotation may destroy the correlation between an action and an identity.

## 8. A scoped assurance statement

> For the RAG assistant and the workspace agent, model version X, prompt version Y, corpus version Z, we ran 8 scripted attacks (3 RAG, 5 agent) and 7 benign tasks. Across the two layered configurations, attack success was 0/8 (all 8 were blocked) and 7/7 benign tasks were preserved. We did not test adaptive paraphrases, encoded payloads, multilingual inputs, cross-tenant retrieval, output-rendering injection, or a compromised model provider. The allowlists are static; an allowed recipient or host can still carry data. Residual risk: a determined authenticated user may exfiltrate a small amount through an allowed channel, and a poisoned allowed document may influence an answer. The suite is a regression test, not a certification.

This statement is long because it is specific. It names what was tested, what passed, and what remains. It does not say "secure."

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Calling 0/8 "no attacks possible" | The number looks absolute | Report the suite and the interval |
| Mapping to a taxonomy and calling it coverage | The table looks complete | Name the tests and the gaps |
| Skipping adaptive tests | The first suite passes | Add paraphrase and encoding variants |
| Reporting only attack success | Security is the focus | Add benign utility and false positives |
| Testing one model version | The API is pinned | Record and re-run on change |
| Aggregating different systems into one score | It makes a clean headline | Report per system and per policy |
| Ignoring cost and latency | Security is the goal | Measure the operational cost |
| No incident plan | The demo works | Write containment and recovery steps |
| Treating a prompt fix as a containment | It is easy to edit | Fix scope, credentials, and egress too |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Results differ across runs | Stochastic decoding | Fix temperature/seed; repeat and report a rate |
| Benign success drops after a filter | False positives | Measure and refine |
| An adaptive variant bypasses the control | The control is pattern-based | Add provenance, authorization, and encoding |
| Cross-tenant test is not possible | No tenant model in the app | Add tenant identity before testing |
| Log cannot reconstruct the event | Missing origin or tool fields | Extend the schema; re-test |
| Approval queue is overloaded | Too many low-risk approvals | Risk-based thresholds |
| Incident recurs after a prompt patch | The underlying scope/egress remains | Fix the authority, not just the wording |

## Check your understanding

1. Why is "8/8 blocked" not a security proof?
2. Map LLM06 Excessive Agency to one LAB-20 control and one residual risk.
3. Which OWASP categories in the table have no lab test, and why does that matter?
4. What does a MITRE ATLAS technique mapping add to an OWASP mapping?
5. Why does an adaptive test matter more than a larger scripted suite?
6. Name two LLM-specific incident-response steps.

Answers are discussed in the [answer key](quiz-answers.md).

## Summary

- Layered defense assigns each control to a failure it can stop. More controls are not automatically better; each adds cost and false positives.
- OWASP LLM 2025 provides ten risk families. Mapping a test to a category is not coverage.
- MITRE ATLAS names techniques; NIST AI 100-2e2025 and the AI RMF provide taxonomy and governance. None certifies a system.
- Evaluation needs scope, version, benign utility, attack suite, adaptive cases, false positives, reproducibility, and residual risk.
- LAB-19 and LAB-20's layered configurations have attack success 0/8 and preserve 7/7 benign tasks. That is evidence about eight tests, not a production guarantee.
- Human factors — approval fatigue, automation bias, workarounds — are part of the defense.
- Incident response must fix authority and scope, not only the prompt.

## Next

Complete the [Module 15 quiz](quiz.md) and [exercises](exercises.md), then review the [Level 4 labs](../../labs/index.md) and the [capstone options](../../projects/capstone.md).
