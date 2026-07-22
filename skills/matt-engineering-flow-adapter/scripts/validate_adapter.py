import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
required = [
    "SKILL.md", "README_CN.md", "VERSION",
    "router/ROUTING_RULES.md", "router/CONFLICT_PRIORITY.md",
    "router/TRIGGER_NEGATIVES.md",
]
required += ["workflows/%02d_%s.md" % item for item in [
    (1, "requirements_grill"), (2, "domain_context"), (3, "to_spec"),
    (4, "vertical_tickets"), (5, "tdd_execution"), (6, "bug_diagnosis"),
    (7, "dual_axis_review"), (8, "handoff"),
]]
required += ["templates/" + name for name in [
    "REQUIREMENTS_CONTRACT.md", "CONTEXT.md", "ADR_TEMPLATE.md", "SPEC.md",
    "TICKET.md", "TDD_EVIDENCE.md", "CODE_REVIEW.md", "HANDOFF.md",
]]
required += ["gates/" + name for name in [
    "PRE_WRITE_GATE.md", "SPEC_GATE.md", "TEST_GATE.md", "REVIEW_GATE.md",
]]
required += ["adapters/" + name for name in ["codex.md", "cursor.md", "kilo.md"]]
failures = []
for rel in required:
    path = root / rel
    if not path.is_file() or path.stat().st_size == 0:
        failures.append("missing_or_empty:" + rel)
skill = (root / "SKILL.md").read_text(encoding="utf-8")
if (root / "SKILL.md").stat().st_size > 12288:
    failures.append("skill_over_12kb")
for path in (root / "workflows").glob("*.md"):
    if path.stat().st_size > 10240:
        failures.append("workflow_over_10kb:" + path.name)
for phrase in ["不自动提交", "不 merge", "不 push", "不注册 Hook", "不管理 Worktree"]:
    if phrase not in skill:
        failures.append("boundary_missing:" + phrase)
cases = json.loads((root / "tests/scenarios/router_cases.json").read_text(encoding="utf-8"))
negative = [x for x in cases if x["id"].startswith("N")]
if any(x["expected"] for x in negative):
    failures.append("negative_trigger_expected_not_empty")
result = {"status": "PASS" if not failures else "FAIL",
          "required_files": len(required), "scenario_count": len(cases),
          "negative_scenarios": len(negative), "failures": failures}
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0 if not failures else 1)
