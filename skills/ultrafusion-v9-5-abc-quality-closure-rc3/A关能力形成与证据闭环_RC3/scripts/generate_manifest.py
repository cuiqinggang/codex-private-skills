from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "00_先看这里" / "FILE_MANIFEST.json"
CHECKSUMS = ROOT / "00_先看这里" / "SHA256_文件校验清单.txt"
EXCLUDED = {MANIFEST.resolve(), CHECKSUMS.resolve()}


def main() -> None:
    entries: list[dict[str, object]] = []
    for path in sorted(ROOT.rglob("*"), key=lambda item: item.as_posix()):
        if not path.is_file() or path.resolve() in EXCLUDED or "__pycache__" in path.parts:
            continue
        data = path.read_bytes()
        entries.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": hashlib.sha256(data).hexdigest().upper(),
                "size": len(data),
            }
        )

    MANIFEST.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    CHECKSUMS.write_text(
        "".join(f"{entry['sha256']}  {entry['path']}\n" for entry in entries),
        encoding="utf-8",
    )
    print(json.dumps({"status": "PASS", "entries": len(entries)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
