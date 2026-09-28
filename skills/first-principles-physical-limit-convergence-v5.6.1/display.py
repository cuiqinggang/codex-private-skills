"""v5.6.1 三行核心头：严格、单一、不可注入。"""
import math

_BAD = ("\r", "\n", "｜", "【", "】")

def _field(name, value):
    if value is None or str(value).strip() == "":
        raise ValueError(f"{name}缺失")
    s = str(value)
    if any(x in s for x in _BAD):
        raise ValueError(f"{name}含非法分隔/换行")
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

    accepted = _field("TASK_ACCEPTED", time_anchor.get("accepted", "未知"))
    event = _field("当前节点时间", time_anchor.get("event"))
    aclock = time_anchor.get("accepted_clock")
    eclock = time_anchor.get("event_clock")
    elapsed = time_anchor.get("elapsed_ms")
    t_valid = time_anchor.get("t_valid_ms")
    t_star = time_anchor.get("t_star_ms")
    same_clock = bool(aclock and eclock and aclock == eclock)

    if elapsed is not None:
        elapsed = _number("整体已用", elapsed)
        if not same_clock:
            raise ValueError("整体已用缺少同一可比较时钟")
    if t_valid is not None:
        t_valid = _number("T_VALID", t_valid)
        if code != 100 or not same_clock:
            raise ValueError("T_VALID不具备合法整体时间条件")
    if t_star is not None:
        t_star = _number("T*", t_star)

    elapsed_text = "未知" if elapsed is None else f"{elapsed:.3f}毫秒"
    t_valid_text = "尚未产生" if t_valid is None else f"{t_valid:.3f}毫秒"
    t_star_text = "未知" if t_star is None else f"{t_star:.3f}毫秒"

    return "\n".join([
        f"【{page}｜{task}｜{seq}｜{phase}】",
        f"【状态机｜v5.6.1｜{code}｜{name}】",
        f"【时间锚｜TASK_ACCEPTED={accepted}｜当前节点时间={event}｜整体已用={elapsed_text}｜T_VALID={t_valid_text}｜T*={t_star_text}】",
    ])
