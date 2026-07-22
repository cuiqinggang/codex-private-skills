from __future__ import annotations

import json
import sys

from common import EVIDENCE, ROOT, write_json


DEPLOY = ["INIT", "ENV_DISCOVERED", "BASELINE_PROTECTED", "CORE_ASSETS_INVENTORIED", "CORE_ASSETS_HASHED", "CORE_ASSETS_LOCKED_READONLY", "CORE_ASSETS_REGISTERED", "V9_FRAMEWORK_CREATED", "MANUAL_M1_READY", "VALIDATION_RUNNING", "RELEASE_CANDIDATE", "USER_DECISION_REQUIRED"]
RUN = ["RUN_CREATED", "QUESTION_REGISTERED", "A_INITIAL_GENERATED", "A_INITIAL_SEALED", "A_STAGE_READY", "A_STAGE_COMPLETE", "B_STAGE_READY", "B_STAGE_COMPLETE", "C_STAGE_READY", "C_STAGE_COMPLETE", "D_STAGE_READY", "D_FINAL_LOCKED", "A_INITIAL_COMPARISON_COPY_OPENED", "VALUE_COMPARISON_COMPLETE"]
EXCEPTIONS = ["BLOCKED", "FAILED", "PARTIAL_PASS", "ROLLED_BACK", "CORE_ASSET_MISMATCH", "READONLY_VIOLATION", "NEEDS_USER_AUTHORIZATION"]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    text = (ROOT / "01_ARCHITECTURE" / "STATE_MACHINE.md").read_text(encoding="utf-8")
    missing = [token for token in DEPLOY + RUN + EXCEPTIONS if token not in text]
    report = {"status": "PASS" if not missing else "FAIL", "missing_tokens": missing}
    write_json(EVIDENCE / "state-machine-validation.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())

