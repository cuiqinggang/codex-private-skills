#!/usr/bin/env python3
"""Static/semantic validation for visual-art-engine-performance-ladder."""

from __future__ import annotations

import hashlib
import json
import re
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METHOD = Path(r"C:\Users\A\.codex\skills\mature-replication-four-column")
EXPECTED_METHOD_HASH = "3813a15c3493a4446e9362e6e61238412eb8f395bd65727c540af4f19f263d32"

REQUIRED = [
    "SKILL.md", "VERSION", "CHANGELOG.md",
    "docs/ARCHITECTURE.md", "docs/VERSIONING.md", "docs/PERFORMANCE-LADDER.md",
    "docs/FREEZE-REOPEN-RULES.md", "docs/RUNTIME-VS-CERTIFICATION.md",
    "methodology/FOUR-COLUMN-INTEGRATION.md", "methodology/FIRST-PRINCIPLES-RULES.md",
    "contracts/P0-BENCHMARK-CONTRACT.md", "contracts/p0-workflow.json",
    "templates/FOUR-COLUMN-STAGE-TEMPLATE.md", "templates/STAGE-EVIDENCE-TEMPLATE.md",
    "templates/FREEZE-MANIFEST-TEMPLATE.md", "state/STAGE-LEDGER.json",
    "state/CURRENT-STATE.md", "scripts/p0/prepare-p0.ps1",
    "scripts/p0/run-p0-control.py", "references/METHODOLOGY-DEPENDENCY.md",
    "assets/p0/black-256.png", "evidence/HISTORICAL-EVIDENCE.md",
]
REQUIRED += [
    "stages/P0-COMFYUI-CONTROL.md", "stages/P1-MINIMAL-AI-IMAGE.md",
    "stages/P2-BASE-IMAGE.md", "stages/P3-ADDED-COMPONENTS.md",
    "stages/P4-ADVANCED-IMAGE.md", "stages/P5-MINIMAL-VIDEO.md",
    "stages/P6-PRODUCTION-WAN.md", "stages/P7-MINIMAL-H3.md",
    "stages/P8-PRODUCTION-H3.md",
]


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    missing = [item for item in REQUIRED if not (ROOT / item).is_file()]
    if missing:
        fail(f"missing required files: {missing}")
    if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != "1.0.0":
        fail("VERSION must be 1.0.0")

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for token in [
        "name: visual-art-engine-performance-ladder",
        'version: "1.0.0"',
        "mature-replication-four-column",
        "P0_CURRENT=PENDING",
        "P0_BENCHMARK_EXECUTED=NO",
    ]:
        if token not in skill:
            fail(f"SKILL.md missing {token}")

    method_skill = METHOD / "SKILL.md"
    if not method_skill.is_file():
        fail("formal V4.0 method skill is missing")
    method_bytes = method_skill.read_bytes()
    method_hash = hashlib.sha256(method_bytes).hexdigest()
    if method_hash != EXPECTED_METHOD_HASH:
        fail(f"method entrypoint hash changed: {method_hash}")
    method_text = method_bytes.decode("utf-8-sig")
    for token in [
        'version: "4.0.0"',
        "CURRENT", "EXTERNAL FRONTIER",
        "FIRST-PRINCIPLES PHYSICAL TIME", "ITERATIVE CONVERGENCE",
        "T_PHY", "PHYSICAL_GAP", "PATH_ARCHITECTURE_ERROR",
    ]:
        if token not in method_text:
            fail(f"formal method missing {token}")

    ledger = json.loads((ROOT / "state" / "STAGE-LEDGER.json").read_text(encoding="utf-8"))
    stages = ledger.get("stages", [])
    if [stage["stage"] for stage in stages] != [f"P{i}" for i in range(9)]:
        fail("stage order must be P0-P8")
    required_fields = {
        "stage", "name", "task_contract", "status", "current",
        "external_frontier", "t_phy", "t_phy_range", "best_time",
        "physical_gap", "delta_t_stage", "score_99", "frozen",
        "freeze_version", "reopen_reason", "fallback_version", "evidence_path",
    }
    for stage in stages:
        if set(stage) != required_fields:
            fail(f"ledger fields differ for {stage.get('stage')}")
        for key in ("current", "external_frontier", "t_phy", "t_phy_range", "best_time", "physical_gap"):
            if stage[key] is not None:
                fail(f"{stage['stage']} contains unverified performance data in {key}")
        if stage["score_99"] or stage["frozen"]:
            fail(f"{stage['stage']} must not be 99/frozen in v1.0.0")
    if stages[0]["status"] != "READY_TO_MEASURE":
        fail("P0 must be READY_TO_MEASURE")
    if any(stage["status"] != "LOCKED_BY_PREVIOUS_STAGE" for stage in stages[1:]):
        fail("P1-P8 must be locked")

    workflow = json.loads((ROOT / "contracts" / "p0-workflow.json").read_text(encoding="utf-8"))
    if [workflow["1"]["class_type"], workflow["2"]["class_type"]] != ["LoadImage", "SaveImage"]:
        fail("P0 workflow node classes changed")
    if workflow["1"]["inputs"]["image"] != "p0-control-black-256.png":
        fail("P0 fixture name changed")

    png = (ROOT / "assets" / "p0" / "black-256.png").read_bytes()
    if not png.startswith(b"\x89PNG\r\n\x1a\n"):
        fail("fixture is not PNG")
    width, height = struct.unpack(">II", png[16:24])
    if (width, height) != (256, 256):
        fail("fixture must be 256x256")
    if b"IDAT" not in png or b"IEND" not in png:
        fail("fixture PNG is incomplete")

    p0 = (ROOT / "stages" / "P0-COMFYUI-CONTROL.md").read_text(encoding="utf-8")
    for token in [
        "CURRENT", "PENDING_MEASUREMENT", "EXTERNAL_FRONTIER",
        "PENDING_RESEARCH", "FIRST_PRINCIPLES_PHYSICAL_TIME",
        "PENDING_DERIVATION", "ITERATIVE_CONVERGENCE", "LOCKED",
        "P0_99=NO", "P0_BENCHMARK_EXECUTED=NO",
    ]:
        if token not in p0:
            fail(f"P0 stage missing {token}")

    all_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".yaml", ".py", ".ps1"}
    )
    forbidden_claims = [
        r"P0_CURRENT\s*=\s*\d",
        r"P0_99\s*=\s*YES",
        r"P0_BENCHMARK_EXECUTED\s*=\s*YES",
        r"PERFORMANCE_OPTIMIZATION_RUN\s*=\s*YES",
        r"H3_RUN\s*=\s*YES",
    ]
    for pattern in forbidden_claims:
        if re.search(pattern, all_text):
            fail(f"forbidden performance claim matched: {pattern}")

    result = {
        "status": "PASS",
        "skill_id": "visual-art-engine-performance-ladder",
        "version": "1.0.0",
        "required_files": len(REQUIRED),
        "stages": 9,
        "method_version": "4.0.0",
        "method_entrypoint_sha256": method_hash.upper(),
        "p0_benchmark_executed": False,
        "performance_optimization_run": False,
        "h3_run": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
