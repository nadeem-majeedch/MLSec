# Labs

Each directory is a self-contained lab package. The student brief lives in [`docs/labs/`](../docs/labs/index.md); this folder holds the code, fixtures, reference implementation, checker, and local quickstart.

## Layout

```text
labs/
  shared/
    requirements-level1.txt     # pinned stack used by every lab except LAB-02
    mlsec_labs/                 # artifact, data, and metric helpers
  lab-01-environment/
  lab-01b-evaluation-audit/
  lab-02-threat-model/
  ...
  lab-20-agent-containment/
```

| File | Role |
|---|---|
| `README.md` | Metadata, scenario, run commands, deliverables, starter map, hints, files, safety, cleanup |
| `starter.py` | Learner scaffold with numbered TODOs that raise `NotImplementedError` |
| `solution.py` | Complete reference implementation |
| `check_*.py` | Independent checker; accepts `--artifacts` |
| `expected_*.json` | Reference values and tolerances |
| `requirements.txt` | Shared pinned stack, or the LAB-02 exception |
| `CHECKING.md` | What the checker verifies, reference results, failure diagnosis, rubric, reflection |
| `report_template.md` | Report headings, where a written report is required |

LAB-02 uses `threat-model.yaml` and `report.md` instead of a Python starter/solution pair. Its reference files are `solution.yaml` and `solution-report.md`. LAB-01B, LAB-12, and LAB-13 include a deterministic fixture generator.

## Run a lab

From the repository root:

```bash
cd labs/lab-03-evasion-magnitude
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

python solution.py --out artifacts
python check_lab03.py --artifacts artifacts
```

Then complete `starter.py` and run the same two commands with `starter.py` in place of `solution.py`. The checker must accept the reference artifacts before you compare your own.

For LAB-02:

```bash
cd labs/lab-02-threat-model
python -m pip install -r requirements.txt
python check_threat_model.py --model solution.yaml --report solution-report.md
python check_threat_model.py --model threat-model.yaml --report report.md
```

## Artifact contract

Most labs write:

| File | Contents |
|---|---|
| `metrics.json` | Measured values with the fields the checker expects |
| `run.json` | Lab ID, seed, environment versions, command |
| `report.md` | Threat model, method, results, limitations, reflection |
| `manifest.json` | SHA-256 and size for the other artifacts |

Lab-specific additions are named in the brief and README: LAB-01 adds `model.joblib` and `splits.npz`; LAB-12 adds `validation.json`, `raw.csv`, and `repaired.csv`; LAB-13 adds `audit.json`, `sbom.json`, and a hardened project tree. LAB-02 produces `threat-model.yaml` and `report.md`.

Never commit `artifacts/`. Delete it when finished.

## Shared helpers

`labs/shared/mlsec_labs/` contains small, dependency-light helpers:

- `artifacts.py` — `write_json`, `environment`, `build_manifest`;
- `data.py` — deterministic synthetic fixtures, including the churn dataset;
- `metrics.py` — metric helpers shared by lab checkers.

A lab imports the package by adding `parents[1] / "shared"` to `sys.path`. Do not copy these helpers into a lab; update the shared package instead.

## Data

No lab downloads data. Most use scikit-learn's bundled digits; the rest generate deterministic synthetic fixtures. The policy and registry are in [`datasets/README.md`](../datasets/README.md).

## Validation

From the repository root:

```bash
python scripts/validate_labs.py --structural
python scripts/validate_labs.py --execute --timeout 600
python scripts/check_links.py
python -m unittest discover -s tests
```

`--structural` checks metadata, required files, links, compilation, and expected-metric shape without running lab code. `--execute` runs the reference solution and checker for each lab with a timeout. See the [lab authoring guide](../docs/lab-authoring-guide.md) and the [validation report](../docs/lab-validation-report.md).

## Adding a lab

Read the [lab authoring guide](../docs/lab-authoring-guide.md) and copy the [lab template](../docs/lab-template.md). Add the catalog entry first; a lab ID without a catalog row is not a lab. Keep the flat directory structure: the shared import path and the local README links depend on it.
