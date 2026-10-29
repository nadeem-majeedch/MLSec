# Lesson 11.3 — Request Bounds, Validation, and Safe Output

<a id="m11-l3"></a>

**Module 11 · Lesson 3 of 6 · 1.5 hours · LO-22**

## Scenario

The API authenticates callers and checks their scopes. A partner sends a batch of 5,000 rows for a morning scoring run. The service accepts the token, reads the body, parses the JSON, and allocates a feature matrix. Memory usage spikes, the event loop stalls, and other partners time out. No credential was stolen and no model was attacked. The service simply had no answer to "how much may one caller send?"

That is a bounds problem. A second partner sends one row with 64 values, all inside `[0, 1]`, one of which is `NaN`. The range check passes because comparisons with `NaN` are false. The model returns a prediction computed from a non-finite value. That is a validation problem.

This lesson adds the bounds and checks, and then examines the output path, because a rejection that leaks internals is its own failure.

## Objectives

By the end of this lesson you will be able to:

1. Explain how body size, batch size, request rate, and concurrency exhaust a prediction service.
2. Enforce a body cap before parsing and a batch cap before model execution.
3. Validate JSON structure, types, shape, finiteness, and range with stable error codes.
4. Distinguish validation from robustness and state what a valid input can still do.
5. Design rate limits and quotas that match the service's trust model.
6. Return safe errors and logs that are useful without disclosing credentials or internals.

## 1. Four ways to exhaust a service

| Resource | Attack | What grows | Control |
|---|---|---|---|
| Memory | Huge body, deeply nested JSON, large batch | Request buffer, parser tree, feature matrix | Body cap, nesting limit, batch cap |
| CPU | Expensive rows, repeated maximum-size batches | Inference time, validation time | Batch cap, rate limit, per-request timeout |
| Connections | Slow or partial requests | Open sockets, worker threads | Read timeouts, header limits, connection caps |
| Budget | Many small requests, scraping | Model calls, downstream quota, cost | Rate limit, quota, per-client accounting |

An 8 KB body cap addresses the first row. It does not address a caller who sends 10,000 valid 1 KB requests. That is why bounds are layered: size per request, rows per request, requests per window, and quota per account.

### Body cap before parsing

The order is the control. If the service reads the body first and checks its length afterward, the hostile allocation has already happened.

```python
try:
    length = int(self.headers.get("Content-Length", "0") or 0)
except ValueError:
    return error(400, "bad_length")
if length <= 0:
    return error(411, "length_required")
if length > MAX_BODY:
    return error(413, "body_too_large")
body = self.rfile.read(length)
```

LAB-14 sets `MAX_BODY = 8192`. The oversized test sends 8,292 bytes and receives 413. Because this check runs before authentication, an oversized body with no token also receives 413; the service does not spend authentication work on a request it will not read.

`Content-Length` is not the only size signal in every protocol. Chunked transfer encoding has no length header, and a reverse proxy may have its own limit. LAB-14 requires the header for simplicity and returns 411 when it is missing. A production edge should enforce the same limit independently.

### Batch cap before allocation

`MAX_BATCH = 32` bounds rows per request. The check happens before the rows are converted to an array, so a 5,000-row list is rejected with 422 rather than materialized.

The cap is a policy choice, not a law. Thirty-two rows is small enough for a test and large enough to exercise batching. A real service chooses a cap from latency, memory, and the caller's contract, and documents it.

## 2. Content type and parsing

| Check | Failure | Status | Why |
|---|---|---|---|
| `Content-Length` valid | Non-integer or missing | 400 or 411 | The service cannot bound what it cannot measure |
| Body size | Over 8 KB | 413 | Protect memory and parser |
| Media type | Not `application/json` | 415 | Do not parse formats you did not intend |
| JSON syntax | Invalid JSON or invalid UTF-8 | 400 | The body is not the declared representation |
| Schema | Wrong structure, shape, type | 422 | The body is well-formed JSON but not a valid request |
| Semantics | Out of range, non-finite | 422 | The values are numeric but not acceptable |

The split between 400 and 422 is useful: 400 means "I cannot parse this"; 422 means "I parsed it, and it is not a valid request." A client can fix both, but the diagnostics differ.

LAB-14 accepts `Content-Type: application/json` with optional parameters by splitting on `;` and lowercasing. That is a small allowance for charset declarations, not a license to accept `text/plain`.

## 3. Schema, type, shape, and range

The payload contract is small and explicit:

```json
{"features": [[0.0, 0.0, "... 64 values ..."]]}
```

- The body is a JSON object.
- `features` is a non-empty list.
- The list has at most 32 rows.
- Each row is a list of exactly 64 numbers.
- Booleans are not numbers.
- Every value is finite and in `[0, 1]`.

The reference implementation:

```python
def validate_payload(payload: object) -> np.ndarray:
    if not isinstance(payload, dict):
        raise ApiError(422, "invalid_payload", "body must be a JSON object")
    features = payload.get("features")
    if not isinstance(features, list) or not features:
        raise ApiError(422, "invalid_payload", "features must be a non-empty list")
    if len(features) > MAX_BATCH:
        raise ApiError(422, "batch_too_large", f"at most {MAX_BATCH} rows per request")
    rows = []
    for row in features:
        if not isinstance(row, list) or len(row) != N_FEATURES:
            raise ApiError(422, "invalid_shape", f"each row must have {N_FEATURES} values")
        values = []
        for value in row:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ApiError(422, "invalid_type", "features must be numeric")
            if not math.isfinite(value) or value < 0.0 or value > 1.0:
                raise ApiError(422, "invalid_range", "features must be finite and in [0, 1]")
            values.append(float(value))
        rows.append(values)
    return np.asarray(rows, dtype=np.float64)
```

Four Python-specific traps:

| Trap | Example | Why it passes a naive check | Fix |
|---|---|---|---|
| `bool` is an `int` | `True` becomes `1` | `isinstance(True, int)` is true | Reject `bool` explicitly |
| `NaN` comparisons are false | `0 <= nan <= 1` is false, but `not (0 <= nan <= 1)` may be mishandled | The check must reject, not merely fail to accept | Call `math.isfinite` first |
| `Infinity` | `1e309` parses as `inf` | It is a float and may compare outside range | `math.isfinite` rejects it |
| JSON extensions | `NaN`, `Infinity`, `-Infinity` | Python's `json` accepts them by default | Treat parser acceptance as untrusted; validate values |

The last row is worth pausing on. RFC 8259 does not permit `NaN` or `Infinity` in JSON. Python's `json` module accepts them for compatibility. Relying on the parser to reject them is a portability bug: a stricter client or proxy may behave differently, and a looser one may pass them through. Validate the values regardless of what the parser allowed.

### Validation is not robustness

An input can satisfy every check and still be adversarial. LAB-11 demonstrates this: 64 values in `[0, 1]`, finite and correctly shaped, can be perturbed by ε = 0.10 in L∞ to change a prediction. LAB-14 rejects malformed inputs; it does not make the model robust.

Keep the two claims separate:

- **Validation** answers "is this a well-formed request for this contract?"
- **Robustness** answers "how does the model behave under an adversary within the allowed input domain?"

A service needs both. Confusing them produces statements like "we validate inputs, so evasion is handled," which LAB-11 refutes.

## 4. Rate limits and quotas

LAB-14 uses a fixed-window limiter keyed by role: 10 requests per 60 seconds. The 11th request returns 429.

```python
class RateLimiter:
    def __init__(self, limit=10, window=60.0):
        self.limit = limit
        self.window = window
        self.entries = {}

    def allow(self, key, now=None):
        current = time.monotonic() if now is None else now
        start, count = self.entries.get(key, (current, 0.0))
        if current - start >= self.window:
            start, count = current, 0
        if count >= self.limit:
            self.entries[key] = (start, count)
            return False
        self.entries[key] = (start, count + 1)
        return True
```

The test resets the limiter, then sends 11 requests. It records 10 allowed and 1 rejected. The reset exists so the test is deterministic; it is also a reminder that in-memory state is not durable.

| Limiter | Behavior | Trade-off |
|---|---|---|
| Fixed window | Simple, deterministic | Burst at a window boundary: up to 2× the limit around the reset |
| Sliding window | Smoother rate | More state and computation |
| Token bucket | Allows controlled bursts | Two parameters to tune; still needs shared state |
| Concurrency limit | Bounds in-flight work | Does not bound total volume |
| Quota | Bounds a longer period | Slow to stop a sudden burst |

LAB-14's limiter is in-process and keyed by role. Three consequences belong in the report:

1. A restart clears the counters.
2. Multiple workers do not share state, so the effective limit is per worker.
3. One client can exhaust the `client` role's budget for every other client with that role.

A production design keys by client, adds a global cap, and stores counters in a shared, low-latency store. It also decides what to do when the store is unavailable: fail closed (reject) or fail open (allow). For abuse prevention, failing closed for the affected route is usually safer, but it can turn a cache outage into an outage of the service. State the choice.

### 429 responses

A 429 should include a `Retry-After` header and a stable error code. Do not include the caller's remaining quota in a way that helps an attacker calibrate; a coarse retry time is enough.

## 5. Safe output

An error is a response like any other. It must be useful, consistent, and non-disclosing.

| Rule | Bad | Good |
|---|---|---|
| No credentials | Echo the `Authorization` header | `{"error": {"code": "unauthorized", "message": "invalid token"}}` |
| No payload echo | Return the offending row | A code and a generic message |
| No stack trace | Framework debug page | Log the trace server-side; return a request id |
| Stable code | Free-text messages only | `invalid_range`, `batch_too_large` |
| Request id | Nothing to correlate | `request_id` in the body and the log |
| Correct media type | HTML error page | `application/json` |
| No caching | Default cache headers | `Cache-Control: no-store` |
| No sniffing | Missing header | `X-Content-Type-Options: nosniff` |

LAB-14's `safe_error_body` case sends an invalid token and checks three things: status 401, the token marker is absent from the response, and the word `traceback` is absent. That is a narrow test. It does not prove every error path is safe; it proves this one is.

The service also logs only request metadata. In the reference run, 28 log records cover 18 test cases plus the 11-request rate-limit burst. No demo token appears in any line. That is a measured property of this run, not a guarantee for future code.

### Output as an information channel

| Output choice | Helps clients | Helps attackers | Mitigation |
|---|---|---|---|
| Stable error codes | Fix requests | Learn validation boundaries | Keep codes coarse where the boundary is sensitive |
| Model version | Debug deployments | Target a known weakness | Expose only where needed; protect admin detail |
| Prediction confidence | Rank results | Calibrate extraction and evasion | Return only what the product needs |
| Timing | Diagnose latency | Infer model or data properties | Add jitter or timeouts; monitor |
| Batch size accepted | Plan workloads | Maximize per-request work | Keep the cap modest and documented |

The product requirement decides. A confidence score may be essential for triage; a model version may be essential for support. The security requirement is to make the disclosure deliberate.

## 6. The 18 cases

| Case | Status | Control exercised |
|---|---:|---|
| `health_ok` | 200 | Public liveness |
| `missing_token` | 401 | Authentication |
| `invalid_token` | 401 | Authentication |
| `viewer_forbidden` | 403 | Scope on `/predict` |
| `valid_predict` | 200 | Happy path |
| `malformed_json` | 400 | Parsing |
| `wrong_content_type` | 415 | Media type |
| `wrong_length` | 422 | Feature shape |
| `out_of_range` | 422 | Range |
| `non_numeric` | 422 | Type |
| `non_finite` | 422 | Finiteness |
| `batch_too_large` | 422 | Batch cap |
| `oversized_body` | 413 | Body cap |
| `rate_limit` | 429 | Quota |
| `admin_stats` | 200 | Admin scope |
| `client_stats_forbidden` | 403 | Scope on `/stats` |
| `unknown_path` | 404 | Routing |
| `safe_error_body` | 401 | Output redaction |

A useful way to read the table: every row is a hypothesis about one control. The suite does not cover concurrent abuse, distributed rate limits, TLS, token expiry, or adversarial in-range inputs. Those are named exclusions, not silent gaps.

## 7. Trade-offs

| Control | Security benefit | Usability or performance cost |
|---|---|---|
| 8 KB body cap | Bounds parser memory | Rejects legitimate large batches |
| 32-row batch cap | Bounds per-request inference | Forces clients to paginate |
| 64-feature exact shape | Prevents shape confusion | Rejects compatible image sizes |
| Strict `[0, 1]` range | Keeps values in the training domain | Rejects valid alternative scalings |
| 10 requests per minute | Limits scraping | May throttle a legitimate integration |
| Generic errors | Reduces disclosure | Slower client debugging |
| Metadata-only logs | Protects credentials and privacy | Less detail for forensics |

A cap that is too small pushes users to bypass the API. A cap that is too large does not bound the resource. The right value comes from the workload contract and a load test, not from a copied constant.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Reading the body before checking its size | The framework reads first | Check `Content-Length` before `read` |
| Checking batch size after converting to an array | The conversion is convenient | Check the list length first |
| Using `isinstance(value, (int, float))` alone | It looks correct | Reject `bool`; check finiteness |
| Relying on JSON to reject `NaN` | Python accepts it | Validate values explicitly |
| Treating validation as robustness | Both are "input checks" | Keep the claims separate; test adversarial in-range inputs |
| Rate limiting by IP only | It is the easiest key | Add client or token identity; consider shared NAT |
| Returning the payload in an error | It helps debugging | Return a code and request id |
| Logging request bodies | It helps reproduction | Log metadata; redact or aggregate |
| A cap with no load test | The number looks reasonable | Test at and above the cap |
| Assuming the limiter is global | It works in one process | Use shared state or document the limit |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| 413 never fires | Size checked after reading | Move the check before `read` |
| 422 for an oversized batch | Batch check after array conversion or wrong status | Check the list length; return 422 as designed |
| Body cap rejects a 33-row batch | Compact JSON still exceeds 8 KB | Raise the cap or lower the batch cap deliberately |
| `NaN` reaches the model | Range check only | Add `math.isfinite` |
| Booleans accepted | `bool` is `int` | Reject `bool` before numeric checks |
| 500 on malformed input | Validation exception escapes | Convert to `ApiError(422, ...)` |
| Limiter never trips | Keyed per request or reset each call | Key by role or client; test 11 requests |
| Limit resets after restart | In-memory state | Persist counters or accept and document |
| Error response contains a path | Traceback serialized | Return a generic body; log the trace |
| Token appears in logs | Headers logged | Log role and metadata only |

## Check your understanding

1. Why must the body-size check run before `read`, not after parsing?
2. Give two reasons a validator that checks `0 <= x <= 1` can still accept a dangerous value.
3. Why does LAB-14 return 422 for an oversized batch but 413 for an oversized body?
4. Name three limitations of an in-process fixed-window rate limiter.
5. A request is well-formed, in range, and adversarial. Which control should catch it, and which module measures that control?
6. What should an error response contain, and what should it never contain?

Answers are discussed in the [answer key](quiz-answers.md) and the exercises.

## Summary

- Bounds are layered: body size, batch size, request rate, concurrency, and quota address different exhaustion paths.
- Check size before reading, batch size before allocation, and schema before inference.
- Python's `bool` and `NaN` behavior defeats naive type and range checks. Reject booleans and non-finite values explicitly.
- Validation is a contract check, not a robustness guarantee. LAB-11 measures the adversarial case.
- LAB-14's fixed-window limiter is deterministic and local. It is not shared across workers and does not survive a restart.
- Safe errors carry a request id, a stable code, and no token, payload, or traceback. Logs carry metadata only.
- LAB-14's 18 cases each test one control. The out-of-scope list is part of the result.

## Next

Continue to [Lesson 11.4 — Monitoring, drift, and attack indicators](lesson-4-monitoring-drift-and-attack-indicators.md), where the service's logs become evidence about behavior the preventive controls cannot classify.
