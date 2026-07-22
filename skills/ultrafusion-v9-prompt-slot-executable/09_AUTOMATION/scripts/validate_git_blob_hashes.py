from __future__ import annotations

import hashlib
import json
import subprocess
import sys

from common import EVIDENCE, ROOT, load_registry, sha256, write_json


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    repo_check = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--is-inside-work-tree"], capture_output=True, text=True)
    in_git = repo_check.returncode == 0 and repo_check.stdout.strip() == "true"
    results = []
    failures = []
    for item in load_registry()["assets"]:
        rel = item["relative_path"]
        repo_rel = f"UltraFusion_V9.0_ReadOnly_Executable_SkillPack/{rel}"
        if in_git:
            proc = subprocess.run(["git", "-C", str(ROOT), "show", f":{repo_rel}"], capture_output=True)
            digest = hashlib.sha256(proc.stdout).hexdigest().upper() if proc.returncode == 0 else None
            passed = proc.returncode == 0 and digest == item["sha256"]
            method = "git_index_blob"
        else:
            local = ROOT / rel
            digest = sha256(local) if local.is_file() else None
            passed = digest == item["sha256"]
            method = "installed_copy_bytes"
        if not passed:
            failures.append(item["asset_id"])
        results.append({"asset_id": item["asset_id"], "path": repo_rel if in_git else rel, "method": method, "content_sha256": digest, "expected_sha256": item["sha256"], "passed": passed})
    report = {"status": "PASS" if not failures else "FAIL", "in_git_worktree": in_git, "failures": failures, "results": results}
    write_json(EVIDENCE / "git-blob-hash-validation.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

