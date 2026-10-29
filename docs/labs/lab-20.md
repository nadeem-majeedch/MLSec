# LAB-20 — Agent Containment and Approval Boundaries

**Tier A · 3 hours · Difficulty 4 · Module M15 · Outcomes LO-27, LO-28**

## Why this lab exists

A tool-using agent turns text into actions. That is the point of an agent, and it
is also the security problem. A model that can read a file, send a message, or
fetch a URL has authority, and authority can be delegated, confused, or
exceeded. The important question is not whether the agent "understands" that an
instruction is malicious. It is whether the enforcement layer lets the requested
action happen.

This lab builds a mock agent with harmless local tools: an in-memory file
workspace, a calculator, a mock email outbox, and a mock fetch tool with an
allowlist. A fifth tool, delete, exists only in the unscoped configurations. Four
benign tasks and five scripted attacks run under four policies. The reference
result is a containment story: the baseline allows all five attacks, capability
scoping stops four but not an untrusted tool output, an approval gate stops three
but leaves path traversal and non-allowlisted fetch open, and the layered policy
blocks all five in this mock. None of that proves an arbitrary agent is contained.

## The system and the threat model

| Element | Assumption |
|---|---|
| Asset | Workspace files, the mock outbox, network egress, destructive file operations, and the audit log |
| Attacker goal | Read outside the workspace, exfiltrate content, trick the agent into a mutating action, or delete a file |
| Attacker knowledge | The tool schema, allowlist behavior, and the approval flow |
| Attacker capability | Submit tasks, request tools, and inject content into a fetched page |
| Constraints | In-memory VFS, two allowlisted recipients, one allowlisted host, four benign tasks, five attacks, ten scripted steps per policy |
| Metric | Benign task success, attack success, denied steps, approvals granted, tool-output denials, hash-chain integrity |
| Lifecycle stage | Agent runtime and action authorization |
| Out of scope | Real model planning, OS sandboxing, real network, real credentials, multi-turn escalation, side channels, signed approvals, compromised tool runtime |

The agent is a scripted planner, not a language model. It follows a step list,
including a step derived from an untrusted fetched page. The tools are Python
functions over in-memory data. No real file, mailbox, or network is touched. The
lab tests the enforcement layer, not the model's judgment.

## What you produce

A folder inside `labs/lab-20-agent-containment/` containing:

| File | Contents |
|---|---|
| `metrics.json` | Workspace, allowlists, four policy results, per-attack decisions, log statistics |
| `run.json` | Lab id, policy list, benign tasks, attacks, full tool set |
| `report.md` | Setup, results, excessive-agency analysis, residual risks, limitations |
| `manifest.json` | SHA-256 hashes of the three files above |

The reference implementation writes these under `artifacts/`. Your completed
`starter.py` must produce the same structure.

## Prerequisites

- Module 15 Lessons 5–6 (agent authority, tools, approval, layered defense, evaluation).
- Module 15 Lessons 3–4 (retrieval boundaries and output handling).
- Module 11 Lessons 4–6 (logging, monitoring, incident response).
- Module 03 (threat modeling and trust boundaries).

## Environment

- Python 3.14.7; the standard library is sufficient.
- No network, cloud account, API key, real mailbox, or real filesystem access.
- The reference run finishes in milliseconds.
- No agent framework is required. LangChain, AutoGPT, or a hosted agent platform
  would add model planning, memory, and tool orchestration, but the enforcement
  layer would still need the checks you write here. This lab isolates that layer;
  it does not test framework bugs or model behavior.

```bash
cd labs/lab-20-agent-containment
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab20.py --artifacts artifacts
```

## Safety rules

- Use only the in-memory workspace, mock outbox, and synthetic fetched pages.
- Never point the mock fetch tool at a real URL, even if you replace it with a real client.
- Do not add real credentials, real recipients, or a real email sender.
- Do not deploy this agent or give it access to a real filesystem or network.
- Do not present the layered result as proof that an arbitrary agent is contained.

## Task specification

1. **Scope paths.** Normalize backslashes to forward slashes, reject absolute paths
   and drive letters, and allow only paths whose first component is exactly
   `workspace`. `../confidential.txt` must be rejected.
2. **Evaluate arithmetic safely.** Reject expressions longer than 80 characters,
   parse with `ast.parse(mode="eval")`, and evaluate only numeric constants and
   the operators supported by `limited_eval`. Reject booleans, names, calls,
   attributes, and unsupported syntax. Do not use `eval` or `exec`.
3. **Enforce the decision order.** Check the tool grant first, then path scope,
   then recipient allowlist, then host allowlist, then approval. Return a deny
   decision with a stable reason at the first failed check.
4. **Handle approval.** When approval is enabled and the tool mutates state, deny
   with `tool_output_cannot_authorize` if the request originated from tool output.
   Otherwise allow with `user_approved` only when the user approved; otherwise deny
   with `approval_denied`.
5. **Run benign tasks.** Read a workspace note, calculate `2 + 3 * 4`, send an
   approved internal email, and fetch an allowlisted page. All four must succeed
   under every policy.
6. **Run attacks.** Attempt a path traversal read, an external email, a
   non-allowlisted fetch, an action authorized by tool output, and an unapproved
   delete.
7. **Log every decision.** Append each step to a SHA-256 hash chain that includes
   the previous hash. Verify the chain after every task.
8. **Compare policies.** Run `baseline`, `scoped`, `approval`, and `layered` over
   the same tasks and tools.
9. **Report residual risk.** Explain excessive agency, delegated authority, the
   confused deputy, approval fatigue, allowlist mistakes, and log limitations.

## Control order

The order is part of the security design:

1. **Capability grant.** Is this tool in the policy's tool set? If not, deny with `tool_not_granted`.
2. **Path scope.** If the tool reads or deletes a file, does the normalized path stay inside `workspace/`? If not, deny with `path_outside_workspace`.
3. **Recipient allowlist.** If the tool sends email, is the recipient on the list? If not, deny with `recipient_not_allowlisted`.
4. **Host allowlist.** If the tool fetches a URL, is the hostname on the list? If not, deny with `host_not_allowlisted`.
5. **Approval.** If the tool mutates state and approval is enabled, was the request authorized by the user rather than by tool output? If not, deny with `tool_output_cannot_authorize` or `approval_denied`.
6. **Execute.** Only an allowed request reaches the tool.
7. **Log.** Append the decision, reason, origin, approval flag, and execution result to the hash chain.

Denying early is deliberate. A path traversal should be reported as a path
problem even if the request also lacks approval, because the reason is what an
auditor will use to distinguish a misconfigured tool from an attack.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `decide` | Enforce capability, path, egress, and approval boundaries |
| `starter.py` | TODO 2 | `path_allowed` | Allow only resolved paths inside the workspace |
| `starter.py` | TODO 3 | `safe_calculate` | Evaluate arithmetic without `eval` or `exec` |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-20-agent-containment/CHECKING.md`.

## Expected outputs

Reference results from the seed-42 run:

| Policy | Benign | Attacks | Denied steps | Approvals | Tool-output denials | Log integrity |
|---|---:|---:|---:|---:|---:|---|
| Baseline | 4/4 | 5/5 | 0 | 0 | 0 | ok |
| Scoped | 4/4 | 1/5 | 4 | 0 | 0 | ok |
| Approval | 4/4 | 2/5 | 3 | 1 | 1 | ok |
| Layered | 4/4 | 0/5 | 5 | 1 | 1 | ok |

Per-attack outcomes:

| Attack | Baseline | Scoped | Approval | Layered |
|---|---|---|---|---|
| Path traversal read | allow | deny: `path_outside_workspace` | allow | deny: `path_outside_workspace` |
| External email | allow | deny: `recipient_not_allowlisted` | deny: `approval_denied` | deny: `recipient_not_allowlisted` |
| Non-allowlisted fetch | allow | deny: `host_not_allowlisted` | allow | deny: `host_not_allowlisted` |
| Untrusted tool output | allow | allow | deny: `tool_output_cannot_authorize` | deny: `tool_output_cannot_authorize` |
| Excessive-agency delete | allow | deny: `tool_not_granted` | deny: `approval_denied` | deny: `tool_not_granted` |

Every policy records ten log entries and verifies its hash chain. The ten entries
are four benign steps plus six attack steps, because the untrusted-output attack
has two steps: fetch the page, then send the email.

The scoped policy is the clearest example of a partial control. It blocks the
out-of-workspace read, the external email, the non-allowlisted fetch, and the
unregistered delete tool. It still allows the injected email because the
recipient is on the approved internal list and scoping alone does not check who
authorized the action. The approval policy has the mirror-image gap: it blocks
mutating actions that the user did not approve and refuses tool-output authority,
but it leaves the read and fetch channels open.

## Threat-to-control mapping

| Threat | Evidence in the lab | Control tested | Residual risk |
|---|---|---|---|
| Path traversal | `../confidential.txt` is readable in the baseline | Path scope after normalization | Symlinks, encoding, and time-of-check/time-of-use gaps |
| Data exfiltration by email | External recipient receives the note | Recipient allowlist | An allowlisted recipient can be compromised or forward |
| Data exfiltration by fetch | Non-allowlisted host receives a query string | Host allowlist | Redirects, DNS rebinding, and allowlisted proxies |
| Confused deputy | Fetched page asks the agent to email notes | Approval origin check | A user can still be tricked into approving |
| Excessive agency | Delete tool is available by default | Tool grant and approval | Other granted tools may have destructive effects |
| Approval fatigue | Benign email needs approval | Approval gate | Users click through prompts |
| Log tampering | Every step is hash-chained | Tamper-evident log | The agent can rewrite the chain if it controls storage |

## Defense-in-depth perspective

Capability scoping limits what the agent can do. Path and egress allowlists limit
where it can do it. Approval limits when a mutating action may proceed, and the
origin check limits who may authorize it. The hash chain makes decisions
reviewable. These controls answer different questions, and each has a failure
mode the others do not cover.

The layers also depend on each other. An approval gate without an origin check
lets tool output authorize itself. A host allowlist without redirect handling can
be bypassed by an allowlisted host that redirects. A path check without
normalization is decorative. A log without external anchoring can be rewritten
by the same agent it is meant to constrain. The lab is designed so that the
layered policy is stronger than any single control, while still visibly
incomplete.

## Deliverables checklist

- [ ] `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] Benign success, attack success, denied steps, and log verification for all four policies.
- [ ] The hash-chained action log and its verification result.
- [ ] `report.md` answers every reflection question and lists residual containment risks.
- [ ] `python check_lab20.py --artifacts artifacts` exits 0.

## Success criteria

- [ ] `run.json` records the four policies in order, four benign tasks, five attacks, and the full tool set.
- [ ] The mock workspace includes the outside synthetic marker file.
- [ ] The recipient and host allowlists match the synthetic sets.
- [ ] Every policy completes all four benign tasks with zero false positives.
- [ ] Every policy records ten log entries with a valid hash chain.
- [ ] Baseline allows all five attacks.
- [ ] Scoped leaves exactly one attack successful, with the expected deny reasons for the other four.
- [ ] Approval leaves exactly two attacks successful, grants one benign approval, and records one tool-output denial.
- [ ] Layered blocks all five, with the expected deny reasons.
- [ ] The solution does not import a network client, subprocess, or use `eval`/`exec`.
- [ ] The report contains "excessive agency", "capability", "approval", "untrusted", "synthetic", and "limitations".
- [ ] `python check_lab20.py --artifacts artifacts` exits 0.

## How to check yourself

The checker validates the policy results, deny reasons, approval counts, log
integrity, and the report language. It also scans `solution.py` for forbidden
imports and `eval`/`exec`. It does not sandbox the agent or prove that the tool
implementations are safe. A different file could still contain a real network
client. The report and reflection questions carry the interpretation.

## Rubric (20 points)

| Item | Points |
|---|---:|
| Decision order and stable deny reasons | 5 |
| Path normalization and workspace scope | 2 |
| Recipient and host allowlists | 3 |
| Approval gate with origin check | 4 |
| Safe arithmetic without `eval` or `exec` | 2 |
| Hash-chained action log | 2 |
| Excessive-agency analysis and limitations | 2 |

## Reflection questions

1. Why does capability scoping stop four attacks but not the untrusted-output
   attack?
2. Why does the approval policy leave path traversal and non-allowlisted fetch
   open, even though both are clearly dangerous?
3. What does the origin check buy that a simple "is this action approved?" check
   does not?
4. Approval is a boolean flag in this lab. What would a real approval need to bind
   to, and why?
5. The hash chain verifies in every run. What does that prove, and what does it
   not prove?
6. Name three ways an allowlisted host or recipient could still be used for
   exfiltration.
7. How does approval fatigue turn a control into a vulnerability?
8. What would you add before giving an agent any real tool in a production
   environment?

## Hints

1. `decide` enforces capability, path, egress, and approval boundaries. Check the authorization source, not only the action name.
2. Path confinement resolves the path and checks that it is inside the workspace; string prefix checks are not enough.
3. `safe_calculate` must parse a restricted grammar, not call `eval` or `exec`.
4. Layer the controls, then test each policy separately. A control that only works when another is present is not independently effective.

## Time box

| Hour | Work |
|---|---|
| 1 | Read the mock tools and task suite; implement path scope and the decision order |
| 2 | Implement safe arithmetic and the approval gate; run all four policies |
| 3 | Inspect deny reasons and log integrity; write the residual-risk report |

Stop at 4.5 hours and submit with a note on what is incomplete.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `NotImplementedError` | A TODO block is untouched | Implement `decide`, `path_allowed`, or `safe_calculate` |
| Baseline denies an attack | A policy flag is enabled in the baseline | Keep all four baseline flags false |
| Scoped blocks the untrusted-output attack | Approval is enabled in the scoped policy | Scoped has no approval gate |
| Approval grants too many actions | Mutating tools set is wrong, or approval defaults to true | Use `send_email` and `delete_file`; default to false |
| Delete is allowed in scoped | `delete_file` is still in the scoped tool list | Use the four base tools only |
| `../confidential.txt` passes the path check | Normalization is skipped or the prefix test is wrong | Normalize first, reject absolute/drive paths, require `workspace/` |
| Calculator accepts `__import__` | `eval` is used, or `limited_eval` accepts calls | Use the AST evaluator and reject unsupported nodes |
| Log integrity fails | A record was modified after hashing, or fields were added later | Append immutable records with the previous hash |
| Report rejected | Missing a required phrase | Discuss excessive agency, capability, approval, untrusted output, and limitations |

## Cleanup

```bash
# Windows PowerShell
Remove-Item -Recurse -Force artifacts
# macOS/Linux
rm -rf artifacts
```

Remove the virtual environment if you created one for this lab. Never commit `artifacts/`.

## References

- [Lab catalog](../lab-catalog.md) · [Learning outcomes](../learning-outcomes.md)
- [References](../references.md) — F-08, F-15, R-85, R-86
- [Module page](../modules/m15-genai-llm-agents/index.md) — M15 — Generative AI, LLM, RAG, and AI Agent Security
- Package checking guide: `labs/lab-20-agent-containment/CHECKING.md`

## What comes next

This is the last numbered lab. Module 15 Lesson 6 connects the RAG and agent
results to OWASP, MITRE ATLAS, and NIST terminology. From here the course turns
from individual techniques to integration:

- [Module 16 — End-to-End ML Security Assessment](../modules/m16-end-to-end-assessment/index.md) turns this lab's evidence into one assessment of a complete system, using a project from the [project catalog](../projects/index.md).
- [Module 17 — ML Red-Team and Blue-Team Simulation](../modules/m17-red-team-blue-team/index.md) runs [RT-01](../projects/rt-01-red-blue.md), where a hostile document path and excessive tool authority become red-team objectives and blue-team detections.
- [Module 18](../modules/m18-capstone-and-research/index.md) and the [capstone](../projects/capstone.md) are where a tested boundary becomes a defended conclusion.
