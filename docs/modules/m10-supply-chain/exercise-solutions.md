# Exercise Solutions — Module 10

**Worked answers and marking guidance.** Accept equivalent reasoning. The key distinctions are rule mapping, verification versus trust, and what a pass does not prove.

## Exercise 1 — Map findings to rules

**1. Findings.**

| Issue | Rule | Severity |
|---|---|---|
| `numpy`, `scikit-learn>=1.8`, `joblib` are unpinned | `DEP-001` | High |
| `joblib.load` in the inference path | `ART-001` | High |
| `canary.pkl` contains `STACK_GLOBAL`, `REDUCE` | `ART-002` | Critical |
| Manifest hash does not match the replaced model | `ART-003` | High |
| No signature file | `ART-004` | Medium |
| No SBOM | `ART-005` | Medium |

Note that `pandas==3.0.5` and `PyYAML==6.0.3` are pinned; the finding is about the unpinned names, not the file as a whole. A correct answer names the specific unpinned requirements.

**2. Blocking under critical + high.**

Four findings are blocking: one critical (`ART-002`) and three high (`DEP-001`, `ART-001`, `ART-003`). Two are medium (`ART-004`, `ART-005`) and are recorded, not blocking, under this policy. State the policy; another organization might block on medium.

**3. A risk outside the rules.**

Accept one:

- the model was trained on poisoned or unlicensed data;
- a pinned dependency is compromised even though the pin is correct;
- the container base image has an unpatched vulnerability;
- the build system is compromised and produces a valid-looking artifact;
- the model has a semantic backdoor that passes format checks.

These are not defects the six rules measure. The audit's scope is the format and the recorded checks, not the model's behavior or the build's integrity.

**4. Why "the canary is harmless" is the wrong argument.**

- **You cannot know from the filename or the author's assurance.** The lab's canary is benign by construction; a real artifact may contain a different stream with the same rule match. The rule flags capability, not intent.
- **A control that is waived for the known case will be waived for the unknown case.** The finding is evidence that the project accepts executable serialization in its artifact set. The correct response is to remove the path, not to adjudicate each file's friendliness.
- **The artifact may change after review.** A file that is benign at audit time can be replaced. The hardened tree should contain no pickle files at all.

**5. First action.**

Hash the file, move it to quarantine, and inspect it statically with `pickletools.genops` (or `pickletools.dis`). Record the opcode list and the rule id. **Do not call `pickle.load`, `joblib.load`, or any loader on it**, even to "see what it does."

## Exercise 2 — Interpret three scan results

**1. Conclusions.**

- `canary.pkl`: contains callable-construction opcodes. Treat as dangerous; do not load. The finding is critical until proven otherwise.
- `model.pkl`: no opcodes from the blocklist. It is a pickle stream with ordinary data (on this scan). It is not thereby trusted.
- `third_party.bin`: the scanner could not parse it. The result is "unknown," which is not "clean." Treat it as untrusted.

**2. Actions for `third_party.bin`.**

1. Quarantine it; record its hash and size.
2. Identify the actual format from magic bytes, not the extension (`file` or a small header read is enough).
3. If it is a pickle or a container that may contain one, run the static scan on the inner content with size and recursion limits.
4. If it is not needed for serving, reject it.
5. If it is needed, convert it in a disposable sandbox with no credentials and no egress, validate the output, and promote only the converted artifact.

**3. Why `model.pkl` is not proven safe.**

Accept three:

- the blocklist may be incomplete for the protocol or for opcodes the scanner does not list;
- the stream may contain data that is wrong or backdoored even with no dangerous opcodes;
- a later stage (framework load, conversion, custom unpickler) may execute code;
- the scanner may have read a different file than the loader will;
- opcodes can be obfuscated or nested;
- the artifact's origin and license are still unverified.

**4. Missing `BUILD`.**

`BUILD` can invoke `__setstate__` or update an object's state, so a stream using it can trigger behavior without `REDUCE`. The scanner would produce a false negative. Add the opcode to the rule set, test the scanner with a known sample, and do not rely on a blocklist as the only control; migrate to a safe format.

**5. One-sentence rule.**

A clean static scan supports only the claim that no blocklisted opcodes were found in the bytes that were scanned; it does not establish that the artifact is safe to load.

## Exercise 3 — Onboard a vendor model

**1. Decision.**

**Reject until conditions are met** (or accept with conditions that block serving). The vendor's evidence is insufficient: the signature is only a boolean claim, the SBOM is empty, dependencies are unpinned, the format is executable, and the training data is proprietary and unspecified.

Conditions before serving:

- a verified signature over a manifest that covers every artifact, using a trusted key or identity;
- a static scan of the received file, with the opcode report;
- conversion to a safe format in a disposable sandbox, with parity tests;
- a real SBOM listing components, versions, and hashes, generated from the resolved environment;
- pinned dependencies with hashes;
- a data contract or model card describing the training data, its rights, and its limitations;
- serving in an environment without cloud credentials, with egress restricted and monitoring enabled.

**2. Conversion path.**

| Step | Environment | Evidence |
|---|---|---|
| Receive | Quarantine registry | Hash, size, timestamp, uploader |
| Inspect | Static scanner host | Opcode report; no execution |
| Convert | Disposable sandbox, no credentials, no egress | Conversion log, output hash, tool versions |
| Validate | Test harness | Shape/dtype checks, prediction parity on a fixed batch |
| Package | Build step | Manifest, signature, SBOM |
| Serve | Privileged runtime | Safe-format loader; no pickle |

**3. Why `"signed": true` is not verification.**

It is a mutable field in a registry record, not a cryptographic check. Verify the signature over the exact manifest bytes with a key or identity you trust; check the key id, its revocation status, and that the manifest covers every file you will load. Record the verification result, not the field.

**4. Empty SBOM.**

It tells you the inventory is absent, not that the model has no components. Request an SBOM generated from the resolved environment or the built artifact, including component names, versions, purls, hashes, and dependency relationships. Compare it with the dependencies you observe. An empty list is a finding.

**5. Residual risks.**

Accept two:

- the proprietary training data may contain poisoned, personal, or unlicensed content that no format control detects;
- the vendor's signing key may be compromised, or the build may be compromised while still producing a valid signature;
- conversion may change behavior in ways the parity test does not cover;
- the SBOM may be incomplete despite being non-empty;
- the model may have a semantic backdoor that passes format and behavior smoke tests.

**6. Vendor questions.**

Accept four, including one on data and one on keys:

- What data was used, under what rights, and does it contain personal data? Provide a model card and a data statement.
- How is the signing key stored, who can use it, how is it rotated, and how are signatures revoked?
- How was the SBOM generated, and can you provide the resolved dependency list with hashes?
- What is the vulnerability disclosure process, and what is the support window for this model version?
- Can you provide a reproducible build or provenance attestation?

## Exercise 4 — Design the promotion gate

**1. Six checks.**

| Check | Evidence |
|---|---|
| Integrity | Manifest hashes match every file |
| Authenticity | Signature verifies over the exact manifest bytes with a trusted key or identity |
| Provenance | Attestation names the builder, source commit, and inputs |
| Inventory | SBOM present, with the required fields and a plausible component count |
| Scan policy | No blocking findings, or an approved, unexpired exception |
| Test evidence | Required tests passed for this exact artifact hash |
| Freshness / revocation | Artifact and key are not revoked; evidence is within the policy window |

Any six of these are acceptable; the first four are essential.

**2. Failures.**

| Failure | Expected result | Check |
|---|---|---|
| One byte of a model file changes | Reject | Hash mismatch |
| Manifest edited after signing | Reject | Signature verification fails |
| A `.pkl` file added | Reject | Artifact format policy / scan rule |
| SBOM missing | Reject or block for release | Inventory check |
| Signature key revoked | Reject | Authenticity or revocation check |

**3. Negative tests.**

- Tamper with the manifest in a test fixture: proves the signature verifier can fail.
- Add a pickle file to a test artifact set: proves the format policy is enforced.
- Remove a pin from a test requirements file: proves `DEP-001` fires.
- Corrupt one byte of a hashed file: proves the integrity check runs.
- Delete the SBOM: proves the inventory check is blocking.

Use at least two; each proves a specific control can reject.

**4. Key in the repository.**

Problems: anyone with repository access can forge a signature, and the verifier cannot distinguish the legitimate signer from an attacker. Rotation and revocation become meaningless because the key is copied everywhere. Better: keep the signing key in a secret manager or hardware-backed store, or use keyless signing bound to a release identity; give the verifier only the public key or trust policy, and record signatures in an audit log or transparency log.

**5. Assurance statement.**

> The artifact passes the implemented promotion checks: every manifest hash matches, the signature verifies over the exact manifest bytes, the SBOM lists the resolved components, and the scan policy reports no blocking findings. The signing key is outside our full trust boundary, so the signature establishes that the artifact was signed by that key, not that the signer or build was uncompromised. Build provenance, SBOM completeness, and runtime behavior were not independently verified. The artifact should be treated as verified against the stated checks and not as proven free of vulnerabilities.
