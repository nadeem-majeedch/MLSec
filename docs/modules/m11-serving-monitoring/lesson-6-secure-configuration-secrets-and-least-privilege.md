# Lesson 11.6 — Secure Configuration, Secrets, and Least Privilege

<a id="m11-l6"></a>

**Module 11 · Lesson 6 of 6 · 1 hour · LO-22, LO-04**

## Scenario

The service passes its tests. It is about to move from a laptop to a shared environment, and someone opens the configuration file:

```yaml
bind: 0.0.0.0
debug: true
model_path: /srv/models/latest.pkl
token: client-demo-token
rate_limit_state: memory
cors: "*"
container_user: root
network_egress: unrestricted
```

Every line is convenient. Every line is a decision that weakens a control LAB-14 established. The tests will still pass after the move, because the tests run against the same permissive configuration.

This lesson treats configuration as part of the attack surface, secrets as lifecycle objects, and least privilege as the default for the process that runs the model.

## Objectives

By the end of this lesson you will be able to:

1. Identify unsafe defaults in serving configuration and replace them with explicit, tested values.
2. Manage secrets through generation, storage, injection, rotation, and revocation.
3. Apply least privilege to the service account, filesystem, network, and artifact access.
4. Design and test kill switches and safe-failure behavior.
5. Distinguish a lab configuration from a production configuration and state the residual risk of each.
6. Map serving controls to governance functions and write a scoped assurance statement.

## 1. Configuration is a control surface

| Setting | Unsafe default | Risk | Safer choice |
|---|---|---|---|
| Bind address | `0.0.0.0` | Exposes the service to every reachable network | `127.0.0.1` or a private interface with policy |
| Debug mode | `true` | Tracebacks, internals, interactive consoles | `false` everywhere; structured errors |
| Model path | Caller-influenced or `latest` | Loads an unverified or substituted artifact | Fixed, verified path pinned by hash |
| Model format | Pickle or joblib | Code execution at load | Safe format or sandboxed conversion (M10) |
| CORS | `*` | Any origin can call from a browser | Explicit allowlist |
| TLS | Terminated nowhere | Credentials and data in clear text | TLS at the edge with modern settings |
| Timeouts | None | Slow requests exhaust workers | Read, write, and inference timeouts |
| Body cap | Framework default or none | Memory exhaustion | Explicit cap enforced before parsing |
| Token source | Source code or image | Credential leak | Secret manager injection |
| Rate-limit state | In-memory | Limits reset and do not share | Shared store with a defined failure mode |
| Container user | `root` | A process flaw becomes host-adjacent privilege | Non-root, read-only filesystem |
| Egress | Unrestricted | Data exfiltration, metadata access | Allowlist of required destinations |

A configuration review is a security review. It should be versioned, diffed, and tested like code.

### Environment drift

The same service behaves differently in development, staging, and production. Drift is dangerous because a control tested in one environment may be absent in another.

| Control | Test it in |
|---|---|
| Bind address | Every environment |
| Auth configuration | Staging and production, with non-production credentials |
| Body and batch caps | Every environment |
| Rate limits | Staging with production-like state |
| Secret injection | Staging and production |
| Egress policy | Staging and production |
| Kill switches | Staging, before an incident |

If a control is disabled in development for convenience, the test that proves it must run in an environment where it is enabled.

## 2. Secrets

A secret is any value whose disclosure grants access: tokens, API keys, signing keys, database passwords, private keys, and sometimes model decryption keys.

### The lifecycle

| Stage | Practice |
|---|---|
| Generate | Use a cryptographically secure generator with sufficient entropy |
| Store | Secret manager or encrypted store, access-controlled and audited |
| Inject | At runtime, into the process, over an authenticated channel |
| Use | In memory only; never write to logs, errors, or temporary files |
| Rotate | On a schedule and on suspicion; support overlap for clients |
| Revoke | Immediately on compromise, offboarding, or scope change |
| Audit | Record issuance, use, rotation, and access |

### Where secrets must not appear

| Location | Why it fails |
|---|---|
| Source code | History, forks, and backups retain it |
| Container image | Layers are pullable by anyone with registry access |
| Environment variable in a shared shell | Visible to other processes and crash reports |
| Command-line argument | Visible in process listings |
| Log line or error message | Indexed, copied, and retained |
| URL or query string | Logged by proxies, browsers, and servers |
| Client-side application | Extractable by the user |
| Test fixture in a public repository | Becomes a real credential if reused |

LAB-14 uses demo tokens as constants because the lab must be reproducible. That is a lab-only choice. The lesson is not "hard-code tokens"; it is "know exactly why this is acceptable here and unacceptable in production."

Environment variables are a common injection mechanism and a limited one. They are better than source code, but they can leak through process inspection, crash dumps, child processes, and misconfigured diagnostics. A secret manager that injects a short-lived credential is stronger.

### Rotation without an outage

A rotation plan needs two valid credentials during the overlap:

1. Issue the new credential.
2. Deploy it to consumers.
3. Verify use.
4. Revoke the old credential.
5. Confirm the old credential fails.

Without step 5, rotation is a hope. Add a negative test: the old token must be rejected.

## 3. Least privilege

The inference process should be able to do its job and very little else.

| Resource | Minimum access | Why |
|---|---|---|
| Model artifact | Read-only, specific path | Prevents substitution and modification |
| Model registry | No write; read only at deploy time | A compromised service cannot publish a model |
| Training data | None at serving time | Serving does not need it |
| Logs | Append to its own stream | Cannot read or alter other logs |
| Secret store | Read only its own secrets | Limits blast radius |
| Network | Named destinations only | Prevents exfiltration and lateral movement |
| Cloud metadata | Blocked | Prevents credential theft from the metadata service |
| Filesystem | Read-only except a small temp area | Limits persistence and tampering |
| Container | Non-root, dropped capabilities | Limits host impact |

### The confused deputy, again

If the service holds a database credential, an attacker who can influence a query may use the service as a deputy. The fix is not only validation; it is scoping the credential to the operations the service performs. A prediction service usually needs read access to a feature table, not write access to the customer database.

### Network policy

| Direction | Policy | Evidence |
|---|---|---|
| Ingress | Only the edge or named clients | Network policy and bind address |
| Egress | Only required dependencies | Allowlist and egress logs |
| Metadata | Blocked | Deny rule and test |
| Admin | Separate path, separate identity | Admin authentication logs |
| Model registry | Read-only at deploy, none at runtime | Registry policy |

LAB-14 binds to loopback, which is a network control. It does not implement TLS, egress policy, or a container sandbox; those are named as out of scope. The production checklist replaces each.

## 4. Kill switches and safe failure

A kill switch is a control you can invoke quickly when a service is causing harm.

| Switch | Effect | Who may invoke | Test |
|---|---|---|---|
| Disable `/predict` | Stops predictions, keeps `/health` | On-call plus incident commander | Endpoint returns a defined maintenance response |
| Revoke a token | Stops one client | Security on-call | Old token returns 401 |
| Set rate limit to zero | Stops new work | Platform on-call | 429 for all callers |
| Disable a model version | Routes to a fallback or stops | ML owner | Version no longer served |
| Turn off a feature | Removes a risky output field | Product owner | Field absent from responses |
| Enable safe mode | Returns abstention instead of prediction | On-call | Response code and body defined |

A kill switch that has never been tested is a hypothesis. Test it in staging, record the result, and define who can invoke it without a second approval.

### Safe failure

| Failure | Safe behavior | Unsafe behavior |
|---|---|---|
| Secret store unavailable | Reject requests with 503; do not use a fallback secret | Start with a default token |
| Authorization service timeout | Deny the request | Allow because the check failed |
| Model file missing or hash mismatch | Refuse to start or serve | Load the nearest file |
| Rate-limit store unavailable | Fail closed for the protected route or degrade explicitly | Ignore limits |
| Upstream feature missing | Abstain or return a defined degraded response | Predict on zeros silently |
| Log write failure | Continue serving, buffer, and alert; do not log to an unsafe fallback | Write payloads to a world-readable file |

Fail-closed is the default for authentication and authorization. Availability-critical systems sometimes choose a documented degraded mode, but that choice must be explicit, tested, and approved. "It kept working" is not the same as "it failed safely."

## 5. Lab versus production

| Control | LAB-14 | Production replacement |
|---|---|---|
| Bind | Loopback only | Private interface plus network policy |
| TLS | Not implemented | Terminated at the edge, modern configuration |
| Tokens | Constants in source | Secret manager, hashed at rest, rotated |
| Identity provider | None | OIDC or mTLS with managed keys |
| Rate limit | In-process, per role | Shared store, per client, with a failure policy |
| Validation | 8 KB, 32 rows, 64 features | Workload-specific caps and load tests |
| Model artifact | Trained in process | Verified artifact from a registry (M10) |
| Logs | Local JSONL | Append-only pipeline with access control and retention |
| Container | Process on the host | Non-root, read-only, minimal image, dropped capabilities |
| Monitoring | LAB-15 statistics | Metrics, traces, alert routing, on-call |

The lab is not a miniature production system. It is a controlled environment where each control is visible and testable. The production table is the bridge between the two.

### Configuration review checklist

- [ ] Bind address is explicit and matches the network policy.
- [ ] Debug mode is off; errors are structured and generic.
- [ ] TLS is terminated with a current configuration.
- [ ] CORS is an allowlist, not `*`.
- [ ] Body, batch, header, and connection limits are set at the edge and in the app.
- [ ] Timeouts exist for reads, writes, inference, and dependencies.
- [ ] Secrets come from a secret store, not source, image, or logs.
- [ ] The model path is fixed and the artifact is verified before load.
- [ ] The runtime user is non-root; the filesystem is read-only.
- [ ] Egress is allowlisted; the metadata service is blocked.
- [ ] Rate-limit state is shared and its failure mode is defined.
- [ ] Kill switches exist, are documented, and have been tested.
- [ ] Logs exclude credentials and minimize personal data.
- [ ] Configuration is versioned and reviewed like code.

## 6. Governance and the assurance statement

Serving controls are evidence for governance functions:

| Framework | Function or practice | Evidence |
|---|---|---|
| NIST CSF 2.0 | Protect, Detect, Respond, Recover | LAB-14 controls; LAB-15 detections and playbook |
| NIST AI RMF | Govern, Map, Measure, Manage | Threat model, test results, residual risk |
| OWASP ASVS | Authentication, access control, validation, logging | 18-case suite and production additions |
| Saltzer & Schroeder | Least privilege, complete mediation, fail-safe defaults | Scoped tokens, object checks, fail-closed behavior |

Mapping is not certification. It tells a reviewer where the evidence lives.

### A scoped assurance statement

Use a sentence like this in the report:

> The service binds to loopback and enforces bearer authentication, scopes, an 8 KB body cap, a 32-row batch cap, 64 finite features in `[0, 1]`, 10 requests per 60 seconds per role, and metadata-only logging. All 18 scripted cases pass, and no demo token appears in 28 log records. These results cover the named cases on a local deployment. They do not establish TLS configuration, identity-provider integration, distributed rate limiting, object-level authorization, or robustness to adversarial in-range inputs, all of which remain out of scope or unverified.

That statement can be audited. "The API is secure" cannot.

## Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Copying a dev config to production | It works locally | Separate configs; test controls in staging |
| Leaving debug on | It helps diagnosis | Structured errors; server-side logs |
| Storing a token in an environment file committed to git | Convenience | Secret manager; secret scanning in CI |
| Granting the service registry write access | The pipeline uses one credential | Separate deploy and runtime identities |
| Running as root | The container works | Non-root user and read-only filesystem |
| Unrestricted egress | Dependencies are easier | Allowlist; block metadata |
| A kill switch no one has tested | It exists in the diagram | Test it in staging and record the result |
| Failing open when auth is unavailable | Availability pressure | Fail closed or document an approved degraded mode |
| Treating configuration as operations, not security | It is "just YAML" | Version and review it with the service |
| Claiming production readiness from LAB-14 | The tests pass | State the production gaps explicitly |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Service reachable externally | Bind address or proxy exposure | Bind to loopback/private; check ingress |
| Token works after rotation | Old credential not revoked | Revoke and test the old token |
| Secret visible in crash output | Environment variable or debug dump | Secret manager; disable debug dumps |
| Permission denied writing temp files | Read-only filesystem | Mount a small writable temp area |
| Egress dependency fails | Allowlist too narrow | Add the specific destination; do not open all egress |
| 503 after secret-store outage | Fail-closed behavior | Verify the policy is intended; alert |
| Kill switch has no effect | Cached config or wrong flag | Test propagation; version the switch |
| Config differs between pods | Manual edits | Immutable config and deployment review |

## Check your understanding

1. Name five unsafe defaults in a serving configuration and the safer choice for each.
2. Why is a token in an environment variable better than one in source code, and why is it still limited?
3. What does least privilege mean for the model artifact and the registry?
4. Give an example of failing closed and an example of a documented degraded mode.
5. Why must a kill switch be tested before an incident?
6. Write one sentence that scopes the assurance provided by LAB-14's 18 passing cases.

Answers are discussed in the [answer key](quiz-answers.md) and the exercises.

## Summary

- Configuration is part of the attack surface. Bind address, debug mode, TLS, CORS, limits, model path, secrets, container user, and egress are security decisions.
- Secrets have a lifecycle: generate, store, inject, use, rotate, revoke, and audit. Source code, images, logs, URLs, and client applications are not secret stores.
- Least privilege applies to the artifact, registry, data, logs, network, metadata service, filesystem, and container.
- Kill switches need an owner, a tested effect, and a defined response.
- Safe failure is explicit: fail closed for authentication and authorization, or document and approve a degraded mode.
- LAB-14 is a controlled lab, not a production deployment. The report must state the gap.
- A scoped assurance statement lists controls, evidence, and exclusions. It is the opposite of "the API is secure."

## Next

Return to the [module overview](index.md) and complete [LAB-14](../../labs/lab-14.md), [LAB-15](../../labs/lab-15.md), the [knowledge check](quiz.md), and the [exercises](exercises.md). The capstone will ask you to integrate these serving controls with the robustness, data, and supply-chain evidence from Modules 08–10.
