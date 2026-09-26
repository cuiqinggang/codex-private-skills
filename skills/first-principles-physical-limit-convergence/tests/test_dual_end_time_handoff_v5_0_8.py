import os,sys,random
HERE=os.path.dirname(__file__)
RUNTIME=os.path.abspath(os.path.join(HERE,"..","runtime"))
if RUNTIME not in sys.path:
    sys.path.insert(0,RUNTIME)

from dual_end_time_handoff_v5_0_8 import TimeEnvelope, validate_envelope, DualEndTimeHandoffViolation

def expect_block(fn):
    try:
        fn()
    except DualEndTimeHandoffViolation:
        return
    raise AssertionError("expected block")

dispatch=TimeEnvelope(
    "【页｜任务｜01-01｜实】","TL-508",
    1000.0,0.0,0.083146,"DISPATCH"
)
validate_envelope(dispatch)

# GPT -> Codex: 5 required visible fields => 32 combinations; only all-present may pass.
fields=("locator","timeline_id","t_closed_loop_elapsed_ms","t_exchange_elapsed_ms","t_star_ms")
allowed=0
for bits in range(1<<len(fields)):
    kw=dispatch.__dict__.copy()
    for i,k in enumerate(fields):
        if not bits&(1<<i):
            kw[k]="" if k in {"locator","timeline_id"} else None
    try:
        validate_envelope(TimeEnvelope(**kw))
        allowed+=1
    except Exception:
        pass
assert allowed==1

# Codex -> GPT FAIL/BLOCKED must still contain numeric time.
for result in ("FAIL","BLOCKED"):
    ret=TimeEnvelope(
        dispatch.locator,dispatch.timeline_id,
        1125.0,125.0,dispatch.t_star_ms,result,
        None,0.0,"NOT_STARTED"
    )
    validate_envelope(
        ret,
        previous_closed_loop_ms=dispatch.t_closed_loop_elapsed_ms,
        expected_timeline_id=dispatch.timeline_id,
        inherited_t_star_ms=dispatch.t_star_ms
    )

# PASS requires real numeric T.
passed=TimeEnvelope(
    dispatch.locator,dispatch.timeline_id,
    1100.0,100.0,dispatch.t_star_ms,"PASS",
    0.071,0.071,"STARTED"
)
validate_envelope(
    passed,
    previous_closed_loop_ms=dispatch.t_closed_loop_elapsed_ms,
    expected_timeline_id=dispatch.timeline_id,
    inherited_t_star_ms=dispatch.t_star_ms
)

# 20,000 full round trips; timeline and cumulative time must never break.
for n in range(20000):
    tl=f"TL-{n}"
    base=random.uniform(1.0,100000.0)
    star=random.uniform(0.001,1000.0)
    d=TimeEnvelope("【页｜任务｜01｜实】",tl,base,0.0,star,"DISPATCH")
    validate_envelope(d)
    attempts=random.randint(1,5)
    previous=base
    for i in range(attempts):
        elapsed=random.uniform(0.001,1000.0)
        current=previous+elapsed
        if i < attempts-1:
            r=TimeEnvelope(d.locator,tl,current,elapsed,star,"FAIL",None,0.0,"NOT_STARTED")
        else:
            real=random.uniform(0.0,star)
            r=TimeEnvelope(d.locator,tl,current,elapsed,star,"PASS",real,real,"STARTED")
        validate_envelope(r,previous,tl,star)
        previous=current

print("GPT_TO_CODEX_DISPATCH_MATRIX=32/32 PASS; ALLOW=1")
print("CODEX_TO_GPT_RETURN_RULES=PASS")
print("ROUND_TRIP_20000=PASS")
