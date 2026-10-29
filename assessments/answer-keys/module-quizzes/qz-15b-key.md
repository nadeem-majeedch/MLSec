# QZ-15B Answer Key — Module 15

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. B — code-level tool scopes, approval, and egress rules

The authorization boundary is the code that decides whether an action is permitted, not the text the model reads or writes. A tool should enforce its own scope, recipient allowlist, amount limit, and approval requirement. Prompt instructions shape behavior; they do not enforce it.

- **A** and **C** are probabilistic mitigations that can be bypassed.
- **D** is a confidence score, not an authorization decision.

Tag: M15 · LO-27 · Bloom 2 · D1.

## 2. C — LLM06 Excessive Agency

The OWASP Top 10 for LLM Applications 2025 places over-broad tools, permissions, and autonomy under LLM06 Excessive Agency. The control is capability scoping plus approval and budgets, not a better system prompt.

- **LLM01** is prompt injection.
- **LLM05** is improper output handling.
- **LLM09** is misinformation.

Tag: M15 · LO-25 · Bloom 2 · D1.

## 3. False

A system prompt is an instruction to a probabilistic model, not an enforcement mechanism. It can be ignored, paraphrased around, or overridden by injected content. The restriction must be enforced in the tool or gateway: an allowlist of recipients, scope checks, approval, and egress control.

Tag: M15 · LO-27 · Bloom 2 · D1.

## 4. True

Output handling is context-specific. HTML needs encoding or sanitization, SQL needs parameterized queries, and a shell needs argument separation and allowlisting. A single "sanitize the output" step is not sufficient across destinations; the control belongs at the sink.

Tag: M15 · LO-27 · Bloom 2 · D1.

## 5. Required element

A refusal is a model behavior, not an access-control decision. It can be bypassed by paraphrase, encoding, role-play, or an indirect injection, and it cannot guarantee that a tool call never occurs. Authorization must be enforced by the code that owns the capability, with the model treated as an untrusted planner.

Tag: M15 · LO-27 · Bloom 3 · D2.

## 6. Required elements (two controls and one residual risk)

Controls such as:

- **`refund` cap in code:** reject amounts above 500 server-side and require a second approver for any exception; the model cannot raise its own limit.
- **`send_email` recipient allowlist:** restrict to approved internal or customer domains, block external addresses, and require human approval for first-time recipients.
- **Instruction hierarchy and provenance:** treat retrieved vendor content as data, not authority; the page cannot grant itself permission.
- **Logging and approval:** record the proposed action, the approving identity, and the tool result; require confirmation for high-impact actions.

Residual risk: an allowlisted account can be compromised, a human approver can be socially engineered, a trusted document can be poisoned, or the refund tool can have a logic bug that bypasses the cap. Name one and state the monitoring or review that would catch it.

Tag: M15 · LO-27 · Bloom 4 · D3.

## 7. Required elements (two flaws and the injection consequence)

Two of:

- **No recipient restriction.** `to` is fully attacker-controlled; the agent can send to any address.
- **No authentication, approval, or scope check.** The function executes whatever the agent asks, and the model is not an authorization authority.
- **No content or egress control.** The body can carry sensitive workspace data, and there is no DLP or size limit.
- **No logging or rate limit.** Abuse is harder to detect and can be repeated.

An indirect prompt injection in a retrieved document can instruct the agent to call `send_email` with an external recipient and exfiltrate workspace content. Because the tool enforces nothing, the model's compliance is sufficient for the action to succeed.

Tag: M15 · LO-27 · Bloom 4 · D3.

## 8. Required elements (four controls, success metric, benign evaluation, two risks)

Controls such as:

1. **Ingest provenance and trust labels:** mark synthetic vendor documents as untrusted data; quarantine or strip active instructions; keep a source inventory.
2. **Instruction hierarchy and delimiters:** retrieved content is data, not authority; the system policy and developer instructions outrank it.
3. **Least-privilege tools:** `create_ticket` accepts only validated fields; no email or file-write tool; the tool enforces project and tenant scope.
4. **Output and action validation:** validate ticket fields, encode output for its destination, and require human approval for high-impact actions.
5. **Canary and monitoring:** place canary strings in documents to detect exfiltration; log tool calls and alert on anomalous ones.

Success metric: attack success on a fixed set of synthetic injected documents, with the denominator stated, plus task completion on benign documents. Benign evaluation: run a set of legitimate vendor documents and measure false positives (blocked or altered benign tasks) as well as completion.

Two risks: a novel paraphrase or encoding can evade filters; a trusted source can be poisoned; the tool implementation can have a bug; a model update can change behavior; approval fatigue can lead to rubber-stamping. The result is scoped to the tested documents and local replica, not a claim that the assistant is secure.

Tag: M15 · LO-26 · Bloom 5 · D3.
