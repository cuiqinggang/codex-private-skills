#!/usr/bin/env python3
"""Register a source with a deterministic ID and duplicate guard."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import date
from pathlib import Path


FIELDS = ["source_id", "title", "type", "author_org", "published_at", "collected_at", "version", "relative_path", "locator", "reliability", "topics", "sha256", "status"]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("source_file", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--author-org", default="待核验")
    parser.add_argument("--published-at", default="")
    parser.add_argument("--version", default="")
    parser.add_argument("--locator", default="")
    parser.add_argument("--reliability", choices=list("ABCD"), required=True)
    parser.add_argument("--topics", default="")
    args = parser.parse_args()

    project = args.project.resolve(strict=True)
    source = args.source_file.resolve(strict=True)
    try:
        relative = source.relative_to(project).as_posix()
    except ValueError as exc:
        raise SystemExit("Source file must be inside the project") from exc
    registry = project / "sources" / "source_registry.csv"
    if not registry.exists():
        raise SystemExit(f"Missing registry: {registry}")
    checksum = digest(source)
    with registry.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    duplicate = next((row for row in rows if row.get("sha256") == checksum and row.get("status") != "rejected"), None)
    if duplicate:
        print(json.dumps({"status": "duplicate", "source_id": duplicate["source_id"], "duplicate_of": duplicate.get("relative_path")}, ensure_ascii=False))
        return 2
    row = {
        "source_id": f"SRC-{checksum[:12].upper()}", "title": args.title, "type": args.type,
        "author_org": args.author_org, "published_at": args.published_at,
        "collected_at": date.today().isoformat(), "version": args.version,
        "relative_path": relative, "locator": args.locator, "reliability": args.reliability,
        "topics": args.topics, "sha256": checksum, "status": "active",
    }
    with registry.open("a", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writerow(row)
    print(json.dumps({"status": "registered", **row}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

