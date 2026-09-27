import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent / "runtime" / "scope_gate_v5_2_2.py"
spec = importlib.util.spec_from_file_location("scope_gate_v5_2_2", RUNTIME)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Real production counterexample supplied from DSE:
bad_dse = """【决策系统引擎1｜DSE v1.0.3轻量版真实使用测试｜01｜实】
【时间锚｜可审计收口段已用=10000ms｜完整闭环时间=未认证｜T*=待现实求解】
TIMELINE_ID=DSE-v1.0.3-R2-20260927-214325
TIME_ORIGIN=2026-09-27T21:43:25+08:00
DSE_VERSION=v1.0.3
FREEZE_ID=DSE-v1.0.3-LIGHTWEIGHT-VIRTUAL-FREEZE-R2
"""

try:
    mod.enforce_in_scope_final_output(bad_dse)
except mod.ScopeGateViolation:
    pass
else:
    raise AssertionError("DSE header-only real output must be blocked")

# Generic header-only outputs must be blocked regardless of business name.
for page, task in [
    ("盈利成本引擎1", "盈利路径真实使用测试"),
    ("混合智能概率引擎7", "HIPE真实使用测试"),
    ("H3-P1视频技能包", "首个图声对真实使用测试"),
]:
    bad = f"""【{page}｜{task}｜01｜实】
FREEZE_ID=EXAMPLE
RETURN_TO_GPT=YES
"""
    try:
        mod.enforce_in_scope_final_output(bad)
    except mod.ScopeGateViolation:
        pass
    else:
        raise AssertionError(f"header-only output must be blocked for {page}")

# Arbitrary businesses must pass through the same skill-wide builder.
for i, (page, task) in enumerate([
    ("决策系统引擎1", "DSE v1.0.4轻量版真实使用测试"),
    ("盈利成本引擎1", "盈利路径真实使用测试"),
    ("混合智能概率引擎7", "HIPE真实使用测试"),
    ("H3-P1视频技能包", "首个图声对真实使用测试"),
], start=1):
    out = mod.build_in_scope_real_dispatch(
        page_name=page,
        task_name=task,
        task_no=i,
        virtual_mature=True,
        solution_frozen=True,
        real_started=False,
        timeline_id=f"GENERIC-LIVE-{i:03d}",
        time_origin_utc="2026-09-27T13:00:00Z",
        turn_start_utc="2026-09-27T13:00:01Z",
        dispatch_utc="2026-09-27T13:00:02Z",
        freeze_id=f"GENERIC-FREEZE-{i}",
        freeze_ref=f"freeze/generic-{i}",
        contract_ref=f"contracts/generic-{i}.json",
        t_star_ms=0.0027,
        executor_task="执行冻结任务；必须实际完成任务，不得只输出状态头。",
    )
    assert mod.enforce_in_scope_final_output(out.text) == "IN_SCOPE_REAL_DISPATCH_VALID"
    assert "\n\n执行：\n" in out.text
    assert "RESULT=PASS|FAIL|BLOCKED" in out.text
    assert "RETURN_TO_GPT=YES" in out.text
    assert "NO_FINAL_VALID_DONE=YES" in out.text

# Non-REAL ordinary outputs are outside this dispatch gate.
assert mod.enforce_in_scope_final_output("普通虚拟阶段说明") == "NO_REAL_DISPATCH_IN_OUTPUT"

print("DSE_REAL_COUNTEREXAMPLE_REJECTED=PASS")
print("GENERIC_HEADER_ONLY_REJECTED=PASS")
print("ALL_BUSINESS_NAMES_USE_SAME_SCOPE_GATE=PASS")
print("COMPLETE_EXECUTION_BODY_REQUIRED=PASS")
print("RETURN_CONTRACT_REQUIRED=PASS")
print("NON_REAL_OUTPUT_NOT_OVERBLOCKED=PASS")


# Real transport may add one Markdown line-continuation backslash after the execution marker.
sample = mod.build_in_scope_real_dispatch(
    page_name="决策系统引擎1",
    task_name="DSE 下游完整派发真实使用测试",
    task_no=1,
    virtual_mature=True,
    solution_frozen=True,
    real_started=False,
    timeline_id="MARKDOWN-LIVE-001",
    time_origin_utc="2026-09-27T13:00:00Z",
    turn_start_utc="2026-09-27T13:00:01Z",
    dispatch_utc="2026-09-27T13:00:02Z",
    freeze_id="MARKDOWN-FREEZE-1",
    freeze_ref="freeze/markdown-1",
    contract_ref="contracts/markdown-1.json",
    t_star_ms=0.0027,
    executor_task="执行冻结任务；必须实际完成任务，不得只输出状态头。",
).text

transport = sample.replace("\n\n执行：\n", "\n\n执行：\\\n", 1)
assert mod.enforce_in_scope_final_output(transport) == "IN_SCOPE_REAL_DISPATCH_VALID"

overescaped = sample.replace("\n\n执行：\n", "\n\n执行：\\\\\n", 1)
try:
    mod.enforce_in_scope_final_output(overescaped)
except mod.ScopeGateViolation as e:
    assert "EXECUTION_BODY_MISSING" in str(e)
else:
    raise AssertionError("double execution-marker escape must be rejected")

print("MARKDOWN_EXECUTION_MARKER_EQUIVALENCE=PASS")
print("OVERESCAPED_EXECUTION_MARKER_REJECTED=PASS")
