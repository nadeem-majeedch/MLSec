# Lesson 10.1 — The ML Supply Chain and Artifact Trust

<a id="m10-l1"></a>

**Module 10 · Lesson 1 of 4 · 1.5 hours · LO-21, LO-30**

## Scenario

A data scientist downloads a model from a public hub, loads it with `joblib.load`, and gets a working classifier. The workflow took two minutes. Nobody asked what else the file contained, which library version produced it, or whether the URL served the file the author uploaded.

The model works. That is the problem: a working result is weak evidence about the artifact's origin and contents. This lesson maps the chain that produced it and the points where trust is assumed rather than verified.

## Objectives

By the end of this lesson you will be able to:

1. Draw an ML supply chain with its artifact types, actors, and trust boundaries.
2. Explain how dependency confusion, typosquatting, artifact substitution, and build compromise differ.
3. Distinguish integrity, authenticity, provenance, and inventory, and name the control for each.
4. Identify which trust assumptions in a pipeline are verified and which are merely stated.
5. Prioritize supply-chain controls by the failure they prevent, not by tool popularity.

## 1. What travels, and who touches it

An ML system consumes more than code.

| Artifact | Produced by | Consumed by | Typical risk |
|---|---|---|---|
| Source code | Developers | Build system | Unreviewed change, malicious dependency |
| Dependencies | Package maintainers | Installer | Typosquat, compromised release, confusion |
| Training data | Collectors, vendors | Pipeline | Poisoning, leakage, license violation |
| Configuration | Engineers | Training and serving | Drift, secret leakage, unsafe default |
| Model weights | Training job | Registry, serving | Substitution, unsafe format |
| Container image | Build system | Runtime | Base-image vulnerability, tampering |
| SBOM and provenance | Build pipeline | Reviewers, policy engine | Missing, incomplete, unsigned |
| Prompts and tools | Application teams | LLM runtime | Injection, excessive capability |

The chain is not linear. A model may be retrained from a vendor checkpoint, packaged in a container built by a third party, and served with a dependency resolved from a public index. Each handoff is a trust boundary.

### Actors and incentives

| Actor | Supplies | Trust assumption |
|---|---|---|
| Upstream maintainer | Package or model | Acts in good faith and is not compromised |
| Public index | Name resolution | Serves the intended package for a name |
| Vendor | Data or model | Contractual terms and quality claims hold |
| Build system | Artifact | Builds the reviewed source with the recorded inputs |
| Registry | Storage and distribution | Preserves bytes and access policy |
| Platform team | Runtime | Applies isolation, patching, and monitoring |
| Reviewer | Approval | Has enough evidence and authority |

Most incidents exploit a gap between what an actor is assumed to do and what the system verifies. The rest of this module is about closing those gaps with checks that produce evidence.

## 2. Four supply-chain attacks

| Attack | Mechanism | Where it lands | Control |
|---|---|---|---|
| Dependency confusion | A public package shadows a private name; the installer prefers the public one | Dependency resolution | Scoped registries, exact pins with hashes, allowlists |
| Typosquatting | A package with a similar name is published | Developer install | Name review, lockfiles, allowlists |
| Artifact substitution | A model or wheel is replaced in transit or at rest | Download, registry | Hash and signature verification at load |
| Build compromise | The build system or a build dependency is modified | CI/CD | Isolated builds, provenance, reproducible builds |
| Malicious serialization | A model file executes code when loaded | Inference or conversion | Static inspection, safe formats, sandboxed conversion |

These are different failures with different fixes. A hash does not stop dependency confusion if the attacker controls the name resolution and the hash is fetched from the same place. A signature does not stop a compromised build system that signs the malicious output. An SBOM does not stop any of them; it improves the speed of response.

### The confused-deputy pattern

Many pipelines run with more privilege than the artifact needs. A model loader inside a training cluster may have network access, cloud credentials, and a writable model registry. A malicious pickle does not need to exploit the model; it inherits the loader's permissions.

Least privilege for artifacts means:

- load in a sandbox with no credentials and no egress;
- convert to a safe format before the artifact reaches a privileged environment;
- separate the account that writes to the registry from the account that reads;
- treat a new artifact like a new deployment, not a file copy.

## 3. Four properties people conflate

| Property | Question | Control | What it does not prove |
|---|---|---|---|
| Integrity | Are these the same bytes I recorded? | Hash, manifest | That the bytes are safe or correct |
| Authenticity | Who attests to these bytes? | Signature, key policy | That the signer is competent or uncompromised |
| Provenance | How and from what was this built? | Build attestation, in-toto, SLSA | That the inputs were trustworthy |
| Inventory | What components are inside? | SBOM | That the inventory is complete |

A useful sentence for a design review: "We verify integrity with a SHA-256 manifest, authenticity with a signature from the release key, provenance from the build attestation, and inventory from the SBOM. None of these proves the artifact is free of vulnerabilities."

### The verification chain

Each control protects the next one's input. If the manifest is unsigned, an attacker who can replace the model can also replace the manifest. If the signature key is stored beside the artifact, the attacker who can write the directory can sign a replacement. If the SBOM is generated from a partial environment, it will miss a component.

```mermaid
flowchart LR
    A[Reviewed source] --> B[Isolated build]
    B --> C[Artifact bytes]
    C --> D[SHA-256 manifest]
    D --> E[Signature over manifest]
    E --> F[Registry policy]
    F --> G[Load-time verification]
    G --> H[Sandboxed runtime]
```

The chain is only as strong as the weakest link, and the weakest link is usually key management or the build environment, not the hash function.

## 4. LAB-13's vulnerable project

LAB-13 makes the abstractions concrete with six findings.

| Rule | Severity | Finding | Why it matters |
|---|---|---|---|
| DEP-001 | High | Unpinned dependencies | Resolution can change between installs; a malicious release can satisfy the requirement |
| ART-001 | High | `joblib.load` inference path | Loading may execute code from the artifact |
| ART-002 | Critical | Callable-construction opcodes in `canary.pkl` | The file can import and call a callable |
| ART-003 | High | Manifest hash mismatch | The recorded hash does not match the bytes |
| ART-004 | Medium | Missing signature | No attestation of who produced the manifest |
| ART-005 | Medium | Missing SBOM | No component inventory for review or response |

The canary is benign and is never loaded. The lab scans it statically with `pickletools.genops`, which parses opcodes without executing them. That choice is the lesson: you can learn what an artifact would do without doing it.

### What the audit does not find

The six rules are a small, explicit set. The project could also have:

- a dependency whose pinned version contains a known vulnerability;
- a model trained on poisoned data;
- a container base image with an unpatched library;
- a build step that fetches code at build time;
- a license that forbids the intended use.

The lab's gate would pass some of these. A report that says "no findings" means "no findings from these six rules," not "no risk."

## 5. Prioritizing controls

Order controls by the failure they prevent and the evidence they produce.

| Priority | Control | Prevents | Evidence |
|---|---|---|---|
| 1 | Do not execute untrusted artifacts | Code execution at load | Static scan record; sandbox logs |
| 2 | Use safe formats | Deserialization attacks | Loader code; format allowlist |
| 3 | Pin and hash dependencies | Silent resolution changes | Lockfile with hashes |
| 4 | Verify integrity at promotion | Artifact substitution | Manifest check at gate |
| 5 | Sign and verify | Manifest substitution | Signature verification log |
| 6 | Record provenance | Unknown build inputs | Attestation, build log |
| 7 | Generate and review SBOM | Unknown components | SBOM diff, component list |
| 8 | Monitor and revoke | Post-deployment compromise | Alerts, revocation record |

The order is not universal. A regulated environment may prioritize provenance; a small team may start with pins and safe formats. What matters is that each control has a failure it addresses and a test that shows it works.

### Negative tests

A control is not implemented until it has failed correctly at least once.

- Corrupt one byte of the artifact: the hash check must fail.
- Tamper with the manifest: the signature must fail.
- Add an unpinned requirement: the gate must fail.
- Introduce a pickle file into the hardened tree: the gate must fail.

LAB-13 performs the manifest tamper test and checks the gate's exit codes on the vulnerable and hardened projects. Without those negative cases, a green gate could mean the check is not running.

## 6. Framework mapping

| Framework | Relevant practice | LAB-13 evidence |
|---|---|---|
| NIST SSDF (SP 800-218) | Protect software, produce well-secured software, respond to vulnerabilities | Pins, safe loader, audit, gate |
| SLSA | Build provenance and isolation | Not fully implemented; manifest and report are partial |
| CycloneDX / SPDX | Component inventory | Five-component SBOM |
| OWASP A08:2021 | Software and data integrity failures | Pickle and manifest findings |
| NIST AI RMF | MAP and MANAGE supply-chain risk | Trust map, residual risk, gate |

Mapping is not certification. It shows a reviewer which practice a control supports and where the evidence lives.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Treating a model file as data | The extension looks harmless | Decide whether the loader can execute |
| Verifying the hash after loading | The load is the convenient step | Inspect and verify before load |
| Pinning versions without hashes | The lockfile looks complete | Add hashes where the ecosystem supports them |
| Assuming a private index is safe | It is internal | Scope resolution; use allowlists and pins |
| Signing with a key stored in the repo | It works in CI | Use a secret manager or keyless signing |
| Claiming SLSA compliance from a manifest | The terms are unfamiliar | Map each claim to a specific requirement |
| No negative test | The happy path passes | Break the artifact and confirm failure |
| SBOM as a one-time PDF | It was requested once | Generate per build and diff on change |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Same requirement installs different code | Unpinned or range dependency | Lock the resolution and record hashes |
| Hash matches on the attacker's file | Manifest fetched from the same untrusted source | Sign the manifest; verify with a trusted key |
| Signature valid for a malicious build | Build system compromised | Isolate builds; require provenance; rotate keys |
| Scanner reports nothing | Rule set does not cover the format | Inspect manually; add rules; do not infer safety |
| Gate blocks every build | Findings treated as binary | Add severity thresholds and an approved exception path |
| SBOM lists packages you did not expect | Transitive dependencies | Review and document them; that is the point |

## Check your understanding

1. Name four artifact types in an ML supply chain and one risk for each.
2. How does dependency confusion differ from typosquatting?
3. What does a signature prove that a hash does not, and what does neither prove?
4. Why is loading an artifact a privilege decision?
5. A gate reports zero findings. Write the sentence that correctly describes what that means.

Answers are in the [quiz answer key](quiz-answers.md) and discussed in the exercises.

## Summary

- An ML supply chain includes code, dependencies, data, configuration, weights, containers, SBOMs, and people.
- Trust boundaries sit at every handoff: index, vendor, build, registry, runtime.
- Dependency confusion, typosquatting, artifact substitution, build compromise, and malicious serialization are different failures with different controls.
- Integrity, authenticity, provenance, and inventory are distinct; each has a control and a limit.
- LAB-13 finds six issues in a toy project: one critical, three high, two medium.
- Controls are ordered by the failure they prevent; negative tests prove a control is running.
- A green gate means the implemented checks passed. It does not mean the supply chain is secure.

## Next

Continue to [Lesson 10.2 — Unsafe serialization and safe formats](lesson-2-unsafe-serialization-and-safe-formats.md), where the canary's opcodes become a static inspection exercise.
