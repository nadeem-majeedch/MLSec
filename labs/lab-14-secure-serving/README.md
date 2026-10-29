# LAB-14 — Hardening a Local Prediction API

| Field | Value |
|---|---|
| Lab ID | LAB-14 |
| Tier | A |
| Time | 5 hours |
| Difficulty | 4 of 4 |
| Module | M11 — Serving and Monitoring |
| Outcomes | LO-22, LO-30 (supporting), LO-28 |
| Prerequisites | M01 lessons 5–6; M11 lessons 1–3; LAB-13 recommended |
| Data | digits plus local loopback |
| Compute | CPU only; a few seconds |

Full brief: [docs/labs/lab-14.md](../../docs/labs/lab-14.md) · Checking guide: [CHECKING.md](CHECKING.md)

## Scenario

The digit classifier is now a service. A partner will call `POST /predict` with
image features, and an operator will call `GET /stats`. You have to make the
service safe to expose on a trusted network before anyone writes a client.

The reference service binds only to `127.0.0.1`, authenticates bearer tokens with
constant-time comparison, enforces scopes, caps bodies at 8 KB and batches at 32
rows, validates 64 finite values in [0, 1] per row, rate-limits each role to 10
requests per 60 seconds, returns generic JSON errors, and logs metadata without
tokens or payloads.

Eighteen security cases exercise the happy path and the attacks: missing and
wrong tokens, a valid token without the right scope, malformed JSON, the wrong
content type, wrong shape, out-of-range values, non-numeric and non-finite
values, an oversized batch, an oversized body, a rate-limit burst, an unknown
path, and an error body that must not echo the token.

All processing is local. The demo tokens are not secrets and must not be reused.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

# reference path
python solution.py --out artifacts
python check_lab14.py --artifacts artifacts

# your path
python starter.py --out artifacts
python check_lab14.py --artifacts artifacts
```

## What you produce

- `artifacts/metrics.json`, `run.json`, `report.md`, and `manifest.json`.
- Results for all 18 security cases, including the expected rejection reason for each.
- `report.md` answers every reflection question and lists residual risks.
- `python check_lab14.py --artifacts artifacts` exits 0.

## Starter and TODO map

| File | TODO | Function or section | What must be implemented |
|---|---|---|---|
| `starter.py` | TODO 1 | `authorize` | Authenticate a bearer token with constant-time comparison and enforce a scope |
| `starter.py` | TODO 2 | `validate_payload` | Validate content, shape, dtype, finiteness, and range |
| `starter.py` | TODO 3 | `RateLimiter.allow` | Count requests per key in a fixed window |

## Hints

- Use `hmac.compare_digest` for token comparison. A plain `==` leaks timing information.
- Validate shape, dtype, finiteness, and range before the model sees the payload. Reject the body; do not silently clip it.
- The rate limiter counts per key in a fixed window. Decide whether a rejected request consumes budget and document it.

## Files

| File | Purpose |
|---|---|
| `CHECKING.md` | Checking guide, failure diagnosis, and rubric |
| `README.md` | Local quickstart |
| `check_lab14.py` | Independent artifact checker |
| `expected_metrics.json` | Reference values and tolerances |
| `requirements.txt` | Pinned dependencies |
| `solution.py` | Reference implementation |
| `starter.py` | Learner scaffold with numbered TODO blocks |

## Safety and cleanup

All data is public or synthetic, and every target is local. No external service, credential, or real person is involved. Do not substitute private data or point the code at a real system.

Run `rm -rf artifacts` (macOS/Linux) or `Remove-Item -Recurse -Force artifacts` (Windows) when finished. Never commit `artifacts/`.
