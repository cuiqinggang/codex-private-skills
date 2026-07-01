#!/usr/bin/env python3
import argparse
import json
import os
import sqlite3
from pathlib import Path


CODEX_ROOT = Path.home() / ".codex"
STATE_DB = CODEX_ROOT / "state_5.sqlite"
SESSION_INDEX = CODEX_ROOT / "session_index.jsonl"


def rows_for_query(con, query):
    if not query:
        return []
    like = f"%{query}%"
    sql = """
    select id, title, archived, archived_at, rollout_path, updated_at,
           created_at_ms, updated_at_ms, preview
    from threads
    where title like ? or preview like ? or first_user_message like ?
    order by updated_at desc
    limit 20
    """
    return [dict(r) for r in con.execute(sql, (like, like, like)).fetchall()]


def session_index_hits(query, thread_id):
    hits = []
    if not SESSION_INDEX.exists():
        return hits
    for n, line in enumerate(SESSION_INDEX.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if (query and query in line) or (thread_id and thread_id in line):
            hits.append({"line": n, "text": line[:1000]})
    return hits[:50]


def classify(row):
    if row is None:
        return "MISSING_FROM_THREADS_TABLE"
    path = row.get("rollout_path") or ""
    exists = os.path.exists(path)
    if row.get("archived"):
        return "ARCHIVED_THREAD"
    if not exists:
        return "ROLLOUT_PATH_MISSING"
    if "archived_sessions" in path.lower():
        return "ACTIVE_FLAG_BUT_ARCHIVE_PATH"
    return "ACTIVE_DB_ROW"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--thread-id")
    ap.add_argument("--query")
    args = ap.parse_args()

    con = sqlite3.connect(STATE_DB)
    con.row_factory = sqlite3.Row
    target = None
    if args.thread_id:
        r = con.execute(
            """
            select id, title, archived, archived_at, rollout_path, updated_at,
                   created_at_ms, updated_at_ms, preview
            from threads where id=?
            """,
            (args.thread_id,),
        ).fetchone()
        target = dict(r) if r else None
    query_rows = rows_for_query(con, args.query)
    con.close()

    if target:
        target["rollout_exists"] = os.path.exists(target["rollout_path"])
        target["classification"] = classify(target)

    report = {
        "state_db": str(STATE_DB),
        "session_index": str(SESSION_INDEX),
        "thread_id": args.thread_id,
        "query": args.query,
        "target": target,
        "query_matches": query_rows,
        "session_index_hits": session_index_hits(args.query, args.thread_id),
        "notes": [
            "If target is active but query_matches does not include the old title, suspect title drift.",
            "If archived is 1, use official unarchive tool first; if that fails for unloaded thread, use repair script.",
            "If rollout_path is missing or points to archived_sessions, copy the JSONL back to sessions and update rollout_path."
        ],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
