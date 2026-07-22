from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from common import EVIDENCE, load_registry, sha256, write_json


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=EVIDENCE / "core-source-inventory.json")
    args = parser.parse_args()
    rows = []
    failures = []
    for item in load_registry()["assets"]:
        path = Path(item["source_path"])
        row = {"asset_id": item["asset_id"], "path": str(path), "exists": path.is_file()}
        if path.is_file():
            stat = path.stat()
            row.update({
                "file_size": stat.st_size,
                "sha256": sha256(path),
                "last_modified": dt.datetime.fromtimestamp(stat.st_mtime).astimezone().isoformat(timespec="seconds"),
            })
        else:
            failures.append(item["asset_id"])
        rows.append(row)
    write_json(args.output, {"schema_version": "1.0", "assets": rows, "missing": failures})
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

