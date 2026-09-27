"""验收隔离与来源判定 v1.0.0：候选逻辑，非浏览器驱动或最终认证器。

证据是否已经核验，必须由读取原始操作记录的调用方提供；
本模块不能验证外部日志真实性，也不接受模型摘要作为操作来源证明。
"""
from typing import Mapping, Any

SOURCES = {"TOOL_TRACE", "ATTRIBUTABLE_ACTION_RECORD", "EXPLICIT_OPERATOR_STATEMENT"}


def classify_event(event: Mapping[str, Any]) -> str:
    if (event.get("verified") is not True
            or event.get("source_kind") not in SOURCES
            or not event.get("evidence_ref")):
        return "UNVERIFIED"
    actor = event.get("actor")
    if actor not in {"AUTOMATION", "HUMAN"}:
        return "UNVERIFIED"
    if event.get("disputed"):
        return "REVIEW_CONFLICT"
    if event.get("purpose") in {"DISPLAY_ONLY", "COMMENTARY_ONLY"}:
        return "NOT_INTERVENTION"
    if actor == "AUTOMATION":
        return "NOT_INTERVENTION"
    if event.get("within_loop") is False:
        if event.get("purpose") == "TASK_SUBMISSION" and event.get("permitted_entry") is True:
            return "NOT_INTERVENTION"
        return "OUTSIDE_MEASUREMENT_WINDOW"
    if (event.get("within_loop") is True
            and event.get("purpose") in {"TRANSFER", "RECOVERY", "EXECUTION", "REPAIR"}):
        return "CONFIRMED_HUMAN_INTERVENTION"
    return "UNVERIFIED"


def review_claim(reported_count: int, verified_events: list[Mapping[str, Any]]) -> str:
    if isinstance(reported_count, bool) or not isinstance(reported_count, int) or reported_count < 0:
        raise ValueError("reported_count 必须为非负整数；只是报告值，不能充当证据")
    # 同一个原始动作证据重复显示时不重复计数。
    distinct = {}
    for event in verified_events:
        ref = event.get("evidence_ref")
        if not ref:
            continue
        if ref in distinct and distinct[ref] != event:
            return "REVIEW_CONFLICT"
        distinct[ref] = event
    outcomes = [classify_event(e) for e in distinct.values()]
    if "REVIEW_CONFLICT" in outcomes:
        return "REVIEW_CONFLICT"
    count = outcomes.count("CONFIRMED_HUMAN_INTERVENTION")
    if count > 0:
        return "MANUAL_FAILURE_SUPPORTED" if reported_count == count else "REVIEW_COUNT_MISMATCH"
    if reported_count > 0:
        return "REVIEW_UNSUPPORTED_MANUAL_CLAIM"
    return "NO_CONFIRMED_EVENT_NOT_ZERO_CERTIFICATION"


def isolation_gate(*, control_context: str, test_context: str,
                   control_conversation: str, test_conversation: str,
                   control_title: str, test_title: str,
                   creation_verified: bool) -> str:
    values = (control_context, test_context, control_conversation, test_conversation,
              control_title, test_title)
    if not all(isinstance(v, str) and v.strip() for v in values):
        return "REVIEW_MISSING_IDENTITY"
    if control_context == test_context:
        return "REJECT_SHARED_BROWSER_CONTEXT"
    if control_conversation == test_conversation:
        return "REJECT_REUSED_CONVERSATION"
    if control_title == test_title:
        return "REJECT_AMBIGUOUS_TITLE"
    if creation_verified is not True:
        return "REVIEW_NEW_CONVERSATION_NOT_VERIFIED"
    return "ISOLATION_PASS_NOT_ACTOR_PROOF"


def wait_gate(*, matching_ack_verified: bool, progress_verified: bool,
              timeout: bool) -> str:
    if matching_ack_verified:
        return "DELIVERED_DO_NOT_RESEND"
    if progress_verified:
        return "IN_PROGRESS_DO_NOT_INTERRUPT"
    return "CHECK_STATE_DO_NOT_AUTO_FAIL_OR_RESEND" if timeout else "WAIT"
