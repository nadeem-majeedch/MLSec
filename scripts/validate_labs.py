"""Validate every practical lab in the ML-Sec repository.

Structural checks run by default and make no network calls:

* lab discovery and required package files
* README metadata table and brief metadata line
* consistency between README, brief, catalog, lab index, and MkDocs nav
* required brief and README sections
* starter TODO markers and starter/solution separation
* checker independence from the reference solution
* Python compilation and an import allowlist
* expected-result JSON and pinned requirements
* internal Markdown links and local assets
* notebook JSON structure
* repository policy files and committed-binary hygiene

Optional checks:

    python scripts/validate_labs.py --execute --timeout 600
    python scripts/validate_labs.py --check-urls --timeout 10
    python scripts/validate_labs.py --json lab-validation.json

``--execute`` runs each reference solution into a temporary directory and then
runs that lab's checker. It never runs ``starter.py`` and never writes into the
repository. ``--check-urls`` probes external HTTP(S) links and is off by default.

Exit code 0 means all enabled checks passed. Structural failures, execution
failures, and (when enabled) URL failures return 1.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_links  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
LABS_ROOT = REPO_ROOT / "labs"
SHARED_REQUIREMENTS = LABS_ROOT / "shared" / "requirements-level1.txt"
THIRD_PARTY_ALLOWLIST = {"numpy", "pandas", "sklearn", "joblib", "yaml"}
SUPPORTED_PYTHON = "3.14.7"

README_FIELDS = [
    "Lab ID",
    "Tier",
    "Time",
    "Difficulty",
    "Module",
    "Outcomes",
    "Prerequisites",
    "Data",
    "Compute",
]
README_SECTIONS = [
    "Scenario",
    "Run",
    "What you produce",
    "Starter and TODO map",
    "Hints",
    "Files",
    "Safety and cleanup",
]
BRIEF_SECTIONS: list[tuple[str, list[str]]] = [
    ("purpose", ["Why this lab exists"]),
    ("scenario", ["What you build", "What you produce"]),
    ("threat model", ["Threat model, scope, and safety", "The system and the threat model"]),
    ("prerequisites", ["Prerequisites"]),
    ("environment", ["Environment", "Data and environment"]),
    ("task specification", ["Task specification"]),
    ("starter map", ["Starter and TODO map"]),
    ("expected observations", ["Expected outputs", "Expected results", "Reference results", "Scenarios and expected outcomes"]),
    ("deliverables", ["Deliverables checklist"]),
    ("success criteria", ["Success criteria"]),
    ("checking", ["How to check yourself"]),
    ("reflection", ["Reflection questions"]),
    ("hints", ["Hints"]),
    ("time box", ["Time box"]),
    ("troubleshooting", ["Troubleshooting"]),
    ("rubric", ["Rubric", "Rubric (20 points)"]),
    ("cleanup", ["Cleanup"]),
    ("references", ["References"]),
    ("next", ["What comes next"]),
]
BINARY_SUFFIXES = {".joblib", ".pkl", ".pickle", ".npz", ".npy", ".h5", ".pt", ".pth", ".onnx"}
CATALOG_PATH = REPO_ROOT / "docs" / "lab-catalog.md"


@dataclass
class LabResult:
    lab_id: str
    directory: str
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


@dataclass
class ExecutionStep:
    name: str
    command: list[str]
    exit_code: int | None
    seconds: float
    detail: str = ""


@dataclass
class ExecutionResult:
    lab_id: str
    status: str
    steps: list[ExecutionStep] = field(default_factory=list)


def split_table_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    cells = [cell.strip() for cell in stripped[1:-1].split("|")]
    if not cells or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
        return None
    return cells


def parse_readme_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("## "):
            break
        cells = split_table_row(line)
        if not cells or len(cells) < 2 or cells[0] in {"Field", "---"}:
            continue
        metadata[cells[0]] = cells[1]
    return metadata


def parse_brief_metadata(text: str) -> dict[str, object] | None:
    match = re.search(
        r"\*\*Tier ([ABC]) · (\d+) hours? · Difficulty ([1-5]) · Modules? (.+?) · Outcomes (.+?)\*\*",
        text,
    )
    if not match:
        return None
    return {
        "tier": match.group(1),
        "hours": int(match.group(2)),
        "difficulty": int(match.group(3)),
        "module": match.group(4).strip(),
        "outcomes": [item.strip() for item in match.group(5).split(",") if item.strip()],
    }


def heading_list(text: str) -> list[str]:
    return re.findall(r"^## +(.+?)\s*$", check_links.strip_code(text), flags=re.MULTILINE)


def section_body(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == f"## {heading}":
            start = index + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end])


def lab_id_from_dir(path: Path) -> str:
    match = re.match(r"lab-(\d+)([a-z]?)(?:-|$)", path.name)
    if not match:
        return path.name.upper()
    number, suffix = match.groups()
    return f"LAB-{number}{suffix.upper()}"


def lab_sort_key(lab_id: str) -> tuple[int, str]:
    match = re.match(r"LAB-(\d+)([A-Z]?)", lab_id)
    return (int(match.group(1)), match.group(2)) if match else (999, "")


def discover_labs(root: Path = LABS_ROOT) -> list[Path]:
    labs = [
        path
        for path in root.iterdir()
        if path.is_dir() and path.name.startswith("lab-") and path.name != "lab-shared"
    ]
    return sorted(labs, key=lambda path: lab_sort_key(lab_id_from_dir(path)))


def catalog_entries(path: Path = CATALOG_PATH) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?ms)^## 2\. Summary\s*$(.*?)(?=^## |\Z)", text)
    block = match.group(1) if match else text
    entries: dict[str, dict[str, str]] = {}
    header: list[str] | None = None
    for line in block.splitlines():
        cells = split_table_row(line)
        if not cells:
            continue
        if cells[0] == "ID":
            header = cells
            continue
        if header and re.fullmatch(r"LAB-\d+[A-Z]?", cells[0]) and len(cells) == len(header):
            entries[cells[0]] = dict(zip(header, cells))
    return entries


def iter_python_imports(source: str) -> set[str]:
    tree = ast.parse(source)
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            modules.add(node.module.split(".")[0])
    return modules


def check_notebook(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [f"{path.name}: invalid notebook JSON ({exc})"]
    if not isinstance(data, dict):
        return [f"{path.name}: notebook root is not an object"]
    if not isinstance(data.get("nbformat"), int):
        errors.append(f"{path.name}: missing integer nbformat")
    cells = data.get("cells")
    if not isinstance(cells, list) or not cells:
        errors.append(f"{path.name}: missing or empty cells list")
        return errors
    for index, cell in enumerate(cells):
        if not isinstance(cell, dict):
            errors.append(f"{path.name}: cell {index} is not an object")
            continue
        if cell.get("cell_type") not in {"code", "markdown", "raw"}:
            errors.append(f"{path.name}: cell {index} has invalid cell_type")
        source = cell.get("source")
        if not (isinstance(source, str) or (isinstance(source, list) and all(isinstance(s, str) for s in source))):
            errors.append(f"{path.name}: cell {index} has invalid source")
        if cell.get("cell_type") == "code" and not isinstance(cell.get("outputs"), list):
            errors.append(f"{path.name}: code cell {index} has no outputs list")
    return errors


def check_requirements(path: Path, label: str, result: LabResult) -> None:
    if not path.exists():
        result.fail(f"missing {label}")
        return
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("-r "):
            included = (path.parent / line[3:].strip()).resolve()
            if not included.exists():
                result.fail(f"{label}:{number} includes missing file {line[3:].strip()}")
            continue
        if not re.fullmatch(r"[A-Za-z0-9_.-]+==[^=\s]+", line):
            result.fail(f"{label}:{number} is not pinned with ==: {line}")


def check_required_files(lab: Path, lab_id: str, result: LabResult) -> dict[str, Path]:
    checker = "check_threat_model.py" if lab_id == "LAB-02" else f"check_lab{lab_id[4:].lower()}.py"
    if lab_id == "LAB-02":
        names = [
            "README.md",
            "CHECKING.md",
            "requirements.txt",
            "report_template.md",
            "threat-model.yaml",
            "report.md",
            "solution.yaml",
            "solution-report.md",
            "expected_summary.json",
            checker,
        ]
    else:
        names = [
            "README.md",
            "CHECKING.md",
            "requirements.txt",
            "starter.py",
            "solution.py",
            "expected_metrics.json",
            checker,
        ]
        if (lab / "report_template.md").exists():
            names.append("report_template.md")
    paths = {name: lab / name for name in names}
    for name, path in paths.items():
        if not path.exists():
            result.fail(f"missing required file {name}")
        elif path.stat().st_size == 0:
            result.fail(f"required file is empty: {name}")
    if lab_id == "LAB-01B" and not (lab / "make_dataset.py").exists():
        result.fail("missing required file make_dataset.py")
    if lab_id == "LAB-12" and not (lab / "dataset.py").exists():
        result.fail("missing required file dataset.py")
    if lab_id == "LAB-13" and not (lab / "project.py").exists():
        result.fail("missing required file project.py")
    return paths


def check_readme(lab: Path, lab_id: str, brief_path: Path, result: LabResult) -> dict[str, str]:
    readme = lab / "README.md"
    if not readme.exists():
        return {}
    text = readme.read_text(encoding="utf-8")
    result.checks += 1
    first_line = text.splitlines()[0] if text else ""
    if lab_id not in first_line:
        result.fail(f"README H1 does not contain {lab_id}")
    metadata = parse_readme_metadata(text)
    for field_name in README_FIELDS:
        if not metadata.get(field_name):
            result.fail(f"README metadata missing '{field_name}'")
    if metadata.get("Lab ID") and metadata["Lab ID"] != lab_id:
        result.fail(f"README Lab ID {metadata['Lab ID']} does not match directory {lab_id}")
    if metadata.get("Tier") not in {"A", "B", "C"}:
        result.fail(f"README Tier must be A, B, or C (got {metadata.get('Tier')!r})")
    time_match = re.fullmatch(r"(\d+) hours?", metadata.get("Time", ""))
    if not time_match:
        result.fail(f"README Time must look like '4 hours' (got {metadata.get('Time')!r})")
    difficulty_match = re.fullmatch(r"([1-5]) of [45]", metadata.get("Difficulty", ""))
    if not difficulty_match:
        result.fail(f"README Difficulty must look like '3 of 4' (got {metadata.get('Difficulty')!r})")
    outcomes = re.findall(r"LO-\d+", metadata.get("Outcomes", ""))
    if not outcomes:
        result.fail("README Outcomes has no LO identifiers")
    if "LO-28" not in outcomes:
        result.fail("README Outcomes does not include LO-28")
    headings = heading_list(text)
    for section in README_SECTIONS:
        if section not in headings:
            result.fail(f"README missing section '## {section}'")
    if brief_path.exists() and brief_path.name not in text:
        result.fail(f"README does not reference its brief {brief_path.name}")
    if "CHECKING.md" not in text:
        result.fail("README does not reference CHECKING.md")
    if "CPU" not in metadata.get("Compute", ""):
        result.warn("README Compute does not state CPU-only execution")
    return metadata


def check_brief(lab_id: str, brief_path: Path, result: LabResult) -> dict[str, object] | None:
    if not brief_path.exists():
        result.fail(f"missing brief {brief_path.relative_to(REPO_ROOT).as_posix()}")
        return None
    text = brief_path.read_text(encoding="utf-8")
    result.checks += 1
    first_line = text.splitlines()[0] if text else ""
    if lab_id not in first_line:
        result.fail(f"brief H1 does not contain {lab_id}")
    metadata = parse_brief_metadata(text)
    if metadata is None:
        result.fail("brief metadata line is missing or malformed")
    headings = heading_list(text)
    for label, variants in BRIEF_SECTIONS:
        if not any(variant in headings for variant in variants):
            result.fail(f"brief missing section for {label} (expected one of {variants})")
    deliverables = section_body(text, "Deliverables checklist")
    if len(re.findall(r"^\s*- \[ \]", deliverables, flags=re.MULTILINE)) < 1:
        result.fail("brief Deliverables checklist has no '- [ ]' items")
    if deliverables and "report.md" not in deliverables:
        result.fail("brief Deliverables checklist does not mention report.md")
    task = section_body(text, "Task specification")
    if len(re.findall(r"^\s*\d+\.\s", task, flags=re.MULTILINE)) < 3:
        result.fail("brief Task specification has fewer than three numbered tasks")
    reflection = section_body(text, "Reflection questions")
    if len(re.findall(r"^\s*\d+\.\s", reflection, flags=re.MULTILINE)) < 2:
        result.fail("brief Reflection questions has fewer than two numbered questions")
    hints = section_body(text, "Hints")
    if len(re.findall(r"^\s*(?:[-*]|\d+\.)\s", hints, flags=re.MULTILINE)) < 2:
        result.fail("brief Hints has fewer than two items")
    troubleshooting = section_body(text, "Troubleshooting")
    table_rows = [
        line
        for line in troubleshooting.splitlines()
        if line.strip().startswith("|") and not re.fullmatch(r"\|[\s:|-]+\|", line.strip())
    ]
    if len(table_rows) < 3:
        result.fail("brief Troubleshooting needs a table with at least two data rows")
    references = section_body(text, "References")
    if not re.search(r"\[[^\]]+\]\([^)]+\)", references):
        result.fail("brief References has no Markdown links")
    return metadata


def check_metadata_consistency(
    lab_id: str,
    readme: dict[str, str],
    brief: dict[str, object] | None,
    catalog: dict[str, str] | None,
    result: LabResult,
) -> None:
    if not readme or brief is None:
        return
    if readme.get("Tier") != brief["tier"]:
        result.fail(f"tier mismatch: README {readme.get('Tier')} vs brief {brief['tier']}")
    time_match = re.fullmatch(r"(\d+) hours?", readme.get("Time", ""))
    if time_match and int(time_match.group(1)) != brief["hours"]:
        result.fail(f"hours mismatch: README {time_match.group(1)} vs brief {brief['hours']}")
    difficulty_match = re.fullmatch(r"([1-5]) of [45]", readme.get("Difficulty", ""))
    if difficulty_match and int(difficulty_match.group(1)) != brief["difficulty"]:
        result.fail(
            f"difficulty mismatch: README {difficulty_match.group(1)} vs brief {brief['difficulty']}"
        )
    readme_module = readme.get("Module", "").split(" — ")[0].strip()
    if readme_module != brief["module"]:
        result.fail(f"module mismatch: README {readme_module!r} vs brief {brief['module']!r}")
    readme_outcomes = re.findall(r"LO-\d+", readme.get("Outcomes", ""))
    brief_outcomes = re.findall(r"LO-\d+", " ".join(str(item) for item in brief["outcomes"]))
    if set(readme_outcomes) != set(brief_outcomes):
        result.fail(f"outcomes mismatch: README {readme_outcomes} vs brief {brief_outcomes}")

    if catalog is None:
        result.fail("lab is missing from docs/lab-catalog.md summary table")
        return
    if catalog.get("Tier") != readme.get("Tier"):
        result.fail(f"catalog tier {catalog.get('Tier')} != README {readme.get('Tier')}")
    if catalog.get("Difficulty") != str(brief["difficulty"]):
        result.fail(f"catalog difficulty {catalog.get('Difficulty')} != brief {brief['difficulty']}")
    if catalog.get("Hours") != str(brief["hours"]):
        result.fail(f"catalog hours {catalog.get('Hours')} != brief {brief['hours']}")
    if catalog.get("Module") != readme_module:
        result.fail(f"catalog module {catalog.get('Module')} != README {readme_module}")
    catalog_outcomes = re.findall(r"LO-\d+", catalog.get("Primary outcome", ""))
    if not set(catalog_outcomes) <= set(readme_outcomes):
        result.fail(f"catalog outcomes {catalog_outcomes} are not a subset of README {readme_outcomes}")
    if "LO-28" not in catalog_outcomes:
        result.fail("catalog primary outcome does not include LO-28")
    if catalog.get("Status") != "Built":
        result.warn(f"catalog status is {catalog.get('Status')!r}, not 'Built'")


def check_checker(lab: Path, lab_id: str, result: LabResult) -> None:
    checker = lab / ("check_threat_model.py" if lab_id == "LAB-02" else f"check_lab{lab_id[4:].lower()}.py")
    if not checker.exists():
        return
    text = checker.read_text(encoding="utf-8")
    result.checks += 1
    if re.search(r"(?m)^\s*(?:from|import)\s+(?:solution|starter)\b", text):
        result.fail(f"{checker.name} imports the reference or starter implementation")
    if lab_id == "LAB-02":
        if "--model" not in text or "--report" not in text:
            result.fail("LAB-02 checker does not accept --model and --report")
    else:
        if "--artifacts" not in text:
            result.fail(f"{checker.name} does not accept --artifacts")
        if "FAIL:" not in text:
            result.warn(f"{checker.name} does not print a FAIL: marker")
    if "checker" not in text.lower():
        result.warn(f"{checker.name} does not describe itself as an independent checker")


def check_starter(lab: Path, lab_id: str, result: LabResult) -> None:
    if lab_id == "LAB-02":
        learner_files = [lab / "threat-model.yaml", lab / "report.md"]
        markers = sum(
            path.read_text(encoding="utf-8").count("TODO") for path in learner_files if path.exists()
        )
        if markers == 0:
            result.fail("LAB-02 learner files contain no TODO markers")
        return
    starter = lab / "starter.py"
    solution = lab / "solution.py"
    if not starter.exists() or not solution.exists():
        return
    starter_text = starter.read_text(encoding="utf-8")
    if "TODO" not in starter_text:
        result.fail("starter.py contains no TODO marker")
    if starter.read_bytes() == solution.read_bytes():
        result.fail("starter.py is identical to solution.py")
    if "NotImplementedError" not in starter_text and "TODO" not in starter_text:
        result.warn("starter.py has neither TODO markers nor NotImplementedError")


def check_python(lab: Path, result: LabResult) -> None:
    local_modules = {path.stem for path in lab.glob("*.py")}
    for path in sorted(lab.rglob("*.py")):
        if any(part in {"__pycache__", ".venv"} for part in path.parts):
            continue
        source = path.read_bytes()
        try:
            compile(source, str(path), "exec")
        except SyntaxError as exc:
            result.fail(f"{path.name}:{exc.lineno}: syntax error: {exc.msg}")
            continue
        result.checks += 1
        try:
            modules = iter_python_imports(source.decode("utf-8"))
        except (UnicodeDecodeError, SyntaxError):
            continue
        for module in sorted(modules):
            if (
                module in sys.stdlib_module_names
                or module in THIRD_PARTY_ALLOWLIST
                or module in local_modules
                or module == "mlsec_labs"
            ):
                continue
            result.fail(f"{path.name}: undeclared import '{module}' (not stdlib, pinned stack, or local)")


def check_expected_json(lab: Path, lab_id: str, result: LabResult) -> None:
    name = "expected_summary.json" if lab_id == "LAB-02" else "expected_metrics.json"
    path = lab / name
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        result.fail(f"{name}: invalid JSON ({exc})")
        return
    if not isinstance(data, dict) or not data:
        result.fail(f"{name}: expected a non-empty JSON object")
    else:
        result.checks += 1


def check_checking(lab: Path, lab_id: str, result: LabResult) -> None:
    path = lab / "CHECKING.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    headings = heading_list(text)
    if f"# Checking Guide — {lab_id}" not in text:
        result.fail("CHECKING.md H1 is not '# Checking Guide — LAB-XX'")
    if not any(heading.startswith("Rubric") for heading in headings):
        result.fail("CHECKING.md has no Rubric section")
    if "Reflection questions" not in headings:
        result.fail("CHECKING.md has no Reflection questions section")


def check_links_for_lab(lab: Path, brief_path: Path, result: LabResult) -> None:
    paths = [lab / "README.md", lab / "CHECKING.md", brief_path]
    for path in paths:
        if not path.exists():
            continue
        for issue in check_links.check_file(path):
            result.fail(
                f"{issue.source}:{issue.line}: broken link {issue.target} ({issue.reason})"
            )


def validate_lab(
    lab: Path,
    brief_path: Path,
    catalog: dict[str, str] | None,
    *,
    check_markdown_links: bool = True,
) -> LabResult:
    lab_id = lab_id_from_dir(lab)
    result = LabResult(lab_id=lab_id, directory=lab.relative_to(REPO_ROOT).as_posix())
    paths = check_required_files(lab, lab_id, result)
    readme = check_readme(lab, lab_id, brief_path, result)
    brief = check_brief(lab_id, brief_path, result)
    check_metadata_consistency(lab_id, readme, brief, catalog, result)
    check_checker(lab, lab_id, result)
    check_starter(lab, lab_id, result)
    check_python(lab, result)
    check_expected_json(lab, lab_id, result)
    check_checking(lab, lab_id, result)
    check_requirements(lab / "requirements.txt", f"{lab.name}/requirements.txt", result)
    if check_markdown_links:
        check_links_for_lab(lab, brief_path, result)
    return result


def validate_repository(root: Path = REPO_ROOT, lab_filter: set[str] | None = None) -> list[LabResult]:
    labs_root = root / "labs"
    entries = catalog_entries(root / "docs" / "lab-catalog.md")
    results: list[LabResult] = []
    for lab in discover_labs(labs_root):
        lab_id = lab_id_from_dir(lab)
        if lab_filter and lab_id not in lab_filter and lab.name not in lab_filter:
            continue
        brief = root / "docs" / "labs" / f"lab-{lab_id[4:].lower()}.md"
        results.append(validate_lab(lab, brief, entries.get(lab_id)))
    return results


def check_repository_globals(root: Path = REPO_ROOT) -> tuple[list[str], list[str], int]:
    errors: list[str] = []
    warnings: list[str] = []
    checks = 0
    required = [
        ".python-version",
        "requirements/labs.txt",
        "requirements/README.md",
        "datasets/README.md",
        "datasets/synthetic/README.md",
        "labs/README.md",
        "docs/lab-authoring-guide.md",
        "docs/lab-template.md",
        "docs/references.md",
        "docs/labs/index.md",
        "mkdocs.yml",
    ]
    for relative in required:
        if not (root / relative).exists():
            errors.append(f"missing repository file {relative}")
        else:
            checks += 1

    version_path = root / ".python-version"
    if version_path.exists() and version_path.read_text(encoding="utf-8").strip() != SUPPORTED_PYTHON:
        errors.append(
            f".python-version is {version_path.read_text(encoding='utf-8').strip()!r}, "
            f"expected {SUPPORTED_PYTHON!r}"
        )

    if SHARED_REQUIREMENTS.exists():
        text = SHARED_REQUIREMENTS.read_text(encoding="utf-8")
        if f"Python {SUPPORTED_PYTHON}" not in text:
            warnings.append(f"shared requirements do not mention Python {SUPPORTED_PYTHON}")
        for number, raw in enumerate(text.splitlines(), start=1):
            line = raw.split("#", 1)[0].strip()
            if line and not re.fullmatch(r"[A-Za-z0-9_.-]+==[^=\s]+", line):
                errors.append(f"labs/shared/requirements-level1.txt:{number} is not pinned: {line}")
        checks += 1

    labs_txt = root / "requirements" / "labs.txt"
    if labs_txt.exists() and "labs/shared/requirements-level1.txt" not in labs_txt.read_text(
        encoding="utf-8"
    ):
        errors.append("requirements/labs.txt does not include labs/shared/requirements-level1.txt")
    else:
        checks += 1

    entries = catalog_entries(root / "docs" / "lab-catalog.md")
    labs_root = root / "labs"
    labs = discover_labs(labs_root)
    for lab in labs:
        lab_id = lab_id_from_dir(lab)
        if lab_id not in entries:
            errors.append(f"{lab_id} is missing from docs/lab-catalog.md")
        if lab_id not in (root / "docs" / "labs" / "index.md").read_text(encoding="utf-8"):
            errors.append(f"{lab_id} is missing from docs/labs/index.md")
        brief_rel = f"labs/lab-{lab_id[4:].lower()}.md"
        if brief_rel not in (root / "mkdocs.yml").read_text(encoding="utf-8"):
            errors.append(f"{lab_id} brief is missing from mkdocs.yml nav ({brief_rel})")
        if lab_id not in (root / "datasets" / "README.md").read_text(encoding="utf-8"):
            warnings.append(f"{lab_id} is not listed in datasets/README.md")
    checks += len(labs)

    for path in labs_root.rglob("*"):
        if path.is_file() and path.suffix.lower() in BINARY_SUFFIXES:
            errors.append(
                f"committed binary artifact under labs/: {path.relative_to(root).as_posix()}"
            )
        if path.name in {"artifacts", "data"} and path.is_dir():
            errors.append(
                f"generated output directory under labs/: {path.relative_to(root).as_posix()}"
            )

    notebooks = [
        path
        for path in root.rglob("*.ipynb")
        if not any(part in check_links.SKIP_DIRS for part in path.relative_to(root).parts)
    ]
    for notebook in notebooks:
        for message in check_notebook(notebook):
            errors.append(message)
    if notebooks:
        checks += len(notebooks)
    return errors, warnings, checks


def _environment() -> dict[str, str]:
    import os

    env = os.environ.copy()
    env.update(
        {
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUTF8": "1",
            "PYTHONHASHSEED": "0",
            "MPLBACKEND": "Agg",
            "OMP_NUM_THREADS": "2",
            "OPENBLAS_NUM_THREADS": "2",
        }
    )
    return env


def _run_step(name: str, command: list[str], cwd: Path, timeout: int) -> ExecutionStep:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            env=_environment(),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        elapsed = time.monotonic() - started
        output = (completed.stdout or "") + (completed.stderr or "")
        return ExecutionStep(
            name=name,
            command=command,
            exit_code=completed.returncode,
            seconds=elapsed,
            detail=output.strip()[-1200:],
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.monotonic() - started
        output = ""
        if exc.stdout:
            output += exc.stdout if isinstance(exc.stdout, str) else exc.stdout.decode("utf-8", "replace")
        if exc.stderr:
            output += exc.stderr if isinstance(exc.stderr, str) else exc.stderr.decode("utf-8", "replace")
        return ExecutionStep(
            name=name,
            command=command,
            exit_code=None,
            seconds=elapsed,
            detail=f"timeout after {timeout}s\n{output.strip()[-1000:]}",
        )
    except OSError as exc:
        return ExecutionStep(
            name=name,
            command=command,
            exit_code=None,
            seconds=time.monotonic() - started,
            detail=str(exc),
        )


def execute_lab(lab: Path, timeout: int, keep: Path | None = None) -> ExecutionResult:
    lab_id = lab_id_from_dir(lab)
    context: tempfile.TemporaryDirectory[str] | None = None
    if keep is None:
        context = tempfile.TemporaryDirectory(prefix=f"mlsec-{lab_id.lower()}-")
        artifacts = Path(context.name) / "artifacts"
    else:
        artifacts = keep / lab_id / "artifacts"
        artifacts.mkdir(parents=True, exist_ok=True)
    result = ExecutionResult(lab_id=lab_id, status="fail")
    python = sys.executable
    try:
        if lab_id == "LAB-02":
            step = _run_step(
                "checker",
                [python, "check_threat_model.py", "--model", "solution.yaml", "--report", "solution-report.md"],
                lab,
                timeout,
            )
            result.steps.append(step)
            result.status = "pass" if step.exit_code == 0 else "fail"
        else:
            if (lab / "make_dataset.py").exists():
                result.steps.append(
                    _run_step(
                        "make_dataset",
                        [python, "make_dataset.py", "--out", str(artifacts)],
                        lab,
                        timeout,
                    )
                )
            solution_step = _run_step(
                "solution", [python, "solution.py", "--out", str(artifacts)], lab, timeout
            )
            result.steps.append(solution_step)
            if solution_step.exit_code != 0:
                result.status = "fail"
            else:
                checker = f"check_lab{lab_id[4:].lower()}.py"
                check_step = _run_step(
                    "checker", [python, checker, "--artifacts", str(artifacts)], lab, timeout
                )
                result.steps.append(check_step)
                result.status = "pass" if check_step.exit_code == 0 else "fail"
    finally:
        if context is not None:
            context.cleanup()
    return result


def print_results(
    results: list[LabResult],
    global_errors: list[str],
    global_warnings: list[str],
    global_checks: int,
    execution: dict[str, ExecutionResult],
) -> bool:
    failed_labs = [result for result in results if not result.ok]
    warned_labs = [result for result in results if result.warnings]
    for result in results:
        status = "PASS" if result.ok else "FAIL"
        suffix = f", {len(result.warnings)} warning(s)" if result.warnings else ""
        print(f"{result.lab_id:<9} {status}  {result.checks} checks{suffix}")
        for error in result.errors:
            print(f"  FAIL {error}")
        for warning in result.warnings:
            print(f"  WARN {warning}")
    for error in global_errors:
        print(f"GLOBAL FAIL {error}")
    for warning in global_warnings:
        print(f"GLOBAL WARN {warning}")

    execution_failures = [value for value in execution.values() if value.status != "pass"]
    if execution:
        print("\nExecution")
        for lab_id, outcome in sorted(execution.items(), key=lambda item: lab_sort_key(item[0])):
            print(f"{lab_id:<9} {outcome.status.upper()}")
            for step in outcome.steps:
                code = "timeout" if step.exit_code is None else str(step.exit_code)
                print(f"  {step.name:<12} exit={code:<8} {step.seconds:6.1f}s")
                if step.exit_code != 0:
                    for line in step.detail.splitlines()[-12:]:
                        print(f"    {line}")

    structural_ok = not failed_labs and not global_errors
    execution_ok = not execution_failures
    print(
        f"\nSummary: {len(results)} labs structurally checked, {len(failed_labs)} failed; "
        f"{global_checks} global checks, {len(global_errors)} global failures, "
        f"{len(global_warnings)} global warnings; {len(warned_labs)} labs with warnings"
    )
    if execution:
        print(
            f"Execution: {len(execution) - len(execution_failures)} passed, "
            f"{len(execution_failures)} failed or timed out"
        )
    else:
        print("Execution: not run (use --execute to run reference solutions and checkers)")
    return structural_ok and execution_ok


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the ML-Sec lab packages.")
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument(
        "--lab",
        action="append",
        default=[],
        help="Restrict to a lab ID or directory name; may be repeated.",
    )
    parser.add_argument(
        "--structural",
        action="store_true",
        help="Run structural checks only (the default).",
    )
    parser.add_argument("--execute", action="store_true", help="Run reference solutions and checkers.")
    parser.add_argument(
        "--keep-artifacts",
        type=Path,
        default=None,
        help="With --execute, keep artifacts under this directory instead of a temp dir.",
    )
    parser.add_argument("--timeout", type=int, default=600, help="Per-step timeout in seconds.")
    parser.add_argument(
        "--check-urls", action="store_true", help="Probe external HTTP(S) links (uses network)."
    )
    parser.add_argument("--json", type=Path, default=None)
    parser.add_argument("--strict-warnings", action="store_true")
    args = parser.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    root = args.root.resolve()
    lab_filter = {value.upper() for value in args.lab} | set(args.lab)
    results = validate_repository(root, lab_filter)
    if not results:
        print("No labs found" + (f" for filter {sorted(args.lab)}" if args.lab else ""))
        return 1
    global_errors, global_warnings, global_checks = check_repository_globals(root)

    url_issues: list[check_links.LinkIssue] = []
    blocked_urls: list[check_links.LinkIssue] = []
    if args.check_urls:
        links = check_links.collect_external_links(root)
        print(f"Checking {len(links)} external links (timeout {args.timeout}s)...")
        url_issues, blocked_urls = check_links.check_external_links(
            links, timeout=float(args.timeout)
        )
        for issue in url_issues:
            global_errors.append(
                f"external link {issue.target} in {issue.source}:{issue.line} ({issue.reason})"
            )
        for issue in blocked_urls:
            global_warnings.append(
                f"external link blocked by host {issue.target} in {issue.source}:{issue.line} "
                f"({issue.reason})"
            )

    execution: dict[str, ExecutionResult] = {}
    if args.execute:
        if args.keep_artifacts:
            args.keep_artifacts.mkdir(parents=True, exist_ok=True)
        labs_root = root / "labs"
        for lab in discover_labs(labs_root):
            lab_id = lab_id_from_dir(lab)
            if lab_filter and lab_id not in lab_filter and lab.name not in lab_filter:
                continue
            print(f"Executing {lab_id}...", flush=True)
            outcome = execute_lab(lab, args.timeout, args.keep_artifacts)
            execution[lab_id] = outcome
            print(f"  {outcome.status}", flush=True)

    ok = print_results(results, global_errors, global_warnings, global_checks, execution)
    if args.strict_warnings and (global_warnings or any(result.warnings for result in results)):
        ok = False
        print("Strict warnings enabled: warnings count as failure")

    if args.json:
        payload = {
            "python": sys.version.split()[0],
            "labs_root": str(root / "labs"),
            "structural": {
                "labs": [
                    {
                        "lab_id": result.lab_id,
                        "directory": result.directory,
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
            },
            "execution": {
                lab_id: {
                    "status": outcome.status,
                    "steps": [asdict(step) for step in outcome.steps],
                }
                for lab_id, outcome in execution.items()
            },
            "external_links_checked": bool(args.check_urls),
            "external_link_issues": [asdict(issue) for issue in url_issues],
            "blocked_external_links": [asdict(issue) for issue in blocked_urls],
            "status": "pass" if ok else "fail",
        }
        args.json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"JSON summary written to {args.json}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
