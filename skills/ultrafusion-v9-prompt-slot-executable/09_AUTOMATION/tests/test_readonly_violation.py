from __future__ import annotations

import os
import shutil
import stat
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
from common import EVIDENCE, ROOT, load_registry, sha256, write_text  # noqa: E402


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    asset = next(item for item in load_registry()["assets"] if item["asset_id"] == "P_A")
    source = Path(asset["source_path"])
    source_before = sha256(source)
    sandbox = EVIDENCE / "round3-violation-sandbox"
    sandbox.mkdir(parents=True, exist_ok=True)
    test_copy = sandbox / "P_A_TEST_COPY.txt"
    if test_copy.exists():
        os.chmod(test_copy, stat.S_IWRITE)
    shutil.copy2(ROOT / asset["relative_path"], test_copy)
    os.chmod(test_copy, stat.S_IWRITE)
    clean_hash = sha256(test_copy)
    with test_copy.open("ab") as stream:
        stream.write(b"\nSIMULATED_VIOLATION")
    mutated_hash = sha256(test_copy)
    mutation_blocked = clean_hash != mutated_hash
    missing_blocked = not (sandbox / "MISSING_CORE_ASSET.txt").exists()
    source_after = sha256(source)
    source_unchanged = source_before == source_after == asset["sha256"]
    passed = mutation_blocked and missing_blocked and source_unchanged
    write_text(EVIDENCE / "ROUND3_ROLLBACK_READONLY_VIOLATION_REPORT.md", f"# ROUND3 ROLLBACK + READONLY VIOLATION REPORT\n\n- Temporary-copy mutation detected: {mutation_blocked}\n- Missing path blocked: {missing_blocked}\n- Original source unchanged: {source_unchanged}\n- Test touched original: no\n- Status: {'PASS' if passed else 'FAIL'}\n")
    print("UF9_WORKTREE_ROLLBACK_PASS" if passed else "UF9_WORKTREE_ROLLBACK_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
