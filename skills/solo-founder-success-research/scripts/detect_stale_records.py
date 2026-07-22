from pathlib import Path
from datetime import date, datetime
import re

ROOT = Path(__file__).resolve().parents[1]
TODAY = date.today()
rows = []
for path in list((ROOT / "examples").glob("*.md")) + list((ROOT / "data/products").glob("*.md")):
    text = path.read_text(encoding="utf-8")
    name = re.search(r"^name:\s*[\"']?(.+?)[\"']?\s*$", text, re.M)
    verified = re.search(r"^last_verified:\s*(\d{4}-\d{2}-\d{2})", text, re.M)
    cadence = re.search(r"^review_cadence_days:\s*(\d+)", text, re.M)
    if not (name and verified):
        continue
    day = datetime.strptime(verified.group(1), "%Y-%m-%d").date()
    limit = int(cadence.group(1)) if cadence else (45 if "data\\products" in str(path) else 90)
    age = (TODAY - day).days
    state = "STALE_REVIEW_REQUIRED" if age > limit else "FRESH"
    rows.append((name.group(1), verified.group(1), limit, age, state, path.relative_to(ROOT).as_posix()))

out = ROOT / "data/indexes/update-status-index.md"
lines = ["# Update Status Index", "", f"Generated: {TODAY.isoformat()}", "",
         "| 记录 | 最近验证 | 周期(天) | 年龄(天) | 状态 | 文件 |", "|---|---|---:|---:|---|---|"]
for row in sorted(rows):
    lines.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | `{row[5]}` |")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
stale = sum(1 for r in rows if r[4] != "FRESH")
print(f"STALE_SCAN_PASS records={len(rows)} stale={stale} index={out}")
