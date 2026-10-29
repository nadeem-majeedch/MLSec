---
title: Knowledge Check — QZ-10
---

# Knowledge Check — QZ-10

**Module 10 · 10 items · 14 points · about 20 minutes**

Answer without running LAB-13. For item 5, give counts and severities.

---

**1. (1 point)** Why is a pickle file best described as a program rather than a data file?

A. It is always compressed.  
B. Its opcodes can import modules and call callables during deserialization.  
C. It can only store NumPy arrays.  
D. It is encrypted by default.

---

**2. (2 points)** Name four pickle opcodes associated with callable construction and state what each does at a high level.

---

**3. (1 point)** Which approach inspects a pickle without executing it?

A. `joblib.load` inside a try/except  
B. `pickletools.genops`  
C. `pickle.loads` in a subprocess  
D. Running the model on a test batch

---

**4. (2 points)** Match each control to what it establishes: integrity, authenticity, provenance, inventory.

- A SHA-256 manifest  
- A signature over the manifest  
- A build attestation  
- An SBOM

---

**5. (2 points)** LAB-13 reports six findings. State the total and the counts by severity, and name the rule with the highest severity.

---

**6. (1 point)** An internal package is named `acme-utils`. An attacker publishes a public `acme-utils` with a higher version, and the installer prefers the public index. Which attack is this?

A. Typosquatting  
B. Dependency confusion  
C. Artifact substitution  
D. Build compromise

---

**7. (2 points)** A CI gate must fail closed. Describe two conditions under which it should exit nonzero even if no rule found a defect, and explain why.

---

**8. (1 point)** An SBOM is generated from `requirements.txt`. Why can it be incomplete?

A. SBOMs cannot list Python packages.  
B. It may omit transitive, build-time, or copied components that are not in that file.  
C. It only lists licenses.  
D. It is always complete if the file is pinned.

---

**9. (1 point)** LAB-13 signs the manifest with a demo HMAC key stored in the repository. What does the signature demonstrate, and what does it not establish?

A. It proves the artifact is safe and authentic to anyone.  
B. It demonstrates the verification flow and tamper rejection; it does not establish authenticity against someone with repository access.  
C. It proves the build was reproducible.  
D. It replaces the need for an SBOM.

---

**10. (1 point)** Which is a valid negative test for an artifact gate?

A. Confirm the known-good artifact passes.  
B. Tamper with the manifest and confirm verification fails.  
C. Increase the model's accuracy.  
D. Add a comment to the README.

---

*When you have finished, compare your answers with the [answer key](quiz-answers.md).*
