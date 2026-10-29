# Lesson 10.3 — Dependency and Artifact Scanning in CI

<a id="m10-l3"></a>

**Module 10 · Lesson 3 of 4 · 1.5 hours · LO-21**

## Scenario

The CI pipeline has a security stage. It runs a scanner, prints a report, and exits 0. The vulnerable toy project from LAB-13 passes. So does a project with a `.pkl` loader and a manifest full of zeros.

The stage is not a gate. It is a log. This lesson is about turning checks into a gate that fails closed, and about the findings a scanner will never see.

## Objectives

By the end of this lesson you will be able to:

1. Explain how dependency resolution can change between installs and how pins and hashes constrain it.
2. Design a CI gate with severity policy, evidence, and an exception path.
3. Triage scanner findings using context rather than raw counts.
4. Write negative tests that prove a gate rejects a bad artifact.
5. State what dependency and artifact scanners cannot detect.

## 1. Resolution is the attack surface

A requirement is a constraint, not a file. `numpy>=2` can resolve to any future release that satisfies the range. The installer chooses a version from an index, following a resolution algorithm and any configured sources.

| Input | What can change | Control |
|---|---|---|
| Version range | The selected release | Pin exact versions |
| Index configuration | Which package a name resolves to | Scope private names; allowlist indexes |
| Transitive dependencies | Packages you did not name | Lock the full resolution |
| Package hashes | The bytes behind a version | Record and verify hashes |
| Install scripts | Code run during installation | Use `--only-binary` where possible; isolate builds |
| Build backend | Code that builds the wheel | Prefer wheels; verify provenance |

LAB-13's vulnerable `requirements.txt` lists five names with no versions. The hardened version pins all five: NumPy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0, joblib 1.5.3, PyYAML 6.0.3. That is the `DEP-001` finding and its remediation.

Pinning is necessary and insufficient. A pinned version can be compromised, yanked, or replaced on an index that does not enforce immutability. Hashes and provenance close part of that gap.

### Dependency confusion in one paragraph

A company publishes an internal package named `acme-utils` to a private index. An attacker publishes a public package with the same name and a higher version. If the installer is configured to prefer the public index, or to fall back to it, the attacker's package is selected. The fix is not "use a private index"; it is scoping the name to the private index, pinning with hashes, and configuring resolution so the public index cannot satisfy a private name.

## 2. What scanners look at

"Scanning" is a family of checks. Know which one produced a finding.

| Scan | Question | Typical signal | Blind spot |
|---|---|---|---|
| Dependency vulnerability | Does a pinned version have a known CVE? | Advisory database match | Unknown vulnerabilities; misconfigured use |
| License | Does a dependency's license permit use? | License identifier | Custom terms; transitive obligations |
| Secret | Is a credential in the repo or artifact? | Pattern or entropy match | Encoded or split secrets |
| Artifact format | Does the model contain dangerous content? | Opcode or signature rules | Novel encodings; semantic backdoors |
| Configuration | Are unsafe defaults set? | Rule match | Context-dependent risk |
| SBOM diff | Did the component inventory change? | Added or removed components | Undeclared components |

A scanner reports matches. A finding is not a risk until someone evaluates context: Is the vulnerable function reachable? Is the package used at build time or runtime? Is the license compatible with distribution? Is the model artifact actually loaded?

### LAB-13's rules

| Rule | Severity | Scan type | Evidence |
|---|---|---|---|
| DEP-001 | High | Requirements review | Five unpinned names |
| ART-001 | High | Loader review | `joblib.load` in the inference path |
| ART-002 | Critical | Static pickle scan | `REDUCE`, `STACK_GLOBAL` in the canary |
| ART-003 | High | Manifest verification | Recorded hash does not match |
| ART-004 | Medium | Signature check | No signature present |
| ART-005 | Medium | SBOM check | No SBOM present |

The gate policy treats critical and high as blocking. Medium findings are recorded and require an owner but do not fail the build in this lab. That is a policy choice, and the report should state it. A different organization might block on medium, or allow high with a time-limited exception.

## 3. Designing the gate

A gate is a function from evidence to an exit code, with a policy that a human can audit.

```text
inputs:   audit report, verification results, policy file
rules:    block if severity in {critical, high}
          block if a negative test fails
          block if the SBOM is missing for a release artifact
outputs:  exit 0 (pass) or exit 1 (block), plus a machine-readable report
```

Requirements for a useful gate:

| Requirement | Why |
|---|---|
| Deterministic | The same artifact produces the same verdict |
| Fast enough to run on every change | A slow gate gets bypassed |
| Fail closed on error | A crashed scanner is not a pass |
| Machine-readable output | The verdict can be attached to the artifact |
| Explicit policy | Severity thresholds are reviewable |
| Exception path | A documented, time-limited override with an owner |
| Negative test | Proves the gate can fail |
| No secrets in output | Scan reports can leak credentials or paths |

### Fail closed, not open

If the scanner is missing, the policy file is unreadable, or the hash cannot be computed, the gate must fail. The common anti-pattern is:

```python
try:
    findings = scan(path)
except Exception:
    findings = []   # "do not block the build"
```

That converts an operational error into a silent approval. LAB-13's gate instead exits 1 when the vulnerable project has findings and 0 only when the hardened project verifies. The checker tests both directions.

### Exceptions are part of the design

A gate with no exception path will be disabled the first time it blocks a release for a false positive. A workable exception has:

- a finding id and a justification;
- an approver with the authority to accept the risk;
- an expiry date;
- a compensating control;
- a record in the audit trail.

An exception without an expiry is a permanent policy change.

## 4. Triage: from finding to decision

A finding list is not a risk register. Triage adds context.

| Question | Example | Effect |
|---|---|---|
| Is the vulnerable code reachable? | The package is a build-time tool, not a runtime import | Lower priority |
| Is the artifact loaded? | The pickle is in the repo but never in the load path | Still remove it; lower immediate impact |
| Is the version affected? | The advisory covers < 2.0, the pin is 2.5.2 | Not applicable; document why |
| Is the license compatible? | Research-only license in a commercial product | Blocking, regardless of severity score |
| Is there a fixed version? | Upgrade available | Remediate |
| Is there a compensating control? | Sandbox, no egress, read-only | Reduces likelihood, not the finding |

For LAB-13, the critical finding (`ART-002`) is blocking because the file can construct callables. The high findings are blocking because they remove the controls that would detect substitution. The medium findings (no signature, no SBOM) are recorded; the hardened project fixes them anyway because the cost is low.

### False positives are data

Every scanner produces them. Track:

- how many findings were reviewed;
- how many were true positives;
- how many were false;
- what rule or configuration caused the false positive;
- what changed as a result.

A gate that nobody trusts is worse than no gate, because it creates a false sense of coverage.

## 5. Negative tests

A gate is only proven by rejection. Minimum tests for an artifact gate:

| Test | Expected result |
|---|---|
| Introduce a dangerous opcode in a test artifact | Fail with a specific rule id |
| Corrupt one byte of a hashed artifact | Hash verification fails |
| Tamper with the manifest | Signature verification fails |
| Remove a pin from requirements | `DEP-001` fires |
| Delete the SBOM from a release | Gate blocks |
| Point the scanner at a missing file | Gate fails closed, not open |
| Submit the known-good artifact | Gate passes |

LAB-13 implements the tamper test and the two exit-code checks. The report should state which negative tests were run and which were not.

## 6. Blind spots

| Blind spot | Why it matters | Complementary control |
|---|---|---|
| Unknown vulnerabilities | No advisory exists yet | Isolation, least privilege, monitoring |
| Malicious but valid package | The package installs and works | Allowlist, provenance, review |
| Compromised pinned release | The pin is correct; the bytes are not | Hashes, signatures, revocation |
| Build-time code execution | `setup.py` runs before your tests | Isolated builds, binary-only installs |
| Semantic model backdoor | The file is format-safe | Model testing, trigger scans (Module 06) |
| Incomplete SBOM | Undeclared transitive component | Generate from the resolved environment |
| Policy drift | The gate runs an old rule set | Version the policy; review changes |

The last row is easy to miss. A gate is software; its rules need tests and reviews like any other code.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Running the scanner but not failing the build | Blocking is disruptive | Define severity policy and exit codes |
| Catching scanner errors and passing | "Do not break CI" | Fail closed |
| Blocking on every finding | Uniform policy feels safe | Triage by reachability and context |
| Pinning versions without hashes | The lockfile looks sufficient | Add hashes and verify at install |
| Treating a CVE match as exploitation | The scanner reports a version | Check reachability and configuration |
| No negative test | The happy path is green | Add a known-bad artifact and expect failure |
| Exceptions without expiry | The release must ship | Expiry, approver, compensating control |
| Ignoring install-time scripts | The package imports cleanly | Isolate builds; prefer wheels |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Gate passes a bad artifact | No blocking rule or scanner not running | Add a negative test; check the exit code |
| Gate fails on a clean artifact | Rule too broad or policy misconfigured | Inspect the finding; narrow the rule; document the exception |
| Same lockfile, different install | Index or platform markers differ | Record the full resolution and environment |
| Hash mismatch after install | Wheel rebuilt or index serves different bytes | Use a hash-pinned lockfile; verify provenance |
| Scanner flags a package you do not use | Transitive or dev dependency | Trace the dependency; remove or document |
| Report contains secrets | Scanner logged environment variables | Redact output; restrict report access |
| Gate is too slow | Full scan on every commit | Incremental scan plus a full scan on release |

## Check your understanding

1. Why does an unpinned requirement make the build non-reproducible even if the code is unchanged?
2. What is dependency confusion, and which two controls reduce it?
3. What does a gate need in order to fail closed?
4. Why is a CVE match a finding rather than a confirmed exploitable risk?
5. Name three supply-chain risks a dependency scanner does not measure.

Answers are in the [quiz answer key](quiz-answers.md) and discussed in the exercises.

## Summary

- Dependency resolution is an attack surface: ranges, indexes, transitive packages, hashes, and install scripts all matter.
- LAB-13 finds five unpinned dependencies; the hardened project pins all five exact versions.
- Scanning is a family of checks; a finding needs triage for reachability, applicability, and context.
- A gate maps evidence and policy to an exit code, fails closed on error, and has an audited exception path.
- Negative tests prove the gate rejects bad artifacts; LAB-13 checks exit 1 on the vulnerable project and 0 on the hardened one.
- Scanners cannot see unknown vulnerabilities, malicious valid packages, compromised pins, build-time code, or semantic backdoors.
- A green gate means the implemented checks passed, not that the supply chain is secure.

## Next

Continue to [Lesson 10.4 — Provenance, signing, SBOM, and promotion gates](lesson-4-provenance-signing-and-promotion.md), where the evidence becomes an artifact that a registry can enforce.
