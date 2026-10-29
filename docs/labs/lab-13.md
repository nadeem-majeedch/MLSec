# LAB-13 — Supply-Chain Audit of a Toy ML Project

**Tier A · 4 hours · Difficulty 3 · Module M10 · Outcomes LO-21, LO-28, LO-30 (supporting)**

## Why this lab exists

A model artifact is executable input. If the loader can deserialize code, then
"downloading a model" is closer to "running a program from a stranger" than to
loading a CSV. The rest of the supply chain — dependency resolution, hashes,
signatures, bills of materials — exists to make that program's origin and
contents checkable before anything executes.

This lab gives you a deliberately weak toy project and asks two questions: what
is wrong with it, and can you prove that your fix works? The fix is not "delete
the pickle." It is a set of controls whose effect you can demonstrate, including
the negative case where tampering is rejected.

## The system and the threat model

| Element | Assumption |
|---|---|
| Asset | A small model project: requirements, loader, weights, manifest, SBOM |
| Threat | A tampered artifact, a malicious pickle, an unpinned dependency, or a missing inventory |
| Attacker capability | Can replace files in transit or publish a look-alike dependency; cannot modify your local audit code |
| Detection surface | Text review, static pickle opcode scan, SHA-256 comparison, HMAC verification, SBOM validation |
| Constraint | Nothing is unpickled; the canary is a benign marker and is never loaded |
| Metric | Findings by rule/severity, verification booleans, CI gate exit codes |
| Lifecycle stage | Build, packaging, model registry, deployment gate |
| Out of scope | Live package-index attacks, build-server compromise, key management, real malware |

The canary pickle would print a fixed string if loaded. It is generated locally
under `artifacts/`, is never distributed, and exists only so the scanner has a
real byte stream to inspect.

## What you produce

A folder inside `labs/lab-13-supply-chain-audit/` containing:

| File | Contents |
|---|---|
| `audit.json` | Findings with rule, severity, file, evidence, remediation; static pickle scan; summary |
| `metrics.json` | Audit summary, verification results, gate exit codes, remediation actions |
| `run.json` | Lab id, seed, finding count, environment versions |
| `report.md` | Findings, fixes, verification evidence, limitations |
| `manifest.json` | SHA-256 hashes of the four files above |
| `project/` | The generated vulnerable project |
| `hardened/` | The repaired project with pins, safe loader, manifest, signature, SBOM |

The reference implementation writes these under `artifacts/`. Your completed
`starter.py` must produce the same structure.

## Prerequisites

- Module 01 Lesson 4 (files, hashing, environments).
- Module 10 Lessons 1–3 (artifact formats, dependency risk, signing and SBOM).
- You can read a Python traceback and a JSON file without a library.

## Environment

- Python 3.14.7; `numpy==2.5.2`, `pandas==3.0.5`, `scikit-learn==1.9.0`, `joblib==1.5.3`, `PyYAML==6.0.3`.
- CPU only; the reference run takes under a second.
- No network, no cloud account, no API key.

```bash
cd labs/lab-13-supply-chain-audit
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab13.py --artifacts artifacts
```

## Safety rules

- Never call `pickle.load`, `joblib.load`, or `np.load(..., allow_pickle=True)` on the generated artifacts.
- Inspect with `pickletools.genops`, which parses opcodes without executing them.
- The canary prints a marker string if loaded; it performs no file, network, or shell action.
- Do not add a payload that does anything beyond a fixed print. Do not distribute the canary outside your own `artifacts/` folder.
- Delete `artifacts/` when you are done if your environment does not already ignore it.

## Task specification

1. **Generate the project.** Call `build_project()` from `project.py`. Do not edit the generator.
2. **Audit.** Detect and report:
   - `DEP-001` (high): unpinned requirements;
   - `ART-001` (high): a loader that calls `joblib.load` or `pickle.load`;
   - `ART-002` (critical): a pickle stream containing `GLOBAL`, `STACK_GLOBAL`, `REDUCE`, or another callable-construction opcode;
   - `ART-003` (high): a manifest hash that does not match the file;
   - `ART-004` (medium): a missing signature;
   - `ART-005` (medium): a missing SBOM.
3. **Record the pickle scan.** The benign `model.pkl` must produce an empty dangerous-opcode list. The canary must produce a non-empty list.
4. **Harden.** Pin all five dependencies, replace the loader with `np.load(..., allow_pickle=False)` and explicit shape checks, copy only safe artifacts, regenerate the manifest from actual bytes, sign it with HMAC-SHA256, and emit a CycloneDX-style SBOM.
5. **Verify.** Confirm every manifest hash, the signature, the absence of pickle files, the pins, and the SBOM component count. Flip one byte of the manifest and confirm the signature fails.
6. **Gate.** The CI gate must exit 1 for the vulnerable project and 0 for the hardened project.
7. **Write the report.** Include the findings table, the remediation list, the verification table, a threat-to-control table with residual risks, and at least four limitations.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `audit_project` | Produce findings for the six planted risks |
| `starter.py` | TODO 2 | `harden_project` | Write the hardened copy with all six fixes |
| `starter.py` | TODO 3 | `verify_project` | Verify the hardened tree and the vulnerable one, including tamper detection |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-13-supply-chain-audit/CHECKING.md`.

## Expected outputs

| Check | Reference |
|---|---|
| Findings | 6 total: 1 critical, 3 high, 2 medium |
| Rules present | DEP-001, ART-001, ART-002, ART-003, ART-004, ART-005 |
| Canary opcodes | `REDUCE`, `STACK_GLOBAL` |
| Benign pickle opcodes | none dangerous |
| Vulnerable hash / signature | mismatch / absent |
| Hardened hash / signature | match / valid |
| Tampered signature | invalid |
| Pickle files in hardened project | 0 |
| Pinned dependencies | 5 |
| SBOM components | 5 |
| Gate exits (vulnerable / hardened) | 1 / 0 |

## Threat-to-control mapping

| Threat | Control | Evidence | Residual risk |
|---|---|---|---|
| Malicious pickle | Static scan plus format migration | Canary flagged; hardened tree has no pickle | Blocklist misses novel encodings |
| Artifact substitution | SHA-256 manifest | Mismatch found; repaired manifest verifies | Attacker can replace manifest too |
| Manifest tampering | HMAC-SHA256 signature | Valid signature and rejected tamper | Demo key is not secret-managed |
| Dependency confusion | Exact pins | Five pinned versions | A pinned version can still be compromised |
| Unknown components | SBOM | Five components with versions and purls | SBOM completeness is not verified |
| Risky build enters production | CI gate | Exit 1 versus 0 | Gate only enforces implemented checks |

## Defense-in-depth perspective

The lab layers controls: pins constrain what gets installed, the format change
removes execution from the load path, the manifest detects substitution, the
signature detects manifest tampering, and the SBOM gives an inventory to check.
None of these is sufficient alone. Pins do not protect against a compromised
release; hashes do not protect against a replaced manifest; a signature does not
protect a leaked key; an SBOM does not protect against an unlisted dependency.

The honest claim after a green gate is: "the implemented checks passed on this
artifact set." That is narrower than "the supply chain is secure," and it is the
only claim the evidence supports.

## Deliverables checklist

- [ ] `artifacts/audit.json`, `metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] The hardened project tree with pinned requirements, safe loading, regenerated manifest, signature, and SBOM.
- [ ] Verification output showing the hardened project passes and a tampered manifest fails.
- [ ] `report.md` answers every reflection question and records the canary handling rule.
- [ ] `python check_lab13.py --artifacts artifacts` exits 0.

## Success criteria

- [ ] All six rules are detected with the correct severity and file.
- [ ] The canary is flagged and the benign pickle is not, using static inspection only.
- [ ] The hardened project contains no pickle artifacts and a safe loader.
- [ ] Manifest hashes and the HMAC signature verify; a tampered manifest is rejected.
- [ ] The SBOM has five pinned components and the model hash.
- [ ] The CI gate exits 1 on the vulnerable project and 0 on the hardened one.
- [ ] The report states that a passing gate is not proof of supply-chain security.
- [ ] `python check_lab13.py --artifacts artifacts` exits 0.

## How to check yourself

The checker re-reads the canary and benign pickles with `pickletools`, recomputes
every hash, verifies the HMAC, tampers with the manifest itself, and inspects the
SBOM. It cannot judge whether your findings explain the risk or whether your
remediation is complete. Use the rubric and reflection questions for that.

## Rubric (20 points)

| Item | Points |
|---|---:|
| Complete audit with correct rules and severities | 6 |
| Static pickle inspection without execution | 4 |
| Hardened project with pins, safe loader, no pickles | 4 |
| Manifest, signature, tamper test, and SBOM | 4 |
| CI gate and report with residual risks and limitations | 2 |

## Reflection questions

1. Why is a pickle file a program rather than a data file, and what does that imply for "model download"?
2. The canary is benign. Why does the lab still refuse to load it, even to prove the point?
3. What does the signature protect that the manifest hash does not, and what protects the signature?
4. A static opcode blocklist is easy to bypass. What would a stronger verification approach look like?
5. Your gate passes. Name three supply-chain risks the gate does not measure.
6. Where should the signing key live, and why is the demo key in this lab not a secret?

## Hints

1. Audit by reading and hashing. Never call `pickle.load`, `joblib.load`, or `np.load(..., allow_pickle=True)` on the project.
2. `pickletools.genops` shows opcodes without executing them. Look for callable-construction opcodes such as `GLOBAL` and `REDUCE`.
3. The hardened copy needs all six fixes: pins, safe loader, no pickle, regenerated manifest, signature, and SBOM.
4. Verify by tampering with a copy and showing the gate fails. A gate that has never rejected anything is untested.

## Time box

| Hour | Work |
|---|---|
| 1 | Generate project, review files, audit dependencies and loader |
| 2 | Static pickle scan and findings schema |
| 3 | Harden: pins, safe loader, manifest, signature, SBOM |
| 4 | Verify, tamper test, gate, report |

Stop at 6 hours and submit with a note on what is incomplete.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `NotImplementedError` | A TODO block is untouched | Implement audit_project, harden_project, or verify_project |
| Canary not flagged | Loading it to inspect, or checking extensions only | Use `pickletools.genops` and inspect opcode names |
| Benign pickle flagged | Flagging any pickle | Only callable-construction opcodes are dangerous |
| Hash mismatch after hardening | Manifest written before the files | Write files first, then hash and write the manifest |
| Signature invalid | Signing a parsed object or adding whitespace after signing | Sign the exact manifest bytes and store hex |
| Tampered manifest still passes | Comparing with `==` | Use `hmac.compare_digest` |
| Gate passes vulnerable project | Gate checks verification only | Block when the audit has findings |

## Cleanup

```bash
# Windows PowerShell
Remove-Item -Recurse -Force artifacts
# macOS/Linux
rm -rf artifacts
```

Remove the virtual environment if you created one for this lab. Never commit `artifacts/`. LAB-13 also generates a benign pickle canary under `artifacts/`; delete it with the rest and do not distribute it.

## References

- [Lab catalog](../lab-catalog.md) · [Learning outcomes](../learning-outcomes.md)
- [References](../references.md) — R-08, F-17, F-05
- [Module page](../modules/m10-supply-chain/index.md) — M10 — Model Serialization, Dependencies, and ML Supply-Chain Security
- Package checking guide: `labs/lab-13-supply-chain-audit/CHECKING.md`

## What comes next

[LAB-14](lab-14.md) takes the hardened model to a local prediction service: bearer
tokens, request bounds, schema validation, safe errors, and security tests.
Module 11 explains the serving threat model before you start.
