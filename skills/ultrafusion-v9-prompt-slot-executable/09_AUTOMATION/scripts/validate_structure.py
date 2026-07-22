from __future__ import annotations

import json
import sys

from common import EVIDENCE, ROOT, write_json


REQUIRED = [
    "SKILL.md", "00_README/README.md", "00_README/QUICK_START.md",
    "01_ARCHITECTURE/SYSTEM_ARCHITECTURE.md", "01_ARCHITECTURE/STATE_MACHINE.md",
    "02_CORE_ASSETS/CORE_ASSET_REGISTRY.json", "02_CORE_ASSETS/CORE_ASSET_PROTECTION_POLICY.md",
    "03_PROMPT_REGISTRY/PROMPT_REGISTRY.json", "03_PROMPT_REGISTRY/P_CORE.slot.json",
    "03_PROMPT_REGISTRY/P_A.slot.json", "03_PROMPT_REGISTRY/P_B.slot.json",
    "03_PROMPT_REGISTRY/P_C.slot.json", "03_PROMPT_REGISTRY/P_D.slot.json",
    "03_PROMPT_REGISTRY/P_VALUE.slot.json", "04_COMMAND_PACKAGE_REGISTRY/COMMAND_PACKAGE_REGISTRY.json",
    "05_MANUAL_M1/MANUAL_M1_SOP.md", "05_MANUAL_M1/RUN_MANIFEST.template.json",
    "06_STAGE_CONTRACTS/A_INITIAL_CONTRACT.md", "06_STAGE_CONTRACTS/A_STAGE_CONTRACT.md",
    "06_STAGE_CONTRACTS/B_STAGE_CONTRACT.md", "06_STAGE_CONTRACTS/C_STAGE_CONTRACT.md",
    "06_STAGE_CONTRACTS/D_STAGE_CONTRACT.md", "06_STAGE_CONTRACTS/VALUE_COMPARISON_CONTRACT.md",
    "07_SECURITY_AND_ROLLBACK/ROLLBACK_RUNBOOK.md", "08_VALIDATION/TEST_MATRIX.md",
    "09_AUTOMATION/scripts/run_static_acceptance.py", "09_AUTOMATION/tests/run_three_rounds.py",
    "10_WEB_W1_SPEC/API_CONTRACT.md", "10_WEB_W1_SPEC/MANUAL_WEB_EQUIVALENCE.md",
    "11_MIGRATION/LEGACY_VERSION_MAP.md", "12_RELEASE/KNOWN_LIMITATIONS.md",
    "13_RUNS/.gitkeep", "references/FAILURE_REVIEW_ENTRY.md", "RECENT_USE_LOG.md"
]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    missing = [item for item in REQUIRED if not (ROOT / item).is_file()]
    report = {"required_count": len(REQUIRED), "missing": missing, "status": "PASS" if not missing else "FAIL"}
    write_json(EVIDENCE / "structure-validation.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())

