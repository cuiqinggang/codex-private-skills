from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
records = list((ROOT / "examples").glob("*.md")) + list((ROOT / "data/products").glob("*.md"))
url_re = re.compile(r'https?://[^\s)>"\]]+')
issues = []
total_urls = set()
for path in records:
    text = path.read_text(encoding="utf-8")
    urls = set(url_re.findall(text))
    total_urls.update(urls)
    if not urls:
        issues.append(f"{path.name}: no URL")
    if "证据等级" not in text and "highest_evidence_level" not in text:
        issues.append(f"{path.name}: no evidence grading")
    if re.search(r"\b(MRR|ARR|收入|revenue)\b", text, re.I) and "非审计" not in text:
        issues.append(f"{path.name}: financial claim lacks 非审计 label")
    if path.parent.name == "examples":
        for key in ["name:", "aliases:", "main_products:", "business_type:", "solo_status:",
                    "country:", "research_date:", "last_verified:", "source_count:",
                    "highest_evidence_level:", "status:"]:
            if key not in text:
                issues.append(f"{path.name}: missing {key}")
if issues:
    print("SOURCES_FAIL")
    print("\n".join(f"- {x}" for x in issues))
    sys.exit(1)
print(f"SOURCES_PASS records={len(records)} unique_urls={len(total_urls)}")
