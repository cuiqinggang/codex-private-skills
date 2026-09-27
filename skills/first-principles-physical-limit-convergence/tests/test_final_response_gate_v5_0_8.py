import os, sys

HERE=os.path.dirname(__file__)
RUNTIME=os.path.abspath(os.path.join(HERE,"..","runtime"))
if RUNTIME not in sys.path:
    sys.path.insert(0,RUNTIME)

from final_response_gate_v5_0_8 import (
    validate_final_response,
    FinalResponseGateViolation,
)

def must_block(text, **kw):
    try:
        validate_final_response(text, **kw)
    except FinalResponseGateViolation:
        return
    raise AssertionError("expected block")

state=dict(
    virtual_mature=True,
    solution_frozen=True,
    real_started=False,
    timeline_established=True,
)

# Reality incident reproduced from DSE v1.0.3:
# It has a REAL locator and content, but no numeric time envelope/timeline/origin/dispatch timestamp.
dse_failed = """【决策系统引擎1｜DSE v1.0.3轻量版首次现实认证｜06｜实】
DSE_VERSION=v1.0.3
FREEZE_ID=DSE-v1.0.3-LIGHTWEIGHT-VIRTUAL-FREEZE-R1
VIRTUAL_MATURE=YES
SOLUTION_FROZEN=YES
REAL_STARTED=NO
RETURN_TO_GPT=NO
"""
must_block(dse_failed, **state)

# Missing auditable timeline must block rather than invent time.
must_block(
    "【页｜任务｜01｜实】\n【时间锚｜整体已用=1.000ms｜本次已用=0.000ms｜T*=1.000ms】",
    virtual_mature=True,
    solution_frozen=True,
    real_started=False,
    timeline_established=False,
)

good = """【决策系统引擎1｜DSE v1.0.3轻量版首次现实认证｜06｜实】
【时间锚｜整体已用=1234.000ms｜本次已用=0.000ms｜T*=0.001210ms】
TIMELINE_ID=DSE-TL-001
TIME_ORIGIN_UTC=2026-09-27T00:00:00+00:00
DISPATCH_UTC=2026-09-27T00:00:01+00:00
FREEZE_ID=DSE-v1.0.3-LIGHTWEIGHT-VIRTUAL-FREEZE-R1
PASS / FAIL / BLOCKED 均返回同一 Timeline。
RETURN_TO_GPT=YES
"""
assert validate_final_response(good, **state) == "REAL_DISPATCH_VALID"

assert validate_final_response(
    "ordinary final answer",
    virtual_mature=False,
    solution_frozen=False,
    real_started=False,
    timeline_established=False,
) == "NO_DISPATCH_REQUIRED"

print("DSE_FAILED_REAL_RESPONSE_REJECTED=PASS")
print("MISSING_TIMELINE_REJECTED=PASS")
print("COMPLETE_REAL_DISPATCH_ACCEPTED=PASS")
