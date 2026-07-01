#!/usr/bin/env python3
import argparse
import json
import shutil
import sqlite3
import time
from pathlib import Path


CODEX_ROOT = Path.home() / ".codex"
STATE_DB = CODEX_ROOT / "state_5.sqlite"
RECOVERY_ROOT = Path("H:/AI/recovery")


def backup_inputs(thread_id, rollout_path):
    ts = time.strftime("%Y%m%d-%H%M%S")
    backup = RECOVERY_ROOT / f"codex-thread-visibility-repair-{ts}-{thread_id}"
    backup.mkdir(parents=True, exist_ok=True)
    for name in ["state_5.sqlite", "state_5.sqlite-wal", "state_5.sqlite-shm", "session_index.jsonl"]:
        p = CODEX_ROOT / name
        if p.exists():
            shutil.copy2(p, backup / name)
    rp = Path(rollout_path) if rollout_path else None
    if rp and rp.exists():
        shutil.copy2(rp, backup / rp.name)
    return backup


def active_path_for_rollout(source):
    source = Path(source)
    name = source.name
    # rollout-2026-06-11T01-16-07-<id>.jsonl -> sessions/2026/06/11/name
    parts = name.split("-")
    if len(parts) >= 4 and parts[0] == "rollout":
        year = parts[1]
        month = parts[2]
        day = parts[3].split("T", 1)[0]
        return CODEX_ROOT / "sessions" / year / month / day / name
    return CODEX_ROOT / "sessions" / name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--thread-id", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--pin", action="store_true", help="Records intent only; use official set_thread_pinned tool when available.")
    args = ap.parse_args()

    con = sqlite3.connect(STATE_DB)
    con.row_factory = sqlite3.Row
    row = con.execute("select * from threads where id=?", (args.thread_id,)).fetchone()
    if not row:
        raise SystemExit(f"Thread not found in {STATE_DB}: {args.thread_id}")
    before = dict(row)
    backup = backup_inputs(args.thread_id, before.get("rollout_path"))

    source_path = Path(before["rollout_path"])
    if not source_path.exists():
        archived_guess = CODEX_ROOT / "archived_sessions" / source_path.name
        if archived_guess.exists():
            source_path = archived_guess
        else:
            raise SystemExit(f"Rollout file missing: {before['rollout_path']}")

    active_path = active_path_for_rollout(source_path)
    active_path.parent.mkdir(parents=True, exist_ok=True)
    if source_path.resolve() != active_path.resolve():
        shutil.copy2(source_path, active_path)

    con.execute(
        "update threads set archived=0, archived_at=NULL, rollout_path=?, title=? where id=?",
        (str(active_path), args.title, args.thread_id),
    )
    con.commit()
    after = dict(con.execute(
        "select id,title,archived,archived_at,rollout_path,updated_at,updated_at_ms from threads where id=?",
        (args.thread_id,),
    ).fetchone())
    con.close()

    report = {
        "thread_id": args.thread_id,
        "backup_dir": str(backup),
        "before": {
            "title": before.get("title"),
            "archived": before.get("archived"),
            "archived_at": before.get("archived_at"),
            "rollout_path": before.get("rollout_path"),
        },
        "after": after,
        "active_rollout_exists": active_path.exists(),
        "pin_requested": args.pin,
        "next_step": "Use codex_app.set_thread_pinned(threadId, pinned=true) when available, then list_threads(query=title).",
    }
    (backup / "repair-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
