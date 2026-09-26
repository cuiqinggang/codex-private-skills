import os, sys, math
HERE=os.path.dirname(__file__)
RUNTIME=os.path.abspath(os.path.join(HERE,"..","runtime"))
if RUNTIME not in sys.path:
    sys.path.insert(0,RUNTIME)

from state_machine_v5_0_7_overlay import (
    NumericTimeAnchor,
    validate_numeric_time_anchor,
    validate_dispatch_visible_snapshot,
    render_numeric_time_tag,
    NumericTimeAnchorViolation,
)

good=NumericTimeAnchor(1000.0,700.0,528.036666)
validate_numeric_time_anchor(good)

snapshot={
    "UNIQUE_OBJECTIVE":"T*=min(T_VALID)",
    "TOP_LEVEL_T_VALID":"T_CLOSED_LOOP_VALID",
    "T_CLOSED_LOOP_ELAPSED_MS":1000.0,
    "T_STAGE_ELAPSED_MS":700.0,
    "T_STAGE_STAR_MS":528.036666,
}
tag=render_numeric_time_tag(snapshot)
assert "闭环已用=1000.000ms" in tag
assert "本段已用=700.000ms" in tag
assert "T*=528.036666ms" in tag
assert "SOLVING" not in tag

# 3 required numeric fields: only all-present combination may pass.
required=("T_CLOSED_LOOP_ELAPSED_MS","T_STAGE_ELAPSED_MS","T_STAGE_STAR_MS")
allowed=0
for bits in range(1<<3):
    d=dict(snapshot)
    for i,k in enumerate(required):
        if not (bits&(1<<i)):
            d.pop(k)
    try:
        validate_dispatch_visible_snapshot(d)
        allowed+=1
    except NumericTimeAnchorViolation:
        pass
assert allowed==1

for key in required:
    for bad in ("N/A","NA","NULL","MISSING","",None,float("inf"),float("nan"),-1.0):
        d=dict(snapshot)
        d[key]=bad
        try:
            validate_dispatch_visible_snapshot(d)
            raise AssertionError((key,bad))
        except NumericTimeAnchorViolation:
            pass

print("V5_0_7_NUMERIC_TIME_ANCHOR=PASS")
print("PRESENCE_MATRIX=8/8 PASS; ALLOW=1")
print("ILLEGAL_VALUES=27/27 BLOCKED")
