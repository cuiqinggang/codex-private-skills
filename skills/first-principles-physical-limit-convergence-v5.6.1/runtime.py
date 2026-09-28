"""v5.6.1：原始证据绑定→机械裁决→状态→三行显示→20同轮发布。"""
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
        if not evidence.get("raw_evidence") or not evidence.get("time_record"):
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

def advance(state, evidence, context, *, page, task, seq, time_anchor, dispatch=None):
    verdict = judge(state, evidence, context, dispatch)
    code, name, phase, action = TRANSITIONS[state][verdict]
    header = render(page, task, seq, phase, code, name, time_anchor)
    result = {"verdict": verdict, "state": code, "action": action, "header": header}
    if state == 20 and verdict == "PASS":
        result["command"] = _dispatch_command(header, dispatch)
    return result
