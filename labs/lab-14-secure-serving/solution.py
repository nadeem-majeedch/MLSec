"""LAB-14 reference solution: a hardened local prediction API.

Run from this directory:
    python solution.py --out artifacts

The server binds to 127.0.0.1 on an ephemeral port, runs 18 security tests,
writes metrics.json, logs/requests.jsonl, run.json, report.md, and manifest.json.
Tokens are demo constants; a real deployment issues them from a secret store.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import math
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

MAX_BODY = 8192
MAX_BATCH = 32
RATE_LIMIT = 10
RATE_WINDOW = 60.0
N_FEATURES = 64
MODEL_VERSION = "digits-logreg-v1"

TOKENS = {
    "client": {"token": "client-demo-token", "scopes": {"predict"}},
    "viewer": {"token": "viewer-demo-token", "scopes": set()},
    "admin": {"token": "admin-demo-token", "scopes": {"predict", "stats"}},
}

MODEL: LogisticRegression | None = None
LIMITER = None
LOG_PATH: Path | None = None
REQUEST_COUNTER = 0
COUNTER_LOCK = threading.Lock()
STATS = {"requests": 0, "rejected": 0, "predictions": 0}
STATS_LOCK = threading.Lock()
LOG_LOCK = threading.Lock()


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message


class RateLimiter:
    """Fixed-window limiter keyed by role; deterministic for the test suite."""

    def __init__(self, limit: int = RATE_LIMIT, window: float = RATE_WINDOW):
        self.limit = limit
        self.window = window
        self.entries: dict[str, tuple[float, int]] = {}

    def allow(self, key: str, now: float | None = None) -> bool:
        current = time.monotonic() if now is None else now
        start, count = self.entries.get(key, (current, 0.0))
        if current - start >= self.window:
            start, count = current, 0
        if count >= self.limit:
            self.entries[key] = (start, count)
            return False
        self.entries[key] = (start, count + 1)
        return True

    def reset(self) -> None:
        self.entries.clear()


def authorize(header_value: str | None, scope: str) -> str:
    """Authenticate a Bearer token, enforce a scope, and return the role."""
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


def validate_payload(payload: object) -> np.ndarray:
    """Return a validated (rows, N_FEATURES) float array or raise ApiError(422)."""
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


def log_event(request_id: str, method: str, path: str, status: int, role: str, body_bytes: int) -> None:
    record = {
        "request_id": request_id,
        "method": method,
        "path": path,
        "status": status,
        "role": role,
        "body_bytes": body_bytes,
    }
    with LOG_LOCK:
        with open(LOG_PATH, "a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def next_request_id() -> str:
    global REQUEST_COUNTER
    with COUNTER_LOCK:
        REQUEST_COUNTER += 1
        return f"req-{REQUEST_COUNTER:04d}"


def make_handler(model: LogisticRegression):
    class Handler(BaseHTTPRequestHandler):
        server_version = "MLSecLab/1.0"
        sys_version = ""
        protocol_version = "HTTP/1.1"

        def log_message(self, format, *args):  # silence the default access log
            return

        def _send(self, status: int, payload: dict, extra_headers: dict | None = None) -> None:
            body = json.dumps(payload, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Connection", "close")
            if extra_headers:
                for key, value in extra_headers.items():
                    self.send_header(key, value)
            self.end_headers()
            self.wfile.write(body)
            self.close_connection = True

        def _error(self, request_id: str, error: ApiError, role: str = "anonymous", body_bytes: int = 0) -> None:
            with STATS_LOCK:
                STATS["rejected"] += 1
            log_event(request_id, self.command, self.path, error.status, role, body_bytes)
            headers = {"WWW-Authenticate": "Bearer"} if error.status == 401 else None
            self._send(
                error.status,
                {
                    "request_id": request_id,
                    "error": {"code": error.code, "message": error.message},
                },
                headers,
            )

        def do_GET(self) -> None:
            request_id = next_request_id()
            with STATS_LOCK:
                STATS["requests"] += 1
            if self.path == "/health":
                log_event(request_id, "GET", self.path, 200, "anonymous", 0)
                self._send(200, {"status": "ok", "model_version": MODEL_VERSION})
                return
            if self.path == "/stats":
                role = "anonymous"
                try:
                    role = authorize(self.headers.get("Authorization"), "stats")
                    with STATS_LOCK:
                        snapshot = dict(STATS)
                    log_event(request_id, "GET", self.path, 200, role, 0)
                    self._send(200, {"request_id": request_id, "stats": snapshot})
                except ApiError as error:
                    self._error(request_id, error, role)
                return
            self._error(request_id, ApiError(404, "not_found", "unknown path"))

        def do_POST(self) -> None:
            request_id = next_request_id()
            with STATS_LOCK:
                STATS["requests"] += 1
            if self.path != "/predict":
                self._error(request_id, ApiError(404, "not_found", "unknown path"))
                return
            try:
                length = int(self.headers.get("Content-Length", "0") or 0)
            except ValueError:
                self._error(request_id, ApiError(400, "bad_length", "invalid Content-Length"))
                return
            if length <= 0:
                self._error(request_id, ApiError(411, "length_required", "Content-Length is required"))
                return
            if length > MAX_BODY:
                self._error(request_id, ApiError(413, "body_too_large", f"body must be at most {MAX_BODY} bytes"), body_bytes=length)
                return
            body = self.rfile.read(length)
            role = "anonymous"
            try:
                role = authorize(self.headers.get("Authorization"), "predict")
                if not LIMITER.allow(role):
                    raise ApiError(429, "rate_limited", "request budget exhausted")
                if self.headers.get("Content-Type", "").split(";")[0].strip().lower() != "application/json":
                    raise ApiError(415, "unsupported_media_type", "Content-Type must be application/json")
                try:
                    payload = json.loads(body.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    raise ApiError(400, "malformed_json", "body is not valid JSON")
                features = validate_payload(payload)
                predictions = model.predict(features).astype(int).tolist()
            except ApiError as error:
                self._error(request_id, error, role, len(body))
                return
            with STATS_LOCK:
                STATS["predictions"] += len(predictions)
            log_event(request_id, "POST", self.path, 200, role, len(body))
            self._send(
                200,
                {
                    "request_id": request_id,
                    "model_version": MODEL_VERSION,
                    "count": len(predictions),
                    "predictions": predictions,
                },
            )

    return Handler


def train_model() -> LogisticRegression:
    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    return LogisticRegression(max_iter=300, C=1.0).fit(X, y)


def call(base_url: str, method: str, path: str, body: bytes | None = None, token: str | None = None, content_type: str = "application/json"):
    headers = {"Content-Type": content_type}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(base_url + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, json.loads(response.read() or b"{}")
    except urllib.error.HTTPError as error:
        raw = error.read()
        try:
            payload = json.loads(raw or b"{}")
        except json.JSONDecodeError:
            payload = {"raw": raw.decode("utf-8", "replace")}
        return error.code, payload


def valid_body(rows: int = 1) -> bytes:
    return json.dumps({"features": [[0] * N_FEATURES for _ in range(rows)]}).encode("utf-8")


def run_security_tests(base_url: str) -> list[dict]:
    tests: list[dict] = []

    def record(name: str, expected: int, status: int, detail: dict | None = None) -> None:
        tests.append(
            {
                "name": name,
                "expected": expected,
                "actual": status,
                "passed": status == expected,
                "detail": detail or {},
            }
        )

    status, payload = call(base_url, "GET", "/health")
    record("health_ok", 200, status, {"keys": sorted(payload)})

    status, payload = call(base_url, "POST", "/predict", valid_body())
    record("missing_token", 401, status)

    status, _ = call(base_url, "POST", "/predict", valid_body(), token="wrong-token")
    record("invalid_token", 401, status)

    status, _ = call(base_url, "POST", "/predict", valid_body(), token="viewer-demo-token")
    record("viewer_forbidden", 403, status)

    status, payload = call(base_url, "POST", "/predict", valid_body(), token="client-demo-token")
    record("valid_predict", 200, status, {"predictions": len(payload.get("predictions", []))})

    status, _ = call(base_url, "POST", "/predict", b"{not json", token="client-demo-token")
    record("malformed_json", 400, status)

    status, _ = call(
        base_url, "POST", "/predict", valid_body(), token="client-demo-token", content_type="text/plain"
    )
    record("wrong_content_type", 415, status)

    status, _ = call(
        base_url, "POST", "/predict",
        json.dumps({"features": [[0.0] * 10]}).encode("utf-8"),
        token="client-demo-token",
    )
    record("wrong_length", 422, status)

    status, _ = call(
        base_url, "POST", "/predict",
        json.dumps({"features": [[1.5] * N_FEATURES]}).encode("utf-8"),
        token="client-demo-token",
    )
    record("out_of_range", 422, status)

    status, _ = call(
        base_url, "POST", "/predict",
        json.dumps({"features": [["a"] * N_FEATURES]}).encode("utf-8"),
        token="client-demo-token",
    )
    record("non_numeric", 422, status)

    status, _ = call(
        base_url, "POST", "/predict",
        json.dumps({"features": [[float("nan")] * N_FEATURES]}).encode("utf-8"),
        token="client-demo-token",
    )
    record("non_finite", 422, status)

    status, _ = call(base_url, "POST", "/predict", valid_body(MAX_BATCH + 1), token="client-demo-token")
    record("batch_too_large", 422, status)

    status, _ = call(base_url, "POST", "/predict", b"x" * (MAX_BODY + 100), token="client-demo-token")
    record("oversized_body", 413, status)

    LIMITER.reset()
    outcomes = [
        call(base_url, "POST", "/predict", valid_body(), token="client-demo-token")[0]
        for _ in range(RATE_LIMIT + 1)
    ]
    record(
        "rate_limit",
        429,
        outcomes[-1],
        {"allowed": sum(1 for status in outcomes if status == 200), "rejected": sum(1 for status in outcomes if status == 429)},
    )

    LIMITER.reset()
    status, payload = call(base_url, "GET", "/stats", token="admin-demo-token")
    record("admin_stats", 200, status, {"keys": sorted(payload.get("stats", {}))})

    status, _ = call(base_url, "GET", "/stats", token="client-demo-token")
    record("client_stats_forbidden", 403, status)

    status, _ = call(base_url, "GET", "/nope")
    record("unknown_path", 404, status)

    status, payload = call(base_url, "POST", "/predict", valid_body(), token="wrong-token")
    serialized = json.dumps(payload).lower()
    leaked = "wrong-token" in serialized
    tests.append(
        {
            "name": "safe_error_body",
            "expected": 401,
            "actual": status,
            "passed": status == 401 and not leaked and "traceback" not in serialized,
            "detail": {"leaked_token_marker": leaked},
        }
    )
    return tests


def main() -> None:
    global MODEL, LIMITER, LOG_PATH

    parser = argparse.ArgumentParser(description="Run the hardened prediction API test suite.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    logs_dir = args.out / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    LOG_PATH = logs_dir / "requests.jsonl"
    LOG_PATH.write_text("", encoding="utf-8")

    MODEL = train_model()
    LIMITER = RateLimiter()
    model_hash = hashlib.sha256(
        np.ascontiguousarray(MODEL.coef_).tobytes() + np.ascontiguousarray(MODEL.intercept_).tobytes()
    ).hexdigest()

    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(MODEL))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        tests = run_security_tests(base_url)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    passed = sum(1 for test in tests if test["passed"])
    metrics = {
        "api": "local prediction service (loopback only)",
        "config": {
            "bind": "127.0.0.1",
            "max_body_bytes": MAX_BODY,
            "max_batch_rows": MAX_BATCH,
            "rate_limit_requests": RATE_LIMIT,
            "rate_limit_window_seconds": RATE_WINDOW,
            "auth": "bearer tokens with scopes",
            "log_fields": ["request_id", "method", "path", "status", "role", "body_bytes"],
        },
        "model_version": MODEL_VERSION,
        "model_hash": model_hash,
        "tests": tests,
        "summary": {"total": len(tests), "passed": passed, "failed": len(tests) - passed},
        "gate": {"exit": 0 if passed == len(tests) else 1},
    }

    log_lines = LOG_PATH.read_text(encoding="utf-8").splitlines()
    token_values = [meta["token"] for meta in TOKENS.values()]
    metrics["log_redaction"] = {
        "lines": len(log_lines),
        "tokens_in_logs": any(token in line for line in log_lines for token in token_values),
    }

    write_json(args.out / "metrics.json", metrics)
    write_json(
        args.out / "run.json",
        {
            "lab": "LAB-14",
            "model_version": MODEL_VERSION,
            "model_hash": model_hash,
            "environment": environment(),
        },
    )
    (args.out / "report.md").write_text(build_report(metrics), encoding="utf-8", newline="\n")
    write_json(
        args.out / "manifest.json",
        build_manifest(args.out, ["metrics.json", "run.json", "report.md", "logs/requests.jsonl"]),
    )

    print(f"tests={passed}/{len(tests)} gate={metrics['gate']['exit']}")
    for test in tests:
        if not test["passed"]:
            print(f"FAILED {test['name']}: expected {test['expected']} got {test['actual']}")
    print(f"tokens in logs={metrics['log_redaction']['tokens_in_logs']}")
    print(f"artifacts written to {args.out}")


def build_report(metrics: dict) -> str:
    tests = metrics["tests"]
    lines = [
        "# LAB-14 report — hardened local prediction API",
        "",
        "The service binds to 127.0.0.1 on an ephemeral port. Every request is",
        "authenticated except `/health`, rate-limited per role, size-bounded, and",
        "schema-validated. Errors are generic JSON with a request id.",
        "",
        "## Security tests",
        "",
        "| Case | Expected | Actual | Pass |",
        "|---|---:|---:|---|",
    ]
    for test in tests:
        lines.append(
            f"| {test['name']} | {test['expected']} | {test['actual']} | {'yes' if test['passed'] else 'NO'} |"
        )
    lines += [
        "",
        f"Passed {metrics['summary']['passed']} of {metrics['summary']['total']} cases.",
        "",
        "## Controls",
        "",
        "| Control | Implementation |",
        "|---|---|",
        "| Authentication | Bearer token compared with `hmac.compare_digest` |",
        "| Authorization | Scopes: `predict`, `stats` |",
        "| Request bounds | 8 KB body, 32 rows per request |",
        "| Input validation | 64 finite numbers per row, each in [0, 1] |",
        "| Rate limiting | 10 requests per 60 seconds per role |",
        "| Safe errors | Generic code and message, no stack trace, no token echo |",
        "| Logging | Role only; no token, header, or body content |",
        "| Network exposure | Loopback bind; connection closed after each response |",
        "",
        "## Defense in depth",
        "",
        "No single control carries the service. Authentication answers who is",
        "calling; authorization answers what they may do; rate limiting bounds",
        "volume; size and schema checks bound each request; safe errors avoid",
        "leaking internals; redacted logs preserve evidence without storing",
        "credentials. Removing any one layer leaves a gap the others do not close.",
        "",
        "## Residual risks and trade-offs",
        "",
        "- Tokens are demo constants, not issued or rotated by a real identity provider.",
        "- The rate limiter is in-process; a restart clears it and multiple workers",
        "  would not share state.",
        "- The model is small and local; no GPU, concurrency, or load testing was done.",
        "- A passing suite proves these cases pass, not that the service is secure.",
        "- Strict validation rejects valid variations (for example, other image sizes)",
        "  and every rejection costs a user request.",
        "",
        "## Limitations",
        "",
        "- No TLS; loopback-only traffic was assumed.",
        "- No persistence for stats or audit logs.",
        "- No adversarial input testing beyond shape, type, and range.",
        "- The test client is sequential; concurrent abuse is untested.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
