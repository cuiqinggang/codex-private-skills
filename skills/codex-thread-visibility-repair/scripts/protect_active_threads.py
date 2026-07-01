#!/usr/bin/env python3
import argparse
import json
import sqlite3
import time
from pathlib import Path


CODEX_ROOT = Path.home() / ".codex"
STATE_DB = CODEX_ROOT / "state_5.sqlite"
SKILL_DIR = CODEX_ROOT / "skills" / "codex-thread-visibility-repair"
LOCKS_FILE = SKILL_DIR / "references" / "title-locks.json"


def load_locks():
    if LOCKS_FILE.exists():
        return json.loads(LOCKS_FILE.read_text(encoding="utf-8"))
    return {"locks": []}


def save_locks(data):
    LOCKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOCKS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--include-not-loaded", action="store_true", default=True)
    ap.add_argument("--limit", type=int, default=0, help="0 means no limit")
    args = ap.parse_args()

    data = load_locks()
    by_id = {x["thread_id"]: x for x in data.get("locks", [])}

    con = sqlite3.connect(STATE_DB)
    con.row_factory = sqlite3.Row
    sql = """
    select id,title,archived,rollout_path,updated_at,created_at_ms,updated_at_ms,preview
    from threads
    where archived = 0
      and title is not null
      and trim(title) != ''
    order by updated_at desc
    """
    rows = con.execute(sql).fetchall()
    con.close()
    if args.limit and args.limit > 0:
        rows = rows[: args.limit]

    added = []
    refreshed = []
    now = time.strftime("%Y-%m-%dT%H:%M:%S")
    for r in rows:
        row = dict(r)
        tid = row["id"]
        if tid in by_id:
            # Preserve the existing stable title; just record that it was seen.
            by_id[tid]["last_seen_active"] = now
            refreshed.append(tid)
            continue
        by_id[tid] = {
            "thread_id": tid,
            "stable_title": row["title"],
            "aliases": [row["title"]],
            "reason": "Auto-protected because it was an active, unarchived Codex thread. User wants saved projects not to disappear from normal access.",
            "rollout_path_at_lock": row["rollout_path"],
            "locked_at": now,
            "last_seen_active": now
        }
        added.append({"thread_id": tid, "title": row["title"]})

    data["locks"] = list(by_id.values())
    save_locks(data)
    print(json.dumps({
        "locks_file": str(LOCKS_FILE),
        "active_threads_seen": len(rows),
        "added": added,
        "refreshed_count": len(refreshed),
        "total_locks": len(data["locks"])
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
