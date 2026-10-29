"""Check internal Markdown links and local assets.

Usage:
    python scripts/check_links.py
    python scripts/check_links.py --check-external --timeout 10
    python scripts/check_links.py --json link-report.json

Internal links are checked by default. External HTTP(S) links are only checked
with --check-external, so the default run makes no network calls.

The checker understands relative files, directory index.md targets, heading
anchors using the MkDocs/Python-Markdown slug convention, and explicit
``{#custom-id}`` anchors. Links inside fenced code blocks and inline code are
ignored.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "site",
    "build",
    "dist",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "artifacts",
}
FENCE_RE = re.compile(r"(?ms)^[ \t]*(`{3,}|~{3,})[^\n]*\n.*?^[ \t]*\1[ \t]*$")
INLINE_CODE_RE = re.compile(r"(?<!`)(`+)(?!`).*?(?<!`)\1(?!`)")
HTML_COMMENT_RE = re.compile(r"(?s)<!--.*?-->")
LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)]*)\)")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


@dataclass(frozen=True)
class Link:
    source: str
    line: int
    text: str
    target: str
    is_image: bool


@dataclass(frozen=True)
class LinkIssue:
    source: str
    line: int
    target: str
    reason: str


def _blank(match: re.Match[str]) -> str:
    """Replace a match with spaces while preserving newlines and offsets."""
    return re.sub(r"[^\n]", " ", match.group(0))


def strip_code(text: str) -> str:
    """Blank fenced blocks, inline code, and HTML comments, preserving lines."""
    text = FENCE_RE.sub(_blank, text)
    text = INLINE_CODE_RE.sub(_blank, text)
    text = HTML_COMMENT_RE.sub(_blank, text)
    return text


def _split_target(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        return value[1 : value.index(">")].strip()
    # Drop an optional Markdown title: [text](path "title").
    match = re.match(r"^(.*?)(?:\s+[\"'(].*[\"')])?$", value)
    return (match.group(1) if match else value).strip()


def extract_links(text: str, source: str = "<text>") -> list[Link]:
    """Return links and images outside code spans and fenced blocks."""
    stripped = strip_code(text)
    links: list[Link] = []
    for match in LINK_RE.finditer(stripped):
        raw = _split_target(match.group(3))
        if not raw:
            continue
        line = stripped.count("\n", 0, match.start()) + 1
        links.append(
            Link(
                source=source,
                line=line,
                text=match.group(2).strip(),
                target=raw,
                is_image=bool(match.group(1)),
            )
        )
    return links


def slugify(value: str, separator: str = "-") -> str:
    """Approximate the MkDocs/Python-Markdown heading slug."""
    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[*_~]", "", value)
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s]+", separator, value).strip(separator)
    return value


def heading_anchors(text: str) -> set[str]:
    """Collect heading anchors, including explicit {#id} attributes."""
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for match in re.finditer(r"<a\s+(?:id|name)=[\"']([^\"']+)[\"']", strip_code(text), flags=re.IGNORECASE):
        anchors.add(match.group(1))
    for line in strip_code(text).splitlines():
        match = re.match(r"^[ \t]{0,3}(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$", line)
        if not match:
            continue
        title = match.group(2).strip()
        explicit = re.search(r"\{#([A-Za-z0-9_.:-]+)\}\s*$", title)
        if explicit:
            anchors.add(explicit.group(1))
            title = title[: explicit.start()].strip()
        base = slugify(title)
        if not base:
            continue
        candidate = base
        index = counts.get(base, 0)
        while candidate in anchors:
            index += 1
            candidate = f"{base}_{index}"
        counts[base] = index
        anchors.add(candidate)
    return anchors


def _is_external(target: str) -> bool:
    return bool(SCHEME_RE.match(target)) and not target.startswith("file:")


def _resolve_target(source: Path, target: str) -> tuple[Path, str]:
    path_part, _, anchor = target.partition("#")
    path_part = urllib.parse.unquote(path_part)
    if path_part.startswith("/"):
        # Prefer docs/ at the repository root for site-absolute links.
        root = next(
            (parent for parent in source.parents if (parent / "mkdocs.yml").exists()),
            None,
        )
        base = root / "docs" if root and (root / "docs").is_dir() else REPO_ROOT
        resolved = (base / path_part.lstrip("/")).resolve()
        if not resolved.exists():
            resolved = (base.parent / path_part.lstrip("/")).resolve()
    else:
        resolved = (source.parent / path_part).resolve()
    if path_part.endswith("/") or resolved.is_dir():
        resolved = resolved / "index.md"
    return resolved, anchor


def check_file(path: Path) -> list[LinkIssue]:
    """Check every internal link and local image in one Markdown file."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    issues: list[LinkIssue] = []
    for link in extract_links(text, _display(path)):
        if _is_external(link.target) or link.target.startswith("#"):
            continue
        if "<" in link.target or ">" in link.target:
            continue
        if link.target.startswith("mailto:") or link.target.startswith("tel:"):
            continue
        resolved, anchor = _resolve_target(path, link.target)
        if not resolved.exists():
            issues.append(
                LinkIssue(link.source, link.line, link.target, f"missing file: {_display(resolved)}")
            )
            continue
        if anchor and resolved.suffix.lower() == ".md":
            try:
                target_text = resolved.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if anchor not in heading_anchors(target_text):
                issues.append(
                    LinkIssue(
                        link.source,
                        link.line,
                        link.target,
                        f"missing anchor '#{anchor}' in {_display(resolved)}",
                    )
                )
    return issues


def _display(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def iter_markdown(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        files.append(path)
    return sorted(files)


def check_repository(root: Path = REPO_ROOT) -> list[LinkIssue]:
    issues: list[LinkIssue] = []
    for path in iter_markdown(root):
        issues.extend(check_file(path))
    return issues


def collect_external_links(root: Path = REPO_ROOT) -> list[Link]:
    seen: dict[str, Link] = {}
    for path in iter_markdown(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        for link in extract_links(text, _display(path)):
            if link.target.startswith(("http://", "https://")) and link.target not in seen:
                seen[link.target] = link
    return list(seen.values())


def _fetch(url: str, timeout: float, method: str) -> tuple[int, str]:
    request = urllib.request.Request(
        url,
        method=method,
        headers={"User-Agent": "mlsec-link-check/1.0 (+local validation)"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.status, response.geturl()


def _probe(url: str, timeout: float) -> tuple[str, str]:
    """Return (state, detail) where state is 'ok', 'blocked', or 'broken'.

    HEAD is tried first. Many documentation hosts reject HEAD or answer 404 to
    it, so any failure is retried with a bounded GET before calling a link
    broken. A GET that is rejected with 401/403/429 is reported as blocked,
    because bot protection is not evidence that the page is missing.
    """
    head_status: int | None = None
    head_detail = "no HEAD response"
    try:
        status, _ = _fetch(url, timeout, "HEAD")
        if 200 <= status < 400:
            return "ok", f"HTTP {status}"
    except urllib.error.HTTPError as exc:
        head_status = exc.code
        head_detail = f"HTTP {exc.code}"
    except Exception as exc:  # noqa: BLE001 - retry with GET
        head_status = None
        head_detail = str(exc)

    try:
        status, _ = _fetch(url, timeout, "GET")
        if 200 <= status < 400:
            return "ok", f"HTTP {status} (GET)"
        return "broken", f"HTTP {status} (GET)"
    except urllib.error.HTTPError as exc:
        detail = f"HEAD {head_detail}; GET HTTP {exc.code}"
        if exc.code in {401, 403, 429}:
            return "blocked", detail
        return "broken", detail
    except Exception as exc:  # noqa: BLE001 - report, do not raise
        prefix = f"HEAD {head_detail}; " if head_status else ""
        return "broken", f"{prefix}GET failed: {exc}"


def check_external_links(
    links: list[Link], timeout: float = 10.0, workers: int = 8
) -> tuple[list[LinkIssue], list[LinkIssue]]:
    """Return (broken, blocked) external link issues."""
    broken: list[LinkIssue] = []
    blocked: list[LinkIssue] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_probe, link.target, timeout): link for link in links}
        for future in as_completed(futures):
            link = futures[future]
            state, detail = future.result()
            issue = LinkIssue(link.source, link.line, link.target, detail)
            if state == "broken":
                broken.append(issue)
            elif state == "blocked":
                blocked.append(issue)
    key = lambda issue: (issue.source, issue.line)  # noqa: E731
    return sorted(broken, key=key), sorted(blocked, key=key)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check Markdown links and local assets.")
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument(
        "--check-external",
        action="store_true",
        help="Also probe HTTP(S) links (network access; off by default).",
    )
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    root = args.root.resolve()
    files = iter_markdown(root)
    issues = check_repository(root)
    external_issues: list[LinkIssue] = []
    blocked_issues: list[LinkIssue] = []
    if args.check_external:
        links = collect_external_links(root)
        print(f"Checking {len(links)} external links (timeout {args.timeout:g}s)...")
        external_issues, blocked_issues = check_external_links(links, args.timeout)
        issues.extend(external_issues)

    for issue in issues:
        print(f"FAIL {issue.source}:{issue.line}: {issue.target} ({issue.reason})")
    for issue in blocked_issues:
        print(f"WARN blocked by host {issue.source}:{issue.line}: {issue.target} ({issue.reason})")

    if args.json:
        args.json.write_text(
            json.dumps(
                {
                    "files_checked": len(files),
                    "external_checked": args.check_external,
                    "issues": [asdict(issue) for issue in issues],
                    "blocked_external": [asdict(issue) for issue in blocked_issues],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    if issues:
        print(f"LINK CHECK FAILED: {len(issues)} issue(s) in {len(files)} files")
        return 1
    suffix = " including external probes" if args.check_external else ""
    print(f"LINK CHECK PASSED: {len(files)} Markdown files{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
