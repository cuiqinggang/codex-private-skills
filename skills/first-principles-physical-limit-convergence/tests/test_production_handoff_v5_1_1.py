import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent / "runtime" / "production_handoff_v5_1_1.py"
spec = importlib.util.spec_from_file_location("production_handoff_v5_1_1", RUNTIME)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

base = dict(
    page_name="整体闭环极限时间引擎 5.1.1版",
    task_name="两项Reality Delta封堵与重新认证",
    task_no=1,
    virtual_mature=True,
    solution_frozen=True,
    real_started=False,
    timeline_id="ESTE-v5.1.1-R2-LIVE-001",
    time_origin_utc="2026-09-27T11:47:59Z",
    turn_start_utc="2026-09-27T11:47:59Z",
    dispatch_utc="2026-09-27T11:48:01Z",
    freeze_id="ESTE-v5.1.1-HANDOFF-TIME-R2",
    frozen_assets="repo=cuiqinggang/codex-private-skills;branch=codex/first-principles-physical-limit-convergence-v5.1.1-handoff-time-r2",
    reality_valid_contract="验证虚拟成熟后自动进入实；Codex用户可见命令必须含数字时间锚与Timeline；禁止任何手工旁路。",
    reality_timing_boundary="REAL_DISPATCH→EXECUTOR_RETURN_*",
    t_star_ms=0.0027,
    t_star_source="HISTORICAL_COMPONENT_REFERENCE_ONLY_NOT_V5_1_1_USER_JOURNEY_CERTIFICATE",
    executor_task="按冻结资产执行生产同构真实验证，不修改代理；返回可审计证据。",
)

out = mod.close_virtual_and_build_real_dispatch(**base)
assert out.text.startswith("【整体闭环极限时间引擎 5.1.1版｜两项Reality Delta封堵与重新认证｜01｜实】")
assert "【时间锚｜整体已用=2000.000ms｜本次已用=2000.000ms｜T*=0.0027ms】" in out.text
assert "TIMELINE_ID=ESTE-v5.1.1-R2-LIVE-001" in out.text
assert "PASS / FAIL / BLOCKED" in out.text
assert "RETURN_TO_GPT=YES" in out.text
assert "FINAL_VALID/DONE 禁止由 Reality 执行器宣布" in out.text

bad = dict(base)
bad["time_origin_utc"] = ""
try:
    mod.close_virtual_and_build_real_dispatch(**bad)
except mod.ProductionHandoffViolation as e:
    assert "UTC_TIMESTAMP_REQUIRED" in str(e)
else:
    raise AssertionError("missing timeline must block")

bad = dict(base)
bad["real_started"] = True
try:
    mod.close_virtual_and_build_real_dispatch(**bad)
except mod.ProductionHandoffViolation as e:
    assert "REAL_ALREADY_STARTED" in str(e)
else:
    raise AssertionError("duplicate dispatch must block")

bad = dict(base)
bad["task_no"] = 7
try:
    mod.close_virtual_and_build_real_dispatch(**bad)
except mod.ProductionHandoffViolation as e:
    assert "TASK_NO_OUT_OF_RANGE_01_06" in str(e)
else:
    raise AssertionError("task_no > 06 must block")

print("AUTO_VIRTUAL_TO_REAL=PASS")
print("NUMERIC_TIME_ENVELOPE_ALWAYS_RENDERED=PASS")
print("MISSING_TIMELINE_HARD_BLOCK=PASS")
print("DUPLICATE_REAL_DISPATCH_BLOCKED=PASS")
print("TASK_NO_01_06_ENFORCED=PASS")
