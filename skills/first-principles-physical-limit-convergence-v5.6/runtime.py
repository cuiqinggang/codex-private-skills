"""整体闭环极限短时间引擎 v5.6：唯一机械状态转移器。"""
from display import render

TRANSITIONS = {
    10: {"PASS": (20, "虚：已冻结", "虚", "冻结最短有效方案"), "FAIL": (10, "虚：准备中", "虚", "留10")},
    20: {"PASS": (30, "虚实交接中", "实", "自动生成完整现实交接；写入共同工作区；立即输出合格Codex短指针"), "FAIL": (10, "虚：准备中", "虚", "回10")},
    30: {"PASS": (40, "实：执行与审核中", "实", "立即执行同一冻结包"), "FAIL": (30, "虚实交接中", "实", "留30并回报阻断")},
    40: {"PASS": (100, "完成", "实", "冻结最终有效证据"), "FAIL": (10, "虚：准备中", "虚", "明确失败回10"), "UNKNOWN": (40, "实：执行与审核中", "实", "证据不足留40")},
    100: {"PASS": (100, "完成", "实", "STOP")},
}

def advance(state, verdict, *, page, task, seq, accepted, event_time,
            elapsed="未知", t_valid="尚未产生", t_star="未知"):
    """状态转移与三行显示是同一个原子结果；不存在无显示的合法转移。"""
    verdict = verdict.upper()
    try:
        code, name, phase, action = TRANSITIONS[state][verdict]
    except KeyError as exc:
        raise ValueError(f"非法状态/裁决: {state}/{verdict}") from exc
    header = render(page, task, seq, phase, code, name, accepted, event_time,
                    elapsed, t_valid, t_star)
    return {"state": code, "action": action, "header": header}
