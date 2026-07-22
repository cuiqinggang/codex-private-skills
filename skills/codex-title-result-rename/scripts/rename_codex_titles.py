import argparse
import json
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path


${REDACTED_SECRET}
${REDACTED_SECRET}


def load_json(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("mapping must be a JSON object: {thread_id: new_title}")
    bad = {k: v for k, v in data.items() if not isinstance(k, str) or not isinstance(v, str) or not v.strip()}
    if bad:
        raise SystemExit(f"mapping contains invalid title entries: {list(bad)[:5]}")
    return data


def connect_readonly(path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con


def read_threads(state_path: Path, cwd_like: str) -> list[sqlite3.Row]:
    con = connect_readonly(state_path)
    rows = con.execute(
        "select id, title, rollout_path, first_user_message from threads where cwd like ? order by updated_at desc",
        (f"%{cwd_like}%",),
    ).fetchall()
    con.close()
    return rows


def backup_files(state_path: Path, index_path: Path, out_dir: Path) -> Path:
    backup_dir = out_dir / "backup"
    backup_dir.mkdir(parents=True, exist_ok=True)

    src = sqlite3.connect(str(state_path))
    dst_path = backup_dir / "state_5.sqlite.backup"
    dst = sqlite3.connect(str(dst_path))
    src.backup(dst)
    dst.close()
    src.close()

    shutil.copy2(index_path, backup_dir / "session_index.jsonl.backup")
    return backup_dir


def update_sqlite(state_path: Path, mapping: dict[str, str]) -> None:
    con = sqlite3.connect(str(state_path))
    for thread_id, title in mapping.items():
        con.execute("update threads set title=? where id=?", (title, thread_id))
    con.commit()
    con.close()


def update_session_index(index_path: Path, mapping: dict[str, str]) -> list[dict[str, str]]:
    lines = index_path.read_text(encoding="utf-8").splitlines()
    output = []
    changes = []
    for line in lines:
        if not line.strip():
            continue
        obj = json.loads(line)
        thread_id = obj.get("id")
        if thread_id in mapping:
            changes.append({"id": thread_id, "old_title": obj.get("thread_name", ""), "new_title": mapping[thread_id]})
            obj["thread_name"] = mapping[thread_id]
        output.append(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))
    index_path.write_text("\n".join(output) + ("\n" if output else ""), encoding="utf-8")
    return changes


def write_reports(out_dir: Path, before: dict[str, str], after: dict[str, str], index_changes: list[dict[str, str]]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = [{"id": thread_id, "old_title": before[thread_id], "new_title": after[thread_id]} for thread_id in before]
    (out_dir / "before_titles.json").write_text(json.dumps(before, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "after_titles.json").write_text(json.dumps(after, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "rename_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "session_index_changes.json").write_text(json.dumps(index_changes, ensure_ascii=False, indent=2), encoding="utf-8")
    with (out_dir / "rename_summary.tsv").open("w", encoding="utf-8", newline="") as f:
        f.write("id\told_title\tnew_title\n")
        for item in summary:
            old = item["old_title"].replace("\t", " ").replace("\r", " ").replace("\n", " ")
            new = item["new_title"].replace("\t", " ").replace("\r", " ").replace("\n", " ")
            f.write(f"{item['id']}\t{old}\t{new}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Rename Codex thread titles to long Chinese result-based names.")
    parser.add_argument("--mapping", required=True, type=Path, help="UTF-8 JSON object: {thread_id: new_title}")
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--cwd-like", default=r"Desktop\1", help="Only threads whose cwd contains this string")
    parser.add_argument("--out-dir", type=Path, default=Path.cwd() / "output" / "codex-thread-title-rename" / datetime.now().strftime("%Y%m%d-%H%M%S"))
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    mapping = load_json(args.mapping)
    rows = read_threads(args.state, args.cwd_like)
    before = {row["id"]: row["title"] for row in rows}
    missing = [row["id"] for row in rows if row["id"] not in mapping]
    extra = [thread_id for thread_id in mapping if thread_id not in before]
    if missing or extra:
        raise SystemExit(json.dumps({"missing_in_mapping": missing, "extra_mapping": extra}, ensure_ascii=False, indent=2))

    if args.dry_run:
        print(json.dumps({"status": "DRY_RUN_OK", "thread_count": len(rows), "out_dir": str(args.out_dir)}, ensure_ascii=False, indent=2))
        return

    backup_dir = backup_files(args.state, args.index, args.out_dir)
    update_sqlite(args.state, mapping)
    index_changes = update_session_index(args.index, mapping)
    after_rows = read_threads(args.state, args.cwd_like)
    after = {row["id"]: row["title"] for row in after_rows}
    write_reports(args.out_dir, before, after, index_changes)
    bad_question = [thread_id for thread_id, title in after.items() if "?" in title]
    print(
        json.dumps(
            {
                "status": "APPLY_OK",
                "thread_rows_updated": len(after),
                "session_index_rows_updated": len(index_changes),
                "backup_dir": str(backup_dir),
                "out_dir": str(args.out_dir),
                "titles_with_question_mark": bad_question,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
