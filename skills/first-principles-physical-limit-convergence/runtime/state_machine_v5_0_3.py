import math
from dataclasses import dataclass, replace
from enum import Enum
from typing import Optional, FrozenSet, Tuple

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
class TimeEvent:
    seq: int
    name: str
    phase: Phase
    at_utc: str
    active_t_star_ms: Optional[float] = None
    t_valid_real_ms: Optional[float] = None
    source: Optional[str] = None

@dataclass(frozen=True)
class EngineState:
    page_name: str
    task_name: str
    generation: int
    attempt: int
    phase: Phase
    timeline_id: str
    time_origin_utc: str
    time_event_seq: int = 0
    time_events: Tuple[TimeEvent, ...] = ()
    t_star_ms: Optional[float] = None
    t_star_status: str = "PENDING"
    best_certified_t_valid_ms: Optional[float] = None
    t_valid_start: Optional[str] = None
    t_valid_end: Optional[str] = None
    t_star_source: Optional[str] = None
    freeze_id: Optional[str] = None
    used_freezes: FrozenSet[str] = frozenset()
    real_adapter: Optional[Adapter] = None
    dispatch_mode: Optional[str] = None
    done: bool = False

@dataclass(frozen=True)
class ExecutionClosureEvidence:
    behavior_implementation_mapped: bool
    behavior_locations_resolved: bool
    exception_classification_implemented: bool
    recovery_fallback_implemented: bool
    executable_path_verified: bool
    fault_injection_passed: bool
    verifier_discriminates: bool
    capsule_contains_implementation: bool
    freeze_manifest_consistent: bool
    payload_materialization_verified: bool
    implementation_map_hash: str
    fault_injection_report_hash: str
    verifier_report_hash: str
    freeze_manifest_consistency_hash: str
    payload_materialization_report_hash: str

@dataclass(frozen=True)
class VirtualMature:
    valid_defined: bool
    reality_facts_ready: bool
    mature_solution_selected: bool
    spec_complete: bool
    execution_chain_closed: bool
    execution_evidence: ExecutionClosureEvidence
    gpt_verification_pass: bool
    gpt_verification_report_hash: str
    external_dependencies_closed: bool
    proposed_t_star_ms: float
    t_valid_start: str
    t_valid_end: str
    t_star_source: str
    event_at_utc: str
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
    real_start_utc: Optional[str] = None
    real_end_utc: Optional[str] = None
    reality_delta: Optional[str] = None
    structural_failure: bool = False

def _require(cond: bool, reason: str):
    if not cond:
        raise Blocked(reason)

def adapter_policy_pass(adapter: Adapter, mode: str) -> bool:
    return adapter in ALLOWED_MODES and mode in ALLOWED_MODES[adapter]

def _nonempty(value: str) -> bool:
    return isinstance(value, str) and bool(value.strip())

def execution_closure_pass(e: ExecutionClosureEvidence) -> bool:
    return (
        isinstance(e, ExecutionClosureEvidence)
        and e.behavior_implementation_mapped
        and e.behavior_locations_resolved
        and e.exception_classification_implemented
        and e.recovery_fallback_implemented
        and e.executable_path_verified
        and e.fault_injection_passed
        and e.verifier_discriminates
        and e.capsule_contains_implementation
        and e.freeze_manifest_consistent
        and e.payload_materialization_verified
        and _nonempty(e.implementation_map_hash)
        and _nonempty(e.fault_injection_report_hash)
        and _nonempty(e.verifier_report_hash)
        and _nonempty(e.freeze_manifest_consistency_hash)
        and _nonempty(e.payload_materialization_report_hash)
    )

def virtual_complete_pass(v: VirtualMature) -> bool:
    if not isinstance(v, VirtualMature):
        return False
    closure = execution_closure_pass(v.execution_evidence)
    return (
        v.valid_defined
        and v.reality_facts_ready
        and v.mature_solution_selected
        and v.spec_complete
        and v.execution_chain_closed
        and closure
        and v.execution_chain_closed == closure
        and v.gpt_verification_pass
        and _nonempty(v.gpt_verification_report_hash)
        and v.external_dependencies_closed
        and v.proposed_t_star_ms is not None
        and math.isfinite(v.proposed_t_star_ms)
        and v.proposed_t_star_ms > 0
        and time_anchor_ready(v.proposed_t_star_ms, v.t_valid_start, v.t_valid_end, v.t_star_source)
        and _nonempty(v.freeze_id)
        and _nonempty(v.freeze_hash)
        and _nonempty(v.reread_hash)
        and v.freeze_hash == v.reread_hash
        and v.real_capsule_self_contained
        and adapter_policy_pass(v.real_adapter, v.dispatch_mode)
        and v.time_contract_ready
        and v.provenance_scoped
        and v.remote_claim_requires_reread
        and v.real_task_phase == Phase.REAL
    )

def append_time_event(
    s: EngineState,
    name: str,
    phase: Phase,
    at_utc: str,
    active_t_star_ms: Optional[float] = None,
    t_valid_real_ms: Optional[float] = None,
    source: Optional[str] = None,
) -> EngineState:
    _require(_nonempty(at_utc), "TIME_EVENT_UTC_MISSING")
    next_seq = s.time_event_seq + 1
    event = TimeEvent(
        seq=next_seq,
        name=name,
        phase=phase,
        at_utc=at_utc,
        active_t_star_ms=active_t_star_ms,
        t_valid_real_ms=t_valid_real_ms,
        source=source,
    )
    return replace(
        s,
        time_event_seq=next_seq,
        time_events=s.time_events + (event,),
    )

def time_anchor_ready(t_star_ms, t_valid_start, t_valid_end, t_star_source) -> bool:
    return (
        t_star_ms is not None
        and math.isfinite(t_star_ms)
        and t_star_ms > 0
        and _nonempty(t_valid_start)
        and _nonempty(t_valid_end)
        and _nonempty(t_star_source)
    )

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
    _require(_nonempty(s.timeline_id), "TIMELINE_ID_MISSING")
    _require(_nonempty(s.time_origin_utc), "TIME_ORIGIN_MISSING")
    _require(s.time_event_seq == len(s.time_events), "TIME_EVENT_SEQ_MISMATCH")
    for idx, event in enumerate(s.time_events, start=1):
        _require(event.seq == idx, "TIME_EVENT_ORDER_INVALID")
        _require(_nonempty(event.name), "TIME_EVENT_NAME_MISSING")
        _require(_nonempty(event.at_utc), "TIME_EVENT_UTC_MISSING")
    _require(s.t_star_status in {"PENDING","VIRTUAL_FROZEN","REAL_CERTIFIED"}, "T_STAR_STATUS_INVALID")
    if s.best_certified_t_valid_ms is not None:
        _require(math.isfinite(s.best_certified_t_valid_ms) and s.best_certified_t_valid_ms >= 0, "BEST_CERTIFIED_T_INVALID")
    if s.phase == Phase.VIRTUAL:
        _require(not s.done, "VIRTUAL_CANNOT_BE_DONE")
        _require(s.t_star_status == "PENDING", "VIRTUAL_T_STAR_STATUS_INVALID")
        any_anchor = (
            s.t_star_ms is not None
            or s.t_valid_start is not None
            or s.t_valid_end is not None
            or s.t_star_source is not None
        )
        if any_anchor:
            _require(
                time_anchor_ready(s.t_star_ms, s.t_valid_start, s.t_valid_end, s.t_star_source),
                "PARTIAL_TIME_ANCHOR"
            )
        _require(s.freeze_id is None, "VIRTUAL_MUST_NOT_HOLD_ACTIVE_FREEZE")
        _require(s.real_adapter is None and s.dispatch_mode is None, "VIRTUAL_MUST_NOT_HOLD_REAL_EXECUTOR")
    if s.phase == Phase.REAL:
        _require(
            time_anchor_ready(s.t_star_ms, s.t_valid_start, s.t_valid_end, s.t_star_source),
            "REAL_TIME_ANCHOR_MISSING"
        )
        _require(s.t_star_status in {"VIRTUAL_FROZEN","REAL_CERTIFIED"}, "REAL_T_STAR_STATUS_INVALID")
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
    if s.t_star_ms is None:
        anchor = "PENDING"
    else:
        anchor = f"{format_ms(s.t_star_ms)}｜T*={s.t_star_ms:.6f}ms"
    return f"【{s.page_name}｜{s.task_name}｜{s.generation:02d}-{s.attempt:02d}｜{s.phase.value}】 极限锚{anchor}"

def render_dispatch_header(s: EngineState) -> str:
    validate_state(s)
    _require(s.phase == Phase.REAL, "DISPATCH_HEADER_REQUIRES_REAL")
    _require(
        time_anchor_ready(s.t_star_ms, s.t_valid_start, s.t_valid_end, s.t_star_source),
        "DISPATCH_TIME_ANCHOR_MISSING"
    )
    return "\n".join([
        render_locator(s),
        f"TIMELINE_ID={s.timeline_id}",
        f"TIME_ORIGIN_UTC={s.time_origin_utc}",
        f"TIME_EVENT_SEQ={s.time_event_seq}",
        f"T_STAR_STATUS={s.t_star_status}",
        f"T_STAR_MS={s.t_star_ms:.6f}",
        f"T_VALID_START={s.t_valid_start}",
        f"T_VALID_END={s.t_valid_end}",
        f"T_STAR_SOURCE={s.t_star_source}",
        f"BEST_CERTIFIED_T_VALID_MS={'' if s.best_certified_t_valid_ms is None else f'{s.best_certified_t_valid_ms:.6f}'}",
    ])

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
        _require(v.spec_complete, "SPEC_NOT_COMPLETE")
        closure = execution_closure_pass(v.execution_evidence)
        _require(v.execution_chain_closed == closure, "EXECUTION_CHAIN_CLAIM_MISMATCH")
        _require(v.execution_chain_closed, "EXECUTION_CHAIN_OPEN")
        _require(closure, "EXECUTION_CHAIN_EVIDENCE_INCOMPLETE")
        _require(v.gpt_verification_pass, "GPT_VERIFICATION_FAIL")
        _require(_nonempty(v.gpt_verification_report_hash), "GPT_VERIFICATION_EVIDENCE_MISSING")
        _require(v.external_dependencies_closed, "EXTERNAL_DEPENDENCIES_OPEN")
        _require(v.proposed_t_star_ms is not None and math.isfinite(v.proposed_t_star_ms) and v.proposed_t_star_ms > 0, "PROPOSED_T_STAR_INVALID")
        _require(_nonempty(v.t_valid_start), "T_VALID_START_MISSING")
        _require(_nonempty(v.t_valid_end), "T_VALID_END_MISSING")
        _require(_nonempty(v.t_star_source), "T_STAR_SOURCE_MISSING")
        _require(_nonempty(v.event_at_utc), "FREEZE_EVENT_UTC_MISSING")
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
        _require(virtual_complete_pass(v), "VIRTUAL_COMPLETE_FALSE")
        out = replace(
            s,
            phase=Phase.REAL,
            t_star_ms=v.proposed_t_star_ms,
            t_star_status="VIRTUAL_FROZEN",
            t_valid_start=v.t_valid_start,
            t_valid_end=v.t_valid_end,
            t_star_source=v.t_star_source,
            freeze_id=v.freeze_id,
            real_adapter=v.real_adapter,
            dispatch_mode=v.dispatch_mode,
        )
        out = append_time_event(
            out,
            "FREEZE_TO_REAL",
            Phase.REAL,
            v.event_at_utc,
            active_t_star_ms=v.proposed_t_star_ms,
            source=v.t_star_source,
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
        _require(_nonempty(r.real_start_utc), "REAL_START_UTC_MISSING")
        _require(_nonempty(r.real_end_utc), "REAL_END_UTC_MISSING")
        _require(r.real_end_ms >= r.real_start_ms, "REAL_TIME_ORDER_INVALID")
        _require(r.t_valid_real_ms >= 0, "T_VALID_REAL_INVALID")
        _require(r.verifier_pass, "VERIFIER_FAIL")
        _require(r.evidence_consistent, "EVIDENCE_INCONSISTENT")
        _require(r.t_valid_real_ms <= s.t_star_ms, "T_STAR_NOT_MET")
        new_used = frozenset(set(s.used_freezes) | {s.freeze_id})
        best = (
            r.t_valid_real_ms
            if s.best_certified_t_valid_ms is None
            else min(s.best_certified_t_valid_ms, r.t_valid_real_ms)
        )
        out = append_time_event(
            s,
            "REAL_START",
            Phase.REAL,
            r.real_start_utc,
            active_t_star_ms=s.t_star_ms,
            source=s.t_star_source,
        )
        out = append_time_event(
            out,
            "REAL_PASS",
            Phase.REAL,
            r.real_end_utc,
            active_t_star_ms=s.t_star_ms,
            t_valid_real_ms=r.t_valid_real_ms,
            source="REAL_CERTIFIED",
        )
        out = replace(
            out,
            used_freezes=new_used,
            done=True,
            t_star_status="REAL_CERTIFIED",
            best_certified_t_valid_ms=best,
        )
        validate_state(out)
        return out

    if event == Event.REAL_FAIL:
        _require(s.phase == Phase.REAL, "REAL_FAIL_ONLY_FROM_REAL")
        r = payload
        _require(isinstance(r, RealResult), "REAL_RESULT_REQUIRED")
        _require(bool(r.reality_delta), "REALITY_DELTA_MISSING")
        _require(_nonempty(r.real_start_utc), "REAL_START_UTC_MISSING")
        _require(_nonempty(r.real_end_utc), "REAL_END_UTC_MISSING")
        _require(s.freeze_id is not None, "REAL_FAIL_WITHOUT_FREEZE")
        new_used = frozenset(set(s.used_freezes) | {s.freeze_id})
        change_generation = r.structural_failure or s.attempt == 6
        out = append_time_event(
            s,
            "REAL_START",
            Phase.REAL,
            r.real_start_utc,
            active_t_star_ms=s.t_star_ms,
            source=s.t_star_source,
        )
        out = append_time_event(
            out,
            "REAL_FAIL",
            Phase.REAL,
            r.real_end_utc,
            active_t_star_ms=s.t_star_ms,
            t_valid_real_ms=r.t_valid_real_ms,
            source=r.reality_delta,
        )
        out = replace(
            out,
            generation=s.generation + (1 if change_generation else 0),
            attempt=1 if change_generation else s.attempt + 1,
            phase=Phase.VIRTUAL,
            t_star_ms=None,
            t_star_status="PENDING",
            t_valid_start=None,
            t_valid_end=None,
            t_star_source=None,
            freeze_id=None,
            used_freezes=new_used,
            real_adapter=None,
            dispatch_mode=None,
            done=False,
        )
        validate_state(out)
        return out

    raise Blocked("EVENT_NOT_ALLOWED")
