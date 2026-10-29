# Datasets

| Field | Value |
|---|---|
| Purpose | Dataset policy and registry for the 21 published labs |
| Data stored here | **None** |
| Downloads required | **None** for published labs |
| Personal data | **None** |

This directory is a policy and registry, not a data store. No CSV, image, archive, or model file belongs here. The labs use either a dataset bundled with scikit-learn or a synthetic fixture generated deterministically by code in the lab package.

## Policy

1. **Bundled public data first.** `sklearn.datasets.load_digits` ships with the pinned scikit-learn install: 1,797 8×8 digit images, 64 features, 10 classes. There is no download, no account, and no network dependency. Check the scikit-learn license before redistributing the data outside a course installation.
2. **Synthetic by default for tabular and system labs.** A generator is a seeded pure function. It writes only under the lab's `--out` directory. Regenerating with the same seed must reproduce the same rows.
3. **No repository data files.** Generated fixtures are never committed. They are small, reproducible, and disposable. `.gitignore` excludes `data/`, `artifacts/`, and model binaries.
4. **No private or personal data.** Do not replace a synthetic fixture with a customer extract, patient record, user log, or proprietary model. If you adapt a lab to a real dataset, do so outside this repository under an approved data-handling agreement.
5. **External datasets are opt-in and documented.** A lab that adds one must record the license, version, checksum, access command, and offline fallback in its README. No published lab currently requires one.

## Registry

| Lab | Data | Provenance | Seed |
|---|---|---|---|
| LAB-01 | digits | scikit-learn bundled | 42 |
| LAB-01B | synthetic churn, 2,040 rows / 1,700 customers | `make_churn_dataset(seed=42)` in `labs/shared/mlsec_labs/data.py` | 42 |
| LAB-02 | none | fictional MediScan scenario | — |
| LAB-03 | digits | scikit-learn bundled | 42 |
| LAB-04 | digits | scikit-learn bundled | 42 |
| LAB-05 | digits | scikit-learn bundled | 42 |
| LAB-06 | 2-D Gaussian mixture | generated in the lab | 7 |
| LAB-07 | 16-feature tabular | generated in the lab | 11 |
| LAB-08 | digits, classes 3 and 8 | scikit-learn bundled | 13 |
| LAB-09 | 10-feature, 5-class synthetic | generated in the lab | 21 |
| LAB-10 | digits, 500 members / 500 non-members | scikit-learn bundled | 31 |
| LAB-11 | digits | scikit-learn bundled | 42 |
| LAB-12 | synthetic customer extract | `labs/lab-12-dataset-validation/dataset.py` | 7 (split 13) |
| LAB-13 | generated toy project | `labs/lab-13-supply-chain-audit/project.py` | — |
| LAB-14 | digits plus synthetic tokens | local model; demo tokens are non-secrets | — |
| LAB-15 | digits plus synthetic traffic | generated in the lab | 37 |
| LAB-16 | digits, 8 simulated clients | scikit-learn bundled | 42 |
| LAB-17 | synthetic Gaussian, 800 rows per class | generated in the lab | 42 |
| LAB-18 | synthetic lending data, 1,200 rows | generated in the lab | 42 |
| LAB-19 | synthetic document corpus | generated in the lab | — |
| LAB-20 | in-memory workspace and mock services | generated in the lab | — |

## Regenerating a fixture

The generators live with their labs, not here:

```bash
cd labs/lab-01b-evaluation-audit && python make_dataset.py --out artifacts
cd labs/lab-12-dataset-validation && python solution.py --out artifacts
cd labs/lab-13-supply-chain-audit && python solution.py --out artifacts
```

Every command writes under `artifacts/`. Delete that directory when finished. Do not copy generated data into this directory or commit it.

## Dataset changes

A dataset change is a lab change. If a seed, generator, or bundled dataset version changes, update `expected_metrics.json`, `CHECKING.md`, and the validation report in the same change. A stale expected value is worse than no expected value because it looks authoritative.

External dataset availability changes over time. The course reference list records alternatives for optional extensions, but the published labs deliberately avoid them so that a learner on an offline laptop can finish the course.
