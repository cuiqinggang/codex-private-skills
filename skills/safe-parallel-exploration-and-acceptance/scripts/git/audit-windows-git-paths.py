from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


INVALID_CHARS = set('<>:"\\|?*')
RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}


def segment_reasons(segment: str) -> list[str]:
    reasons: list[str] = []
    if segment.endswith(" "):
        reasons.append("TRAILING_SPACE")
    if segment.endswith("."):
        reasons.append("TRAILING_DOT")
    if any(ch in INVALID_CHARS for ch in segment):
        reasons.append("WINDOWS_INVALID_CHARACTER")
    if any(ord(ch) < 32 for ch in segment):
        reasons.append("CONTROL_CHARACTER")
    base = segment.rstrip(" .").split(".", 1)[0].upper()
    if base in RESERVED:
        reasons.append("WINDOWS_RESERVED_NAME")
    return reasons


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Audit a Git tree before Windows checkout/worktree creation.")
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--revision", default="HEAD")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    proc = subprocess.run(
        ["git", "-c", "core.quotepath=false", "-C", str(args.repository), "ls-tree", "-r", "--name-only", "-z", args.revision],
        capture_output=True,
    )
    if proc.returncode != 0:
        result = {"status": "ERROR", "repository": str(args.repository), "revision": args.revision, "git_error": proc.stderr.decode("utf-8", "replace")}
        code = 3
    else:
        names = [raw.decode("utf-8", "surrogateescape") for raw in proc.stdout.split(b"\0") if raw]
        blocked = []
        warnings = []
        for name in names:
            reasons = sorted({reason for segment in name.split("/") for reason in segment_reasons(segment)})
            if reasons:
                blocked.append({"path": name, "reasons": reasons})
            if len(name) > 240:
                warnings.append({"path": name, "reason": "LONG_WINDOWS_PATH"})
        result = {
            "status": "WINDOWS_PATH_BLOCKED" if blocked else "PASS",
            "repository": str(args.repository.resolve()),
            "revision": args.revision,
            "paths_scanned": len(names),
            "blocked_count": len(blocked),
            "blocked_paths": blocked,
            "warnings": warnings,
        }
        code = 2 if blocked else 0
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return code


if __name__ == "__main__":
    raise SystemExit(main())

