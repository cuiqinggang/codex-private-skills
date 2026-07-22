#!/usr/bin/env python3
"""对七文件标准验证器运行正例和关键反例回归测试。"""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "standard-evidence"
VALIDATOR_PATH = ROOT / "scripts" / "validate_standard_evidence.py"
spec = importlib.util.spec_from_file_location("ecc_standard_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(validator)


def load_bundle() -> dict[str, object]:
    bundle: dict[str, object] = {}
    for path in EXAMPLE.iterdir():
        if path.suffix == ".json":
            bundle[path.name] = json.loads(path.read_text(encoding="utf-8"))
        elif path.is_file():
            bundle[path.name] = path.read_text(encoding="utf-8")
    return bundle


def write_bundle(bundle: dict[str, object], root: Path) -> None:
    for name, value in bundle.items():
        path = root / name
        if name.endswith(".json"):
            path.write_text(
                json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )
        else:
            path.write_text(str(value), encoding="utf-8", newline="\n")


def expect_case(name: str, mutate: Callable[[dict[str, object]], None] | None, should_pass: bool) -> tuple[str, bool, list[str]]:
    bundle = load_bundle()
    if mutate:
        mutate(bundle)
    with tempfile.TemporaryDirectory(prefix="ecc-standard-test-") as temp:
        root = Path(temp)
        write_bundle(bundle, root)
        errors = validator.validate(root)
    passed = not errors
    return name, passed == should_pass, errors


def remove_audit_agent(bundle: dict[str, object]) -> None:
    ledger = bundle["run-ledger.json"]
    ledger["agents"] = [x for x in ledger["agents"] if x["role"] != "audit"]


def add_fifth_role(bundle: dict[str, object]) -> None:
    bundle["run-ledger.json"]["agents"][2]["role"] = "writer"


def remove_return_event(bundle: dict[str, object]) -> None:
    runtime = bundle["runtime-evidence.json"]
    runtime["events"] = [x for x in runtime["events"] if x["event_id"] != "EV-RETURN-AUDIT"]


def self_audit(bundle: dict[str, object]) -> None:
    bundle["verification.json"]["audits"][0]["auditor_agent_id"] = "execution-1"


def remove_negative_check(bundle: dict[str, object]) -> None:
    verification = bundle["verification.json"]
    verification["checks"] = [x for x in verification["checks"] if x["check_type"] != "NEGATIVE"]


def set_minimum_runtime(bundle: dict[str, object]) -> None:
    bundle["run-config.json"]["minimum_runtime_minutes"] = 300


def require_unused_skill(bundle: dict[str, object]) -> None:
    bundle["run-ledger.json"]["work_packages"][0]["required_skills"] = ["missing-skill"]


def alter_standard_hash(bundle: dict[str, object]) -> None:
    bundle["run-config.json"]["twelve_layer_standard_sha256"] = "0" * 64


def alter_standard_version(bundle: dict[str, object]) -> None:
    bundle["run-config.json"]["twelve_layer_standard_version"] = "2026-07-19中文版"


def alter_artifact_hash(bundle: dict[str, object]) -> None:
    bundle["runtime-evidence.json"]["artifacts"][0]["sha256"] = "0" * 64


def early_without_review(bundle: dict[str, object]) -> None:
    bundle["final-acceptance.json"].pop("early_completion_review", None)


def config_skill_not_bound(bundle: dict[str, object]) -> None:
    bundle["run-config.json"]["required_skills"] = ["declared-only-skill"]


def missing_event_receipt(bundle: dict[str, object]) -> None:
    bundle["runtime-evidence.json"]["events"][0].pop("receipt_id", None)


def negative_check_not_passed(bundle: dict[str, object]) -> None:
    bundle["verification.json"]["checks"][1]["result"] = "FAIL"


def remove_artifact_creation_event(bundle: dict[str, object]) -> None:
    runtime = bundle["runtime-evidence.json"]
    runtime["events"] = [x for x in runtime["events"] if x["kind"] != "artifact_created"]


def placeholder_layers(bundle: dict[str, object]) -> None:
    for layer in bundle["run-ledger.json"]["layers"]:
        layer["actual_actions"] = ["待填写"]
        layer["next_gate_or_failure_return"] = "待填写"


def empty_early_review(bundle: dict[str, object]) -> None:
    bundle["final-acceptance.json"]["early_completion_review"] = {"auditor_agent_id":"audit-1", "accepted":True}


def remove_platform_recheck(bundle: dict[str, object]) -> None:
    bundle["final-acceptance.json"].pop("platform_receipts_recheck", None)


def optimization_without_contract(bundle: dict[str, object]) -> None:
    bundle["run-config.json"]["task_type"] = "optimization"


def assessment_lower_mismatch(bundle: dict[str, object]) -> None:
    bundle["final-acceptance.json"]["early_completion_assessment"]["expected_duration_lower_minutes"] = 10


def fake_history_evidence(bundle: dict[str, object]) -> None:
    bundle["run-config.json"]["expected_duration_lower_minutes"] = 15
    assessment = bundle["final-acceptance.json"]["early_completion_assessment"]
    assessment["reliable_history_available"] = True
    assessment["expected_duration_lower_minutes"] = 15
    assessment["history_basis_evidence_ids"] = ["FAKE-HISTORY"]
    assessment["is_anomalously_early"] = False


def optimization_fake_auditor(bundle: dict[str, object]) -> None:
    bundle["run-config.json"]["task_type"] = "optimization"
    bundle["run-config.json"]["optimization_stop_contract"] = {
        "baseline_metric":"基线",
        "target_metric":"目标",
        "initial_candidates":["候选一"],
        "no_gain_round_limit":2,
        "cost_or_risk_limit":"不超过预算",
        "max_window_minutes":60,
        "independent_stop_auditor_id":"fake-auditor"
    }


def platform_recheck_only_one_event(bundle: dict[str, object]) -> None:
    bundle["final-acceptance.json"]["platform_receipts_recheck"]["evidence_ids"] = ["EV-START-CONTROL"]


def nonexistent_skill_path(bundle: dict[str, object]) -> None:
    bundle["run-config.json"]["required_skills"] = ["fake-skill"]
    bundle["run-ledger.json"]["work_packages"][0]["required_skills"] = ["fake-skill"]
    for kind, event_id, receipt_id, timestamp in (
        ("skill_read", "EV-SKILL-READ", "receipt-skill-read", "2026-07-19T09:05:00-07:00"),
        ("skill_use", "EV-SKILL-USE", "receipt-skill-use", "2026-07-19T09:06:00-07:00"),
    ):
        bundle["runtime-evidence.json"]["events"].append({
            "event_id":event_id,
            "receipt_id":receipt_id,
            "kind":kind,
            "source":"platform_event_log",
            "agent_id":"execution-1",
            "work_package_id":"WP-001",
            "skill":"fake-skill",
            "skill_path":"/definitely-missing/SKILL.md",
            "skill_entry_copy_path":"final-report.md",
            "skill_sha256":"aca68ba718c42cd7c2490210251f2965334e1ffa3063d077fecd1aaf3389fe62",
            "timestamp":timestamp,
            "platform_run_id":"run-execution-001",
            "exported_by_runtime":True
        })
    bundle["run-ledger.json"]["layers"][2]["evidence_ids"] = ["EV-SKILL-READ", "EV-SKILL-USE"]
    bundle["final-acceptance.json"]["platform_receipts_recheck"]["evidence_ids"].extend(["EV-SKILL-READ", "EV-SKILL-USE"])


def artifact_event_after_return(bundle: dict[str, object]) -> None:
    event = next(x for x in bundle["runtime-evidence.json"]["events"] if x["kind"] == "artifact_created")
    event["timestamp"] = "2026-07-19T09:18:00-07:00"


def remove_check_completion_event(bundle: dict[str, object]) -> None:
    runtime = bundle["runtime-evidence.json"]
    runtime["events"] = [x for x in runtime["events"] if x["kind"] != "check_completed"]


def layer_ten_unrelated_evidence(bundle: dict[str, object]) -> None:
    bundle["run-ledger.json"]["layers"][9]["evidence_ids"] = ["EV-START-CONTROL"]


def original_skill_differs_from_copy(bundle: dict[str, object]) -> None:
    bundle["run-config.json"]["required_skills"] = ["mismatched-skill"]
    bundle["run-ledger.json"]["work_packages"][0]["required_skills"] = ["mismatched-skill"]
    new_ids = []
    for kind, event_id, receipt_id, timestamp in (
        ("skill_read", "EV-SKILL-MISMATCH-READ", "receipt-skill-mismatch-read", "2026-07-19T09:05:00-07:00"),
        ("skill_use", "EV-SKILL-MISMATCH-USE", "receipt-skill-mismatch-use", "2026-07-19T09:06:00-07:00"),
    ):
        new_ids.append(event_id)
        bundle["runtime-evidence.json"]["events"].append({
            "event_id":event_id,
            "receipt_id":receipt_id,
            "kind":kind,
            "source":"platform_event_log",
            "agent_id":"execution-1",
            "work_package_id":"WP-001",
            "skill":"mismatched-skill",
            "skill_path":str(EXAMPLE / "raw-checks.log"),
            "skill_entry_copy_path":"final-report.md",
            "skill_sha256":"aca68ba718c42cd7c2490210251f2965334e1ffa3063d077fecd1aaf3389fe62",
            "timestamp":timestamp,
            "platform_run_id":"run-execution-001",
            "exported_by_runtime":True
        })
    bundle["run-ledger.json"]["layers"][2]["evidence_ids"] = new_ids
    bundle["final-acceptance.json"]["platform_receipts_recheck"]["evidence_ids"].extend(new_ids)


def valid_optimization(bundle: dict[str, object]) -> None:
    bundle["run-config.json"]["task_type"] = "optimization"
    bundle["run-config.json"]["optimization_stop_contract"] = {
        "baseline_metric":"结构错误数量为零",
        "target_metric":"保持结构错误为零并减少证据负担",
        "initial_candidates":["合并证据文件"],
        "no_gain_round_limit":2,
        "cost_or_risk_limit":"不能降低真实多智能体和独立审计硬门",
        "max_window_minutes":60,
        "independent_stop_auditor_id":"audit-1"
    }
    bundle["verification.json"]["optimization_experiments"] = [
        {"candidate":"合并证据文件","metric_before":"二十个固定文件","metric_after":"七个固定文件和按需附件","result_chinese":"负担下降且结构检查通过。","evidence_ids":["CHECK-SUCCESS"]}
    ]
    bundle["final-acceptance.json"]["optimization_stop_decision"] = {
        "auditor_agent_id":"audit-1",
        "accepted":True,
        "matched_stop_condition":"达到目标指标且没有未验证候选",
        "evidence_ids":["CHECK-SUCCESS"]
    }


def main() -> int:
    cases = (
        ("完整正例", None, True),
        ("开放式优化完整正例", valid_optimization, True),
        ("缺少独立审计角色", remove_audit_agent, False),
        ("出现第五类角色", add_fifth_role, False),
        ("缺少系统回传事件", remove_return_event, False),
        ("执行者自我审计", self_audit, False),
        ("缺少错误案例", remove_negative_check, False),
        ("普通任务设置300分钟最低时长", set_minimum_runtime, False),
        ("技能写入计划但没有真实事件", require_unused_skill, False),
        ("十二层标准版本号错误", alter_standard_version, False),
        ("十二层标准校验值被篡改", alter_standard_hash, False),
        ("产物校验值与副本不一致", alter_artifact_hash, False),
        ("异常早完但没有独立复核", early_without_review, False),
        ("总配置技能没有下沉工作包", config_skill_not_bound, False),
        ("系统事件缺少唯一回执编号", missing_event_receipt, False),
        ("错误案例存在但检查本身失败", negative_check_not_passed, False),
        ("任务产物缺少创建事件", remove_artifact_creation_event, False),
        ("十二层全部使用占位文字", placeholder_layers, False),
        ("异常早完复核只有两个空字段", empty_early_review, False),
        ("没有平台侧回执复核", remove_platform_recheck, False),
        ("开放式优化没有停止合同", optimization_without_contract, False),
        ("早完判断下界与运行配置不一致", assessment_lower_mismatch, False),
        ("历史范围引用不存在的证据", fake_history_evidence, False),
        ("优化停止审计者是假编号", optimization_fake_auditor, False),
        ("平台回读只抽查一个事件", platform_recheck_only_one_event, False),
        ("技能真实路径不存在", nonexistent_skill_path, False),
        ("产物创建发生在执行者回传后", artifact_event_after_return, False),
        ("检查只自填通过但没有运行事件", remove_check_completion_event, False),
        ("第10层引用无关控制事件", layer_ten_unrelated_evidence, False),
        ("原始技能文件与证据副本不一致", original_skill_differs_from_copy, False),
    )
    failures: list[dict[str, object]] = []
    for name, mutate, should_pass in cases:
        case_name, correct, errors = expect_case(name, mutate, should_pass)
        if not correct:
            failures.append({"case": case_name, "errors": errors})
    result = {
        "status": "PASS" if not failures else "FAIL",
        "status_chinese": "全部正反例符合预期" if not failures else "存在未按预期阻断的案例",
        "total_cases": len(cases),
        "failed_cases": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
