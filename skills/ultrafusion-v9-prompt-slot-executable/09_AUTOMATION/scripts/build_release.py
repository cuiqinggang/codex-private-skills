from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

from common import ROOT, sha256


def included(path: Path) -> bool:
    parts = set(path.parts)
    return not ({"__pycache__", ".git", ".cache"} & parts) and path.suffix.lower() not in {".pyc"}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sums = ROOT / "12_RELEASE" / "SHA256SUMS.txt"
    files = sorted(path for path in ROOT.rglob("*") if path.is_file() and included(path) and path != sums)
    sums.write_text("\n".join(f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}" for path in files) + "\n", encoding="utf-8")
    files.append(sums)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(files):
            archive.write(path, f"UltraFusion_V9.0_ReadOnly_Executable_SkillPack/{path.relative_to(ROOT).as_posix()}")
    print(f"ZIP={args.output}")
    print(f"SHA256={sha256(args.output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

