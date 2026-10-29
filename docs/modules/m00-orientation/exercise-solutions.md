# Module 00 Exercises — Model Answers

**Read only after completing your own attempt.** These are model answers, not the only acceptable answers. Your reasoning matters more than matching the wording.

---

## Exercise 1 — Environment verification report

### Expected values

If `artifact.txt` contains exactly the eleven characters `mlsec-lab-01` followed by one newline, the file is **12 bytes** and the SHA-256 is:

```text
4ff7794ac45e6255f7ed6926943f91bd4968b9834592ca2f2958504e4862380b
```

After adding `-tampered` before the newline, the hash becomes:

```text
fb40fd8c7e2bfccf3a42ca2d2d9fd8bb3a421666cef52bd8ff42315a48a8dc1b
```

Your package versions should match the pinned requirements. A typical report:

| Field | Example value |
|---|---|
| Operating system | Windows 10.0.19045, 64-bit |
| Python | 3.14.7, `C:\Users\you\MLSec\.venv\Scripts\python.exe` |
| NumPy / pandas / scikit-learn | Versions from `requirements.txt` |
| Virtual environment | `C:\Users\you\MLSec\.venv` |
| Original file | 12 bytes, `4ff7794a…380b` |
| Tampered file | 21 bytes, `fb40fd8c…dc1b` |
| Verification | `OK` before, `MISMATCH` after |

### Why the hashes differ

SHA-256 is a cryptographic digest of the exact bytes. Changing the content changes the digest. This is useful for integrity: a manifest tells you whether a file changed, not whether it is safe. A file can match its manifest and still contain malicious code if the manifest was created after the compromise. Provenance and scanning are separate controls.

### Common partial answers

- Recording only the Python version and not the packages: not sufficient for reproducibility.
- Hashing with `open(path, "r")` and `read()`: line-ending translation can change bytes on Windows. Use `"rb"`.
- Saying "the hash changed because the file got bigger": true but incomplete; the hash is sensitive to any byte change, including one that preserves length.

---

## Exercise 2 — Authorization review

| Request | Decision | Conditions met | Conditions missing or violated |
|---|---|---|---|
| A — public CTF container | **ALLOW** | Ownership/public sandbox, scope defined by the challenge, lawful purpose, no personal data, rules published | None, provided you stay inside the container and follow the platform rules |
| B — former employer production API | **DENY** | None that matter; an old login is not permission | Written permission, current scope, data handling (real customer data), disclosure path; using a revoked-but-working credential may itself be unauthorized access |
| C — your own digits model | **ALLOW** | Ownership, scope (local), lawful purpose, no personal data, no destructive action | None |
| D — public library vulnerability | **ASK / stop and disclose** | Lawful purpose (defensive research), no personal data | Disclosure path and remediation window; immediate publication violates coordinated disclosure |

### Request B — example message

> Thank you for the request. I can help, but I cannot use the production API or my old login. I need written authorization that names the system, the allowed tests, the time window, and a security contact, and the work should run against a local replica with synthetic data. If that is not possible, I can review the model design and threat model instead.

This is under 80 words, declines the unsafe path, and offers a lawful alternative.

### Request D — first three steps

1. Stop testing and preserve the minimal reproducer and logs.
2. Contact the maintainer privately through their security policy with the version, impact, and a suggested fix; do not include real user data.
3. Agree on a remediation window and disclosure date; do not publish an exploit before a fix or an agreed deadline.

### What earns full credit

- Request B is not accepted because of the old credential.
- Request A is accepted only inside the challenge scope.
- Request D separates discovery from publication.
- The message is professional and offers an alternative.

---

## Exercise 3 — A 12-week study plan

A workable plan for 6 hours per week:

| Week | Focus | Deliverable | Retrieval |
|---:|---|---|---|
| 1 | M00 lessons 00.1–00.2 | Environment report draft | Explain adversarial ML vs AppSec |
| 2 | M00 lesson 00.3 + exercises | Ethics statement, authorization review | Five-part authorization test from memory |
| 3 | LAB-01 part 1 | Working environment and split | Name the artifact files |
| 4 | LAB-01 part 2 | Model, metrics, manifest | Explain why the manifest matters |
| 5 | M01 lessons 1–2 | Notes and NumPy examples | Broadcasting rules |
| 6 | M01 lessons 3–4 | pandas and scikit-learn examples | `fit` vs `transform` |
| 7 | M01 lesson 5 + QZ-01 | Reproducibility note; quiz | Sources of nondeterminism |
| 8 | M02 lessons 1–2 | Loss and gradient exercises | Cross-entropy and learning rate |
| 9 | M02 lessons 3–4 | Evaluation and leakage exercises | Precision vs recall |
| 10 | LAB-01B | Audit report | Three leakage types |
| 11 | M03 lessons 1–3 | Asset and boundary inventory | CIA vs privacy |
| 12 | M03 lessons 4–5 + QZ-03 | Threat model draft | ATLAS vs AI RMF |

**Buffer.** Week 12 doubles as the buffer; if nothing slips, use it for the LAB-02 threat model. A second buffer can come from weeks 5–6 if the Python refresher is easy.

**Most likely to slip.** LAB-01B (week 10) and the threat model (weeks 11–12), because both require judgment and writing, not just running code.

**Cut first.** Optional challenge exercises and extra papers. **Never cut.** LAB-02, the ethics statement, the manifest, and the reflection. They are the evidence that the level was completed.

**Reviews for Module 03.** Schedule 1 day, 3 days, 7 days, and 21 days after finishing the threat model. At each review, redraw the data-flow diagram from memory and name one control you would test.

### Scoring rubric (10 points)

| Criterion | Points |
|---|---:|
| All modules and labs scheduled | 3 |
| Total time within 72 hours and includes a buffer | 2 |
| Retrieval activities, not only reading | 2 |
| Realistic risk analysis and cut list | 2 |
| Review schedule for Module 03 | 1 |

---

Return to the [exercises](exercises.md) or start [LAB-01](../../labs/lab-01.md).
