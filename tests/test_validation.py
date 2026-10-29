"""Lightweight tests for the lab validation tooling.

Run from the repository root:
    python -m unittest discover -s tests

These tests use only the standard library and synthetic temporary files. They do
not execute lab code, download data, or make network calls.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import check_links  # noqa: E402
import validate_assessments  # noqa: E402
import validate_labs  # noqa: E402


class MetadataTests(unittest.TestCase):
    def test_readme_metadata_table(self) -> None:
        text = """# LAB-99 — Fixture

| Field | Value |
|---|---|
| Lab ID | LAB-99 |
| Tier | A |
| Time | 4 hours |
| Difficulty | 2 of 4 |
| Module | M04 — Evasion |
| Outcomes | LO-05, LO-28 |
| Prerequisites | None |
| Data | synthetic |
| Compute | CPU only; seconds |

## Scenario
"""
        metadata = validate_labs.parse_readme_metadata(text)
        self.assertEqual(metadata["Lab ID"], "LAB-99")
        self.assertEqual(metadata["Tier"], "A")
        self.assertEqual(metadata["Time"], "4 hours")
        self.assertEqual(metadata["Difficulty"], "2 of 4")
        self.assertNotIn("Field", metadata)

    def test_brief_metadata_singular_and_plural_module(self) -> None:
        singular = "**Tier A · 4 hours · Difficulty 2 · Module M04 · Outcomes LO-05, LO-28**\n"
        plural = "**Tier A · 3 hours · Difficulty 1 · Modules M00–M01 · Outcomes LO-01, LO-28**\n"
        first = validate_labs.parse_brief_metadata(singular)
        second = validate_labs.parse_brief_metadata(plural)
        self.assertIsNotNone(first)
        self.assertIsNotNone(second)
        assert first is not None and second is not None
        self.assertEqual(first["module"], "M04")
        self.assertEqual(first["difficulty"], 2)
        self.assertEqual(second["module"], "M00–M01")
        self.assertEqual(second["outcomes"], ["LO-01", "LO-28"])

    def test_section_body_stops_at_next_heading(self) -> None:
        text = "## Hints\n- one\n- two\n\n## Time box\n| Time | Work |\n"
        self.assertEqual(validate_labs.section_body(text, "Hints").strip(), "- one\n- two")

    def test_section_variants_accept_known_headings(self) -> None:
        headings = [variant for _, variants in validate_labs.BRIEF_SECTIONS for variant in variants]
        self.assertIn("What you build", headings)
        self.assertIn("Reference results", headings)
        self.assertIn("Data and environment", headings)


class LinkTests(unittest.TestCase):
    def test_slugify(self) -> None:
        self.assertEqual(check_links.slugify("Hello, World!"), "hello-world")
        self.assertEqual(check_links.slugify("LAB-01B — Evaluation"), "lab-01b-evaluation")
        self.assertEqual(check_links.slugify("What you build"), "what-you-build")

    def test_links_inside_code_are_ignored(self) -> None:
        text = """[real](target.md)
`[inline](ignored.md)`
```markdown
[fenced](also-ignored.md)
```
"""
        targets = [link.target for link in check_links.extract_links(text)]
        self.assertEqual(targets, ["target.md"])

    def test_explicit_anchor_and_duplicate_headings(self) -> None:
        text = "# Title\n## Same\n## Same\n## Custom {#custom-id}\n"
        anchors = check_links.heading_anchors(text)
        self.assertIn("same", anchors)
        self.assertIn("same_1", anchors)
        self.assertIn("custom-id", anchors)

    def test_check_file_reports_missing_file_and_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.md"
            target.write_text("# Present\n", encoding="utf-8")
            source = root / "source.md"
            source.write_text(
                "[ok](target.md#present)\n[bad anchor](target.md#absent)\n[missing](nope.md)\n",
                encoding="utf-8",
            )
            original_root = check_links.REPO_ROOT
            check_links.REPO_ROOT = root
            try:
                issues = check_links.check_file(source)
            finally:
                check_links.REPO_ROOT = original_root
            reasons = " ".join(issue.reason for issue in issues)
            self.assertEqual(len(issues), 2)
            self.assertIn("missing anchor", reasons)
            self.assertIn("missing file", reasons)

    def test_directory_link_resolves_to_index(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "guide").mkdir()
            (root / "guide" / "index.md").write_text("# Guide\n", encoding="utf-8")
            source = root / "source.md"
            source.write_text("[guide](guide/)\n", encoding="utf-8")
            original_root = check_links.REPO_ROOT
            check_links.REPO_ROOT = root
            try:
                self.assertEqual(check_links.check_file(source), [])
            finally:
                check_links.REPO_ROOT = original_root


class PythonAndNotebookTests(unittest.TestCase):
    def test_import_extraction(self) -> None:
        source = "import os\nimport numpy as np\nfrom sklearn.pipeline import Pipeline\nfrom . import local\n"
        modules = validate_labs.iter_python_imports(source)
        self.assertIn("os", modules)
        self.assertIn("numpy", modules)
        self.assertIn("sklearn", modules)
        self.assertNotIn("local", modules)

    def test_valid_notebook_structure(self) -> None:
        notebook = {
            "nbformat": 4,
            "nbformat_minor": 5,
            "metadata": {},
            "cells": [
                {"cell_type": "markdown", "metadata": {}, "source": ["# Title\n"]},
                {
                    "cell_type": "code",
                    "metadata": {},
                    "execution_count": None,
                    "outputs": [],
                    "source": ["print('hello')\n"],
                },
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ok.ipynb"
            path.write_text(json.dumps(notebook), encoding="utf-8")
            self.assertEqual(validate_labs.check_notebook(path), [])

    def test_invalid_notebook_structure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.ipynb"
            path.write_text(json.dumps({"cells": [{"cell_type": "code"}]}), encoding="utf-8")
            errors = validate_labs.check_notebook(path)
            self.assertTrue(errors)

    def test_notebook_json_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.ipynb"
            path.write_text("{not json", encoding="utf-8")
            errors = validate_labs.check_notebook(path)
            self.assertEqual(len(errors), 1)
            self.assertIn("invalid notebook JSON", errors[0])


class RepositoryTests(unittest.TestCase):
    def test_every_lab_directory_has_a_brief_and_catalog_entry(self) -> None:
        labs = validate_labs.discover_labs(REPO_ROOT / "labs")
        self.assertEqual(len(labs), 21)
        entries = validate_labs.catalog_entries(REPO_ROOT / "docs" / "lab-catalog.md")
        for lab in labs:
            lab_id = validate_labs.lab_id_from_dir(lab)
            self.assertIn(lab_id, entries)
            brief = REPO_ROOT / "docs" / "labs" / f"lab-{lab_id[4:].lower()}.md"
            self.assertTrue(brief.exists(), f"missing brief for {lab_id}")

    def test_one_lab_structural_validation_passes(self) -> None:
        lab = REPO_ROOT / "labs" / "lab-03-evasion-magnitude"
        brief = REPO_ROOT / "docs" / "labs" / "lab-03.md"
        entries = validate_labs.catalog_entries(REPO_ROOT / "docs" / "lab-catalog.md")
        result = validate_labs.validate_lab(lab, brief, entries.get("LAB-03"))
        self.assertTrue(result.ok, "\n".join(result.errors))

    def test_authoring_guide_and_template_exist(self) -> None:
        self.assertTrue((REPO_ROOT / "docs" / "lab-authoring-guide.md").exists())
        self.assertTrue((REPO_ROOT / "docs" / "lab-template.md").exists())


class AssessmentTests(unittest.TestCase):
    def test_quiz_blueprint_totals(self) -> None:
        self.assertEqual(sum(validate_assessments.QUIZ_POINTS), 12)
        self.assertEqual(sum(validate_assessments.LEVEL_CHECK_POINTS), 20)

    def test_compound_tag_line_parses(self) -> None:
        text = "Tag: M04 · LO-05 · Bloom 3 · D2 and M06 · LO-10 · Bloom 3 · D2.\n"
        tags, malformed = validate_assessments.key_tags(text)
        self.assertEqual(malformed, [])
        self.assertEqual(len(tags), 1)
        modules, outcomes, bloom, difficulty = tags[0]
        self.assertEqual(modules, ["M04", "M06"])
        self.assertEqual(outcomes, ["LO-05", "LO-10"])
        self.assertEqual((bloom, difficulty), (3, 2))

    def test_malformed_tag_line_is_reported(self) -> None:
        tags, malformed = validate_assessments.key_tags("Tag: M04 · Bloom 3 · D2.\n")
        self.assertEqual(tags, [])
        self.assertEqual(len(malformed), 1)

    def test_every_module_quiz_validates(self) -> None:
        for module in validate_assessments.MODULES:
            result = validate_assessments.validate_quiz(module)
            self.assertTrue(result.ok, f"{result.name}: " + "; ".join(result.errors))

    def test_every_level_check_validates(self) -> None:
        for level in range(1, 6):
            result = validate_assessments.validate_level_check(level)
            self.assertTrue(result.ok, f"{result.name}: " + "; ".join(result.errors))

    def test_bank_diagnostic_and_final_validate(self) -> None:
        for result in (
            validate_assessments.validate_diagnostic(),
            validate_assessments.validate_bank(),
            validate_assessments.validate_final(),
        ):
            self.assertTrue(result.ok, f"{result.name}: " + "; ".join(result.errors))

    def test_rubric_weights_total_one_hundred(self) -> None:
        for name in ("lab-rubric.md", "capstone-rubric.md", "project-rubric.md"):
            path = REPO_ROOT / "docs" / "assessments" / "rubrics" / name
            self.assertEqual(validate_assessments.rubric_weight_sum(path), 100, name)

    def test_practice_widget_validates(self) -> None:
        result = validate_assessments.validate_widget()
        self.assertTrue(result.ok, "; ".join(result.errors))

    def test_global_assessment_checks_pass(self) -> None:
        errors, warnings, checks = validate_assessments.validate_globals()
        self.assertEqual(errors, [])
        self.assertGreater(checks, 50)


if __name__ == "__main__":
    unittest.main()
