"""整体闭环极限短时间引擎 v5.6：唯一机械状态转移器。"""

TRANSITIONS = {
    10: {
        "PASS": (20, "冻结最短有效方案"),
        "FAIL": (10, "留10"),
    },
    20: {
        "PASS": (30, "自动生成完整现实交接；写入共同工作区；立即输出合格Codex短指针"),
        "FAIL": (10, "回10"),
    },
    30: {
        "PASS": (40, "立即执行同一冻结包"),
        "FAIL": (30, "留30并回报阻断"),
    },
    40: {
        "PASS": (100, "冻结最终有效证据"),
        "FAIL": (10, "明确失败回10"),
        "UNKNOWN": (40, "证据不足留40"),
    },
    100: {
        "PASS": (100, "STOP"),
        "FAIL": (100, "不得改变已完成记录"),
    },
}

def advance(state: int, verdict: str):
    """只按冻结表返回唯一下一状态和固定动作；无自由路由。"""
    verdict = verdict.upper()
    try:
        return TRANSITIONS[state][verdict]
    except KeyError as exc:
        raise ValueError(f"非法状态/裁决: {state}/{verdict}") from exc
