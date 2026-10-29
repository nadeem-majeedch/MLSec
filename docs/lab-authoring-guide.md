# Lab Authoring Guide

| Field | Value |
|---|---|
| Document | Rules for writing, reviewing, and validating ML-Sec labs |
| Version | 1.0 |
| Date | 2026-10-28 |
| Applies to | LAB-01, LAB-01B, LAB-02–LAB-20 |
| Companion documents | [Lab template](lab-template.md) · [Lab catalog](lab-catalog.md) · [Validation report](lab-validation-report.md) |

This guide is for anyone adding or changing a lab. It states the contract the published labs follow, the reasons behind it, and the checks a lab must pass before it enters navigation. The template in [lab-template.md](lab-template.md) is the copyable form.

## 1. Architecture decision: keep the flat lab packages

The repository keeps one package per lab at `labs/lab-XX-name/`, with the student brief at `docs/labs/lab-XX.md`. It does **not** use `labs/level-1/`, `labs/level-2/`, or per-lab `notebooks/` directories.

This is deliberate:

- Every starter imports the shared helpers through `Path(__file__).resolve().parents[1] / "shared"`. A level directory would add one path segment and break all 20 imports at once.
- Every README links to `../../docs/labs/lab-XX.md`. Moving packages changes every local link.
- The lab identifier already carries the learning order. `LAB-03` belongs to Module 04; a second directory level would duplicate the module map without adding information.
- The catalog and module pages are the navigation layer. Directory depth is not a teaching device.
- A flat tree makes the validation script's job unambiguous: one directory, one lab ID, one README, one checker.

Datasets are not stored in a top-level `datasets/` tree. Labs that need data either use a bundled scikit-learn dataset or generate deterministic synthetic data in the lab package. `datasets/README.md` records that policy and the dataset registry. Storing generated CSV files would add large, unnecessary artifacts and create a second source of truth.

The repository-level layout is therefore:

```text
labs/
  shared/                    # pinned requirements and small helper package
  lab-01-environment/
  lab-01b-evaluation-audit/
  lab-02-threat-model/
  ...
  lab-20-agent-containment/
datasets/                    # policy and registry only; no generated data
requirements/                # consolidated pinned environments
scripts/                     # lab and link validation
tests/                       # lightweight tests for the validation tooling
docs/labs/                   # student briefs
docs/lab-authoring-guide.md
docs/lab-template.md
docs/lab-validation-report.md
```

## 2. The eleven-part lab contract

Every student brief contains these elements. The table gives the canonical heading; a lab may add headings, but it may not omit one.

| # | Required element | Canonical location in the brief |
|---:|---|---|
| 1 | Lab ID, title, difficulty, time, prerequisites | H1 title; metadata line (`Tier · hours · Difficulty · Module · Outcomes`); `## Prerequisites` |
| 2 | Scenario and learning objectives | `## Why this lab exists`; `## What you produce`; outcomes in the metadata line |
| 3 | Threat model, scope, and safety boundaries | `## The system and the threat model`; `## Data and safety` or `## Safety rules` |
| 4 | Environment setup | `## Environment` or `## Data and environment` |
| 5 | Starter code and marked TODOs | `## Starter and TODO map` |
| 6 | Step-by-step tasks with expected observations | `## Task specification`; `## Expected outputs` |
| 7 | Tests or measurable success criteria | `## Success criteria`; `## How to check yourself` |
| 8 | Interpretation questions | `## Reflection questions` |
| 9 | Deliverables checklist | `## Deliverables checklist` |
| 10 | Hints and a separate checking guide | `## Hints`; package `CHECKING.md` |
| 11 | Troubleshooting and references | `## Troubleshooting`; `## References` |

A brief that has all eleven but no runnable package is not a lab. A package that runs but has no brief is not publishable either.

### 2.1 Metadata line

Use one line immediately under the H1:

```markdown
**Tier A · 4 hours · Difficulty 3 · Module M04 · Outcomes LO-05, LO-06, LO-07, LO-28**
```

- **Tier A** is laptop-only and CPU-only, with a reference run of ten minutes or less. **Tier B** is still CPU-only but ships a reduced configuration for a longer or heavier reference run. Neither tier requires a GPU.
- Hours are guided time for a learner who reads the prerequisites. They are not a deadline.
- Difficulty is 1 (guided) to 5 (research-grade), using the scale in [lab-catalog.md](lab-catalog.md). It measures conceptual and debugging load, not length. Published labs use 1–4.
- Outcomes must match [learning-outcomes.md](learning-outcomes.md) and [lab-catalog.md](lab-catalog.md). When the two disagree, the catalog and the outcomes document win, and the brief is corrected.
- Prerequisites belong in `## Prerequisites`, not in the metadata line. Name the prerequisite lab and the module lessons.

### 2.2 Learning objectives

State what the learner can do at the end, in verbs that produce an artifact: measure, implement, compare, audit, harden, explain with evidence. "Understand" is not an objective because it cannot be checked.

Each lab maps to at least one LO. The lab may support an LO without being its primary assessment; mark that as `LO-30 (supporting)` in the metadata and explain the relationship in the brief.

## 3. Package contract

Every lab directory contains the following files. Optional files are listed after the required set.

| File | Required | Purpose |
|---|---|---|
| `README.md` | yes | Local quickstart: metadata, scenario, run commands, deliverables, starter map, hints, files, safety, cleanup |
| `starter.py` | yes, except LAB-02 | Learner scaffold with marked TODOs that raise `NotImplementedError` |
| `solution.py` | yes, except LAB-02 | Reference implementation, runnable with the same CLI |
| `check_*.py` | yes | Independent artifact checker; never imports `solution.py` |
| `expected_*.json` | yes | Reference values and tolerances in machine-readable form |
| `requirements.txt` | yes | Imports the pinned shared stack, or pins the minimal exception |
| `CHECKING.md` | yes | What the checker verifies, reference results, failure diagnosis, rubric, reflection prompts |
| `report_template.md` | where a written report is required | Headings and prompts; never pre-filled conclusions |
| Generator (e.g. `make_dataset.py`, `dataset.py`, `project.py`) | optional | Deterministic fixture builder; must be seeded and local |
| `threat-model.yaml`, `report.md`, `solution.yaml`, `solution-report.md` | LAB-02 only | YAML/report lab replaces the Python starter/solution pair |

Names are part of the contract. A checker called `check_lab17.py` is expected to accept `--artifacts`; a generator called `make_dataset.py` is expected to accept `--out`.

### 3.1 Starter, solution, checker separation

The three roles must stay separate:

1. **Starter** contains the task scaffold, constants, data loading, metric definitions that are part of the contract, and TODOs. It must run far enough to fail at the first missing piece with a clear `NotImplementedError`, not with a `NameError` three functions later.
2. **Solution** is a complete implementation. It may share data loading and metric code with the starter, but it must not be imported by the checker.
3. **Checker** rebuilds the deterministic model, split, or fixture from the public description and verifies the learner's artifacts. It must not trust values recorded in `metrics.json` when it can recompute them. It exits non-zero with `FAIL: <reason>` on the first failed check and prints `LAB-XX CHECK PASSED` on success.

Do not add a hidden "solution mode" to the starter. Do not have the checker compare a learner artifact against `solution.py` output by running the solution. That would make the checker a regression test for one implementation, not an independent check of the task.

### 3.2 TODO conventions

- Mark each TODO with a numbered label (`TODO 1`, `TODO 2`, …) and a one-line statement of the required behavior.
- Put the TODO on the function that the learner must implement, not on the call site.
- Keep the number of TODOs small enough to finish in the time tier. The published range is one (LAB-05) to four (LAB-08).
- The starter's docstring states the command to run and the number of TODOs.
- A hint may describe the shape, the invariant, or the failure mode. It may not be the completed expression.
- The checker must fail on a partly completed starter. Test this by running the checker against an empty or partial artifact directory, not by trusting the `NotImplementedError`.

## 4. Reproducibility rules

### 4.1 Python and dependencies

- Supported interpreter: **Python 3.14.7**. The repository records this in `.python-version`.
- The shared stack is pinned in `labs/shared/requirements-level1.txt`: NumPy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0, joblib 1.5.3, PyYAML 6.0.3.
- A lab's `requirements.txt` normally contains exactly `-r ../shared/requirements-level1.txt`. LAB-02 is the documented exception because it needs only PyYAML; it pins `PyYAML==6.0.3` directly.
- The consolidated file `requirements/labs.txt` repeats the same pins for readers who want one install command. It must stay in sync with the shared file; the validation script checks the pin sets.
- Do not add a dependency to one lab because it was convenient. If a lab needs a new package, add it to the shared file, record why, and verify every lab still runs.
- A different interpreter version is allowed only if the learner records it in `run.json`; results from mixed environments must not be compared.

### 4.2 Determinism

- Every random operation takes an explicit seed. The seed appears in the starter, the solution, the checker, and `expected_metrics.json`.
- Splits are deterministic: fixed `random_state`, fixed test fraction, and `stratify=` where class balance matters.
- Generated data is a pure function of its seed. LAB-01B prints the CSV hash; a changed hash means a changed fixture.
- Expected values are ranges with stated tolerance, not false precision. A checker may require an exact count for a structural property (five budget rows, 49 patch positions) and a tolerance for a measured metric.
- A learner's run must be comparable across machines. If a result depends on BLAS threading or platform floating point, widen the tolerance and say so in `CHECKING.md`.

### 4.3 Compute and artifacts

- Default labs are CPU-only and finish in seconds to a few minutes on a laptop. Tier A target: under 10 minutes for the reference run. LAB-11 (about two minutes) is the slowest published reference run.
- Do not commit generated datasets, model binaries, logs, or `artifacts/`. `.gitignore` covers virtual environments, `artifacts/`, `data/`, caches, and checkpoints.
- A generator that produces a fixture writes it under `--out`, never into the package or repository root.
- Every lab has a cleanup instruction: remove `artifacts/`, deactivate the virtual environment, and restore any starter file that the learner edited. LAB-02 learners restore `threat-model.yaml` and `report.md` from the templates.
- No secrets, tokens, credentials, private data, or real endpoints. Demo tokens in LAB-14 are explicitly non-secrets and must not be reused.

### 4.4 Notebooks

There are no notebooks in the published course. A notebook is added only when interactive inspection is the learning objective, not when it is a convenient container for code. If one is added:

- it must have a script equivalent that the checker and CI can run headlessly;
- it must execute top-to-bottom in a clean environment with a bounded timeout;
- outputs must be cleared before commit, except small textual outputs that are part of the explanation;
- it must not download data, call a network service, or require a GPU;
- it must be listed in the README and in the lab metadata.

The validator checks notebook JSON structure and optional execution. It does not execute unknown notebooks by default.

## 5. Data policy

1. **Bundled public data** — scikit-learn `load_digits` is the default. It ships with the pinned dependency, so there is no download and no license surprise for the learner.
2. **Programmatic synthetic data** — preferred for tabular, churn, federation, privacy, fairness, RAG, and agent labs. The generator lives in the lab package, is seeded, and writes only under `--out`.
3. **No repository datasets** — do not add CSV, NPZ, image, or model files to the repository. `datasets/README.md` is a policy and registry, not a data store.
4. **External datasets** — allowed only with a documented license, a stable access path, and an offline fallback. They are not used by the 21 published labs. A lab that adds one must record the license, the version, the checksum, the download command, and the fallback in its README.
5. **No personal or private data** — never substitute a real customer extract, patient record, user log, or proprietary model for a synthetic fixture. The safety section of each brief states the boundary in the lab's own terms.

## 6. Safety boundaries

Every offensive lab states:

- the target is a model, file, or service the learner owns and runs locally;
- the data is public, synthetic, or explicitly licensed;
- no external service, real credential, real person, or production system is contacted;
- the result does not generalize to a named product or deployment;
- any generated malicious-looking artifact is benign, bounded, and deleted with `artifacts/`.

LAB-13 (pickle canary), LAB-14 (local API), LAB-19 (prompt injection), and LAB-20 (agent tools) carry the strongest boundaries because their subject matter looks like real offensive capability. Their briefs include a `## Safety rules` section and their checkers verify containment properties. A lab that cannot state a local, bounded target does not ship.

## 7. Brief and README conventions

### 7.1 Student brief (`docs/labs/lab-XX.md`)

- The H1 is `LAB-XX — Title`; the metadata line follows immediately.
- `## Why this lab exists` gives the decision the learner will be able to make, not a table of contents.
- `## The system and the threat model` states assets, actor, knowledge, capability, access, and success metric.
- `## Task specification` is numbered and observable. Each task says what to run and what to look at.
- `## Expected outputs` gives the artifact names and the shape of the result, with reference values where the lab has them. It does not give the learner's conclusions.
- `## Success criteria` is a checklist of observable conditions.
- `## Reflection questions` asks for interpretation, comparison, limitation, or a counterfactual. At least one question must ask what the result does **not** show.
- `## Deliverables checklist` lists files and report contents.
- `## Hints` is progressive: a nudge, then a diagnostic, then a pointer to the relevant concept. It never contains the full answer.
- `## Troubleshooting` maps symptom → likely cause → fix.
- `## References` links to the course reference list and the relevant module. External URLs belong in [references.md](references.md), where they are versioned and checked.
- `## What comes next` links to the next lab or module.

### 7.2 Local README (`labs/lab-XX-name/README.md`)

The README is a quickstart, not a second brief. It contains:

1. title and a metadata table (ID, tier, time, difficulty, module, outcomes, data, compute);
2. a link to the full brief and to `CHECKING.md`;
3. the scenario in two or three sentences;
4. copy-paste run commands for the reference path and the learner path;
5. what the learner produces;
6. the starter/TODO map;
7. three or four hints;
8. the file table;
9. safety and cleanup.

It does not repeat the full task specification, the rubric, or the reference results. Those live in the brief and `CHECKING.md`.

### 7.3 Checking guide (`CHECKING.md`)

The checking guide is the separate solution-facing document. It contains:

- what the checker verifies, in the order it verifies it;
- reference results with seed and tolerance;
- common failures and their causes;
- the rubric with point totals;
- the reflection questions and what a strong answer covers.

It may reveal expected values. It must not contain a line-by-line copy of `solution.py`.

## 8. Checker rules

- **Independent**: rebuild the split, model, or fixture; do not import the solution.
- **Specific**: fail with the file, the field, and the observed versus expected value.
- **Bounded**: no network, no GPU, no writes outside `--artifacts`, no sleeps longer than a few seconds.
- **Deterministic**: same input, same verdict. If a check is statistical, state the tolerance and why.
- **Structural before numerical**: missing files and malformed JSON fail before model refitting.
- **Containment-aware**: for LAB-13, LAB-14, LAB-19, and LAB-20, verify the safety property (no pickle load, loopback bind, no forbidden tool call, hash-chained log), not only the metric.
- **Exit codes**: 0 on pass, non-zero on fail. Print one line per passed group and a final `LAB-XX CHECK PASSED`.

The checker is not a grader of prose. It checks that required sections and claims are present; a human or rubric reviews quality.

## 9. Validation tooling

The repository provides:

```bash
python scripts/validate_labs.py --structural
python scripts/validate_labs.py --execute --timeout 600
python scripts/validate_labs.py --check-urls
python scripts/check_links.py
python -m unittest discover -s tests
```

- `--structural` (default) checks metadata, required files, Markdown links and anchors, Python compilation, expected-metric JSON shape, notebook structure, and required brief sections. It does not run lab code.
- `--execute` runs each completed lab's solution and checker in a temporary environment with a per-lab timeout. It is opt-in because it executes code and takes minutes.
- `--check-urls` probes external HTTP(S) links across the documentation. It is opt-in and never part of the default run.
- `check_links.py` resolves every internal link, anchor, and local asset in the documentation and lab READMEs.
- The unit tests cover the validator itself: metadata parsing, link resolution, anchor slugging, import extraction, and notebook structure checks.

The validator never executes a starter, an unknown notebook, or downloaded code. `--execute` runs only the repository's own reference solution and checker, or the LAB-02 reference checker and its two reference files.

## 10. Adding or changing a lab

1. Confirm the lab exists in [lab-catalog.md](lab-catalog.md) with an ID, module, tier, time, and outcomes. If it does not, add the catalog entry first.
2. Copy [lab-template.md](lab-template.md) to `docs/labs/lab-XX.md` and fill every section. Remove the template guidance comments.
3. Create `labs/lab-XX-name/` with the required package files. Use the shared requirements file.
4. Implement the starter TODOs, the solution, the independent checker, and `expected_metrics.json`.
5. Write `CHECKING.md` with reference results, failure diagnosis, rubric, and reflection answers.
6. Write the README quickstart and add the lab to `docs/labs/index.md`, the module page, and `mkdocs.yml` navigation.
7. Run `python scripts/validate_labs.py --structural`, then `--execute` for the new lab, then `mkdocs build --strict`.
8. Record the run in [lab-validation-report.md](lab-validation-report.md), including any check that was not executed and why.
9. Do not commit, publish, or deploy unless the owner has authorized that action separately.

When changing a lab, update `expected_metrics.json` and `CHECKING.md` in the same change. A changed reference number with an unchanged checking guide is an inconsistency, even if the checker still passes.

## 11. Review checklist

- [ ] Metadata line matches the catalog and the learning-outcomes document.
- [ ] All eleven brief sections are present and specific to this lab.
- [ ] Prerequisites name a lab or module lessons, not a generic skill list.
- [ ] Threat model names actor, knowledge, capability, access, and success metric.
- [ ] Safety section states the local, bounded target.
- [ ] Every TODO is numbered, described, and reachable.
- [ ] The starter fails loudly; the solution passes; the checker rejects a partial artifact.
- [ ] Seeds and expected ranges are recorded; the checker uses tolerances.
- [ ] `requirements.txt` uses the shared pin set or documents its exception.
- [ ] No network, GPU, secret, private data, or committed artifact is required.
- [ ] README run commands work from the lab directory.
- [ ] `CHECKING.md` is separate from the brief and does not paste the solution.
- [ ] Cleanup instructions remove generated artifacts and restore edited starters.
- [ ] References point to the course reference list and the relevant module.
- [ ] Validation report records structural and execution status separately.

## 12. Non-goals

This guide does not define the course's research claims, the capstone rubric, or the project assessments. It does not authorize publication, deployment, or committing generated artifacts. It does not replace the security review of an offensive lab; it only states the minimum safety contract.
