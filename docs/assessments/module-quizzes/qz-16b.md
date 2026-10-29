# Module 16 Alternate Quiz (QZ-16B)

| Field | Value |
|---|---|
| Module | M16 — End-to-End ML Security Assessment |
| Quiz A | [QZ-16](../../modules/m16-end-to-end-assessment/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-33 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-16b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. Scope and non-goals

Which item is a **non-goal** rather than an in-scope asset for an assessment of a local credit-scoring API?

A. The scoring API at version 2.3  
B. The vendor's hosted training pipeline  
C. The deny/approve decision the API supports  
D. The API's input schema and feature set

## 2. A test that can fail

Which test plan entry is falsifiable?

A. "Review the model for robustness."  
B. "At ε = 0.05, run 40-step PGD with three restarts on the frozen 500-row base set; report ASR and robust accuracy against the undefended baseline."  
C. "Check that the system is secure."  
D. "Ensure the model behaves well under attack."

## 3. Findings and baselines

True or false: an attack result without a clean or random baseline can still be reported as a finding.

## 4. Remediation content

True or false: a usable remediation recommendation names an owner, a cost or effort estimate, and the residual risk that remains after the control.

## 5. Zero budget

Why does a zero-budget test belong in every attack experiment? Answer in one or two sentences.

## 6. Test-count arithmetic

A plan lists 20 tests. The team executes 14, of which 9 pass, 3 fail, and 2 are inconclusive. Four tests are blocked and two are not run.

Compute the execution rate, the pass rate among executed tests, the failure rate among executed tests, and the share of inconclusive results. Explain why reporting "9 of 10 passed, so 90% passed" would be misleading.

## 7. Find the flaw

A project plan says:

> The dataset has no names or email addresses, so we will commit it to the public portfolio repository. The model and attack scripts will also be public.

Identify two flaws in the data-handling decision and state the correction.

## 8. Scenario: the 11-hour scope

You have 11 hours to assess a local credit-scoring API that you own. Write a one-page scope covering the decision, assets and classification, adversary profile, two or three questions, deliverables, and explicit non-goals. Keep the target local and the data synthetic or licensed.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can scope an assessment that produces evidence, not activity. |
| 10 | Pass. Review the missed item before starting a project. |
| 8–9 | Reread M16.L2 and L3, especially falsifiable tests and findings. |
| Below 8 | Reread M16 and rebuild the scope and test matrix. |
