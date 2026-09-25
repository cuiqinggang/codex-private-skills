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

class Blocked(Exception):
    pass

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

def _require(cond: bool, reason: str):
    if not cond:
        raise Blocked(reason)

def adapter_policy_pass(adapter: Adapter, mode: str) -> bool:
    return adapter in ALLOWED_MODES and mode in ALLOWED_MODES[adapter]

def format_ms(ms: float) -> str:
    _require(ms is not None and math.isfinite(ms) and ms > 0, "T_STAR_INVALID")
    total_ms = int(round(ms))
    minutes, rem = divmod(total_ms, 60000)
    seconds, millis = divmod(rem, 1000)
    return f"{minutes:02d}:{seconds:02d}.{millis:03d}"

def validate_state(s: EngineState):
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
        if s.done:
            _require(s.freeze_id in s.used_freezes, "DONE_FREEZE_NOT_CONSUMED")
        else:
            _require(s.freeze_id not in s.used_freezes, "FREEZE_REUSED_BEFORE_REAL")

def render_locator(s: EngineState) -> str:
    validate_state(s)
    return f"【{s.page_name}｜{s.task_name}｜{s.generation:02d}-{s.attempt:02d}｜{s.phase.value}】 极限锚{format_ms(s.t_star_ms)}"

def transition(s: EngineState, event: Event, payload):
    validate_state(s)
    _require(not s.done, "TASK_ALREADY_DONE")

    if event == Event.FREEZE_TO_REAL:
        _require(s.phase == Phase.VIRTUAL, "FREEZE_ONLY_FROM_VIRTUAL")
        v = payload
        _require(isinstance(v, VirtualMature), "VIRTUAL_PAYLOAD_REQUIRED")
        _require(v.valid_defined, "VALID_NOT_DEFINED")
        _require(v.reality_facts_ready, "REALITY_FACTS_NOT_READY")
        _require(v.mature_solution_selected, "MATURE_SOLUTION_NOT_SELECTED")
        _require(v.execution_chain_closed, "EXECUTION_CHAIN_OPEN")
        _require(v.external_dependencies_closed, "EXTERNAL_DEPENDENCIES_OPEN")
        _require(v.proposed_t_star_ms is not None and math.isfinite(v.proposed_t_star_ms) and v.proposed_t_star_ms > 0, "PROPOSED_T_STAR_INVALID")
        _require(bool(v.freeze_id), "FREEZE_ID_MISSING")
        _require(v.freeze_id not in s.used_freezes, "FREEZE_ID_ALREADY_USED")
        _require(bool(v.freeze_hash), "FREEZE_HASH_MISSING")
        _require(bool(v.reread_hash), "REREAD_HASH_MISSING")
        _require(v.freeze_hash == v.reread_hash, "FREEZE_REREAD_HASH_MISMATCH")
        _require(v.real_capsule_self_contained, "REAL_CAPSULE_NOT_SELF_CONTAINED")
        _require(adapter_policy_pass(v.real_adapter, v.dispatch_mode), "ADAPTER_MODE_ILLEGAL")
        _require(v.time_contract_ready, "TIME_CONTRACT_MISSING")
        _require(v.provenance_scoped, "PROVENANCE_SCOPE_MISSING")
        _require(v.remote_claim_requires_reread, "REMOTE_REREAD_POLICY_MISSING")
        _require(v.real_task_phase == Phase.REAL, "REAL_TASK_PHASE_NOT_REAL")
        out = replace(
            s,
            phase=Phase.REAL,
            t_star_ms=v.proposed_t_star_ms,
            freeze_id=v.freeze_id,
            real_adapter=v.real_adapter,
            dispatch_mode=v.dispatch_mode,
        )
        validate_state(out)
        return out

    if event == Event.REAL_PASS:
        _require(s.phase == Phase.REAL, "REAL_PASS_ONLY_FROM_REAL")
        r = payload
        _require(isinstance(r, RealResult), "REAL_RESULT_REQUIRED")
        _require(r.real_start_ms is not None, "REAL_START_MISSING")
        _require(r.real_end_ms is not None, "REAL_END_MISSING")
        _require(r.t_valid_real_ms is not None, "T_VALID_REAL_MISSING")
        _require(r.real_end_ms >= r.real_start_ms, "REAL_TIME_ORDER_INVALID")
        _require(r.t_valid_real_ms >= 0, "T_VALID_REAL_INVALID")
        _require(r.verifier_pass, "VERIFIER_FAIL")
        _require(r.evidence_consistent, "EVIDENCE_INCONSISTENT")
        _require(r.t_valid_real_ms <= s.t_star_ms, "T_STAR_NOT_MET")
        new_used = frozenset(set(s.used_freezes) | {s.freeze_id})
        out = replace(s, used_freezes=new_used, done=True)
        validate_state(out)
        return out

    if event == Event.REAL_FAIL:
        _require(s.phase == Phase.REAL, "REAL_FAIL_ONLY_FROM_REAL")
        r = payload
        _require(isinstance(r, RealResult), "REAL_RESULT_REQUIRED")
        _require(bool(r.reality_delta), "REALITY_DELTA_MISSING")
        _require(s.freeze_id is not None, "REAL_FAIL_WITHOUT_FREEZE")
        new_used = frozenset(set(s.used_freezes) | {s.freeze_id})
        change_generation = r.structural_failure or s.attempt == 6
        out = EngineState(
            page_name=s.page_name,
            task_name=s.task_name,
            generation=s.generation + (1 if change_generation else 0),
            attempt=1 if change_generation else s.attempt + 1,
            phase=Phase.VIRTUAL,
            t_star_ms=s.t_star_ms,
            freeze_id=None,
            used_freezes=new_used,
            real_adapter=None,
            dispatch_mode=None,
            done=False,
        )
        validate_state(out)
        return out

    raise Blocked("EVENT_NOT_ALLOWED")
