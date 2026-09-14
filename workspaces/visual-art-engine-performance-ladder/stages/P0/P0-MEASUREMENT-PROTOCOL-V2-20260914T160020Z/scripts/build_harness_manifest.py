#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HARNESS_FILES = (
    "scripts/run_measurement_v2.py",
    "scripts/start-label-blind-aa-comfyui.ps1",
    "scripts/invoke-start-label-blind-aa-comfyui.ps1",
    "decision-rules.json",
    "scripts/bracket_summary.py",
    "contracts/p0-workflow.json",
    "assets/black-256.png",
)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def load_runner(path: Path):
    spec = importlib.util.spec_from_file_location("measurement_v2_manifest_target", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("runner import spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    stage = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else stage / "harness-manifest-label-blind.json"
    entries = []
    for relative in HARNESS_FILES:
        path = stage / relative
        data = path.read_bytes()
        entries.append({"path": relative, "bytes": len(data), "sha256": sha_bytes(data)})

    runner = load_runner(stage / "scripts" / "run_measurement_v2.py")
    workflow_path = stage / "contracts" / "p0-workflow.json"
    a_artifact = runner.artifact_identity("AA", 1, "0123456789ab")
    b_artifact = runner.artifact_identity("AA", 2, "fedcba987654")
    a_workflow = runner.workflow(workflow_path, a_artifact["run_prefix"])
    b_workflow = runner.workflow(workflow_path, b_artifact["run_prefix"])
    a_normalized = runner.normalized_workflow_sha(a_workflow)
    b_normalized = runner.normalized_workflow_sha(b_workflow)
    timed_leak = runner.label_leak_count(a_artifact, b_artifact)
    workflow_leak = runner.label_leak_count(a_workflow, b_workflow)
    http_leak = runner.label_leak_count(
        "/prompt",
        "/history/{opaque_prompt_id}",
        "/view",
        {"filename": "opaque-output.png", "subfolder": "p0-v2\\AA", "type": "output"},
    )
    equal = a_normalized == b_normalized
    if timed_leak or workflow_leak or http_leak or not equal:
        raise RuntimeError("label-blind harness gate failed")

    payload = {
        "schema_version": 1,
        "fingerprint_algorithm": "SHA256_OF_CANONICAL_JSON_PAYLOAD",
        "files": entries,
        "label_blind_gates": {
            "A_NORMALIZED_WORKFLOW_SHA": a_normalized,
            "B_NORMALIZED_WORKFLOW_SHA": b_normalized,
            "NORMALIZED_A_B_WORKFLOW_EQUAL": "YES" if equal else "NO",
            "TIMED_PATH_LABEL_LEAK": timed_leak,
            "WORKFLOW_LABEL_LEAK": workflow_leak,
            "HTTP_LABEL_LEAK": http_leak,
        },
    }
    result = {
        **payload,
        "RUNNER_SHA": next(item["sha256"] for item in entries if item["path"] == "scripts/run_measurement_v2.py"),
        "HARNESS_MANIFEST_SHA": sha_bytes(canonical_bytes(payload)),
        "superseded_runner": {
            "sha256": "8f5c3a592ba18a0570b5213996bdbb4f9618f178d0bd80af16f0c56e912d4062",
            "status": "SUPERSEDED_LABEL_BLIND_RUNNER",
        },
    }
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    output.write_text(encoded, encoding="utf-8")
    print(json.dumps({
        "output": str(output),
        "RUNNER_SHA": result["RUNNER_SHA"],
        "HARNESS_MANIFEST_SHA": result["HARNESS_MANIFEST_SHA"],
        **result["label_blind_gates"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
