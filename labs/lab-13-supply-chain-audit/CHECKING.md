# Checking Guide — LAB-13

## What the checker verifies

1. `audit.json`, `metrics.json`, `run.json`, `report.md`, and `manifest.json` exist; the manifest covers the four core outputs, and `run.json` records LAB-13.
2. The audit contains exactly six findings — DEP-001, ART-001, ART-002, ART-003, ART-004, ART-005 — with the expected severity and file for each.
3. Severity totals are 1 critical, 3 high, 2 medium.
4. The canary pickle contains dangerous opcodes, the benign pickle does not, and the audit reports exactly that split.
5. The hardened project pins all five dependencies to the reference versions, includes no `*.pkl` files, and its loader uses `allow_pickle=False` with no pickle-based load.
6. Every hardened manifest hash matches the file bytes.
7. The HMAC-SHA256 signature on the hardened manifest verifies, and a one-byte-tampered manifest does not.
8. The SBOM is CycloneDX-formatted, has five components with matching pinned versions and purls, and its model hash equals the SHA-256 of `model.npz`.
9. `metrics.verification` records the vulnerable/hardened/tamper results, and the CI gate exits 1 for the vulnerable project and 0 for the hardened project.
10. The report contains "pickle", "hash", "signature", "sbom", "pin", and "limitations".

## Reference results

| Check | Result |
|---|---|
| Findings | 6 (1 critical, 3 high, 2 medium) |
| Canary flagged | yes |
| Benign pickle flagged | no |
| Hardened manifest hashes | match |
| Hardened signature | valid |
| Tampered manifest signature | invalid |
| Pickle files in hardened project | 0 |
| Pinned dependencies | 5 |
| SBOM components | 5 |
| Gate: vulnerable / hardened | 1 / 0 |

Pickle opcode evidence for the canary: `STACK_GLOBAL` and `REDUCE`. The benign
pickle uses only data opcodes.

## Why these numbers matter

The canary demonstrates the core rule without requiring malware: a pickle is a
program, and a static opcode scan can spot a callable reduction before anything
runs. But the scan is a blocklist. It will not catch every encoding, and it says
nothing about a benign-looking pickle whose loaded object has malicious
properties. The defensible control is to avoid pickle for model artifacts and to
verify signatures and hashes before loading anything.

Signing the manifest is not the same as signing the model. The signature covers
the manifest bytes; the manifest covers the file hashes. Break either link and
verification fails. That is why the checker tests the tampered case rather than
only the happy path.

A gate that passes means these checks passed. It does not mean the dependencies
are vulnerability-free, the build is reproducible, or the signing key is safe.

## Threat-to-control mapping

| Threat | Control | Evidence | Residual risk |
|---|---|---|---|
| Unpinned dependency resolves to a malicious release | Exact version pins | Five `==` pins | Pins can themselves be compromised |
| Malicious pickle executes at load | Format migration and static scan | Canary flagged, no pickle in hardened tree | Blocklist misses novel encodings |
| Artifact swapped after build | SHA-256 manifest | Hash mismatch detected and corrected | Manifest can be replaced with the artifact |
| Manifest tampered in transit | HMAC signature | Signature valid; tamper rejected | Demo key is not secret-managed |
| Unknown dependency inventory | SBOM | Five components with purls | SBOM can be incomplete or stale |
| Risky artifact reaches production | CI gate | Gate blocks vulnerable tree | Gate covers only the checks it runs |

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| `NotImplementedError` | A TODO block is untouched | Implement audit_project, harden_project, or verify_project |
| Canary not flagged | Scanning by unpickling or checking only file names | Use `pickletools.genops` and inspect opcode names |
| Benign pickle flagged | Treating any pickle as dangerous | Flag only callable-construction opcodes |
| Hardened hash fails | Hashing before writing all files | Regenerate the manifest after the files are final |
| Signature fails after copying | Signing the JSON object instead of the exact bytes | Sign `manifest.json` bytes and store hex |
| Tampered manifest still verifies | Comparing with `==` on user input | Use `hmac.compare_digest` |
| SBOM missing versions | Listing dependency names only | Include pinned versions and purls |

## Rubric (20 points)

| Item | Points |
|---|---:|
| Complete audit with correct rules and severities | 6 |
| Static pickle inspection without execution | 4 |
| Hardened project with pins, safe loader, no pickles | 4 |
| Manifest, signature, tamper test, and SBOM | 4 |
| CI gate and report with residual risks and limitations | 2 |

## Reflection questions

1. Why is unpickling an artifact equivalent to running code, even when the file is called a "model"?
2. The canary is benign. What would change in your audit if it were not, and why does the lab still avoid loading it?
3. What does the HMAC signature protect that the SHA-256 manifest does not?
4. Why is a blocklist of pickle opcodes weaker than migrating to `np.load(allow_pickle=False)`?
5. The gate passes the hardened project. Name three supply-chain risks it still does not cover.
6. Where would the signing key live in a real pipeline, and who should be able to use it?
