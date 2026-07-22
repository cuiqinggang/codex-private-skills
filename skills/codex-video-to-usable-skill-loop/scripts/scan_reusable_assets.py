#!/usr/bin/env python
"""Scan known Codex memory locations for reusable skills, SOPs, rules, and reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


HOT_ROOTS = [
${REDACTED_SECRET}
${REDACTED_SECRET}
]

BACKUP_ROOTS = [
    Path(r"K:\AI\skills"),
    Path(r"K:\AI\workspaces"),
]

INTERESTING_NAMES = {
    "SKILL.md",
    "AGENTS.md",
    "README.md",
}

INTERESTING_PATTERNS = (
    "SOP",
    "RULE",
    "CHECKLIST",
    "FAILURE",
    "REVIEW_READY",
    "PASS",
    "USAGE-LOG",
)


def is_interesting(path: Path) -> bool:
    name = path.name.upper()
    if path.name in INTERESTING_NAMES:
        return True
    return any(pattern in name for pattern in INTERESTING_PATTERNS)


def scan(root: Path, limit: int) -> list[dict[str, str]]:
    matches: list[dict[str, str]] = []
    if not root.exists():
        return matches
    for path in root.rglob("*"):
        if len(matches) >= limit:
            break
        if path.is_file() and is_interesting(path):
            matches.append(
                {
                    "root": str(root),
                    "path": str(path),
                    "name": path.name,
                    "modified": path.stat().st_mtime.__str__(),
                }
            )
    return matches


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=300)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--include-backups",
        action="store_true",
        help="Opt in to scanning K-drive backup/history roots.",
    )
    args = parser.parse_args()

    roots = [*HOT_ROOTS, *(BACKUP_ROOTS if args.include_backups else [])]
    results: list[dict[str, str]] = []
    per_root_limit = max(1, args.limit // len(roots))
    for root in roots:
        results.extend(scan(root, per_root_limit))

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("REUSABLE_ASSET_SCAN")
        print("BACKUP_ROOTS: " + ("ENABLED" if args.include_backups else "DISABLED"))
        for item in results:
            print(f"- {item['path']}")
        print(f"TOTAL: {len(results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
