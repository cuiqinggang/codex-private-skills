#!/usr/bin/env python3
"""Validate an industry-wiki project's structure and traceability contract."""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


REQUIRED_PATHS = ["00_INDEX.md", "PROJECT_BRIEF.md", "AGENTS.md", "sources/raw", "sources/extracted", "sources/source_registry.csv", "wiki", "evidence", "conflicts", "questions/diagnostic_questions.md", "changelog"]
WIKI_HEADINGS = ["## 一句话定义", "## 核心结论", "## 证据表", "## 争议与边界", "## 相关页面", "## 待验证问题", "## 更新记录"]
REGISTRY_FIELDS = ["source_id", "title", "type", "author_org", "published_at", "collected_at", "version", "relative_path", "locator", "reliability", "topics", "sha256", "status"]


def validate(project: Path, require_sources: bool) -> dict:
    project = project.resolve(strict=True)
    errors: list[str] = []
    warnings: list[str] = []
    for relative in REQUIRED_PATHS:
        if not (project / relative).exists():
            errors.append(f"missing:{relative}")

    registry = project / "sources" / "source_registry.csv"
    rows: list[dict] = []
    if registry.exists():
        with registry.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            missing_fields = [field for field in REGISTRY_FIELDS if field not in (reader.fieldnames or [])]
            if missing_fields:
                errors.append("registry_missing_fields:" + ",".join(missing_fields))
            rows = list(reader)
        if require_sources and not rows:
            errors.append("registry_has_no_sources")
        for number, row in enumerate(rows, 2):
            if not re.fullmatch(r"SRC-[0-9A-F]{12}", row.get("source_id", "")):
                errors.append(f"registry_row_{number}:invalid_source_id")
            if row.get("reliability") not in set("ABCD"):
                errors.append(f"registry_row_{number}:invalid_reliability")
            if not re.fullmatch(r"[0-9a-f]{64}", row.get("sha256", "")):
                errors.append(f"registry_row_{number}:invalid_sha256")
            source_path = (project / row.get("relative_path", "")).resolve()
            try:
                source_path.relative_to(project)
            except ValueError:
                errors.append(f"registry_row_{number}:path_outside_project")
            else:
                if not source_path.is_file():
                    errors.append(f"registry_row_{number}:source_missing")

    diagnostic = project / "questions" / "diagnostic_questions.md"
    question_count = 0
    if diagnostic.exists():
        question_count = len(re.findall(r"(?m)^\s*\d+\.\s+", diagnostic.read_text(encoding="utf-8-sig")))
        if question_count < 12:
            errors.append(f"diagnostic_questions_too_few:{question_count}")

    wiki_files = [path for path in (project / "wiki").glob("*.md") if path.name != "00_PAGE_TEMPLATE.md"] if (project / "wiki").exists() else []
    if require_sources and not wiki_files:
        errors.append("no_compiled_wiki_pages")
    for path in wiki_files:
        text = path.read_text(encoding="utf-8-sig")
        for heading in WIKI_HEADINGS:
            if heading not in text:
                errors.append(f"wiki_missing_heading:{path.name}:{heading[3:]}")
        if "SRC-" not in text:
            warnings.append(f"wiki_has_no_source_id:{path.name}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "project": str(project), "source_count": len(rows), "wiki_page_count": len(wiki_files),
        "diagnostic_question_count": question_count, "errors": errors, "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--require-sources", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = validate(args.project, args.require_sources)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

