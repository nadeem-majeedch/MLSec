# Checking Guide — LAB-20

## What the checker verifies

1. `metrics.json`, `run.json`, `report.md`, and `manifest.json` exist, and the manifest covers the three output files.
2. `run.json` records LAB-20, the four policies in order, four benign tasks, five attacks, and the full mock tool set.
3. The workspace records the synthetic outside file `../confidential.txt`, and the recipient and host allowlists are the expected synthetic sets.
4. Every policy completes all four benign tasks, reports no benign false positives, logs ten steps, and passes its hash-chain check.
5. Baseline allows all five attacks and logs no denials.
6. Scoping blocks the path, external-recipient, non-allowlisted-host, and unregistered-tool attacks, but leaves the tool-output email successful.
7. The approval gate blocks the external email, the delete, and the tool-output-authorized send, but leaves the path read and non-allowlisted fetch successful.
8. The layered policy blocks all five attacks with the expected reason codes.
9. The approval and layered policies grant exactly one approval (the benign internal email) and record exactly one tool-output denial.
10. `solution.py` contains no network client, subprocess import, `eval`, or `exec`.
11. The report contains "excessive agency", "capability", "approval", "untrusted", "synthetic", and "limitations".

## Reference results

| Policy | Benign | Attacks | Denied steps | Approvals granted | Tool-output denials | Log |
|---|---:|---:|---:|---:|---:|---|
| baseline | 4/4 | 5/5 | 0 | 0 | 0 | ok |
| scoped | 4/4 | 1/5 | 4 | 0 | 0 | ok |
| approval | 4/4 | 2/5 | 3 | 1 | 1 | ok |
| layered | 4/4 | 0/5 | 5 | 1 | 1 | ok |

Per-attack outcome (hit / blocked with reason):

| Attack | baseline | scoped | approval | layered |
|---|---|---|---|---|
| path_traversal_read | hit | blocked: path_outside_workspace | hit | blocked: path_outside_workspace |
| external_email | hit | blocked: recipient_not_allowlisted | blocked: approval_denied | blocked: recipient_not_allowlisted |
| non_allowlisted_fetch | hit | blocked: host_not_allowlisted | hit | blocked: host_not_allowlisted |
| untrusted_tool_output | hit | hit | blocked: tool_output_cannot_authorize | blocked: tool_output_cannot_authorize |
| excessive_agency_delete | hit | blocked: tool_not_granted | blocked: approval_denied | blocked: tool_not_granted |

## Why these numbers matter

The baseline is the excessive-agency case: the agent holds a delete tool it does
not need for its task, can read outside its workspace, can contact any recipient,
and treats a fetched page as an instruction source. Every attack succeeds.

Scoping is a capability and egress control. It reduces the attack surface but is
not an authorization control: the injected email goes to an allowlisted internal
recipient, so the action passes. This is the key lesson of the lab. A control that
limits where an action can go does not establish that the action was requested by
the right principal.

The approval gate is an authorization control, and it explicitly refuses tool
output as an approver. On its own it still permits a read outside the workspace
and a fetch to a non-allowlisted host, because those capabilities were never
restricted.

The layered policy blocks all five attacks, but the honest conclusion is narrower:
this combination covers these five scripts in this mock. A poisoned trusted page,
an allowlisted-but-compromised recipient, approval fatigue, a compromised tool, or
a rewritten log would change the result. The hash chain is tamper-evident only if
its head is stored where the agent cannot rewrite it.

## Threat-to-control mapping

| Threat | Control tested | Metric | Residual risk |
|---|---|---|---|
| Out-of-workspace read | Path confinement | Denied read | Allowed path with sensitive content |
| Data exfiltration by email | Recipient allowlist | Denied send | Compromised allowlisted recipient |
| Contact with external host | Egress allowlist | Denied fetch | Allowlisted host serving malicious content |
| Indirect instruction in tool output | Origin-bound approval | Tool-output denial | Confused deputy through a trusted tool |
| Excessive agency | Tool grant list | Unregistered-tool denial | Over-broad grants within the list |
| Destructive action | Approval gate | Denied delete | Approval fatigue and mis-scoped approval |
| Log rewriting | Hash chain | Chain verification | Head not stored independently |

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| Scoped policy blocks the benign internal email | Recipient missing from the allowlist | Add `team@internal.test` to the synthetic allowlist |
| Path read succeeds under scoped | Confinement checks the raw string instead of the normalized path | Normalize, then require the first component to be `workspace` |
| Untrusted-output email succeeds under layered | Approval checks the recipient but not the origin | Deny mutating actions whose origin is `tool_output` |
| Approval policy blocks the benign email | `user_approval` is not set for the benign task | Set the flag on the benign task only |
| Log chain fails | A field was added after hashing or the previous hash is wrong | Hash the full record except `hash`, using the prior hash as `prev` |
| Delete attack succeeds under scoped | `delete_file` is still in the granted tool set | Remove it from the scoped tool list |
| Calculator uses `eval` | Shortcut implementation | Parse with `ast` and evaluate the allowlisted nodes only |

## Rubric

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
