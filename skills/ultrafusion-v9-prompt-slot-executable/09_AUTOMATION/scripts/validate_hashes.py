from __future__ import annotations

import json
import os
import stat
import sys
from pathlib import Path

from common import EVIDENCE, ROOT, load_registry, sha256, write_json


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    results = []
    failures = []
    for item in load_registry()["assets"]:
        path = ROOT / Path(item["relative_path"])
        exists = path.is_file()
        hash_ok = exists and sha256(path) == item["sha256"]
        size_ok = exists and path.stat().st_size == item["file_size"]
        readonly_ok = True
        if exists and os.name == "nt" and hasattr(path.stat(), "st_file_attributes"):
            readonly_ok = bool(path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY)
        passed = exists and hash_ok and size_ok and readonly_ok
        if not passed:
            failures.append(item["asset_id"])
        results.append({"asset_id": item["asset_id"], "copy_path": str(path), "exists": exists, "hash_ok": hash_ok, "size_ok": size_ok, "readonly_ok": readonly_ok, "passed": passed})
    report = {"status": "PASS" if not failures else "FAIL", "failures": failures, "results": results}
    write_json(EVIDENCE / "readonly-copy-validation.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

