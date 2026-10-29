"""Independent checker for LAB-20.

Usage:
    python solution.py --out artifacts
    python check_lab20.py --artifacts artifacts

Exit code 0 means every check passed.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def attack_map(policy: dict) -> dict:
    return {attack["name"]: attack for attack in policy["attacks"]}


def expect_attack(policy_name: str, attacks: dict, name: str, decision: str, reason: str) -> None:
    attack = attacks.get(name)
    if attack is None:
        fail(f"{policy_name} is missing attack {name}")
    if attack["final_decision"] != decision:
        fail(f"{policy_name}/{name} must end in {decision}, got {attack['final_decision']}")
    if reason and attack["final_reason"] != reason:
        fail(f"{policy_name}/{name} must report {reason}, got {attack['final_reason']}")
    if attack["success"] != (decision == "allow"):
        fail(f"{policy_name}/{name} success flag does not match its decision")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-20 artifacts.")
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    root = args.artifacts

    metrics = load_json(root / "metrics.json")
    run = load_json(root / "run.json")
    manifest = load_json(root / "manifest.json")
    report = root / "report.md"
    if not report.exists():
        fail("missing report.md")

    required = {"metrics.json", "run.json", "report.md"}
    paths = {entry["path"] for entry in manifest.get("files", [])}
    if not required <= paths:
        fail(f"manifest does not cover {sorted(required - paths)}")
    if run.get("lab") != "LAB-20":
        fail("run.json lab is not LAB-20")
    if run.get("policies") != ["baseline", "scoped", "approval", "layered"]:
        fail("run.json must record the four policies in order")
    if len(run.get("benign_tasks", [])) != 4:
        fail("run.json must record four benign tasks")
    if len(run.get("attacks", [])) != 5:
        fail("run.json must record five attacks")
    if "delete_file" not in run.get("tools", []):
        fail("run.json must record the full mock tool set")

    workspace = metrics.get("workspace", {})
    if "../confidential.txt" not in workspace.get("outside_files", []):
        fail("the mock workspace must include the outside synthetic marker file")
    allowlists = metrics.get("allowlists", {})
    if allowlists.get("recipients") != ["security@internal.test", "team@internal.test"]:
        fail("recipient allowlist is not the expected synthetic set")
    if allowlists.get("hosts") != ["docs.example.test"]:
        fail("host allowlist is not the expected synthetic set")
    if "synthetic" not in metrics.get("note", "").lower():
        fail("metrics note must state that the setup is synthetic")

    policies = metrics.get("policies", {})
    for name in ("baseline", "scoped", "approval", "layered"):
        if name not in policies:
            fail(f"missing policy {name}")
        policy = policies[name]
        if policy["benign_success"] != 4 or policy["benign_total"] != 4:
            fail(f"{name} must complete all four benign tasks")
        if policy["false_positives"] != 0:
            fail(f"{name} must not report benign false positives")
        if policy["log_integrity"] != "ok":
            fail(f"{name} action log failed its hash-chain check")
        if policy["log_entries"] != 10:
            fail(f"{name} must log ten steps, got {policy['log_entries']}")
        if len(policy["attacks"]) != 5:
            fail(f"{name} must report five attacks")

    baseline = attack_map(policies["baseline"])
    if policies["baseline"]["attack_successes"] != 5:
        fail("baseline must allow all five attacks")
    for name in baseline:
        expect_attack("baseline", baseline, name, "allow", "allowed")

    scoped = attack_map(policies["scoped"])
    if policies["scoped"]["attack_successes"] != 1:
        fail("scoped policy must leave exactly one attack successful")
    expect_attack("scoped", scoped, "path_traversal_read", "deny", "path_outside_workspace")
    expect_attack("scoped", scoped, "external_email", "deny", "recipient_not_allowlisted")
    expect_attack("scoped", scoped, "non_allowlisted_fetch", "deny", "host_not_allowlisted")
    expect_attack("scoped", scoped, "untrusted_tool_output", "allow", "allowed")
    expect_attack("scoped", scoped, "excessive_agency_delete", "deny", "tool_not_granted")
    if policies["scoped"]["tool_output_denials"] != 0:
        fail("scoped policy has no approval gate, so it must not report tool-output denials")

    approval = attack_map(policies["approval"])
    if policies["approval"]["attack_successes"] != 2:
        fail("approval policy must leave exactly two attacks successful")
    expect_attack("approval", approval, "path_traversal_read", "allow", "allowed")
    expect_attack("approval", approval, "external_email", "deny", "approval_denied")
    expect_attack("approval", approval, "non_allowlisted_fetch", "allow", "allowed")
    expect_attack(
        "approval", approval, "untrusted_tool_output", "deny", "tool_output_cannot_authorize"
    )
    expect_attack("approval", approval, "excessive_agency_delete", "deny", "approval_denied")
    if policies["approval"]["approvals_granted"] != 1:
        fail("approval policy must grant only the benign internal email")
    if policies["approval"]["tool_output_denials"] != 1:
        fail("approval policy must deny exactly one tool-output-authorized action")

    layered = attack_map(policies["layered"])
    if policies["layered"]["attack_successes"] != 0:
        fail("layered policy must block all five attacks in this mock")
    expect_attack("layered", layered, "path_traversal_read", "deny", "path_outside_workspace")
    expect_attack("layered", layered, "external_email", "deny", "recipient_not_allowlisted")
    expect_attack("layered", layered, "non_allowlisted_fetch", "deny", "host_not_allowlisted")
    expect_attack(
        "layered", layered, "untrusted_tool_output", "deny", "tool_output_cannot_authorize"
    )
    expect_attack("layered", layered, "excessive_agency_delete", "deny", "tool_not_granted")
    if policies["layered"]["approvals_granted"] != 1:
        fail("layered policy must grant only the benign internal email")
    if policies["layered"]["tool_output_denials"] != 1:
        fail("layered policy must deny exactly one tool-output-authorized action")

    solution = Path(__file__).with_name("solution.py")
    if solution.exists():
        source = solution.read_text(encoding="utf-8")
        for forbidden in ("import requests", "import socket", "import subprocess", "urllib.request"):
            if forbidden in source:
                fail(f"solution imports or references {forbidden}")
        if re.search(r"\beval\(", source):
            fail("solution must not call eval")
        if re.search(r"\bexec\(", source):
            fail("solution must not call exec")

    text = report.read_text(encoding="utf-8").lower()
    for phrase in ("excessive agency", "capability", "approval", "untrusted", "synthetic", "limitations"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print("PASS baseline: all five attacks succeed and all benign tasks complete")
    print("PASS scoped: path, egress, and unregistered-tool attacks blocked; untrusted output still acts")
    print("PASS approval: mutating actions gated and tool output cannot authorize; read and fetch remain open")
    print("PASS layered: all five attacks blocked in this mock")
    print("PASS hash-chained action logs verify for every policy and task")
    print("PASS solution uses no network client, subprocess, eval, or exec")
    print("PASS report covers excessive agency, capability, approval, untrusted output, and limits")
    print("LAB-20 CHECK PASSED")


if __name__ == "__main__":
    main()
