# Requirements

| Field | Value |
|---|---|
| Purpose | One place for the pinned environments used by the published labs |
| Supported interpreter | Python 3.14.7 |
| Platforms verified | Windows 10 (x64), CPU only |
| Network at runtime | Not required by any published lab |

## Install

From the repository root:

```bash
python -m pip install -r requirements/labs.txt
```

Or install one lab's environment from its package directory:

```bash
cd labs/lab-03-evasion-magnitude
python -m pip install -r requirements.txt
```

Both paths resolve to the same pins. The per-lab file exists so a learner can work inside one folder without knowing the repository layout.

## Pinned stack

| Package | Pin | Used for |
|---|---|---|
| NumPy | 2.5.2 | Arrays, gradients, synthetic data |
| pandas | 3.0.5 | Tabular fixtures and validation |
| scikit-learn | 1.9.0 | Models, splits, metrics, bundled digits |
| joblib | 1.5.3 | Model serialization in LAB-01 and LAB-01B |
| PyYAML | 6.0.3 | LAB-02 threat-model file and run records |

`labs/shared/requirements-level1.txt` is the source of truth. `requirements/labs.txt` includes it rather than repeating the pins, so the two cannot drift. LAB-02's package file pins PyYAML directly because it needs nothing else.

## Version policy

- The course is verified on Python 3.14.7. A newer patch release is acceptable if every lab still passes its checker in your environment; record the actual version in `run.json`.
- Do not mix package versions across runs that you intend to compare. A changed NumPy or scikit-learn version can move a metric enough to fail a tight tolerance.
- If a pin becomes unavailable or insecure, update the shared file, re-run the validation suite, update `expected_metrics.json` where needed, and record the change. Do not silently float a dependency.
- Optional tools named in the course (SHAP, LIME, Opacus, Flower, garak, and others) are not required by the 21 published labs. Do not add them to this file unless a lab uses them.
