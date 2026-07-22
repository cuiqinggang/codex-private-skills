#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
RESULTS: list[dict] = []


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([PY, *args], capture_output=True, text=True, encoding="utf-8")


def record(name: str, ok: bool, detail: dict) -> None:
    RESULTS.append({"test": name, "status": "PASS" if ok else "FAIL", "detail": detail})


required = [
    "SKILL.md", "agents/openai.yaml", "scripts/scaffold_industry_kb.py", "scripts/register_source.py",
    "scripts/manifest_tool.py", "scripts/validate_industry_kb.py", "references/WORKFLOW.md",
    "references/DATA-CONTRACT.md", "references/FAILURE-REVIEW.md", "references/RECENT-USE-LOG.md",
    "references/AGENTS-PATCH-DRAFT.md", "references/ROI-GATE.md", "assets/templates/wiki_page.md",
    "assets/templates/source_registry.csv", "assets/templates/diagnostic_questions.md",
]
missing = [item for item in required if not (ROOT / item).exists()]
frontmatter = (ROOT / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
extra_frontmatter = [line for line in frontmatter.splitlines() if line and not line.startswith(("name:", "description:"))]
record("Round 1 - package contract", not missing and not extra_frontmatter, {"missing": missing, "extra_frontmatter": extra_frontmatter})

with tempfile.TemporaryDirectory() as temp:
    project = Path(temp) / "pilot"
    first = run(str(ROOT / "scripts/scaffold_industry_kb.py"), str(project), "--industry", "示例行业", "--purpose", "测试")
    second = run(str(ROOT / "scripts/scaffold_industry_kb.py"), str(project), "--industry", "示例行业", "--purpose", "测试")
    first_data = json.loads(first.stdout) if first.returncode == 0 else {}
    second_data = json.loads(second.stdout) if second.returncode == 0 else {}
    ok = first.returncode == 0 and second.returncode == 0 and len(first_data.get("created", [])) >= 7 and not second_data.get("created")
    record("Round 2 - scaffold and idempotency", ok, {"first_returncode": first.returncode, "second_returncode": second.returncode, "created_first": len(first_data.get("created", [])), "created_second": len(second_data.get("created", []))})

    raw = project / "sources" / "raw"
    (raw / "a.md").write_text("产业链：上游-中游-下游", encoding="utf-8")
    (raw / "b.md").write_text("市场数据：2025年，单位亿元，口径示例", encoding="utf-8")
    (raw / "copy-a.md").write_text("产业链：上游-中游-下游", encoding="utf-8")
    manifest1 = project / "evidence" / "manifest1.json"
    m1 = run(str(ROOT / "scripts/manifest_tool.py"), str(raw), "--out", str(manifest1))
    first_manifest = json.loads(manifest1.read_text(encoding="utf-8"))
    (raw / "b.md").write_text("市场数据：2026年更新，单位亿元，口径示例", encoding="utf-8")
    (raw / "a.md").unlink()
    (raw / "c.md").write_text("监管规则示例", encoding="utf-8")
    manifest2 = project / "evidence" / "manifest2.json"
    m2 = run(str(ROOT / "scripts/manifest_tool.py"), str(raw), "--previous", str(manifest1), "--out", str(manifest2))
    second_manifest = json.loads(manifest2.read_text(encoding="utf-8"))
    statuses = {item["relative_path"]: item["status"] for item in second_manifest["files"]}

    reg1 = run(str(ROOT / "scripts/register_source.py"), str(project), str(raw / "b.md"), "--title", "市场数据", "--type", "report", "--author-org", "示例机构", "--reliability", "B", "--locator", "第1页")
    duplicate = run(str(ROOT / "scripts/register_source.py"), str(project), str(raw / "b.md"), "--title", "重复", "--type", "report", "--reliability", "B")
    page = project / "wiki" / "01_行业总览.md"
    shutil.copy2(ROOT / "assets" / "templates" / "wiki_page.md", page)
    registered = json.loads(reg1.stdout)
    page.write_text(page.read_text(encoding="utf-8") + f"\n证据：{registered['source_id']}，第1页。\n", encoding="utf-8")
    valid = run(str(ROOT / "scripts/validate_industry_kb.py"), str(project), "--require-sources")
    page.write_text("# 损坏页面\n", encoding="utf-8")
    invalid = run(str(ROOT / "scripts/validate_industry_kb.py"), str(project), "--require-sources")
    ok3 = (
        m1.returncode == 0 and first_manifest["duplicate_count"] == 1 and m2.returncode == 0
        and statuses.get("b.md") == "updated" and statuses.get("c.md") == "new"
        and "a.md" in second_manifest["deleted"] and reg1.returncode == 0 and duplicate.returncode == 2
        and valid.returncode == 0 and invalid.returncode == 1
    )
    record("Round 3 - incremental, dedupe, validation and negative gate", ok3, {"manifest1_duplicates": first_manifest["duplicate_count"], "statuses": statuses, "deleted": second_manifest["deleted"], "register_returncode": reg1.returncode, "duplicate_returncode": duplicate.returncode, "valid_returncode": valid.returncode, "invalid_returncode": invalid.returncode})

summary = {"total": len(RESULTS), "passed": sum(item["status"] == "PASS" for item in RESULTS), "failed": sum(item["status"] == "FAIL" for item in RESULTS), "results": RESULTS}
(ROOT / "tests" / "test_report.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))
raise SystemExit(0 if summary["failed"] == 0 else 1)

