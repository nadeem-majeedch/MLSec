# Module 11 Alternate Quiz (QZ-11B)

| Field | Value |
|---|---|
| Module | M11 — Secure Model Serving, API Security, Monitoring, and Incident Response |
| Quiz A | [QZ-11](../../modules/m11-serving-monitoring/quiz.md) |
| Items | 8 |
| Points | 12 |
| Time guide | 20 minutes |
| Pass | 10/12 |
| Outcomes | LO-22, LO-23 |
| Answer key | Separate file: `assessments/answer-keys/module-quizzes/qz-11b-key.md` |

Answer without notes. Items 1–5 are worth 1 point, items 6–7 are worth 2 points, and item 8 is worth 3 points.

## 1. Bad credentials

A request presents a token with an invalid signature. Which status code is correct?

A. 400  
B. 401  
C. 403  
D. 429

## 2. Work before trust

Why should authentication run before expensive model inference?

A. It improves model accuracy  
B. It prevents unauthenticated callers from consuming inference capacity  
C. It replaces input validation  
D. It makes rate limiting unnecessary

## 3. Error detail

True or false: returning a detailed validation error to an external caller, including feature names and expected ranges, is always safe.

## 4. Per-IP limits

True or false: a per-IP rate limit is sufficient to stop a distributed credential-stuffing or query-flood attack.

## 5. Evasion signals

Name two monitoring signals that could indicate an evasion campaign, and give one benign cause for each.

## 6. Fixed-window burst

A limiter allows 30 requests per key per fixed 60-second window. A client sends 30 requests at 12:00:59 and 30 at 12:01:01.

How many requests are allowed across the two-second span, and what property of fixed windows does this demonstrate? Name one alternative limiter design.

## 7. Find the flaw

The code below is presented as incident recovery.

```python
if new_model_accuracy < 0.90:
    restore_previous_model()
    print("incident resolved")
```

Identify two flaws and explain why the incident should not be closed at this point.

## 8. Scenario: the query burst

A local inference service alerts on a 50× query burst from one token, together with inputs whose feature values fall outside the training range. You own the service and may inspect its logs and checkpoints.

Write a bounded incident-response outline with containment, evidence handling, a rollback criterion, and one residual risk. Do not touch any third-party system.

## Scoring

| Score | Interpretation |
|---:|---|
| 11–12 | Strong. You can respond without destroying evidence or overclaiming recovery. |
| 10 | Pass. Review the missed item before LAB-15. |
| 8–9 | Reread M11.L4 and L5, especially evidence and rollback criteria. |
| Below 8 | Reread M11 and rerun LAB-14 and LAB-15 in order. |
