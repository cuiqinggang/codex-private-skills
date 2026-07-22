#!/usr/bin/env python3
"""验证ECC标准生产模式的七文件证据；错误信息以中文为主。"""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


JSON_FILES = (
    "run-config.json",
    "run-ledger.json",
    "runtime-evidence.json",
    "verification.json",
    "checkpoints.json",
    "final-acceptance.json",
)
TEXT_FILE = "final-report.md"
STANDARD_VERSION = "V2.0.0"
ROLES = {"control", "materials", "execution", "audit"}
STATUSES = {"PASS", "PARTIAL", "BLOCKED", "REJECTED"}
LAYER_SPECS = (
    (1, "Control Plane / Orchestrator", "主控调度层"),
    (2, "Short Entry / Memory", "短入口 / 项目记忆层"),
    (3, "Skills / Progressive Disclosure", "技能按需加载 / 渐进加载层"),
    (4, "Planning / Work Decomposition", "任务拆解层"),
    (5, "Subagents / Context Isolation", "子智能体 / 上下文隔离层"),
    (6, "Execution Plane", "执行平面"),
    (7, "Hooks / Lifecycle Triggers", "生命周期钩子层"),
    (8, "Scripts / Deterministic Checks", "脚本确定性检查层"),
    (9, "Verification Plane", "独立验证平面"),
    (10, "Repair Loop", "返修循环层"),
    (11, "Compact / Handoff", "压缩交接层"),
    (12, "Final Acceptance", "最终验收层"),
)


def nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple, set)):
        return bool(value)
    return True


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else None
    except ValueError:
        return None


def number(value: Any, label: str, errors: list[str]) -> float:
    if isinstance(value, bool):
        errors.append(f"{label}必须是数字。")
        return 0.0
    try:
        result = float(value)
    except (TypeError, ValueError):
        errors.append(f"{label}必须是有效数字。")
        return 0.0
    if not math.isfinite(result):
        errors.append(f"{label}必须是有限数字。")
        return 0.0
    return result


def load_json(path: Path, errors: list[str]) -> Any:
    if not path.is_file():
        errors.append(f"缺少必需文件：{path.name}。")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.name}无法解析：{exc}。")
        return {}


def require_list(value: Any, label: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{label}必须是数组。")
        return []
    return value


def require_dict(value: Any, label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label}必须是对象。")
        return {}
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def has_chinese(text: str) -> bool:
    return len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", text)) >= 50


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    data = {name: load_json(root / name, errors) for name in JSON_FILES}
    report_path = root / TEXT_FILE
    if not report_path.is_file():
        errors.append(f"缺少必需文件：{TEXT_FILE}。")
        report = ""
    else:
        report = report_path.read_text(encoding="utf-8", errors="replace")
    if errors:
        return errors

    config = require_dict(data["run-config.json"], "run-config.json", errors)
    ledger = require_dict(data["run-ledger.json"], "run-ledger.json", errors)
    runtime = require_dict(data["runtime-evidence.json"], "runtime-evidence.json", errors)
    verification = require_dict(data["verification.json"], "verification.json", errors)
    checkpoints = require_list(data["checkpoints.json"], "checkpoints.json", errors)
    final = require_dict(data["final-acceptance.json"], "final-acceptance.json", errors)

    if config.get("evidence_profile") != "standard":
        errors.append("evidence_profile必须是standard，中文意思是标准证据模式。")
    if config.get("task_type") not in {"production", "preparation", "optimization"}:
        errors.append("标准模式只允许真实生产、准备或开放式优化任务；耐力验证必须使用严格模式。")
    if number(config.get("minimum_runtime_minutes", 0), "minimum_runtime_minutes最低时长", errors) > 0:
        errors.append("标准生产模式不能设置必须耗满的最低时长。")
    if config.get("required_roles") != ["control", "materials", "execution", "audit"]:
        errors.append("required_roles必须依次包含控制、资料、工程执行、独立审计四类角色。")
    config_skills = {str(x) for x in config.get("required_skills") or []}
    if config.get("task_type") == "optimization":
        contract = config.get("optimization_stop_contract")
        if not isinstance(contract, dict):
            errors.append("开放式优化必须在第4层预先建立optimization_stop_contract优化停止合同。")
        else:
            for field in ("baseline_metric", "target_metric", "initial_candidates", "no_gain_round_limit", "cost_or_risk_limit", "max_window_minutes", "independent_stop_auditor_id"):
                if not nonempty(contract.get(field)):
                    errors.append(f"优化停止合同缺少{field}。")

    standard_path = Path(__file__).resolve().parent.parent / "references" / "twelve-layer-standard.md"
    if config.get("twelve_layer_standard_version") != STANDARD_VERSION:
        errors.append(f"十二层标准版本必须是{STANDARD_VERSION}，不能用日期、旧版本或空值代替。")
    if config.get("twelve_layer_standard_sha256") != sha256(standard_path):
        errors.append("十二层标准校验值与当前完整中文版不一致，不能证明继承了固定十六项。")

    requirements = require_list(ledger.get("requirements"), "run-ledger.requirements", errors)
    layers = require_list(ledger.get("layers"), "run-ledger.layers", errors)
    agents = require_list(ledger.get("agents"), "run-ledger.agents", errors)
    packages = require_list(ledger.get("work_packages"), "run-ledger.work_packages", errors)
    requirement_ids = {str(x.get("requirement_id", "")) for x in requirements if isinstance(x, dict)}
    if not requirement_ids or "" in requirement_ids:
        errors.append("用户要求必须有非空且唯一的requirement_id。")
    if len(requirement_ids) != len(requirements):
        errors.append("用户要求编号不能重复。")

    layer_evidence_ids: set[str] = set()
    if len(layers) != 12:
        errors.append("任务级十二层必须恰好十二项；不得缺层或为每个工作包复制。")
    for position, spec in enumerate(LAYER_SPECS):
        if position >= len(layers) or not isinstance(layers[position], dict):
            continue
        layer = layers[position]
        if (layer.get("layer_number"), layer.get("english_name"), layer.get("chinese_name")) != spec:
            errors.append(f"第{position + 1}层名称、中文名或顺序与固定标准不一致。")
        if layer.get("status") not in STATUSES or layer.get("skippable") is not False:
            errors.append(f"第{position + 1}层状态无效或被错误标为可跳过。")
        for field in ("actual_inputs", "actual_actions", "new_artifacts", "evidence_ids", "next_gate_or_failure_return"):
            if not nonempty(layer.get(field)):
                errors.append(f"第{position + 1}层缺少本次动态字段：{field}。")
        dynamic_text = json.dumps(
            {"actions": layer.get("actual_actions"), "next": layer.get("next_gate_or_failure_return")},
            ensure_ascii=False,
        )
        if len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", dynamic_text)) < 8:
            errors.append(f"第{position + 1}层的实际动作和下一关口过于空泛，不能用占位文字通过。")
        if re.search(r"(?i)\b(?:TODO|TBD|PLACEHOLDER)\b|待填写|仅占位", dynamic_text):
            errors.append(f"第{position + 1}层包含未完成占位符。")
        layer_evidence_ids.update(str(x) for x in layer.get("evidence_ids") or [])

    agent_map: dict[str, dict[str, Any]] = {}
    roles: set[str] = set()
    contexts: set[str] = set()
    workspaces: set[str] = set()
    run_ids: set[str] = set()
    agent_evidence_ids: set[str] = set()
    for index, agent in enumerate(agents, 1):
        if not isinstance(agent, dict):
            errors.append(f"第{index}个智能体记录必须是对象。")
            continue
        agent_id = str(agent.get("agent_id", "")).strip()
        role = str(agent.get("role", "")).strip()
        if not agent_id or agent_id in agent_map:
            errors.append(f"第{index}个智能体编号缺失或重复。")
        agent_map[agent_id] = agent
        if role not in ROLES:
            errors.append(f"智能体{agent_id}角色无效；只能是控制、资料、工程执行、独立审计。")
        roles.add(role)
        for field, seen in (("context_id", contexts), ("workspace", workspaces), ("platform_run_id", run_ids)):
            value = str(agent.get(field, "")).strip().casefold()
            if not value or value in seen:
                errors.append(f"智能体{agent_id}的{field}缺失或不能证明独立。")
            seen.add(value)
        if not parse_time(agent.get("started_at")) or not parse_time(agent.get("returned_at")):
            errors.append(f"智能体{agent_id}缺少带时区的真实起止时间。")
        if not nonempty(agent.get("responsibility")) or not nonempty(agent.get("evidence_ids")):
            errors.append(f"智能体{agent_id}缺少边界责任或证据编号。")
        agent_evidence_ids.update(str(x) for x in agent.get("evidence_ids") or [])
    if roles != ROLES:
        errors.append("正式标准模式必须真实包含控制、资料、工程执行、独立审计四类角色。")
    if sum(1 for agent in agents if isinstance(agent, dict) and agent.get("role") == "control") != 1:
        errors.append("每次运行必须恰好有一个根控制角色。")
    for agent_id, agent in agent_map.items():
        parent_id = str(agent.get("parent_agent_id", "")).strip()
        if agent.get("role") == "control":
            if parent_id:
                errors.append("根控制角色不能再声明父级智能体。")
        elif parent_id not in agent_map or agent_map.get(parent_id, {}).get("role") != "control":
            errors.append(f"智能体{agent_id}必须绑定已登记的根控制角色。")
    if config.get("task_type") == "optimization":
        stop_auditor = str((config.get("optimization_stop_contract") or {}).get("independent_stop_auditor_id", ""))
        if agent_map.get(stop_auditor, {}).get("role") != "audit":
            errors.append("优化停止合同的独立停止审计者必须是已登记的audit独立审计角色。")

    events = require_list(runtime.get("events"), "runtime-evidence.events", errors)
    artifacts = require_list(runtime.get("artifacts"), "runtime-evidence.artifacts", errors)
    event_ids: set[str] = set()
    starts: set[str] = set()
    returns: set[str] = set()
    start_events: dict[str, dict[str, Any]] = {}
    return_events: dict[str, dict[str, Any]] = {}
    skill_events: set[tuple[str, str, str]] = set()
    receipt_ids: set[str] = set()
    artifact_creation_events: dict[str, dict[str, Any]] = {}
    check_completion_events: dict[str, dict[str, Any]] = {}
    for event in events:
        if not isinstance(event, dict):
            errors.append("运行事件必须是对象。")
            continue
        event_id = str(event.get("event_id", "")).strip()
        if not event_id or event_id in event_ids:
            errors.append("运行事件编号缺失或重复。")
        event_ids.add(event_id)
        if event.get("source") not in {"system_trace", "runtime_api", "platform_event_log"} or event.get("exported_by_runtime") is not True:
            errors.append(f"运行事件{event_id}缺少受信来源或运行导出标记。")
        receipt_id = str(event.get("receipt_id", "")).strip()
        if not receipt_id or receipt_id in receipt_ids:
            errors.append(f"运行事件{event_id}缺少唯一的平台回执编号。")
        receipt_ids.add(receipt_id)
        agent_id = str(event.get("agent_id", "")).strip()
        event_time = parse_time(event.get("timestamp"))
        if agent_id not in agent_map or not event_time:
            errors.append(f"运行事件{event_id}的智能体或时间无效。")
        else:
            agent_start = parse_time(agent_map[agent_id].get("started_at"))
            agent_return = parse_time(agent_map[agent_id].get("returned_at"))
            if agent_start and agent_return and not (agent_start <= event_time <= agent_return):
                errors.append(f"运行事件{event_id}发生在智能体真实运行区间之外。")
        kind = event.get("kind")
        if kind == "agent_start":
            starts.add(agent_id)
            start_events[agent_id] = event
        if kind == "agent_return":
            returns.add(agent_id)
            return_events[agent_id] = event
        if kind in {"skill_read", "skill_use"}:
            skill_events.add((str(event.get("work_package_id", "")), str(event.get("skill", "")), str(kind)))
            for field in ("skill_path", "skill_sha256", "platform_run_id"):
                if not nonempty(event.get(field)):
                    errors.append(f"技能事件{event_id}缺少{field}，不能只自填技能名。")
            skill_original = Path(str(event.get("skill_path", "")))
            if not skill_original.is_file():
                errors.append(f"技能事件{event_id}引用的真实技能入口不存在。")
            elif str(event.get("skill_sha256", "")).lower() != sha256(skill_original):
                errors.append(f"技能事件{event_id}的声明校验值与原始技能入口不一致。")
            skill_copy_value = str(event.get("skill_entry_copy_path", ""))
            skill_copy = (root / skill_copy_value).resolve()
            try:
                skill_copy.relative_to(root.resolve())
            except ValueError:
                skill_copy = Path("/__ecc_invalid_skill_copy__")
            if not skill_copy_value or Path(skill_copy_value).is_absolute() or ".." in Path(skill_copy_value).parts or not skill_copy.is_file():
                errors.append(f"技能事件{event_id}缺少证据目录内的技能入口副本。")
            elif str(event.get("skill_sha256", "")).lower() != sha256(skill_copy):
                errors.append(f"技能事件{event_id}的校验值与技能入口副本不一致。")
        if kind == "artifact_created":
            artifact_creation_events[str(event.get("artifact_id", ""))] = event
        if kind == "check_completed":
            check_completion_events[str(event.get("check_id", ""))] = event
    if set(agent_map) - starts or set(agent_map) - returns:
        errors.append("每个真实智能体都必须有系统启动和回传事件。")
    for agent_id, agent in agent_map.items():
        start_event = start_events.get(agent_id, {})
        return_event = return_events.get(agent_id, {})
        if start_event.get("platform_run_id") != agent.get("platform_run_id") or return_event.get("platform_run_id") != agent.get("platform_run_id"):
            errors.append(f"智能体{agent_id}的平台运行编号与系统事件不一致。")
        if start_event.get("timestamp") != agent.get("started_at") or return_event.get("timestamp") != agent.get("returned_at"):
            errors.append(f"智能体{agent_id}的起止时间与系统事件不一致。")

    package_map: dict[str, dict[str, Any]] = {}
    covered_requirements: set[str] = set()
    package_skills: set[str] = set()
    for package in packages:
        if not isinstance(package, dict):
            errors.append("工作包必须是对象。")
            continue
        package_id = str(package.get("work_package_id", "")).strip()
        if not package_id or package_id in package_map:
            errors.append("工作包编号缺失或重复。")
        package_map[package_id] = package
        reqs = {str(x) for x in package.get("requirement_ids") or []}
        if not reqs or not reqs <= requirement_ids:
            errors.append(f"工作包{package_id}没有正确绑定用户要求。")
        covered_requirements |= reqs
        executor = str(package.get("executor_agent_id", ""))
        auditor = str(package.get("auditor_agent_id", ""))
        if agent_map.get(executor, {}).get("role") != "execution":
            errors.append(f"工作包{package_id}的执行者不是工程执行角色。")
        if agent_map.get(auditor, {}).get("role") != "audit" or executor == auditor:
            errors.append(f"工作包{package_id}缺少不同的独立审计者。")
        if not nonempty(package.get("acceptance_criteria")) or not nonempty(package.get("rollback")) or not nonempty(package.get("stop_condition")):
            errors.append(f"工作包{package_id}缺少验收、回滚或停止条件。")
        for skill in package.get("required_skills") or []:
            package_skills.add(str(skill))
            if (package_id, str(skill), "skill_read") not in skill_events or (package_id, str(skill), "skill_use") not in skill_events:
                errors.append(f"工作包{package_id}的必需技能{skill}没有真实读取和使用事件。")
    if not packages:
        errors.append("正式任务至少需要一个真实工作包。")
    if requirement_ids - covered_requirements:
        errors.append("存在没有进入任何工作包的用户要求。")
    if config_skills - package_skills:
        errors.append("运行配置中的必需技能没有全部下沉并绑定到工作包。")

    artifact_ids: set[str] = set()
    artifacts_by_package: set[str] = set()
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            errors.append("产物记录必须是对象。")
            continue
        artifact_id = str(artifact.get("artifact_id", "")).strip()
        package_id = str(artifact.get("work_package_id", "")).strip()
        if not artifact_id or artifact_id in artifact_ids:
            errors.append("产物编号缺失或重复。")
        artifact_ids.add(artifact_id)
        artifacts_by_package.add(package_id)
        producer = str(artifact.get("produced_by_agent_id", ""))
        if package_id not in package_map or producer != str(package_map.get(package_id, {}).get("executor_agent_id", "")):
            errors.append(f"产物{artifact_id}的工作包或生产者无效。")
        copy_value = str(artifact.get("evidence_copy_path", ""))
        copy_path = (root / copy_value).resolve()
        try:
            copy_path.relative_to(root.resolve())
        except ValueError:
            copy_path = Path("/__ecc_invalid_path__")
        if not copy_value or Path(copy_value).is_absolute() or ".." in Path(copy_value).parts or not copy_path.is_file():
            errors.append(f"产物{artifact_id}缺少证据目录内的真实副本。")
        elif str(artifact.get("sha256", "")).lower() != sha256(copy_path):
            errors.append(f"产物{artifact_id}的校验值与真实副本不一致。")
        creation = artifact_creation_events.get(artifact_id)
        if not creation or creation.get("work_package_id") != package_id or creation.get("agent_id") != producer or creation.get("platform_run_id") != agent_map.get(producer, {}).get("platform_run_id"):
            errors.append(f"产物{artifact_id}没有与工程执行者平台运行一致的创建事件。")
        elif creation.get("artifact_sha256") != artifact.get("sha256"):
            errors.append(f"产物{artifact_id}创建事件中的校验值与最终副本不一致。")
        if not nonempty(artifact.get("purpose_chinese")) or artifact.get("artifact_kind") not in {"task_output", "code", "configuration", "data", "model", "report"}:
            errors.append(f"产物{artifact_id}缺少任务用途或有效产物类型。")

    claims = require_list(verification.get("claims"), "verification.claims", errors)
    checks = require_list(verification.get("checks"), "verification.checks", errors)
    audits = require_list(verification.get("audits"), "verification.audits", errors)
    rounds = require_list(verification.get("rounds"), "verification.rounds", errors)
    claim_ids: set[str] = set()
    claim_by_package: dict[str, str] = {}
    for claim in claims:
        if not isinstance(claim, dict): continue
        claim_id = str(claim.get("claim_id", ""))
        package_id = str(claim.get("work_package_id", ""))
        claim_ids.add(claim_id)
        claim_by_package[package_id] = claim_id
        if package_id not in package_map or str(claim.get("executor_agent_id", "")) != str(package_map.get(package_id, {}).get("executor_agent_id", "")):
            errors.append(f"执行声明{claim_id}的工作包或执行者无效。")
        if not set(str(x) for x in claim.get("artifact_ids") or []) <= artifact_ids:
            errors.append(f"执行声明{claim_id}引用了不存在的产物。")
        if not set(str(x) for x in claim.get("requirement_ids") or []) <= requirement_ids:
            errors.append(f"执行声明{claim_id}引用了不存在的用户要求。")
    for package_id in package_map:
        if package_id not in claim_by_package or package_id not in artifacts_by_package:
            errors.append(f"工作包{package_id}缺少执行声明或真实产物。")

    checks_by_package: dict[str, set[str]] = {}
    check_ids: set[str] = set()
    check_evidence_ids: set[str] = set()
    check_times_by_package: dict[str, list[datetime]] = {}
    for check in checks:
        if not isinstance(check, dict): continue
        package_id = str(check.get("work_package_id", ""))
        check_type = str(check.get("check_type", ""))
        check_id = str(check.get("check_id", ""))
        if not check_id or check_id in check_ids:
            errors.append("检查编号缺失或重复。")
        check_ids.add(check_id)
        check_evidence_ids.update(str(x) for x in check.get("evidence_ids") or [])
        if check.get("executed") is True and check.get("result") == "PASS":
            checks_by_package.setdefault(package_id, set()).add(check_type)
        if package_id not in package_map or check.get("result") not in {"PASS", "FAIL"}:
            errors.append("检查记录的工作包或结果无效。")
        completed_at = parse_time(check.get("completed_at"))
        if check.get("executed") is not True or not completed_at:
            errors.append(f"检查{check_id}没有真实执行状态或完成时间。")
        elif completed_at:
            check_times_by_package.setdefault(package_id, []).append(completed_at)
        for field in ("method", "expected", "observed", "raw_result", "raw_result_path", "raw_result_sha256", "runtime_event_id", "exit_code", "evidence_ids"):
            if not nonempty(check.get(field)):
                errors.append(f"工作包{package_id}的检查缺少{field}。")
        raw_value = str(check.get("raw_result_path", ""))
        raw_path = (root / raw_value).resolve()
        try:
            raw_path.relative_to(root.resolve())
        except ValueError:
            raw_path = Path("/__ecc_invalid_check_output__")
        if not raw_value or Path(raw_value).is_absolute() or ".." in Path(raw_value).parts or not raw_path.is_file():
            errors.append(f"检查{check_id}缺少证据目录内的原始结果文件。")
        elif str(check.get("raw_result_sha256", "")).lower() != sha256(raw_path):
            errors.append(f"检查{check_id}的原始结果校验值不一致。")
        check_event = check_completion_events.get(check_id)
        if not check_event or check_event.get("event_id") != check.get("runtime_event_id") or check_event.get("work_package_id") != package_id or check_event.get("timestamp") != check.get("completed_at") or check_event.get("raw_output_sha256") != check.get("raw_result_sha256"):
            errors.append(f"检查{check_id}没有与运行事件、时间和原始结果形成一致绑定。")

    audit_by_claim: dict[str, dict[str, Any]] = {}
    audit_ids: set[str] = set()
    audit_evidence_ids: set[str] = set()
    for audit in audits:
        if not isinstance(audit, dict): continue
        claim_id = str(audit.get("claim_id", ""))
        audit_id = str(audit.get("audit_id", ""))
        if not audit_id or audit_id in audit_ids:
            errors.append("审计编号缺失或重复。")
        audit_ids.add(audit_id)
        audit_evidence_ids.update(str(x) for x in audit.get("evidence_ids") or [])
        audit_by_claim[claim_id] = audit
        package_id = next((pid for pid, cid in claim_by_package.items() if cid == claim_id), "")
        if claim_id not in claim_ids or str(audit.get("auditor_agent_id", "")) != str(package_map.get(package_id, {}).get("auditor_agent_id", "")):
            errors.append(f"声明{claim_id}缺少有效独立审计者。")
        if audit.get("decision") not in {"ACCEPT", "REJECT"} or not nonempty(audit.get("reason_chinese")):
            errors.append(f"声明{claim_id}的审计决定或中文理由无效。")
        audit_time = parse_time(audit.get("decided_at"))
        auditor_return = parse_time(agent_map.get(str(audit.get("auditor_agent_id", "")), {}).get("returned_at"))
        if not audit_time or (auditor_return and audit_time > auditor_return):
            errors.append(f"声明{claim_id}的审计决定时间无效。")
        if audit_time and check_times_by_package.get(package_id) and audit_time < max(check_times_by_package[package_id]):
            errors.append(f"声明{claim_id}的审计时间早于确定性检查完成时间。")

    round_map: dict[str, list[dict[str, Any]]] = {}
    round_ids: set[str] = set()
    for item in rounds:
        if isinstance(item, dict):
            round_id = str(item.get("round_id", ""))
            if not round_id or round_id in round_ids:
                errors.append("返修轮次缺少唯一round_id。")
            round_ids.add(round_id)
            round_map.setdefault(str(item.get("work_package_id", "")), []).append(item)
    maximum_rounds = int(number(config.get("max_repair_rounds", 3), "最大返修轮数", errors))
    for package_id, package_rounds in round_map.items():
        if any(int(item.get("round", -1)) > maximum_rounds for item in package_rounds):
            errors.append(f"工作包{package_id}超过最大返修轮数。")
    final_status = str(final.get("final_status", ""))
    if final_status == "PASS":
        for package_id, claim_id in claim_by_package.items():
            if not {"SUCCESS", "NEGATIVE"} <= checks_by_package.get(package_id, set()):
                errors.append(f"通过工作包{package_id}必须同时有成功和错误案例。")
            if audit_by_claim.get(claim_id, {}).get("decision") != "ACCEPT":
                errors.append(f"通过工作包{package_id}没有被独立审计接受。")
            package_rounds = sorted(round_map.get(package_id, []), key=lambda x: x.get("round", -1))
            if not package_rounds or [x.get("round") for x in package_rounds] != list(range(len(package_rounds))):
                errors.append(f"工作包{package_id}的轮次必须从0连续记录。")
            for item in package_rounds[1:]:
                if item.get("strategy_changed") is not True:
                    errors.append(f"工作包{package_id}第1轮起必须改变返修策略。")
            if package_rounds and package_rounds[-1].get("decision") != "ACCEPT":
                errors.append(f"通过工作包{package_id}最后一轮没有接受。")

    delivery = require_dict(verification.get("delivery_safety"), "verification.delivery_safety", errors)
    if final_status == "PASS":
        for field in ("metadata_checked", "secrets_checked", "internal_paths_checked", "temporary_materials_checked", "attachments_checked", "references_checked", "accepted"):
            if delivery.get(field) is not True:
                errors.append(f"最终通过前交付安全字段{field}必须为真。")

    checkpoint_ids: set[str] = set()
    checkpoint_times: list[datetime] = []
    checkpoint_evidence_ids: set[str] = set()
    for checkpoint in checkpoints:
        if not isinstance(checkpoint, dict): continue
        checkpoint_id = str(checkpoint.get("checkpoint_id", ""))
        timestamp = parse_time(checkpoint.get("timestamp"))
        if not checkpoint_id or checkpoint_id in checkpoint_ids or not timestamp:
            errors.append("检查点编号缺失、重复或时间无效。")
        checkpoint_ids.add(checkpoint_id)
        if timestamp: checkpoint_times.append(timestamp)
        if not nonempty(checkpoint.get("meaningful_progress")) or not nonempty(checkpoint.get("evidence_ids")):
            errors.append(f"检查点{checkpoint_id}缺少真实进展或证据。")
        checkpoint_evidence_ids.update(str(x) for x in checkpoint.get("evidence_ids") or [])
        if not isinstance(checkpoint.get("layer_number"), int) or not 1 <= checkpoint.get("layer_number") <= 12:
            errors.append(f"检查点{checkpoint_id}的层号无效。")
        if not set(str(x) for x in checkpoint.get("work_package_ids") or []) <= set(package_map):
            errors.append(f"检查点{checkpoint_id}引用了不存在的工作包。")
    if checkpoint_times != sorted(checkpoint_times):
        errors.append("检查点时间必须严格按真实顺序记录。")
    if not any(isinstance(x, dict) and x.get("is_final") is True for x in checkpoints):
        errors.append("缺少最终检查点。")

    if final_status not in STATUSES or not nonempty(final.get("status_code_chinese")):
        errors.append("最终状态无效或缺少中文解释。")
    if agent_map.get(str(final.get("final_signer_agent_id", "")), {}).get("role") != "control":
        errors.append("最终签署者必须是已登记的根控制角色。")
    elapsed = number(final.get("elapsed_minutes", 0), "elapsed_minutes实际用时", errors)
    expected_lower = number(config.get("expected_duration_lower_minutes", 0), "预计时长下界", errors)
    assessment = final.get("early_completion_assessment")
    assessment_auditor = ""
    reliable_history = False
    assessment_history_ids: set[str] = set()
    if config.get("task_type") in {"production", "optimization"}:
        if not isinstance(assessment, dict):
            errors.append("生产和开放式优化任务必须有独立早完异常判断。")
            assessment = {}
        assessment_auditor = str(assessment.get("auditor_agent_id", ""))
        if agent_map.get(assessment_auditor, {}).get("role") != "audit" or not nonempty(assessment.get("basis_chinese")):
            errors.append("早完异常判断必须由独立审计角色给出中文依据。")
        reliable_history = assessment.get("reliable_history_available") is True
        if number(assessment.get("expected_duration_lower_minutes", 0), "早完判断预计下界", errors) != expected_lower:
            errors.append("早完异常判断中的预计下界必须与运行配置完全一致。")
        if reliable_history:
            if expected_lower <= 0 or not nonempty(assessment.get("history_basis_evidence_ids")):
                errors.append("声称有可靠历史范围时，必须提供正数下界和历史依据证据。")
            assessment_history_ids = {str(x) for x in assessment.get("history_basis_evidence_ids") or []}
        elif expected_lower != 0:
            errors.append("没有可靠历史范围时，预计下界必须为0，不能伪装精确基线。")
        for field, actual in (
            ("goal_count", len(requirements)),
            ("work_package_count", len(packages)),
            ("artifact_count", len(artifacts)),
            ("check_count", len(checks)),
        ):
            if assessment.get(field) != actual:
                errors.append(f"早完异常判断的{field}与真实运行记录不一致。")
        must_review = (not reliable_history) or (expected_lower > 0 and elapsed < expected_lower)
        if must_review and assessment.get("is_anomalously_early") is not True:
            errors.append("首次运行或低于可靠历史下界时必须标记异常并执行专项复核。")
        if must_review:
            review = final.get("early_completion_review")
            if not isinstance(review, dict):
                errors.append("缺少完整的异常早完专项复核。")
                review = {}
            if review.get("accepted") is not True or str(review.get("auditor_agent_id", "")) != assessment_auditor:
                errors.append("异常早完专项复核未由同一独立审计角色接受。")
            for field in ("goal_coverage_complete", "all_work_packages_handled", "required_skills_used", "multi_agent_receipts_complete", "real_outputs_present", "deterministic_checks_run", "negative_cases_run", "no_skipped_items", "independent_audit"):
                if review.get(field) is not True:
                    errors.append(f"异常早完专项复核缺少通过项：{field}。")
            if not nonempty(review.get("evidence_ids")) or not nonempty(review.get("reason_chinese")):
                errors.append("异常早完专项复核缺少证据编号或中文理由。")
    if final_status == "PASS":
        if any(isinstance(layer, dict) and layer.get("status") != "PASS" for layer in layers):
            errors.append("最终通过时十二层必须逐层通过。")
        for field in ("twelve_layers_complete", "real_multi_agent_accepted", "skill_gates_accepted", "deterministic_checks_accepted", "independent_audit_accepted", "delivery_safety_accepted", "handoff_accepted"):
            if final.get(field) is not True:
                errors.append(f"最终通过时{field}必须为真。")
        if nonempty(final.get("open_blockers")) or nonempty(final.get("open_rejections")):
            errors.append("最终通过不能保留阻塞或拒绝项。")
    optimization_evidence_ids: set[str] = set()
    optimization_experiment_ids: set[str] = set()
    if config.get("task_type") == "optimization":
        experiments = verification.get("optimization_experiments")
        if not isinstance(experiments, list) or not experiments:
            errors.append("开放式优化必须保存至少一轮实验、结果或排除证据。")
        else:
            for item in experiments:
                if not isinstance(item, dict) or not all(nonempty(item.get(field)) for field in ("candidate", "metric_before", "metric_after", "result_chinese", "evidence_ids")):
                    errors.append("开放式优化实验记录缺少候选、前后指标、中文结果或证据。")
                elif isinstance(item, dict):
                    item_ids = {str(x) for x in item.get("evidence_ids") or []}
                    optimization_experiment_ids |= item_ids
                    optimization_evidence_ids |= item_ids
        decision = final.get("optimization_stop_decision")
        expected_auditor = str((config.get("optimization_stop_contract") or {}).get("independent_stop_auditor_id", ""))
        if not isinstance(decision, dict) or decision.get("accepted") is not True or str(decision.get("auditor_agent_id", "")) != expected_auditor or not nonempty(decision.get("matched_stop_condition")) or not nonempty(decision.get("evidence_ids")):
            errors.append("开放式优化缺少由预定独立审计者接受的最终停止决定和证据。")
        else:
            decision_ids = {str(x) for x in decision.get("evidence_ids") or []}
            optimization_evidence_ids |= decision_ids
            if not optimization_experiment_ids <= decision_ids:
                errors.append("开放式优化停止决定没有引用全部实验或排除依据。")
    handoff = final.get("handoff")
    if not isinstance(handoff, dict) or not nonempty(handoff.get("handoff_evidence_id")) or not nonempty(handoff.get("recovery_entry")) or not nonempty(handoff.get("remaining_risks")):
        errors.append("最终验收缺少可恢复交接。")
        handoff = {}
    final_evidence_id = str(final.get("final_acceptance_evidence_id", ""))
    if not final_evidence_id:
        errors.append("最终验收缺少专属证据编号。")
    if not has_chinese(report):
        errors.append("final-report.md必须以足够完整的中文说明目标、证据、结果和风险。")
    handoff_ids = {str(handoff.get("handoff_evidence_id", ""))} - {""}
    final_ids = {final_evidence_id} - {""}
    known_evidence_ids = event_ids | artifact_ids | check_ids | audit_ids | requirement_ids | set(package_map) | claim_ids | round_ids | checkpoint_ids | handoff_ids | final_ids
    referenced_evidence_ids = layer_evidence_ids | agent_evidence_ids | check_evidence_ids | audit_evidence_ids | checkpoint_evidence_ids | optimization_evidence_ids
    missing_evidence = sorted(referenced_evidence_ids - known_evidence_ids)
    if missing_evidence:
        errors.append(f"这些证据编号没有对应运行事件、产物、检查或审计记录：{', '.join(missing_evidence)}。")
    if assessment_history_ids - known_evidence_ids:
        errors.append("早完异常判断引用了不存在的历史依据证据。")
    layer_map = {x.get("layer_number"): set(str(v) for v in x.get("evidence_ids") or []) for x in layers if isinstance(x, dict)}
    start_event_ids = {event_id for event_id, event in ((str(x.get("event_id", "")), x) for x in events if isinstance(x, dict)) if event.get("kind") == "agent_start"}
    return_event_ids = {event_id for event_id, event in ((str(x.get("event_id", "")), x) for x in events if isinstance(x, dict)) if event.get("kind") == "agent_return"}
    materials_return_ids = {event_id for event_id, event in ((str(x.get("event_id", "")), x) for x in events if isinstance(x, dict)) if event.get("kind") == "agent_return" and agent_map.get(str(event.get("agent_id", "")), {}).get("role") == "materials"}
    control_return_ids = {event_id for event_id, event in ((str(x.get("event_id", "")), x) for x in events if isinstance(x, dict)) if event.get("kind") == "agent_return" and agent_map.get(str(event.get("agent_id", "")), {}).get("role") == "control"}
    skill_event_ids = {str(x.get("event_id", "")) for x in events if isinstance(x, dict) and x.get("kind") in {"skill_read", "skill_use"}}
    required_check_ids = {str(x.get("check_id", "")) for x in checks if isinstance(x, dict) and x.get("check_type") in {"SUCCESS", "NEGATIVE"} and x.get("result") == "PASS"}
    if not requirement_ids <= layer_map.get(1, set()):
        errors.append("第1层必须引用全部用户要求编号。")
    if not materials_return_ids <= layer_map.get(2, set()):
        errors.append("第2层必须引用资料角色的回传事件。")
    if config_skills and not skill_event_ids <= layer_map.get(3, set()):
        errors.append("第3层必须引用全部必需技能读取和使用事件。")
    if not config_skills and not materials_return_ids <= layer_map.get(3, set()):
        errors.append("没有外部技能时，第3层仍需引用资料角色确认无需技能的回传证据。")
    if not set(package_map) <= layer_map.get(4, set()):
        errors.append("第4层必须引用全部工作包编号。")
    if not start_event_ids <= layer_map.get(5, set()):
        errors.append("第5层必须引用四类真实智能体的全部启动事件。")
    if not (artifact_ids | claim_ids) <= layer_map.get(6, set()):
        errors.append("第6层必须引用全部执行声明和任务本体产物。")
    if not checkpoint_ids <= layer_map.get(7, set()):
        errors.append("第7层必须引用全部动作级检查点。")
    if not required_check_ids <= layer_map.get(8, set()):
        errors.append("第8层必须引用成功和错误案例检查。")
    if not audit_ids <= layer_map.get(9, set()):
        errors.append("第9层必须引用独立审计记录。")
    if not round_ids <= layer_map.get(10, set()):
        errors.append("第10层必须引用第0轮和实际返修轮次。")
    if not handoff_ids <= layer_map.get(11, set()):
        errors.append("第11层必须引用交接和恢复证据。")
    if not (final_ids | control_return_ids) <= layer_map.get(12, set()):
        errors.append("第12层必须引用最终签署和控制角色回传证据。")
    platform_review = final.get("platform_receipts_recheck")
    if not isinstance(platform_review, dict) or platform_review.get("accepted") is not True or agent_map.get(str(platform_review.get("auditor_agent_id", "")), {}).get("role") != "audit" or not nonempty(platform_review.get("method_chinese")) or not nonempty(platform_review.get("evidence_ids")):
        errors.append("正式通过前必须由独立审计者保存平台侧回执复核；仅自填来源和导出标记不能证明真实运行。")
    else:
        platform_ids = {str(x) for x in platform_review.get("evidence_ids") or []}
        if platform_ids != event_ids:
            errors.append("平台侧回执复核必须完整覆盖全部运行事件，不能只抽查一个回执。")
    agent_starts = [parse_time(x.get("started_at")) for x in agents if isinstance(x, dict)]
    agent_returns = [parse_time(x.get("returned_at")) for x in agents if isinstance(x, dict)]
    if agent_starts and agent_returns and all(agent_starts) and all(agent_returns):
        wall_minutes = (max(agent_returns) - min(agent_starts)).total_seconds() / 60
        if abs(wall_minutes - elapsed) > 2:
            errors.append("声明耗时与真实智能体最早启动、最晚回传形成的时间范围不一致。")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("用法：python3 validate_standard_evidence.py <证据目录>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    errors = validate(root)
    if errors:
        print(json.dumps({"status": "FAIL", "status_chinese": "不通过", "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"status": "STRUCTURE_PASS", "status_chinese": "结构检查通过", "message": "七文件标准证据的可确定结构和交叉引用已通过；脚本不能认证平台事件签名，仍需第9层核对受信平台回执和第12层最终验收。"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
