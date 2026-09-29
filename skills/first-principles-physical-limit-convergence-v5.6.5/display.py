"""v5.6.5 三行核心头：状态机不变，时间模型只显示实际流程起点、节点时间和两类效率指标。"""
import math
from datetime import datetime

_BAD = ("\r", "\n", "｜", "【", "】")


def _field(name, value):
    if value is None or str(value).strip() == "":
        raise ValueError(f"{name}缺失")
    s = str(value)
    if any(x in s for x in _BAD):
        raise ValueError(f"{name}含非法分隔/换行")
    return s


def _time_field(name, value):
    s = _field(name, value)
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{name}不是现实可读时间") from exc
    if dt.tzinfo is None:
        raise ValueError(f"{name}缺少时区")
    return s


def _number(name, value):
    x = float(value)
    if not math.isfinite(x) or x < 0:
        raise ValueError(f"{name}非法")
    return x


def render(page, task, seq, phase, code, name, time_anchor):
    page = _field("页面名", page)
    task = _field("任务名", task)
    seq = _field("序号", seq)
    phase = _field("虚实", phase)
    name = _field("状态名", name)
    if phase not in ("虚", "实"):
        raise ValueError("虚/实非法")

    flow_start_state = int(time_anchor.get("flow_start_state"))
    if flow_start_state not in (10, 20, 30, 40, 100):
        raise ValueError("本轮起点状态非法")
    flow_start = _time_field("本轮起点时间", time_anchor.get("flow_start"))
    state_time = _time_field("当前节点时间", time_anchor.get("state_time"))

    elapsed = time_anchor.get("flow_elapsed_ms")
    t_valid = time_anchor.get("t_valid_ms")
    t_star = time_anchor.get("t_star_ms")

    if elapsed is not None:
        elapsed = _number("本轮已用", elapsed)
    if t_valid is not None:
        t_valid = _number("T_VALID", t_valid)
        if code != 100:
            raise ValueError("非100状态不得确认数值T_VALID")
    if t_star is not None:
        t_star = _number("T*", t_star)

    elapsed_text = "未知" if elapsed is None else f"{elapsed:.3f}毫秒"
    t_valid_text = "尚未产生" if t_valid is None else f"{t_valid:.3f}毫秒"
    t_star_text = "未知" if t_star is None else f"{t_star:.3f}毫秒"

    return "\n".join([
        f"【{page}｜{task}｜{seq}｜{phase}】",
        f"【状态机｜v5.6.5｜{code}｜{name}】",
        f"【时间｜本轮起点={flow_start_state}@{flow_start}｜当前节点={code}@{state_time}｜本轮已用(T_FLOW)={elapsed_text}｜T_VALID={t_valid_text}｜T*={t_star_text}】",
    ])
