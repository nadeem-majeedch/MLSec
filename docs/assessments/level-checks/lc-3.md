# Level 3 Check — Practical Defenses (LC-3)

| Field | Value |
|---|---|
| Level | 3 — Practical defenses and secure engineering |
| Modules | M08–M11 |
| Items | 10 |
| Points | 20 |
| Time guide | 35 minutes |
| Pass | 16/20 |
| Outcomes | LO-16, LO-17, LO-18, LO-20, LO-21, LO-22, LO-23 |
| Answer key | Separate file: `assessments/answer-keys/level-checks/lc-3-key.md` |

Answer without notes. Items 1–6 are worth 1 point, items 7–8 are worth 2 points, and items 9–10 are worth 5 points. For audits, name the missing element before proposing a fix.

## 1. Adaptive evidence (1 point)

Which result best supports a robustness claim?

A. ASR 0 under FGSM at one budget  
B. ASR 0.12 under PGD with BPDA at a stated budget, with clean accuracy and the base set reported  
C. Clean accuracy 0.99 on the test set  
D. No attack was run

## 2. Entity split (1 point)

Which split prevents entity leakage when the same customer has multiple rows?

A. A random row-wise split  
B. `GroupShuffleSplit` grouped by customer  
C. Stratification by the label  
D. A larger test set

## 3. Safe format (1 point)

Which format avoids executing arbitrary constructors during load?

A. A pickle file  
B. A joblib file  
C. A safetensors file  
D. A pickle renamed to `.bin`

## 4. Authorization status (1 point)

A request presents a valid token that lacks the `stats` scope and calls `GET /stats`. Which status code is correct?

A. 400  
B. 401  
C. 403  
D. 429

## 5. Manifest coverage (1 point)

True or false: a signature over a manifest protects files that the manifest does not list.

## 6. Fail closed (1 point)

True or false: a CI artifact gate should fail open when the scanner errors, to keep delivery moving.

## 7. Gradient masking (2 points)

Name two signs of gradient masking and one adaptive test that can reveal it.

## 8. Integrity, authenticity, authorization (2 points)

Distinguish artifact integrity, artifact authenticity, and API authorization. Give one concrete check for each.

## 9. Scenario: the defense report (5 points)

A report says:

> Our defense reduces attack success from 0.40 to 0.02 under FGSM. Clean accuracy fell from 0.94 to 0.86, and we changed the decision threshold from 0.50 to 0.35 to recover recall. We did not run an adaptive attack because the drop was large.

Identify three confounds or gaps and design the minimum retest that would make the claim interpretable. State what the current numbers can and cannot support.

## 10. Scenario: promotion and serving (5 points)

A local recommendation model is uploaded to a registry and served by an API. The registry accepts unsigned uploads, and the API has no authentication.

Design four controls across the supply chain and serving path. For each, give one negative test. End with one residual risk and the evidence that would show the gate works.

## Scoring

| Score | Interpretation |
|---:|---|
| 18–20 | Strong. You can audit a defense and a delivery path. |
| 16–17 | Pass. Review the missed item and the linked lab. |
| 12–15 | Not yet. Rerun LAB-11 through LAB-15 as needed. |
| Below 12 | Reread M08–M11 before Level 4. |
