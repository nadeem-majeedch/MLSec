# LAB-14 — Hardening a Local Prediction API

**Tier A · 5 hours · Difficulty 4 · Module M11 · Outcomes LO-22, LO-28, LO-30 (supporting)**

## Why this lab exists

A model that answers HTTP requests is an attack surface with a model attached.
Before the first partner integrates, the service needs an answer for four
questions: who is calling, what may they do, how much may they send, and what
does the service say when the request is wrong. Each answer is a control, and
each control has a failure mode you can test.

This lab builds the service with the Python standard library and hardens it in
layers. You write the security-critical functions — token authorization, payload
validation, and rate limiting — while the routing, bounds, logging, and test
suite are given. The suite is the evidence; the report is where you explain what
the evidence does not prove.

## The system and the threat model

| Element | Assumption |
|---|---|
| Asset | A local digit-classification endpoint and its request logs |
| Attacker goal | Unauthorized predictions, resource exhaustion, information leakage, or scraping |
| Attacker knowledge | The API shape is public; tokens are not |
| Attacker capability | Send arbitrary HTTP requests to the loopback service |
| Constraints | The service binds to 127.0.0.1; bodies ≤ 8 KB; batches ≤ 32 rows; 10 requests per 60 s per role |
| Base behavior | Valid requests return class predictions; `/health` is public; `/stats` requires an admin scope |
| Metric | HTTP status codes for 18 scripted cases, plus log-redaction checks |
| Lifecycle stage | Serving and API boundary |
| Out of scope | TLS, internet exposure, identity-provider integration, distributed rate limiting, model evasion |

The demo tokens stand in for credentials issued by an identity provider. They are
constants in the source so the lab is reproducible; that is exactly what you must
not do in production.

## What you produce

A folder inside `labs/lab-14-secure-serving/` containing:

| File | Contents |
|---|---|
| `metrics.json` | Configuration, 18 test records, summary, gate result, model hash, redaction check |
| `logs/requests.jsonl` | One JSON record per request: id, method, path, status, role, body size |
| `run.json` | Lab id, model version and hash, environment versions |
| `report.md` | Controls, test table, residual risks, trade-offs, limitations |
| `manifest.json` | SHA-256 hashes of the four files above |

The reference implementation writes these under `artifacts/`. Your completed
`starter.py` must produce the same structure.

## Prerequisites

- Module 01 Lesson 5 (files, JSON, exceptions) and Lesson 6 (modules and testing).
- Module 11 Lessons 1–3 (API authentication, resource bounds, input validation).
- LAB-13 recommended (artifact and model integrity before serving).

## Environment

- Python 3.14.7; `numpy==2.5.2`, `pandas==3.0.5`, `scikit-learn==1.9.0`, `joblib==1.5.3`, `PyYAML==6.0.3`.
- CPU only; the suite finishes in a few seconds.
- No network egress; the server binds to loopback on an ephemeral port.
- No cloud account or API key.

```bash
cd labs/lab-14-secure-serving
python -m pip install -r requirements.txt
python solution.py --out artifacts
python check_lab14.py --artifacts artifacts
```

## Safety rules

- Bind to `127.0.0.1` only. Do not change the bind address or expose the port.
- Use the demo tokens only against this local service. Never reuse them.
- Do not point the test client at a third-party service.
- Keep the rate-limit test small; it sends 11 requests, not a flood.
- Delete `artifacts/` when finished if your environment does not ignore it.

## Task specification

1. **Authenticate.** Parse `Authorization: Bearer <token>`. Compare against every
   demo token with `hmac.compare_digest` and return the role only when a match is
   found. Missing, malformed, or unknown credentials produce 401 with a
   `WWW-Authenticate: Bearer` header.
2. **Authorize.** `POST /predict` requires the `predict` scope; `GET /stats`
   requires `stats`. A valid token without the scope gets 403.
3. **Bound the request.** Reject bodies over 8 KB with 413 before reading them
   into the application, and require `Content-Length`. Enforce JSON content type
   with 415 and a 32-row batch cap with 422.
4. **Validate features.** The body must be an object with a non-empty `features`
   list. Each row has exactly 64 numbers; booleans are not numbers; every value
   must be finite and in [0, 1]. Violations return 422 with a stable error code.
5. **Rate limit.** Allow 10 requests per role per 60-second fixed window and
   return 429 for the next one. The limiter must be resettable for the test.
6. **Fail safely.** Return JSON with a request id and an error code/message. No
   stack trace, no token echo, no payload echo. Log only request metadata.
7. **Test.** Run the 18 cases. Record expected and actual status codes, plus the
   valid prediction count, rate-limit counts, and token-leak flag.
8. **Report.** Explain the control order, the trade-offs, the residual risks,
   and why a green suite is not a security proof.

## Control order

The order is part of the design, not an implementation detail:

1. **Body size** — cheapest rejection; protects the parser and memory.
2. **Authentication** — identifies the caller before allocating per-caller state.
3. **Rate limit** — bounds work for authenticated callers.
4. **Content type and JSON parsing** — rejects incompatible or malformed bodies.
5. **Schema and range validation** — rejects hostile values before the model.
6. **Prediction** — only fully validated requests reach the model.

The suite encodes this order. For example, an oversized body with a valid token
returns 413, not 401, because the size check runs first.

## Starter and TODO map

| File | TODO | Function | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `authorize` | Authenticate a bearer token with constant-time comparison and enforce a scope |
| `starter.py` | TODO 2 | `validate_payload` | Validate content, shape, dtype, finiteness, and range |
| `starter.py` | TODO 3 | `RateLimiter.allow` | Count requests per key in a fixed window |

The reference path is separate from the learner path. Run `solution.py` first to see a complete artifact set, then complete `starter.py` and check your own output. The package checking guide is `labs/lab-14-secure-serving/CHECKING.md`.

## Expected outputs

| Case | Expected status |
|---|---:|
| `health_ok` | 200 |
| `missing_token` | 401 |
| `invalid_token` | 401 |
| `viewer_forbidden` | 403 |
| `valid_predict` | 200 |
| `malformed_json` | 400 |
| `wrong_content_type` | 415 |
| `wrong_length` | 422 |
| `out_of_range` | 422 |
| `non_numeric` | 422 |
| `non_finite` | 422 |
| `batch_too_large` | 422 |
| `oversized_body` | 413 |
| `rate_limit` | 429 |
| `admin_stats` | 200 |
| `client_stats_forbidden` | 403 |
| `unknown_path` | 404 |
| `safe_error_body` | 401 |

Summary: 18 passed, 0 failed; gate exit 0; no tokens in logs.

## Threat-to-control mapping

| Threat | Control | Evidence | Residual risk |
|---|---|---|---|
| Unauthorized use | Bearer authentication | 401 cases | Demo tokens do not rotate |
| Privilege confusion | Scopes | 403 cases | Coarse permission model |
| Large-body exhaustion | 8 KB cap | 413 case | Many small requests still cost work |
| Batch amplification | 32-row cap | 422 case | Per-row cost varies |
| Parser confusion | Content-type and JSON checks | 415, 400 cases | Valid JSON with hostile values remains |
| Non-finite values | `math.isfinite` check | 422 case | Valid-looking adversarial inputs pass |
| Scraping | Rate limit | 429 case | In-process, per-worker state |
| Credential leakage | Redacted logs | No tokens in 28 lines | Metadata still reveals traffic patterns |
| Internal disclosure | Generic errors | No token or traceback | Error codes reveal validation rules |

## Defense-in-depth perspective

Each layer answers a different question. Authentication does not bound work;
rate limiting does not validate content; validation does not hide internals; safe
errors do not stop abuse. The service is defensible because the layers are
independent and the failure of one does not silently disable the others.

Composition has limits. A valid token can still send adversarial but in-range
features; the rate limit does not exist across processes; the logs are only as
private as the filesystem. The report must state which layer would fail first
under a realistic load and what would replace the demo controls in production.

## Deliverables checklist

- [ ] `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- [ ] Results for all 18 security cases, including the expected rejection reason for each.
- [ ] `report.md` answers every reflection question and lists residual risks.
- [ ] `python check_lab14.py --artifacts artifacts` exits 0.

## Success criteria

- [ ] All 18 cases return exactly the expected status code.
- [ ] Missing, malformed, and unknown tokens return 401; a valid token without scope returns 403.
- [ ] Non-finite, non-numeric, out-of-range, wrong-shape, and oversized-batch inputs are rejected with 422.
- [ ] The 11th request in a fresh window returns 429.
- [ ] Error bodies contain no token, payload echo, or traceback.
- [ ] The log has only the six metadata fields and no token values.
- [ ] The report states that a passing suite is not proof of security.
- [ ] `python check_lab14.py --artifacts artifacts` exits 0.

## How to check yourself

The checker validates the recorded evidence: configuration, expected/actual
status pairs, gate result, and redaction. It does not re-run your server. That is
a deliberate limitation of artifact-based checking: a forged metrics file could
pass. The rubric asks you to defend the design, and the reflection questions test
whether you understand what the suite leaves out.

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

1. Why does the size check run before authentication, and what would change if it ran after?
2. Why is a 403 the correct answer for a valid token without the scope, rather than a 401?
3. Why can a validator that checks `0 <= x <= 1` still accept a dangerous value?
4. What happens to the rate limit under four worker processes, and how would you fix it?
5. The suite passes. Name three attacks or failure modes it does not cover.
6. Which single control would you remove last, and why?

## Hints

1. Use `hmac.compare_digest` for token comparison. A plain `==` leaks timing information.
2. Validate shape, dtype, finiteness, and range before the model sees the payload. Reject the body; do not silently clip it.
3. The rate limiter counts per key in a fixed window. Decide whether a rejected request consumes budget and document it.
4. Error responses must be generic. If the token appears in an error body, the test suite should fail.

## Time box

| Hour | Work |
|---|---|
| 1 | Read the server skeleton and tests; implement authorization |
| 2 | Implement validation and rate limiting |
| 3 | Run the suite, fix status mismatches, inspect logs |
| 4 | Report: control order, threat mapping, trade-offs |
| 5 | Reflection and a fresh-process reproduction |

Stop at 7.5 hours and submit with a note on what is incomplete.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `NotImplementedError` | A TODO block is untouched | Implement authorize, validate_payload, or RateLimiter.allow |
| Every request 401 | Comparing the full header to the token | Split `Bearer <token>` and compare the token |
| Viewer can predict | Scope check skipped | Require `predict` on `/predict` |
| NaN accepted | Bounds check without finiteness | Use `math.isfinite` first |
| 500 on bad input | Validation exception escapes | Raise `ApiError(422, ...)` and return JSON |
| Batch case returns 413 | Compact JSON still too large | 33 rows of `0` fit; keep the body under 8 KB |
| Rate case never 429 | Limiter keyed per request | Key by role and reset once before the burst |
| Token in logs | Logging headers or body | Log role, path, status, and sizes only |

## Cleanup

```bash
# Windows PowerShell
Remove-Item -Recurse -Force artifacts
# macOS/Linux
rm -rf artifacts
```

Remove the virtual environment if you created one for this lab. Never commit `artifacts/`.

## References

- [Lab catalog](../lab-catalog.md) · [Learning outcomes](../learning-outcomes.md)
- [References](../references.md) — F-18, F-21
- [Module page](../modules/m11-serving-monitoring/index.md) — M11 — Secure Model Serving, API Security, Monitoring, and Incident Response
- Package checking guide: `labs/lab-14-secure-serving/CHECKING.md`

## What comes next

[LAB-15](lab-15.md) assumes the service is running and asks whether you can tell
normal traffic from drift, scraping, and evasion using only the telemetry the
service emits. Module 11 Lessons 4–6 cover monitoring, incident response, and
rollback before you start.
