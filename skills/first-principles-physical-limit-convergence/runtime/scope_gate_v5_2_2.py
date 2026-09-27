import importlib.util
from pathlib import Path
import re

class ScopeGateViolation(Exception):
    pass

_REAL_LOCATOR_RE = re.compile(r"【[^\n｜]+｜[^\n｜]+｜(?:0[1-6]|[1-6])｜实】")

def _require(cond, reason):
    if not cond:
        raise ScopeGateViolation(reason)

def _load_renderer():
    here = Path(__file__).resolve().parent
    renderer_path = here / "production_handoff_v5_2_0.py"
    _require(renderer_path.exists(), "PRODUCTION_RENDERER_NOT_FOUND")
    spec = importlib.util.spec_from_file_location("production_handoff_v5_2_0", renderer_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def is_real_scope_output(text: str) -> bool:
    return bool(text and _REAL_LOCATOR_RE.search(text))

def enforce_in_scope_final_output(text: str) -> str:
    """
    Skill-wide final-output gate.

    Any user-visible output produced under this skill that contains a REAL locator
    is a Reality Dispatch candidate, regardless of business/page/task name.
    It must therefore satisfy the same complete production dispatch contract.
    """
    _require(bool(text and text.strip()), "FINAL_OUTPUT_EMPTY")

    if not is_real_scope_output(text):
        return "NO_REAL_DISPATCH_IN_OUTPUT"

    renderer = _load_renderer()
    try:
        renderer.validate_rendered_dispatch(text)
    except Exception as exc:
        raise ScopeGateViolation("IN_SCOPE_REAL_OUTPUT_INVALID:" + str(exc)) from exc

    _require("\n\n执行：\n" in text, "EXECUTION_BODY_MISSING")
    body = text.split("\n\n执行：\n", 1)[1].split("\n\n返回：", 1)[0].strip()
    _require(bool(body), "EXECUTION_BODY_EMPTY")

    _require("RESULT=PASS|FAIL|BLOCKED" in text, "RETURN_RESULT_CONTRACT_MISSING")
    _require("RETURN_TO_GPT=YES" in text, "RETURN_TO_GPT_MISSING")
    _require("NO_FINAL_VALID_DONE=YES" in text, "FINAL_OWNERSHIP_MISSING")

    return "IN_SCOPE_REAL_DISPATCH_VALID"

def build_in_scope_real_dispatch(**kwargs):
    """
    The only skill-wide production builder for business Reality Dispatches.
    Business/page/task names are data, not special cases.
    """
    renderer = _load_renderer()
    out = renderer.build_real_dispatch(**kwargs)
    enforce_in_scope_final_output(out.text)
    return out
