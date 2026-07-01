#!/usr/bin/env python3
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path


def file_info(path_text: str):
    if not path_text:
        return None
    path = Path(path_text)
    if not path.exists():
        return {"path": str(path), "exists": False}
    h = hashlib.sha256()
    if path.is_file():
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return {
            "path": str(path),
            "exists": True,
            "type": "file",
            "size": path.stat().st_size,
            "sha256_16": h.hexdigest()[:16],
        }
    count = sum(1 for p in path.rglob("*") if p.is_file())
    return {"path": str(path), "exists": True, "type": "directory", "file_count": count}


def main():
    parser = argparse.ArgumentParser(description="Append a Cursor/Kilo SuperTool stage sync entry.")
    parser.add_argument("--stage", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--artifact", default="")
    parser.add_argument("--notes", default="")
    parser.add_argument("--next", default="")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parents[1]
    refs = skill_dir / "references"
    log_md = refs / "recent-use-log.md"
    log_jsonl = refs / "recent-use-log.jsonl"
    now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    entry = {
        "time": now,
        "stage": args.stage,
        "status": args.status,
        "artifact": file_info(args.artifact),
        "notes": args.notes,
        "next": args.next,
    }

    with log_jsonl.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    artifact_path = entry["artifact"]["path"] if entry["artifact"] else ""
    artifact_state = "exists" if entry["artifact"] and entry["artifact"].get("exists") else "missing/not provided"
    block = (
        f"\n## {now} - {args.stage}\n\n"
        f"- Status: `{args.status}`\n"
        f"- Artifact: `{artifact_path}` ({artifact_state})\n"
        f"- Notes: {args.notes or 'none'}\n"
        f"- Next: {args.next or 'not specified'}\n"
    )
    with log_md.open("a", encoding="utf-8") as f:
        f.write(block)

    print(f"SYNC_OK {log_md}")


if __name__ == "__main__":
    main()
