# Lesson 11.2 — Authentication and Authorization

<a id="m11-l2"></a>

**Module 11 · Lesson 2 of 6 · 1.5 hours · LO-22, LO-04**

## Scenario

The first version of the prediction API accepted any request. The team adds a token check and considers the problem solved. A partner integration then fails in a way nobody expected: the partner's analytics service holds a valid token, calls `GET /stats`, and receives a 401. The partner retries with the same token, then opens a ticket saying the credential is broken.

The credential is not broken. The caller is authenticated and not authorized. The API conflated two different decisions, and the error told the client to fix the wrong one.

This lesson separates the decisions, implements both, and tests the cases that distinguish them.

## Objectives

By the end of this lesson you will be able to:

1. Distinguish identification, authentication, and authorization, and map each to an HTTP failure.
2. Compare API keys, bearer tokens, OIDC-issued tokens, and mTLS by what they prove and how they fail.
3. Implement token authentication with constant-time comparison and scope-based authorization.
4. Design an authorization matrix for roles, endpoints, and objects, including tenant isolation.
5. Explain object-level authorization and why a valid token is not a permission.
6. Write negative tests for missing, malformed, invalid, expired, and under-scoped credentials.

## 1. Three decisions, not one

| Decision | Question | Typical evidence | Failure response |
|---|---|---|---|
| Identification | Who is claiming to call? | A subject identifier, client id, certificate name | 401 if no usable claim |
| Authentication | Can the claim be verified? | Token signature, key match, certificate chain | 401 |
| Authorization | May this subject perform this action on this object? | Scopes, roles, policy, ownership | 403, or 404 when object existence is sensitive |

A request can pass the first two and fail the third. That is normal, and it is not a credential problem. The response must say so.

### The 401/403 rule

- **401 Unauthorized** (the name is misleading): the request lacks valid authentication credentials. Include `WWW-Authenticate: Bearer` when the scheme is bearer.
- **403 Forbidden**: the server understood the request and the caller is authenticated, but the caller lacks permission.

LAB-14 tests both. A missing token, a malformed header, and an unknown token return 401. A viewer token calling `/predict` and a client token calling `/stats` return 403.

```text
POST /predict  no Authorization header        -> 401
POST /predict  Authorization: Token abc       -> 401 (wrong scheme)
POST /predict  Authorization: Bearer wrong    -> 401 (unknown token)
POST /predict  Bearer viewer-demo-token       -> 403 (authenticated, no predict scope)
POST /predict  Bearer client-demo-token       -> 200
GET  /stats    Bearer client-demo-token       -> 403 (no stats scope)
GET  /stats    Bearer admin-demo-token        -> 200
```

## 2. Credential types

| Credential | What it proves | Strengths | Weaknesses | Good use |
|---|---|---|---|---|
| API key | Possession of a secret string | Simple, easy to rotate per client | Long-lived, often over-scoped, leaks in URLs and logs | Server-to-server with tight scope and rotation |
| Bearer token (opaque) | Possession of a token the issuer recognizes | Revocable server-side, no client crypto | Anyone who holds it can use it | Session or service tokens behind an issuer |
| OIDC/JWT | A signed claim set from an identity provider | Standard claims, short lifetime, federation | Validation mistakes, algorithm confusion, revocation lag | User or workload identity |
| mTLS | Possession of a private key and a valid certificate | Strong mutual identity, no bearer secret in the request | Certificate lifecycle, termination complexity | Service mesh, high-assurance internal calls |
| Signed request | Possession of a key and the exact request bytes | Binds the credential to the request; replay-resistant with a nonce | More implementation work | High-value internal APIs |

None of these is universally better. The question is what failure you are defending against: leakage, replay, revocation, or impersonation.

### API keys

If you issue API keys:

- generate at least 128 bits of randomness;
- store a hash, not the key, and compare in constant time;
- scope each key to the minimum actions;
- never put a key in a URL, query string, or log;
- support rotation with an overlap window;
- revoke on offboarding, leak suspicion, or scope change.

A key in a repository is compromised even if the repository is private. History, forks, CI logs, and backups all retain it.

### OIDC and JWTs

A JWT is a container. It is not automatically trustworthy. Before accepting one, verify:

1. **Signature** with the issuer's current key, using an allowlisted algorithm.
2. **Issuer (`iss`)** equals the expected identity provider.
3. **Audience (`aud`)** includes this service.
4. **Expiry (`exp`)** and **not-before (`nbf`)** are valid with a small clock skew.
5. **Key id (`kid`)** resolves to a trusted key, not an arbitrary URL.
6. **Claims** used for authorization are present and intended for this use.

Common failures: accepting `alg: none`, letting the token choose the algorithm, trusting `kid` as a file path or URL, skipping audience checks, and treating a valid signature as proof of authorization. A signed token can be valid and still lack the scope for this endpoint.

### mTLS

Mutual TLS authenticates both ends with certificates. It is strong when the certificate lifecycle is managed: issuance, renewal, revocation, and the mapping from certificate identity to application identity. It does not solve authorization. A valid client certificate says who connected, not what the client may do.

## 3. LAB-14's implementation

LAB-14 uses three demo tokens with scopes:

```python
TOKENS = {
    "client": {"token": "client-demo-token", "scopes": {"predict"}},
    "viewer": {"token": "viewer-demo-token", "scopes": set()},
    "admin": {"token": "admin-demo-token", "scopes": {"predict", "stats"}},
}

def authorize(header_value: str | None, scope: str) -> str:
    if header_value is None:
        raise ApiError(401, "unauthorized", "missing bearer token")
    scheme, separator, token = header_value.partition(" ")
    if not separator or scheme.lower() != "bearer" or not token.strip():
        raise ApiError(401, "unauthorized", "malformed authorization header")
    candidate = token.strip().encode("utf-8")
    matched = None
    for role, meta in TOKENS.items():
        if hmac.compare_digest(candidate, meta["token"].encode("utf-8")):
            matched = role
    if matched is None:
        raise ApiError(401, "unauthorized", "invalid token")
    if scope not in TOKENS[matched]["scopes"]:
        raise ApiError(403, "forbidden", "insufficient scope")
    return matched
```

Four details matter:

| Detail | Why it matters |
|---|---|
| `partition(" ")` | Separates the scheme from the token; comparing the whole header fails every request |
| `scheme.lower() != "bearer"` | Accepts case variations of the scheme without accepting another scheme |
| `hmac.compare_digest` | Avoids a timing signal from comparing secrets with `==` |
| Scope check after identity | Keeps 401 and 403 distinct and returns the role for logging |

The loop does not break on a match, so the number of comparisons does not reveal which role matched. That is a small improvement, not a complete defense: token length, caching, and network timing still leak information. Constant-time comparison removes one channel, not all of them.

### The demo-token caveat

The tokens are constants in source so the lab is reproducible. In production this is a credential leak waiting for a repository clone. A real service reads credentials from a secret store, hashes them at rest, rotates them, and logs only the role or a token identifier — never the token.

## 4. Authorization models

| Model | Decision input | Strength | Weakness | Example |
|---|---|---|---|---|
| RBAC | Role assigned to subject | Simple to reason about | Role explosion; coarse | `admin`, `client`, `viewer` |
| ABAC | Attributes of subject, action, resource, environment | Fine-grained, context-aware | Policy complexity and testing | Allow if `tenant == resource.tenant` and `region == "eu"` |
| ReBAC | Relationships in a graph | Natural for sharing and hierarchies | Requires relationship data and consistency | Owner, editor, viewer of a document |
| Scope-based | Permissions carried by the token | Decentralized and simple for APIs | Coarse; scope sprawl | `predict`, `stats` |

LAB-14 uses scope-based authorization with roles as labels. Three scopes (`predict`, `stats`) are enough for the lab and too coarse for a real product. A production API often needs both scopes and object-level checks: `predict` says the caller may request predictions; ownership says whose prediction history they may read.

### The authorization matrix

Write the matrix before writing code.

| Endpoint | Anonymous | Viewer | Client | Admin | Object check |
|---|---|---|---|---|---|
| `GET /health` | allow | allow | allow | allow | none |
| `POST /predict` | 401 | 403 | allow | allow | batch belongs to caller's tenant |
| `GET /stats` | 401 | 403 | 403 | allow | aggregate only; no per-caller data |
| `GET /predictions/{id}` | 401 | 403 | owner only | allow | `prediction.tenant == token.tenant` |
| `POST /model/reload` | 401 | 403 | 403 | allow + re-auth | artifact signature verified |

The object-check column is where most real breaches happen. A route can be perfectly authenticated and still return another tenant's record because the handler looked up the id without checking ownership.

### Object-level authorization and IDOR

Insecure direct object reference (IDOR) occurs when an application exposes an internal identifier and authorizes the action but not the object. The fix is not to hide the identifier; it is to check the relationship on every access.

```python
def get_prediction(prediction_id: str, claims: dict) -> dict:
    record = store.fetch(prediction_id)
    if record is None or record["tenant"] != claims["tenant"]:
        raise ApiError(404, "not_found", "prediction not found")
    if claims["role"] not in {"owner", "admin"} and record["owner"] != claims["sub"]:
        raise ApiError(403, "forbidden", "not the owner")
    return record
```

Returning 404 for a cross-tenant miss avoids confirming that the identifier exists. Returning 403 is also defensible when existence is not sensitive. Choose one policy and apply it consistently; the inconsistency is what leaks.

### Tenant isolation

Tenant isolation is more than a filter in one handler.

| Layer | Isolation question |
|---|---|
| Identity | Is the tenant derived from a verified token claim, not from the request body? |
| Data | Does every query filter by tenant, including joins and counts? |
| Cache | Is the tenant part of every cache key? |
| Logs | Are tenant identifiers access-controlled and retained appropriately? |
| Artifacts | Can one tenant influence the model or configuration used by another? |
| Rate limits | Is one tenant able to exhaust another tenant's quota? |

A tenant id accepted from the request body is an authorization bypass waiting to happen. Derive it from the authenticated context.

## 5. Threats and controls

| Threat | Mechanism | Control | Test |
|---|---|---|---|
| Credential stuffing | Reuse leaked passwords or keys | Rate limits, anomaly detection, rotation, MFA at the IdP | Many failed auth attempts trigger 429 or lockout |
| Token theft | Read a token from logs, URLs, or storage | Never log tokens; TLS; short lifetimes; scope limits | Log scan finds no token values |
| Replay | Resend a captured request | Short-lived tokens, nonces, mTLS, request signing | Old token rejected after expiry |
| Privilege escalation | Use a low-privilege token on a high-privilege route | Scope checks on every route | Viewer receives 403 on `/predict` and `/stats` |
| IDOR / BOLA | Change an object id in the request | Object-level authorization on every access | Cross-tenant read returns 404 or 403 |
| Confused deputy | Make the service act with its own credentials | Least privilege; do not pass caller input into privileged calls | Service cannot write to the registry |
| Scope creep | Grant broad scopes for convenience | Minimum scopes; review on issuance | Token introspection shows only required scopes |
| Cross-tenant leakage | Shared cache or unfiltered query | Tenant in key and query; tests with two tenants | Tenant A cannot see Tenant B's data |

OWASP API Security Top 10 places broken object-level authorization at the top of the list for a reason. It survives authentication, it looks like a normal request, and it is easy to miss in a code review that focuses on the login flow.

## 6. Negative tests

A control is not implemented until it fails correctly.

| Case | Expected | What it proves |
|---|---|---|
| No `Authorization` header | 401 + `WWW-Authenticate: Bearer` | Missing credentials are rejected |
| `Authorization: Token abc` | 401 | Scheme is enforced |
| `Authorization: Bearer` (empty) | 401 | Malformed credentials are rejected |
| Unknown token | 401 | Token lookup fails closed |
| Valid token, wrong scope | 403 | Authorization is separate from authentication |
| Expired token | 401 | Lifetime is enforced |
| Wrong audience | 401 | Token is not accepted by the wrong service |
| `alg: none` token | 401 | Algorithm allowlist is enforced |
| Cross-tenant object id | 404 or 403 | Object-level authorization runs |
| Token in log after failure | absent | Redaction works on the error path too |

LAB-14 covers the first five directly. The rest belong in a production suite; Lesson 6 and the exercises ask you to design them.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Comparing the full header to the token | The header looks like the credential | Parse the scheme and token separately |
| Using `==` for token comparison | It is the obvious operator | Use `hmac.compare_digest` |
| Returning 401 for missing scope | One auth error path | Return 403 after successful authentication |
| Trusting a JWT because it decodes | Decoding is not verification | Verify signature, issuer, audience, expiry, algorithm |
| Reading the tenant from the body | The client sends it | Derive tenant from verified claims |
| Checking the role but not the object | The route is protected | Add an ownership or tenant check |
| Logging the token for debugging | Failures are hard to trace | Log a token id or role, never the token |
| Long-lived, broadly scoped keys | Easier integration | Short lifetimes, minimum scopes, rotation |
| Assuming mTLS replaces authorization | It authenticates the connection | Add per-action and per-object policy |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| All requests 401 | Header parsing or scheme case | Split on the first space; compare `scheme.lower()` |
| A valid token is rejected after restart | Tokens generated in memory | Load stable credentials from a secret store |
| Viewer can call `/predict` | Scope check missing on the route | Require `predict` in the handler |
| 403 for an admin token | Scope name mismatch | Use the same scope constants in issuance and checks |
| Cross-tenant read succeeds | Object check missing | Filter by tenant in the query and verify before return |
| Token appears in logs | Header or body logged | Log metadata only; add a log-redaction test |
| Expired token still works | `exp` not checked | Validate lifetime with a small clock skew |
| JWT accepted from another issuer | `iss` or `aud` not checked | Enforce both against configuration |

## Check your understanding

1. A caller presents a valid token without the `stats` scope. Which status code is correct, and what does the other status code imply?
2. Why is `hmac.compare_digest` preferred over `==` for token comparison? What does it not protect against?
3. Name four claims or headers a JWT validator must check besides the signature.
4. A route checks that the caller is authenticated but looks up a record by id without checking ownership. Which risk class is this, and what is the fix?
5. Why should a tenant identifier come from the token rather than the request body?
6. Design two negative tests for an authorization matrix that LAB-14 does not run.

Answers are discussed in the [answer key](quiz-answers.md) and the exercises.

## Summary

- Identification, authentication, and authorization are different decisions. 401 means the credential is missing or invalid; 403 means it is valid but insufficient.
- API keys, opaque bearer tokens, OIDC/JWT, mTLS, and signed requests prove different things and fail differently.
- LAB-14 authenticates with `hmac.compare_digest`, enforces `predict` and `stats` scopes, and tests 401 and 403 separately.
- Constant-time comparison closes a timing channel; it does not make demo tokens safe or replace rotation and storage controls.
- Authorization needs a matrix: subject, action, endpoint, and object. Object-level and tenant checks are where real APIs fail.
- Every control needs a negative test, including expiry, audience, algorithm, cross-tenant access, and log redaction on the error path.

## Next

Continue to [Lesson 11.3 — Request bounds, validation, and safe output](lesson-3-request-bounds-validation-and-safe-output.md), where authenticated requests are bounded and checked before they reach the model.
