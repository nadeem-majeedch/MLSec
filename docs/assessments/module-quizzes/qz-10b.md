# Module 10 Alternate Quiz (QZ-10B)

| Field | Value |
|---|---|
| Module | M10 — Model Serialization, Dependencies, and ML Supply-Chain Security |
| Quiz A | [QZ-10](../../modules/m10-supply-chain/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-21 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-10b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. Data, not instructions

Which format stores arrays or tensors **without** constructing arbitrary Python objects during load?

A. A pickle file  
B. A joblib file  
C. A safetensors file  
D. A pickle file with a `.bin` extension

## 2. Signature versus hash

What does a digital signature add over a SHA-256 hash?

A. It proves the artifact is accurate on a test set  
B. It binds an identity to the exact bytes and detects changes after signing  
C. It guarantees the training data were lawful  
D. It makes the artifact executable

## 3. Version pins

True or false: pinning a dependency to an exact version guarantees that the package content cannot change.

## 4. Build attestations

True or false: a signed build attestation is only as trustworthy as the build system that produced it.

## 5. Failing closed

Explain in one or two sentences why a CI artifact gate should fail closed when the scanner errors or cannot complete.

## 6. The unlisted file

A signed manifest covers `model.pkl` and `config.json` but not `tokenizer.json`, which the loader also reads.

Explain the verification gap, what an attacker can do without breaking the signature, and the two changes needed to close it.

## 7. Find the flaw

The code below is meant to block unsafe artifacts in CI.

```python
result = subprocess.run(["scanner", artifact_path], capture_output=True)
if "CRITICAL" in result.stdout.decode():
    sys.exit(1)
print("gate passed")
```

Identify two flaws and explain the consequence for a pipeline that uses this gate.

## 8. Scenario: the promotion gate

A local model registry accepts uploads from several accounts and deploys the latest file automatically.

Design a promotion gate with three controls in order. For each, state the evidence it verifies and one negative test that proves the control can fail. End with one residual risk that remains after all three.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can connect supply-chain claims to verifiable evidence. |
| 10 | Pass. Review the missed item before LAB-13. |
| 8–9 | Reread M10.L2–L4, especially manifests and signatures. |
| Below 8 | Reread M10 and rebuild LAB-13 from the starter. |
