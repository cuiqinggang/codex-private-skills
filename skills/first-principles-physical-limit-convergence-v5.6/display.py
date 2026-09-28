"""v5.6 三行核心头：唯一显示器。"""

def render(page, task, seq, phase, code, name, accepted, event_time,
           elapsed="未知", t_valid="尚未产生", t_star="未知"):
    values = (page, task, seq, phase, code, name, accepted, event_time)
    if any(v is None or str(v).strip() == "" for v in values):
        raise ValueError("三行核心头必填字段缺失")
    if phase not in ("虚", "实"):
        raise ValueError("虚/实非法")
    return "\n".join([
        f"【{page}｜{task}｜{seq}｜{phase}】",
        f"【状态机｜v5.6｜{code}｜{name}】",
        f"【时间锚｜TASK_ACCEPTED={accepted}｜当前节点时间={event_time}｜整体已用={elapsed}｜T_VALID={t_valid}｜T*={t_star}】",
    ])
