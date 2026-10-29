# Lab Validation Report

| Field | Value |
|---|---|
| Document | Structural and execution validation of every published lab |
| Date | 2026-10-28 |
| Scope | LAB-01, LAB-01B, LAB-02 through LAB-20 (21 packages, 21 briefs) |
| Environment | Windows 10 x64, Python 3.14.7, NumPy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0, joblib 1.5.3, PyYAML 6.0.3, CPU only |
| Structural result | **21 of 21 labs pass**; 148 lab-level checks and 34 repository-level checks; 0 failures, 0 warnings |
| Execution result | **21 of 21 reference paths pass**; 283.0 s total wall-clock; no timeouts |
| Unit tests | **16 of 16 pass** |
| Internal links | **0 broken** in 281 Markdown files after this report was added |
| External links | **221 probed: 210 reachable, 11 bot-blocked, 0 confirmed broken** |
| MkDocs strict build | **Pass** (after this report was added) |

This report separates what was checked statically from what was executed. A structural pass means the package, metadata, links, and source files are consistent; it does not prove the pedagogy or the security reasoning. An execution pass means the reference solution ran and its independent checker accepted the artifacts on this machine.

## 1. What was checked

### 1.1 Lab packages and metadata

For each of the 21 labs, `scripts/validate_labs.py` checks:

- discovery of the lab directory, its brief, and its catalog entry;
- the nine README metadata fields: Lab ID, tier, time, difficulty, module, outcomes, prerequisites, data, and compute;
- agreement between README, brief metadata line, and `docs/lab-catalog.md` on tier, hours, difficulty, module, and outcomes;
- README and brief section contracts, including scenario, threat model, environment, task specification, starter/TODO map, expected observations, deliverables, success criteria, checking, reflection, hints, time box, troubleshooting, rubric, cleanup, references, and next steps;
- the presence of `LO-28` in every lab's outcomes and the primary-outcome entry in the catalog;
- required package files: README, checking guide, requirements, starter and solution (or the LAB-02 threat-model files), expected-result JSON, and the independent checker;
- TODO markers in the learner files, and that `starter.py` is not a copy of `solution.py`;
- that checkers do not import `solution` or `starter`;
- Python compilation of every lab source file;
- an import allowlist: the standard library, the pinned stack (`numpy`, `pandas`, `sklearn`, `joblib`, `yaml`), `mlsec_labs`, or a local module;
- pinned requirements, including the shared Level 1 stack;
- valid expected-result JSON;
- `CHECKING.md` title, rubric, and reflection sections;
- internal links and local assets in each README, checking guide, and brief.

### 1.2 Repository-level checks

- `.python-version` is `3.14.7`.
- The shared requirements file pins every direct dependency and names the supported interpreter.
- `requirements/labs.txt` includes the shared stack.
- Every lab appears in the catalog, the lab index, the dataset registry, and the MkDocs navigation.
- No `.joblib`, `.pkl`, `.npz`, `.npy`, model, or generated output directory is committed under `labs/`.
- Any notebook must parse as JSON with valid `nbformat`, cells, cell types, sources, and output lists.

### 1.3 Execution

`--execute` runs each reference path in a temporary directory, using the documented command shape:

- LAB-02: `python check_threat_model.py --model solution.yaml --report solution-report.md`.
- LAB-01B: `python make_dataset.py --out <tmp>`, then `python solution.py --out <tmp>`, then `python check_lab01b.py --artifacts <tmp>`.
- All other labs: `python solution.py --out <tmp>`, then `python check_lab<NN>.py --artifacts <tmp>`.

Each step had a 600 s timeout. The runner never executes `starter.py`, never loads a serialized model from an untrusted source, and never writes into the repository. Execution used UTF-8 output, a fixed hash seed, and two BLAS/OpenMP threads.

### 1.4 Links and notebooks

`scripts/check_links.py` checks relative files, directory `index.md` targets, heading anchors (including explicit `<a id="...">` anchors), and local images. Links inside fenced code and inline code are ignored. External HTTP(S) checks are opt-in.

No Jupyter notebooks exist in the published labs. The notebook structural validator is present and covered by unit tests using synthetic notebooks; no notebook was executed because there is nothing to execute.

## 2. Results

| Lab | Structural | Checks | Execution | Runtime (s) | Notes |
|---|---|---:|---|---:|---|
| LAB-01 | PASS | 7 | PASS | 11.5 | solution + checker |
| LAB-01B | PASS | 8 | PASS | 25.7 | generator + solution + checker |
| LAB-02 | PASS | 5 | PASS | 0.3 | checker on reference YAML and report |
| LAB-03 | PASS | 7 | PASS | 9.0 | solution + checker |
| LAB-04 | PASS | 7 | PASS | 12.1 | solution + checker |
| LAB-05 | PASS | 7 | PASS | 9.5 | solution + checker |
| LAB-06 | PASS | 7 | PASS | 8.0 | solution + checker |
| LAB-07 | PASS | 7 | PASS | 7.8 | solution + checker |
| LAB-08 | PASS | 7 | PASS | 9.5 | solution + checker |
| LAB-09 | PASS | 7 | PASS | 56.3 | solution + checker |
| LAB-10 | PASS | 7 | PASS | 18.9 | solution + checker |
| LAB-11 | PASS | 7 | PASS | 16.4 | solution + checker |
| LAB-12 | PASS | 8 | PASS | 16.4 | solution + checker |
| LAB-13 | PASS | 8 | PASS | 8.7 | solution + checker |
| LAB-14 | PASS | 7 | PASS | 9.0 | solution + checker |
| LAB-15 | PASS | 7 | PASS | 8.9 | solution + checker |
| LAB-16 | PASS | 7 | PASS | 14.6 | solution + checker |
| LAB-17 | PASS | 7 | PASS | 7.7 | solution + checker |
| LAB-18 | PASS | 7 | PASS | 18.1 | solution + checker |
| LAB-19 | PASS | 7 | PASS | 7.0 | solution + checker |
| LAB-20 | PASS | 7 | PASS | 7.6 | solution + checker |

Total execution time was 283.0 s (about 4.7 minutes) on the machine above. Every checker exited 0 and printed its pass marker. Runtime is machine-dependent; the order of magnitude, not the exact seconds, is the reproducible claim.

## 3. Failures found and corrected

The quality pass found and fixed the following repository issues before the final run:

| Issue | Correction |
|---|---|
| LAB-04 through LAB-10 briefs lacked a `## How to check yourself` section | Added a section with the exact install, reference, and checker commands and a pointer to `CHECKING.md` |
| LAB-06 README said Tier B while the brief and catalog said Tier A | README corrected to Tier A; the lab runs in under a second on CPU |
| LAB-11 catalog said difficulty 4 while README and brief said 3 | Catalog corrected to 3 |
| LAB-14 catalog said difficulty 3 while README and brief said 4 | Catalog corrected to 4 |
| LAB-12 through LAB-15 treated `LO-30 (supporting)` as a different outcome from `LO-30` | The validator now extracts LO identifiers before comparison; the catalog's primary outcome remains a subset that includes `LO-28` |
| Three external links pointed at moved pages | Replaced after verifying the destination: joblib's generated `joblib.dump` page, GitHub's current private-reporting guide, and the current OWASP ML Security Top Ten page |
| Template and authoring-guide links were not valid MkDocs targets | Converted repository-external paths to inline code and a valid module index link |
| Link checker did not recognize explicit `<a id="...">` anchors | Added explicit-anchor extraction; internal links now resolve |
| External checker treated HEAD 404 as final and treated bot blocks as broken | It retries with GET and reports 401/403/429 separately as blocked |

No lab implementation, metric definition, expected result, checker threshold, or security claim was changed. The only brief content added is the checking section described above.

## 4. Repository checks

| Check | Result |
|---|---|
| Python compilation of lab sources | Pass |
| Import allowlist | Pass |
| Starter/solution separation | Pass |
| Checker independence | Pass (no checker imports `solution` or `starter`) |
| Pinned lab requirements | Pass (21 of 21) |
| Shared stack pins | Pass |
| Expected-result JSON | Pass (21 of 21) |
| Catalog/index/dataset/nav coverage | Pass (21 of 21) |
| Committed model or data binaries under `labs/` | None found |
| Internal links and assets | Pass after this report was added |
| Unit tests | 16 passed |
| MkDocs strict build | Pass after this report was added |

## 5. External links

External checks are opt-in because they require network access and their results depend on the network path. The final run probed 221 unique HTTP(S) links in the documentation.

| Outcome | Count | Meaning |
|---|---:|---|
| Reachable | 210 | HTTP 2xx/3xx, including a successful GET after a HEAD rejection |
| Blocked | 11 | HTTP 401/403/429 from publisher bot protection; not evidence that the page is missing |
| Broken | 0 | Non-success after both HEAD and GET |

Blocked links remain unverified. They are DOI resolvers and publisher pages that refuse automated clients:

| Source | Link |
|---|---|
| `docs/course-blueprint.md:652` | https://doi.org/10.1145/2523813 |
| `docs/course-blueprint.md:706` | https://doi.org/10.1145/2810103.2813677 |
| `docs/course-blueprint.md:710` | https://doi.org/10.1561/0400000042 |
| `docs/course-blueprint.md:722` | https://doi.org/10.1145/3133956.3133982 |
| `docs/modules/m13-privacy-preserving-ml/index.md:219` | https://doi.org/10.1142/S0218488502001648 |
| `docs/modules/m13-privacy-preserving-ml/index.md:224` | https://doi.org/10.1145/2976749.2978318 |
| `docs/modules/m14-explainability-fairness/index.md:203` | https://doi.org/10.1145/2939672.2939778 |
| `docs/modules/m14-explainability-fairness/index.md:208` | https://doi.org/10.1145/3375627.3375830 |
| `docs/modules/m14-explainability-fairness/index.md:213` | https://doi.org/10.1089/big.2016.0047 |
| `docs/references.md:55` | https://doi.org/10.1145/3411764.3445518 |
| `docs/references.md:56` | https://doi.org/10.1145/2382577.2382579 |

A blocked result must not be reported as a working citation, and it must not be reported as a broken one. The machine-readable result of the final run is produced with `--json`.

## 6. What was not executed

- **Learner starters.** `starter.py` and the LAB-02 learner YAML/report were not executed. They intentionally contain TODOs and raise or fail until completed.
- **Notebooks.** There are no published notebooks. Notebook execution therefore does not apply; only the structural validator was tested.
- **External services and cloud/GPU paths.** No lab requires them. All execution was local and CPU-only.
- **Blocked external links.** See §5. They were probed but could not be verified.
- **Pedagogical and security quality.** The checks confirm structure, consistency, and reproducibility. They do not grade whether a threat model is insightful or a report is well argued; that remains the rubric's job.

## 7. How to reproduce

From the repository root:

```bash
python -m pip install -r requirements/labs.txt

# Structure, metadata, compilation, imports, expected JSON, internal links
python scripts/validate_labs.py

# Run every reference solution and checker (temporary artifacts, 600 s per step)
python scripts/validate_labs.py --execute --timeout 600

# Internal Markdown links only (no network)
python scripts/check_links.py

# Optional external probes (network access)
python scripts/check_links.py --check-external --timeout 15

# Tooling tests
python -m unittest discover -s tests

# Documentation build
python -m mkdocs build --strict
```

Expected final lines:

```text
Summary: 21 labs structurally checked, 0 failed; 34 global checks, 0 global failures, 0 global warnings; 0 labs with warnings
Execution: 21 passed, 0 failed or timed out
LINK CHECK PASSED: 281 Markdown files
Ran 16 tests ... OK
```

A failure is actionable: the validator prints `FAIL` with the lab, file, and reason. Execution failures include the last lines of the failing step's output. Nothing is marked passed unless the command actually exited 0.
