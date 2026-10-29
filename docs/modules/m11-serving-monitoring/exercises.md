---
title: Module 11 Exercises
---

# Module 11 Exercises

**Four exercises · about 45 minutes · one scenario**

All exercises use the same fictional service: **Meridian Assist**, a partner-facing prediction API built on the LAB-14 service and monitored with the LAB-15 design. The data and numbers are synthetic. Do not point any test at a real service.

---

## Exercise 1 — Status codes and control order (10 minutes)

Meridian Assist exposes `GET /health`, `POST /predict`, and `GET /stats`. It uses the LAB-14 configuration: 8 KB body cap, 32-row batch cap, 64 features per row, 10 requests per 60 seconds per role, bearer tokens with scopes.

For each request, give the status code and the control that decides it:

| # | Request | Status |
|---|---|---:|
| 1 | `POST /predict` with no `Authorization` header, valid 1-row body | ? |
| 2 | `POST /predict` with a viewer token and a valid body | ? |
| 3 | `POST /predict` with a valid client token and a 9 KB body | ? |
| 4 | `POST /predict` with no token and a 9 KB body | ? |
| 5 | `POST /predict` with a client token and 33 compact rows | ? |
| 6 | `POST /predict` with a client token and one `NaN` feature | ? |
| 7 | `GET /stats` with a client token | ? |
| 8 | The 11th `POST /predict` from one role in a fresh 60-second window | ? |
| 9 | `GET /model` (no such route) | ? |

Then answer:

1. Which two cases prove that authentication and authorization are separate decisions?
2. Which case proves that the body-size check runs before authentication?
3. Name two residual risks that these statuses do not address.
4. If you could remove only one control last, which would it be, and why?

---

## Exercise 2 — Authorization matrix and object-level checks (10 minutes)

Meridian Assist adds a prediction-history endpoint, `GET /predictions/{id}`, and a model-reload endpoint, `POST /model/reload`. Each prediction belongs to exactly one tenant. Tokens carry `sub`, `tenant`, `role`, and scopes.

Roles:

- **viewer** — can see liveness only;
- **client** — can predict and read its own tenant's predictions;
- **auditor** — can read aggregate statistics, no predictions;
- **admin** — can do everything, and must re-authenticate for model reload.

1. Complete the matrix with `allow`, `401`, `403`, or `404`:

| Endpoint | Anonymous | Viewer | Client | Auditor | Admin |
|---|---|---|---|---|---|
| `GET /health` | ? | ? | ? | ? | ? |
| `POST /predict` | ? | ? | ? | ? | ? |
| `GET /predictions/{id}` | ? | ? | ? | ? | ? |
| `GET /stats` | ? | ? | ? | ? | ? |
| `POST /model/reload` | ? | ? | ? | ? | ? |

2. State the object-level rule for `GET /predictions/{id}` in one sentence.
3. A client sends the id of another tenant's prediction. What do you return, and why?
4. Design two negative tests: one for the matrix and one for object-level authorization.
5. Why must the tenant come from the token rather than a `tenant` field in the request body?

---

## Exercise 3 — Triage, rollback, and incident response (15 minutes)

The monitor uses the LAB-15 thresholds: input shift 0.1529 (high), mean confidence 0.8232 (low), shadow disagreement 0.0823 (high), client concentration 0.60 (high), throughput 5.0 req/s (high).

Four blocks of 100-request windows produce:

| Windows | Signals above threshold | Mean confidence | Shadow disagreement | Concentration | Throughput |
|---|---|---|---:|---:|---:|---:|
| 40–45 | input shift | 0.86 | 0.03 | 0.25 | 1.4 |
| 46–51 | input shift, low confidence, shadow disagreement | 0.69 | 0.21 | 0.30 | 1.7 |
| 52–57 | client concentration, throughput | 0.89 | 0.04 | 0.92 | 8.5 |
| 58–60 | none | 0.90 | 0.02 | 0.31 | 1.5 |

1. Classify each episode and assign severity using the LAB-15 triage rule.
2. How many alerting windows, episodes, and confirmed incidents are there?
3. Which episode is `INC-001`, and what is the first containment action?
4. Rollback is tested on a captured attack batch. Current ASR is 0.41; previous checkpoint ASR is 0.38. The criterion is `previous < 0.5 * current`. Compute the threshold, decide whether rollback is restored, and justify the decision.
5. Edge squeezing reduces ASR from 0.41 to 0.24 and clean accuracy from 0.9500 to 0.9300. Compute the absolute ASR reduction and the clean-accuracy cost, and state why squeezing is temporary.
6. Recovery windows 58–60 show no alerts. What else must be true before closing the incident?
7. Write a three-line incident timeline with roles and time bounds for detection, containment, and rollback decision.

---

## Exercise 4 — Configuration and secrets review (10 minutes)

A deployment proposal contains:

```yaml
bind: 0.0.0.0
debug: true
model_path: ./models/latest.pkl
auth_token: client-demo-token
rate_limit_store: memory
cors_origins: ["*"]
tls: false
container_user: root
egress: allow-all
log_request_bodies: true
```

1. Identify at least eight unsafe settings and the risk each creates.
2. Prioritize the five you would fix first. Justify the order by impact and ease.
3. Design one kill-switch test and state the expected result.
4. State a safe-failure policy for a secret-store outage and for an authorization-service timeout.
5. Rewrite the following claim as a scoped assurance statement: "The service is production-ready because it binds to 0.0.0.0, uses a token, and has a rate limiter."

---

## Self-assessment

| Criterion | Check |
|---|---|
| Status codes distinguish 401, 403, 413, 422, and 429 correctly | [ ] |
| The authorization matrix includes object-level and tenant rules | [ ] |
| Triage separates drift, evasion, and abuse by signal family | [ ] |
| Rollback is evaluated with a pre-defined criterion, not assumed | [ ] |
| The mitigation's utility cost and residual risk are stated | [ ] |
| The configuration review prioritizes secrets, exposure, and privilege | [ ] |
| The assurance statement is scoped and names exclusions | [ ] |

Worked answers: [exercise-solutions.md](exercise-solutions.md).
