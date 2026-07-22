from __future__ import annotations
import argparse
from pathlib import Path
from common import iter_files, rel_posix, sha256_file


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate SHA-256 manifest")
    ap.add_argument("root")
    ap.add_argument("--output", default="MANIFEST_SHA256.txt")
    ap.add_argument("--exclude", action="append", default=[])
    args = ap.parse_args()
    root = Path(args.root).resolve()
    out = Path(args.output)
    if not out.is_absolute():
        out = root / out
    lines = []
    for p in iter_files(root, args.exclude + [out.relative_to(root).as_posix()] if out.is_relative_to(root) else args.exclude):
        lines.append(f"{sha256_file(p)}  {rel_posix(p, root)}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE {len(lines)} entries: {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
