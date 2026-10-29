"""Independent checker for LAB-14.

Usage:
    python solution.py --out artifacts
    python check_lab14.py --artifacts artifacts

Exit code 0 means every check passed. The checker validates the recorded
evidence; it does not re-run your server.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED_TESTS = {
    "health_ok": 200,
    "missing_token": 401,
    "invalid_token": 401,
    "viewer_forbidden": 403,
    "valid_predict": 200,
    "malformed_json": 400,
    "wrong_content_type": 415,
    "wrong_length": 422,
    "out_of_range": 422,
    "non_numeric": 422,
    "non_finite": 422,
    "batch_too_large": 422,
    "oversized_body": 413,
    "rate_limit": 429,
    "admin_stats": 200,
    "client_stats_forbidden": 403,
    "unknown_path": 404,
    "safe_error_body": 401,
}
TOKENS = ["client-demo-token", "viewer-demo-token", "admin-demo-token"]
LOG_FIELDS = {"request_id", "method", "path", "status", "role", "body_bytes"}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-14 artifacts.")
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    root = args.artifacts

    metrics = load_json(root / "metrics.json")
    run = load_json(root / "run.json")
    manifest = load_json(root / "manifest.json")
    report = root / "report.md"
    logs_path = root / "logs" / "requests.jsonl"
    if not report.exists():
        fail("missing report.md")
    if not logs_path.exists():
        fail("missing logs/requests.jsonl")

    required = {"metrics.json", "run.json", "report.md", "logs/requests.jsonl"}
    paths = {entry["path"] for entry in manifest.get("files", [])}
    if not required <= paths:
        fail(f"manifest does not cover {sorted(required - paths)}")
    if run.get("lab") != "LAB-14":
        fail("run.json lab is not LAB-14")
    if run.get("model_hash") != metrics.get("model_hash"):
        fail("run.json model_hash does not match metrics.json")
    if len(metrics.get("model_hash", "")) != 64:
        fail("model_hash must be a SHA-256 hex digest")

    config = metrics["config"]
    if config["bind"] != "127.0.0.1":
        fail("the service must bind to loopback only")
    if config["max_body_bytes"] != 8192 or config["max_batch_rows"] != 32:
        fail("request bounds must be 8192 bytes and 32 rows")
    if config["rate_limit_requests"] != 10 or config["rate_limit_window_seconds"] != 60:
        fail("rate limit must be 10 requests per 60 seconds")
    if "bearer" not in config["auth"].lower():
        fail("config must document bearer authentication")

    tests = {test["name"]: test for test in metrics.get("tests", [])}
    if set(tests) != set(EXPECTED_TESTS):
        fail(f"test names are {sorted(tests)}, expected {sorted(EXPECTED_TESTS)}")
    for name, expected in EXPECTED_TESTS.items():
        test = tests[name]
        if test["expected"] != expected:
            fail(f"{name} expects {test['expected']}, reference is {expected}")
        if test["actual"] != expected:
            fail(f"{name} returned {test['actual']}, expected {expected}")
        if not test["passed"]:
            fail(f"{name} is marked failed")
    if tests["valid_predict"]["detail"].get("predictions") != 1:
        fail("valid_predict must return exactly one prediction")
    rate = tests["rate_limit"]["detail"]
    if rate.get("allowed") != 10 or rate.get("rejected") != 1:
        fail("rate_limit must allow 10 requests and reject the 11th")
    if tests["safe_error_body"]["detail"].get("leaked_token_marker"):
        fail("the error body leaked the token value")

    summary = metrics["summary"]
    if summary != {"total": 18, "passed": 18, "failed": 0}:
        fail(f"test summary is {summary}, expected 18/18/0")
    if metrics["gate"] != {"exit": 0}:
        fail("gate exit must be 0 when all tests pass")

    lines = [line for line in logs_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) < 18:
        fail("the request log must contain at least 18 entries")
    statuses = set()
    for index, line in enumerate(lines, start=1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            fail(f"log line {index} is not JSON")
        if set(record) != LOG_FIELDS:
            fail(f"log line {index} fields are {sorted(record)}, expected {sorted(LOG_FIELDS)}")
        statuses.add(int(record["status"]))
        lowered = line.lower()
        if any(token in line for token in TOKENS):
            fail(f"log line {index} contains a token value")
        if "authorization" in lowered or "features" in lowered:
            fail(f"log line {index} contains request content")
    for status in (200, 400, 401, 403, 404, 413, 415, 422, 429):
        if status not in statuses:
            fail(f"the request log never records status {status}")
    if metrics["log_redaction"]["tokens_in_logs"]:
        fail("metrics says tokens were found in logs")
    if metrics["log_redaction"]["lines"] != len(lines):
        fail("log_redaction.lines does not match the log file")

    text = report.read_text(encoding="utf-8").lower()
    for phrase in ("authentication", "validation", "rate", "error", "limitations", "defense"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print("PASS config: loopback bind, 8 KB body, 32 rows, 10 requests/60 s, bearer auth")
    print("PASS 18 security cases produced the expected status codes")
    print("PASS validation rejects wrong shape, type, range, non-finite, and oversized batches")
    print("PASS rate limiting allows 10 and rejects the 11th request")
    print("PASS logs contain only request metadata and no token or payload content")
    print("PASS report covers authentication, validation, rate limiting, errors, defense, limitations")
    print("LAB-14 CHECK PASSED")


if __name__ == "__main__":
    main()
