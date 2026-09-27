import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent / "runtime" / "acceptance_supervisor_v5_3_3.py"
spec = importlib.util.spec_from_file_location("acceptance_supervisor_v5_3_3", RUNTIME)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

s = mod.Supervisor()
x = mod.before_dispatch(s)
assert x["dispatch_count"] == 1
assert x["active_path"] == "A"
assert x["browser_executor"] == "playwright-native-ai-browser"

assert mod.transport_failure(s) == "RETRY_SAME_PATH_ONCE"
assert mod.transport_failure(s) == "SWITCH_TO_PATH_B"
assert mod.transport_failure(s) == "RETRY_SAME_PATH_ONCE"
assert mod.transport_failure(s) == "SWITCH_TO_PATH_C"
assert mod.transport_failure(s) == "RETRY_SAME_PATH_ONCE"
assert mod.transport_failure(s) == "ALL_PATHS_UNAVAILABLE_BLOCK"

assert mod.acceptance_result("PASS","NONE") == "FSM_PASS_TO_FINAL_VALID"
assert mod.acceptance_result("FAIL","PRODUCT") == "FSM_FAIL_TO_VIRTUAL_REMATURE_REFREEZE"
assert mod.acceptance_result("FAIL","TEST_HARNESS") == "SUPERVISOR_RECOVER_OR_SWITCH_WITH_SAME_PRODUCT_FREEZE"
assert mod.acceptance_result("FAIL","TRANSPORT") == "SUPERVISOR_RECOVER_OR_SWITCH_WITH_SAME_PRODUCT_FREEZE"
assert mod.acceptance_result("BLOCKED","EXTERNAL") == "SUPERVISOR_RECOVER_OR_SWITCH_ELSE_FSM_BLOCKED"

req = mod.codex_acceptance_requirements()
assert req["test_case_selected_by"] == "CODEX_AT_RUNTIME"
assert req["browser_skill_required"] == "playwright-native-ai-browser"
assert req["ad_hoc_browser_script_allowed"] is False
assert req["product_plan_authority"] == "GPT"
assert req["acceptance_task_selection_authority"] == "CODEX"

s2 = mod.Supervisor()
for i in range(6):
    out = mod.before_dispatch(s2)
    assert out["dispatch_count"] == i + 1
try:
    mod.before_dispatch(s2)
except mod.SupervisorViolation as e:
    assert "MAX_6_DISPATCHES_REACHED" in str(e)
else:
    raise AssertionError("7th dispatch must be blocked")

print("JEV_BROWSER_FIXED=PASS")
print("CODEX_SELECTS_TEST_CASE=PASS")
print("PRODUCT_FAIL_RETURNS_VIRTUAL=PASS")
print("TEST_HARNESS_FAIL_PRESERVES_PRODUCT_FREEZE=PASS")
print("TRANSPORT_FAIL_USES_ORCHESTRATOR_RECOVERY=PASS")
print("ABC_PATH_SWITCHING=PASS")
print("MAX_6_DISPATCHES=PASS")
print("GPT_REMAINS_PRODUCT_PLAN_AUTHORITY=PASS")
