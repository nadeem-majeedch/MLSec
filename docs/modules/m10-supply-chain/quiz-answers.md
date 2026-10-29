# Answer Key — QZ-10

**Module 10 · 10 items · 14 points**

Use this key after attempting the quiz.

## 1. (1 point) B — Opcodes can import and call

Pickle is a stack-machine format. Deserialization reconstructs arbitrary Python objects, and some opcodes resolve module attributes and invoke callables. The Python documentation explicitly warns against unpickling untrusted data.

## 2. (2 points) Any four correctly described

- `GLOBAL` — pushes a global object identified by module and name.
- `STACK_GLOBAL` — resolves a module/name pair taken from the stack.
- `REDUCE` — calls a callable with arguments from the stack.
- `BUILD` — invokes `__setstate__` or updates an object's `__dict__`.
- `INST` — instantiates a class with arguments.
- `OBJ` — builds an object from a class and arguments.
- `NEWOBJ` / `NEWOBJ_EX` — create a new object via a class's `__new__`.
- `EXT1` / `EXT2` / `EXT4` — resolve an object through the extension registry.

Half a point each, up to two points. A list of names without a description earns at most one point.

## 3. (1 point) B — `pickletools.genops`

`genops` parses the byte stream into opcodes without executing them. Loading in a subprocess still executes the payload; a try/except does not prevent execution; running the model is a dynamic test after loading.

## 4. (2 points) One point for all four correct

- SHA-256 manifest — **integrity**.
- Signature over the manifest — **authenticity** (who attests).
- Build attestation — **provenance** (how and from what it was built).
- SBOM — **inventory** (what components are inside).

A signature can also be described as integrity plus authenticity; accept that if the distinction is explained. The key is that the four are not interchangeable.

## 5. (2 points) Six findings: 1 critical, 3 high, 2 medium

- Critical: `ART-002`, callable-construction opcodes in `canary.pkl`.
- High: `DEP-001` unpinned dependencies, `ART-001` unsafe `joblib.load` path, `ART-003` manifest hash mismatch.
- Medium: `ART-004` missing signature, `ART-005` missing SBOM.

Award 1 point for the total and severity counts, 1 point for naming `ART-002` as critical.

## 6. (1 point) B — Dependency confusion

The attacker exploits name resolution across indexes, not a misspelled name (typosquatting), a replaced artifact, or a compromised build. The public package shadows the private name when resolution prefers the public index.

## 7. (2 points) Any two

- The scanner is missing, crashes, or returns an unreadable report → exit nonzero; a broken check is not an approval.
- The policy file cannot be read or is unsigned/unversioned → exit nonzero; the verdict is not auditable.
- A required artifact is missing (manifest, SBOM, signature) → exit nonzero; absence of evidence is a failed check.
- The evidence does not match the artifact being promoted (wrong hash or id) → exit nonzero; the verification is about a different file.
- A negative test fails (a known-bad artifact passes) → exit nonzero; the gate itself is not working.

The principle: operational failure must not be converted into a pass by an exception handler. Award 1 point per condition with a correct reason.

## 8. (1 point) B — It may omit transitive, build-time, or copied components

A requirements file names direct dependencies. The resolved environment includes transitive packages; the build may use tools not in the file; a container may copy files after installation. Generate from the lockfile or the built artifact and diff releases.

## 9. (1 point) B — Flow and tamper rejection, not authenticity

The HMAC demonstrates that the verifier detects a changed manifest when the key is secret. Because the demo key is in the repository, anyone with access can compute a valid MAC. Authenticity requires a key that only the signer controls, or an identity-based signing system with a trust policy.

## 10. (1 point) B — Tamper and confirm failure

A negative test checks that the gate rejects a bad case. Confirming the good case passes is a positive test; changing model accuracy or a README does not test the gate.
