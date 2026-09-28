"""整体闭环极限短时间引擎 v5.6：证据裁决、状态转移、显示与20→30发布一体。"""
from display import render

TRANSITIONS = {
    10: {"PASS": (20, "虚：已冻结", "虚", "冻结最短有效方案"), "FAIL": (10, "虚：准备中", "虚", "留10"), "UNKNOWN": (10, "虚：准备中", "虚", "留10")},
    20: {"PASS": (30, "虚实交接中", "实", "发布现实交接"), "FAIL": (10, "虚：准备中", "虚", "回10"), "UNKNOWN": (20, "虚：已冻结", "虚", "留20补证据")},
    30: {"PASS": (40, "实：执行与审核中", "实", "立即执行同一冻结包"), "FAIL": (30, "虚实交接中", "实", "留30并回报阻断"), "UNKNOWN": (30, "虚实交接中", "实", "留30并回报阻断")},
    40: {"PASS": (100, "完成", "实", "冻结最终有效证据"), "FAIL": (10, "虚：准备中", "虚", "明确失败回10"), "UNKNOWN": (40, "实：执行与审核中", "实", "证据不足留40")},
    100: {"PASS": (100, "完成", "实", "STOP")},
}

REQUIRED = {
    10: ("goal", "valid_defined", "task_accepted"),
    20: ("frozen_body", "task_link", "time_anchor", "materials_readable", "dispatch_ready"),
    30: ("task_match", "materials_match", "time_anchor_match", "same_package"),
    40: ("result_valid", "raw_evidence", "task_link", "time_record", "final_valid"),
}

def judge(state, evidence):
    if state == 100:
        return "PASS"
    vals = [evidence.get(k) for k in REQUIRED[state]]
    if any(v is False for v in vals):
        return "FAIL"
    if any(v is not True for v in vals):
        return "UNKNOWN"
    return "PASS"

def _dispatch_command(header, dispatch):
    """20 PASS时生成唯一可发布命令；优先共同工作区，失败才允许内联备用正文。"""
    repo = dispatch.get("repo")
    commit = dispatch.get("commit")
    entry = dispatch.get("entry")
    if repo and commit and entry:
        body = (
            f"从共同私库 {repo} 固定提交：\n{commit}\n\n"
            f"读取并严格执行：\n{entry}"
        )
    else:
        inline = dispatch.get("inline")
        if not inline:
            raise ValueError("20 PASS缺少可发布交接：共同工作区指针或内联备用正文")
        body = inline
    return header + "\n\n" + body

def advance(state, evidence, *, page, task, seq, accepted, event_time,
            elapsed="未知", t_valid="尚未产生", t_star="未知", dispatch=None):
    """一次调用完成：证据→裁决→状态→三行显示；20 PASS同时生成可直接发布的30命令。"""
    verdict = judge(state, evidence)
    code, name, phase, action = TRANSITIONS[state][verdict]
    header = render(page, task, seq, phase, code, name, accepted, event_time,
                    elapsed, t_valid, t_star)
    result = {"verdict": verdict, "state": code, "action": action, "header": header}
    if state == 20 and verdict == "PASS":
        if dispatch is None:
            raise ValueError("20 PASS必须在同一次调用生成现实交接")
        result["command"] = _dispatch_command(header, dispatch)
    return result
