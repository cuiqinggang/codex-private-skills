from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Verify locked assets in working copy and optionally Git index.")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--git-index", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
    rows, failures = [], []
    for item in manifest["assets"]:
        rel = item["path"].replace("\\", "/")
        file_path = args.root / Path(rel)
        working_hash = digest(file_path.read_bytes()) if file_path.is_file() else None
        working_ok = working_hash == item["sha256"].upper()
        index_hash = None
        index_ok = None
        if args.git_index:
            proc = subprocess.run(["git", "-C", str(args.root), "show", f":{rel}"], capture_output=True)
            index_hash = digest(proc.stdout) if proc.returncode == 0 else None
            index_ok = index_hash == item["sha256"].upper()
        passed = working_ok and (index_ok is not False)
        if not passed:
            failures.append(item["asset_id"])
        rows.append({"asset_id": item["asset_id"], "path": rel, "working_sha256": working_hash, "working_ok": working_ok, "git_index_sha256": index_hash, "git_index_ok": index_ok, "passed": passed})
    result = {"status": "PASS" if not failures else "EXACT_BYTE_MISMATCH", "root": str(args.root.resolve()), "git_index_checked": args.git_index, "failures": failures, "results": rows}
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())

