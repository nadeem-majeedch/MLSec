# Module 11 Exercise Solutions

**Worked answers for the four exercises · one scenario: Meridian Assist**

These are reference answers, not the only defensible ones. Where a policy choice exists, the reasoning matters more than the exact label.

---

## Exercise 1 — Status codes and control order

| # | Request | Status | Deciding control |
|---|---|---:|---|
| 1 | No `Authorization`, valid body | **401** | Authentication |
| 2 | Viewer token, valid body | **403** | Scope on `/predict` |
| 3 | Client token, 9 KB body | **413** | Body cap |
| 4 | No token, 9 KB body | **413** | Body cap (runs first) |
| 5 | Client token, 33 compact rows | **422** | Batch cap |
| 6 | Client token, `NaN` feature | **422** | Finiteness check |
| 7 | Client token on `/stats` | **403** | Scope on `/stats` |
| 8 | 11th request in a fresh window | **429** | Rate limit |
| 9 | Unknown route | **404** | Routing |

1. **Cases 1 and 2** (or 1 and 7) show the split: no credential is 401; a valid credential without permission is 403. Case 2 proves the caller is known and still denied.
2. **Case 4** proves the size check precedes authentication: an unauthenticated oversized body receives 413, not 401.
3. Any two: demo tokens are static and shared; the limiter is in-process and per role; there is no TLS; there is no object-level authorization; validation does not stop adversarial in-range inputs; tokens do not expire.
4. A defensible answer is **authentication**. Authorization, per-role rate limits, audit identity, and tenant checks all depend on knowing who is calling. Removing size or schema validation still leaves a protected identity boundary; removing authentication makes every caller anonymous and collapses the rest of the policy. Another defensible answer is schema validation, if the argument is that the model must never see out-of-contract values. State the reasoning.

---

## Exercise 2 — Authorization matrix

| Endpoint | Anonymous | Viewer | Client | Auditor | Admin |
|---|---|---|---|---|---|
| `GET /health` | allow | allow | allow | allow | allow |
| `POST /predict` | 401 | 403 | allow | 403 | allow |
| `GET /predictions/{id}` | 401 | 403 | allow if own tenant | 403 | allow |
| `GET /stats` | 401 | 403 | 403 | allow | allow |
| `POST /model/reload` | 401 | 403 | 403 | 403 | allow + re-auth |

1. **Object-level rule:** allow the read only when the prediction's `tenant` equals the token's verified `tenant` claim and the role permits prediction access; admins bypass the tenant check, and no other role does.
2. **Cross-tenant request:** return **404** under a policy that does not confirm the existence of another tenant's records. A 403 is also defensible if object existence is not sensitive, but the same policy should apply everywhere.
3. **Negative tests (any two):**
   - A viewer token calls `POST /predict`; expect 403, not 401.
   - A client token requests a prediction id belonging to another tenant; expect 404 (or 403 under the chosen policy).
   - An expired token calls `/health` or `/predict`; expect 401 on the protected route.
   - An auditor calls `GET /predictions/{id}`; expect 403.
   - A client calls `/model/reload`; expect 403, and an admin without re-authentication expects a step-up challenge.
4. **Tenant from the token:** the body is attacker-controlled. A client could send another tenant's id and, if the server trusted it, read or write across tenants. The token claim is issued and signed by the identity provider; the service verifies it and derives the tenant from that verified context.

---

## Exercise 3 — Triage, rollback, and incident response

1. **Classifications:**
   - Windows 40–45: one content signal (input shift) → **low**, distribution drift under review.
   - Windows 46–51: three content signals → **high**, probable evasion or model-targeted abuse.
   - Windows 52–57: volume signals only → **medium**, client abuse or scraping.
   - Windows 58–60: no signals → none.
2. **Alerting windows:** 6 + 6 + 6 = **18**. **Episodes:** **3**. **Confirmed incidents:** **1** (the high-severity episode).
3. **INC-001** is windows 46–51. The first containment action is to enable edge input squeezing as a temporary brake and keep the existing rate limits, because the attack is content-targeted and distributed. Preserve logs, assign an incident commander, and test the rollback hypothesis before changing the model version.
4. **Rollback threshold:**

\[
0.5 \times 0.41 = 0.205
\]

The previous checkpoint's ASR is **0.38**, which is **not** below 0.205. Therefore `restored = false`, and **rollback is rejected**. Both checkpoints share the same weakness; the small difference does not meet the pre-defined criterion. Rollback would be valid only if the previous checkpoint materially reduced ASR on the same base set and budget, its artifact verified, and it did not reintroduce another vulnerability.
5. **Mitigation numbers:**
   - ASR reduction: \(0.41 - 0.24 = 0.17\), or **17 percentage points**.
   - Clean-accuracy cost: \(0.95 - 0.93 = 0.02\), or **2 percentage points**.
   - Squeezing is temporary because an adaptive attacker can approximate the quantizer, the underlying model weakness remains, and the result is measured on one captured batch and one attack family. It is a brake, not a fix.
6. Before closing: confirm the attack traffic has stopped, remove the temporary squeezing control, verify clean windows remain inside the calibrated band, identify or explicitly mark the root cause, assign corrective actions with owners and dates, preserve and restrict evidence, and record residual risk with an owner. Three quiet windows alone are not enough.
7. **Timeline example:**

| Time | Role | Action |
|---|---|---|
| T+0 | On-call engineer | Detector fires on windows 46–51; acknowledge within 15 minutes |
| T+15 min | Incident commander | Open INC-001 as high severity; assign containment and evidence owners |
| T+1 h | Platform on-call | Enable edge squeezing; preserve logs; confirm rate limits unchanged |
| T+2 h | ML owner + commander | Replay captured batch: current 0.41, previous 0.38; reject rollback and record the decision |
| T+24 h | ML owner | Verify recovery after removing squeezing; draft corrective actions |
| T+5 days | Commander | Postmortem with owners and due dates |

---

## Exercise 4 — Configuration and secrets review

1. **Unsafe settings:**

| Setting | Risk |
|---|---|
| `bind: 0.0.0.0` | Exposes the service to every reachable network |
| `debug: true` | Tracebacks, internals, and debug consoles |
| `model_path: ./models/latest.pkl` | Unverified artifact and unsafe pickle load; substitution |
| `auth_token: client-demo-token` | Static credential in configuration; shared and leakable |
| `rate_limit_store: memory` | Limits reset on restart and are per worker |
| `cors_origins: ["*"]` | Any browser origin can call the API |
| `tls: false` | Credentials and predictions travel in clear text |
| `container_user: root` | A process flaw has root-level impact |
| `egress: allow-all` | Exfiltration and metadata-service access |
| `log_request_bodies: true` | Credentials and personal data in logs |

2. **Priority order (one defensible answer):**
   1. Remove the static token; inject a short-lived credential from a secret manager.
   2. Turn off debug and request-body logging; return structured, generic errors.
   3. Restrict the bind address and enable TLS at the edge.
   4. Pin a verified model artifact and use a safe format or sandboxed conversion.
   5. Run as non-root with an egress allowlist and a read-only filesystem.

   The order fixes credential exposure and data leakage first, then network exposure, then the artifact execution path, then host privilege. `cors: "*"` and the in-memory limiter follow immediately after.
3. **Kill-switch test:** invoke the documented switch that disables `/predict`, then send a valid request with a valid token. Expect the defined maintenance response (for example, 503 with a stable code) and `/health` still returning 200. Restore the switch and confirm predictions resume. Record who invoked it, when, and why.
4. **Safe failure:**
   - Secret-store outage: refuse to start or return 503; never fall back to a default or demo token.
   - Authorization-service timeout: deny the request (fail closed), return a generic error, and alert. If the product requires a degraded mode, document it, scope it to a named route, and get approval.
5. **Scoped statement:**

> The proposed deployment uses a static demo token, binds to all interfaces, disables TLS, loads `latest.pkl`, runs as root with unrestricted egress, and keeps rate-limit state in memory. Those choices are not production-ready. On a loopback-only deployment with the LAB-14 configuration, 18 scripted cases pass and no token appears in 28 log records; TLS, identity-provider integration, distributed rate limiting, object-level authorization, verified model loading, and adversarial in-range robustness remain unverified.

The rewrite must not claim production readiness. It should name the measured cases and the exclusions.

---

## Scoring guide

| Exercise | Points | Full credit |
|---|---:|---|
| 1 | 5 | All nine statuses correct; order and separation explained |
| 2 | 6 | Matrix correct; object and tenant rules explicit; two tests |
| 3 | 7 | Triage correct; 18/3/1 counts; rollback math and decision; mitigation numbers |
| 4 | 6 | At least eight issues; prioritized five; tested kill switch; safe failure; scoped statement |

Total: 24 points. A score below 18 suggests rereading Lessons 2–5 and rerunning the labs before the capstone.
