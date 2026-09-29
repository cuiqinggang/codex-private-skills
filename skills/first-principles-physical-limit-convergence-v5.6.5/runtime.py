"""v5.6.5 R2：时间模型保持简化；仅机械化 Reality 最终权限边界与 T_VALID 独立区间。"""
from pathlib import Path
from datetime import datetime
import hashlib
from display import render

TRANSITIONS = {
    10: {"PASS": (20, "虚：已冻结", "虚", "冻结"), "FAIL": (10, "虚：准备中", "虚", "留10"), "UNKNOWN": (10, "虚：准备中", "虚", "留10")},
    20: {"PASS": (30, "虚实交接中", "实", "发布现实交接"), "FAIL": (10, "虚：准备中", "虚", "回10"), "UNKNOWN": (10, "虚：准备中", "虚", "回10")},
    30: {"PASS": (40, "实：执行与审核中", "实", "立即执行同一冻结包"), "FAIL": (30, "虚实交接中", "实", "留30"), "UNKNOWN": (30, "虚实交接中", "实", "留30")},
    40: {"PASS": (40, "实：执行与审核中", "实", "RETURN_TO_GPT"), "FAIL": (10, "虚：准备中", "虚", "明确失败回10"), "UNKNOWN": (40, "实：执行与审核中", "实", "缺证据留40")},
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


_FLOW_ORIGINS = {}


def _parse_real_time(name, value):
    if value is None or str(value).strip() == "":
        raise ValueError(f"{name}缺失")
    s = str(value)
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{name}不是现实可读时间") from exc
    if dt.tzinfo is None:
        raise ValueError(f"{name}缺少时区")
    return s, dt


def _now_text():
    return datetime.now().astimezone().isoformat(timespec="microseconds")


def _freeze_flow_origin_once(state, context, supplied):
    key = id(context)
    frozen = _FLOW_ORIGINS.get(key)
    if frozen and frozen[0] is context:
        return
    start_text = supplied.get("flow_start") or supplied.get("event") or _now_text()
    start_text, start_dt = _parse_real_time("本轮起点时间", start_text)
    start_state = supplied.get("flow_start_state", state)
    if type(start_state) is not int or start_state not in TRANSITIONS:
        raise ValueError("本轮起点状态非法")
    _FLOW_ORIGINS[key] = (context, start_state, start_text, start_dt)


def _flow_origin_for(context):
    frozen = _FLOW_ORIGINS.get(id(context))
    if frozen and frozen[0] is context:
        return frozen[1], frozen[2], frozen[3]
    return None


def _derived_time_anchor(context, supplied, code):
    origin = _flow_origin_for(context)
    if not origin:
        raise ValueError("本轮实际起点尚未建立")
    start_state, start_text, start_dt = origin

    state_text = supplied.get("event") or _now_text()
    state_text, state_dt = _parse_real_time("当前节点时间", state_text)
    elapsed_ms = None
    if state_dt >= start_dt:
        elapsed_ms = (state_dt - start_dt).total_seconds() * 1000.0

    if supplied.get("t_valid_ms") not in (None, ""):
        raise ValueError("禁止外部直接提交T_VALID数值；必须提供t_valid_start/t_valid_end独立边界")

    t_valid_ms = None
    if code == 100:
        valid_start = supplied.get("t_valid_start")
        valid_end = supplied.get("t_valid_end")
        if valid_start not in (None, "") and valid_end not in (None, ""):
            _, valid_start_dt = _parse_real_time("T_VALID_START", valid_start)
            _, valid_end_dt = _parse_real_time("T_VALID_END", valid_end)
            if valid_end_dt >= valid_start_dt:
                t_valid_ms = (valid_end_dt - valid_start_dt).total_seconds() * 1000.0

    return {
        "flow_start_state": start_state,
        "flow_start": start_text,
        "state_time": state_text,
        "flow_elapsed_ms": elapsed_ms,
        "t_valid_ms": t_valid_ms,
        "t_star_ms": supplied.get("t_star_ms"),
    }


def advance(
    state, evidence, context, *, page, task, seq,
    time_anchor=None, dispatch=None,
    final_review=False, reviewer=None,
):
    if context.get("page") not in (None, page):
        raise ValueError("页面定位与冻结上下文不一致")
    if task != context.get("task") or seq != context.get("seq"):
        raise ValueError("任务/序号定位与冻结上下文不一致")
    supplied = time_anchor or {}
    _freeze_flow_origin_once(state, context, supplied)
    verdict = judge(state, evidence, context, dispatch)
    code, name, phase, action = TRANSITIONS[state][verdict]

    if state == 40 and verdict == "PASS" and final_review:
        if reviewer != "GPT":
            raise ValueError("只有GPT Final Reviewer可以把状态40签入100")
        code, name, phase, action = (100, "完成", "实", "STOP")

    derived = _derived_time_anchor(context, supplied, code)
    header = render(page, task, seq, phase, code, name, derived)
    result = {"verdict": verdict, "state": code, "action": action, "header": header, "time": derived}
    if state == 20 and verdict == "PASS":
        result["command"] = _dispatch_command(header, dispatch)
    return result
