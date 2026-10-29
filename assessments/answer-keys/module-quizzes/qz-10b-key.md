# QZ-10B Answer Key — Module 10

**Scoring:** items 1–5 = 1 point each; items 6–7 = 2 points each; item 8 = 3 points. Total 12. Pass 10/12.

## 1. C — safetensors

Safetensors stores tensor data and metadata in a format whose loader does not execute arbitrary constructors. That removes the pickle opcode path that makes deserialization dangerous. "Safer" is the accurate word: the parser can still have bugs, and origin still needs verification.

- **A, B, and D** are pickle-based. Renaming a pickle does not change its opcodes.
- The course still recommends verifying origin and using safe formats even when the loader is restricted.

Tag: M10 · LO-21 · Bloom 2 · D1.

## 2. B — identity plus integrity

A hash answers "are these the same bytes?" A signature answers "who attests to these bytes, and have they changed since signing?" The signature binds a key identity to the manifest content and fails if either changes.

- **A** is a model-quality claim; a signature says nothing about accuracy.
- **C** is a legal and governance claim; a signature does not establish it.
- **D** confuses verification with execution.

Tag: M10 · LO-21 · Bloom 2 · D1.

## 3. False

A version pin tells the installer which version to request, not which bytes it will receive. If the index or registry can replace the artifact under the same version, the pin does not protect you. Content hashes in a lock file, a trusted index, and signature verification are what bind the version to specific bytes.

Tag: M10 · LO-21 · Bloom 2 · D1.

## 4. True

An attestation is a statement by a builder about how an artifact was produced. If the builder is compromised, it can sign a truthful-looking attestation for a malicious artifact. The attestation's value depends on the builder's isolation, identity, and policy, not only on the signature.

Tag: M10 · LO-21 · Bloom 2 · D1.

## 5. Required element

A scanner error means the gate has no evidence that the artifact is safe; treating "no result" as "pass" lets unknown artifacts through. Failing closed trades availability for integrity, which is the correct default for a promotion gate. The error should be visible and actionable, not silently converted into a pass.

Tag: M10 · LO-21 · Bloom 3 · D2.

## 6. Required elements

The manifest defines the verification boundary: files not listed are not covered by the hash or signature. An attacker can replace `tokenizer.json` with a malicious or different file, and the signature over the manifest still verifies because the manifest never claimed anything about that file.

Two changes:

1. Add every runtime artifact the loader reads to the manifest, with its own SHA-256, and sign the updated manifest.
2. Verify the manifest and every listed file at load or promotion time, and fail if any required file is unlisted or its hash differs. Provenance and an SBOM should also record the tokenizer as a component.

A signature that covers only part of the runtime is a partial control; the unlisted file is outside the trust boundary.

Tag: M10 · LO-21 · Bloom 3 · D2.

## 7. Required elements (two flaws and the consequence)

Two of:

- **The return code is ignored.** If the scanner crashes, is missing, or exits nonzero without printing "CRITICAL", `result.stdout` may be empty and the gate prints "gate passed." That is a fail-open path.
- **Only `CRITICAL` is checked.** High or medium findings pass silently; the policy is not stated and is weaker than it looks.
- **String matching is brittle.** Output formatting changes, localization, or a finding on stderr can evade the check.
- **No hash or signature verification.** The gate scans content but does not establish that the artifact is the approved one.
- **No negative test.** Nothing shows the gate can fail on a tampered artifact.

Consequence: an unsafe or substituted artifact can be promoted while the pipeline reports success, and the failure is silent. The gate should check the return code, parse structured output, enforce a stated severity policy, verify the manifest/signature, and have a tamper test.

Tag: M10 · LO-21 · Bloom 4 · D3.

## 8. Required elements (three controls, evidence, negative tests, residual risk)

A workable order:

| Control | Evidence verified | Negative test |
|---|---|---|
| 1. Manifest hash check | Every runtime file's SHA-256 matches the signed manifest | Flip one byte in a file and confirm promotion fails |
| 2. Signature verification | The manifest signature verifies with the pinned trusted key | Tamper with the manifest or use an untrusted key and confirm failure |
| 3. Provenance and policy check | Build attestation names the approved source, commit, builder, and inputs; SBOM and scans meet policy | Supply an artifact from an unapproved commit or with missing attestation and confirm rejection |

A dependency/artifact scan can be a fourth control: no pickle artifacts, pinned hashes, no known-critical vulnerabilities, with a negative test using a deliberately bad package.

One residual risk: a compromised signing key or build system can produce valid hashes, a valid signature, and a truthful-looking attestation for a malicious artifact. Other candidates: the scanner misses a novel issue; the SBOM omits a copied component; an insider with promotion rights bypasses policy. State one with an owner and monitoring plan.

The gate must verify evidence itself, not trust a registry boolean such as `signed: true`. "We have a gate" without a negative test is not evidence that it can fail.

Tag: M10 · LO-21 · Bloom 5 · D3.
