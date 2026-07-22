from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from common import EVIDENCE, ROOT, write_text


SCRIPTS = [
    "inventory_core_assets.py",
    "verify_readonly_assets.py",
    "validate_hashes.py",
    "validate_git_blob_hashes.py",
    "validate_structure.py",
    "validate_registry.py",
    "validate_state_machine.py",
    "validate_git_safety.py",
]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    script_dir = Path(__file__).resolve().parent
    sections = []
    failed = []
    for name in SCRIPTS:
        proc = subprocess.run([sys.executable, str(script_dir / name)], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        sections.append(f"## {name}\n\n```text\n{proc.stdout}{proc.stderr}\n```\n")
        if proc.returncode:
            failed.append(name)
    status = "PASS" if not failed else "FAIL"
    codes = [] if failed else [
        "UF9_REPOSITORY_SAFETY_PASS", "UF9_CORE_ASSET_INVENTORY_PASS",
        "UF9_CORE_ASSETS_READONLY_PASS", "UF9_FRAMEWORK_STATIC_PASS"
    ]
    report = "# ROUND1 STRUCTURE + READONLY REPORT\n\n" + f"Status: `{status}`\n\n" + "\n".join(f"- `{code}`" for code in codes) + "\n\n" + "\n".join(sections)
    write_text(EVIDENCE / "ROUND1_STRUCTURE_READONLY_REPORT.md", report)
    print(report)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
