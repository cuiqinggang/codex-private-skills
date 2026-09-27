import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent / "runtime" / "production_handoff_v5_2_0.py"
spec = importlib.util.spec_from_file_location("production_handoff_v5_2_0", RUNTIME)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

base = dict(
    page_name="整体闭环极限时间引擎 5.2版",
    task_name="v5.2.0真实使用",
    task_no=1,
    virtual_mature=True,
    solution_frozen=True,
    real_started=False,
    timeline_id="ESTE-v5.2.0-LIVE-001",
    time_origin_utc="2026-09-27T12:00:00Z",
    turn_start_utc="2026-09-27T12:00:00Z",
    dispatch_utc="2026-09-27T12:00:02Z",
    freeze_id="ESTE-v5.2.0-VIRTUAL-FREEZE-R1",
    frozen_assets="repo=cuiqinggang/codex-private-skills;branch=codex/first-principles-physical-limit-convergence-v5.2.0-virtual",
    reality_valid_contract="按正式生产路径进行真实使用验收。",
    reality_timing_boundary="REAL_DISPATCH→EXECUTOR_RETURN_*",
    t_star_ms=0.0027,
    t_star_source="HISTORICAL_REFERENCE_ONLY",
    executor_task="执行冻结任务并返回真实结果。",
)

out = mod.build_real_dispatch(**base)
assert out.text.startswith("【整体闭环极限时间引擎 5.2版｜v5.2.0真实使用｜01｜实】")
assert "【时间锚｜整体已用=2000.000ms｜本次已用=2000.000ms｜T*=0.0027ms】" in out.text
assert "TIMELINE_ID=ESTE-v5.2.0-LIVE-001" in out.text
assert "PASS / FAIL / BLOCKED" in out.text
assert "RETURN_TO_GPT=YES" in out.text

def must_block(changes, expected):
    data = dict(base)
    data.update(changes)
    try:
        mod.build_real_dispatch(**data)
    except mod.ProductionHandoffViolation as e:
        assert expected in str(e), (expected, str(e))
        return
    raise AssertionError("expected block: " + expected)

must_block({"timeline_id": ""}, "TIMELINE_ID_REQUIRED")
must_block({"time_origin_utc": ""}, "UTC_TIMESTAMP_REQUIRED")
must_block({"real_started": True}, "REAL_ALREADY_STARTED")
must_block({"task_no": 7}, "TASK_NO_OUT_OF_RANGE_01_06")

print("RENDERED_TIME_REGEX=PASS")
print("MISSING_TIMELINE_ID_BLOCK=PASS")
print("MISSING_TIME_ORIGIN_BLOCK=PASS")
print("DUPLICATE_REAL_DISPATCH_BLOCK=PASS")
print("TASK_NO_01_06_BLOCK=PASS")

# A manually composed/incomplete Reality dispatch must be rejected by the same production validator.
manual_incomplete = """【整体闭环极限时间引擎 5.2版｜v5.2.0真实使用｜01｜实】
FREEZE_ID=ESTE-v5.2.0-VIRTUAL-FREEZE-R1
RETURN_TO_GPT=YES
"""
try:
    mod.validate_rendered_dispatch(manual_incomplete)
except mod.ProductionHandoffViolation:
    pass
else:
    raise AssertionError("manual incomplete dispatch must be rejected")

print("MANUAL_BYPASS_INCOMPLETE_REJECTED=PASS")
