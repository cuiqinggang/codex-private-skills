import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent / "runtime" / "dse_reality_dispatch_v1_0_4.py"
spec = importlib.util.spec_from_file_location("dse_reality_dispatch_v1_0_4", RUNTIME)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

bad_header_only = """【决策系统引擎1｜DSE v1.0.3轻量版真实使用测试｜01｜实】
【时间锚｜可审计收口段已用=10000ms｜完整闭环时间=未认证｜T*=待现实求解】
TIMELINE_ID=DSE-v1.0.3-R2-20260927-214325
TIME_ORIGIN=2026-09-27T21:43:25+08:00
DSE_VERSION=v1.0.3
FREEZE_ID=DSE-v1.0.3-LIGHTWEIGHT-VIRTUAL-FREEZE-R2
"""

try:
    mod.validate_dse_dispatch(bad_header_only)
except Exception:
    pass
else:
    raise AssertionError("header-only DSE dispatch must be rejected")

out = mod.build_dse_real_dispatch(
    task_name="DSE v1.0.4轻量版真实使用测试",
    task_no=1,
    timeline_id="DSE-v1.0.4-LIVE-001",
    time_origin_utc="2026-09-27T13:00:00Z",
    turn_start_utc="2026-09-27T13:00:01Z",
    dispatch_utc="2026-09-27T13:00:02Z",
    integration_freeze_id="DSE-v1.0.4-DISPATCH-BINDING-VIRTUAL-FREEZE-R1",
    freeze_ref="freeze/dse-v1.0.4-r1",
    contract_ref="skills/decision-system-engine/contracts/REALITY-DISPATCH-BINDING-v1.0.4.json",
    dse_logic_freeze_id="DSE-v1.0.3-LIGHTWEIGHT-VIRTUAL-FREEZE-R2",
    t_star_reference_ms=0.0012098,
    executor_task="按冻结 DSE 逻辑完成真实使用测试；执行正式任务，不得只输出状态头。完成后按返回合同回 GPT。",
)

text = out.text
assert text.startswith("【决策系统引擎1｜DSE v1.0.4轻量版真实使用测试｜01｜实】")
assert "【时间锚｜整体已用=2000.000ms｜本次已用=1000.000ms｜T*=0.00121ms】" in text
assert "TIME_ORIGIN_UTC=" in text
assert "DISPATCH_UTC=" in text
assert "FREEZE_REF=freeze/dse-v1.0.4-r1" in text
assert "DSE_VERSION=1.0.4" in text
assert "DSE_LOGIC_FREEZE_ID=DSE-v1.0.3-LIGHTWEIGHT-VIRTUAL-FREEZE-R2" in text
assert "T_STAR_STATUS=VIRTUAL_REFERENCE_PENDING_REAL_USAGE_TEST" in text
assert "\n\n执行：\n" in text
body = text.split("\n\n执行：\n",1)[1].split("\n\n返回：",1)[0].strip()
assert body
assert "RESULT=PASS|FAIL|BLOCKED" in text
assert "RETURN_TO_GPT=YES" in text
assert "NO_FINAL_VALID_DONE=YES" in text
assert mod.validate_dse_dispatch(text) == "DSE_DISPATCH_VALID"

print("HEADER_ONLY_REJECTED=PASS")
print("PARENT_RENDERER_BOUND=PASS")
print("NUMERIC_TIME_ENVELOPE=PASS")
print("TIMELINE_AND_DISPATCH_UTC=PASS")
print("EXECUTION_BODY_PRESENT=PASS")
print("RETURN_CONTRACT_PRESENT=PASS")
print("DSE_VERSION_AND_LOGIC_FREEZE=PASS")
print("COMPLETE_CODEX_COMMAND=PASS")
