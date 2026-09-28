"""整体闭环极限短时间引擎 v5.6：证据裁决、状态转移、三行显示一体。"""
from display import render

TRANSITIONS = {
    10: {"PASS": (20, "虚：已冻结", "虚", "冻结最短有效方案"), "FAIL": (10, "虚：准备中", "虚", "留10"), "UNKNOWN": (10, "虚：准备中", "虚", "留10")},
    20: {"PASS": (30, "虚实交接中", "实", "自动生成完整现实交接；写入共同工作区；立即输出合格Codex短指针"), "FAIL": (10, "虚：准备中", "虚", "回10"), "UNKNOWN": (20, "虚：已冻结", "虚", "留20补证据")},
    30: {"PASS": (40, "实：执行与审核中", "实", "立即执行同一冻结包"), "FAIL": (30, "虚实交接中", "实", "留30并回报阻断"), "UNKNOWN": (30, "虚实交接中", "实", "留30并回报阻断")},
    40: {"PASS": (100, "完成", "实", "冻结最终有效证据"), "FAIL": (10, "虚：准备中", "虚", "明确失败回10"), "UNKNOWN": (40, "实：执行与审核中", "实", "证据不足留40")},
    100: {"PASS": (100, "完成", "实", "STOP")},
}

REQUIRED = {
    10: ("goal", "valid_defined", "task_accepted"),
    20: ("frozen_body", "task_link", "time_anchor", "materials_readable"),
    30: ("task_match", "materials_match", "time_anchor_match", "same_package"),
    40: ("result_valid", "raw_evidence", "task_link", "time_record", "final_valid"),
}

def judge(state, evidence):
    """只依据当前状态固定验收字段裁决；调用者不能传PASS。"""
    if state == 100:
        return "PASS"
    required = REQUIRED[state]
    vals = [evidence.get(k) for k in required]
    if any(v is False for v in vals):
        return "FAIL"
    if any(v is not True for v in vals):
        return "UNKNOWN"
    return "PASS"

def advance(state, evidence, *, page, task, seq, accepted, event_time,
            elapsed="未知", t_valid="尚未产生", t_star="未知"):
    """证据→裁决→状态→三行显示，一个机械调用完成。"""
    verdict = judge(state, evidence)
    code, name, phase, action = TRANSITIONS[state][verdict]
    header = render(page, task, seq, phase, code, name, accepted, event_time,
                    elapsed, t_valid, t_star)
    return {"verdict": verdict, "state": code, "action": action, "header": header}
