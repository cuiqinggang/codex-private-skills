from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

from common import EVIDENCE, load_registry, sha256, write_json


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    results = []
    failures = []
    for item in load_registry()["assets"]:
        path = Path(item["source_path"])
        checks = {"exists": path.is_file()}
        if path.is_file():
            stat = path.stat()
            expected_time = dt.datetime.fromisoformat(item["last_modified"]).timestamp()
            checks.update({
                "name_unchanged": path.name == Path(item["source_path"]).name,
                "size_unchanged": stat.st_size == item["file_size"],
                "sha256_unchanged": sha256(path) == item["sha256"],
                "mtime_unchanged": abs(stat.st_mtime - expected_time) < 1.5,
            })
        passed = all(checks.values())
        if not passed:
            failures.append(item["asset_id"])
        results.append({"asset_id": item["asset_id"], "path": str(path), "checks": checks, "passed": passed})
    report = {"status": "PASS" if not failures else "FAIL", "failures": failures, "results": results}
    write_json(EVIDENCE / "core-source-after.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failures:
        print("UF9_CORE_ASSETS_READONLY_FAIL")
        return 1
    print("UF9_CORE_ASSETS_READONLY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

