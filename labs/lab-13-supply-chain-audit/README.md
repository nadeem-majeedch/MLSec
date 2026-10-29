# LAB-13 — Supply-Chain Audit of a Toy ML Project

| Field | Value |
|---|---|
| Lab ID | LAB-13 |
| Tier | A |
| Time | 4 hours |
| Difficulty | 3 of 4 |
| Module | M10 — Supply Chain |
| Outcomes | LO-21, LO-30 (supporting), LO-28 |
| Prerequisites | M01 lesson 4; M10 lessons 1–3 |
| Data | generated toy project |
| Compute | CPU only; under 1 second |

Full brief: [docs/labs/lab-13.md](../../docs/labs/lab-13.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

A colleague hands you a small "churn model" project: unpinned requirements, a
`joblib.load` inference path, a manifest whose hash is all zeros, no signature,
no SBOM, and a pickle file with a callable-construction opcode. The pickle is a
benign canary — if it were ever loaded, it would print a fixed marker string.
Nothing in this lab loads it.

You audit the project without executing its artifacts, then produce a hardened
copy: pinned dependencies, a `np.load(..., allow_pickle=False)` loader, no
pickle files, a regenerated manifest, an HMAC-SHA256 signature, and a minimal
CycloneDX-style SBOM. Finally you verify the hardened copy and demonstrate that
a tampered manifest fails verification and that the CI gate blocks the vulnerable
project while passing the hardened one.

The canary is generated locally under `artifacts/` and is never distributed. No
real malware is created or used.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab13.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab13.py --artifacts artifacts
```

## What you produce

- `artifacts/audit.json`, `metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- The hardened project tree with pinned requirements, safe loading, regenerated manifest, signature, and SBOM.
- Verification output showing the hardened project passes and a tampered manifest fails.
- `report.md` answers every reflection question and records the canary handling rule.
- `python check_lab13.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `audit_project` | Produce findings for the six planted risks |
| `starter.py` | TODO 2 | `harden_project` | Write the hardened copy with all six fixes |
| `starter.py` | TODO 3 | `verify_project` | Verify the hardened tree and the vulnerable one, including tamper detection |

## Hints

- Audit by reading and hashing. Never call `pickle.load`, `joblib.load`, or `np.load(..., allow_pickle=True)` on the project.
- `pickletools.genops` shows opcodes without executing them. Look for callable-construction opcodes such as `GLOBAL` and `REDUCE`.
- The hardened copy needs all six fixes: pins, safe loader, no pickle, regenerated manifest, signature, and SBOM.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab13.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `project.py` | Generates the toy project under audit |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
