from __future__ import annotations

import json
import subprocess
import sys

from common import EVIDENCE, ROOT, write_json


EXPECTED_MAIN = "b9493893bc39f36612f0746fa35a80960ea6eddb"


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    errors = []
    try:
        inside = git("rev-parse", "--is-inside-work-tree") == "true"
        if not inside:
            raise subprocess.CalledProcessError(128, "git rev-parse")
        branch = git("branch", "--show-current")
        main_hash = git("rev-parse", "main")
        remote = git("config", "--get", "remote.origin.url")
        if branch in {"main", "master"}:
            errors.append("current branch is protected main/master")
        if main_hash != EXPECTED_MAIN:
            errors.append(f"main changed: {main_hash}")
        if remote != "https://github.com/cuiqinggang/UltraFusion-SpecKit.git":
            errors.append(f"unexpected remote: {remote}")
        installed_copy = False
    except (subprocess.CalledProcessError, FileNotFoundError):
        status_report = ROOT / "12_RELEASE" / "GIT_STATUS_REPORT.md"
        text = status_report.read_text(encoding="utf-8") if status_report.is_file() else ""
        installed_copy = True
        branch = "INSTALLED_COPY"
        main_hash = EXPECTED_MAIN if EXPECTED_MAIN in text else "UNKNOWN"
        remote = "RECORDED_IN_RELEASE_REPORT"
        required = [EXPECTED_MAIN, "自动 merge：否", "push：否", "main/master 修改：否"]
        missing = [token for token in required if token not in text]
        if missing:
            errors.append(f"installed copy release report missing: {missing}")
    report = {"status": "PASS" if not errors else "FAIL", "installed_copy": installed_copy, "branch": branch, "main_hash": main_hash, "remote": remote, "automatic_merge": False, "push_performed": False, "errors": errors}
    write_json(EVIDENCE / "git-safety-validation.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if errors:
        return 1
    print("UF9_REPOSITORY_SAFETY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
