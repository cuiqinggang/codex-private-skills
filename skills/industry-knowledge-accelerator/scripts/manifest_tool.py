#!/usr/bin/env python3
"""Create a deterministic, symlink-safe source manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build(root: Path, previous: Path | None = None) -> dict:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError(f"Not a directory: {root}")
    previous_files: dict[str, dict] = {}
    if previous and previous.exists():
        previous_data = json.loads(previous.read_text(encoding="utf-8-sig"))
        previous_files = {item["relative_path"]: item for item in previous_data.get("files", [])}

    files: list[dict] = []
    duplicates: list[dict] = []
    skipped_symlinks: list[str] = []
    seen_hash: dict[str, str] = {}
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().casefold()):
        if path.is_symlink():
            skipped_symlinks.append(path.relative_to(root).as_posix())
            continue
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        digest = sha256(path)
        old = previous_files.get(relative)
        status = "new" if old is None else ("unchanged" if old.get("sha256") == digest else "updated")
        if digest in seen_hash:
            duplicates.append({"file": relative, "duplicate_of": seen_hash[digest], "sha256": digest})
        else:
            seen_hash[digest] = relative
        files.append({"relative_path": relative, "size_bytes": path.stat().st_size, "sha256": digest, "status": status})

    current_paths = {item["relative_path"] for item in files}
    deleted = sorted(set(previous_files) - current_paths)
    return {
        "schema_version": 2,
        "root": str(root),
        "file_count": len(files),
        "duplicate_count": len(duplicates),
        "deleted_count": len(deleted),
        "files": files,
        "duplicates": duplicates,
        "deleted": deleted,
        "skipped_symlinks": skipped_symlinks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = build(args.source_dir, args.previous)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("file_count", "duplicate_count", "deleted_count")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

