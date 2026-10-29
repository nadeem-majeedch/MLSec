# Knowledge Check Answers — QZ-11

**Module 11 · 10 items · 14 points**

## 1. (1 point) — C

A valid token without the required scope is authenticated but not authorized, so the response is **403 Forbidden**. A 401 would tell the client the credential is missing or invalid, and retrying authentication cannot fix a permission problem.

## 2. (2 points)

The request should receive **413 Payload Too Large**.

The size check runs first so the service rejects the body before reading it into memory or parsing it. That protects the parser, the request buffer, and worker capacity from unauthenticated traffic. LAB-14 encodes this order: an oversized body with a valid token returns 413, not 401, and the same is true without a token.

If authentication ran first, the service would do credential work before rejecting the body, and a naive implementation might read the body before or during authentication. The request would likely return 401, which hides the size failure and spends work on a request that cannot be accepted. The size bound would no longer protect the earliest stage of the request path.

## 3. (2 points)

Two acceptable answers:

- **`True`**: Python treats `bool` as a subclass of `int`, and `True == 1`, so `True < 0` and `True > 1` are both false. Reject it with an explicit `isinstance(value, bool)` check before numeric checks.
- **`NaN`**: both `nan < 0` and `nan > 1` are false, so a validator that rejects only on those comparisons lets it through. Reject it with `math.isfinite(value)` before the range check.

A third acceptable answer is a numeric string such as `"0.5"` if the validator's "numeric" check uses a permissive conversion; reject it by requiring `int` or `float` and not `bool`. `Infinity` is caught by `x > 1`, so it is not a correct answer for this validator.

## 4. (2 points)

With a limit of 10 in a fresh window:

- Requests 1–10 are **allowed** (200).
- Requests 11 and 12 receive **429**.
- Allowed: **10**; rejected: **2**.

Two limitations (any two):

- The state is in-process, so multiple workers do not share counters and the effective limit is per worker.
- A restart clears the counters.
- The limiter is keyed by role, so one client can exhaust the budget for every other client with that role.
- A fixed window allows a burst of up to twice the limit around the boundary.
- It does not provide a longer-horizon quota.

## 5. (1 point) — C

The **query burst** produces `client_concentration` and `throughput` alerts only. It is triaged as medium-severity client abuse or scraping, not as model compromise.

## 6. (1 point) — C

Thresholds are calibrated on the **quiet calibration period only** (12 windows in the reference run). Calibrating on monitored traffic would absorb the attack or drift into the reference distribution.

## 7. (2 points)

The criterion is:

\[
0.5 \times 0.3507 = 0.17535
\]

The previous checkpoint's attack success is **0.3299**, which is **not** below 0.17535. Therefore `restored = false`, and LAB-15 **rejects the rollback**.

The previous checkpoint is only slightly better on this batch, and both checkpoints share the same linear weakness. Rolling back changes the version label without materially changing the security property.

Rollback would be valid if, on the same base set and attack budget, the previous checkpoint's attack success fell below the pre-defined criterion; the old artifact's hash and signature verified; its input/output contracts remained compatible; and it did not reintroduce a known vulnerability. The decision and evidence must be recorded either way.

## 8. (1 point)

Any one of:

- An adaptive attacker can approximate the quantizer or use a backpropagation-friendly approximation, so the measured reduction is not a guarantee (LAB-11 demonstrates this pattern).
- It costs clean accuracy, from 0.9600 to 0.9433 on this batch, so it trades utility for a temporary gain.
- The result is measured on one captured batch, one attack (FGSM at ε = 0.10), and one model; it does not establish robustness at other budgets or against other attacks.
- It is preprocessing, not eradication; the underlying model weakness remains.

## 9. (1 point)

Any three:

- source code or version control;
- container images or build artifacts;
- logs, error messages, or crash dumps;
- URLs or query strings;
- command-line arguments or process listings;
- client-side applications;
- test fixtures or public repositories.

Production mechanism: a secret manager that injects a short-lived credential at runtime (or an identity provider issuing short-lived tokens), with rotation, revocation, and access auditing. Environment variables are better than source code but are not a complete answer on their own.

## 10. (1 point)

A scoped statement such as:

> The loopback-bound service enforces bearer authentication with scopes, an 8 KB body cap, a 32-row batch cap, 64 finite features in `[0, 1]`, 10 requests per 60 seconds per role, generic errors, and metadata-only logging. All 18 scripted cases pass, and no demo token appears in 28 log records. These results cover the named cases on a local deployment; they do not establish TLS configuration, identity-provider integration, distributed rate limiting, object-level authorization, or robustness to adversarial in-range inputs, which remain out of scope or unverified.

The rewrite must keep the measured facts, name the deployment context, and state at least one exclusion. "The service is secure" is not supported by the evidence.

---

**Scoring:** 14 points total. 12–14 strong; 9–11 review Lessons 1–3 and the rollback section of Lesson 5; below 9 reread the module and rerun LAB-14 and LAB-15 before attempting the exercises.
