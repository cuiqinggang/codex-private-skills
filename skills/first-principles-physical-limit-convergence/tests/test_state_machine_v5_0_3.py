from dataclasses import replace
from itertools import product

from state_machine_v5_0_3 import (
    Phase, Event, Adapter, Blocked,
    EngineState, TimeEvent, ExecutionClosureEvidence, VirtualMature, RealResult,
    transition, render_locator, render_dispatch_header, render_time_control_snapshot,
    authorize_executable_step, validate_state, execution_closure_pass,
    virtual_complete_pass, UNIQUE_OBJECTIVE,
)

PAGE = "整体闭环极限时间引擎5.0.2版"
TASK = "v5.0.3连续时间状态虚拟成熟"
TL = "TL-v5.0.3-0001"
ORIGIN = "2026-09-26T23:50:00+08:00"

def good_e():
    return ExecutionClosureEvidence(
        True,True,True,True,True,True,True,True,True,True,
        "impl","fault","verify","manifest","materialize"
    )

def good_v(t_star=1500.0, event_at="2026-09-26T23:51:00+08:00", freeze_id="F1"):
    return VirtualMature(
        True,True,True,True,True,good_e(),True,"gpt",True,
        t_star,
        "PROGRAM_START",
        "VALID_OUTPUT_COMMITTED",
        "VIRTUAL_MIN_VALID_BENCHMARK",
        event_at,
        freeze_id,"h","h",True,Adapter.CODEX,"CHAT",
        True,True,True,Phase.REAL
    )

def good_pass(t_valid=500.0):
    return RealResult(
        verifier_pass=True,
        evidence_consistent=True,
        real_start_ms=1000.0,
        real_end_ms=1000.0+t_valid,
        t_valid_real_ms=t_valid,
        real_start_utc="2026-09-26T23:52:00+08:00",
        real_end_utc="2026-09-26T23:52:01+08:00",
    )

def good_fail(t_valid=700.0, structural=False):
    return RealResult(
        verifier_pass=False,
        evidence_consistent=True,
        real_start_ms=2000.0,
        real_end_ms=2000.0+t_valid,
        t_valid_real_ms=t_valid,
        real_start_utc="2026-09-26T23:53:00+08:00",
        real_end_utc="2026-09-26T23:53:01+08:00",
        reality_delta="TIME_ONLY",
        structural_failure=structural,
    )

def expect_block(fn, reason=None):
    try:
        fn()
    except Blocked as e:
        if reason is not None:
            assert str(e) == reason, (str(e), reason)
        return
    raise AssertionError("expected block")

# 1. New task has one continuous timeline and may be PENDING in early Virtual.
s0 = EngineState(PAGE,TASK,5,1,Phase.VIRTUAL,TL,ORIGIN)
validate_state(s0)
assert render_locator(s0) == f"【{PAGE}｜{TASK}｜05-01｜虚】 锚定物=T*=min(T_VALID)｜状态=PENDING｜当前T*=PENDING｜现实最优=PENDING"
assert s0.time_event_seq == 0 and s0.time_events == ()
assert s0.t_star_status == "PENDING"

# 2. Virtual maturity freezes the first active T* onto the same timeline.
v1 = good_v(1500.0, freeze_id="F1")
assert virtual_complete_pass(v1)
s1 = transition(s0, Event.FREEZE_TO_REAL, v1)
assert s1.timeline_id == TL
assert s1.time_origin_utc == ORIGIN
assert s1.time_event_seq == 1
assert [e.name for e in s1.time_events] == ["FREEZE_TO_REAL"]
assert s1.time_events[0].active_t_star_ms == 1500.0
assert s1.t_star_ms == 1500.0
assert s1.t_star_status == "VIRTUAL_FROZEN"

header = render_dispatch_header(s1)
for expected in [
    "ACTION=REAL_DISPATCH",
    "UNIQUE_ANCHOR=T*=min(T_VALID)",
    f"TIMELINE_ID={TL}",
    f"TIME_ORIGIN_UTC={ORIGIN}",
    "TIME_EVENT_SEQ=1",
    "ANCHOR_STATE=VIRTUAL_FROZEN",
    "ACTIVE_T_STAR_MS=1500.000000ms",
    "T_VALID_START=PROGRAM_START",
    "T_VALID_END=VALID_OUTPUT_COMMITTED",
    "T_STAR_SOURCE=VIRTUAL_MIN_VALID_BENCHMARK",
]:
    assert expected in header

# 3. Missing any frozen time-anchor component blocks Virtual -> Real.
for field,value,reason in [
    ("proposed_t_star_ms",0.0,"PROPOSED_T_STAR_INVALID"),
    ("t_valid_start","","T_VALID_START_MISSING"),
    ("t_valid_end","","T_VALID_END_MISSING"),
    ("t_star_source","","T_STAR_SOURCE_MISSING"),
    ("event_at_utc","","FREEZE_EVENT_UTC_MISSING"),
]:
    expect_block(lambda field=field,value=value: transition(s0,Event.FREEZE_TO_REAL,replace(v1,**{field:value})),reason)

# 4. REAL FAIL appends history, preserves timeline and previous certified best,
#    but clears only the active freeze anchor so stale T* cannot be reused.
s0_with_best = replace(s0,best_certified_t_valid_ms=900.0)
s1b = transition(s0_with_best,Event.FREEZE_TO_REAL,v1)
s2 = transition(s1b,Event.REAL_FAIL,good_fail())
assert s2.phase == Phase.VIRTUAL
assert s2.timeline_id == TL and s2.time_origin_utc == ORIGIN
assert s2.time_event_seq == 3
assert [e.name for e in s2.time_events] == ["FREEZE_TO_REAL","REAL_START","REAL_FAIL"]
assert s2.time_events[-1].t_valid_real_ms == 700.0
assert s2.best_certified_t_valid_ms == 900.0
assert s2.t_star_ms is None
assert s2.t_star_status == "PENDING"
assert s2.t_valid_start is None and s2.t_valid_end is None and s2.t_star_source is None
assert "状态=PENDING｜当前T*=PENDING" in render_locator(s2)

# 5. Second freeze continues the SAME timeline and appends a new active T*.
v2 = good_v(1200.0,event_at="2026-09-26T23:54:00+08:00",freeze_id="F2")
s3 = transition(s2,Event.FREEZE_TO_REAL,v2)
assert s3.timeline_id == TL and s3.time_origin_utc == ORIGIN
assert s3.time_event_seq == 4
assert [e.name for e in s3.time_events] == ["FREEZE_TO_REAL","REAL_START","REAL_FAIL","FREEZE_TO_REAL"]
assert [e.active_t_star_ms for e in s3.time_events if e.name=="FREEZE_TO_REAL"] == [1500.0,1200.0]
assert s3.t_star_ms == 1200.0
assert s3.t_star_status == "VIRTUAL_FROZEN"

# 6. REAL PASS appends start/pass and absorbs real T_VALID into certified best.
s4 = transition(s3,Event.REAL_PASS,good_pass(500.0))
assert s4.done is True
assert s4.timeline_id == TL and s4.time_origin_utc == ORIGIN
assert s4.time_event_seq == 6
assert [e.name for e in s4.time_events] == [
    "FREEZE_TO_REAL","REAL_START","REAL_FAIL","FREEZE_TO_REAL","REAL_START","REAL_PASS"
]
assert s4.time_events[-1].t_valid_real_ms == 500.0
assert s4.best_certified_t_valid_ms == 500.0
assert s4.t_star_status == "REAL_CERTIFIED"
assert s4.t_star_ms == 1200.0
assert "BEST_CERTIFIED_T_VALID_MS=500.000000ms" in render_dispatch_header(s4)

# 7. Certified best is min(previous,current), not reset by later state.
base_best = EngineState(PAGE,TASK,5,1,Phase.VIRTUAL,TL,ORIGIN,best_certified_t_valid_ms=400.0)
real_best = transition(base_best,Event.FREEZE_TO_REAL,good_v(1000.0,freeze_id="F3"))
done_best = transition(real_best,Event.REAL_PASS,good_pass(500.0))
assert done_best.best_certified_t_valid_ms == 400.0

# 8. REAL PASS uses the exact active frozen T*.
tight = transition(s0,Event.FREEZE_TO_REAL,good_v(499.0,freeze_id="F4"))
expect_block(lambda:transition(tight,Event.REAL_PASS,good_pass(500.0)),"T_STAR_NOT_MET")

# 9. UTC boundaries are mandatory for ledger continuity.
real_for_utc = transition(s0,Event.FREEZE_TO_REAL,good_v(1000.0,freeze_id="F5"))
expect_block(lambda:transition(real_for_utc,Event.REAL_PASS,replace(good_pass(),real_start_utc=None)),"REAL_START_UTC_MISSING")
expect_block(lambda:transition(real_for_utc,Event.REAL_PASS,replace(good_pass(),real_end_utc=None)),"REAL_END_UTC_MISSING")
expect_block(lambda:transition(real_for_utc,Event.REAL_FAIL,replace(good_fail(),real_start_utc=None)),"REAL_START_UTC_MISSING")
expect_block(lambda:transition(real_for_utc,Event.REAL_FAIL,replace(good_fail(),real_end_utc=None)),"REAL_END_UTC_MISSING")

# 10. Timeline identity/origin are mandatory and event ledger is append-only ordered.
expect_block(lambda:validate_state(replace(s0,timeline_id="")),"TIMELINE_ID_MISSING")
expect_block(lambda:validate_state(replace(s0,time_origin_utc="")),"TIME_ORIGIN_MISSING")
bad_event = TimeEvent(2,"X",Phase.VIRTUAL,"2026-09-26T23:51:00+08:00")
expect_block(lambda:validate_state(replace(s0,time_event_seq=1,time_events=(bad_event,))),"TIME_EVENT_ORDER_INVALID")
expect_block(lambda:validate_state(replace(s0,time_event_seq=2,time_events=(TimeEvent(1,"X",Phase.VIRTUAL,"2026-09-26T23:51:00+08:00"),))),"TIME_EVENT_SEQ_MISMATCH")

# 11. Unique anchor is mandatory in every state and every executable step.
assert s0.anchor_metric == UNIQUE_OBJECTIVE
pending_snapshot = authorize_executable_step(s0,"VIRTUAL_ANALYZE")
for expected in [
    "ACTION=VIRTUAL_ANALYZE",
    "UNIQUE_ANCHOR=T*=min(T_VALID)",
    "ANCHOR_STATE=PENDING",
    "ACTIVE_T_STAR_MS=PENDING",
    "BEST_CERTIFIED_T_VALID_MS=PENDING",
]:
    assert expected in pending_snapshot
frozen_snapshot = authorize_executable_step(s1,"VIRTUAL_FREEZE_READY")
assert "ANCHOR_STATE=VIRTUAL_FROZEN" in frozen_snapshot
assert "ACTIVE_T_STAR_MS=1500.000000ms" in frozen_snapshot
certified_snapshot = authorize_executable_step(s4,"FINAL_REPORT")
assert "ANCHOR_STATE=REAL_CERTIFIED" in certified_snapshot
assert "BEST_CERTIFIED_T_VALID_MS=500.000000ms" in certified_snapshot
expect_block(lambda:validate_state(replace(s0,anchor_metric="OTHER")),"UNIQUE_ANCHOR_INVALID")
expect_block(lambda:authorize_executable_step(s0,""),"ACTION_NAME_MISSING")

# 12. Exhaustive time-anchor presence matrix: only all 5 present can enter REAL.
cases=allowed=0
for bits in product([False,True],repeat=5):
    tstar,start,end,source,event_at=bits
    v=replace(
        v1,
        proposed_t_star_ms=1000.0 if tstar else 0.0,
        t_valid_start="S" if start else "",
        t_valid_end="E" if end else "",
        t_star_source="SRC" if source else "",
        event_at_utc="2026-09-26T23:51:00+08:00" if event_at else "",
        freeze_id=f"F-{bits}"
    )
    try:
        transition(s0,Event.FREEZE_TO_REAL,v)
        ok=True
    except Blocked:
        ok=False
    assert ok == all(bits), (bits,ok)
    cases += 1
    allowed += int(ok)
assert cases==32 and allowed==1

# 13. Failure loop keeps a single ledger through all legal retries.
loop = EngineState(PAGE,TASK,7,1,Phase.VIRTUAL,"TL-LOOP",ORIGIN)
expected_seq=0
for attempt in range(1,6):
    real = transition(loop,Event.FREEZE_TO_REAL,good_v(1000.0-attempt,freeze_id=f"LF{attempt}",event_at=f"2026-09-27T00:0{attempt}:00+08:00"))
    expected_seq += 1
    assert real.time_event_seq == expected_seq
    loop = transition(real,Event.REAL_FAIL,good_fail())
    expected_seq += 2
    assert loop.time_event_seq == expected_seq
    assert loop.timeline_id=="TL-LOOP" and loop.time_origin_utc==ORIGIN
    assert loop.attempt==attempt+1
assert expected_seq==15
assert len(loop.time_events)==15

print("V5_0_3_CONTINUOUS_TIME_LEDGER=PASS")
print("ANCHOR_MATRIX=32/32 PASS; ALLOW=1")
print("CONTINUOUS_RETRY_EVENTS=15/15 PRESERVED")
print("FINAL_CHAIN_EVENTS="+",".join(e.name for e in s4.time_events))
print("FINAL_BEST_CERTIFIED_T_VALID_MS=500.000000")
