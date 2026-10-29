"""LAB-13 reference solution: audit and harden a toy ML project.

Run from this directory:
    python solution.py --out artifacts

The generated artifacts are benign. The canary pickle is inspected as bytes and
is never passed to pickle.load. Artifacts: audit.json, metrics.json, run.json,
report.md, manifest.json, plus project/ and hardened/.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import pickletools
import shutil
import sys
from pathlib import Path

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, sha256_file, write_json  # noqa: E402

from project import (  # noqa: E402
    PINNED,
    SAFE_LOADER_SOURCE,
    build_project,
)

DEMO_KEY = b"lab-13-demo-key-not-for-production"
DANGEROUS_OPCODES = {"GLOBAL", "STACK_GLOBAL", "REDUCE", "INST", "OBJ", "NEWOBJ", "NEWOBJ_EX"}


def sign_bytes(payload: bytes, key: bytes = DEMO_KEY) -> str:
    return hmac.new(key, payload, hashlib.sha256).hexdigest()


def verify_signature(payload: bytes, signature: str, key: bytes = DEMO_KEY) -> bool:
    return hmac.compare_digest(sign_bytes(payload, key), signature.strip())


def pickle_opcodes(path: Path) -> list[tuple[str, object]]:
    """Read opcodes without unpickling. The stream is never executed."""
    with open(path, "rb") as handle:
        return [(opcode.name, arg) for opcode, arg, _ in pickletools.genops(handle)]


def audit_project(project_dir: Path) -> dict:
    findings = []
    pickle_scan = {}

    requirements = [
        line.strip()
        for line in (project_dir / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    unpinned = [line for line in requirements if "==" not in line]
    if unpinned:
        findings.append(
            {
                "rule": "DEP-001",
                "severity": "high",
                "file": "requirements.txt",
                "detail": f"{len(unpinned)} dependencies are unpinned",
                "evidence": unpinned,
                "remediation": "Pin exact versions with ==",
            }
        )

    loader = (project_dir / "load_model.py").read_text(encoding="utf-8")
    if "joblib.load(" in loader or "pickle.load(" in loader:
        findings.append(
            {
                "rule": "ART-001",
                "severity": "high",
                "file": "load_model.py",
                "detail": "model artifacts are deserialized with a pickle-based loader",
                "evidence": ["joblib.load" if "joblib.load(" in loader else "pickle.load"],
                "remediation": "Use np.load(..., allow_pickle=False) and validate shapes",
            }
        )

    for path in sorted(project_dir.glob("*.pkl")):
        opcodes = pickle_opcodes(path)
        dangerous = sorted({name for name, _ in opcodes if name in DANGEROUS_OPCODES})
        pickle_scan[path.name] = dangerous
        if dangerous:
            findings.append(
                {
                    "rule": "ART-002",
                    "severity": "critical",
                    "file": path.name,
                    "detail": "pickle stream contains callable-construction opcodes",
                    "evidence": dangerous,
                    "remediation": "Remove the artifact; migrate to a non-executable format",
                }
            )

    manifest_path = project_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    mismatches = []
    for entry in manifest.get("files", []):
        actual = sha256_file(project_dir / entry["path"])
        if actual != entry["sha256"]:
            mismatches.append(
                {"path": entry["path"], "expected": entry["sha256"], "actual": actual}
            )
    if mismatches:
        findings.append(
            {
                "rule": "ART-003",
                "severity": "high",
                "file": "manifest.json",
                "detail": "artifact hash does not match the manifest",
                "evidence": [item["path"] for item in mismatches],
                "remediation": "Regenerate the manifest from verified artifacts",
            }
        )

    if not (project_dir / "manifest.sig").exists():
        findings.append(
            {
                "rule": "ART-004",
                "severity": "medium",
                "file": "manifest.json",
                "detail": "manifest is not signed",
                "evidence": ["manifest.sig is missing"],
                "remediation": "Sign the manifest with a key held outside the repository",
            }
        )

    if not (project_dir / "sbom.json").exists():
        findings.append(
            {
                "rule": "ART-005",
                "severity": "medium",
                "file": "sbom.json",
                "detail": "no software bill of materials",
                "evidence": ["sbom.json is missing"],
                "remediation": "Emit an SBOM with pinned components and the model hash",
            }
        )

    by_rule = {finding["rule"]: 1 for finding in findings}
    summary = {
        "total": len(findings),
        "critical": sum(1 for finding in findings if finding["severity"] == "critical"),
        "high": sum(1 for finding in findings if finding["severity"] == "high"),
        "medium": sum(1 for finding in findings if finding["severity"] == "medium"),
        "by_rule": by_rule,
    }
    return {"findings": findings, "pickle_scan": pickle_scan, "summary": summary}


def harden_project(project_dir: Path, hardened_dir: Path) -> list[str]:
    if hardened_dir.exists():
        shutil.rmtree(hardened_dir)
    hardened_dir.mkdir(parents=True)

    requirements = "".join(f"{name}=={version}\n" for name, version in PINNED.items())
    (hardened_dir / "requirements.txt").write_text(requirements, encoding="utf-8", newline="\n")
    (hardened_dir / "load_model.py").write_text(SAFE_LOADER_SOURCE, encoding="utf-8", newline="\n")
    shutil.copy2(project_dir / "train.py", hardened_dir / "train.py")
    shutil.copy2(project_dir / "model.npz", hardened_dir / "model.npz")

    files = ["model.npz", "load_model.py", "requirements.txt", "train.py"]
    manifest = {
        "algorithm": "sha256",
        "files": [
            {
                "path": name,
                "sha256": sha256_file(hardened_dir / name),
                "bytes": (hardened_dir / name).stat().st_size,
            }
            for name in files
        ],
    }
    manifest_bytes = (
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    (hardened_dir / "manifest.json").write_bytes(manifest_bytes)
    (hardened_dir / "manifest.sig").write_text(
        sign_bytes(manifest_bytes) + "\n", encoding="utf-8", newline="\n"
    )

    components = [
        {
            "type": "library",
            "name": name,
            "version": version,
            "purl": f"pkg:pypi/{name.lower()}@{version}",
        }
        for name, version in PINNED.items()
    ]
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "version": 1,
        "metadata": {
            "component": {
                "type": "machine-learning-model",
                "name": "lab13-toy-model",
                "version": "1.0.0",
                "hashes": [
                    {"alg": "SHA-256", "content": sha256_file(hardened_dir / "model.npz")}
                ],
            }
        },
        "components": components,
    }
    write_json(hardened_dir / "sbom.json", sbom)

    return [
        "pinned all dependencies",
        "replaced the pickle loader with np.load(allow_pickle=False)",
        "excluded pickle artifacts from the hardened project",
        "regenerated the manifest from actual bytes",
        "signed the manifest with HMAC-SHA256",
        "emitted a minimal CycloneDX-style SBOM",
    ]


def verify_project(hardened_dir: Path, audit: dict) -> dict:
    manifest_bytes = (hardened_dir / "manifest.json").read_bytes()
    signature = (hardened_dir / "manifest.sig").read_text(encoding="utf-8").strip()
    manifest = json.loads(manifest_bytes)
    hashes_match = all(
        sha256_file(hardened_dir / entry["path"]) == entry["sha256"]
        for entry in manifest.get("files", [])
    )
    tampered = bytes([manifest_bytes[0] ^ 1]) + manifest_bytes[1:]
    requirements = [
        line.strip()
        for line in (hardened_dir / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    sbom = json.loads((hardened_dir / "sbom.json").read_text(encoding="utf-8"))
    return {
        "vulnerable_hash_match": audit["summary"]["by_rule"].get("ART-003") is None,
        "vulnerable_signature_present": audit["summary"]["by_rule"].get("ART-004") is None,
        "canary_flagged": bool(audit["pickle_scan"].get("canary.pkl")),
        "safe_pickle_flagged": bool(audit["pickle_scan"].get("model.pkl")),
        "hardened_hash_match": bool(hashes_match),
        "all_manifest_hashes_match": bool(hashes_match),
        "hardened_signature_valid": verify_signature(manifest_bytes, signature),
        "tampered_signature_valid": verify_signature(tampered, signature),
        "hardened_pickle_files": len(list(hardened_dir.glob("*.pkl"))),
        "hardened_pinned_dependencies": sum(1 for line in requirements if "==" in line),
        "sbom_components": len(sbom.get("components", [])),
    }


def ci_gate(audit: dict, verification: dict | None = None) -> int:
    """Return 1 when the gate blocks, 0 when it passes."""
    if verification is None:
        return 1 if audit["summary"]["total"] else 0
    checks = (
        verification["hardened_hash_match"],
        verification["hardened_signature_valid"],
        verification["hardened_pickle_files"] == 0,
        verification["hardened_pinned_dependencies"] == len(PINNED),
        verification["sbom_components"] == len(PINNED),
        not verification["tampered_signature_valid"],
    )
    return 0 if all(checks) else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit and harden a toy ML project.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    project_dir = build_project(args.out / "project")
    audit = audit_project(project_dir)
    actions = harden_project(project_dir, args.out / "hardened")
    verification = verify_project(args.out / "hardened", audit)
    gates = {
        "vulnerable_exit": ci_gate(audit),
        "hardened_exit": ci_gate(audit, verification),
    }

    write_json(args.out / "audit.json", audit)
    metrics = {
        "project": "toy ML project with benign artifacts",
        "audit": audit["summary"],
        "pickle_scan": audit["pickle_scan"],
        "verification": verification,
        "gate": gates,
        "remediation": actions,
        "signing": {"algorithm": "HMAC-SHA256", "key": "demo key embedded in the lab; not a secret"},
    }
    write_json(args.out / "metrics.json", metrics)
    write_json(
        args.out / "run.json",
        {
            "lab": "LAB-13",
            "seed": 0,
            "findings": audit["summary"]["total"],
            "environment": environment(),
        },
    )
    (args.out / "report.md").write_text(build_report(metrics), encoding="utf-8", newline="\n")
    write_json(
        args.out / "manifest.json",
        build_manifest(args.out, ["audit.json", "metrics.json", "run.json", "report.md"]),
    )

    print(f"findings={audit['summary']['total']} {audit['summary']['by_rule']}")
    print(f"canary flagged={verification['canary_flagged']} safe pickle flagged={verification['safe_pickle_flagged']}")
    print(
        f"hardened hash={verification['hardened_hash_match']} "
        f"signature={verification['hardened_signature_valid']} "
        f"tampered={verification['tampered_signature_valid']}"
    )
    print(f"gates vulnerable={gates['vulnerable_exit']} hardened={gates['hardened_exit']}")
    print(f"artifacts written to {args.out}")


def build_report(metrics: dict) -> str:
    audit = metrics["audit"]
    verification = metrics["verification"]
    lines = [
        "# LAB-13 report — supply-chain audit",
        "",
        "## Findings",
        "",
        "| Rule | Severity | Count |",
        "|---|---|---:|",
        f"| DEP-001 unpinned dependencies | high | "
        f"{1 if 'DEP-001' in audit['by_rule'] else 0} |",
        f"| ART-001 unsafe loader | high | {1 if 'ART-001' in audit['by_rule'] else 0} |",
        f"| ART-002 dangerous pickle opcodes | critical | "
        f"{1 if 'ART-002' in audit['by_rule'] else 0} |",
        f"| ART-003 hash mismatch | high | {1 if 'ART-003' in audit['by_rule'] else 0} |",
        f"| ART-004 unsigned manifest | medium | {1 if 'ART-004' in audit['by_rule'] else 0} |",
        f"| ART-005 missing SBOM | medium | {1 if 'ART-005' in audit['by_rule'] else 0} |",
        f"| **Total** | | **{audit['total']}** |",
        "",
        "The pickle scan is static: the canary stream is read with `pickletools`",
        "and never unpickled. The safe pickle contains no callable-construction",
        "opcodes.",
        "",
        "## Verification after hardening",
        "",
        "| Check | Result |",
        "|---|---|",
        f"| Manifest hashes match | {verification['hardened_hash_match']} |",
        f"| HMAC signature valid | {verification['hardened_signature_valid']} |",
        f"| Tampered manifest rejected | {not verification['tampered_signature_valid']} |",
        f"| Pickle files remaining | {verification['hardened_pickle_files']} |",
        f"| Pinned dependencies | {verification['hardened_pinned_dependencies']} |",
        f"| SBOM components | {verification['sbom_components']} |",
        "",
        f"The CI gate blocks the vulnerable project (exit {metrics['gate']['vulnerable_exit']}) "
        f"and passes the hardened project (exit {metrics['gate']['hardened_exit']}).",
        "",
        "## Limitations",
        "",
        "- The signing key is a demo constant, not a secret-management solution.",
        "- The SBOM lists pinned components and the model hash; it does not hash",
        "  downloaded wheels.",
        "- Static pickle scanning finds known dangerous opcodes, not every unsafe",
        "  data flow.",
        "- The toy project is small; a real audit covers transitive dependencies,",
        "  build provenance, and CI identity.",
        "- A passing gate means these checks passed, not that the supply chain is secure.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
