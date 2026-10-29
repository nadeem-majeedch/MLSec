---
title: Module 10 Exercises
---

# Module 10 Exercises

**Four exercises · about 40 minutes · one scenario**

These exercises test audit judgment. You may use the LAB-13 rule list. Do not load or execute any artifact.

---

## Exercise 1 — Map findings to rules (10 minutes)

A colleague's project contains:

```text
requirements.txt
  numpy
  pandas==3.0.5
  scikit-learn>=1.8
  joblib
  PyYAML==6.0.3

inference.py
  import joblib
  model = joblib.load("artifacts/model.joblib")

artifacts/
  model.joblib
  manifest.json       # records sha256 for model.joblib, but the file was replaced
  canary.pkl          # contains STACK_GLOBAL and REDUCE
  training_notes.md
```

There is no signature file and no SBOM.

1. Map each issue to a LAB-13 rule (`DEP-001`, `ART-001`, `ART-002`, `ART-003`, `ART-004`, `ART-005`) and assign the severity from the lab.
2. How many findings are blocking under a policy that blocks critical and high? How many are medium?
3. Name one risk in this project that none of the six rules detects.
4. The team says "the canary is harmless, so we can ignore ART-002." Give two reasons that reasoning is wrong in a real project.
5. What is the first action you take on `canary.pkl`, and what do you explicitly not do?

---

## Exercise 2 — Interpret three scan results (10 minutes)

A static scanner returns:

```text
canary.pkl      -> ['REDUCE', 'STACK_GLOBAL']
model.pkl       -> []
third_party.bin -> scanner error: unrecognized format
```

1. What can you conclude about each file?
2. What do you do with `third_party.bin`? Give a sequence of actions, not a single verdict.
3. A colleague says `model.pkl` returned no dangerous opcodes, so the model is safe to load. Give three reasons this conclusion is unsupported.
4. The scanner's blocklist does not include `BUILD`. What is the likely consequence, and what should you do about it?
5. State the general rule for a clean static scan in one sentence.

---

## Exercise 3 — Onboard a vendor model (12 minutes)

A vendor sends:

- `model.pkl` (their format);
- `requirements.txt` with unpinned packages;
- a registry record with `"signed": true`;
- a JSON file labeled `sbom.json` containing only `{"components": []}`;
- a README saying the model was trained on "proprietary customer data."

Your team wants to serve it in a privileged environment with cloud credentials.

1. Decide: accept, accept with conditions, or reject. Justify with at least three controls that must be satisfied before serving.
2. Design the conversion path from `model.pkl` to a format your serving environment can load. Name the environment for each step and the evidence produced.
3. The registry field says `"signed": true`. Why is that not verification? What would you check?
4. The SBOM has zero components. What does that tell you, and what do you request?
5. Name two residual risks after all controls pass.
6. List four questions for the vendor, including one about the training data and one about key management.

---

## Exercise 4 — Design the promotion gate (8 minutes)

Your registry will accept only artifacts that pass a gate. The gate runs before an artifact enters the privileged environment.

1. List six checks the gate should perform and the evidence for each.
2. For each of these failures, state the expected result and which check fires:
   - one byte of a model file changes;
   - the manifest is edited after signing;
   - a `.pkl` file is added to the artifact set;
   - the SBOM is missing;
   - the signature key has been revoked.
3. Name two negative tests you would add to CI and what each proves.
4. The team proposes storing the signing key in the repository so the gate can verify. Give two problems and a better design.
5. Write a four-sentence assurance statement for an artifact that passes all checks but was signed with a key you do not fully trust.

---

## Self-assessment

| Criterion | Check |
|---|---|
| Findings use rule ids and severities consistently | [ ] |
| No artifact is loaded to inspect it | [ ] |
| Scanner errors are treated as failures, not passes | [ ] |
| The conversion path names environments and evidence | [ ] |
| "Signed: true" is not accepted as verification | [ ] |
| The gate has negative tests and a revocation check | [ ] |
| The assurance statement is scoped and honest | [ ] |

Worked answers: [exercise-solutions.md](exercise-solutions.md).
