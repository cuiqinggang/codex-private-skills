from __future__ import annotations
import argparse, json, tempfile, shutil
from pathlib import Path
from typing import Any
from common import (iter_files, rel_posix, read_text_best_effort, count_pattern,
                    locate_pattern, sha256_file, matches_any, extract_archive, write_json)

ARCHIVE_SUFFIXES = {".zip", ".7z"}


def scan_one_root(root: Path, contract: dict[str, Any], recursive_archives: bool = True, archive_depth: int = 0, max_depth: int = 4) -> dict[str, Any]:
    excludes = list(contract.get("exclude_globs", []))
    # The contract itself contains required/forbidden literals by definition and must not be counted as a business artifact.
    excludes += ["CHANGE_CONTRACT.json", "**/CHANGE_CONTRACT.json", "CHANGE_CONTRACT.*.json", "**/CHANGE_CONTRACT.*.json"]
    encodings = contract.get("text_encodings") or None
    files = list(iter_files(root, excludes))
    required_results = []
    forbidden_results = []
    archive_results = []

    def eval_rule(rule: dict[str, Any], kind: str):
        pattern = rule["pattern"]
        mode = rule.get("mode", "literal")
        case_sensitive = rule.get("case_sensitive", True)
        globs = rule.get("scope_globs", ["**/*"])
        rule_excludes = rule.get("exclude_globs", [])
        total = 0
        hits = []
        for p in files:
            rel = rel_posix(p, root)
            if not matches_any(rel, globs):
                continue
            if any(__import__("fnmatch").fnmatch.fnmatch(rel, x) or Path(rel).match(x) for x in rule_excludes):
                continue
            if rule.get("check_filenames", False):
                c = count_pattern(rel, pattern, mode, case_sensitive)
                if c:
                    total += c
                    hits.append({"path": rel, "location": "filename", "count": c})
            text, enc = read_text_best_effort(p, encodings)
            if text is None:
                continue
            c = count_pattern(text, pattern, mode, case_sensitive)
            if c:
                total += c
                hits.append({"path": rel, "location": "content", "encoding": enc, "count": c,
                             "matches": locate_pattern(text, pattern, mode, case_sensitive)})
        min_count = rule.get("min_count", 0)
        max_count = rule.get("max_count", None)
        ok = total >= min_count and (max_count is None or total <= max_count)
        return {"id": rule.get("id", pattern), "kind": kind, "pattern": pattern, "count": total,
                "min_count": min_count, "max_count": max_count, "status": "PASS" if ok else "FAIL", "hits": hits}

    for r in contract.get("required", []):
        required_results.append(eval_rule(r, "required"))
    for r in contract.get("forbidden", []):
        forbidden_results.append(eval_rule(r, "forbidden"))

    locked_results = []
    for item in contract.get("locked_files", []):
        p = root / item["path"]
        actual = sha256_file(p) if p.is_file() else None
        expected = item["sha256"].upper()
        locked_results.append({"path": item["path"], "expected": expected, "actual": actual,
                               "status": "PASS" if actual == expected else "FAIL"})

    mirror_results = []
    for item in contract.get("mirrors", []):
        a, b = root / item["left"], root / item["right"]
        if not a.is_file() or not b.is_file():
            status = "FAIL"
            detail = "missing file"
        elif item.get("mode", "bytes") == "bytes":
            status = "PASS" if a.read_bytes() == b.read_bytes() else "FAIL"
            detail = {"left_sha256": sha256_file(a), "right_sha256": sha256_file(b)}
        else:
            status = "UNSUPPORTED"
            detail = item.get("mode")
        mirror_results.append({**item, "status": status, "detail": detail})

    derived_results = []
    for item in contract.get("derived_relations", []):
        target = root / item["target"]
        sources = [root / s for s in item["sources"]]
        if not target.is_file() or any(not s.is_file() for s in sources):
            derived_results.append({**item, "status": "FAIL", "detail": "missing target/source"})
            continue
        mode = item.get("mode", "concatenate")
        if mode == "concatenate":
            sep = item.get("separator", "").encode("utf-8")
            expected = sep.join(s.read_bytes() for s in sources)
            actual = target.read_bytes()
            derived_results.append({**item, "status": "PASS" if actual == expected else "FAIL",
                                    "expected_sha256": __import__('hashlib').sha256(expected).hexdigest().upper(),
                                    "actual_sha256": sha256_file(target)})
        else:
            derived_results.append({**item, "status": "UNSUPPORTED"})

    if recursive_archives and archive_depth < max_depth:
        for p in files:
            if p.suffix.lower() not in ARCHIVE_SUFFIXES:
                continue
            rel = rel_posix(p, root)
            with tempfile.TemporaryDirectory(prefix="eclr-archive-") as td:
                status, detail = extract_archive(p, Path(td))
                entry = {"path": rel, "extract_status": status, "extractor": detail}
                if status == "PASS":
                    entry["scan"] = scan_one_root(Path(td), contract, True, archive_depth + 1, max_depth)
                archive_results.append(entry)

    statuses = []
    for group in [required_results, forbidden_results, locked_results, mirror_results, derived_results]:
        statuses += [x.get("status") for x in group]
    pending = any(a.get("extract_status", "").startswith("PENDING") for a in archive_results)
    nested_fail = any(a.get("extract_status") == "FAIL" or a.get("scan", {}).get("status") == "FAIL" for a in archive_results)
    status = "FAIL" if "FAIL" in statuses or nested_fail else ("PENDING" if pending else "PASS")
    return {
        "status": status,
        "root": str(root),
        "file_count": len(files),
        "required": required_results,
        "forbidden": forbidden_results,
        "locked_files": locked_results,
        "mirrors": mirror_results,
        "derived_relations": derived_results,
        "archives": archive_results,
        "semantic_checks": contract.get("semantic_checks", []),
        "pending_checks": contract.get("pending_checks", [])
    }


def markdown_report(result: dict[str, Any]) -> str:
    lines = ["# Evidence Closed Loop Verification", "", f"- Status: `{result['status']}`", f"- Root: `{result['root']}`", f"- Files: `{result['file_count']}`", ""]
    for title, key in [("Required", "required"), ("Forbidden", "forbidden"), ("Locked", "locked_files"), ("Mirrors", "mirrors"), ("Derived", "derived_relations")]:
        lines += [f"## {title}", ""]
        for r in result.get(key, []):
            lines.append(f"- `{r.get('status')}` — `{r.get('id', r.get('path', r.get('target','')) )}` — count `{r.get('count','')}`")
        lines.append("")
    lines += ["## Archives", ""]
    for a in result.get("archives", []):
        lines.append(f"- `{a.get('extract_status')}` — `{a.get('path')}` — nested `{a.get('scan',{}).get('status','N/A')}`")
    lines += ["", "## Pending", ""]
    for p in result.get("pending_checks", []):
        lines.append(f"- {p}")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify a candidate tree against an independent change contract")
    ap.add_argument("--root", required=True)
    ap.add_argument("--contract", required=True)
    ap.add_argument("--out-dir", default="evidence")
    ap.add_argument("--no-recursive-archives", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))
    result = scan_one_root(root, contract, not args.no_recursive_archives)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "verification.json", result)
    (out / "verification.md").write_text(markdown_report(result), encoding="utf-8")
    print(json.dumps({"status": result["status"], "files": result["file_count"], "out": str(out)}, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else (3 if result["status"] == "PENDING" else 2)

if __name__ == "__main__":
    raise SystemExit(main())
