from dataclasses import dataclass
from acceptance_review_v1_0_1 import review_acceptance, review_wait

MAX_DISPATCHES = 6
PATHS = ("A", "B", "C")

class SupervisorViolation(Exception):
    pass

@dataclass
class Supervisor:
    dispatch_count: int = 0
    active_path: str = "A"
    recovery_used_on_path: bool = False

def _require(cond, reason):
    if not cond:
        raise SupervisorViolation(reason)

def before_dispatch(s: Supervisor):
    _require(s.dispatch_count < MAX_DISPATCHES, "MAX_6_DISPATCHES_REACHED")
    s.dispatch_count += 1
    return {
        "dispatch_count": s.dispatch_count,
        "active_path": s.active_path,
        "browser_executor": "playwright-native-ai-browser",
        "browser_mode": "JEV_NATIVE_PLAYWRIGHT_R3",
    }

def transport_failure(s: Supervisor):
    """
    Reuse only the mature A/B/C transport policy from
    gpt-codex-convergence-orchestrator v1.5.2.
    This does NOT change product FSM state.
    """
    if not s.recovery_used_on_path:
        s.recovery_used_on_path = True
        return "RETRY_SAME_PATH_ONCE"

    idx = PATHS.index(s.active_path)
    if idx + 1 < len(PATHS):
        s.active_path = PATHS[idx + 1]
        s.recovery_used_on_path = False
        return f"SWITCH_TO_PATH_{s.active_path}"

    return "ALL_PATHS_UNAVAILABLE_BLOCK"

def acceptance_result(result: str, fail_source: str, *, expected=None, evidence=None):
    r = str(result).upper().strip()
    f = str(fail_source).upper().strip()

    _require(r in {"PASS", "FAIL", "BLOCKED"}, "UNKNOWN_RESULT")
    _require(f in {"NONE", "PRODUCT", "TEST_HARNESS", "TRANSPORT", "EXTERNAL", "MANUAL_HANDOFF"}, "UNKNOWN_FAIL_SOURCE")

    r, f = review_acceptance(r, f, expected=expected, evidence=evidence)
    if r == "HOLD":
        return f
    if f == "MANUAL_HANDOFF":
        return "ACCEPTANCE_FAIL_CONFIRMED_HUMAN_NO_PRODUCT_CHANGE"

    if r == "PASS":
        return "FSM_PASS_TO_FINAL_VALID"

    if r == "FAIL" and f == "PRODUCT":
        return "FSM_FAIL_TO_VIRTUAL_REMATURE_REFREEZE"

    if r == "FAIL" and f in {"TEST_HARNESS", "TRANSPORT"}:
        return "SUPERVISOR_RECOVER_OR_SWITCH_WITH_SAME_PRODUCT_FREEZE"

    if r == "BLOCKED" and f in {"EXTERNAL", "TRANSPORT", "TEST_HARNESS"}:
        return "SUPERVISOR_RECOVER_OR_SWITCH_ELSE_FSM_BLOCKED"

    if r == "FAIL":
        return "FSM_FAIL_TO_VIRTUAL_REMATURE_REFREEZE"

    return "FSM_BLOCKED"

def acceptance_wait(*, expected=None, observation=None):
    return review_wait(expected=expected, observation=observation)

def codex_acceptance_requirements():
    return {
        "test_case_selected_by": "CODEX_AT_RUNTIME",
        "browser_skill_required": "playwright-native-ai-browser",
        "ad_hoc_browser_script_allowed": False,
        "gpt_preselects_test_case": False,
        "user_preselects_test_case": False,
        "product_plan_authority": "GPT",
        "acceptance_task_selection_authority": "CODEX",
    }
