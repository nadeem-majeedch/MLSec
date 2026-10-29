---
title: Lab Template
---

# LAB-XX — <Title>

Copy this file to `docs/labs/lab-XX.md`, replace every `<...>` placeholder, and delete the guidance lines. The rules behind each section are in [lab-authoring-guide.md](lab-authoring-guide.md). A lab is not publishable while any placeholder remains.

---

**Tier <A|B> · <N> hours · Difficulty <1–5> · Module <Mxx> · Outcomes <LO-xx>, <LO-yy>**

<!-- One line. Outcomes must match lab-catalog.md and learning-outcomes.md. -->

## Why this lab exists

<The decision the learner will be able to make after the lab. Two short paragraphs: the situation, and why the artifact matters. Do not summarize the module.>

## The system and the threat model

| Element | Statement |
|---|---|
| System | <What is being attacked or audited> |
| Asset | <What the adversary wants: label, confidentiality, availability, integrity, budget> |
| Actor | <Who the adversary is> |
| Knowledge | <What the adversary knows: weights, architecture, data, query access> |
| Capability | <What the adversary can change or submit, with limits> |
| Access | <Local process, local API, files, query budget> |
| Success metric | <ASR, fidelity, leakage, false-positive rate, audit finding, etc.> |
| Out of scope | <The real systems, data, or claims this lab does not cover> |

## Prerequisites

| Requirement | Check |
|---|---|
| <LAB-xx or module lessons> | <Observable check> |
| <Skill> | <Observable check> |

## Environment

```bash
cd labs/lab-XX-<name>
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

- Supported interpreter: Python 3.14.7.
- CPU only; <reference runtime> on a laptop.
- No network, no cloud account, no API key.
- <Any generator command the learner must run first.>

## Data and safety

<Data source, size, license or synthetic provenance. State the safety boundary: local model, synthetic data, no real service, no personal data. State what the learner must not substitute.>

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `<function>` | <Behavior> |
| `starter.py` | TODO 2 | `<function>` | <Behavior> |

Run the reference path first to see a complete artifact set:

```bash
python solution.py --out artifacts
python check_labXX.py --artifacts artifacts
```

Then complete `starter.py` and check your own output. The reference solution is separate from the checker; reading it before attempting the TODOs removes most of the learning value.

## Task specification

1. **<Task name>.** <What to run or implement, what input to use, and what to record.>
2. **<Task name>.** <...>
3. **<Task name>.** <...>

## Expected outputs

| Artifact | Contents |
|---|---|
| `artifacts/metrics.json` | <Required fields and shapes> |
| `artifacts/run.json` | Lab ID, seed, environment |
| `artifacts/report.md` | <Required headings> |
| `artifacts/manifest.json` | Hashes of the other artifacts |

<Reference values with seed and tolerance, or the expected qualitative shape when the lab has no single reference number.>

## Success criteria

- [ ] <Observable condition>
- [ ] <Observable condition>
- [ ] The checker exits 0.
- [ ] The report states a limitation of the result.

## Reflection questions

1. <Question that requires interpreting a measured result.>
2. <Question that compares two conditions.>
3. <Question that asks what the result does not show, or how an adaptive adversary would change it.>
4. <Question that connects the result to a defense or deployment decision.>

## Deliverables checklist

- [ ] Completed `starter.py` with all TODOs implemented.
- [ ] `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] <Lab-specific artifact, e.g. validation report, hardened tree, incident playbook.>
- [ ] Written answers to the reflection questions in `report.md`.
- [ ] Checker output showing `LAB-XX CHECK PASSED`.

## Hints

<Progressive hints: a nudge, a diagnostic, a concept pointer. Do not give the completed expression.>

1. <Nudge>
2. <Diagnostic: what a wrong result usually means>
3. <Pointer to the module lesson or reference>

## How to check yourself

```bash
python check_labXX.py --artifacts artifacts
```

<What a pass means and what it does not mean. Link to `labs/lab-XX-name/CHECKING.md` for reference results, failure diagnosis, and the rubric.>

## Time box

| Time | Work |
|---|---|
| <First block> | <Work> |
| <Second block> | <Work> |
| <Third block> | <Work> |

If you pass <2× the estimate>, stop and submit what you have with a note on what is incomplete.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `NotImplementedError` | TODO untouched | Implement the named function |
| <Symptom> | <Cause> | <Fix> |
| `ModuleNotFoundError` | Virtual environment not active or requirements not installed | Activate `.venv` and reinstall `requirements.txt` |

## Cleanup

```bash
# Windows PowerShell
Remove-Item -Recurse -Force artifacts
# macOS/Linux
rm -rf artifacts
```

<Restore any starter file edited in place. Deactivate the virtual environment. Never commit `artifacts/`.>

## References

- [Lab catalog](lab-catalog.md)
- [Learning outcomes](learning-outcomes.md)
- [References](references.md) — <IDs used by this lab, e.g. R-11, R-18>
- [Module index](modules/index.md) — replace with `<Mxx>` and its directory

## Rubric

| Item | Points |
|---|---:|
| <Criterion> | <Points> |
| **Total** | **<Total>** |

## What comes next

<Link to the next lab, module, or project and state the connection in one sentence.>

---

## Package checklist

Create `labs/lab-XX-<name>/` with:

- [ ] `README.md` — metadata table, scenario, run commands, deliverables, starter map, hints, files, safety, cleanup.
- [ ] `starter.py` — numbered TODOs raising `NotImplementedError`.
- [ ] `solution.py` — complete reference implementation.
- [ ] `check_labXX.py` — independent checker with `--artifacts`.
- [ ] `expected_metrics.json` — seed, values, tolerances.
- [ ] `requirements.txt` — `-r ../shared/requirements-level1.txt` unless documented otherwise.
- [ ] `CHECKING.md` — what is checked, reference results, failures, rubric, reflection guidance.
- [ ] `report_template.md` — when a written report is required.
- [ ] Generator — when the lab needs a deterministic fixture.

## README skeleton

```markdown
# LAB-XX — <Title>

| Field | Value |
|---|---|
| Lab ID | LAB-XX |
| Tier | <A|B> |
| Time | <N> hours |
| Difficulty | <1–5> of 5 |
| Module | <Mxx> |
| Outcomes | <LO-xx>, <LO-yy> |
| Data | <Source> |
| Compute | CPU only; <runtime> |

Full brief: [docs/labs/lab-XX.md](../../docs/labs/lab-XX.md).
Checking guide: [CHECKING.md](CHECKING.md).

## Scenario

<Two or three sentences.>

## Run

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_labXX.py --artifacts artifacts
```

## What you produce

<Short list.>

## Starter and TODO map

<Short table.>

## Hints

<Three or four progressive hints.>

## Files

<Table.>

## Safety and cleanup

<Local target statement and artifact removal.>
```
