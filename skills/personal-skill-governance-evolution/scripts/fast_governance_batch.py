#!/usr/bin/env python3
"""Apply explicit, non-overlapping skill edits with per-skill rollback.

The manifest is JSON: {batch_id, operations:[{skill, replacements:[{old,new,count}],
copy_files:[{source,destination}], remove_frontmatter_keys:[...]}]}.
This script never discovers targets by scanning the skill library.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def metrics(path: Path) -> dict:
    skill = path / "SKILL.md"
    text = skill.read_text(encoding="utf-8") if skill.exists() else ""
    return {
        "skill_lines": len(text.splitlines()),
        "skill_chars": len(text), "skill_sha256": hashlib.sha256(text.encode()).hexdigest(),
    }


def snapshot_touched(target: Path, op: dict, backup: Path) -> list[dict]:
    touched = [target / "SKILL.md"]
    touched += [safe_child(target, target / x["destination"]) for x in op.get("copy_files", [])]
    records = []
    backup.mkdir(parents=True, exist_ok=True)
    for i, path in enumerate(dict.fromkeys(touched)):
        existed = path.exists()
        item = {"path": str(path.relative_to(target)), "existed": existed}
        if existed:
            slot = backup / f"{i:03d}-{hashlib.sha256(str(path).encode()).hexdigest()[:12]}.bin"
            shutil.copy2(path, slot)
            item["backup"] = str(slot)
        records.append(item)
    (backup / "snapshot-map.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return records


def restore_touched(target: Path, records: list[dict]) -> None:
    for item in records:
        path = safe_child(target, target / item["path"])
        if item["existed"]:
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item["backup"], path)
        elif path.exists():
            path.unlink()


def safe_child(root: Path, child: Path) -> Path:
    resolved = child.resolve()
    if root.resolve() not in resolved.parents:
        raise ValueError(f"target escapes root: {resolved}")
    return resolved


def strip_frontmatter_keys(text: str, keys: list[str]) -> str:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated YAML frontmatter")
    fm, body = text[4:end], text[end + 5:]
    lines = fm.splitlines()
    out, i = [], 0
    keyset = set(keys)
    while i < len(lines):
        m = re.match(r"^([A-Za-z0-9_-]+):", lines[i])
        if m and m.group(1) in keyset:
            i += 1
            while i < len(lines) and (lines[i].startswith(" ") or not lines[i].strip()):
                i += 1
            continue
        out.append(lines[i]); i += 1
    return "---\n" + "\n".join(out) + "\n---\n" + body


def static_check(skill_dir: Path, quick_validate: Path) -> tuple[bool, str]:
    skill = skill_dir / "SKILL.md"
    try:
        text = skill.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"UTF8/SKILL failure: {e}"
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return False, "frontmatter boundary failure"
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    cp = subprocess.run([sys.executable, str(quick_validate), str(skill_dir)],
                        text=True, capture_output=True, encoding="utf-8", errors="replace", env=env)
    return cp.returncode == 0, (cp.stdout + cp.stderr).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, type=Path)
${REDACTED_SECRET}
    ap.add_argument("--rollback-root", required=True, type=Path)
${REDACTED_SECRET}
    ap.add_argument("--result", required=True, type=Path)
    args = ap.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
    batch = data["batch_id"]
    seen, results = set(), []
    for op in data["operations"]:
        name = op["skill"]
        if name in seen: raise ValueError(f"duplicate owner in manifest: {name}")
        seen.add(name)
        if name in {".system", "firecrawl-web-api"} or name.startswith("."):
            results.append({"skill": name, "status": "SKIPPED_PROTECTED"}); continue
        target = safe_child(args.skills_root, args.skills_root / name)
        short = hashlib.sha256(name.encode()).hexdigest()[:12]
        backup = args.rollback_root / batch / "before" / short
        if not (target / "SKILL.md").exists():
            results.append({"skill": name, "status": "SKIPPED_MISSING"}); continue
        records = []
        before = None
        try:
            if backup.exists(): shutil.rmtree(backup)
            backup.parent.mkdir(parents=True, exist_ok=True)
            records = snapshot_touched(target, op, backup)
            before = metrics(target)
            skill = target / "SKILL.md"
            text = skill.read_text(encoding="utf-8")
            for item in op.get("replacements", []):
                found = text.count(item["old"])
                expected = int(item.get("count", 1))
                if found != expected:
                    raise ValueError(f"replacement count {found}!={expected}: {item['old'][:60]}")
                text = text.replace(item["old"], item["new"])
            if op.get("remove_frontmatter_keys"):
                text = strip_frontmatter_keys(text, op["remove_frontmatter_keys"])
            skill.write_text(text, encoding="utf-8", newline="\n")
            for item in op.get("copy_files", []):
                src = Path(item["source"])
                dst = safe_child(target, target / item["destination"])
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            ok, evidence = static_check(target, args.quick_validate)
            if not ok: raise ValueError(evidence)
            results.append({"skill": name, "status": "KEPT", "before": before,
                            "after": metrics(target), "validation": evidence})
        except Exception as e:
            if records:
                restore_touched(target, records)
            results.append({"skill": name, "status": "ROLLED_BACK", "reason": str(e),
                            "before": before, "restored": metrics(target)})
    payload = {"batch_id": batch, "assigned": len(data["operations"]), "results": results}
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"batch_id": batch, "kept": sum(r["status"]=="KEPT" for r in results),
                      "rolled_back": sum(r["status"]=="ROLLED_BACK" for r in results),
                      "skipped": sum(r["status"].startswith("SKIPPED") for r in results)}, ensure_ascii=False))
    return 0


if __name__ == "__main__": raise SystemExit(main())
