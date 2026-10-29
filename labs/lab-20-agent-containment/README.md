# LAB-20 — Agent Containment and Approval Boundaries

| Field | Value |
|---|---|
| Lab ID | LAB-20 |
| Tier | A |
| Time | 3 hours |
| Difficulty | 4 of 4 |
| Module | M15 — Generative AI and Agents |
| Outcomes | LO-27, LO-28 |
| Prerequisites | M15 lessons 3–6; M11 lessons 4–6; M03 |
| Data | in-memory workspace |
| Compute | CPU only; milliseconds |

Full brief: [docs/labs/lab-20.md](../../docs/labs/lab-20.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

A mock agent is given a small tool set: read a workspace file, evaluate arithmetic,
queue a mock email, fetch a mock URL, and (in the unscoped configurations) delete a
workspace file. All files are held in memory, the outbox is synthetic, and the
fetch tool never uses the network.

The agent is a scripted planner, not a language model. One attack supplies a
fetched page containing an instruction to email the workspace notes. The agent
naively proposes the email, and the enforcement layer decides whether tool output
can authorize it.

You compare four policies: no controls, capability scoping plus egress allowlists,
an approval gate, and all controls layered.

| Policy | Benign | Attacks | Denied steps | Log |
|---|---:|---:|---:|---|
| baseline | 4/4 | 5/5 | 0 | ok |
| scoped | 4/4 | 1/5 | 4 | ok |
| approval | 4/4 | 2/5 | 3 | ok |
| layered | 4/4 | 0/5 | 5 | ok |

Scoping blocks the out-of-workspace read, the external email, the non-allowlisted
fetch, and the unregistered delete tool. It does not stop the injected email,
because the recipient is internal and scoping does not ask who authorized the
action. The approval gate refuses the external email, the delete, and any action
authorized only by tool output, but without scoping it leaves the confidential
read and the non-allowlisted fetch open. Only the layered policy blocks all five
attacks in this mock.

That result is not a proof of containment. Approval fatigue, allowlist mistakes,
a compromised tool, and log storage outside the hash chain are residual risks
covered in the module.

Every decision is appended to a hash-chained action log, and the checker verifies
the chain. No real file, mailbox, network, credential, or destructive action is
used.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab20.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab20.py --artifacts artifacts
```

## What you produce

- `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- Benign success, attack success, denied steps, and log verification for all four policies.
- The hash-chained action log and its verification result.
- `report.md` answers every reflection question and lists residual containment risks.
- `python check_lab20.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `decide` | Enforce capability, path, egress, and approval boundaries |
| `starter.py` | TODO 2 | `path_allowed` | Allow only resolved paths inside the workspace |
| `starter.py` | TODO 3 | `safe_calculate` | Evaluate arithmetic without `eval` or `exec` |

## Hints

- `decide` enforces capability, path, egress, and approval boundaries. Check the authorization source, not only the action name.
- Path confinement resolves the path and checks that it is inside the workspace; string prefix checks are not enough.
- `safe_calculate` must parse a restricted grammar, not call `eval` or `exec`.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab20.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
