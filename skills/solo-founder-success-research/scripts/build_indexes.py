from pathlib import Path
from datetime import date
import re

ROOT = Path(__file__).resolve().parents[1]

def field(text, key, default=""):
    m = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, re.M)
    return m.group(1).strip().strip("'\"") if m else default

founder_rows = []
for path in sorted((ROOT / "examples").glob("*.md")):
    text = path.read_text(encoding="utf-8")
    founder_rows.append([field(text, "name"), field(text, "main_products"), field(text, "research_date"),
                         field(text, "last_verified"), field(text, "status"), field(text, "highest_evidence_level"),
                         path.relative_to(ROOT).as_posix()])
fp = ROOT / "data/indexes/founders-index.md"
lines = ["# Founders Index", "", f"Generated: {date.today().isoformat()}", "",
         "| 人物 | 主要产品 | 研究日期 | 最近验证 | 状态 | 证据等级 | 文件 |", "|---|---|---|---|---|---|---|"]
lines += ["| " + " | ".join(r) + " |" for r in founder_rows]
fp.write_text("\n".join(lines) + "\n", encoding="utf-8")

product_rows = []
for path in sorted((ROOT / "data/products").glob("*.md")):
    text = path.read_text(encoding="utf-8")
    product_rows.append([field(text, "name"), field(text, "founder"), field(text, "last_verified"),
                         field(text, "status"), path.relative_to(ROOT).as_posix()])
pp = ROOT / "data/indexes/products-index.md"
plines = ["# Products Index", "", f"Generated: {date.today().isoformat()}", "",
          "| 产品 | 创始人 | 最近验证 | 状态 | 文件 |", "|---|---|---|---|---|"]
plines += ["| " + " | ".join(r) + " |" for r in product_rows]
pp.write_text("\n".join(plines) + "\n", encoding="utf-8")
print(f"INDEX_BUILD_PASS founders={len(founder_rows)} products={len(product_rows)}")
