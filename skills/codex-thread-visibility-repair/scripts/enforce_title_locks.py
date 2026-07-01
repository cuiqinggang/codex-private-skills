#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import sqlite3
import time
from pathlib import Path


CODEX_ROOT = Path.home() / ".codex"
STATE_DB = CODEX_ROOT / "state_5.sqlite"
SKILL_DIR = CODEX_ROOT / "skills" / "codex-thread-visibility-repair"
LOCKS_FILE = SKILL_DIR / "references" / "title-locks.json"
RECOVERY_ROOT = Path("H:/AI/recovery")


def backup_state(label):
    ts = time.strftime("%Y%m%d-%H%M%S")
    backup = RECOVERY_ROOT / f"codex-thread-title-lock-{ts}-{label}"
    backup.mkdir(parents=True, exist_ok=True)
    for name in ["state_5.sqlite", "state_5.sqlite-wal", "state_5.sqlite-shm", "session_index.jsonl"]:
        p = CODEX_ROOT / name
        if p.exists():
            shutil.copy2(p, backup / name)
    return backup


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--locks", default=str(LOCKS_FILE))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    locks = json.loads(Path(args.locks).read_text(encoding="utf-8"))["locks"]
    con = sqlite3.connect(STATE_DB)
    con.row_factory = sqlite3.Row
    changes = []
    for lock in locks:
        row = con.execute(
            "select id,title,archived,archived_at,rollout_path from threads where id=?",
            (lock["thread_id"],),
        ).fetchone()
        if not row:
            changes.append({"thread_id": lock["thread_id"], "status": "MISSING"})
            continue
        row = dict(row)
        need_title = row["title"] != lock["stable_title"]
        need_unarchive = bool(row["archived"])
        need_path = False
        rollout_path = row.get("rollout_path") or ""
        if rollout_path:
            lower = rollout_path.lower()
            need_path = ("archived_sessions" in lower) or (not os.path.exists(rollout_path))
        changes.append({
            "thread_id": lock["thread_id"],
            "before_title": row["title"],
            "stable_title": lock["stable_title"],
            "before_archived": row["archived"],
            "before_rollout_path": rollout_path,
            "rollout_exists": os.path.exists(rollout_path) if rollout_path else False,
            "will_update": need_title or need_unarchive or need_path,
        })
    backup = None
    if any(c.get("will_update") for c in changes) and not args.dry_run:
        backup = backup_state("apply")
        for lock in locks:
            row = con.execute("select rollout_path from threads where id=?", (lock["thread_id"],)).fetchone()
            rollout_path = row["rollout_path"] if row else ""
            new_path = rollout_path
            if rollout_path and "archived_sessions" in rollout_path.lower():
                source = Path(rollout_path)
                active = CODEX_ROOT / "sessions" / source.name
                parts = source.name.split("-")
                if len(parts) >= 4 and parts[0] == "rollout":
                    active = CODEX_ROOT / "sessions" / parts[1] / parts[2] / parts[3].split("T", 1)[0] / source.name
                active.parent.mkdir(parents=True, exist_ok=True)
                if source.exists():
                    shutil.copy2(source, active)
                    new_path = str(active)
            con.execute(
                "update threads set title=?, archived=0, archived_at=NULL, rollout_path=? where id=?",
                (lock["stable_title"], new_path, lock["thread_id"]),
            )
        con.commit()
    con.close()
    print(json.dumps({
        "locks_file": str(args.locks),
        "dry_run": args.dry_run,
        "backup_dir": str(backup) if backup else None,
        "changes": changes,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
