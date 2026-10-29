# Lesson 10.2 — Unsafe Serialization and Safe Formats

<a id="m10-l2"></a>

**Module 10 · Lesson 2 of 4 · 2 hours · LO-21**

## Scenario

A model arrives as `model.pkl`. It loads in one line:

```python
import joblib
model = joblib.load("model.pkl")
```

The line looks like reading a file. It is closer to running one. The pickle format can encode instructions to import a module, look up an attribute, and call it. If the file came from someone else, that call happens with your process's permissions.

This lesson teaches you to inspect the file without running it, choose formats that store data rather than instructions, and state precisely what a clean scan does and does not prove.

## Objectives

By the end of this lesson you will be able to:

1. Explain why pickle is a stack-based program format and which opcodes enable callable construction.
2. Inspect a pickle stream statically with `pickletools` without executing it.
3. Choose a safer format for weights or arrays and state its residual risk.
4. Explain the limits of opcode blocklists and name stronger controls.
5. Verify that a hardened project contains no pickle artifacts and a safe loader.

## 1. Pickle is a program

Python's `pickle` module serializes objects by emitting opcodes. The unpickler is a small stack machine: opcodes push values, build containers, and call functions. Most opcodes handle ordinary data. A few can resolve names and invoke callables.

| Opcode | What it does | Why it matters |
|---|---|---|
| `GLOBAL` | Pushes a global object by module and name | Can reference a function |
| `STACK_GLOBAL` | Resolves a module/name pair from the stack | Same, with names computed at runtime |
| `REDUCE` | Calls a callable with arguments | Executes the referenced callable |
| `BUILD` | Calls `__setstate__` or updates `__dict__` | Can trigger object behavior |
| `INST`, `OBJ`, `NEWOBJ` | Construct objects | Can invoke constructors |
| `EXT1`, `EXT2`, `EXT4` | Resolve via a copyreg registry | Indirect name resolution |

The [Python documentation](https://docs.python.org/3/library/pickle.html) is explicit: pickle is not secure against malicious data, and untrusted input must not be unpickled. This is not a bug that a patch removes. It is the format's design: it reconstructs arbitrary Python objects, and arbitrary objects can have behavior.

`joblib` uses pickle under the hood for many objects. A `.joblib` or `.pkl` file from a model hub inherits the same property.

### A benign canary

LAB-13 generates `canary.pkl`, which would print a fixed marker string if loaded. It does nothing else. The lab still never loads it, because the point is to demonstrate inspection without execution. The canary's opcode list is `REDUCE` and `STACK_GLOBAL`.

The benign `model.pkl` in the same project contains no dangerous opcodes. That does not make it trusted; it makes it a pickle with ordinary data. The scanner reports the difference, and the hardening step removes pickles from the load path entirely.

## 2. Static inspection

`pickletools` parses a pickle stream into opcodes without executing it.

```python
from pathlib import Path
import pickletools

DANGEROUS = {
    "GLOBAL", "STACK_GLOBAL", "REDUCE", "BUILD", "INST", "OBJ",
    "NEWOBJ", "NEWOBJ_EX", "EXT1", "EXT2", "EXT4",
}

def scan_opcodes(path: Path) -> list[str]:
    data = path.read_bytes()
    names = {
        op.name
        for op, _arg, _pos in pickletools.genops(data)
        if op.name in DANGEROUS
    }
    return sorted(names)
```

On LAB-13's artifacts:

```text
canary.pkl -> ['REDUCE', 'STACK_GLOBAL']
model.pkl  -> []
```

`pickletools.dis(data)` prints a human-readable disassembly when you need to see the sequence, not just the set of opcodes.

### Reading the result

A non-empty list is a finding: the file can construct and call objects. An empty list means the stream contains no opcodes from the blocklist. It does **not** mean the file is safe.

Reasons a clean scan is not a safety proof:

- the blocklist may be incomplete for the pickle protocol version;
- an opcode can be hidden behind an extension registry entry or a nested payload;
- a later stage (conversion, framework loading) may execute code even if the pickle does not;
- the data itself may be wrong, backdoored, or licensed incorrectly;
- the scanner may be reading a different file than the loader.

This is the same distinction as Module 08's attack evaluation: a negative result is evidence about the test, not proof about the system.

### Scanning is not loading

Do not "just load it in a sandbox to see." A sandbox reduces impact but does not make execution a safe inspection method, and a misconfigured sandbox is a real incident. Static inspection answers the structural question without granting the artifact a runtime.

If dynamic analysis is unavoidable, use a disposable environment with no credentials, no network, and no persistent storage, and treat any behavior as hostile. For this course, static inspection is sufficient.

## 3. Safe formats

A safe format stores data without executable construction. "Safer" is more accurate than "safe": every format has parsers, every parser has bugs, and none removes the need to verify origin.

| Format | Stores | Loader guidance | Residual risk |
|---|---|---|---|
| NumPy `.npy` / `.npz` | Arrays | `np.load(..., allow_pickle=False)` | Object arrays require pickle; reject them |
| safetensors | Tensors and metadata | Framework loader with no arbitrary code | Parser bugs; metadata still needs review |
| ONNX | Computation graph | Runtime with a restricted op set | Custom operators can require native libraries |
| JSON / CSV / Parquet | Tabular or structured data | Schema validation after load | Type coercion, malicious content in fields |
| Text weights + config | Parameters | Explicit parsing and shape checks | Reconstruction code must be trusted |

### NumPy's `allow_pickle`

`numpy.load` defaults to `allow_pickle=False` in current versions, but older code and tutorials often pass `True`. An object array in a `.npy` file requires pickle to reconstruct, which reintroduces the risk. The hardened loader in LAB-13 reads arrays with `allow_pickle=False` and validates shape and dtype explicitly:

```python
with np.load(path, allow_pickle=False) as data:
    weights = data["weights"]
if weights.shape != (10, 64) or weights.dtype != np.float64:
    raise ValueError("unexpected weight shape or dtype")
```

The shape check is not a security boundary by itself. It prevents a malformed or substituted file from silently changing the model's behavior, and it fails closed.

### Framework loaders

Framework loaders change defaults over time. A loader that once unpickled by default may now require an explicit opt-in, or the reverse. Read the documentation for the version you pinned. Do not assume that a familiar function is safe because it is familiar.

## 4. Conversion as a control

The strongest practical control is to convert untrusted artifacts to a safe format in an isolated environment, then promote the converted artifact.

| Step | Environment | Control |
|---|---|---|
| Receive | Quarantine | No execution; hash and record |
| Inspect | Static scanner | Opcode scan, size, metadata |
| Convert | Disposable sandbox | No credentials, no egress, resource limits |
| Validate | Test harness | Shape, dtype, output parity on fixed inputs |
| Sign and promote | Registry | Manifest, signature, SBOM |

The conversion environment is the only place that may load the risky format, and it is treated as hostile. If conversion is not possible, the artifact does not enter the privileged environment.

This pattern also applies to notebooks and scripts distributed with a model: a notebook can execute on open or on run. Treat it as code, review it, and disable automatic execution in viewers.

## 5. Hardening LAB-13's load path

The lab's remediation has four parts:

1. **Remove pickle artifacts** from the hardened project. The count of pickle files must be zero.
2. **Replace the loader** with `np.load(..., allow_pickle=False)` plus shape and dtype checks.
3. **Regenerate the manifest** from the actual bytes after writing every file.
4. **Add a gate** that fails if a pickle file appears, a dependency is unpinned, a hash mismatches, or a signature is missing or invalid.

The result is not "the model is safe." It is "the hardened project does not load executable serialization, its recorded hashes match, and the implemented checks reject the known-bad cases."

### The negative tests

- Flip a byte in the manifest: signature verification must fail.
- Place a `.pkl` file in the hardened tree: the gate must fail.
- Remove a pin from `requirements.txt`: the gate must fail.

A control without a failing case is untested. LAB-13 includes the tamper test and the gate exit codes so that the evidence includes a rejection, not only a success.

## 6. Limits of scanners and blocklists

| Limitation | Example | Stronger control |
|---|---|---|
| Blocklist incompleteness | An opcode not in the list | Format allowlist; no pickle in production |
| Obfuscation | Protocol tricks, nested data | Conversion in a sandbox, not just a scan |
| Extension confusion | File named `.bin` but pickled | Inspect magic bytes, not extensions |
| Nested archives | A zip containing a pickle | Recursive inspection with limits |
| Semantic attacks | A valid pickle with a backdoored model | Model behavior testing, provenance |
| Scanner drift | Tool outdated for a new protocol | Pin and update the scanner; test it |

Scanners such as ModelScan and picklescan are useful triage tools. They are not a security boundary, and their output should be treated the same way as a validation rule: a finding is evidence, and a pass is not proof.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Loading to inspect | It is the fastest way to see the object | Use `pickletools.genops` |
| Trusting the file extension | `.bin` or `.pt` feels different | Inspect magic bytes and loader behavior |
| Flagging every pickle | It looks conservative | Flag callable-construction opcodes; then remove pickles from the load path |
| Treating a clean scan as approval | The tool returned no findings | State what the scan covered and what it did not |
| Passing `allow_pickle=True` "temporarily" | The array is an object array | Convert the data; do not weaken the loader |
| Converting in the production environment | It is convenient | Convert in an isolated sandbox |
| Skipping shape checks | The model loads | Validate shape and dtype; fail closed |
| Signing before the final write | The manifest changes | Write all files, then hash, then sign |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `pickletools` raises on the file | Not a pickle or truncated | Check magic bytes; treat as untrusted |
| Canary scan is empty | Reading the wrong file or catching exceptions silently | Print the path and the opcode count |
| Benign model flagged | Blocklist includes ordinary opcodes | Narrow the list to callable construction |
| `np.load` raises `Object arrays cannot be loaded` | `allow_pickle=False` on an object array | Convert the artifact; do not enable pickle |
| Shape check fails on a valid model | Layout or dtype assumptions differ | Record the expected contract; update the validator |
| Hardened gate still finds pickles | Copy step included the vulnerable tree | Copy only allowlisted files |
| Signature fails after formatting | Manifest rewritten with whitespace changes | Sign exact bytes; do not reformat after signing |

## Check your understanding

1. Which pickle opcodes enable callable construction, and what do they do?
2. Why is `pickletools.genops` preferable to loading the file in a sandbox?
3. A `.npy` file loads with `allow_pickle=False`. What risk remains?
4. Give two reasons a clean opcode scan does not prove an artifact is safe.
5. What negative tests should accompany a hardened load path?

Answers are in the [quiz answer key](quiz-answers.md) and discussed in the exercises.

## Summary

- Pickle is a stack-machine program format; `GLOBAL`, `STACK_GLOBAL`, `REDUCE`, and related opcodes can construct and call objects.
- `joblib` inherits pickle behavior. Loading a downloaded artifact can execute code with your permissions.
- Static inspection with `pickletools.genops` reveals opcodes without execution. LAB-13's canary contains `REDUCE` and `STACK_GLOBAL`; the benign model contains none.
- A clean scan is not a safety proof: blocklists are incomplete, formats can be mislabeled, and later stages can execute.
- Safe formats store data rather than instructions: `.npy` with `allow_pickle=False`, safetensors, restricted ONNX, and validated tabular formats.
- Conversion belongs in an isolated sandbox; the privileged environment receives only the converted artifact.
- Hardening means removing pickle from the load path, validating shape and dtype, regenerating the manifest, and gating on negative tests.

## Next

Continue to [Lesson 10.3 — Dependency and artifact scanning in CI](lesson-3-dependency-and-artifact-scanning.md), where the checks become a gate that fails closed.
