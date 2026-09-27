import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent / "runtime" / "fsm_v5_3_0.py"
spec = importlib.util.spec_from_file_location("fsm_v5_3_0", RUNTIME)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert int(mod.State.NEW) == 0
assert int(mod.State.VIRTUAL) == 10
assert int(mod.State.VIRTUAL_MATURE) == 20
assert int(mod.State.FROZEN) == 30
assert int(mod.State.REAL_DISPATCHED) == 40
assert int(mod.State.BLOCKED) == 90
assert int(mod.State.FINAL_VALID) == 100

machine = mod.Machine()
mod.start(machine)
assert machine.state == 10

mod.mark_virtual_mature(machine)
assert machine.state == 20
assert mod.may_end_user_reply(machine) is False
try:
    mod.require_reply_may_end(machine)
except mod.FSMViolation as e:
    assert "REPLY_END_FORBIDDEN_BEFORE_REAL_DISPATCH" in str(e)
else:
    raise AssertionError("reply end must be forbidden at VIRTUAL_MATURE")

assert not hasattr(mod, "freeze_only")

machine, out = mod.freeze_and_dispatch(
    machine,
    page_name="决策系统引擎1",
    task_name="DSE真实使用测试",
    task_no=1,
    virtual_mature=True,
    solution_frozen=True,
    real_started=False,
    timeline_id="FSM-LIVE-001",
    time_origin_utc="2026-09-27T14:00:00Z",
    turn_start_utc="2026-09-27T14:00:01Z",
    dispatch_utc="2026-09-27T14:00:02Z",
    freeze_id="FSM-FREEZE-001",
    freeze_ref="freeze/fsm-001",
    contract_ref="contracts/fsm-001.json",
    t_star_ms=0.0027,
    executor_task="执行冻结任务；必须实际完成，不得只输出状态头。",
)
assert machine.state == 40
assert machine.last_result == "DISPATCHED"
assert mod.require_reply_may_end(machine) == "REPLY_END_ALLOWED"
assert "\n\n执行：\n" in out.text
assert "RESULT=PASS|FAIL|BLOCKED" in out.text

mod.apply_reality_result(machine, "FAIL")
assert machine.state == 10
assert machine.last_result == "FAIL"

mod.mark_virtual_mature(machine)
machine, out2 = mod.freeze_and_dispatch(
    machine,
    page_name="盈利成本引擎1",
    task_name="盈利路径真实使用测试",
    task_no=2,
    virtual_mature=True,
    solution_frozen=True,
    real_started=False,
    timeline_id="FSM-LIVE-002",
    time_origin_utc="2026-09-27T14:10:00Z",
    turn_start_utc="2026-09-27T14:10:01Z",
    dispatch_utc="2026-09-27T14:10:02Z",
    freeze_id="FSM-FREEZE-002",
    freeze_ref="freeze/fsm-002",
    contract_ref="contracts/fsm-002.json",
    t_star_ms=0.0027,
    executor_task="执行冻结任务。",
)
mod.apply_reality_result(machine, "BLOCKED")
assert machine.state == 90
mod.resume_blocked(machine)
assert machine.state == 10

mod.mark_virtual_mature(machine)
machine, out3 = mod.freeze_and_dispatch(
    machine,
    page_name="H3-P1视频技能包",
    task_name="图声对真实使用测试",
    task_no=3,
    virtual_mature=True,
    solution_frozen=True,
    real_started=False,
    timeline_id="FSM-LIVE-003",
    time_origin_utc="2026-09-27T14:20:00Z",
    turn_start_utc="2026-09-27T14:20:01Z",
    dispatch_utc="2026-09-27T14:20:02Z",
    freeze_id="FSM-FREEZE-003",
    freeze_ref="freeze/fsm-003",
    contract_ref="contracts/fsm-003.json",
    t_star_ms=0.0027,
    executor_task="执行冻结任务。",
)
mod.apply_reality_result(machine, "PASS")
assert machine.state == 100
assert machine.last_result == "PASS"
assert mod.require_reply_may_end(machine) == "REPLY_END_ALLOWED"

# Illegal state jumps are impossible through public APIs.
try:
    mod.mark_virtual_mature(mod.Machine())
except mod.FSMViolation:
    pass
else:
    raise AssertionError("illegal NEW->VIRTUAL_MATURE must be blocked")

print("STATE_CODES_FIXED=PASS")
print("VIRTUAL_MATURE_REPLY_END_BLOCKED=PASS")
print("NO_FREEZE_ONLY_API=PASS")
print("FREEZE_TO_REAL_ATOMIC=PASS")
print("REAL_DISPATCH_COMPLETE=PASS")
print("FAIL_RETURNS_VIRTUAL=PASS")
print("BLOCKED_RESUME_PATH=PASS")
print("PASS_FINAL_VALID=PASS")
print("ILLEGAL_TRANSITION_BLOCKED=PASS")
print("BUSINESS_AGNOSTIC_STATE_MACHINE=PASS")
