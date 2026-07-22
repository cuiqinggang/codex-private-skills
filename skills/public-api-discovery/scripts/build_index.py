#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

LINK_RE = re.compile(r"^\[([^]]+)\]\(([^)]+)\)$")

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def norm(value, allowed):
    value = value.strip().strip("`")
    return value if value in allowed else "Unknown"

def parse(repo):
    readme = repo / "README.md"
    commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    category = None
    table_valid = False
    records, failures = [], []
    for lineno, raw in enumerate(readme.read_text(encoding="utf-8").splitlines(), 1):
        if raw.startswith("### "):
            category = raw[4:].strip()
            table_valid = False
            continue
        if category and re.match(r"^\|?\s*API\s*\|\s*Description\s*\|\s*Auth\s*\|\s*HTTPS\s*\|\s*CORS\s*\|?\s*$", raw):
            table_valid = True
            continue
        if not category or not table_valid or not raw.startswith("| ["):
            continue
        cells = [cell.strip() for cell in raw.strip().strip("|").split("|")]
        if len(cells) < 5:
            failures.append({"line": lineno, "reason": "fewer_than_5_columns", "text": raw})
            continue
        match = LINK_RE.match(cells[0])
        if not match:
            failures.append({"line": lineno, "reason": "invalid_markdown_link", "text": raw})
            continue
        name, url = match.groups()
        records.append({
            "category": category,
            "name": name,
            "description": cells[1],
            "auth": norm(cells[2], {"No", "apiKey", "OAuth", "Unknown"}),
            "https": norm(cells[3], {"Yes", "No", "Unknown"}),
            "cors": norm(cells[4], {"Yes", "No", "Unknown"}),
            "documentation_url": url,
            "source_commit": commit,
            "review_status": "unverified",
        })
    unique, seen = [], set()
    for row in records:
        key = tuple(row.values())
        if key not in seen:
            seen.add(key)
            unique.append(row)
    return commit, unique, len(records) - len(unique), failures

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path(r"C:\AI\resources\public-apis"))
    args = ap.parse_args()
    repo = args.repo.resolve()
    out = repo / "generated"
    out.mkdir(exist_ok=True)
    commit, rows, duplicate_count, failures = parse(repo)
    categories = Counter(row["category"] for row in rows)
    auth = Counter(row["auth"] for row in rows)
    https = Counter(row["https"] for row in rows)
    cors = Counter(row["cors"] for row in rows)
    (out / "public_apis_index.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    with (out / "public_apis_index.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    (out / "categories.json").write_text(json.dumps(dict(sorted(categories.items())), ensure_ascii=False, indent=2), encoding="utf-8")
    report = {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "source_commit": commit,
        "readme_sha256": sha256(repo / "README.md"),
        "license_sha256": sha256(repo / "LICENSE"),
        "category_count": len(categories),
        "record_count": len(rows),
        "duplicate_count": duplicate_count,
        "parse_failure_count": len(failures),
        "parse_failures": failures,
        "auth_distribution": auth,
        "https_distribution": https,
        "cors_distribution": cors,
    }
    (out / "build_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md = ["# Public APIs 索引构建报告", "", f"- 生成时间：{report['generated_at']}", f"- 源 Commit：`{commit}`", f"- 分类数：{len(categories)}", f"- API 条目数：{len(rows)}", f"- 完全重复数：{duplicate_count}", f"- 解析失败数：{len(failures)}", f"- 认证分布：`{dict(auth)}`", f"- HTTPS 分布：`{dict(https)}`", f"- CORS 分布：`{dict(cors)}`", "", "所有条目初始状态均为 `unverified`。"]
    if failures:
        md += ["", "## 解析失败", ""] + [f"- 行 {x['line']}：{x['reason']} — `{x['text']}`" for x in failures]
    (out / "build_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
