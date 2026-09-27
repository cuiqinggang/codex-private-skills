import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent / "runtime" / "production_handoff_v5_2_0.py"
spec = importlib.util.spec_from_file_location("production_handoff_v5_2_0", RUNTIME)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

base = dict(
    page_name="整体闭环极限时间引擎 5.2版",
    task_name="v5.2.0真实使用测试",
    task_no=3,
    virtual_mature=True,
    solution_frozen=True,
    real_started=False,
    timeline_id="ESTE-v5.2.0-LIVE-001",
    time_origin_utc="2026-09-27T12:00:00Z",
    turn_start_utc="2026-09-27T12:00:01Z",
    dispatch_utc="2026-09-27T12:00:02Z",
    freeze_id="ESTE-v5.2.0-REAL-USAGE-TEST-VIRTUAL-FREEZE-R3",
    freeze_ref="freeze/este-v5.2.0-r3",
    contract_ref="docs/first-principles/v5.2.0/REAL-USAGE-TEST-CONTRACT-R3.json",
    t_star_ms=0.0027,
    executor_task="读取冻结清单与合同，运行冻结低层检查，再按合同直接检查本次收到的用户可见命令；禁止创建临时辅助脚本。",
)

out = mod.build_real_dispatch(**base)
assert out.text.startswith("【整体闭环极限时间引擎 5.2版｜v5.2.0真实使用测试｜03｜实】")
assert "【时间锚｜整体已用=2000.000ms｜本次已用=1000.000ms｜T*=0.0027ms】" in out.text
assert "FREEZE_REF=freeze/este-v5.2.0-r3" in out.text
assert "CONTRACT_REF=docs/first-principles/v5.2.0/REAL-USAGE-TEST-CONTRACT-R3.json" in out.text
assert "FROZEN_ASSETS=" not in out.text
assert "REALITY_VALID_CONTRACT=" not in out.text
assert "RESULT=PASS|FAIL|BLOCKED" in out.text
assert "RETURN_TO_GPT=YES" in out.text
assert "NO_FINAL_VALID_DONE=YES" in out.text

header = out.text.split("\n\n执行：", 1)[0]
assert len(header) <= 1200

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
must_block({"freeze_ref": ""}, "FREEZE_REF_REQUIRED")
must_block({"contract_ref": ""}, "CONTRACT_REF_REQUIRED")

manual_incomplete = """【整体闭环极限时间引擎 5.2版｜v5.2.0真实使用测试｜03｜实】
FREEZE_ID=ESTE-v5.2.0-REAL-USAGE-TEST-VIRTUAL-FREEZE-R3
RETURN_TO_GPT=YES
"""
try:
    mod.validate_rendered_dispatch(manual_incomplete)
except mod.ProductionHandoffViolation:
    pass
else:
    raise AssertionError("manual incomplete dispatch must be rejected")

escaped_time = out.text.replace("T*=", r"T\*=", 1)
mod.validate_rendered_dispatch(escaped_time)

overescaped_time = out.text.replace("T*=", r"T\\*=", 1)
try:
    mod.validate_rendered_dispatch(overescaped_time)
except mod.ProductionHandoffViolation as e:
    assert "NUMERIC_TIME_ENVELOPE_MISSING" in str(e)
else:
    raise AssertionError("overescaped time anchor must be rejected")

wrong_token = out.text.replace("T*=", "TSTAR=", 1)
try:
    mod.validate_rendered_dispatch(wrong_token)
except mod.ProductionHandoffViolation as e:
    assert "NUMERIC_TIME_ENVELOPE_MISSING" in str(e)
else:
    raise AssertionError("semantic token change must be rejected")

expanded = out.text.replace("FREEZE_REF=", "FROZEN_ASSETS=x\nFREEZE_REF=", 1)
try:
    mod.validate_rendered_dispatch(expanded)
except mod.ProductionHandoffViolation as e:
    assert "EXPANDED_ASSET_LIST_FORBIDDEN" in str(e)
else:
    raise AssertionError("expanded visible asset list must be rejected")

print("COMPACT_DISPATCH_RENDER=PASS")
print("NUMERIC_TIME_ENVELOPE=PASS")
print("TIMELINE_GATES=PASS")
print("TASK_NO_01_06=PASS")
print("FREEZE_AND_CONTRACT_REFS=PASS")
print("MANUAL_INCOMPLETE_REJECTED=PASS")
print("MARKDOWN_T_STAR_EQUIVALENCE=PASS")
print("OVERBROAD_NORMALIZATION_REJECTED=PASS")
print("EXPANDED_VISIBLE_ASSET_LIST_REJECTED=PASS")
print("CONTROL_HEADER_BUDGET=PASS")
