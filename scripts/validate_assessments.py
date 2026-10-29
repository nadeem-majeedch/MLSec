"""Validate the ML-Sec student assessment package.

Structural checks run offline and make no network calls:

* every required student page, key, and blueprint exists
* each of the 19 module alternate quizzes has 8 items, 12 points, and 8 keyed entries
* each of the five level checks has 10 items, 20 points, and 10 keyed entries
* the diagnostic, question bank, and final assessment match their declared counts
* every keyed item carries a module / outcome / Bloom / difficulty tag
* keys live outside the MkDocs build and are not in the navigation
* answer-key paths named by student pages resolve
* the student navigation exposes every assessment entry point
* rubric weights total 100 and every lab appears in the completion checklists
* the practice widget defines ten items with in-range keys
* internal Markdown links in the assessment tree resolve
* no question stem is duplicated verbatim across assessments

Usage:
    python scripts/validate_assessments.py
    python scripts/validate_assessments.py --json assessment-validation.json
    python scripts/validate_assessments.py --strict-warnings

Exit code 0 means every enabled check passed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_links  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_ASSESSMENTS = REPO_ROOT / "docs" / "assessments"
KEYS_ROOT = REPO_ROOT / "assessments" / "answer-keys"
MKdocs = REPO_ROOT / "mkdocs.yml"

MODULES = [f"M{number:02d}" for number in range(19)]
LEVEL_MODULES = {
    1: ["M00", "M01", "M02", "M03"],
    2: ["M04", "M05", "M06", "M07"],
    3: ["M08", "M09", "M10", "M11"],
    4: ["M12", "M13", "M14", "M15"],
    5: ["M16", "M17", "M18"],
}
VALID_OUTCOMES = {f"LO-{number:02d}" for number in range(1, 36)}
TAG_LINE_RE = re.compile(r"^Tag: (.+)$", re.MULTILINE)
QUIZ_POINTS = [1, 1, 1, 1, 1, 2, 2, 3]
LEVEL_CHECK_POINTS = [1, 1, 1, 1, 1, 1, 2, 2, 5, 5]

REQUIRED_FILES = [
    "docs/assessments/index.md",
    "docs/assessments/practice.md",
    "docs/assessments/diagnostic/index.md",
    "docs/assessments/module-quizzes/index.md",
    "docs/assessments/level-checks/index.md",
    "docs/assessments/final-assessment/index.md",
    "docs/assessments/question-bank/index.md",
    "docs/assessments/rubrics/index.md",
    "docs/assessments/rubrics/lab-rubric.md",
    "docs/assessments/rubrics/lab-completion-checklists.md",
    "docs/assessments/rubrics/project-rubric.md",
    "docs/assessments/rubrics/capstone-rubric.md",
    "docs/assessments/progress-and-reflection.md",
    "assessments/README.md",
    "assessments/diagnostic/README.md",
    "assessments/module-quizzes/README.md",
    "assessments/level-checks/README.md",
    "assessments/final-assessment/README.md",
    "assessments/rubrics/README.md",
    "assessments/answer-keys/diagnostic-key.md",
    "assessments/answer-keys/question-bank-key.md",
    "assessments/answer-keys/final-assessment-key.md",
    "docs/javascripts/self-check.js",
    "docs/stylesheets/self-check.css",
]

NAV_ENTRIES = [
    "assessments/index.md",
    "assessments/practice.md",
    "assessments/diagnostic/index.md",
    "assessments/module-quizzes/index.md",
    "assessments/level-checks/index.md",
    "assessments/final-assessment/index.md",
    "assessments/question-bank/index.md",
    "assessments/rubrics/index.md",
    "assessments/rubrics/lab-rubric.md",
    "assessments/rubrics/lab-completion-checklists.md",
    "assessments/rubrics/project-rubric.md",
    "assessments/rubrics/capstone-rubric.md",
    "assessments/progress-and-reflection.md",
]

LAB_IDS = ["LAB-01", "LAB-01B"] + [f"LAB-{number:02d}" for number in range(2, 21)]


@dataclass
class AssessmentResult:
    name: str
    path: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: int = 0

    @property
    def ok(self) -> bool:
        return not self.errors

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def split_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    cells = [cell.strip() for cell in stripped[1:-1].split("|")]
    if not cells or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
        return None
    return cells


def parse_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("## "):
            break
        cells = split_row(line)
        if not cells or len(cells) < 2 or cells[0] in {"Field", "---"}:
            continue
        metadata[cells[0]] = cells[1]
    return metadata


def numbered_sections(text: str, prefix: str) -> dict[int, str]:
    pattern = re.compile(rf"^{re.escape(prefix)}(\d+)\.\s", re.MULTILINE)
    matches = list(pattern.finditer(text))
    sections: dict[int, str] = {}
    for position, match in enumerate(matches):
        start = match.end()
        end = matches[position + 1].start() if position + 1 < len(matches) else len(text)
        sections[int(match.group(1))] = text[start:end]
    return sections


def item_type(body: str) -> str:
    options = re.findall(r"^\s*([A-D])\.\s+\S", body, re.MULTILINE)
    if len(options) >= 2:
        return "mcq"
    if re.search(r"true or false", body, re.IGNORECASE):
        return "tf"
    return "written"


def keyed_answer(body: str) -> str | None:
    first_line = next((line.strip() for line in body.splitlines() if line.strip()), "")
    match = re.match(r"^([A-D])\s+[—-]\s+", first_line)
    if match:
        return match.group(1)
    match = re.match(r"^(True|False)\b", first_line)
    if match:
        return match.group(1)
    return None


def key_tags(text: str) -> tuple[list[tuple[list[str], list[str], int, int]], list[str]]:
    tags: list[tuple[list[str], list[str], int, int]] = []
    malformed: list[str] = []
    for line in TAG_LINE_RE.findall(text):
        modules = re.findall(r"\b(PRE|M\d{2})\b", line)
        outcomes = re.findall(r"\bLO-\d{2}\b", line)
        bloom = re.search(r"Bloom ([1-6])", line)
        difficulty = re.search(r"D([1-5])\.?$", line)
        if not modules or not outcomes or not bloom or not difficulty:
            malformed.append(line)
            continue
        tags.append(
            (
                sorted(set(modules)),
                sorted(set(outcomes)),
                int(bloom.group(1)),
                int(difficulty.group(1)),
            )
        )
    return tags, malformed


def check_tag_membership(
    result: AssessmentResult,
    tags: list[tuple[list[str], list[str], int, int]],
    allowed_modules: set[str],
    allowed_outcomes: set[str] | None = None,
) -> None:
    for modules, outcomes, bloom, difficulty in tags:
        for module in modules:
            if module not in allowed_modules:
                result.fail(f"key tag names unexpected module {module}")
        for outcome in outcomes:
            if outcome not in VALID_OUTCOMES:
                result.fail(f"key tag names unknown outcome {outcome}")
            elif allowed_outcomes is not None and outcome not in allowed_outcomes:
                result.fail(f"key tag outcome {outcome} is not listed in the page metadata")
        if not 1 <= bloom <= 6:
            result.fail(f"key tag has invalid Bloom level {bloom}")
        if not 1 <= difficulty <= 5:
            result.fail(f"key tag has invalid difficulty D{difficulty}")


def validate_item_pairs(
    result: AssessmentResult,
    student_sections: dict[int, str],
    key_sections: dict[int, str],
    keys_text: str,
    expected: int,
    label: str,
) -> None:
    if sorted(student_sections) != list(range(1, expected + 1)):
        result.fail(f"{label} student items are {sorted(student_sections)}, expected 1..{expected}")
    if sorted(key_sections) != list(range(1, expected + 1)):
        result.fail(f"{label} key items are {sorted(key_sections)}, expected 1..{expected}")
    tags, malformed = key_tags(keys_text)
    if len(tags) != expected:
        result.fail(f"{label} key has {len(tags)} tags, expected {expected}")
    for line in malformed:
        result.fail(f"{label} key has a malformed tag line: {line[:80]}")
    if len(tags) + len(malformed) != expected:
        result.fail(
            f"{label} key has {len(tags) + len(malformed)} tag lines, expected {expected}"
        )
    for number, body in sorted(student_sections.items()):
        if number not in key_sections:
            continue
        kind = item_type(body)
        answer = keyed_answer(key_sections[number])
        if kind == "mcq":
            options = re.findall(r"^\s*([A-D])\.\s+\S", body, re.MULTILINE)
            if len(options) != 4:
                result.fail(f"item {number} has {len(options)} options, expected 4")
            if answer is None or answer not in options:
                result.fail(f"item {number} key answer {answer!r} is not one of its options")
        elif kind == "tf":
            if answer not in {"True", "False"}:
                result.fail(f"item {number} is true/false but the key starts {answer!r}")
        else:
            if answer is not None:
                result.fail(f"item {number} is written but the key starts with a choice {answer!r}")


def require_metadata(
    result: AssessmentResult,
    metadata: dict[str, str],
    fields: list[str],
) -> None:
    for name in fields:
        if not metadata.get(name):
            result.fail(f"metadata field '{name}' is missing or empty")


def validate_answer_key_path(
    result: AssessmentResult,
    metadata: dict[str, str],
    relative: str,
) -> None:
    if metadata.get("Answer key") and relative not in metadata["Answer key"]:
        result.fail(f"Answer key metadata does not name {relative}")
    if not (REPO_ROOT / relative).exists():
        result.fail(f"missing answer key {relative}")
    else:
        result.checks += 1


def validate_quiz(module: str) -> AssessmentResult:
    name = f"QZ-{module[1:]}B"
    page = DOCS_ASSESSMENTS / "module-quizzes" / f"qz-{module[1:]}b.md"
    key = KEYS_ROOT / "module-quizzes" / f"qz-{module[1:]}b-key.md"
    relative_key = key.relative_to(REPO_ROOT).as_posix()
    result = AssessmentResult(name=name, path=page.relative_to(REPO_ROOT).as_posix())
    if not page.exists():
        result.fail("missing student page")
        return result
    if not key.exists():
        result.fail(f"missing {relative_key}")
        return result
    text = page.read_text(encoding="utf-8")
    key_text = key.read_text(encoding="utf-8")
    metadata = parse_metadata(text)
    require_metadata(
        result, metadata, ["Module", "Items", "Points", "Time guide", "Pass", "Outcomes", "Answer key"]
    )
    if metadata.get("Items") != "8":
        result.fail(f"Items is {metadata.get('Items')!r}, expected '8'")
    if metadata.get("Points") != "12":
        result.fail(f"Points is {metadata.get('Points')!r}, expected '12'")
    if metadata.get("Pass") != "10/12":
        result.fail(f"Pass is {metadata.get('Pass')!r}, expected '10/12'")
    if metadata.get("Module", "")[:3] != module:
        result.fail(f"Module metadata does not start with {module}")
    validate_answer_key_path(result, metadata, relative_key)
    outcomes = set(re.findall(r"LO-\d{2}", metadata.get("Outcomes", "")))
    if not outcomes:
        result.fail("Outcomes metadata lists no LO identifiers")
    validate_item_pairs(
        result,
        numbered_sections(text, "## "),
        numbered_sections(key_text, "## "),
        key_text,
        8,
        "quiz",
    )
    tags, malformed = key_tags(key_text)
    check_tag_membership(result, tags, set(MODULES), outcomes)
    tagged_outcomes = {outcome for _, outcomes_, _, _ in tags for outcome in outcomes_}
    if tagged_outcomes != outcomes:
        result.fail(
            f"Outcomes metadata {sorted(outcomes)} does not match keyed outcomes "
            f"{sorted(tagged_outcomes)}"
        )
    if not any(module in modules for modules, _, _, _ in tags):
        result.fail(f"quiz key never tags an item to its own module {module}")
    for line in malformed:
        result.fail(f"quiz key has a malformed tag line: {line[:80]}")
    if sum(QUIZ_POINTS) != 12:
        result.fail("internal error: quiz point blueprint does not total 12")
    result.checks += 4
    return result


def expand_modules(value: str) -> set[str]:
    modules: set[str] = set()
    for start, end in re.findall(r"M(\d{2})\s*[–-]\s*M(\d{2})", value):
        modules.update(f"M{number:02d}" for number in range(int(start), int(end) + 1))
    stripped = re.sub(r"M\d{2}\s*[–-]\s*M\d{2}", "", value)
    modules.update(re.findall(r"M\d{2}", stripped))
    return modules


def validate_level_check(level: int) -> AssessmentResult:
    name = f"LC-{level}"
    page = DOCS_ASSESSMENTS / "level-checks" / f"lc-{level}.md"
    key = KEYS_ROOT / "level-checks" / f"lc-{level}-key.md"
    relative_key = key.relative_to(REPO_ROOT).as_posix()
    result = AssessmentResult(name=name, path=page.relative_to(REPO_ROOT).as_posix())
    if not page.exists() or not key.exists():
        result.fail("missing student page or answer key")
        return result
    text = page.read_text(encoding="utf-8")
    key_text = key.read_text(encoding="utf-8")
    metadata = parse_metadata(text)
    require_metadata(
        result, metadata, ["Level", "Modules", "Items", "Points", "Time guide", "Pass", "Outcomes", "Answer key"]
    )
    if metadata.get("Items") != "10":
        result.fail(f"Items is {metadata.get('Items')!r}, expected '10'")
    if metadata.get("Points") != "20":
        result.fail(f"Points is {metadata.get('Points')!r}, expected '20'")
    if metadata.get("Pass") != "16/20":
        result.fail(f"Pass is {metadata.get('Pass')!r}, expected '16/20'")
    modules = expand_modules(metadata.get("Modules", ""))
    expected_modules = set(LEVEL_MODULES[level])
    if modules != expected_modules:
        result.fail(f"Modules are {sorted(modules)}, expected {sorted(expected_modules)}")
    validate_answer_key_path(result, metadata, relative_key)
    outcomes = set(re.findall(r"LO-\d{2}", metadata.get("Outcomes", "")))
    validate_item_pairs(
        result,
        numbered_sections(text, "## "),
        numbered_sections(key_text, "## "),
        key_text,
        10,
        "level check",
    )
    tags, malformed = key_tags(key_text)
    check_tag_membership(result, tags, modules, outcomes)
    tagged_outcomes = {outcome for _, outcomes_, _, _ in tags for outcome in outcomes_}
    if tagged_outcomes != outcomes:
        result.fail(
            f"Outcomes metadata {sorted(outcomes)} does not match keyed outcomes "
            f"{sorted(tagged_outcomes)}"
        )
    for line in malformed:
        result.fail(f"level-check key has a malformed tag line: {line[:80]}")
    if sum(LEVEL_CHECK_POINTS) != 20:
        result.fail("internal error: level-check point blueprint does not total 20")
    result.checks += 4
    return result


def validate_final() -> AssessmentResult:
    page = DOCS_ASSESSMENTS / "final-assessment" / "index.md"
    key = KEYS_ROOT / "final-assessment-key.md"
    result = AssessmentResult(name="FIN-01", path=page.relative_to(REPO_ROOT).as_posix())
    if not page.exists() or not key.exists():
        result.fail("missing student page or answer key")
        return result
    text = page.read_text(encoding="utf-8")
    key_text = key.read_text(encoding="utf-8")
    metadata = parse_metadata(text)
    require_metadata(result, metadata, ["Assessment", "Covers", "Items", "Points", "Time guide", "Pass", "Outcomes sampled", "Answer key"])
    if metadata.get("Items") != "25":
        result.fail(f"Items is {metadata.get('Items')!r}, expected '25'")
    if metadata.get("Points") != "100":
        result.fail(f"Points is {metadata.get('Points')!r}, expected '100'")
    if metadata.get("Pass") != "80/100":
        result.fail(f"Pass is {metadata.get('Pass')!r}, expected '80/100'")
    validate_answer_key_path(result, metadata, key.relative_to(REPO_ROOT).as_posix())
    outcomes = set(re.findall(r"LO-\d{2}", metadata.get("Outcomes sampled", "")))
    if not outcomes:
        result.fail("Outcomes sampled lists no LO identifiers")
    parts = re.findall(r"^## Part ([A-E]) — .*?20 points", text, re.MULTILINE)
    if parts != ["A", "B", "C", "D", "E"]:
        result.fail(f"final parts are {parts}, expected A–E")
    validate_item_pairs(
        result,
        numbered_sections(text, "### "),
        numbered_sections(key_text, "## "),
        key_text,
        25,
        "final",
    )
    tags, malformed = key_tags(key_text)
    check_tag_membership(result, tags, set(MODULES), outcomes)
    tagged_outcomes = {outcome for _, outcomes_, _, _ in tags for outcome in outcomes_}
    if tagged_outcomes != outcomes:
        result.fail(
            f"Outcomes sampled {sorted(outcomes)} does not match keyed outcomes "
            f"{sorted(tagged_outcomes)}"
        )
    for line in malformed:
        result.fail(f"final key has a malformed tag line: {line[:80]}")
    result.checks += 4
    return result


def validate_diagnostic() -> AssessmentResult:
    page = DOCS_ASSESSMENTS / "diagnostic" / "index.md"
    key = KEYS_ROOT / "diagnostic-key.md"
    result = AssessmentResult(name="DIA-01", path=page.relative_to(REPO_ROOT).as_posix())
    if not page.exists() or not key.exists():
        result.fail("missing student page or answer key")
        return result
    text = page.read_text(encoding="utf-8")
    key_text = key.read_text(encoding="utf-8")
    metadata = parse_metadata(text)
    require_metadata(result, metadata, ["ID", "Items", "Points", "Time guide", "Pass for course readiness", "Modules", "Outcomes", "Answer key"])
    if metadata.get("Items") != "20" or metadata.get("Points") != "20 (1 per item)":
        result.fail("diagnostic Items/Points metadata does not match 20 items at 1 point")
    if metadata.get("Pass for course readiness") != "14/20":
        result.fail("diagnostic pass mark is not 14/20")
    validate_answer_key_path(result, metadata, key.relative_to(REPO_ROOT).as_posix())
    items = [int(number) for number in re.findall(r"^\*\*(\d+)\. \[", text, re.MULTILINE)]
    if items != list(range(1, 21)):
        result.fail(f"diagnostic items are {items}, expected 1..20")
    key_sections = numbered_sections(key_text, "### ")
    if sorted(key_sections) != list(range(1, 21)):
        result.fail(f"diagnostic key items are {sorted(key_sections)}, expected 1..20")
    tags, malformed = key_tags(key_text)
    if len(tags) + len(malformed) != 20:
        result.fail(f"diagnostic key has {len(tags) + len(malformed)} tags, expected 20")
    outcomes = set(re.findall(r"LO-\d{2}", metadata.get("Outcomes", "")))
    check_tag_membership(result, tags, {"PRE"} | set(MODULES[:5]), outcomes)
    tagged_outcomes = {outcome for _, outcomes_, _, _ in tags for outcome in outcomes_}
    if tagged_outcomes != outcomes:
        result.fail(
            f"Outcomes metadata {sorted(outcomes)} does not match keyed outcomes "
            f"{sorted(tagged_outcomes)}"
        )
    for line in malformed:
        result.fail(f"diagnostic key has a malformed tag line: {line[:80]}")
    result.checks += 4
    return result


def bank_sections(text: str) -> dict[str, dict[str, object]]:
    pattern = re.compile(r"^## Section ([A-E]) — .*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    sections: dict[str, dict[str, object]] = {}
    for position, match in enumerate(matches):
        start = match.end()
        end = matches[position + 1].start() if position + 1 < len(matches) else len(text)
        block = text[start:end]
        declared = re.search(r"\*\*(\d+) items? · (\d+) points?\.\*\*", block)
        types: dict[str, int] = {"mcq": 0, "tf": 0, "short": 0, "scenario": 0}
        for heading, kind in [
            ("Multiple-choice", "mcq"),
            ("True/false", "tf"),
            ("Short answer", "short"),
            ("Scenario", "scenario"),
        ]:
            sub = re.search(rf"^### {heading}[^\n]*$", block, re.MULTILINE)
            if not sub:
                continue
            next_heading = re.search(r"^### ", block[sub.end():], re.MULTILINE)
            body = block[sub.end(): sub.end() + next_heading.start()] if next_heading else block[sub.end():]
            types[kind] = len(re.findall(r"^\*\*[A-E]\d+\.\*\*", body, re.MULTILINE))
        sections[match.group(1)] = {
            "declared": (int(declared.group(1)), int(declared.group(2))) if declared else None,
            "counts": types,
        }
    return sections


def validate_bank() -> AssessmentResult:
    page = DOCS_ASSESSMENTS / "question-bank" / "index.md"
    key = KEYS_ROOT / "question-bank-key.md"
    result = AssessmentResult(name="QB-01", path=page.relative_to(REPO_ROOT).as_posix())
    if not page.exists() or not key.exists():
        result.fail("missing student page or answer key")
        return result
    text = page.read_text(encoding="utf-8")
    key_text = key.read_text(encoding="utf-8")
    metadata = parse_metadata(text)
    require_metadata(result, metadata, ["Coverage", "Items", "Points", "Answer key"])
    if metadata.get("Items") != "56 (24 multiple-choice, 12 true/false, 12 short answer, 8 scenario)":
        result.fail("question bank Items metadata does not declare 56 items by type")
    if metadata.get("Points") != "92":
        result.fail(f"Points is {metadata.get('Points')!r}, expected '92'")
    validate_answer_key_path(result, metadata, key.relative_to(REPO_ROOT).as_posix())
    labels = re.findall(r"^\*\*([A-E]\d+)\.\*\*", text, re.MULTILINE)
    if len(labels) != 56 or len(set(labels)) != 56:
        result.fail(f"question bank has {len(labels)} item labels ({len(set(labels))} unique), expected 56")
    key_labels = re.findall(r"^### ([A-E]\d+) — ", key_text, re.MULTILINE)
    if key_labels != labels:
        result.fail("question bank key labels do not match the student page in order")
    tags, malformed = key_tags(key_text)
    if len(tags) + len(malformed) != 56:
        result.fail(f"question bank key has {len(tags) + len(malformed)} tags, expected 56")
    check_tag_membership(result, tags, set(MODULES))
    for line in malformed:
        result.fail(f"question bank key has a malformed tag line: {line[:80]}")
    sections = bank_sections(text)
    if sorted(sections) != ["A", "B", "C", "D", "E"]:
        result.fail(f"question bank sections are {sorted(sections)}, expected A–E")
    totals = {"mcq": 0, "tf": 0, "short": 0, "scenario": 0}
    points = 0
    weights = {"mcq": 1, "tf": 1, "short": 2, "scenario": 4}
    for label, data in sorted(sections.items()):
        declared = data["declared"]
        counts = data["counts"]
        assert isinstance(counts, dict)
        item_total = sum(counts.values())
        point_total = sum(counts[kind] * weights[kind] for kind in counts)
        for kind in counts:
            totals[kind] += counts[kind]
        points += point_total
        if declared is None:
            result.fail(f"Section {label} has no 'N items · P points' declaration")
        elif declared != (item_total, point_total):
            result.fail(
                f"Section {label} declares {declared[0]} items/{declared[1]} points "
                f"but contains {item_total}/{point_total}"
            )
    if totals != {"mcq": 24, "tf": 12, "short": 12, "scenario": 8}:
        result.fail(f"question bank item mix is {totals}, expected 24/12/12/8")
    if points != 92:
        result.fail(f"question bank points total {points}, expected 92")
    result.checks += 6
    return result


def rubric_weight_sum(path: Path) -> int:
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        cells = split_row(line)
        if cells != ["Dimension", "Weight"] and not (
            cells and cells[:2] == ["Dimension", "Weight"]
        ):
            continue
        total = 0
        for row in lines[index + 2 :]:
            row_cells = split_row(row)
            if not row_cells or len(row_cells) < 2:
                break
            if not row_cells[1].isdigit():
                break
            total += int(row_cells[1])
        return total
    return 0


def validate_rubrics() -> AssessmentResult:
    result = AssessmentResult(name="Rubrics", path="docs/assessments/rubrics")
    lab = DOCS_ASSESSMENTS / "rubrics" / "lab-rubric.md"
    capstone = DOCS_ASSESSMENTS / "rubrics" / "capstone-rubric.md"
    project = DOCS_ASSESSMENTS / "rubrics" / "project-rubric.md"
    checklists = DOCS_ASSESSMENTS / "rubrics" / "lab-completion-checklists.md"
    for path in (lab, capstone, project, checklists):
        if not path.exists():
            result.fail(f"missing {path.relative_to(REPO_ROOT).as_posix()}")
    if result.errors:
        return result
    for path, expected in ((lab, 100), (capstone, 100), (project, 100)):
        total = rubric_weight_sum(path)
        if total != expected:
            result.fail(f"{path.name} dimension weights total {total}, expected {expected}")
    lab_text = lab.read_text(encoding="utf-8")
    for dimension in ("R1", "R2", "R3", "R4", "R5"):
        if f"### {dimension} —" not in lab_text:
            result.fail(f"lab rubric has no descriptor section for {dimension}")
    capstone_text = capstone.read_text(encoding="utf-8")
    if "Automatic fail" not in capstone_text:
        result.fail("capstone rubric has no automatic-fail section")
    checklist_text = checklists.read_text(encoding="utf-8")
    for lab_id in LAB_IDS:
        if not re.search(rf"^## {re.escape(lab_id)}\b", checklist_text, re.MULTILINE):
            result.fail(f"completion checklists have no section for {lab_id}")
    result.checks += 6
    return result


def validate_progress() -> AssessmentResult:
    page = DOCS_ASSESSMENTS / "progress-and-reflection.md"
    result = AssessmentResult(name="Progress", path=page.relative_to(REPO_ROOT).as_posix())
    if not page.exists():
        result.fail("missing progress and reflection page")
        return result
    text = page.read_text(encoding="utf-8")
    for module in MODULES:
        if not re.search(rf"\b{module}\b", text):
            result.fail(f"progress record does not mention {module}")
    for level in range(1, 6):
        if not re.search(rf"\bLC-{level}\b", text):
            result.fail(f"progress record does not mention LC-{level}")
    if "ethics" not in text.lower():
        result.fail("progress record has no ethics statement")
    result.checks += 3
    return result


def validate_widget() -> AssessmentResult:
    js_path = REPO_ROOT / "docs" / "javascripts" / "self-check.js"
    page = DOCS_ASSESSMENTS / "practice.md"
    result = AssessmentResult(name="Practice widget", path="docs/assessments/practice.md")
    if not js_path.exists() or not page.exists():
        result.fail("missing widget script or practice page")
        return result
    script = js_path.read_text(encoding="utf-8")
    blocks = re.split(r'\n    \{\n      id: "', script)[1:]
    if len(blocks) != 10:
        result.fail(f"widget defines {len(blocks)} questions, expected 10")
    ids = re.findall(r'id: "([^"]+)"', script)
    if len(set(ids)) != len(ids):
        result.fail("widget question ids are not unique")
    for index, block in enumerate(blocks, start=1):
        answer = re.search(r"answer: (\d+),", block)
        options = len(re.findall(r'\{ text: "', block))
        if options != 4:
            result.fail(f"widget item {index} has {options} options, expected 4")
        if not answer or not 0 <= int(answer.group(1)) < options:
            result.fail(f"widget item {index} has an out-of-range answer index")
        if not re.search(r"note: \"", block):
            result.fail(f"widget item {index} has no option explanation")
        if not re.search(r'why:\s*"', block):
            result.fail(f"widget item {index} has no rationale")
    page_text = page.read_text(encoding="utf-8")
    if "ten items" not in page_text.lower():
        result.fail("practice page does not state the item count")
    if "not protected in the source" not in page_text:
        result.fail("practice page does not disclose that the source contains answers")
    result.checks += 3
    return result


def duplicate_stems() -> list[str]:
    stems: dict[str, str] = {}
    duplicates: list[str] = []
    sources = list((DOCS_ASSESSMENTS / "module-quizzes").glob("qz-*.md"))
    sources += list((DOCS_ASSESSMENTS / "level-checks").glob("lc-*.md"))
    sources += [
        DOCS_ASSESSMENTS / "diagnostic" / "index.md",
        DOCS_ASSESSMENTS / "final-assessment" / "index.md",
        DOCS_ASSESSMENTS / "question-bank" / "index.md",
    ]
    for path in sources:
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(
            r"^(?:## \d+\.\s+|\*\*[0-9A-E]+\.[\*\s]+)(.+)$", text, re.MULTILINE
        ):
            stem = re.sub(r"[^a-z0-9 ]", " ", match.group(1).lower())
            stem = re.sub(r"\s+", " ", stem).strip()
            if len(stem) < 25:
                continue
            key = stem[:160]
            if key in stems and stems[key] != path.name:
                duplicates.append(f"duplicate stem in {path.name} and {stems[key]}: {match.group(1)[:70]}")
            stems.setdefault(key, path.name)
    return duplicates


def validate_globals() -> tuple[list[str], list[str], int]:
    errors: list[str] = []
    warnings: list[str] = []
    checks = 0
    for relative in REQUIRED_FILES:
        if not (REPO_ROOT / relative).exists():
            errors.append(f"missing repository file {relative}")
        else:
            checks += 1

    if (DOCS_ASSESSMENTS / "answer-keys").exists():
        errors.append("docs/assessments/answer-keys exists; keys must stay outside the MkDocs build")
    leaked = [
        path.relative_to(REPO_ROOT).as_posix()
        for path in DOCS_ASSESSMENTS.rglob("*-key.md")
    ]
    if leaked:
        errors.append(f"key files found under docs/: {', '.join(leaked)}")

    mkdocs_text = MKdocs.read_text(encoding="utf-8") if MKdocs.exists() else ""
    for entry in NAV_ENTRIES:
        if entry not in mkdocs_text:
            errors.append(f"mkdocs.yml nav does not include {entry}")
    for asset in ("stylesheets/self-check.css", "javascripts/self-check.js"):
        if asset not in mkdocs_text:
            errors.append(f"mkdocs.yml does not reference {asset}")
    if "answer-keys" in mkdocs_text:
        errors.append("mkdocs.yml references answer-keys")
    for pattern in ("/assessments/module-quizzes/qz-*.md", "/assessments/level-checks/lc-*.md"):
        if pattern not in mkdocs_text:
            errors.append(f"not_in_nav does not exclude {pattern}")
    checks += len(NAV_ENTRIES) + 3

    index_texts = {
        "module-quizzes": (DOCS_ASSESSMENTS / "module-quizzes" / "index.md").read_text(encoding="utf-8"),
        "level-checks": (DOCS_ASSESSMENTS / "level-checks" / "index.md").read_text(encoding="utf-8"),
    }
    for module in MODULES:
        identifier = f"QZ-{module[1:]}B"
        if identifier not in index_texts["module-quizzes"]:
            errors.append(f"module quiz index does not list {identifier}")
    for level in range(1, 6):
        if f"LC-{level}" not in index_texts["level-checks"]:
            errors.append(f"level-check index does not list LC-{level}")
    checks += 24

    for path in DOCS_ASSESSMENTS.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"assessments/answer-keys/[A-Za-z0-9_./-]+\.md", text):
            if not (REPO_ROOT / target).exists():
                errors.append(f"{path.relative_to(REPO_ROOT).as_posix()} names missing key {target}")
        for issue in check_links.check_file(path):
            errors.append(
                f"{issue.source}:{issue.line}: broken link {issue.target} ({issue.reason})"
            )
    checks += 1

    for message in duplicate_stems():
        errors.append(message)

    return errors, warnings, checks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the ML-Sec assessment package.")
    parser.add_argument("--json", type=Path, default=None)
    parser.add_argument("--strict-warnings", action="store_true")
    args = parser.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    results: list[AssessmentResult] = []
    results.extend(validate_quiz(module) for module in MODULES)
    results.extend(validate_level_check(level) for level in range(1, 6))
    results.append(validate_diagnostic())
    results.append(validate_bank())
    results.append(validate_final())
    results.append(validate_rubrics())
    results.append(validate_progress())
    results.append(validate_widget())

    global_errors, global_warnings, global_checks = validate_globals()

    failed = [result for result in results if not result.ok]
    for result in results:
        status = "PASS" if result.ok else "FAIL"
        suffix = f", {len(result.warnings)} warning(s)" if result.warnings else ""
        print(f"{result.name:<9} {status}  {result.checks} checks{suffix}")
        for error in result.errors:
            print(f"  FAIL {error}")
        for warning in result.warnings:
            print(f"  WARN {warning}")
    for error in global_errors:
        print(f"GLOBAL FAIL {error}")
    for warning in global_warnings:
        print(f"GLOBAL WARN {warning}")

    ok = not failed and not global_errors
    print(
        f"\nSummary: {len(results)} assessments checked, {len(failed)} failed; "
        f"{global_checks} global checks, {len(global_errors)} global failures, "
        f"{len(global_warnings)} global warnings"
    )
    if args.strict_warnings and (global_warnings or any(result.warnings for result in results)):
        ok = False
        print("Strict warnings enabled: warnings count as failure")

    if args.json:
        payload = {
            "python": sys.version.split()[0],
            "assessments": [
                {
                    "name": result.name,
                    "path": result.path,
                    "status": "pass" if result.ok else "fail",
                    "checks": result.checks,
                    "errors": result.errors,
                    "warnings": result.warnings,
                }
                for result in results
            ],
            "global_errors": global_errors,
            "global_warnings": global_warnings,
            "global_checks": global_checks,
            "status": "pass" if ok else "fail",
        }
        args.json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"JSON summary written to {args.json}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
