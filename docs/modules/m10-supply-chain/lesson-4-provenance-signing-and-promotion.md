# Lesson 10.4 — Provenance, Signing, SBOM, and Promotion Gates

<a id="m10-l4"></a>

**Module 10 · Lesson 4 of 4 · 2 hours · LO-21, LO-30**

## Scenario

A model registry accepts any file uploaded by any account with write access. The deployment job downloads the latest file and serves it. There is a manifest, but nobody verifies it. There is a signature field in the schema, but it is optional and usually empty.

An attacker with a compromised developer account uploads a replacement model. The filename is the same, the accuracy on the smoke test is similar, and the deployment is automatic. This lesson is about the controls that make that substitution fail: signatures, provenance, inventories, and a promotion gate that verifies them.

## Objectives

By the end of this lesson you will be able to:

1. Explain what a signature adds over a hash, and what protects the signing key.
2. Describe build provenance and how it differs from a manifest.
3. Generate and review an SBOM, and state its completeness limits.
4. Design a promotion gate that verifies integrity, authenticity, provenance, and inventory.
5. Report a signed artifact's assurance with residual risk and revocation.

## 1. From hash to signature

A hash answers: are these the same bytes? A signature answers: who attests to these bytes, and have they changed since?

| Control | Protects against | Does not protect against |
|---|---|---|
| SHA-256 hash | Accidental corruption; naive substitution | An attacker who replaces both file and hash |
| Manifest | Loss of individual file integrity | A replaced manifest |
| HMAC signature | Manifest tampering by someone without the key | Key compromise; signer dishonesty |
| Asymmetric signature | Same, with public verification | Key compromise; signer dishonesty |
| Keyless signing with identity | Key management burden; ties signature to an identity | Identity compromise; policy errors |

LAB-13 uses **HMAC-SHA256** over the exact manifest bytes. The signer and verifier share a key. The lab's key is a demo constant, and the report must say so: a key in the repository is not a secret, and anyone with the repository can forge a signature. The value of the exercise is the verification flow and the negative test, not the cryptographic assurance.

### What the signature covers

Sign the manifest, not each file separately, and make the manifest list every file with its hash. Then:

- changing a file breaks its hash in the manifest;
- changing the manifest breaks the signature;
- replacing both requires the key.

If the signature covers only the model file, an attacker can add a loader or a configuration file. If the manifest omits a file, that file is outside the verification boundary.

### Key management is the hard part

| Question | Bad answer | Better answer |
|---|---|---|
| Where is the private key? | In the repo, in CI variables, on a laptop | Secret manager or hardware-backed key |
| Who can sign? | Anyone with write access | A dedicated release identity with approval |
| How is the public key distributed? | A wiki page | A pinned key in the verifier, or a transparency log |
| How is a key revoked? | Delete the file | Published revocation and a verifier policy |
| How is rotation handled? | Never | Versioned keys with overlap windows |

Sigstore's keyless model addresses part of this by binding a short-lived certificate to an OIDC identity and recording the signature in a transparency log. It reduces long-lived key risk and introduces new dependencies: identity provider trust, log availability, and policy about which identities are allowed.

## 2. Provenance

A signature says who signed. Provenance says how the artifact was built: source repository, commit, build command, builder identity, inputs, and environment.

| Question | Manifest + signature | Provenance |
|---|---|---|
| Which bytes? | Yes | Yes |
| Who attested? | Yes | Yes |
| From which source commit? | No | Yes |
| Built by which builder? | No | Yes |
| With which dependencies? | Partial | Yes |
| Reproducible from source? | No | Can be tested |

SLSA defines build levels that progressively require provenance, hosted builds, and hardened isolation. The levels are a vocabulary for maturity, not a certificate that a specific artifact is safe. A signed provenance statement is only as good as the builder that produced it: a compromised build system can produce a valid attestation for a malicious artifact.

in-toto describes a supply-chain layout: which steps must occur, who may perform them, and what artifacts they consume and produce. It is useful when a build has multiple stages and you need to verify the sequence, not just the final file.

### Reproducible builds

A reproducible build lets an independent party rebuild the artifact from source and compare hashes. That is the strongest provenance evidence, and it is difficult: timestamps, file ordering, compiler versions, and embedded paths all affect bytes.

For ML artifacts, full reproducibility may be impractical because training is stochastic and expensive. A weaker but useful claim: "the artifact was produced by this pipeline at this commit with these inputs, as attested by the builder." That is provenance, not reproducibility. Say which one you have.

## 3. SBOM

A software bill of materials lists the components in an artifact: name, version, supplier, identifiers, hashes, and relationships.

| Field | Example | Why |
|---|---|---|
| Component name | `numpy` | Identification |
| Version | `2.5.2` | Vulnerability matching |
| Supplier | Project or vendor | Accountability |
| Package URL (purl) | `pkg:pypi/numpy@2.5.2` | Machine-readable identity |
| Hash | SHA-256 of the distribution | Integrity |
| Dependency relationship | `scikit-learn` depends on `numpy` | Impact analysis |

LAB-13 emits a minimal CycloneDX-style SBOM with five components and the model hash. CycloneDX and SPDX are the common formats; the choice matters less than generating from the resolved environment and keeping it with the artifact.

### Completeness

An SBOM is complete only with respect to what the generator can see.

- A generator that reads `requirements.txt` misses transitive packages.
- A generator that reads the installed environment misses build-time tools.
- A hand-written SBOM misses whatever the author forgot.
- A container SBOM may miss files copied into the image after package installation.

Generate from the resolved lockfile or the built artifact, diff on every release, and treat an unexpected component as a finding. An SBOM is an inventory, not a safety certificate: a listed component can be vulnerable, and an unlisted one can be present.

### VEX and vulnerability context

An SBOM tells you a component is present. It does not tell you whether a known vulnerability is exploitable in your use. Vulnerability Exploitability eXchange (VEX) statements record a supplier's assessment — affected, not affected, fixed, under investigation — with justification. They are useful and depend on the supplier's honesty and competence.

## 4. The promotion gate

A promotion gate is the policy enforcement point between a build and a registry or environment. It verifies evidence before the artifact is accepted.

| Check | Evidence | Failure action |
|---|---|---|
| Integrity | Manifest hashes match | Reject |
| Authenticity | Signature verifies with a trusted key | Reject |
| Provenance | Builder and source match policy | Reject or require review |
| Inventory | SBOM present and includes required fields | Reject or warn |
| Scan policy | No blocking findings, or an approved exception | Reject |
| Test evidence | Required tests passed for this artifact | Reject |
| Freshness | Artifact and evidence within the policy window | Reject |

The gate should verify the evidence itself, not trust a boolean in a database that someone else could set. "Signed: true" in a registry record is not a signature verification.

### Environments and promotion

A typical flow:

```text
build -> quarantine registry -> verify -> staging registry -> verify -> production registry
```

Each promotion re-verifies the evidence and records who approved it. The artifact bytes do not change between environments; only the policy and the approval do. Rebuilding for each environment creates a new artifact and a new verification problem.

### Revocation

Verification is not a one-time event. A key can be compromised, a vulnerability discovered, or a build system found to be untrusted. The registry needs:

- an artifact-to-key mapping, so affected artifacts can be found;
- a revocation list or policy that verifiers consult;
- a way to mark an artifact as withdrawn without deleting the audit trail;
- a rollback path for deployed systems.

## 5. Threat-to-control mapping

| Threat | Control | LAB-13 evidence | Residual risk |
|---|---|---|---|
| Malicious pickle | Static scan plus format migration | Canary flagged; hardened tree has no pickle | Blocklist misses novel encodings |
| Artifact substitution | SHA-256 manifest | Mismatch found; repaired manifest verifies | Attacker can replace manifest too |
| Manifest tampering | HMAC-SHA256 signature | Valid signature; tampered manifest rejected | Demo key is not secret-managed |
| Dependency confusion | Exact pins | Five pinned versions | A pinned release can be compromised |
| Unknown components | SBOM | Five components with versions | Completeness is not verified |
| Risky build enters production | CI gate | Exit 1 versus 0 | Gate enforces only implemented checks |
| Compromised build system | Provenance and isolation | Not implemented in the lab | A compromised builder can sign malicious output |
| Key compromise | Key management and rotation | Not implemented; demo key | Forgery until revocation propagates |

The lab implements the middle rows. The last two are outside its scope, and the report must say so.

## 6. Reporting a signed artifact

A defensible statement:

> The hardened artifact set passes the implemented checks: every manifest hash matches, the HMAC-SHA256 signature verifies over the exact manifest bytes, a one-byte tamper is rejected, the project contains no pickle artifacts, all five dependencies are pinned, and the SBOM lists five components. The signing key is a demo constant stored in the repository, so the signature demonstrates the verification flow but does not establish authenticity against an attacker with repository access. Build provenance, key management, and SBOM completeness were not evaluated.

That is narrower than "the supply chain is secure," and it is what the evidence supports.

### What to put in the release record

| Field | Example |
|---|---|
| Artifact hashes | SHA-256 of each file and the manifest |
| Signature and key id | Algorithm, key identifier, verification result |
| Provenance reference | Build id, source commit, builder identity |
| SBOM location | Path or registry link, format, component count |
| Gate result | Policy version, findings, exceptions |
| Approver | Identity and role |
| Revocation contact | Who to call if the key or build is compromised |

The release record is what an incident responder needs at 2 a.m. If it takes an hour to find the key id, the signature was not operationally useful.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Signing the artifact but not the manifest | The artifact is the important file | Sign the manifest; it covers every file |
| Storing the key in the repo | It works in CI | Secret manager or keyless signing |
| Treating "signed" as "safe" | The check passed | Separate integrity, authenticity, and behavior |
| Generating an SBOM from a partial environment | It is fast | Generate from the resolved lockfile or artifact |
| A gate that reads a boolean | The registry schema has a field | Verify the signature at the gate |
| No revocation plan | Nobody plans for compromise | Artifact-to-key mapping and revocation policy |
| Rebuilding per environment | It is the existing pipeline | Promote the same bytes; verify again |
| Claiming SLSA compliance without provenance | The terms are aspirational | Map each claim to a specific requirement and evidence |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Signature verifies locally, fails in CI | Different manifest bytes (line endings, encoding) | Sign and verify exact bytes; no reformatting |
| Tampered manifest passes | Comparing with `==` or verifying the wrong file | Use `hmac.compare_digest`; verify the signed bytes |
| SBOM component count differs between builds | Generated from a different environment | Generate from the lockfile; diff releases |
| Provenance says the wrong commit | Build triggered from a branch, not a tag | Bind provenance to the resolved commit and inputs |
| Revoked artifact still deploys | Verifier does not consult revocation | Add the check to the promotion gate |
| Key rotation breaks old artifacts | Only one key is trusted | Support overlapping key versions with expiry |
| Gate passes an artifact with a missing SBOM | SBOM check is a warning | Make it blocking for release artifacts |

## Check your understanding

1. What does a signature add over a hash, and what protects the signature?
2. How does provenance differ from a manifest?
3. Why can an SBOM be complete with respect to a generator and still miss a component?
4. What must a promotion gate verify directly rather than trust from a registry field?
5. Write a scoped assurance statement for a signed artifact with a demo key.

Answers are in the [quiz answer key](quiz-answers.md) and discussed in the exercises.

## Summary

- A signature binds a hash to a key; the manifest should cover every file, and the signature should cover the manifest.
- Key management determines whether the signature means anything. LAB-13's demo key demonstrates the flow, not authenticity.
- Provenance records how an artifact was built; SLSA and in-toto provide vocabulary and structure, not automatic assurance.
- An SBOM inventories components; its completeness is limited by what the generator can see.
- A promotion gate verifies integrity, authenticity, provenance, inventory, scans, and tests directly, and rejects on failure.
- Revocation and rollback are part of verification; a key or build can be compromised after promotion.
- Report assurance narrowly: which checks passed, with which keys, and what was not evaluated.

## Next

Complete [LAB-13](../../labs/lab-13.md), then the [knowledge check](quiz.md) and [exercises](exercises.md). The lab produces the audit, the hardened project, the tamper test, and the gate evidence this module has built toward.
