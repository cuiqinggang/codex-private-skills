from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "SKILL.md", "README.md", "VERSION.md", "CHANGELOG.md", "agents/openai.yaml",
    "sources/source-quality-rules.md", "sources/fact-checking-rules.md", "sources/citation-format.md",
    "frameworks/founder-research-framework.md", "frameworks/product-analysis-framework.md",
    "frameworks/failure-analysis-framework.md", "frameworks/success-pattern-framework.md",
    "frameworks/monetization-framework.md", "frameworks/solo-operability-framework.md",
    "frameworks/update-framework.md", "templates/founder-profile-template.md",
    "templates/product-profile-template.md", "templates/timeline-template.md",
    "templates/comparative-analysis-template.md", "templates/evidence-table-template.md",
    "templates/lessons-template.md", "templates/final-report-template.md",
    "examples/marc-lou.md", "examples/pieter-levels.md", "examples/tony-dinh.md",
    "examples/danny-postma.md", "examples/ivan-kutskir.md", "examples/aj-carrd.md",
    "data/products/photo-ai.md", "data/indexes/founders-index.md",
    "data/indexes/products-index.md", "data/indexes/sectors-index.md",
    "data/indexes/update-status-index.md", "tests/test_case_01_founder.md",
    "tests/test_case_02_product.md", "tests/test_case_03_comparison.md",
]

missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
empty = [p for p in REQUIRED if (ROOT / p).is_file() and (ROOT / p).stat().st_size == 0]
if missing or empty:
    print("STRUCTURE_FAIL")
    if missing:
        print("missing:", *missing, sep="\n- ")
    if empty:
        print("empty:", *empty, sep="\n- ")
    sys.exit(1)
print(f"STRUCTURE_PASS files={len(REQUIRED)}")
