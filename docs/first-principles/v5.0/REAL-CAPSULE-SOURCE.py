import math
from dataclasses import dataclass, replace
from enum import Enum
from typing import Optional, FrozenSet

class Phase(str, Enum):
    VIRTUAL = "虚"
    REAL = "实"

class Event(str, Enum):
    FREEZE_TO_REAL = "冻结转实"
    REAL_PASS = "现实通过"
    REAL_FAIL = "现实失败"

class Adapter(str, Enum):
    CODEX = "CODEX"
    PLAYWRIGHT = "PLAYWRIGHT"
    REASONIX = "REASONIX"
    LOCAL_FROZEN = "LOCAL_FROZEN"

ALLOWED_MODES = {
    Adapter.CODEX: frozenset({"CHAT"}),
    Adapter.PLAYWRIGHT: frozenset({"NATIVE_BROWSER"}),
    Adapter.REASONIX: frozenset({"UI_AGENT"}),
    Adapter.LOCAL_FROZEN: frozenset({"FROZEN_RUNNER"}),
}

class Blocked(Exception): pass

@dataclass(frozen=True)
class EngineState:
    page_name: str
    task_name: str
    generation: int
    attempt: int
    phase: Phase
    t_star_ms: float
    freeze_id: Optional[str] = None
    used_freezes: FrozenSet[str] = frozenset()
    real_adapter: Optional[Adapter] = None
    dispatch_mode: Optional[str] = None
    done: bool = False

@dataclass(frozen=True)
class VirtualMature:
    valid_defined: bool
    reality_facts_ready: bool
    mature_solution_selected: bool
    execution_chain_closed: bool
    external_dependencies_closed: bool
    proposed_t_star_ms: float
    freeze_id: str
    freeze_hash: str
    reread_hash: str
    real_capsule_self_contained: bool
    real_adapter: Adapter
    dispatch_mode: str
    time_contract_ready: bool
    provenance_scoped: bool
    remote_claim_requires_reread: bool
    real_task_phase: Phase

@dataclass(frozen=True)
class RealResult:
    verifier_pass: bool
    evidence_consistent: bool
    real_start_ms: Optional[float]
    real_end_ms: Optional[float]
    t_valid_real_ms: Optional[float]
    reality_delta: Optional[str] = None
    structural_failure: bool = False

def _require(cond, reason):
    if not cond: raise Blocked(reason)

def adapter_policy_pass(adapter, mode):
    return adapter in ALLOWED_MODES and mode in ALLOWED_MODES[adapter]

def format_ms(ms):
    _require(ms is not None and math.isfinite(ms) and ms > 0, "T_STAR_INVALID")
    total_ms = int(round(ms))
    minutes, rem = divmod(total_ms, 60000)
    seconds, millis = divmod(rem, 1000)
    return f"{minutes:02d}:{seconds:02d}.{millis:03d}"

def validate_state(s):
    _require(bool(s.page_name.strip()), "PAGE_NAME_MISSING")
    _require(bool(s.task_name.strip()), "TASK_NAME_MISSING")
    _require(s.generation >= 1, "GENERATION_INVALID")
    _require(1 <= s.attempt <= 6, "ATTEMPT_INVALID")
    _require(s.t_star_ms is not None and math.isfinite(s.t_star_ms) and s.t_star_ms > 0, "T_STAR_INVALID")
    if s.phase == Phase.VIRTUAL:
        _require(not s.done, "VIRTUAL_CANNOT_BE_DONE")
        _require(s.freeze_id is None, "VIRTUAL_MUST_NOT_HOLD_ACTIVE_FREEZE")
        _require(s.real_adapter is None and s.dispatch_mode is None, "VIRTUAL_MUST_NOT_HOLD_REAL_EXECUTOR")
    if s.phase == Phase.REAL:
        _require(bool(s.freeze_id), "REAL_WITHOUT_FREEZE")
        _require(s.real_adapter is not None, "REAL_ADAPTER_MISSING")
        _require(bool(s.dispatch_mode), "DISPATCH_MODE_MISSING")
        _require(adapter_policy_pass(s.real_adapter, s.dispatch_mode), "ADAPTER_MODE_ILLEGAL")
        if s.done: _require(s.freeze_id in s.used_freezes, "DONE_FREEZE_NOT_CONSUMED")
        else: _require(s.freeze_id not in s.used_freezes, "FREEZE_REUSED_BEFORE_REAL")

def render_locator(s):
    validate_state(s)
    return f"【{s.page_name}｜{s.task_name}｜{s.generation:02d}-{s.attempt:02d}｜{s.phase.value}】 极限锚{format_ms(s.t_star_ms)}"

def transition(s, event, payload):
    validate_state(s); _require(not s.done, "TASK_ALREADY_DONE")
    if event == Event.FREEZE_TO_REAL:
        _require(s.phase == Phase.VIRTUAL, "FREEZE_ONLY_FROM_VIRTUAL")
        v=payload; _require(isinstance(v, VirtualMature), "VIRTUAL_PAYLOAD_REQUIRED")
        _require(v.valid_defined,"VALID_NOT_DEFINED"); _require(v.reality_facts_ready,"REALITY_FACTS_NOT_READY")
        _require(v.mature_solution_selected,"MATURE_SOLUTION_NOT_SELECTED"); _require(v.execution_chain_closed,"EXECUTION_CHAIN_OPEN")
        _require(v.external_dependencies_closed,"EXTERNAL_DEPENDENCIES_OPEN")
        _require(v.proposed_t_star_ms is not None and math.isfinite(v.proposed_t_star_ms) and v.proposed_t_star_ms>0,"PROPOSED_T_STAR_INVALID")
        _require(bool(v.freeze_id),"FREEZE_ID_MISSING"); _require(v.freeze_id not in s.used_freezes,"FREEZE_ID_ALREADY_USED")
        _require(bool(v.freeze_hash),"FREEZE_HASH_MISSING"); _require(bool(v.reread_hash),"REREAD_HASH_MISSING")
        _require(v.freeze_hash==v.reread_hash,"FREEZE_REREAD_HASH_MISMATCH")
        _require(v.real_capsule_self_contained,"REAL_CAPSULE_NOT_SELF_CONTAINED")
        _require(adapter_policy_pass(v.real_adapter,v.dispatch_mode),"ADAPTER_MODE_ILLEGAL")
        _require(v.time_contract_ready,"TIME_CONTRACT_MISSING"); _require(v.provenance_scoped,"PROVENANCE_SCOPE_MISSING")
        _require(v.remote_claim_requires_reread,"REMOTE_REREAD_POLICY_MISSING"); _require(v.real_task_phase==Phase.REAL,"REAL_TASK_PHASE_NOT_REAL")
        out=replace(s,phase=Phase.REAL,t_star_ms=v.proposed_t_star_ms,freeze_id=v.freeze_id,real_adapter=v.real_adapter,dispatch_mode=v.dispatch_mode)
        validate_state(out); return out
    if event == Event.REAL_PASS:
        _require(s.phase==Phase.REAL,"REAL_PASS_ONLY_FROM_REAL")
        r=payload; _require(isinstance(r,RealResult),"REAL_RESULT_REQUIRED")
        _require(r.real_start_ms is not None,"REAL_START_MISSING"); _require(r.real_end_ms is not None,"REAL_END_MISSING")
        _require(r.t_valid_real_ms is not None,"T_VALID_REAL_MISSING"); _require(r.real_end_ms>=r.real_start_ms,"REAL_TIME_ORDER_INVALID")
        _require(r.t_valid_real_ms>=0,"T_VALID_REAL_INVALID"); _require(r.verifier_pass,"VERIFIER_FAIL")
        _require(r.evidence_consistent,"EVIDENCE_INCONSISTENT"); _require(r.t_valid_real_ms<=s.t_star_ms,"T_STAR_NOT_MET")
        out=replace(s,used_freezes=frozenset(set(s.used_freezes)|{s.freeze_id}),done=True); validate_state(out); return out
    if event == Event.REAL_FAIL:
        _require(s.phase==Phase.REAL,"REAL_FAIL_ONLY_FROM_REAL")
        r=payload; _require(isinstance(r,RealResult),"REAL_RESULT_REQUIRED"); _require(bool(r.reality_delta),"REALITY_DELTA_MISSING")
        new_used=frozenset(set(s.used_freezes)|{s.freeze_id}); change=r.structural_failure or s.attempt==6
        out=EngineState(s.page_name,s.task_name,s.generation+(1 if change else 0),1 if change else s.attempt+1,Phase.VIRTUAL,s.t_star_ms,None,new_used,None,None,False)
        validate_state(out); return out
    raise Blocked("EVENT_NOT_ALLOWED")

if __name__=="__main__":
    from itertools import product
    base=EngineState("整体闭环极限时间引擎 4.7版2","v5.0确定性状态机现实认证",5,1,Phase.VIRTUAL,194419.3759)
    good=VirtualMature(True,True,True,True,True,194419.3759,"ESTE-v5.0-0501-VIRTUAL-FREEZE-01","h","h",True,Adapter.CODEX,"CHAT",True,True,True,Phase.REAL)
    rr=RealResult(True,True,1000.0,2000.0,1000.0)
    real=transition(base,Event.FREEZE_TO_REAL,good)
    directed=0
    def block(fn):
        global directed
        try: fn()
        except Blocked: directed+=1; return
        raise AssertionError("expected BLOCK")
    def ok(fn,p=lambda x:True):
        global directed
        out=fn(); assert p(out); directed+=1; return out
    ok(lambda:transition(base,Event.FREEZE_TO_REAL,good),lambda s:s.phase==Phase.REAL)
    block(lambda:transition(base,Event.REAL_PASS,rr)); block(lambda:validate_state(replace(base,t_star_ms=0)))
    block(lambda:validate_state(replace(base,attempt=7))); block(lambda:transition(base,Event.FREEZE_TO_REAL,replace(good,reread_hash="x")))
    block(lambda:transition(base,Event.FREEZE_TO_REAL,replace(good,real_capsule_self_contained=False)))
    block(lambda:transition(base,Event.FREEZE_TO_REAL,replace(good,dispatch_mode="EXEC")))
    block(lambda:transition(base,Event.FREEZE_TO_REAL,replace(good,dispatch_mode="POWERSHELL")))
    block(lambda:transition(base,Event.FREEZE_TO_REAL,replace(good,dispatch_mode="SHELL")))
    block(lambda:transition(base,Event.FREEZE_TO_REAL,replace(good,real_task_phase=Phase.VIRTUAL)))
    block(lambda:transition(base,Event.FREEZE_TO_REAL,replace(good,time_contract_ready=False)))
    block(lambda:transition(base,Event.FREEZE_TO_REAL,replace(good,provenance_scoped=False)))
    block(lambda:transition(replace(base,used_freezes=frozenset({good.freeze_id})),Event.FREEZE_TO_REAL,good))
    block(lambda:transition(real,Event.REAL_PASS,replace(rr,real_start_ms=None))); block(lambda:transition(real,Event.REAL_PASS,replace(rr,real_end_ms=None)))
    block(lambda:transition(real,Event.REAL_PASS,replace(rr,t_valid_real_ms=None))); block(lambda:transition(real,Event.REAL_PASS,replace(rr,verifier_pass=False)))
    block(lambda:transition(real,Event.REAL_PASS,replace(rr,evidence_consistent=False))); block(lambda:transition(real,Event.REAL_PASS,replace(rr,t_valid_real_ms=200000.0)))
    done=ok(lambda:transition(real,Event.REAL_PASS,rr),lambda s:s.done); block(lambda:transition(done,Event.REAL_FAIL,replace(rr,reality_delta="x")))
    block(lambda:transition(real,Event.REAL_FAIL,replace(rr,reality_delta=None)))
    ok(lambda:transition(real,Event.REAL_FAIL,replace(rr,reality_delta="x")),lambda s:s.attempt==2)
    ok(lambda:transition(real,Event.REAL_FAIL,replace(rr,reality_delta="x",structural_failure=True)),lambda s:s.generation==6 and s.attempt==1)
    ok(lambda:transition(replace(real,attempt=6),Event.REAL_FAIL,replace(rr,reality_delta="x")),lambda s:s.generation==6 and s.attempt==1)
    assert render_locator(base)=="【整体闭环极限时间引擎 4.7版2｜v5.0确定性状态机现实认证｜05-01｜虚】 极限锚03:14.419"; directed+=1
    assert directed==26
    fn=fa=0
    for b in product([False,True],repeat=14):
        valid,reality,mature,chain,external,tstar,hashok,capsule,adapter,timec,prov,remote,realphase,unused=b
        fid="F"; st=base if unused else replace(base,used_freezes=frozenset({fid}))
        v=VirtualMature(valid,reality,mature,chain,external,1234.0 if tstar else 0.0,fid,"h","h" if hashok else "x",capsule,Adapter.CODEX,"CHAT" if adapter else "EXEC",timec,prov,remote,Phase.REAL if realphase else Phase.VIRTUAL)
        try: transition(st,Event.FREEZE_TO_REAL,v); allowed=True
        except Blocked: allowed=False
        assert allowed==all(b); fn+=1; fa+=int(allowed)
    pn=pa=0
    for b in product([False,True],repeat=7):
        start,end,tval,verify,evidence,order,within=b
        r=RealResult(verify,evidence,1000.0 if start else None,(2000.0 if order else 500.0) if end else None,(1000.0 if within else 200000.0) if tval else None)
        try: transition(real,Event.REAL_PASS,r); allowed=True
        except Blocked: allowed=False
        assert allowed==all(b); pn+=1; pa+=int(allowed)
    modes=["CHAT","EXEC","POWERSHELL","SHELL","NATIVE_BROWSER","UI_AGENT","FROZEN_RUNNER","UNKNOWN"]; an=0
    for a in Adapter:
        for m in modes: assert adapter_policy_pass(a,m)==(m in ALLOWED_MODES[a]); an+=1
    fail=0
    for n in range(1,7):
        rs=replace(real,attempt=n)
        for structural in [False,True]:
            out=transition(rs,Event.REAL_FAIL,replace(rr,reality_delta="d",structural_failure=structural))
            assert (out.generation,out.attempt)==((rs.generation+1,1) if (structural or n==6) else (rs.generation,n+1)); fail+=1
    det=0
    for sample in [(base,Event.FREEZE_TO_REAL,good),(real,Event.REAL_PASS,rr),(real,Event.REAL_FAIL,replace(rr,reality_delta="d")),(base,Event.FREEZE_TO_REAL,replace(good,dispatch_mode="EXEC")),(real,Event.REAL_PASS,replace(rr,t_valid_real_ms=200000.0))]:
        vals=[]
        for _ in range(5):
            try: vals.append(("OK",transition(*sample)))
            except Blocked as e: vals.append(("BLOCK",str(e)))
        assert len(set(map(str,vals)))==1; det+=1
    assert (fn,fa)==(16384,1) and (pn,pa)==(128,1) and an==32 and fail==12 and det==5
    assert directed+fn+pn+an+fail+det==16587
    print("STATE_MACHINE_RENDER="+render_locator(real))
    print("TOTAL=16587/16587 PASS")
