# Checking Guide — LAB-14

## What the checker verifies

1. `metrics.json`, `run.json`, `report.md`, `manifest.json`, and `logs/requests.jsonl` exist; the manifest covers the four core outputs.
2. `run.json` records LAB-14 and its model hash matches `metrics.json`; the hash is a 64-character digest.
3. The recorded configuration binds to `127.0.0.1`, caps bodies at 8 KB and batches at 32, limits each role to 10 requests per 60 seconds, and documents bearer authentication.
4. The test set contains exactly the 18 reference cases; each expected status matches the reference and each actual status matches its expectation; no case is marked failed.
5. The valid request returns exactly one prediction; the rate-limit case allows 10 and rejects the 11th; the safe-error case shows no token marker.
6. Summary is 18 passed, 0 failed, and the gate exits 0.
7. The request log has at least 18 JSON lines with exactly the six allowed fields; it never contains a token value, an `Authorization` header, or feature payload content; it records every status code from 200 to 429 used by the suite.
8. `log_redaction` agrees with the file.
9. The report contains "authentication", "validation", "rate", "error", "defense", and "limitations".

The checker validates the recorded evidence. It does not re-run your server, so a forged metrics file could pass these checks; the rubric and oral-style reflection questions are where understanding is assessed.

## Reference results

| Case | Status |
|---|---:|
| health_ok | 200 |
| missing_token | 401 |
| invalid_token | 401 |
| viewer_forbidden | 403 |
| valid_predict | 200 |
| malformed_json | 400 |
| wrong_content_type | 415 |
| wrong_length | 422 |
| out_of_range | 422 |
| non_numeric | 422 |
| non_finite | 422 |
| batch_too_large | 422 |
| oversized_body | 413 |
| rate_limit | 429 |
| admin_stats | 200 |
| client_stats_forbidden | 403 |
| unknown_path | 404 |
| safe_error_body | 401 |

Summary: 18/18. Gate: 0. Tokens found in logs: none.

## Why these numbers matter

The interesting cases are the near-misses:

- `viewer_forbidden` (403) proves authentication and authorization are separate. A valid token is not a permission.
- `wrong_content_type` (415) and `oversized_body` (413) happen before parsing, so malformed or hostile bodies never reach the model.
- `non_finite` (422) catches `NaN`, which passes a naive range check.
- `rate_limit` (429) allows exactly 10 and rejects the 11th; the detail field records both counts.
- `safe_error_body` (401) verifies the response does not echo `wrong-token` or a stack trace.

A green suite means these 18 cases passed. It does not mean the API is secure.
There is no TLS, no identity provider, no concurrency test, and no adversarial
model input. The report must say so.

## Threat-to-control mapping

| Threat | Control | Evidence | Residual risk |
|---|---|---|---|
| Anonymous prediction | Bearer authentication | 401 for missing/invalid tokens | Demo tokens do not rotate |
| Valid token, wrong permission | Scopes | 403 for viewer and client on `/stats` | Scope model is coarse |
| Credential theft from logs | Redacted logging | No token values in 28 log lines | Other metadata can still leak usage |
| Resource exhaustion by large bodies | 8 KB cap | 413 before parsing | Many small requests remain possible |
| Oversized batch | 32-row cap | 422 on 33 rows | Per-row compute still varies |
| Malformed or hostile features | Schema validation | 400/415/422 cases | Valid-looking adversarial inputs pass |
| Brute force or scraping | Fixed-window rate limit | 10 allowed, 11th rejected | In-process state, restart clears it |
| Information leakage in errors | Generic error schema | No token, no traceback | Error codes still reveal validation rules |

## Common failures

| Symptom | Cause | Fix |
|---|---|---|
| `NotImplementedError` | A TODO block is untouched | Implement authorize, validate_payload, or RateLimiter.allow |
| Every request returns 401 | Token comparison against the header instead of the token | Split `Bearer <token>` and compare the token |
| Viewer can predict | Scope check skipped | Require `predict` for `/predict` and `stats` for `/stats` |
| NaN accepted | Range check only | Reject with `math.isfinite` before comparing bounds |
| 500 errors on bad input | Validation exception uncaught | Convert to `ApiError(422, ...)` and return JSON |
| Batch test returns 413 | 33 rows exceed the body cap | Use compact JSON; the cap is bytes, not rows |
| Rate test never hits 429 | Limiter reset or keyed per request | Key by role and reset once before the burst |
| Token appears in logs | Logging headers or the raw body | Log only role, path, status, and sizes |

## Rubric (20 points)

| Item | Points |
|---|---:|
| Authentication with constant-time comparison | 4 |
| Authorization scopes and correct 401/403 split | 4 |
| Body, batch, type, shape, range, and finiteness validation | 5 |
| Rate limiting and 429 behavior | 3 |
| Safe errors and redacted logging | 2 |
| Security tests and honest report | 2 |

## Reflection questions

1. Why should authentication happen before rate limiting, and why does the body-size check happen before both?
2. What is the difference between a 401 and a 403, and why does the distinction matter to a client?
3. Why is `NaN` dangerous in a validator that only checks `0 <= x <= 1`?
4. The rate limiter is in-process. What changes with four workers or a restart?
5. The safe-error test checks that the token is not echoed. What else should never appear in an error body?
6. The suite passes. Name three attacks it does not test.
