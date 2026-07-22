#!/usr/bin/env python3
"""验证ECC四角色十二层闭环的结构化运行证据。

本脚本检查可确定的结构和硬门，不替代第9层独立审计与第12层最终验收。
机器字段保留英文，所有错误都同时给出中文解释。
"""

from __future__ import annotations

import json
import hashlib
import math
import ntpath
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


JSON_FILES = (
    "run-config.json",
    "layer-status.json",
    "declared-requirements.json",
    "completion-ledger.json",
    "source-confidence-register.json",
    "tool-inventory.json",
    "agents.json",
    "work-packages.json",
    "execution-claims.json",
    "artifact-manifest.json",
    "deterministic-checks.json",
    "claim-acceptance-matrix.json",
    "rounds.json",
    "checkpoints.json",
    "delivery-safety-check.json",
    "handoff.json",
    "evidence-index.json",
    "final-acceptance.json",
)

TEXT_FILES = ("final-acceptance.md", "final-report.md")

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

LAYER_REQUIRED_FIELDS = (
    ("positioning", "本层定位"),
    ("purpose", "本层目的"),
    ("inputs", "本层输入"),
    ("actions", "本层动作"),
    ("artifacts", "本层产物"),
    ("file_requirements", "本层文件要求"),
    ("content_requirements", "本层内容要求"),
    ("prohibitions", "本层禁止事项"),
    ("time_policy", "本层时间门槛关联"),
    ("multi_agent_requirements", "本层多智能体要求"),
    ("verification_method", "本层验证方法"),
    ("failure_return", "失败返回"),
    ("evidence_paths", "证据路径"),
    ("next_layer_condition", "连接下一层条件"),
    ("task_application", "本任务具体应用"),
)

FINAL_STATUSES = {"PASS", "PARTIAL", "BLOCKED", "REJECTED"}
LAYER_STATUSES = {"PASS", "PARTIAL", "BLOCKED", "REJECTED"}

ALIAS_KEYS = {
    "execution-claims": "execution-claims.json",
    "artifact-manifest": "artifact-manifest.json",
    "script-verification-result": "deterministic-checks.json",
    "claim-acceptance-matrix": "claim-acceptance-matrix.json",
    "repair-loop-log": "rounds.json",
    "compact-handoff": "handoff.json",
    "evidence-index": "evidence-index.json",
    "final-acceptance-structured": "final-acceptance.json",
    "final-acceptance-readable": "final-acceptance.md",
    "final-report": "final-report.md",
}


def nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) > 0
    return True


def read_json(path: Path, errors: list[str]) -> Any:
    if not path.is_file():
        errors.append(f"缺少必需文件：{path.name}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"文件无法解析：{path.name}；原因：{exc}")
        return None


def read_text(path: Path, errors: list[str]) -> str:
    if not path.is_file():
        errors.append(f"缺少必需文件：{path.name}")
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"文件无法读取：{path.name}；原因：{exc}")
        return ""


def require_object(value: Any, name: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{name}必须是对象。")
        return {}
    return value


def require_list(value: Any, name: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{name}必须是数组。")
        return []
    return value


def drive_letter(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    normalized = value.strip().replace("/", "\\")
    if len(normalized) < 3 or normalized[1:3] != ":\\":
        return ""
    return normalized[0].upper()


def normalized_windows_path(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        return ""
    return ntpath.normcase(ntpath.normpath(value.strip().replace("/", "\\")))


def safe_float(value: Any, label: str, errors: list[str], default: float = 0.0) -> float:
    if isinstance(value, bool):
        errors.append(f"{label}必须是数字，不能是布尔值。")
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        errors.append(f"{label}必须是有效数字。")
        return default
    if not math.isfinite(number):
        errors.append(f"{label}必须是有限数字。")
        return default
    return number


def safe_int(value: Any, label: str, errors: list[str], default: int = 0) -> int:
    if isinstance(value, bool):
        errors.append(f"{label}必须是整数，不能是布尔值。")
        return default
    try:
        number = int(value)
    except (TypeError, ValueError):
        errors.append(f"{label}必须是有效整数。")
        return default
    if isinstance(value, float) and not value.is_integer():
        errors.append(f"{label}必须是整数。")
        return default
    return number


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        return parsed if parsed.tzinfo is not None else None
    except ValueError:
        return None


def verified_relative_file(root: Path, value: Any) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        return None
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        return None
    return resolved if resolved.is_file() else None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_contains_han(value: Any) -> bool:
    """判断用户可读字段是否真的含有汉字，而不是只写英文占位。"""
    if isinstance(value, str):
        return bool(re.search(r"[\u3400-\u4dbf\u4e00-\u9fff]", value))
    if isinstance(value, list):
        return any(text_contains_han(item) for item in value)
    if isinstance(value, dict):
        return any(text_contains_han(item) for item in value.values())
    return False


def chinese_is_primary(content: str) -> bool:
    """用户主文必须以中文为主体；英文代码、路径和固定名仍可保留。"""
    han = len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", content))
    latin = len(re.findall(r"[A-Za-z]", content))
    return han >= 60 and han >= (han + latin) * 0.45


CHINESE_FIELD_KEYS = {
    "description_chinese",
    "chinese_conclusion",
    "status_code_chinese",
    "statement_chinese",
    "reason_chinese",
    "chinese_reason",
    "acceptance_criteria",
    "positioning",
    "purpose",
    "inputs",
    "actions",
    "artifacts",
    "content_requirements",
    "prohibitions",
    "time_policy",
    "multi_agent_requirements",
    "verification_method",
    "failure_return",
    "next_layer_condition",
    "task_application",
    "responsibility",
    "work_evidence",
    "measured_benefit",
    "merge_cost",
    "meaningful_progress",
    "artifact_delta",
    "audit_decision",
    "meaningful_delta",
    "reason",
    "build_from_scratch_reason",
    "project_affiliation",
    "operation_type",
    "goal",
    "rollback",
    "stop_condition",
    "hypothesis",
    "expected",
    "observed",
    "kind",
    "disposition",
    "claim",
    "evidence",
    "uncertainty",
    "verified_facts",
    "remaining_risks",
}


def validate_chinese_fields(value: Any, errors: list[str], path: str = "") -> None:
    """递归检查明确声明为中文或面向用户的字段。"""
    if isinstance(value, dict):
        for key, item in value.items():
            item_path = f"{path}.{key}" if path else str(key)
            if key in CHINESE_FIELD_KEYS or key.endswith("_chinese"):
                if nonempty(item) and not text_contains_han(item):
                    errors.append(f"{item_path}必须包含真实中文说明，不能只写英文、代码或占位符。")
            validate_chinese_fields(item, errors, item_path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            validate_chinese_fields(item, errors, f"{path}[{index}]")


def secret_like_paths(value: Any, prefix: str = "") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            lowered = str(key).lower()
            if re.search(r"(^|_)(api_?key|secret|password|access_?token|private_?key)($|_)", lowered):
                if nonempty(item) and not lowered.endswith(("_risk", "_redacted", "_present")):
                    findings.append(path)
            findings.extend(secret_like_paths(item, path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            findings.extend(secret_like_paths(item, f"{prefix}[{index}]"))
    return findings


def text_contains_secret(content: str) -> bool:
    direct_patterns = (
        r"\bsk-[A-Za-z0-9_-]{20,}\b",
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        r"(?i)\b(?:api[_-]?key|password|access[_-]?token|private[_-]?key)\b\s*[:=]\s*[\"']?(?!已脱敏|redacted|none|null)[^\s\"']{8,}",
    )
    return any(re.search(pattern, content) for pattern in direct_patterns)


def validate_secret_texts(
    root: Path,
    texts: dict[str, str],
    artifacts: list[Any],
    errors: list[str],
) -> None:
    for filename, content in texts.items():
        if text_contains_secret(content):
            errors.append(f"{filename}疑似包含未脱敏密钥或口令。")
    for item in artifacts:
        if not isinstance(item, dict):
            continue
        artifact_id = str(item.get("artifact_id", ""))
        evidence_copy = verified_relative_file(root, item.get("evidence_copy_path"))
        if not evidence_copy:
            continue
        try:
            content = evidence_copy.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if text_contains_secret(content):
            errors.append(f"产物{artifact_id}的证据副本疑似包含未脱敏密钥或口令。")


def validate(root: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    data = {name: read_json(root / name, errors) for name in JSON_FILES}
    texts = {name: read_text(root / name, errors) for name in TEXT_FILES}
    if errors:
        return result(errors, warnings)

    config = require_object(data["run-config.json"], "run-config.json", errors)
    acceptance = require_object(data["final-acceptance.json"], "final-acceptance.json", errors)
    layers = require_list(data["layer-status.json"], "layer-status.json", errors)
    requirements = require_list(data["declared-requirements.json"], "declared-requirements.json", errors)
    ledger = require_list(data["completion-ledger.json"], "completion-ledger.json", errors)
    sources = require_list(data["source-confidence-register.json"], "source-confidence-register.json", errors)
    tools = require_list(data["tool-inventory.json"], "tool-inventory.json", errors)
    agents = require_list(data["agents.json"], "agents.json", errors)
    packages = require_list(data["work-packages.json"], "work-packages.json", errors)
    claims = require_list(data["execution-claims.json"], "execution-claims.json", errors)
    artifacts = require_list(data["artifact-manifest.json"], "artifact-manifest.json", errors)
    checks = require_list(data["deterministic-checks.json"], "deterministic-checks.json", errors)
    matrix = require_list(data["claim-acceptance-matrix.json"], "claim-acceptance-matrix.json", errors)
    rounds = require_list(data["rounds.json"], "rounds.json", errors)
    checkpoints = require_list(data["checkpoints.json"], "checkpoints.json", errors)
    delivery = require_object(data["delivery-safety-check.json"], "delivery-safety-check.json", errors)
    handoff = require_object(data["handoff.json"], "handoff.json", errors)
    evidence_index = require_object(data["evidence-index.json"], "evidence-index.json", errors)

    final_status = acceptance.get("final_status")
    if final_status not in FINAL_STATUSES:
        errors.append("final_status只能是PASS、PARTIAL、BLOCKED或REJECTED，并须在用户报告中给出中文解释。")
    task_type = config.get("task_type")
    if task_type not in ("production", "optimization", "endurance", "preparation"):
        errors.append("task_type必须是production、optimization、endurance或preparation，中文分别是真实生产、开放式优化、耐力验证、准备任务。")

    truthful_preparation_block = (
        task_type == "preparation"
        and final_status in {"BLOCKED", "PARTIAL"}
        and config.get("real_multi_agent_available") is False
        and nonempty(config.get("multi_agent_unavailable_reason"))
    )

    indexed_evidence_ids, indexed_evidence_files = validate_evidence_index(root, evidence_index, errors)
    config_evidence_ids = validate_config(config, acceptance, indexed_evidence_ids, errors)
    validate_layers(layers, final_status, errors)
    requirement_ids, ledger_evidence_ids = validate_requirements(requirements, ledger, final_status, errors)
    source_map, source_evidence_ids = validate_sources(
        sources, config, indexed_evidence_ids, errors
    )
    validate_tools(tools, config, errors)
    agent_ids, role_by_agent, agent_evidence_ids = validate_agents(
        root, agents, config, indexed_evidence_files, truthful_preparation_block, errors
    )
    validate_ledger_auditors(ledger, agent_ids, role_by_agent, errors)
    package_ids, executors, package_map, skill_evidence_ids = validate_packages(
        packages,
        requirement_ids,
        agent_ids,
        role_by_agent,
        indexed_evidence_files,
        final_status,
        truthful_preparation_block,
        errors,
    )
    artifact_ids, artifact_map = validate_artifacts(
        root, artifacts, package_ids, package_map, agent_ids, role_by_agent, final_status, errors
    )
    claim_ids, claim_evidence_ids = validate_claims(
        claims,
        package_ids,
        package_map,
        requirement_ids,
        agent_ids,
        role_by_agent,
        artifact_ids,
        artifact_map,
        source_map,
        skill_evidence_ids,
        final_status,
        errors,
    )
    check_evidence_ids = validate_checks(checks, package_ids, config, final_status, errors)
    validate_package_check_bindings(packages, checks, errors)
    matrix_evidence_ids = validate_matrix(matrix, claims, claim_ids, role_by_agent, final_status, errors)
    validate_rounds(
        rounds, packages, package_ids, checks, indexed_evidence_ids, config, errors
    )
    checkpoint_evidence_ids = validate_checkpoints(
        checkpoints, task_type, package_ids, indexed_evidence_ids, errors
    )
    validate_delivery(delivery, role_by_agent, final_status, truthful_preparation_block, errors)
    validate_handoff(handoff, final_status, errors)
    validate_aliases(evidence_index, errors)
    validate_time(
        config,
        acceptance,
        checkpoints,
        agents,
        requirements,
        packages,
        artifacts,
        checks,
        role_by_agent,
        indexed_evidence_ids,
        errors,
    )
    validate_drives(config, agents, artifacts, errors)
    validate_final(
        acceptance,
        texts,
        layers,
        requirements,
        ledger,
        packages,
        claims,
        matrix,
        agent_ids,
        role_by_agent,
        executors,
        delivery,
        truthful_preparation_block,
        errors,
    )

    status_evidence_ids = {str(item) for item in acceptance.get("status_code_evidence_ids") or []}
    referenced_evidence_ids = (
        ledger_evidence_ids
        | check_evidence_ids
        | matrix_evidence_ids
        | agent_evidence_ids
        | skill_evidence_ids
        | claim_evidence_ids
        | checkpoint_evidence_ids
        | status_evidence_ids
        | config_evidence_ids
        | source_evidence_ids
    )
    missing_index_entries = sorted(referenced_evidence_ids - indexed_evidence_ids)
    if missing_index_entries:
        errors.append(f"这些被引用的证据编号未进入evidence-index（证据索引）：{', '.join(missing_index_entries)}。")

    secret_paths = secret_like_paths(data)
    if secret_paths:
        errors.append(f"结构化证据疑似保存了密钥值，必须脱敏；字段：{', '.join(secret_paths)}。")
    validate_secret_texts(root, texts, artifacts, errors)

    validate_chinese_fields(data, errors)

    if not requirement_ids:
        errors.append("至少需要一项Declared Requirement（已声明要求），不能用空目标通过。")
    if errors:
        return result(errors, warnings)
    return result(errors, warnings)


def validate_config(
    config: dict[str, Any],
    acceptance: dict[str, Any],
    indexed_evidence_ids: set[str],
    errors: list[str],
) -> set[str]:
    referenced_evidence_ids: set[str] = set()
    for field, chinese in (
        ("task_id", "任务编号"),
        ("project_affiliation", "项目归属"),
        ("operation_type", "操作类型"),
        ("size_tier", "任务规模"),
        ("active_harnesses", "实际执行环境"),
    ):
        if not nonempty(config.get(field)):
            errors.append(f"run-config.json缺少{field}，中文意思是{chinese}。")
    if config.get("real_multi_agent_required") is not True:
        errors.append("real_multi_agent_required必须为true，中文意思是真实多智能体是正式长任务硬门。")
    if acceptance.get("final_status") == "PASS" and config.get("real_multi_agent_available") is not True:
        errors.append("最终通过时real_multi_agent_available必须为true，中文意思是真实多智能体能力已经实际可用。")
    if config.get("logical_isolation_can_satisfy_gate") is not False:
        errors.append("logical_isolation_can_satisfy_gate必须为false，中文意思是逻辑隔离不能代替真实子智能体。")
    if config.get("required_roles") != ["control", "materials", "execution", "audit"]:
        errors.append("required_roles必须依次包含控制、资料、工程执行、独立审计四类角色。")
    if config.get("task_type") == "optimization":
        contract = config.get("optimization_stop_contract")
        if not isinstance(contract, dict):
            errors.append("开放式优化必须预先建立optimization_stop_contract优化停止合同。")
        else:
            for field in ("baseline_metric", "target_metric", "initial_candidates", "no_gain_round_limit", "cost_or_risk_limit", "max_window_minutes", "independent_stop_auditor_id"):
                if not nonempty(contract.get(field)):
                    errors.append(f"优化停止合同缺少{field}。")
    if config.get("mature_component_review_required") is True:
        review = config.get("mature_component_review")
        if not isinstance(review, dict):
            errors.append("需要成熟组件比较，但缺少mature_component_review对象。")
        else:
            if not nonempty(review.get("routes_compared")):
                errors.append("成熟组件比较缺少直接采用、小幅适配和自研等路线。")
            if not nonempty(review.get("selected_route")) or not nonempty(review.get("reason")):
                errors.append("成熟组件比较缺少选定路线或中文理由。")
            if review.get("selected_route") == "BUILD_FROM_SCRATCH" and not nonempty(review.get("build_from_scratch_reason")):
                errors.append("选择从零自研时必须记录没有采用成熟方案的具体理由。")
    model_route = config.get("model_tool_route")
    if not isinstance(model_route, dict):
        errors.append("缺少model_tool_route，中文意思是模型、工具和执行环境的计划与实际路线。")
    else:
        planned = model_route.get("planned")
        actual = model_route.get("actual")
        if not nonempty(planned) or not nonempty(actual):
            errors.append("模型和工具路线必须同时记录planned（计划）与actual（实际）。")
        if planned != actual:
            evidence_id = str(model_route.get("change_authorization_evidence_id", "")).strip()
            if not evidence_id or evidence_id not in indexed_evidence_ids:
                errors.append("实际模型或工具路线与计划不一致，但没有进入证据索引的批准证据编号。")
            else:
                referenced_evidence_ids.add(evidence_id)
    if acceptance.get("final_status") == "PASS" and config.get("formal_modification_authorized") is False:
        if config.get("task_type") == "production" and config.get("production_goal_requires_writes") is True:
            errors.append("生产目标需要正式写入，但没有正式修改授权，不能最终通过。")
    if config.get("k_drive_mode", "disabled") == "user_approved_backup_only":
        evidence_id = str(config.get("k_drive_user_approval_evidence_id", "")).strip()
        if not evidence_id or evidence_id not in indexed_evidence_ids:
            errors.append("K盘备份必须引用进入证据索引的用户批准证据编号。")
        else:
            referenced_evidence_ids.add(evidence_id)
    return referenced_evidence_ids


def validate_layers(layers: list[Any], final_status: Any, errors: list[str]) -> None:
    if len(layers) != 12:
        errors.append(f"layer-status.json必须恰好有12层，当前为{len(layers)}层。")
    by_number: dict[int, dict[str, Any]] = {}
    for index, item in enumerate(layers):
        label = f"layer-status.json第{index + 1}项"
        if not isinstance(item, dict):
            errors.append(f"{label}必须是对象。")
            continue
        expected_number, expected_english, expected_chinese = LAYER_SPECS[index] if index < 12 else (None, None, None)
        if expected_number is not None and (
            item.get("layer_number") != expected_number
            or item.get("english_name") != expected_english
            or item.get("chinese_name") != expected_chinese
        ):
            errors.append(
                f"{label}位置错误；数组第{index + 1}项必须是第{expected_number}层"
                f"{expected_english}（{expected_chinese}），不得重排。"
            )
        number = item.get("layer_number")
        if not isinstance(number, int) or number in by_number:
            errors.append(f"{label}的layer_number缺失、无效或重复。")
            continue
        by_number[number] = item
    for number, english, chinese in LAYER_SPECS:
        item = by_number.get(number)
        if not item:
            errors.append(f"缺少第{number}层：{english}（{chinese}）。")
            continue
        if item.get("english_name") != english:
            errors.append(f"第{number}层英文固定名必须是{english}。")
        if item.get("chinese_name") != chinese:
            errors.append(f"第{number}层中文固定名必须是“{chinese}”，不得改写。")
        if item.get("skippable") is not False:
            errors.append(f"第{number}层必须明确skippable=false，中文意思是不允许跳过。")
        if item.get("status") not in LAYER_STATUSES:
            errors.append(f"第{number}层状态无效。")
        if final_status == "PASS" and item.get("status") != "PASS":
            errors.append(f"最终通过但第{number}层状态不是PASS（通过）。")
        for field, chinese_field in LAYER_REQUIRED_FIELDS:
            if not nonempty(item.get(field)):
                errors.append(f"第{number}层缺少{field}，中文意思是{chinese_field}。")
    if final_status in {"PARTIAL", "BLOCKED", "REJECTED"} and by_number:
        if all(item.get("status") == "PASS" for item in by_number.values()):
            errors.append("最终状态不是通过，但十二层全部写成PASS；必须在真实失败层记录部分完成、阻塞或拒绝。")


def validate_requirements(
    requirements: list[Any], ledger: list[Any], final_status: Any, errors: list[str]
) -> tuple[set[str], set[str]]:
    requirement_ids: set[str] = set()
    for index, item in enumerate(requirements):
        label = f"declared-requirements.json第{index + 1}项"
        if not isinstance(item, dict):
            errors.append(f"{label}必须是对象。")
            continue
        req_id = str(item.get("requirement_id", "")).strip()
        if not req_id or req_id in requirement_ids:
            errors.append(f"{label}的requirement_id缺失或重复。")
        requirement_ids.add(req_id)
        if not nonempty(item.get("description_chinese")) or not nonempty(item.get("acceptance_criteria")):
            errors.append(f"已声明要求{req_id}缺少中文说明或验收标准。")
        if not isinstance(item.get("critical"), bool):
            errors.append(f"已声明要求{req_id}必须明确critical，中文意思是是否关键。")
    ledger_map: dict[str, dict[str, Any]] = {}
    evidence_ids: set[str] = set()
    for index, item in enumerate(ledger):
        label = f"completion-ledger.json第{index + 1}项"
        if not isinstance(item, dict):
            errors.append(f"{label}必须是对象。")
            continue
        req_id = str(item.get("requirement_id", "")).strip()
        if req_id in ledger_map:
            errors.append(f"完成台账中的要求编号重复：{req_id}")
        ledger_map[req_id] = item
        if item.get("status") not in {"ACCEPTED", "WAIVED", "BLOCKED", "REJECTED"}:
            errors.append(f"完成台账{req_id}状态无效。")
        if not nonempty(item.get("evidence_ids")) or not nonempty(item.get("chinese_conclusion")):
            errors.append(f"完成台账{req_id}缺少证据编号或中文结论。")
        for evidence_id in item.get("evidence_ids") or []:
            evidence_ids.add(str(evidence_id))
    for req_id in requirement_ids:
        if req_id not in ledger_map:
            errors.append(f"已声明要求{req_id}没有进入Completion Ledger（完成台账）。")
    if final_status == "PASS":
        incomplete = [req_id for req_id in requirement_ids if ledger_map.get(req_id, {}).get("status") != "ACCEPTED"]
        if incomplete:
            errors.append(f"最终通过但这些已声明要求未被接受：{', '.join(incomplete)}。")
    return requirement_ids, evidence_ids


def validate_ledger_auditors(
    ledger: list[Any], agent_ids: set[str], role_by_agent: dict[str, str], errors: list[str]
) -> None:
    for index, item in enumerate(ledger):
        if not isinstance(item, dict):
            continue
        if item.get("status") != "ACCEPTED":
            continue
        auditor = str(item.get("accepted_by_agent_id", "")).strip()
        if auditor not in agent_ids or role_by_agent.get(auditor) != "audit":
            errors.append(
                f"completion-ledger.json第{index + 1}项声称已接受，但accepted_by_agent_id不是已登记的独立审计角色。"
            )


def validate_sources(
    sources: list[Any],
    config: dict[str, Any],
    indexed_evidence_ids: set[str],
    errors: list[str],
) -> tuple[dict[str, dict[str, Any]], set[str]]:
    source_map: dict[str, dict[str, Any]] = {}
    referenced_evidence_ids: set[str] = set()
    if not sources:
        errors.append("source-confidence-register.json至少需要一条来源或关键假设。")
    for index, item in enumerate(sources):
        label = f"source-confidence-register.json第{index + 1}项"
        if not isinstance(item, dict):
            errors.append(f"{label}必须是对象。")
            continue
        for field, chinese in (("source_id", "来源编号"), ("claim", "关键断言"), ("project_affiliation", "项目归属")):
            if not nonempty(item.get(field)):
                errors.append(f"{label}缺少{field}，中文意思是{chinese}。")
        source_id = str(item.get("source_id", "")).strip()
        if not source_id or source_id in source_map:
            errors.append(f"{label}的source_id缺失或重复。")
        else:
            source_map[source_id] = item
        if item.get("project_affiliation") != config.get("project_affiliation"):
            errors.append(f"{label}的项目归属与当前任务不一致。")
        confidence = item.get("confidence")
        if confidence not in {"VERIFIED", "ESTIMATE", "SPECULATION"}:
            errors.append(f"{label}置信度必须是VERIFIED（已核实）、ESTIMATE（估计值）或SPECULATION（推测）。")
        source_evidence_ids = {str(value).strip() for value in item.get("evidence_ids") or []}
        if confidence == "VERIFIED" and not source_evidence_ids:
            errors.append(f"{label}声称已核实但没有证据编号。")
        unknown_source_evidence = sorted(source_evidence_ids - indexed_evidence_ids)
        if unknown_source_evidence:
            errors.append(f"{label}引用未进入证据索引的来源证据：{', '.join(unknown_source_evidence)}。")
        referenced_evidence_ids.update(source_evidence_ids)
        if confidence == "ESTIMATE" and item.get("used_in_final") is True:
            if item.get("explicitly_labeled") is not True or item.get("downstream_use_approved") is not True:
                errors.append(f"{label}的估计值进入最终产物，但没有显式标注或下游批准。")
            if not nonempty(item.get("uncertainty")):
                errors.append(f"{label}的估计值缺少不确定性说明。")
        if confidence == "SPECULATION" and item.get("used_in_final") is True:
            errors.append(f"{label}是推测，不能进入正式最终结论。")
    return source_map, referenced_evidence_ids


def validate_tools(tools: list[Any], config: dict[str, Any], errors: list[str]) -> None:
    if not tools and not nonempty(config.get("tool_inventory_not_applicable_reason")):
        errors.append("tool-inventory.json为空时必须说明为什么工具清单不适用。")
    for index, item in enumerate(tools):
        label = f"tool-inventory.json第{index + 1}项"
        if not isinstance(item, dict):
            errors.append(f"{label}必须是对象。")
            continue
        for field, chinese in (
            ("tool_name", "工具名"),
            ("source", "来源"),
            ("stateful", "是否保存状态"),
            ("auth_required", "是否需要认证"),
            ("context_cost", "上下文成本"),
            ("secret_exposure_risk", "密钥暴露风险"),
            ("enabled_for_stage", "允许使用的阶段"),
            ("reason", "中文理由"),
        ):
            if field not in item or item.get(field) in (None, ""):
                errors.append(f"{label}缺少{field}，中文意思是{chinese}。")


def validate_agents(
    root: Path,
    agents: list[Any],
    config: dict[str, Any],
    evidence_files: dict[str, Path],
    allow_missing: bool,
    errors: list[str],
) -> tuple[set[str], dict[str, str], set[str]]:
    agent_ids: set[str] = set()
    role_by_agent: dict[str, str] = {}
    contexts: set[str] = set()
    workspaces: set[str] = set()
    start_receipts: set[str] = set()
    return_receipts: set[str] = set()
    roles: set[str] = set()
    receipt_evidence_ids: set[str] = set()
    platform_run_ids: set[str] = set()
    agent_records: dict[str, dict[str, Any]] = {}
    for index, agent in enumerate(agents):
        label = f"agents.json第{index + 1}项"
        if not isinstance(agent, dict):
            errors.append(f"{label}必须是对象。")
            continue
        agent_id = str(agent.get("agent_id", "")).strip()
        role = str(agent.get("role", "")).strip()
        if role not in {"control", "materials", "execution", "audit"}:
            errors.append(f"{label}的role只能是control控制、materials资料、execution工程执行或audit独立审计。")
        if not agent_id or agent_id in agent_ids:
            errors.append(f"{label}的agent_id缺失或重复。")
        agent_ids.add(agent_id)
        agent_records[agent_id] = agent
        role_by_agent[agent_id] = role
        roles.add(role)
        if role != "control" and not nonempty(agent.get("parent_agent_id")):
            errors.append(f"{label}缺少parent_agent_id，中文意思是父级智能体编号。")
        for field, chinese in (
            ("context_id", "独立上下文编号"),
            ("workspace", "独立工作空间"),
            ("runtime_start_receipt", "系统启动回执"),
            ("runtime_return_receipt", "系统回传回执"),
            ("runtime_receipt_source", "不可由智能体自填的运行系统证据来源"),
            ("runtime_receipt_evidence_id", "运行回执证据编号"),
            ("platform_run_id", "平台运行编号"),
            ("started_at", "真实开始时间"),
            ("returned_at", "真实回传时间"),
            ("responsibility", "有边界责任"),
            ("work_evidence", "实际工作证据"),
            ("measured_benefit", "时间或质量收益"),
            ("merge_cost", "合并成本"),
        ):
            if not nonempty(agent.get(field)):
                errors.append(f"{label}缺少{field}，中文意思是{chinese}。")
        if agent.get("runtime_receipt_source") not in {"system_trace", "runtime_api", "platform_event_log"}:
            errors.append(
                f"{label}的runtime_receipt_source必须来自系统追踪、运行接口或平台事件日志，不能是自述。"
            )
        if nonempty(agent.get("runtime_receipt_evidence_id")):
            receipt_evidence_id = str(agent.get("runtime_receipt_evidence_id")).strip()
            receipt_evidence_ids.add(receipt_evidence_id)
            event_file = evidence_files.get(receipt_evidence_id)
            if event_file:
                validate_platform_event(event_file, agent, label, errors)
            else:
                errors.append(f"{label}引用的平台运行回执没有有效证据文件。")
        platform_run_id = str(agent.get("platform_run_id", "")).strip()
        if platform_run_id:
            if platform_run_id.casefold() in platform_run_ids:
                errors.append(f"{label}的平台运行编号与其他智能体重复。")
            platform_run_ids.add(platform_run_id.casefold())
        for field, values, chinese in (
            ("context_id", contexts, "独立上下文编号"),
            ("workspace", workspaces, "独立工作空间"),
            ("runtime_start_receipt", start_receipts, "启动回执"),
            ("runtime_return_receipt", return_receipts, "回传回执"),
        ):
            value = agent.get(field)
            if nonempty(value):
                if field == "workspace":
                    normalized = normalized_windows_path(value)
                else:
                    normalized = str(value).strip().casefold()
                if normalized in values:
                    errors.append(f"{label}的{chinese}与其他智能体重复，不能证明独立运行。")
                values.add(normalized)
        started = parse_time(agent.get("started_at"))
        returned = parse_time(agent.get("returned_at"))
        if not started or not returned or returned < started:
            errors.append(f"{label}的开始和回传时间无效或顺序错误。")
    if not allow_missing:
        required_roles = config.get("required_roles") or ["control", "materials", "execution", "audit"]
        missing = [role for role in required_roles if role not in roles]
        if missing:
            errors.append(f"缺少必需真实角色：{', '.join(missing)}。默认应有控制、资料、执行、审计。")
        if len(agent_ids) < 4:
            errors.append("正式长任务默认需要控制、资料、工程执行、独立审计四个真实上下文。")
    control_ids = [agent_id for agent_id, role in role_by_agent.items() if role == "control"]
    if agents and len(control_ids) != 1:
        errors.append("每次运行必须恰好有一个控制角色作为根主控。")
    for agent_id, agent in agent_records.items():
        parent_id = str(agent.get("parent_agent_id", "")).strip()
        if role_by_agent.get(agent_id) == "control":
            if parent_id or str(agent.get("parent_platform_run_id", "")).strip():
                errors.append(f"根控制智能体{agent_id}不应再声明父级。")
            continue
        parent = agent_records.get(parent_id)
        if not parent:
            errors.append(f"智能体{agent_id}引用的父级{parent_id}不存在。")
            continue
        expected_parent_run = str(parent.get("platform_run_id", "")).strip()
        if str(agent.get("parent_platform_run_id", "")).strip() != expected_parent_run:
            errors.append(f"智能体{agent_id}的平台父运行编号与父智能体不一致。")
    return agent_ids, role_by_agent, receipt_evidence_ids


def validate_platform_event(
    event_file: Path, agent: dict[str, Any], label: str, errors: list[str]
) -> None:
    try:
        event = json.loads(event_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label}的平台事件文件无法解析：{exc}")
        return
    if not isinstance(event, dict):
        errors.append(f"{label}的平台事件文件必须是对象。")
        return
    pairs = (
        ("event_source", "runtime_receipt_source"),
        ("agent_id", "agent_id"),
        ("context_id", "context_id"),
        ("parent_agent_id", "parent_agent_id"),
        ("start_event_id", "runtime_start_receipt"),
        ("return_event_id", "runtime_return_receipt"),
        ("started_at", "started_at"),
        ("returned_at", "returned_at"),
        ("platform_run_id", "platform_run_id"),
        ("parent_platform_run_id", "parent_platform_run_id"),
    )
    for event_key, agent_key in pairs:
        if str(event.get(event_key, "")).strip() != str(agent.get(agent_key, "")).strip():
            errors.append(f"{label}的平台事件字段{event_key}与agents.json中的{agent_key}不一致。")
    if event.get("exported_by_platform") is not True:
        errors.append(f"{label}的平台事件没有exported_by_platform=true导出标记。")
    if event.get("event_status") != "RETURNED":
        errors.append(f"{label}的平台事件状态必须是RETURNED（已经回传）。")


def validate_packages(
    packages: list[Any],
    requirement_ids: set[str],
    agent_ids: set[str],
    role_by_agent: dict[str, str],
    evidence_files: dict[str, Path],
    final_status: Any,
    allow_empty: bool,
    errors: list[str],
) -> tuple[set[str], set[str], dict[str, dict[str, Any]], set[str]]:
    package_ids: set[str] = set()
    executors: set[str] = set()
    package_map: dict[str, dict[str, Any]] = {}
    skill_evidence_ids: set[str] = set()
    covered_requirements: set[str] = set()
    if not packages and not allow_empty:
        errors.append("正式运行至少需要一个真实工作包，空工作包不能通过。")
    for index, package in enumerate(packages):
        label = f"work-packages.json第{index + 1}项"
        if not isinstance(package, dict):
            errors.append(f"{label}必须是对象。")
            continue
        package_id = str(package.get("work_package_id", "")).strip()
        if not package_id or package_id in package_ids:
            errors.append(f"{label}的工作包编号缺失或重复。")
        package_ids.add(package_id)
        package_map[package_id] = package
        executor = str(package.get("executor_agent_id", ""))
        auditor = str(package.get("auditor_agent_id", ""))
        executors.add(executor)
        if executor not in agent_ids or role_by_agent.get(executor) != "execution":
            errors.append(f"工作包{package_id}的执行者必须是已登记的execution（执行）角色。")
        if auditor not in agent_ids or role_by_agent.get(auditor) != "audit":
            errors.append(f"工作包{package_id}的审计者必须是已登记的audit（审计）角色。")
        if executor == auditor:
            errors.append(f"工作包{package_id}的执行和审计不能是同一智能体。")
        for field, chinese in (
            ("declared_requirement_ids", "对应已声明要求"),
            ("required_skills", "必需技能"),
            ("acceptance_criteria", "关键验收标准"),
            ("verification_evidence", "确定性检查证据"),
            ("rollback", "回滚方式"),
            ("stop_condition", "停止条件"),
        ):
            if not nonempty(package.get(field)):
                errors.append(f"工作包{package_id}缺少{field}，中文意思是{chinese}。")
        package_requirement_ids = {str(item).strip() for item in package.get("declared_requirement_ids") or []}
        covered_requirements.update(package_requirement_ids)
        unknown_requirements = sorted(package_requirement_ids - requirement_ids)
        if unknown_requirements:
            errors.append(f"工作包{package_id}引用不存在的已声明要求：{', '.join(unknown_requirements)}。")
        evidence = package.get("skill_use_evidence") or []
        used: set[str] = set()
        for evidence_item in evidence:
            if not isinstance(evidence_item, dict):
                errors.append(f"工作包{package_id}的skill_use_evidence必须是对象数组。")
                continue
            evidence_id = str(evidence_item.get("evidence_id", "")).strip()
            if not evidence_id:
                errors.append(f"工作包{package_id}的技能使用记录缺少evidence_id证据编号。")
            else:
                skill_evidence_ids.add(evidence_id)
            if (
                evidence_item.get("used") is True
                and nonempty(evidence_item.get("evidence"))
                and evidence_id
            ):
                used.add(str(evidence_item.get("skill", "")).strip())
                validate_skill_event(
                    evidence_files.get(evidence_id),
                    evidence_item,
                    package_id,
                    executor,
                    errors,
                )
        missing_skills = [skill for skill in package.get("required_skills") or [] if skill not in used]
        if missing_skills:
            errors.append(f"工作包{package_id}缺少必需技能实际使用证据：{', '.join(missing_skills)}。")
        if package.get("status") == "PASS" and package.get("audit_accepted") is not True:
            errors.append(f"工作包{package_id}声称通过，但没有独立审计接受。")
    if final_status == "PASS":
        uncovered = sorted(requirement_ids - covered_requirements)
        if uncovered:
            errors.append(f"这些已声明要求没有进入任何工作包：{', '.join(uncovered)}。")
    return package_ids, executors, package_map, skill_evidence_ids


def validate_skill_event(
    event_file: Path | None,
    evidence_item: dict[str, Any],
    package_id: str,
    executor: str,
    errors: list[str],
) -> None:
    evidence_id = str(evidence_item.get("evidence_id", "")).strip()
    if not event_file:
        errors.append(f"技能证据{evidence_id}没有进入证据索引或文件校验失败。")
        return
    try:
        event = json.loads(event_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"技能证据{evidence_id}无法解析：{exc}")
        return
    if not isinstance(event, dict):
        errors.append(f"技能证据{evidence_id}必须是运行工具导出的对象。")
        return
    if event.get("source") not in {"tool_trace", "system_trace", "platform_event_log"}:
        errors.append(f"技能证据{evidence_id}缺少受支持的工具或运行追踪来源。")
    expected_pairs = (
        ("skill", str(evidence_item.get("skill", "")).strip()),
        ("work_package_id", package_id),
        ("agent_id", executor),
    )
    for field, expected in expected_pairs:
        if str(event.get(field, "")).strip() != expected:
            errors.append(f"技能证据{evidence_id}的{field}与工作包绑定不一致。")
    if event.get("exported_by_runtime") is not True:
        errors.append(f"技能证据{evidence_id}没有exported_by_runtime=true运行导出标记。")
    for field in ("read_event_id", "use_event_id", "occurred_at"):
        if not nonempty(event.get(field)):
            errors.append(f"技能证据{evidence_id}缺少{field}运行字段。")
    if not parse_time(event.get("occurred_at")):
        errors.append(f"技能证据{evidence_id}的occurred_at不是有效时间。")


def validate_artifacts(
    root: Path,
    artifacts: list[Any],
    package_ids: set[str],
    package_map: dict[str, dict[str, Any]],
    agent_ids: set[str],
    role_by_agent: dict[str, str],
    final_status: Any,
    errors: list[str],
) -> tuple[set[str], dict[str, dict[str, Any]]]:
    artifact_ids: set[str] = set()
    artifact_map: dict[str, dict[str, Any]] = {}
    if final_status == "PASS" and not artifacts:
        errors.append("最终通过必须有artifact-manifest（产物清单）。")
    for index, item in enumerate(artifacts):
        label = f"artifact-manifest.json第{index + 1}项"
        if not isinstance(item, dict):
            errors.append(f"{label}必须是对象。")
            continue
        artifact_id = str(item.get("artifact_id", "")).strip()
        if not artifact_id or artifact_id in artifact_ids:
            errors.append(f"{label}的artifact_id缺失或重复。")
        artifact_ids.add(artifact_id)
        artifact_map[artifact_id] = item
        package_id = str(item.get("work_package_id", "")).strip()
        if package_id not in package_ids:
            errors.append(f"产物{artifact_id}引用不存在的工作包。")
        producer = str(item.get("produced_by_agent_id", "")).strip()
        if producer not in agent_ids or role_by_agent.get(producer) != "execution":
            errors.append(f"产物{artifact_id}的生产者没有真实智能体记录。")
        if package_map.get(package_id) and producer != str(package_map[package_id].get("executor_agent_id", "")).strip():
            errors.append(f"产物{artifact_id}的生产者与工作包执行者不一致。")
        for field, chinese in (
            ("path", "正式或影子产物路径"),
            ("evidence_copy_path", "证据目录内的产物副本"),
            ("sha256", "校验值"),
            ("kind", "产物类型"),
            ("disposition", "处置状态"),
        ):
            if not nonempty(item.get(field)):
                errors.append(f"产物{artifact_id}缺少{field}，中文意思是{chinese}。")
        evidence_copy = verified_relative_file(root, item.get("evidence_copy_path"))
        if not evidence_copy:
            errors.append(f"产物{artifact_id}的证据副本不存在、不是相对路径或越出证据目录。")
        elif str(item.get("sha256", "")).lower() != sha256_file(evidence_copy):
            errors.append(f"产物{artifact_id}的校验值与证据副本不一致。")
    return artifact_ids, artifact_map


def validate_claims(
    claims: list[Any],
    package_ids: set[str],
    package_map: dict[str, dict[str, Any]],
    requirement_ids: set[str],
    agent_ids: set[str],
    role_by_agent: dict[str, str],
    artifact_ids: set[str],
    artifact_map: dict[str, dict[str, Any]],
    source_map: dict[str, dict[str, Any]],
    skill_evidence_ids: set[str],
    final_status: Any,
    errors: list[str],
) -> tuple[set[str], set[str]]:
    claim_ids: set[str] = set()
    referenced_evidence_ids: set[str] = set()
    covered_requirements: set[str] = set()
    if final_status == "PASS" and not claims:
        errors.append("最终通过必须有execution-claims（执行声明）。")
    for index, item in enumerate(claims):
        label = f"execution-claims.json第{index + 1}项"
        if not isinstance(item, dict):
            errors.append(f"{label}必须是对象。")
            continue
        claim_id = str(item.get("claim_id", "")).strip()
        if not claim_id or claim_id in claim_ids:
            errors.append(f"{label}的claim_id缺失或重复。")
        claim_ids.add(claim_id)
        package_id = str(item.get("work_package_id", "")).strip()
        package = package_map.get(package_id, {})
        if package_id not in package_ids:
            errors.append(f"执行声明{claim_id}引用不存在的工作包。")
        executor = str(item.get("executor_agent_id", "")).strip()
        if executor not in agent_ids or role_by_agent.get(executor) != "execution":
            errors.append(f"执行声明{claim_id}的执行者没有真实记录。")
        if package and executor != str(package.get("executor_agent_id", "")).strip():
            errors.append(f"执行声明{claim_id}的执行者与工作包绑定不一致。")
        if not nonempty(item.get("statement_chinese")) or not nonempty(item.get("artifact_ids")):
            errors.append(f"执行声明{claim_id}缺少中文陈述或产物编号。")
        for artifact_id in item.get("artifact_ids") or []:
            if artifact_id not in artifact_ids:
                errors.append(f"执行声明{claim_id}引用不存在的产物：{artifact_id}")
            else:
                artifact = artifact_map.get(str(artifact_id), {})
                if artifact.get("work_package_id") != package_id or artifact.get("produced_by_agent_id") != executor:
                    errors.append(f"执行声明{claim_id}的产物{artifact_id}与工作包或执行者不一致。")
        claim_requirement_ids = {str(value).strip() for value in item.get("declared_requirement_ids") or []}
        covered_requirements.update(claim_requirement_ids)
        if not claim_requirement_ids:
            errors.append(f"执行声明{claim_id}没有绑定已声明要求。")
        unknown_requirements = sorted(claim_requirement_ids - requirement_ids)
        if unknown_requirements:
            errors.append(f"执行声明{claim_id}引用不存在的已声明要求：{', '.join(unknown_requirements)}。")
        package_requirements = {str(value).strip() for value in package.get("declared_requirement_ids") or []}
        if not claim_requirement_ids.issubset(package_requirements):
            errors.append(f"执行声明{claim_id}绑定的要求超出其工作包范围。")
        claim_skill_ids = {str(value).strip() for value in item.get("skill_evidence_ids") or []}
        if not claim_skill_ids:
            errors.append(f"执行声明{claim_id}缺少技能实际使用证据编号。")
        unknown_skill_ids = sorted(claim_skill_ids - skill_evidence_ids)
        if unknown_skill_ids:
            errors.append(f"执行声明{claim_id}引用不存在的技能证据：{', '.join(unknown_skill_ids)}。")
        referenced_evidence_ids.update(claim_skill_ids)
        source_ids = {str(value).strip() for value in item.get("source_ids") or []}
        if not source_ids:
            errors.append(f"执行声明{claim_id}缺少来源编号，不能审计推测是否进入最终产物。")
        for source_id in source_ids:
            source = source_map.get(source_id)
            if not source:
                errors.append(f"执行声明{claim_id}引用不存在的来源：{source_id}。")
            elif source.get("confidence") == "SPECULATION":
                errors.append(f"执行声明{claim_id}使用了推测来源{source_id}，不能进入正式最终结论。")
            elif source.get("confidence") == "ESTIMATE" and (
                source.get("explicitly_labeled") is not True
                or source.get("downstream_use_approved") is not True
            ):
                errors.append(f"执行声明{claim_id}使用的估计来源{source_id}没有标注或下游批准。")
    if final_status == "PASS":
        uncovered = sorted(requirement_ids - covered_requirements)
        if uncovered:
            errors.append(f"这些已声明要求没有进入任何执行声明：{', '.join(uncovered)}。")
    return claim_ids, referenced_evidence_ids


def validate_checks(
    checks: list[Any], package_ids: set[str], config: dict[str, Any], final_status: Any, errors: list[str]
) -> set[str]:
    evidence_ids: set[str] = set()
    check_ids: set[str] = set()
    types_by_package: dict[str, set[str]] = defaultdict(set)
    if final_status == "PASS" and not checks:
        errors.append("最终通过必须有script-verification-result（脚本验证结果）。")
    for index, item in enumerate(checks):
        label = f"deterministic-checks.json第{index + 1}项"
        if not isinstance(item, dict):
            errors.append(f"{label}必须是对象。")
            continue
        package_id = str(item.get("work_package_id", "")).strip()
        if package_id not in package_ids:
            errors.append(f"{label}引用不存在的工作包。")
        check_type = item.get("check_type")
        if check_type not in {"SUCCESS", "NEGATIVE", "STRUCTURE", "SAFETY"}:
            errors.append(f"{label}的check_type无效。")
        types_by_package[package_id].add(str(check_type))
        for field, chinese in (
            ("check_id", "检查编号"),
            ("command_or_method", "命令或方法"),
            ("expected", "预期结果"),
            ("observed", "观察结果"),
            ("result", "检查结果"),
            ("evidence_id", "证据编号"),
        ):
            if not nonempty(item.get(field)):
                errors.append(f"{label}缺少{field}，中文意思是{chinese}。")
        check_id = str(item.get("check_id", "")).strip()
        if check_id:
            if check_id in check_ids:
                errors.append(f"{label}的check_id重复：{check_id}。")
            check_ids.add(check_id)
        evidence_ids.add(str(item.get("evidence_id", "")))
        if final_status == "PASS" and item.get("result") != "PASS":
            errors.append(f"最终通过但检查{item.get('check_id')}没有通过。")
    if final_status == "PASS":
        for package_id in package_ids:
            if "SUCCESS" not in types_by_package.get(package_id, set()):
                errors.append(f"工作包{package_id}缺少成功信号检查。")
            if config.get("negative_case_required", True) is True and "NEGATIVE" not in types_by_package.get(package_id, set()):
                errors.append(f"工作包{package_id}缺少错误案例检查。")
    return evidence_ids


def validate_package_check_bindings(
    packages: list[Any], checks: list[Any], errors: list[str]
) -> None:
    check_to_package = {
        str(item.get("check_id", "")).strip(): str(item.get("work_package_id", "")).strip()
        for item in checks
        if isinstance(item, dict)
    }
    for package in packages:
        if not isinstance(package, dict):
            continue
        package_id = str(package.get("work_package_id", "")).strip()
        for check_id in package.get("verification_evidence") or []:
            check_id = str(check_id).strip()
            if check_to_package.get(check_id) != package_id:
                errors.append(f"工作包{package_id}引用的检查{check_id}不存在或属于其他工作包。")


def validate_matrix(
    matrix: list[Any],
    claims: list[Any],
    claim_ids: set[str],
    role_by_agent: dict[str, str],
    final_status: Any,
    errors: list[str],
) -> set[str]:
    decisions: dict[str, dict[str, Any]] = {}
    evidence_ids: set[str] = set()
    executor_by_claim = {
        str(item.get("claim_id")): str(item.get("executor_agent_id")) for item in claims if isinstance(item, dict)
    }
    for index, item in enumerate(matrix):
        label = f"claim-acceptance-matrix.json第{index + 1}项"
        if not isinstance(item, dict):
            errors.append(f"{label}必须是对象。")
            continue
        claim_id = str(item.get("claim_id", "")).strip()
        if claim_id not in claim_ids or claim_id in decisions:
            errors.append(f"{label}的声明编号不存在或重复。")
        decisions[claim_id] = item
        auditor = str(item.get("auditor_agent_id", ""))
        if role_by_agent.get(auditor) != "audit" or auditor == executor_by_claim.get(claim_id):
            errors.append(f"声明{claim_id}必须由不同于执行者的真实审计角色验收。")
        if item.get("decision") not in {"ACCEPT", "REJECT"}:
            errors.append(f"声明{claim_id}的决定必须是ACCEPT（接受）或REJECT（拒绝）。")
        if not nonempty(item.get("reason_chinese")) or not nonempty(item.get("evidence_ids")):
            errors.append(f"声明{claim_id}缺少中文理由或独立证据。")
        if item.get("fact_recheck_complete") is not True or item.get("delivery_recheck_complete") is not True:
            errors.append(f"声明{claim_id}没有完成独立事实复核和交付前复检。")
        for evidence_id in item.get("evidence_ids") or []:
            evidence_ids.add(str(evidence_id))
    for claim_id in claim_ids:
        if claim_id not in decisions:
            errors.append(f"执行声明{claim_id}没有进入claim-acceptance-matrix（声明验收矩阵）。")
    if final_status == "PASS":
        rejected = [claim_id for claim_id, item in decisions.items() if item.get("decision") != "ACCEPT"]
        if rejected:
            errors.append(f"最终通过但这些声明未被接受：{', '.join(rejected)}。")
    return evidence_ids


def validate_rounds(
    rounds: list[Any],
    packages: list[Any],
    package_ids: set[str],
    checks: list[Any],
    indexed_evidence_ids: set[str],
    config: dict[str, Any],
    errors: list[str],
) -> None:
    by_package: dict[str, list[dict[str, Any]]] = defaultdict(list)
    package_map = {
        str(item.get("work_package_id")): item for item in packages if isinstance(item, dict)
    }
    check_to_package = {
        str(item.get("check_id", "")).strip(): str(item.get("work_package_id", "")).strip()
        for item in checks
        if isinstance(item, dict)
    }
    max_repairs = safe_int(config.get("max_repair_rounds", 3), "max_repair_rounds返修上限", errors, 3)
    if max_repairs < 0:
        errors.append("max_repair_rounds返修上限不能小于0。")
        max_repairs = 0
    for index, item in enumerate(rounds):
        label = f"rounds.json第{index + 1}项"
        if not isinstance(item, dict):
            errors.append(f"{label}必须是对象。")
            continue
        package_id = str(item.get("work_package_id", "")).strip()
        if package_id not in package_ids:
            errors.append(f"{label}引用不存在的工作包。")
        by_package[package_id].append(item)
        round_no = item.get("round")
        if not isinstance(round_no, int) or round_no < 0:
            errors.append(f"{label}的round必须是非负整数。")
        elif round_no > max_repairs:
            errors.append(f"工作包{package_id}超过最大返修轮次{max_repairs}。")
        expected_package = package_map.get(package_id, {})
        if item.get("executor_agent_id") != expected_package.get("executor_agent_id"):
            errors.append(f"{label}的执行者与工作包绑定不一致。")
        if item.get("auditor_agent_id") != expected_package.get("auditor_agent_id"):
            errors.append(f"{label}的审计者与工作包绑定不一致。")
        if not nonempty(item.get("meaningful_delta")) or not nonempty(item.get("decision")):
            errors.append(f"{label}缺少真实变化或本轮决定。")
        if item.get("decision") not in {"ACCEPT", "REJECT", "CONTINUE", "BLOCKED"}:
            errors.append(f"{label}的decision只能是接受、拒绝、继续返修或阻塞。")
        if not nonempty(item.get("checks_rerun")) or not nonempty(item.get("audit_rerun")):
            errors.append(f"{label}缺少重新检查或独立复审证据。")
        for check_id in item.get("checks_rerun") or []:
            check_id = str(check_id).strip()
            if check_to_package.get(check_id) != package_id:
                errors.append(f"{label}引用的重跑检查{check_id}不存在或属于其他工作包。")
        audit_evidence_id = str(item.get("audit_rerun", "")).strip()
        if audit_evidence_id and audit_evidence_id not in indexed_evidence_ids:
            errors.append(f"{label}的独立复审证据{audit_evidence_id}没有进入证据索引。")
    for package_id in package_ids:
        items = by_package.get(package_id, [])
        numbers = sorted(item.get("round") for item in items if isinstance(item.get("round"), int))
        if not numbers or numbers[0] != 0:
            errors.append(f"工作包{package_id}必须从第0轮第一版开始记录。")
            continue
        if numbers != list(range(0, max(numbers) + 1)):
            errors.append(f"工作包{package_id}的轮次不连续：{numbers}。")
        if len(numbers) != len(set(numbers)):
            errors.append(f"工作包{package_id}存在重复轮次。")
        for item in items:
            if isinstance(item.get("round"), int) and item.get("round") > 0 and item.get("strategy_changed") is not True:
                errors.append(f"工作包{package_id}在失败后的下一轮没有改变策略。")
        ordered = sorted(
            (item for item in items if isinstance(item.get("round"), int)),
            key=lambda item: item["round"],
        )
        if any(item.get("decision") == "ACCEPT" for item in ordered[:-1]):
            errors.append(f"工作包{package_id}在已经接受后仍追加返修轮次。")
        if ordered:
            package_status = package_map.get(package_id, {}).get("status")
            final_decision = ordered[-1].get("decision")
            if package_status == "PASS" and final_decision != "ACCEPT":
                errors.append(f"工作包{package_id}声称通过，但最后一轮没有被独立接受。")
            if package_status != "PASS" and final_decision == "ACCEPT":
                errors.append(f"工作包{package_id}最后一轮已接受，但工作包状态未同步为通过。")


def validate_checkpoints(
    checkpoints: list[Any],
    task_type: Any,
    package_ids: set[str],
    indexed_evidence_ids: set[str],
    errors: list[str],
) -> set[str]:
    if not checkpoints:
        errors.append("至少需要一个有真实动作证据的检查点。")
    previous_time: datetime | None = None
    checkpoint_ids: set[str] = set()
    referenced_evidence_ids: set[str] = set()
    for index, item in enumerate(checkpoints):
        label = f"checkpoints.json第{index + 1}项"
        if not isinstance(item, dict):
            errors.append(f"{label}必须是对象。")
            continue
        timestamp = parse_time(item.get("timestamp"))
        if not timestamp:
            errors.append(f"{label}缺少有效timestamp，中文意思是真实时间。")
        elif previous_time and timestamp <= previous_time:
            errors.append(f"{label}时间没有晚于上一检查点，不能复制、补造或重排时间。")
        else:
            previous_time = timestamp
        for field, chinese in (
            ("checkpoint_id", "检查点编号"),
            ("layer_number", "当前层"),
            ("work_package_ids", "工作包编号"),
            ("meaningful_progress", "真实进展"),
            ("evidence_ids", "证据编号"),
        ):
            if not nonempty(item.get(field)):
                errors.append(f"{label}缺少{field}，中文意思是{chinese}。")
        checkpoint_id = str(item.get("checkpoint_id", "")).strip()
        if checkpoint_id:
            if checkpoint_id in checkpoint_ids:
                errors.append(f"{label}的checkpoint_id重复：{checkpoint_id}。")
            checkpoint_ids.add(checkpoint_id)
        layer_number = item.get("layer_number")
        if not isinstance(layer_number, int) or layer_number not in range(1, 13):
            errors.append(f"{label}的layer_number必须是1到12。")
        unknown_packages = sorted(
            {str(value).strip() for value in item.get("work_package_ids") or []} - package_ids
        )
        if unknown_packages:
            errors.append(f"{label}引用不存在的工作包：{', '.join(unknown_packages)}。")
        for evidence_id in item.get("evidence_ids") or []:
            evidence_id = str(evidence_id).strip()
            referenced_evidence_ids.add(evidence_id)
            if evidence_id not in indexed_evidence_ids:
                errors.append(f"{label}引用未进入证据索引的证据编号：{evidence_id}。")
        if not any(nonempty(item.get(field)) for field in ("artifact_delta", "command_or_test", "audit_decision")):
            errors.append(f"{label}必须至少包含产物差异、命令／测试或审计决定之一。")
        if task_type == "endurance" and item.get("scheduled_for") and not nonempty(item.get("late_reason")):
            scheduled = parse_time(item.get("scheduled_for"))
            if scheduled and timestamp and timestamp > scheduled:
                errors.append(f"{label}是晚检查点但没有记录真实原因。")
    return referenced_evidence_ids


def validate_delivery(
    delivery: dict[str, Any],
    role_by_agent: dict[str, str],
    final_status: Any,
    allow_unfinished: bool,
    errors: list[str],
) -> None:
    if allow_unfinished and delivery.get("accepted") is not True:
        if not nonempty(delivery.get("unavailable_reason")):
            errors.append("准备任务因无真实多智能体而阻塞时，交付复检必须记录未执行原因。")
        return
    auditor = str(delivery.get("auditor_agent_id", ""))
    if role_by_agent.get(auditor) != "audit":
        errors.append("delivery-safety-check必须由真实审计角色执行。")
    for field, chinese in (
        ("metadata_checked", "元数据"),
        ("secrets_checked", "密钥"),
        ("internal_paths_checked", "内部路径"),
        ("temporary_materials_checked", "临时材料"),
        ("attachments_checked", "附件"),
        ("references_checked", "引用"),
    ):
        if delivery.get(field) is not True:
            errors.append(f"交付前复检未确认：{chinese}。")
    if final_status == "PASS" and delivery.get("accepted") is not True:
        errors.append("最终通过但交付安全复检没有接受。")


def validate_handoff(handoff: dict[str, Any], final_status: Any, errors: list[str]) -> None:
    for field, chinese in (
        ("verified_facts", "已验证事实"),
        ("completed_items", "已完成项目"),
        ("skipped_items", "跳过项目及理由"),
        ("open_rejections", "开放拒绝"),
        ("open_blockers", "开放阻塞"),
        ("recovery_entry", "恢复入口"),
        ("next_resume_path", "下一恢复路径"),
        ("remaining_risks", "剩余风险"),
        ("agent_receipts_summary", "智能体回执摘要"),
        ("skill_status", "技能状态"),
        ("round_status", "返修状态"),
        ("session_snapshot_summary", "会话快照摘要"),
        ("tool_inventory_summary", "工具清单摘要"),
        ("workspace_lifecycle_summary", "工作空间生命周期摘要"),
        ("file_alias_map", "文件别名对应表"),
    ):
        if field not in handoff:
            errors.append(f"handoff.json缺少{field}，中文意思是{chinese}。")
    if final_status == "PASS" and (nonempty(handoff.get("open_rejections")) or nonempty(handoff.get("open_blockers"))):
        errors.append("最终通过但交接包仍有开放拒绝或阻塞。")


def validate_evidence_index(
    root: Path, index: dict[str, Any], errors: list[str]
) -> tuple[set[str], dict[str, Path]]:
    items = index.get("items")
    if not isinstance(items, list) or not items:
        errors.append("evidence-index.json必须包含非空items证据数组。")
        return set(), {}
    ids: set[str] = set()
    files: dict[str, Path] = {}
    for position, item in enumerate(items):
        label = f"evidence-index.json的items第{position + 1}项"
        if not isinstance(item, dict):
            errors.append(f"{label}必须是对象。")
            continue
        evidence_id = str(item.get("evidence_id", "")).strip()
        if not evidence_id or evidence_id in ids:
            errors.append(f"{label}的evidence_id缺失或重复。")
        ids.add(evidence_id)
        if not nonempty(item.get("kind")) or not nonempty(item.get("path")) or not nonempty(item.get("sha256")):
            errors.append(f"证据{evidence_id}缺少类型、路径或校验值。")
            continue
        evidence_file = verified_relative_file(root, item.get("path"))
        if not evidence_file:
            errors.append(f"证据{evidence_id}的文件不存在、不是相对路径或越出证据目录。")
        elif str(item.get("sha256", "")).lower() != sha256_file(evidence_file):
            errors.append(f"证据{evidence_id}的校验值与文件内容不一致。")
        else:
            files[evidence_id] = evidence_file
    return ids, files


def validate_aliases(index: dict[str, Any], errors: list[str]) -> None:
    aliases = index.get("aliases")
    if not isinstance(aliases, dict):
        errors.append("evidence-index.json缺少aliases，中文意思是旧产物名与当前文件的对应表。")
        return
    for alias, target in ALIAS_KEYS.items():
        if aliases.get(alias) != target:
            errors.append(f"证据别名{alias}必须映射到{target}。")


def validate_time(
    config: dict[str, Any],
    acceptance: dict[str, Any],
    checkpoints: list[Any],
    agents: list[Any],
    requirements: list[Any],
    packages: list[Any],
    artifacts: list[Any],
    checks: list[Any],
    role_by_agent: dict[str, str],
    indexed_evidence_ids: set[str],
    errors: list[str],
) -> None:
    task_type = config.get("task_type")
    elapsed = safe_float(acceptance.get("elapsed_minutes", 0), "elapsed_minutes实际用时", errors)
    if task_type in {"production", "optimization"}:
        if acceptance.get("final_status") == "PASS" and elapsed <= 0:
            errors.append("真实生产任务通过时elapsed_minutes必须是正数。")
        if safe_float(config.get("minimum_runtime_minutes", 0), "minimum_runtime_minutes最低时长", errors) > 0:
            errors.append("真实生产任务不能设置必须耗满的最低时长。")
        budget = safe_float(config.get("time_budget_minutes", 0), "time_budget_minutes时间预算", errors)
        expected_lower = safe_float(
            config.get("expected_duration_lower_minutes", 0),
            "expected_duration_lower_minutes同类任务预计下界",
            errors,
        )
        if "early_completion_threshold_ratio" in config:
            errors.append("当前运行包禁止使用固定异常早完比例；旧字段只能作为历史文本，不能参与验收。")
        assessment = acceptance.get("early_completion_assessment")
        assessment_auditor = ""
        reliable_history = False
        if not isinstance(assessment, dict):
            errors.append("生产和开放式优化任务必须有独立早完异常判断。")
            assessment = {}
        assessment_auditor = str(assessment.get("auditor_agent_id", ""))
        if role_by_agent.get(assessment_auditor) != "audit" or not nonempty(assessment.get("basis_chinese")):
            errors.append("早完异常判断必须由真实独立审计智能体给出中文依据。")
        reliable_history = assessment.get("reliable_history_available") is True
        if safe_float(assessment.get("expected_duration_lower_minutes", 0), "早完判断预计下界", errors) != expected_lower:
            errors.append("早完异常判断中的预计下界必须与运行配置完全一致。")
        if reliable_history:
            if expected_lower <= 0 or not nonempty(assessment.get("history_basis_evidence_ids")):
                errors.append("声称有可靠历史范围时，必须提供正数下界和历史依据证据。")
            for evidence_id in assessment.get("history_basis_evidence_ids") or []:
                if str(evidence_id) not in indexed_evidence_ids:
                    errors.append("早完异常判断引用了未进入证据索引的历史依据。")
        elif expected_lower != 0:
            errors.append("没有可靠历史范围时，预计下界必须为0并执行首次运行保守复核。")
        for field, actual in (
            ("goal_count", len(requirements)),
            ("work_package_count", len(packages)),
            ("artifact_count", len(artifacts)),
            ("check_count", len(checks)),
        ):
            if assessment.get(field) != actual:
                errors.append(f"早完异常判断的{field}与严格证据记录不一致。")
        early_review_needed = (not reliable_history) or (expected_lower > 0 and elapsed < expected_lower)
        if early_review_needed and assessment.get("is_anomalously_early") is not True:
            errors.append("首次运行或低于可靠历史下界时必须标记异常并执行专项复核。")
        if early_review_needed:
            validate_early_review(acceptance, role_by_agent, errors)
            review = acceptance.get("early_completion_review") or {}
            if str(review.get("auditor_agent_id", "")) != assessment_auditor:
                errors.append("异常早完专项复核必须由早完判断中的同一独立审计智能体执行。")
        platform_review = acceptance.get("platform_receipts_recheck")
        if not isinstance(platform_review, dict) or platform_review.get("accepted") is not True or role_by_agent.get(str(platform_review.get("auditor_agent_id", ""))) != "audit" or not nonempty(platform_review.get("method_chinese")) or not nonempty(platform_review.get("evidence_ids")):
            errors.append("正式通过前必须由独立审计者保存平台侧回执复核。")
        else:
            for evidence_id in platform_review.get("evidence_ids") or []:
                if str(evidence_id) not in indexed_evidence_ids:
                    errors.append("平台侧回执复核引用了未进入证据索引的事件。")
        if task_type == "optimization":
            contract = config.get("optimization_stop_contract") or {}
            expected_auditor = str(contract.get("independent_stop_auditor_id", ""))
            if role_by_agent.get(expected_auditor) != "audit":
                errors.append("优化停止合同的独立停止审计者必须是已登记的audit独立审计角色。")
            experiments = acceptance.get("optimization_experiments")
            experiment_evidence_ids: set[str] = set()
            if not isinstance(experiments, list) or not experiments:
                errors.append("严格开放式优化必须保存至少一轮实验或排除记录。")
            else:
                for item in experiments:
                    if not isinstance(item, dict) or not all(nonempty(item.get(field)) for field in ("candidate", "metric_before", "metric_after", "result_chinese", "matched_candidate", "evidence_ids")):
                        errors.append("严格开放式优化实验记录缺少候选、前后指标、停止条件映射或证据。")
                        continue
                    for evidence_id in item.get("evidence_ids") or []:
                        evidence_id = str(evidence_id)
                        experiment_evidence_ids.add(evidence_id)
                        if evidence_id not in indexed_evidence_ids:
                            errors.append("严格开放式优化实验引用了未进入证据索引的依据。")
            decision = acceptance.get("optimization_stop_decision")
            if not isinstance(decision, dict) or decision.get("accepted") is not True or str(decision.get("auditor_agent_id", "")) != expected_auditor or not nonempty(decision.get("matched_stop_condition")) or not nonempty(decision.get("experiment_evidence_ids")):
                errors.append("开放式优化缺少由预定独立审计者接受的最终停止决定和实验依据。")
            else:
                decision_ids = {str(x) for x in decision.get("experiment_evidence_ids") or []}
                for evidence_id in decision.get("experiment_evidence_ids") or []:
                    if str(evidence_id) not in indexed_evidence_ids:
                        errors.append("开放式优化停止决定引用了未进入证据索引的实验依据。")
                if experiment_evidence_ids != decision_ids:
                    errors.append("开放式优化停止决定必须完整引用且不得替换实验记录中的依据集合。")
        starts = [
            parse_time(item.get("started_at"))
            for item in agents
            if isinstance(item, dict) and parse_time(item.get("started_at"))
        ]
        returns = [
            parse_time(item.get("returned_at"))
            for item in agents
            if isinstance(item, dict) and parse_time(item.get("returned_at"))
        ]
        if starts and returns:
            envelope_start = min(starts)
            envelope_end = max(returns)
            wall_minutes = (envelope_end - envelope_start).total_seconds() / 60
            if abs(wall_minutes - elapsed) > 2:
                errors.append("生产任务声明耗时与真实智能体最早启动、最晚回传形成的时间范围不一致。")
            for index, checkpoint in enumerate(checkpoints):
                if not isinstance(checkpoint, dict):
                    continue
                timestamp = parse_time(checkpoint.get("timestamp"))
                if timestamp and not (envelope_start <= timestamp <= envelope_end):
                    errors.append(f"生产任务第{index + 1}个检查点不在真实智能体运行时间范围内。")
    elif task_type == "endurance":
        minimum = safe_float(config.get("minimum_runtime_minutes", 0), "minimum_runtime_minutes耐力最低时长", errors)
        interval = safe_float(config.get("checkpoint_interval_minutes", 0), "checkpoint_interval_minutes检查点间隔", errors)
        start = parse_time(acceptance.get("original_started_at"))
        end = parse_time(acceptance.get("ended_at"))
        if minimum <= 0 or interval <= 0:
            errors.append("耐力验证必须设置真实最低时间和检查点间隔。")
        if not start or not end or end < start:
            errors.append("耐力验证缺少有效原始开始时间、结束时间或时间顺序错误。")
        if elapsed < minimum:
            errors.append(f"耐力验证实际时间{elapsed}分钟，未达到最低{minimum}分钟。")
        if start and end:
            wall_minutes = (end - start).total_seconds() / 60
            if abs(wall_minutes - elapsed) > max(2, interval):
                errors.append("耐力验证声明耗时与原始起止时间不一致。")
        if interval > 0 and elapsed > 0:
            required_count = math.ceil(elapsed / interval) + 1
            if len(checkpoints) < required_count:
                errors.append(f"耐力验证检查点不足：实际{len(checkpoints)}，至少{required_count}。")
        checkpoint_times = sorted(
            timestamp
            for item in checkpoints
            if isinstance(item, dict)
            for timestamp in [parse_time(item.get("timestamp"))]
            if timestamp
        )
        if start and end and interval > 0 and checkpoint_times:
            if (checkpoint_times[0] - start).total_seconds() / 60 > interval:
                errors.append("耐力验证首个检查点距离原始开始时间超过一个检查间隔。")
            if (end - checkpoint_times[-1]).total_seconds() / 60 > interval:
                errors.append("耐力验证最后检查点没有覆盖结束前最后一个检查间隔。")
            if checkpoint_times[0] < start or checkpoint_times[-1] > end:
                errors.append("耐力验证检查点超出原始起止时间范围。")
            timed_items = sorted(
                [
                    (timestamp, item)
                    for item in checkpoints
                    if isinstance(item, dict)
                    for timestamp in [parse_time(item.get("timestamp"))]
                    if timestamp
                ],
                key=lambda pair: pair[0],
            )
            for (previous, _), (current, current_item) in zip(timed_items, timed_items[1:]):
                gap_minutes = (current - previous).total_seconds() / 60
                if gap_minutes > interval + 0.1 and not nonempty(current_item.get("late_reason")):
                    errors.append(
                        f"耐力验证相邻检查点间隔{gap_minutes:.1f}分钟，超过计划{interval:.1f}分钟且没有晚点原因。"
                    )
        if not any(isinstance(item, dict) and item.get("is_final") is True for item in checkpoints):
            errors.append("耐力验证缺少最终检查点。")
        if not nonempty(acceptance.get("runtime_driver_evidence")):
            errors.append("耐力验证缺少持续运行驱动和真实工作证据。")
        elif str(acceptance.get("runtime_driver_evidence")).strip() not in indexed_evidence_ids:
            errors.append("耐力验证的持续运行驱动证据没有进入证据索引。")
        if acceptance.get("interrupted") is True and not nonempty(acceptance.get("recovery_events")):
            errors.append("耐力验证发生中断但没有恢复事件证据。")
        if acceptance.get("final_status") == "PARTIAL_STARTED":
            errors.append("耐力任务不能以PARTIAL_STARTED（仅已部分启动）作为停止状态。")


def validate_early_review(
    acceptance: dict[str, Any], role_by_agent: dict[str, str], errors: list[str]
) -> None:
    review = acceptance.get("early_completion_review")
    if acceptance.get("early_completion_review_accepted") is not True:
        errors.append("异常提前完成已自动触发复核，但复核没有被独立接受。")
    if not isinstance(review, dict):
        errors.append("缺少early_completion_review，中文意思是提前完成逐项复核。")
        return
    if role_by_agent.get(str(review.get("auditor_agent_id", ""))) != "audit":
        errors.append("提前完成复核必须由真实独立审计智能体执行。")
    for field, chinese in (
        ("goal_coverage_complete", "原目标完整覆盖"),
        ("all_work_packages_handled", "全部工作包处理"),
        ("required_skills_used", "必需技能真实使用"),
        ("multi_agent_receipts_complete", "多智能体回执完整"),
        ("real_outputs_present", "真实产物存在"),
        ("deterministic_checks_run", "确定性检查运行"),
        ("negative_cases_run", "错误案例运行"),
        ("no_skipped_items", "没有跳过项目"),
        ("independent_audit", "审计独立"),
    ):
        if review.get(field) is not True:
            errors.append(f"提前完成复核未确认：{chinese}。")
    if review.get("decision") != "ACCEPT":
        errors.append("提前完成复核决定必须是ACCEPT，中文意思是接受提前完成。")


def validate_drives(
    config: dict[str, Any], agents: list[Any], artifacts: list[Any], errors: list[str]
) -> None:
    if str(config.get("authority_drive", "C")).upper() != "C":
        errors.append("authority_drive必须为C，中文意思是C盘是当前正式权威源。")
    if config.get("h_drive_mode", "history_only") != "history_only":
        errors.append("H盘只能作为历史资料。")
    k_mode = config.get("k_drive_mode", "disabled")
    if k_mode not in ("disabled", "user_approved_backup_only"):
        errors.append("K盘只能禁用或经用户批准后仅作备份。")
    if k_mode == "user_approved_backup_only" and not nonempty(config.get("k_drive_user_approval_evidence_id")):
        errors.append("K盘备份被启用但缺少进入证据索引的用户批准证据编号。")
    active_paths: list[tuple[str, Any]] = []
    for field in ("formal_workspace", "shadow_workspace", "evidence_workspace"):
        active_paths.append((field, config.get(field)))
    for agent in agents:
        if isinstance(agent, dict):
            active_paths.append((f"智能体{agent.get('agent_id')}工作空间", agent.get("workspace")))
    for artifact in artifacts:
        if isinstance(artifact, dict):
            active_paths.append((f"产物{artifact.get('artifact_id')}路径", artifact.get("path")))
    for label, path in active_paths:
        normalized = normalized_windows_path(path)
        if normalized.startswith("\\\\"):
            errors.append(f"{label}使用了网络共享或UNC路径；当前正式权威源必须是可核对的C盘路径。")
            continue
        drive = drive_letter(path)
        if drive != "C":
            shown = drive or "无法识别"
            errors.append(f"{label}的活动路径盘符为{shown}；正式、影子、证据、智能体和产物活动路径必须在C盘。")


def validate_final(
    acceptance: dict[str, Any],
    texts: dict[str, str],
    layers: list[Any],
    requirements: list[Any],
    ledger: list[Any],
    packages: list[Any],
    claims: list[Any],
    matrix: list[Any],
    agent_ids: set[str],
    role_by_agent: dict[str, str],
    executors: set[str],
    delivery: dict[str, Any],
    truthful_preparation_block: bool,
    errors: list[str],
) -> None:
    status_word = {
        "PASS": "通过",
        "PARTIAL": "部分完成",
        "BLOCKED": "阻塞",
        "REJECTED": "拒绝",
    }.get(acceptance.get("final_status"), "")
    for filename, content in texts.items():
        if len(content.strip()) < 120:
            errors.append(f"{filename}内容过短，不能只返回路径或一句结论。")
        if not chinese_is_primary(content):
            errors.append(
                f"{filename}必须以中文为主体；固定英文层名、状态码、命令和路径可以保留，但须有就近中文解释。"
            )
        for phrase in ("中文最终状态", "原目标", "证据"):
            if phrase not in content:
                errors.append(f"{filename}缺少“{phrase}”中文审计内容。")
        if status_word and status_word not in content:
            errors.append(f"{filename}没有用中文写出与结构化结果一致的最终状态“{status_word}”。")
    signer = str(acceptance.get("final_signer_agent_id", ""))
    if signer not in agent_ids and not truthful_preparation_block:
        errors.append("最终签署者没有真实智能体记录。")
    if signer in executors:
        errors.append("最终签署者不能是工作包执行者。")
    if signer and role_by_agent.get(signer) != "control":
        errors.append("最终签署者应为控制角色；独立审计负责接受声明，控制角色只汇总未被拒绝的事实。")
    if not nonempty(acceptance.get("status_code")) or not nonempty(acceptance.get("status_code_chinese")):
        errors.append("最终验收必须同时给出状态码和中文解释。")
    if not nonempty(acceptance.get("status_code_evidence_ids")):
        errors.append("最终状态码必须关联证据编号。")
    if acceptance.get("final_document_path") != "final-acceptance.md":
        errors.append("final_document_path必须指向final-acceptance.md。")
    if acceptance.get("final_report_path") != "final-report.md":
        errors.append("final_report_path必须指向final-report.md。")
    if acceptance.get("final_status") == "PASS":
        gates = (
            ("twelve_layers_complete", "十二层完整"),
            ("declared_requirements_complete", "已声明要求完整"),
            ("real_multi_agent_accepted", "真实多智能体"),
            ("skill_use_gates_accepted", "技能使用关口"),
            ("independent_audit_accepted", "独立审计"),
            ("delivery_safety_accepted", "交付安全"),
            ("handoff_accepted", "交接"),
        )
        for field, chinese in gates:
            if acceptance.get(field) is not True:
                errors.append(f"最终通过但{chinese}未接受。")
        if not packages or not claims or not matrix:
            errors.append("最终通过但工作包、执行声明或声明验收矩阵为空。")
        nonpassing = [
            str(item.get("work_package_id"))
            for item in packages
            if isinstance(item, dict) and (item.get("status") != "PASS" or item.get("audit_accepted") is not True)
        ]
        if nonpassing:
            errors.append(f"最终通过但这些工作包未通过：{', '.join(nonpassing)}。")
        open_rejections = safe_int(
            acceptance.get("open_rejections", 0), "open_rejections开放拒绝数量", errors
        )
        if open_rejections != 0 or nonempty(acceptance.get("open_blockers")):
            errors.append("最终通过但仍有开放拒绝或阻塞。")
        if delivery.get("accepted") is not True:
            errors.append("最终通过但交付前复检未接受。")


def result(errors: list[str], warnings: list[str]) -> dict[str, Any]:
    return {
        "pass": not errors,
        "中文状态": "确定性结构检查通过" if not errors else "确定性结构检查失败",
        "错误": errors,
        "警告": warnings,
        "说明": "本结果只检查可确定结构，不替代第9层独立审计和第12层最终验收。",
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("用法：python3 validate_run_evidence.py <证据目录>", file=sys.stderr)
        return 2
    output = validate(Path(sys.argv[1]).resolve())
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if output["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
