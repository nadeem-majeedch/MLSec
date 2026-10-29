"""Independent checker for LAB-02 threat models.

Usage:
    python check_threat_model.py --model solution.yaml --report solution-report.md
    python check_threat_model.py --model threat-model.yaml --report report.md

Exit code 0 means every structural check passed. The checker validates the
model for completeness and internal consistency; it cannot judge whether the
security reasoning is good. Use the rubric in docs/labs/lab-02.md for that.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: python -m pip install -r requirements.txt")

ATLAS_ALLOWLIST = {
    "AML.T0015": "Evade AI Model",
    "AML.T0043": "Craft Adversarial Data",
    "AML.T0020": "Training Data Poisoning",
    "AML.T0018": "Manipulate AI Model",
    "AML.T0024": "Exfiltration via AI Inference API",
    "AML.T0040": "AI Model Inference API Access",
    "AML.T0051": "LLM Prompt Injection",
}

OWASP_ML_ALLOWLIST = {
    "ML01": "Input Manipulation Attack",
    "ML02": "Data Poisoning Attack",
    "ML03": "Model Inversion Attack",
    "ML04": "Membership Inference Attack",
    "ML05": "Model Theft",
    "ML06": "AI Supply Chain Attacks",
    "ML07": "Transfer Learning Attack",
    "ML08": "Model Skewing",
    "ML09": "Output Integrity Attack",
    "ML10": "Model Poisoning",
}

NIST_GOALS = {"integrity", "availability", "privacy", "abuse"}
STAGES = {"data_collection", "training", "artifact", "serving", "monitoring"}
SEVERITIES = {"low", "medium", "high", "critical"}
RESIDUAL = {"low", "medium", "high"}
RMF_FUNCTIONS = {"GOVERN", "MAP", "MEASURE", "MANAGE"}
REPORT_HEADINGS = [
    "## System and scope",
    "## Data-flow diagram",
    "## Assets",
    "## Trust boundaries",
    "## Attack surfaces",
    "## Adversary model",
    "## Threat register",
    "## Attack trees",
    "## Mitigations and residual risk",
    "## Framework crosswalk",
    "## Assumptions and rejected threats",
    "## Reproduction",
]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def words(text: str) -> int:
    return len(str(text).split())


def severity_for(impact: int, likelihood: int) -> str:
    score = impact * likelihood
    if score <= 4:
        return "low"
    if score <= 9:
        return "medium"
    if score <= 16:
        return "high"
    return "critical"


def require(mapping: dict, key: str, where: str, kind=str) -> object:
    if key not in mapping:
        fail(f"{where} is missing '{key}'")
    value = mapping[key]
    if kind is int and not isinstance(value, int):
        fail(f"{where}.{key} must be an integer")
    if kind is str and (not isinstance(value, str) or not value.strip()):
        fail(f"{where}.{key} must be a non-empty string")
    if kind is list and (not isinstance(value, list) or not value):
        fail(f"{where}.{key} must be a non-empty list")
    return value


def add_unique(seen: set, value: str, where: str) -> None:
    if value in seen:
        fail(f"duplicate id {value} at {where}")
    seen.add(value)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check a LAB-02 threat model.")
    parser.add_argument("--model", type=Path, default=Path("threat-model.yaml"))
    parser.add_argument("--report", type=Path, default=Path("report.md"))
    parser.add_argument("--summary", type=Path, default=None, help="Optional path to write a JSON summary.")
    args = parser.parse_args()

    if not args.model.exists():
        fail(f"missing model file {args.model}")
    with open(args.model, encoding="utf-8") as handle:
        doc = yaml.safe_load(handle)
    if not isinstance(doc, dict):
        fail("the model file must contain a YAML mapping")

    system = doc.get("system")
    if not isinstance(system, dict):
        fail("missing 'system' mapping")
    for key in ("name", "description", "owner", "deployment"):
        require(system, key, "system")

    assets = require(doc, "assets", "document", list)
    boundaries = require(doc, "trust_boundaries", "document", list)
    surfaces = require(doc, "attack_surfaces", "document", list)
    threats = require(doc, "threats", "document", list)
    trees = doc.get("attack_trees")
    if not isinstance(trees, list):
        fail("'attack_trees' must be a list")
    crosswalk = doc.get("crosswalk")
    if not isinstance(crosswalk, dict):
        fail("missing 'crosswalk' mapping")

    if len(assets) < 6:
        fail("at least 6 assets are required")
    if len(boundaries) < 5:
        fail("at least 5 trust boundaries are required")
    if len(surfaces) < 8:
        fail("at least 8 attack surfaces are required")

    asset_ids: set[str] = set()
    for index, asset in enumerate(assets):
        where = f"assets[{index}]"
        if not isinstance(asset, dict):
            fail(f"{where} must be a mapping")
        asset_id = require(asset, "id", where)
        add_unique(asset_ids, asset_id, where)
        require(asset, "name", where)
        require(asset, "description", where)
        require(asset, "cia", where, list)
        require(asset, "sensitivity", where)

    boundary_ids: set[str] = set()
    boundary_surfaces: dict[str, set[str]] = {}
    for index, boundary in enumerate(boundaries):
        where = f"trust_boundaries[{index}]"
        if not isinstance(boundary, dict):
            fail(f"{where} must be a mapping")
        boundary_id = require(boundary, "id", where)
        add_unique(boundary_ids, boundary_id, where)
        require(boundary, "name", where)
        require(boundary, "between", where, list)
        require(boundary, "controls", where, list)
        boundary_surfaces[boundary_id] = set()

    surface_ids: set[str] = set()
    surface_boundary: dict[str, str] = {}
    for index, surface in enumerate(surfaces):
        where = f"attack_surfaces[{index}]"
        if not isinstance(surface, dict):
            fail(f"{where} must be a mapping")
        surface_id = require(surface, "id", where)
        add_unique(surface_ids, surface_id, where)
        require(surface, "name", where)
        boundary_id = require(surface, "boundary", where)
        if boundary_id not in boundary_ids:
            fail(f"{where}.boundary references unknown {boundary_id}")
        require(surface, "entry_point", where)
        require(surface, "attacker_access", where)
        surface_boundary[surface_id] = boundary_id
        boundary_surfaces[boundary_id].add(surface_id)

    threat_ids: set[str] = set()
    accepted: dict[str, dict] = {}
    rejected: dict[str, dict] = {}
    for index, threat in enumerate(threats):
        where = f"threats[{index}]"
        if not isinstance(threat, dict):
            fail(f"{where} must be a mapping")
        threat_id = require(threat, "id", where)
        add_unique(threat_ids, threat_id, where)
        status = require(threat, "status", where)
        if status not in {"accepted", "rejected"}:
            fail(f"{where}.status must be 'accepted' or 'rejected'")
        require(threat, "title", where)
        require(threat, "attack_class", where)
        require(threat, "nist_goal", where)
        require(threat, "lifecycle_stage", where)
        require(threat, "actor", where)
        require(threat, "knowledge", where)
        require(threat, "capability", where)
        require(threat, "impact_statement", where)
        require(threat, "detection_hypothesis", where)
        require(threat, "assumptions", where, list)
        require(threat, "assets", where, list)
        require(threat, "surfaces", where, list)
        if "atlas" not in threat:
            fail(f"{where} is missing 'atlas' (use an empty list if none applies)")
        if not isinstance(threat["atlas"], list):
            fail(f"{where}.atlas must be a list")
        if threat["nist_goal"] not in NIST_GOALS:
            fail(f"{where}.nist_goal must be one of {sorted(NIST_GOALS)}")
        if threat["lifecycle_stage"] not in STAGES:
            fail(f"{where}.lifecycle_stage must be one of {sorted(STAGES)}")
        for atlas_id in threat["atlas"]:
            if atlas_id not in ATLAS_ALLOWLIST:
                fail(f"{where}.atlas contains unsupported ID {atlas_id}")
        for asset_id in threat["assets"]:
            if asset_id not in asset_ids:
                fail(f"{where}.assets references unknown {asset_id}")
        for surface_id in threat["surfaces"]:
            if surface_id not in surface_ids:
                fail(f"{where}.surfaces references unknown {surface_id}")
        impact = require(threat, "impact", where, int)
        likelihood = require(threat, "likelihood", where, int)
        if not 1 <= impact <= 5 or not 1 <= likelihood <= 5:
            fail(f"{where} impact and likelihood must be 1-5")
        severity = require(threat, "severity", where)
        expected = severity_for(impact, likelihood)
        if severity != expected:
            fail(f"{where}.severity is {severity}; {impact}x{likelihood} should be {expected}")
        mitigations = threat.get("mitigations")
        if not isinstance(mitigations, dict):
            fail(f"{where} is missing 'mitigations'")
        for kind in ("preventive", "detective", "corrective"):
            values = mitigations.get(kind)
            if not isinstance(values, list) or not values:
                fail(f"{where}.mitigations.{kind} must be a non-empty list")
        residual = require(threat, "residual_risk", where)
        if residual not in RESIDUAL:
            fail(f"{where}.residual_risk must be one of {sorted(RESIDUAL)}")
        if status == "accepted":
            if words(threat["impact_statement"]) < 10:
                fail(f"{where}.impact_statement is too short to be testable")
            if words(threat["detection_hypothesis"]) < 8:
                fail(f"{where}.detection_hypothesis is too short to be testable")
            if severity in {"critical", "high"}:
                if len(mitigations["preventive"]) < 2:
                    fail(f"{where} is {severity} but has fewer than two preventive controls")
                if residual == "high":
                    fail(f"{where} is {severity} with high residual risk; add a control or justify acceptance")
            accepted[threat_id] = threat
        else:
            if words(threat.get("rationale", "")) < 10:
                fail(f"{where} is rejected but has no substantive rationale")
            rejected[threat_id] = threat

    if len(accepted) < 9:
        fail(f"at least 9 accepted threats are required; found {len(accepted)}")
    if not rejected:
        fail("at least one threat must be rejected with reasoning")

    referenced_assets = {asset for threat in accepted.values() for asset in threat["assets"]}
    if asset_ids - referenced_assets:
        fail(f"assets with no accepted threat: {sorted(asset_ids - referenced_assets)}")
    referenced_surfaces = {surface for threat in accepted.values() for surface in threat["surfaces"]}
    if surface_ids - referenced_surfaces:
        fail(f"attack surfaces with no accepted threat: {sorted(surface_ids - referenced_surfaces)}")

    for boundary_id, owned in boundary_surfaces.items():
        if not (owned & referenced_surfaces):
            fail(f"trust boundary {boundary_id} has no surface covered by an accepted threat")

    stages = {threat["lifecycle_stage"] for threat in accepted.values()}
    if stages != STAGES:
        fail(f"accepted threats must cover all lifecycle stages; missing {sorted(STAGES - stages)}")
    goals = {threat["nist_goal"] for threat in accepted.values()}
    if goals != NIST_GOALS:
        fail(f"accepted threats must cover all four NIST goals; missing {sorted(NIST_GOALS - goals)}")
    attack_classes = {threat["attack_class"] for threat in accepted.values()}
    if len(attack_classes) < 6:
        fail(f"at least 6 distinct attack classes are required; found {len(attack_classes)}")

    if len(trees) < 3:
        fail("at least 3 attack trees are required")
    tree_ids: set[str] = set()
    for index, tree in enumerate(trees):
        where = f"attack_trees[{index}]"
        if not isinstance(tree, dict):
            fail(f"{where} must be a mapping")
        add_unique(tree_ids, require(tree, "id", where), where)
        require(tree, "name", where)
        require(tree, "root", where)
        steps = require(tree, "steps", where, list)
        if len(steps) < 3:
            fail(f"{where} needs at least 3 steps")
        for step_index, step in enumerate(steps):
            step_where = f"{where}.steps[{step_index}]"
            if not isinstance(step, dict):
                fail(f"{step_where} must be a mapping")
            require(step, "action", step_where)
            threat_id = require(step, "threat", step_where)
            if threat_id not in accepted:
                fail(f"{step_where}.threat must reference an accepted threat")

    rmf = crosswalk.get("ai_rmf")
    if not isinstance(rmf, list):
        fail("crosswalk.ai_rmf must be a list")
    rmf_functions = set()
    for index, entry in enumerate(rmf):
        where = f"crosswalk.ai_rmf[{index}]"
        if not isinstance(entry, dict):
            fail(f"{where} must be a mapping")
        function = require(entry, "function", where)
        if function not in RMF_FUNCTIONS:
            fail(f"{where}.function must be one of {sorted(RMF_FUNCTIONS)}")
        if words(require(entry, "note", where)) < 5:
            fail(f"{where}.note is too short")
        rmf_functions.add(function)
    if rmf_functions != RMF_FUNCTIONS:
        fail(f"crosswalk.ai_rmf must cover all four functions; missing {sorted(RMF_FUNCTIONS - rmf_functions)}")

    owasp_ml = crosswalk.get("owasp_ml")
    if not isinstance(owasp_ml, list) or len(owasp_ml) < 4:
        fail("crosswalk.owasp_ml must list at least 4 entries")
    for index, entry in enumerate(owasp_ml):
        where = f"crosswalk.owasp_ml[{index}]"
        if not isinstance(entry, dict):
            fail(f"{where} must be a mapping")
        owasp_id = require(entry, "id", where)
        if owasp_id not in OWASP_ML_ALLOWLIST:
            fail(f"{where}.id {owasp_id} is not a valid OWASP ML Top 10 ID")
        mapped = require(entry, "threats", where, list)
        for threat_id in mapped:
            if threat_id not in accepted:
                fail(f"{where}.threats references non-accepted threat {threat_id}")

    llm = crosswalk.get("owasp_llm")
    if not isinstance(llm, dict) or "applicable" not in llm:
        fail("crosswalk.owasp_llm must state 'applicable: true|false'")
    if not isinstance(llm["applicable"], bool):
        fail("crosswalk.owasp_llm.applicable must be a boolean")
    if llm["applicable"] is False and words(llm.get("rationale", "")) < 8:
        fail("crosswalk.owasp_llm needs a rationale when not applicable")

    if not args.report.exists():
        fail(f"missing report {args.report}")
    report = args.report.read_text(encoding="utf-8")
    for heading in REPORT_HEADINGS:
        if heading not in report:
            fail(f"report is missing heading: {heading}")
    if "```mermaid" not in report:
        fail("report must contain at least one Mermaid diagram")
    if "TB" not in report:
        fail("report must name at least one trust boundary (for example TB1)")

    severities = Counter(threat["severity"] for threat in accepted.values())
    summary = {
        "system": system["name"],
        "assets": len(assets),
        "boundaries": len(boundaries),
        "surfaces": len(surfaces),
        "accepted_threats": len(accepted),
        "rejected_threats": len(rejected),
        "severity": {level: severities.get(level, 0) for level in ("critical", "high", "medium", "low")},
        "nist_goals": dict(Counter(threat["nist_goal"] for threat in accepted.values())),
        "attack_classes": len(attack_classes),
        "lifecycle_stages": len(stages),
        "attack_trees": len(trees),
        "owasp_ml_entries": len(owasp_ml),
        "atlas_ids": sorted({atlas for threat in accepted.values() for atlas in threat["atlas"]}),
    }

    if args.summary:
        args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"PASS schema for {summary['system']}")
    print(f"PASS {len(assets)} assets, {len(boundaries)} boundaries, {len(surfaces)} surfaces, all referenced")
    print(f"PASS {len(accepted)} accepted and {len(rejected)} rejected threats; all five lifecycle stages")
    print(f"PASS all four NIST goals and {len(attack_classes)} attack classes represented")
    print(f"PASS severity scores, two-control rule, detection hypotheses, and {len(trees)} attack trees")
    print("PASS AI RMF functions and OWASP ML crosswalk")
    print("PASS report structure includes a Mermaid data-flow diagram")
    print(f"Severity: {summary['severity']}")
    print("LAB-02 CHECK PASSED")


if __name__ == "__main__":
    main()
