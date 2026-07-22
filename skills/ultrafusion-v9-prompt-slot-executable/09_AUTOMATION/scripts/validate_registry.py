from __future__ import annotations

import json
import sys

from common import EVIDENCE, ROOT, load_registry, write_json


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    errors = []
    registry = load_registry()
    assets = {item["asset_id"]: item for item in registry["assets"]}
    required_assets = {"A_INITIAL", "P_CORE", "P_A", "P_B", "P_C", "P_D", "CP_A", "CP_B", "CP_C", "CP_D"}
    if set(assets) != required_assets:
        errors.append(f"asset ids mismatch: {sorted(set(assets) ^ required_assets)}")
    fields = {"asset_id", "asset_name", "asset_type", "logical_role", "source_path", "relative_path", "version", "encoding", "file_size", "sha256", "last_modified", "readonly_status", "load_status", "compatibility_status", "notes"}
    for asset_id, item in assets.items():
        missing = sorted(fields - set(item))
        if missing:
            errors.append(f"{asset_id} missing {missing}")
        if item.get("readonly_status") != "LOCKED_READONLY":
            errors.append(f"{asset_id} not LOCKED_READONLY")
    prompts = read_json("03_PROMPT_REGISTRY/PROMPT_REGISTRY.json")
    slots = {item["slot_id"] for item in prompts["slots"]}
    if slots != {"P_CORE", "P_A", "P_B", "P_C", "P_D", "P_VALUE"}:
        errors.append("prompt slots incomplete")
    commands = read_json("04_COMMAND_PACKAGE_REGISTRY/COMMAND_PACKAGE_REGISTRY.json")
    if {item["package_id"] for item in commands["packages"]} != {"CP_A", "CP_B", "CP_C", "CP_D"}:
        errors.append("command packages incomplete")
    report = {"status": "PASS" if not errors else "FAIL", "errors": errors}
    write_json(EVIDENCE / "registry-validation.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

