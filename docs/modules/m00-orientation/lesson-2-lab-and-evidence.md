# Lesson 00.2 — Your Lab, Your Evidence

**Module 00 · 60 minutes · Requires a terminal and Python 3.11 or newer**

## Scenario

Two learners submit the same accuracy, 96.9%. One ran the notebook once and wrote the number in a report. The other shipped a virtual environment file, a fixed split, a saved model, a metrics file, and a manifest of SHA-256 hashes. Six months later, only the second result can be defended. The difference is not talent. It is evidence hygiene.

This lesson sets up the environment you will use for LAB-01 and teaches the artifact pattern that every later lab repeats.

## Learning objectives

By the end of this lesson you will be able to:

1. Create and activate an isolated Python environment and verify its interpreter and packages.
2. Save a model and its configuration as separate, versioned artifacts.
3. Generate and verify a SHA-256 manifest that detects a modified file.
4. Apply notebook, path, and local-Git hygiene rules that keep results reproducible.

## The environment

Use one environment per level, not one global installation. A virtual environment isolates package versions, so a later lab cannot silently upgrade a library that an earlier lab depended on.

### Create it

From the repository root:

```bash
python -m venv .venv
```

Activate it:

=== "Windows (PowerShell)"

    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```

=== "Windows (Git Bash)"

    ```bash
    source .venv/Scripts/activate
    ```

=== "macOS / Linux"

    ```bash
    source .venv/bin/activate
    ```

Your prompt should now start with `(.venv)`. Confirm that the interpreter is the one inside the environment:

```bash
python -c "import sys; print(sys.executable)"
```

Expected shape (the path depends on your machine):

```text
C:\Users\you\MLSec\.venv\Scripts\python.exe
```

If the path does not contain `.venv`, the environment is not active. Do not continue.

### Install the Level 1 requirements

```bash
python -m pip install --upgrade pip
python -m pip install -r labs/lab-01-environment/requirements.txt
```

The requirements file pins exact versions. The versions in this repository were verified on Python 3.14.7 on Windows; the code uses no platform-specific features and runs on Linux and macOS. If you use a different Python minor version, keep the same package versions where wheels exist and record any substitution in your environment report.

Verify the stack:

```bash
python - <<'PY'
import platform, numpy, pandas, sklearn, joblib, yaml
print("python", platform.python_version())
print("numpy", numpy.__version__)
print("pandas", pandas.__version__)
print("scikit-learn", sklearn.__version__)
print("joblib", joblib.__version__)
print("pyyaml", yaml.__version__)
PY
```

Expected output has the same six labels with the pinned versions, for example:

```text
python 3.14.7
numpy 2.5.2
pandas 3.0.5
scikit-learn 1.9.0
joblib 1.5.3
pyyaml 6.0.3
```

The exact numbers may differ if you installed from a different lockfile; what matters is that you **recorded** them. An unrecorded version is a reproducibility bug waiting to happen.

## The artifact pattern

Every lab produces the same anatomy:

```text
work/lab01/
├─ model.joblib          # learned parameters
├─ config.json           # seed, split sizes, model settings
├─ metrics.json          # accuracy, per-class recall, confusion matrix
├─ predictions.npy       # predictions on a fixed set of test rows
├─ test_indices.npy      # which rows those are
├─ manifest.json         # SHA-256 of every file above
└─ README.md             # what you did, what you measured, what is missing
```

Three rules make this pattern work:

1. **Separate the model from its configuration.** A serialized object without the seed and preprocessing is not reproducible.
2. **Save the exact rows you evaluated.** If you save predictions but not indices, a different split makes them meaningless.
3. **Hash what you ship.** A manifest turns "I think this is the file" into "this is the file."

### Worked example: a manifest that detects tampering

This example uses only the standard library. It creates a file with known content, hashes it, writes a manifest, verifies it, then modifies the file and verifies again.

```python
from pathlib import Path
import hashlib
import json

root = Path("manifest_demo")
root.mkdir(exist_ok=True)

artifact = root / "artifact.txt"
artifact.write_text("mlsec-lab-01\n", encoding="utf-8")

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()

manifest = {"artifact.txt": sha256(artifact)}
(root / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print("hash:", manifest["artifact.txt"])
print("verification:", "OK" if sha256(artifact) == manifest["artifact.txt"] else "MISMATCH")

artifact.write_text("mlsec-lab-01-tampered\n", encoding="utf-8")
print("verification after edit:", "OK" if sha256(artifact) == manifest["artifact.txt"] else "MISMATCH")
```

Expected output:

```text
hash: 4ff7794ac45e6255f7ed6926943f91bd4968b9834592ca2f2958504e4862380b
verification: OK
verification after edit: MISMATCH
```

The hash is exact because the content and newline are fixed. If your output differs, check whether your editor added a carriage return or removed the final newline. That is not a trivia point: byte-level differences are exactly what a manifest is designed to catch.

## Notebook and Git hygiene

### Notebooks

- **Run all cells before saving.** A notebook that only works with hidden state is not reproducible.
- **Keep the seed in the first cell**, not buried in a later one.
- **Do not commit large outputs.** Clear tensors and image grids; keep small tables and the final metrics.
- **Prefer scripts for reusable logic.** Put functions in a `.py` file, import them in the notebook, and test the script directly.

### Paths

Use paths relative to the repository root, or construct them with `pathlib.Path(__file__).resolve()`. Absolute paths such as `C:\Users\you\...` break on every other machine.

### Local Git

You may create a local repository and commit your work. Do not add a remote, push, or publish someone else's data. A minimal `.gitignore` should exclude:

```text
.venv/
work/
data/
*.pyc
__pycache__/
.ipynb_checkpoints/
```

If you use Git, commit the code, configuration, and small reports; ignore datasets and model binaries, and record their hashes in the manifest instead.

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Installing into the global interpreter | `ModuleNotFoundError` after switching labs | Activate `.venv`; check `sys.executable` |
| Hashing text after opening in text mode | Different hash on Windows | Read bytes with `"rb"` |
| Saving the model but not the preprocessing | Predictions differ after reload | Save a scikit-learn `Pipeline`, not just the estimator |
| Overwriting `metrics.json` on every run | You cannot compare runs | Include a run ID or timestamp in the filename |
| Using `random_state` in one place only | Split changes when code is reordered | Centralize the seed and pass it explicitly |
| Committing `work/` or datasets | Repository bloat; leaked data | Add them to `.gitignore` |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `python` opens the Microsoft Store | Windows app alias shadows Python | Install Python from python.org or disable the alias; use `py -3.12` if available |
| `Activate.ps1 cannot be loaded` | PowerShell execution policy | Run `Set-ExecutionPolicy -Scope Process RemoteSigned` for the session |
| `pip` SSL certificate error | Corporate proxy or missing certificates | Configure the proxy or use an internal index; do not disable TLS verification |
| `python` still finds global packages | Environment not activated | Check the prompt and `sys.executable` |
| Hash differs between machines | Line-ending conversion | Write bytes and avoid text-mode newline translation |
| `FileNotFoundError` for a data file | Working directory differs | Resolve paths from `__file__`, not the current shell |

## Key terms

**Virtual environment**, **interpreter**, **lockfile**, **artifact**, **manifest**, **SHA-256**, **seed**, **hidden state**, **reproducibility**, **run-all**.

## Summary

- One isolated environment per level prevents version drift.
- Record the interpreter and every package version; "it worked yesterday" is not evidence.
- Save model, config, metrics, predictions, indices, and a manifest together.
- Hash files as bytes; a manifest detects tampering and accidental edits.
- Run all cells, use relative paths, and keep large artifacts out of version control.

## References

| Reference | Use |
|---|---|
| [Python `venv`](https://docs.python.org/3/library/venv.html) | Environment creation and activation |
| [Python `hashlib`](https://docs.python.org/3/library/hashlib.html) | SHA-256 hashing |
| [scikit-learn `Pipeline`](https://scikit-learn.org/stable/modules/compose.html) | Saving preprocessing with the model |
| [joblib persistence](https://joblib.readthedocs.io/en/stable/generated/joblib.dump.html) | Model serialization used in LAB-01 |
| [Git documentation](https://git-scm.com/doc) | Local commits and `.gitignore` |

Next: [Lesson 00.3 — Rules of engagement](lesson-3-rules-of-engagement.md).
