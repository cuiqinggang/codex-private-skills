from __future__ import annotations
import argparse, hashlib
from pathlib import Path

EXCLUDE = {"MANIFEST_SHA256.txt", "SELF_TEST_RESULT.json"}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--output", default="MANIFEST_SHA256.txt")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    lines = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.name in EXCLUDE:
            continue
        rel = p.relative_to(root).as_posix()
        lines.append(f"{sha256(p)}  {rel}")
    out = root / args.output
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"已写入 {out}，共 {len(lines)} 项")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
