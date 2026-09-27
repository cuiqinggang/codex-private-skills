import re

class FinalResponseGateViolation(Exception):
    pass

REQUIRED_MARKERS = (
    "TIMELINE_ID=",
    "TIME_ORIGIN_UTC=",
    "DISPATCH_UTC=",
    "FREEZE_ID=",
)

def _require(cond, reason):
    if not cond:
        raise FinalResponseGateViolation(reason)

def requires_real_dispatch(virtual_mature, solution_frozen, real_started):
    return bool(virtual_mature and solution_frozen and not real_started)

def validate_final_response(
    text,
    *,
    virtual_mature,
    solution_frozen,
    real_started,
    timeline_established,
):
    if not requires_real_dispatch(virtual_mature, solution_frozen, real_started):
        return "NO_DISPATCH_REQUIRED"

    _require(timeline_established, "TIMELINE_NOT_ESTABLISHED_DO_NOT_FAKE_TIME")
    _require(bool(text and text.strip()), "FINAL_RESPONSE_EMPTY")
    _require(re.search(r"【[^\n｜]+｜[^\n｜]+｜[^\n｜]+｜实】", text) is not None,
             "REAL_LOCATOR_MISSING")
    _require(re.search(
        r"【时间锚｜整体已用=\d+(?:\.\d+)?ms｜本次已用=\d+(?:\.\d+)?ms｜T\*=\d+(?:\.\d+)?ms】",
        text
    ) is not None, "NUMERIC_TIME_ENVELOPE_MISSING")

    for marker in REQUIRED_MARKERS:
        _require(marker in text, marker.rstrip("=") + "_MISSING")

    _require(
        ("PASS" in text and "FAIL" in text and "BLOCKED" in text)
        or "PASS / FAIL / BLOCKED" in text
        or "PASS/FAIL/BLOCKED" in text,
        "RETURN_RESULT_CONTRACT_MISSING"
    )
    _require("RETURN_TO_GPT=YES" in text, "RETURN_TO_GPT_REQUIRED")
    return "REAL_DISPATCH_VALID"
