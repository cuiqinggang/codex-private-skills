from state_machine import (
    Phase, Event, Adapter, Blocked, EngineState, VirtualMature, RealResult,
    transition, render_locator, validate_state, adapter_policy_pass, ALLOWED_MODES
)
from dataclasses import replace
from itertools import product

base = EngineState("整体闭环极限时间引擎 4.7版2","v5.0确定性状态机虚拟成熟",5,1,Phase.VIRTUAL,194419.3759)
good_v = VirtualMature(True,True,True,True,True,194419.3759,"ESTE-v5.0-0501-VIRTUAL-FREEZE-01","h","h",True,Adapter.CODEX,"CHAT",True,True,True,Phase.REAL)
good_real = RealResult(True,True,1000.0,2000.0,1000.0)

directed = 0
def expect_block(fn, reason=None):
    global directed
    try:
        fn()
    except Blocked as e:
        if reason is not None: assert str(e) == reason, (str(e), reason)
        directed += 1
        return
    raise AssertionError("expected block")
def expect_pass(fn, predicate=lambda x: True):
    global directed
    out=fn(); assert predicate(out); directed += 1; return out

real=expect_pass(lambda:transition(base,Event.FREEZE_TO_REAL,good_v),lambda s:s.phase==Phase.REAL and not s.done)
expect_block(lambda:transition(base,Event.REAL_PASS,good_real),"REAL_PASS_ONLY_FROM_REAL")
expect_block(lambda:validate_state(replace(base,t_star_ms=0)),"T_STAR_INVALID")
expect_block(lambda:validate_state(replace(base,attempt=7)),"ATTEMPT_INVALID")
expect_block(lambda:transition(base,Event.FREEZE_TO_REAL,replace(good_v,reread_hash="x")),"FREEZE_REREAD_HASH_MISMATCH")
expect_block(lambda:transition(base,Event.FREEZE_TO_REAL,replace(good_v,real_capsule_self_contained=False)),"REAL_CAPSULE_NOT_SELF_CONTAINED")
expect_block(lambda:transition(base,Event.FREEZE_TO_REAL,replace(good_v,dispatch_mode="EXEC")),"ADAPTER_MODE_ILLEGAL")
expect_block(lambda:transition(base,Event.FREEZE_TO_REAL,replace(good_v,dispatch_mode="POWERSHELL")),"ADAPTER_MODE_ILLEGAL")
expect_block(lambda:transition(base,Event.FREEZE_TO_REAL,replace(good_v,dispatch_mode="SHELL")),"ADAPTER_MODE_ILLEGAL")
expect_block(lambda:transition(base,Event.FREEZE_TO_REAL,replace(good_v,real_task_phase=Phase.VIRTUAL)),"REAL_TASK_PHASE_NOT_REAL")
expect_block(lambda:transition(base,Event.FREEZE_TO_REAL,replace(good_v,time_contract_ready=False)),"TIME_CONTRACT_MISSING")
expect_block(lambda:transition(base,Event.FREEZE_TO_REAL,replace(good_v,provenance_scoped=False)),"PROVENANCE_SCOPE_MISSING")
expect_block(lambda:transition(replace(base,used_freezes=frozenset({good_v.freeze_id})),Event.FREEZE_TO_REAL,good_v),"FREEZE_ID_ALREADY_USED")
expect_block(lambda:transition(real,Event.REAL_PASS,replace(good_real,real_start_ms=None)),"REAL_START_MISSING")
expect_block(lambda:transition(real,Event.REAL_PASS,replace(good_real,real_end_ms=None)),"REAL_END_MISSING")
expect_block(lambda:transition(real,Event.REAL_PASS,replace(good_real,t_valid_real_ms=None)),"T_VALID_REAL_MISSING")
expect_block(lambda:transition(real,Event.REAL_PASS,replace(good_real,verifier_pass=False)),"VERIFIER_FAIL")
expect_block(lambda:transition(real,Event.REAL_PASS,replace(good_real,evidence_consistent=False)),"EVIDENCE_INCONSISTENT")
expect_block(lambda:transition(real,Event.REAL_PASS,replace(good_real,t_valid_real_ms=200000.0)),"T_STAR_NOT_MET")
final=expect_pass(lambda:transition(real,Event.REAL_PASS,good_real),lambda s:s.phase==Phase.REAL and s.done)
expect_block(lambda:transition(final,Event.REAL_FAIL,replace(good_real,reality_delta="x")),"TASK_ALREADY_DONE")
expect_block(lambda:transition(real,Event.REAL_FAIL,replace(good_real,reality_delta=None)),"REALITY_DELTA_MISSING")
expect_pass(lambda:transition(real,Event.REAL_FAIL,replace(good_real,reality_delta="x")),lambda s:s.phase==Phase.VIRTUAL and s.generation==5 and s.attempt==2 and s.freeze_id is None)
expect_pass(lambda:transition(real,Event.REAL_FAIL,replace(good_real,reality_delta="x",structural_failure=True)),lambda s:s.phase==Phase.VIRTUAL and s.generation==6 and s.attempt==1)
expect_pass(lambda:transition(replace(real,attempt=6),Event.REAL_FAIL,replace(good_real,reality_delta="x")),lambda s:s.generation==6 and s.attempt==1)
assert render_locator(base)=="【整体闭环极限时间引擎 4.7版2｜v5.0确定性状态机虚拟成熟｜05-01｜虚】 极限锚03:14.419"
directed += 1

freeze_cases=freeze_allowed=0
for bits in product([False,True],repeat=14):
    (valid,reality,mature,chain,external,tstar_valid,hashmatch,selfcontained,adapterok,timecontract,provenance,remote_policy,phase_real,freeze_unused)=bits
    fid="F"
    state=base if freeze_unused else replace(base,used_freezes=frozenset({fid}))
    vm=VirtualMature(valid,reality,mature,chain,external,1234.0 if tstar_valid else 0.0,fid,"h","h" if hashmatch else "x",selfcontained,Adapter.CODEX,"CHAT" if adapterok else "EXEC",timecontract,provenance,remote_policy,Phase.REAL if phase_real else Phase.VIRTUAL)
    expected=all(bits)
    try: transition(state,Event.FREEZE_TO_REAL,vm); allowed=True
    except Blocked: allowed=False
    assert allowed==expected,(bits,allowed,expected)
    freeze_cases += 1; freeze_allowed += int(allowed)

real_cases=real_allowed=0
for bits in product([False,True],repeat=7):
    start_ok,end_ok,tval_ok,verifier,evidence,timeorder,within=bits
    rr=RealResult(verifier,evidence,1000.0 if start_ok else None,(2000.0 if timeorder else 500.0) if end_ok else None,(1000.0 if within else 200000.0) if tval_ok else None)
    expected=all(bits)
    try: transition(real,Event.REAL_PASS,rr); allowed=True
    except Blocked: allowed=False
    assert allowed==expected,(bits,allowed,expected)
    real_cases += 1; real_allowed += int(allowed)

modes=["CHAT","EXEC","POWERSHELL","SHELL","NATIVE_BROWSER","UI_AGENT","FROZEN_RUNNER","UNKNOWN"]
adapter_cases=0
for adapter in list(Adapter):
    for mode in modes:
        assert adapter_policy_pass(adapter,mode)==(mode in ALLOWED_MODES[adapter]); adapter_cases += 1

failure_cases=0
for attempt in range(1,7):
    rs=replace(real,attempt=attempt)
    for structural in [False,True]:
        out=transition(rs,Event.REAL_FAIL,replace(good_real,reality_delta="delta",structural_failure=structural))
        if structural or attempt==6: assert out.generation==rs.generation+1 and out.attempt==1
        else: assert out.generation==rs.generation and out.attempt==attempt+1
        assert out.phase==Phase.VIRTUAL and out.freeze_id is None and rs.freeze_id in out.used_freezes
        failure_cases += 1

determinism_cases=0
samples=[
(base,Event.FREEZE_TO_REAL,good_v),
(real,Event.REAL_PASS,good_real),
(real,Event.REAL_FAIL,replace(good_real,reality_delta="delta")),
(base,Event.FREEZE_TO_REAL,replace(good_v,dispatch_mode="EXEC")),
(real,Event.REAL_PASS,replace(good_real,t_valid_real_ms=200000.0))]
for sample in samples:
    outcomes=[]
    for _ in range(5):
        try: outcomes.append(("OK",transition(*sample)))
        except Blocked as e: outcomes.append(("BLOCK",str(e)))
    assert all(item==outcomes[0] for item in outcomes); determinism_cases += 1

total=directed+freeze_cases+real_cases+adapter_cases+failure_cases+determinism_cases
assert directed==26
assert freeze_cases==16384 and freeze_allowed==1
assert real_cases==128 and real_allowed==1
assert adapter_cases==32
assert failure_cases==12
assert determinism_cases==5
assert total==16587
print("TOTAL=16587/16587 PASS")
