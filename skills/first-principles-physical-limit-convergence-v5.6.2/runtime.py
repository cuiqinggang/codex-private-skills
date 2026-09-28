"""v5.6.2：冻结上下文绑定 + 实体证据校验 + 冻结起点机械计时。"""
from pathlib import Path
import hashlib
from display import render

TRANSITIONS = {
    10: {"PASS": (20, "虚：已冻结", "虚", "冻结"), "FAIL": (10, "虚：准备中", "虚", "留10"), "UNKNOWN": (10, "虚：准备中", "虚", "留10")},
    20: {"PASS": (30, "虚实交接中", "实", "发布现实交接"), "FAIL": (10, "虚：准备中", "虚", "回10"), "UNKNOWN": (10, "虚：准备中", "虚", "回10")},
    30: {"PASS": (40, "实：执行与审核中", "实", "立即执行同一冻结包"), "FAIL": (30, "虚实交接中", "实", "留30"), "UNKNOWN": (30, "虚实交接中", "实", "留30")},
    40: {"PASS": (100, "完成", "实", "冻结最终证据"), "FAIL": (10, "虚：准备中", "虚", "明确失败回10"), "UNKNOWN": (40, "实：执行与审核中", "实", "缺证据留40")},
    100: {"PASS": (100, "完成", "实", "STOP")},
}

def _missing(*values):
    return any(v is None or v == "" for v in values)

def _eq(evidence, context, keys):
    missing = False
    for key in keys:
        actual = evidence.get(key)
        expected = context.get(key)
        if _missing(actual, expected):
            missing = True
        elif actual != expected:
            return "FAIL"
    return "UNKNOWN" if missing else "PASS"

def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _artifact_proof(value):
    if not isinstance(value, dict):
        return "UNKNOWN"
    path = value.get("path")
    expected = value.get("sha256")
    if _missing(path, expected):
        return "UNKNOWN"
    try:
        p = Path(path)
        if not p.is_file():
            return "UNKNOWN"
        return "PASS" if _sha256_file(p) == str(expected).lower() else "UNKNOWN"
    except (OSError, ValueError, TypeError):
        return "UNKNOWN"

def judge(state, evidence, context, dispatch=None):
    if state == 100:
        return "PASS"

    if state == 10:
        vals = (evidence.get("goal"), evidence.get("valid_id"), evidence.get("task_accepted"))
        if any(v is False for v in vals):
            return "FAIL"
        if _missing(*vals):
            return "UNKNOWN"
        return "PASS"

    if state == 20:
        verdict = _eq(evidence, context, (
            "task", "seq", "package", "freeze_id", "freeze_hash",
            "time_anchor_id", "materials_hash",
        ))
        if verdict != "PASS":
            return verdict
        if not dispatch:
            return "UNKNOWN"
        if not ((dispatch.get("repo") and dispatch.get("commit") and dispatch.get("entry")) or dispatch.get("inline")):
            return "UNKNOWN"
        return "PASS"

    if state == 30:
        return _eq(evidence, context, (
            "task", "seq", "package", "freeze_id", "freeze_hash",
            "time_anchor_id", "materials_hash",
        ))

    if state == 40:
        identity = _eq(evidence, context, ("task", "seq", "package", "valid_id"))
        if identity != "PASS":
            return identity
        status = evidence.get("result_status")
        if status == "FAIL":
            return "FAIL"
        if status != "PASS":
            return "UNKNOWN"
        if _artifact_proof(evidence.get("raw_evidence")) != "PASS":
            return "UNKNOWN"
        if _artifact_proof(evidence.get("time_record")) != "PASS":
            return "UNKNOWN"
        return "PASS"

    raise ValueError(f"未知状态: {state}")

def _dispatch_command(header, dispatch):
    if dispatch.get("repo") and dispatch.get("commit") and dispatch.get("entry"):
        body = (
            f"从共同私库 {dispatch['repo']} 固定提交：\n{dispatch['commit']}\n\n"
            f"读取并严格执行：\n{dispatch['entry']}"
        )
    elif dispatch.get("inline"):
        body = dispatch["inline"]
    else:
        raise ValueError("缺少可发布交接")
    return header + "\n\n" + body

def _derived_time_anchor(context, supplied, code):
    if supplied.get("accepted") != context.get("accepted"):
        raise ValueError("TASK_ACCEPTED显示与冻结上下文不一致")
    if supplied.get("accepted_clock") != context.get("accepted_clock"):
        raise ValueError("TASK_ACCEPTED时钟身份与冻结上下文不一致")

    out = {
        "accepted": context.get("accepted"),
        "event": supplied.get("event"),
        "elapsed_ms": None,
        "t_valid_ms": None,
        "t_star_ms": supplied.get("t_star_ms"),
    }

    accepted_clock = context.get("accepted_clock")
    event_clock = supplied.get("event_clock")
    accepted_tick = context.get("accepted_tick_ns")
    event_tick = supplied.get("event_tick_ns")

    comparable = (
        accepted_clock not in (None, "", "unknown", "未知")
        and event_clock == accepted_clock
        and isinstance(accepted_tick, int) and accepted_tick >= 0
        and isinstance(event_tick, int) and event_tick >= accepted_tick
    )
    if comparable:
        elapsed = (event_tick - accepted_tick) / 1_000_000.0
        out["elapsed_ms"] = elapsed
        if code == 100:
            out["t_valid_ms"] = elapsed
    return out

def advance(state, evidence, context, *, page, task, seq, time_anchor, dispatch=None):
    if context.get("page") not in (None, page):
        raise ValueError("页面定位与冻结上下文不一致")
    if task != context.get("task") or seq != context.get("seq"):
        raise ValueError("任务/序号定位与冻结上下文不一致")
    verdict = judge(state, evidence, context, dispatch)
    code, name, phase, action = TRANSITIONS[state][verdict]
    derived = _derived_time_anchor(context, time_anchor, code)
    header = render(page, task, seq, phase, code, name, derived)
    result = {"verdict": verdict, "state": code, "action": action, "header": header}
    if state == 20 and verdict == "PASS":
        result["command"] = _dispatch_command(header, dispatch)
    return result
