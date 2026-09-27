"""验收入口来源复核 v1.0.1。仅核对证据绑定/分类，不采集日志、不伪造认证。

expected 来自冻结任务及已回读的会话绑定；evidence 来自独立读取原始记录的调用方。
布尔 verified 是调用方责任，不是本模块验证了远端事实。
"""
from collections.abc import Mapping
from acceptance_isolation_guard_v1 import classify_event, isolation_gate, wait_gate

IDENTITY = ("task_id", "timeline_id", "run_id", "conversation_id")
STAGES = frozenset(("TASK_SUBMISSION", "COMMAND_RECEIPT", "BUSINESS_EXECUTION", "RESULT_RETURN"))
PASS_GATES = ("business_verified", "delivery_verified", "scope_verified",
              "runtime_binding_verified", "closed_loop_verified", "timeline_verified")
REVIEW = "REVIEW_EVIDENCE_REQUIRED_NO_STATE_CHANGE"


def _bound(expected, evidence):
    if not isinstance(expected, Mapping) or not isinstance(evidence, Mapping):
        return False
    return all(isinstance(expected.get(k), str) and expected[k].strip()
               and evidence.get(k) == expected[k] for k in IDENTITY)


def review_acceptance(result, fail_source, *, expected=None, evidence=None):
    """返回 HOLD/FAIL/PASS 及原因。HOLD 不触发 FSM 转移或恢复重发。"""
    if not _bound(expected, evidence):
        return "HOLD", "REVIEW_TASK_BINDING_REQUIRED_NO_STATE_CHANGE"
    session = evidence.get("session")
    if not isinstance(session, Mapping):
        return "HOLD", "REVIEW_SESSION_BINDING_REQUIRED_NO_STATE_CHANGE"
    try:
        isolated = isolation_gate(**session)
    except (TypeError, ValueError):
        return "HOLD", "REVIEW_SESSION_SCHEMA_NO_STATE_CHANGE"
    if isolated != "ISOLATION_PASS_NOT_ACTOR_PROOF":
        return "HOLD", isolated
    if session["test_conversation"] != expected["conversation_id"]:
        return "HOLD", "REVIEW_CONVERSATION_BINDING_NO_STATE_CHANGE"
    if evidence.get("provenance_disputed") is not False:
        return "HOLD", "REVIEW_PROVENANCE_DISPUTE_OR_UNKNOWN"

    events = evidence.get("events")
    if not isinstance(events, list):
        return "HOLD", REVIEW
    distinct = {}
    for e in events:
        if not isinstance(e, Mapping) or not _bound(expected, e):
            return "HOLD", "REVIEW_EVENT_BINDING_NO_STATE_CHANGE"
        ref = e.get("evidence_ref")
        if not isinstance(ref, str) or not ref.strip():
            return "HOLD", REVIEW
        if ref in distinct and dict(distinct[ref]) != dict(e):
            return "HOLD", "REVIEW_CONFLICT_NO_STATE_CHANGE"
        distinct[ref] = e

    outcomes = [classify_event(e) for e in distinct.values()]
    if any(o in {"UNVERIFIED", "REVIEW_CONFLICT"} for o in outcomes):
        return "HOLD", REVIEW
    humans = outcomes.count("CONFIRMED_HUMAN_INTERVENTION")
    reported = evidence.get("reported_human_count")
    if reported is not None and (type(reported) is not int or reported < 0):
        return "HOLD", "REVIEW_INVALID_REPORTED_COUNT"
    if humans:
        return "FAIL", "MANUAL_HANDOFF"
    if reported not in (None, 0):
        return "HOLD", "REVIEW_UNSUPPORTED_MANUAL_CLAIM"

    if result == "PASS":
        # 不能用“没见到人工”替代完整自动链的正面证据。
        covered = {e.get("stage") for e in distinct.values()
                   if e.get("actor") == "AUTOMATION"
                   and e.get("source_kind") == "TOOL_TRACE"
                   and e.get("purpose") not in {"DISPLAY_ONLY", "COMMENTARY_ONLY"}}
        if not STAGES.issubset(covered):
            return "HOLD", "REVIEW_AUTOMATED_CHAIN_INCOMPLETE"
        if not all(evidence.get(k) is True for k in PASS_GATES):
            return "HOLD", "REVIEW_FULL_VALID_EVIDENCE_INCOMPLETE"
        return "PASS", "NONE"
    if fail_source == "MANUAL_HANDOFF":
        return "HOLD", "REVIEW_UNSUPPORTED_MANUAL_CLAIM"
    if evidence.get("failure_verified") is not True or not evidence.get("failure_evidence_ref"):
        return "HOLD", "REVIEW_FAILURE_NOT_VERIFIED"
    if evidence.get("failure_basis") in {None, "TIMEOUT_ONLY", "NO_OUTPUT_YET"}:
        return "HOLD", "CHECK_STATE_DO_NOT_AUTO_FAIL_OR_RESEND"
    return result, fail_source


def review_wait(*, expected=None, observation=None):
    """只接受本任务本会话的确认或进展；超时不直接触发失败/重发。"""
    if not _bound(expected, observation) or not observation.get("evidence_ref"):
        return "CHECK_STATE_DO_NOT_AUTO_FAIL_OR_RESEND"
    return wait_gate(matching_ack_verified=observation.get("matching_ack_verified") is True,
                     progress_verified=observation.get("progress_verified") is True,
                     timeout=observation.get("timeout") is True)
