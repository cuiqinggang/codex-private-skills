import os
import sys
from dataclasses import replace

HERE = os.path.dirname(__file__)
RUNTIME = os.path.abspath(os.path.join(HERE, "..", "runtime"))
if RUNTIME not in sys.path:
    sys.path.insert(0, RUNTIME)

from state_machine_v5_0_3 import (
    Phase, Event, Adapter, EngineState, ExecutionClosureEvidence,
    VirtualMature, RealResult, transition as base_transition
)
from state_machine_v5_0_5_overlay import (
    SegmentTimeAnchor, TimeMasterContext, transition, validate_source_policy, Blocked
)

PAGE="整体闭环极限时间引擎5.0.2版"
TASK="v5.0.5状态机保持与时间总控"
ORIGIN="2026-09-27T01:34:00+08:00"

def evidence():
    return ExecutionClosureEvidence(
        True,True,True,True,True,True,True,True,True,
        "a","b","c","d"
    )

def good_v(fid="F1"):
    return VirtualMature(
        True,True,True,True,True,True,True,
        1.0,0.0,1.0,"VIRTUAL_LOOP_T_STAR",
        fid,"h","h",True,Adapter.CODEX,"CHAT",
        True,True,True,Phase.REAL,
        evidence(),
        "2026-09-27T01:35:00+08:00"
    )

def tm(state="VIRTUAL_FROZEN", close=True):
    return TimeMasterContext(
        "T*=min(T_VALID)",
        "T_CLOSED_LOOP_VALID",
        10.0,
        state,
        close,
        (SegmentTimeAnchor("virtual",5.0,"VIRTUAL_FROZEN",1.0),),
        "AVAILABLE",
        "REMOTE_SHARED_REPO_DIRECT",
        False
    )

# 原状态机动作结果必须完全保持。
s0=EngineState(PAGE,TASK,1,1,Phase.VIRTUAL,"TL",ORIGIN)
v=good_v("F1")
assert transition(s0,Event.FREEZE_TO_REAL,v,tm()) == base_transition(s0,Event.FREEZE_TO_REAL,v)

# 正常路径不得使用下载包/本地副本。
for mode in ("DOWNLOAD_PACKAGE","LOCAL_COPY","INLINE_COPY"):
    bad=replace(tm(),source_mode=mode)
    try:
        transition(s0,Event.FREEZE_TO_REAL,v,bad)
        raise AssertionError(mode)
    except Blocked as e:
        assert "REMOTE_SOURCE_PRIMARY_PATH_VIOLATION" in str(e)

# REAL 中共同私库不可达只能 STOP/回 GPT，不能现场切备用源。
real=base_transition(s0,Event.FREEZE_TO_REAL,v)
for status in ("NETWORK_UNAVAILABLE","AUTH_UNAVAILABLE","REPOSITORY_UNAVAILABLE"):
    bad=replace(tm(),remote_status=status)
    try:
        transition(real,Event.REAL_FAIL,RealResult(False,False,1.0,2.0,1.0,"a","b","REMOTE_DOWN",False),bad)
        raise AssertionError(status)
    except Blocked as e:
        assert "REMOTE_REPO_UNAVAILABLE_RETURN_TO_GPT" in str(e)

# N/A/NULL/MISSING 永久非法。
for token in ("N/A","NA","NULL","MISSING","空值",""):
    bad=replace(tm(),anchor_state=token)
    try:
        transition(s0,Event.FREEZE_TO_REAL,v,bad)
        raise AssertionError(token)
    except Blocked:
        pass

print("V5_0_5_STATE_MACHINE_PRESERVATION=PASS")
print("REMOTE_SHARED_REPO_PRIMARY_PATH=PASS")
print("TIME_ANCHOR_NA_ILLEGAL=PASS")
