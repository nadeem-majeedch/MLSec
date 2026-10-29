"""Independent checker for LAB-13.

Usage:
    python solution.py --out artifacts
    python check_lab13.py --artifacts artifacts

Exit code 0 means every check passed. The checker never unpickles an artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import pickletools
from pathlib import Path

from project import PINNED

DEMO_KEY = b"lab-13-demo-key-not-for-production"
EXPECTED_RULES = {
    "DEP-001": ("high", "requirements.txt"),
    "ART-001": ("high", "load_model.py"),
    "ART-002": ("critical", "canary.pkl"),
    "ART-003": ("high", "manifest.json"),
    "ART-004": ("medium", "manifest.json"),
    "ART-005": ("medium", "sbom.json"),
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def signature(payload: bytes) -> str:
    return hmac.new(DEMO_KEY, payload, hashlib.sha256).hexdigest()


def dangerous_opcodes(path: Path) -> set[str]:
    with open(path, "rb") as handle:
        names = {opcode.name for opcode, _, _ in pickletools.genops(handle)}
    return names & {"GLOBAL", "STACK_GLOBAL", "REDUCE", "INST", "OBJ", "NEWOBJ", "NEWOBJ_EX"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-13 artifacts.")
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    root = args.artifacts

    audit = load_json(root / "audit.json")
    metrics = load_json(root / "metrics.json")
    run = load_json(root / "run.json")
    manifest = load_json(root / "manifest.json")
    report = root / "report.md"
    project = root / "project"
    hardened = root / "hardened"
    if not report.exists():
        fail("missing report.md")
    if not project.is_dir():
        fail("missing project/")
    if not hardened.is_dir():
        fail("missing hardened/")

    required = {"audit.json", "metrics.json", "run.json", "report.md"}
    paths = {entry["path"] for entry in manifest.get("files", [])}
    if not required <= paths:
        fail(f"manifest does not cover {sorted(required - paths)}")
    if run.get("lab") != "LAB-13":
        fail("run.json lab is not LAB-13")

    rules = {finding["rule"]: finding for finding in audit.get("findings", [])}
    if set(rules) != set(EXPECTED_RULES):
        fail(f"audit rules are {sorted(rules)}, expected {sorted(EXPECTED_RULES)}")
    for rule, (severity, filename) in EXPECTED_RULES.items():
        if rules[rule]["severity"] != severity:
            fail(f"{rule} severity is {rules[rule]['severity']}, expected {severity}")
        if rules[rule]["file"] != filename:
            fail(f"{rule} file is {rules[rule]['file']}, expected {filename}")
    summary = audit["summary"]
    if summary["total"] != 6 or summary["critical"] != 1 or summary["high"] != 3 or summary["medium"] != 2:
        fail("audit summary counts are wrong")

    if dangerous_opcodes(project / "canary.pkl") == set():
        fail("the canary pickle must contain dangerous opcodes")
    if dangerous_opcodes(project / "model.pkl") != set():
        fail("the benign model pickle must not contain dangerous opcodes")
    if not audit["pickle_scan"].get("canary.pkl"):
        fail("audit did not flag the canary pickle")
    if audit["pickle_scan"].get("model.pkl"):
        fail("audit flagged the benign pickle as dangerous")

    requirements = [
        line.strip()
        for line in (hardened / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(requirements) != len(PINNED):
        fail("hardened requirements must pin every dependency")
    for line in requirements:
        name, separator, version = line.partition("==")
        if not separator or PINNED.get(name) != version:
            fail(f"bad pin: {line}")
    loader = (hardened / "load_model.py").read_text(encoding="utf-8")
    if "allow_pickle=False" not in loader:
        fail("hardened loader must use allow_pickle=False")
    if "joblib.load(" in loader or "pickle.load(" in loader:
        fail("hardened loader still uses a pickle-based loader")
    if list(hardened.glob("*.pkl")):
        fail("hardened project still contains pickle artifacts")

    manifest_bytes = (hardened / "manifest.json").read_bytes()
    signed = json.loads(manifest_bytes)
    for entry in signed.get("files", []):
        if sha256(hardened / entry["path"]) != entry["sha256"]:
            fail(f"hardened manifest hash mismatch for {entry['path']}")
    if set(entry["path"] for entry in signed["files"]) != {
        "model.npz", "load_model.py", "requirements.txt", "train.py"
    }:
        fail("hardened manifest does not cover the expected files")

    sig = (hardened / "manifest.sig").read_text(encoding="utf-8").strip()
    if not hmac.compare_digest(signature(manifest_bytes), sig):
        fail("hardened manifest signature does not verify")
    tampered = bytes([manifest_bytes[0] ^ 1]) + manifest_bytes[1:]
    if hmac.compare_digest(signature(tampered), sig):
        fail("a tampered manifest must not verify")

    sbom = load_json(hardened / "sbom.json")
    if sbom.get("bomFormat") != "CycloneDX":
        fail("SBOM is not CycloneDX-format")
    components = sbom.get("components", [])
    if len(components) != len(PINNED):
        fail(f"SBOM has {len(components)} components, expected {len(PINNED)}")
    for component in components:
        name = component.get("name")
        if PINNED.get(name) != component.get("version"):
            fail(f"SBOM component {name} has the wrong version")
        if not component.get("purl"):
            fail(f"SBOM component {name} has no purl")
    model_hash = sbom["metadata"]["component"]["hashes"][0]["content"]
    if model_hash != sha256(hardened / "model.npz"):
        fail("SBOM model hash does not match model.npz")

    verification = metrics["verification"]
    expected_checks = {
        "vulnerable_hash_match": False,
        "vulnerable_signature_present": False,
        "canary_flagged": True,
        "safe_pickle_flagged": False,
        "hardened_hash_match": True,
        "hardened_signature_valid": True,
        "tampered_signature_valid": False,
        "hardened_pickle_files": 0,
        "hardened_pinned_dependencies": len(PINNED),
        "sbom_components": len(PINNED),
    }
    for key, value in expected_checks.items():
        if verification.get(key) != value:
            fail(f"metrics.verification.{key} is {verification.get(key)}, expected {value}")
    if metrics["gate"] != {"vulnerable_exit": 1, "hardened_exit": 0}:
        fail("CI gate results are wrong")

    text = report.read_text(encoding="utf-8").lower()
    for phrase in ("pickle", "hash", "signature", "sbom", "pin", "limitations"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print("PASS audit finds 6 issues across DEP-001 and ART-001 to ART-005")
    print("PASS canary pickle flagged statically; benign pickle not flagged")
    print("PASS hardened project pins dependencies and ships no pickle files")
    print("PASS hardened manifest hashes and HMAC signature verify; tamper rejected")
    print("PASS SBOM lists 5 pinned components and the model hash")
    print("PASS CI gate blocks the vulnerable project and passes the hardened project")
    print("LAB-13 CHECK PASSED")


if __name__ == "__main__":
    main()
