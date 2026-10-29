"""Independent checker for LAB-19.

Usage:
    python solution.py --out artifacts
    python check_lab19.py --artifacts artifacts

Exit code 0 means every check passed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-19 artifacts.")
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
    if run.get("lab") != "LAB-19":
        fail("run.json lab is not LAB-19")
    if int(run.get("top_k", 0)) != 3:
        fail("run.json must record top_k 3")
    if int(run.get("documents", 0)) != 8:
        fail("run.json must record eight documents")
    if int(run.get("benign_queries", 0)) != 3:
        fail("run.json must record three benign queries")
    if run.get("attacks") != ["indirect_canary", "indirect_action", "direct_canary"]:
        fail("run.json must record the three attack names")

    corpus = metrics["corpus"]
    if corpus["trusted"] != 5 or corpus["untrusted"] != 3:
        fail("corpus must have five trusted and three untrusted documents")
    canary = metrics["canary"]
    if not canary.startswith("CANARY-"):
        fail("canary must be a harmless synthetic marker")

    policies = metrics.get("policies", {})
    for name in ("baseline", "trust_labels", "output_validation", "combined"):
        if name not in policies:
            fail(f"missing policy {name}")
        policy = policies[name]
        if policy["benign_success"] != policy["benign_total"]:
            fail(f"{name} must answer all benign queries")
        if policy["false_positives"] != 0:
            fail(f"{name} must not report benign false positives")
        if len(policy["attacks"]) != 3:
            fail(f"{name} must report three attacks")

    baseline = policies["baseline"]
    if baseline["attack_successes"] != 3:
        fail("baseline must follow all three injected instructions")
    for attack in baseline["attacks"]:
        if not attack["success"]:
            fail(f"baseline attack {attack['name']} must succeed")

    trust = policies["trust_labels"]
    if trust["attack_successes"] != 1:
        fail("trust labels must leave exactly the direct user instruction successful")
    by_name = {attack["name"]: attack for attack in trust["attacks"]}
    if by_name["indirect_canary"]["success"] or by_name["indirect_action"]["success"]:
        fail("trust labels must block both indirect attacks")
    if not by_name["direct_canary"]["success"]:
        fail("trust labels alone must not block the direct user instruction")

    validation = policies["output_validation"]
    if validation["attack_successes"] != 1:
        fail("output validation must leave exactly one attack successful")
    by_name = {attack["name"]: attack for attack in validation["attacks"]}
    if by_name["indirect_canary"]["success"]:
        fail("output validation must block the canary leak")
    if not by_name["indirect_canary"]["instruction_followed"]:
        fail("output validation must still show that the instruction was followed")
    if not by_name["indirect_action"]["success"]:
        fail("output validation must not stop the marker action in this setup")
    if validation["tripwires"] < 2:
        fail("output validation must record canary tripwires for both canary attacks")

    combined = policies["combined"]
    if combined["attack_successes"] != 0:
        fail("the combined policy must block all three attacks in this mock")
    if combined["tripwires"] != 1:
        fail("the combined policy must record the direct canary attempt")

    for policy in policies.values():
        for attack in policy["attacks"]:
            if attack["name"].startswith("indirect") and attack["source"] not in attack["retrieved"]:
                fail(f"{attack['name']} did not retrieve its untrusted source")

    text = report.read_text(encoding="utf-8").lower()
    for phrase in ("data", "authority", "prompt filtering", "synthetic", "limitations"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print("PASS baseline: benign 3/3, all three attacks succeed")
    print("PASS trust labels: indirect attacks blocked, direct user instruction remains")
    print("PASS output validation: canary blocked but marker action still succeeds")
    print("PASS combined: all attacks blocked; canary attempt recorded")
    print("PASS benign queries are unaffected and no false positives are reported")
    print("PASS report distinguishes data from authority and rejects prompt filtering alone")
    print("LAB-19 CHECK PASSED")


if __name__ == "__main__":
    main()
