#!/usr/bin/env python3
"""Create a minimal industry-wiki project without overwriting user files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "assets" / "templates"
DIRECTORIES = (
    "sources/raw", "sources/extracted", "wiki", "entities", "evidence",
    "conflicts", "questions", "changelog", "tests",
)


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def create(target: Path, values: dict[str, str]) -> dict:
    target = target.resolve()
    target.mkdir(parents=True, exist_ok=True)
    for directory in DIRECTORIES:
        (target / directory).mkdir(parents=True, exist_ok=True)

    mappings = {
        "PROJECT_BRIEF.md": "PROJECT_BRIEF.md",
        "AGENTS.md": "AGENTS_PROJECT_TEMPLATE.md",
        "sources/source_registry.csv": "source_registry.csv",
        "questions/diagnostic_questions.md": "diagnostic_questions.md",
        "conflicts/CONFLICT_TEMPLATE.md": "conflict_record.md",
        "wiki/00_PAGE_TEMPLATE.md": "wiki_page.md",
    }
    created: list[str] = []
    skipped: list[str] = []
    for relative, template_name in mappings.items():
        destination = target / relative
        if destination.exists():
            skipped.append(relative)
            continue
        content = render((TEMPLATES / template_name).read_text(encoding="utf-8"), values)
        destination.write_text(content, encoding="utf-8")
        created.append(relative)

    index = target / "00_INDEX.md"
    if not index.exists():
        index.write_text(
            f"# {values['INDUSTRY']} 行业知识库\n\n状态：PILOT\n\n"
            "## 导航\n\n- [项目简报](PROJECT_BRIEF.md)\n- [诊断问题](questions/diagnostic_questions.md)\n"
            "- [页面模板](wiki/00_PAGE_TEMPLATE.md)\n- [来源登记](sources/source_registry.csv)\n",
            encoding="utf-8",
        )
        created.append("00_INDEX.md")
    else:
        skipped.append("00_INDEX.md")
    return {"target": str(target), "created": created, "skipped": skipped}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    parser.add_argument("--industry", required=True)
    parser.add_argument("--purpose", default="建立可追溯的行业基础知识库")
    parser.add_argument("--region", default="待确认")
    parser.add_argument("--period", default="当前与近三年")
    args = parser.parse_args()
    result = create(args.target, {"INDUSTRY": args.industry, "PURPOSE": args.purpose, "REGION": args.region, "PERIOD": args.period})
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
