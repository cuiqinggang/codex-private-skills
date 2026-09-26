# -*- coding: utf-8 -*-
"""整体闭环极限短时间引擎 v5.0.2 — 05-05 proof-carrying Reality Capsule.
Top-level method remains only: 虚 -> 实.
This capsule is executable implementation + verifier, not an implementation note.
"""
import math
from dataclasses import dataclass, replace
from enum import Enum
from itertools import product
from time import perf_counter_ns

class Phase(str, Enum):
    VIRTUAL = "虚"
    REAL = "实"

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

def req(ok, reason):
    if not ok:
        raise Blocked(reason)

def nonempty(v):
    return isinstance(v, str) and bool(v.strip())

@dataclass(frozen=True)
class EngineState:
    page_name: str
    task_name: str
    generation: int
    attempt: int
    phase: Phase
    t_star_ms: float
    freeze_id: str | None = None
    used_freezes: frozenset[str] = frozenset()
    real_adapter: Adapter | None = None
    dispatch_mode: str | None = None
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
    real_start_ms: float | None
    real_end_ms: float | None
    t_valid_real_ms: float | None
    reality_delta: str | None = None
    structural_failure: bool = False

def adapter_policy_pass(adapter, mode):
    return adapter in ALLOWED_MODES and mode in ALLOWED_MODES[adapter]

def execution_closure_pass(e):
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
        and nonempty(e.implementation_map_hash)
        and nonempty(e.fault_injection_report_hash)
        and nonempty(e.verifier_report_hash)
        and nonempty(e.freeze_manifest_consistency_hash)
        and nonempty(e.payload_materialization_report_hash)
    )

def virtual_complete_pass(v):
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
        and nonempty(v.gpt_verification_report_hash)
        and v.external_dependencies_closed
        and v.proposed_t_star_ms is not None
        and math.isfinite(v.proposed_t_star_ms)
        and v.proposed_t_star_ms > 0
        and nonempty(v.freeze_id)
        and nonempty(v.freeze_hash)
        and nonempty(v.reread_hash)
        and v.freeze_hash == v.reread_hash
        and v.real_capsule_self_contained
        and adapter_policy_pass(v.real_adapter, v.dispatch_mode)
        and v.time_contract_ready
        and v.provenance_scoped
        and v.remote_claim_requires_reread
        and v.real_task_phase == Phase.REAL
    )

def validate_state(s):
    req(nonempty(s.page_name), "PAGE_NAME_MISSING")
    req(nonempty(s.task_name), "TASK_NAME_MISSING")
    req(s.generation >= 1, "GENERATION_INVALID")
    req(1 <= s.attempt <= 6, "ATTEMPT_INVALID")
    req(math.isfinite(s.t_star_ms) and s.t_star_ms > 0, "T_STAR_INVALID")
    if s.phase == Phase.VIRTUAL:
        req(not s.done, "VIRTUAL_CANNOT_BE_DONE")
        req(s.freeze_id is None, "VIRTUAL_ACTIVE_FREEZE")
        req(s.real_adapter is None and s.dispatch_mode is None, "VIRTUAL_REAL_EXECUTOR")
    else:
        req(nonempty(s.freeze_id), "REAL_WITHOUT_FREEZE")
        req(s.real_adapter is not None, "REAL_ADAPTER_MISSING")
        req(adapter_policy_pass(s.real_adapter, s.dispatch_mode), "ADAPTER_MODE_ILLEGAL")
        if s.done:
            req(s.freeze_id in s.used_freezes, "DONE_FREEZE_NOT_CONSUMED")
        else:
            req(s.freeze_id not in s.used_freezes, "FREEZE_REUSED_BEFORE_REAL")

def freeze_to_real(s, v):
    validate_state(s)
    req(s.phase == Phase.VIRTUAL and not s.done, "FREEZE_ONLY_FROM_VIRTUAL")
    req(isinstance(v, VirtualMature), "VIRTUAL_PAYLOAD_REQUIRED")
    req(v.valid_defined, "VALID_NOT_DEFINED")
    req(v.reality_facts_ready, "REALITY_FACTS_NOT_READY")
    req(v.mature_solution_selected, "MATURE_SOLUTION_NOT_SELECTED")
    req(v.spec_complete, "SPEC_NOT_COMPLETE")
    closure = execution_closure_pass(v.execution_evidence)
    req(v.execution_chain_closed == closure, "EXECUTION_CHAIN_CLAIM_MISMATCH")
    req(v.execution_chain_closed, "EXECUTION_CHAIN_OPEN")
    req(v.gpt_verification_pass, "GPT_VERIFICATION_FAIL")
    req(nonempty(v.gpt_verification_report_hash), "GPT_VERIFICATION_EVIDENCE_MISSING")
    req(v.external_dependencies_closed, "EXTERNAL_DEPENDENCIES_OPEN")
    req(v.proposed_t_star_ms > 0 and math.isfinite(v.proposed_t_star_ms), "PROPOSED_T_STAR_INVALID")
    req(nonempty(v.freeze_id) and v.freeze_id not in s.used_freezes, "FREEZE_ID_INVALID")
    req(nonempty(v.freeze_hash) and v.freeze_hash == v.reread_hash, "FREEZE_REREAD_HASH_MISMATCH")
    req(v.real_capsule_self_contained, "REAL_CAPSULE_NOT_SELF_CONTAINED")
    req(adapter_policy_pass(v.real_adapter, v.dispatch_mode), "ADAPTER_MODE_ILLEGAL")
    req(v.time_contract_ready, "TIME_CONTRACT_MISSING")
    req(v.provenance_scoped, "PROVENANCE_SCOPE_MISSING")
    req(v.remote_claim_requires_reread, "REMOTE_REREAD_POLICY_MISSING")
    req(v.real_task_phase == Phase.REAL, "REAL_TASK_PHASE_NOT_REAL")
    req(virtual_complete_pass(v), "VIRTUAL_COMPLETE_FALSE")
    out = replace(
        s, phase=Phase.REAL, t_star_ms=v.proposed_t_star_ms,
        freeze_id=v.freeze_id, real_adapter=v.real_adapter,
        dispatch_mode=v.dispatch_mode
    )
    validate_state(out)
    return out

def real_pass(s, r):
    validate_state(s)
    req(s.phase == Phase.REAL and not s.done, "REAL_PASS_ONLY_FROM_REAL")
    req(r.real_start_ms is not None and r.real_end_ms is not None and r.t_valid_real_ms is not None, "REAL_TIMING_MISSING")
    req(r.real_end_ms >= r.real_start_ms and r.t_valid_real_ms >= 0, "REAL_TIMING_INVALID")
    req(r.verifier_pass, "VERIFIER_FAIL")
    req(r.evidence_consistent, "EVIDENCE_INCONSISTENT")
    req(r.t_valid_real_ms <= s.t_star_ms, "T_STAR_NOT_MET")
    used = frozenset(set(s.used_freezes) | {s.freeze_id})
    out = replace(s, used_freezes=used, done=True)
    validate_state(out)
    return out

def real_fail(s, r):
    validate_state(s)
    req(s.phase == Phase.REAL and not s.done, "REAL_FAIL_ONLY_FROM_REAL")
    req(nonempty(r.reality_delta), "REALITY_DELTA_MISSING")
    used = frozenset(set(s.used_freezes) | {s.freeze_id})
    next_generation = r.structural_failure or s.attempt == 6
    out = EngineState(
        s.page_name, s.task_name,
        s.generation + (1 if next_generation else 0),
        1 if next_generation else s.attempt + 1,
        Phase.VIRTUAL, s.t_star_ms, None, used, None, None, False
    )
    validate_state(out)
    return out

def render_locator(s):
    validate_state(s)
    total = int(round(s.t_star_ms))
    m, rem = divmod(total, 60000)
    sec, ms = divmod(rem, 1000)
    return f"【{s.page_name}｜{s.task_name}｜{s.generation:02d}-{s.attempt:02d}｜{s.phase.value}】 极限锚{m:02d}:{sec:02d}.{ms:03d}"

def run_verifier():
    base = EngineState("整体闭环极限时间引擎5.0.2版", "v5.0.2虚拟成熟现实认证", 5, 5, Phase.VIRTUAL, 1000.0)
    good_e = ExecutionClosureEvidence(True,True,True,True,True,True,True,True,True,True,"impl","fault","verify","manifest","materialize")
    good_v = VirtualMature(True,True,True,True,True,good_e,True,"gpt",True,1000.0,"F","h","h",True,Adapter.CODEX,"CHAT",True,True,True,Phase.REAL)
    real = freeze_to_real(base, good_v)
    assert virtual_complete_pass(good_v)
    assert render_locator(base).endswith("｜05-05｜虚】 极限锚00:01.000")

    # Fault injection over every implementation-closure Boolean.
    closure_cases = closure_allowed = 0
    fields = (
        "behavior_implementation_mapped","behavior_locations_resolved",
        "exception_classification_implemented","recovery_fallback_implemented",
        "executable_path_verified","fault_injection_passed",
        "verifier_discriminates","capsule_contains_implementation",
        "freeze_manifest_consistent","payload_materialization_verified"
    )
    for bits in product((False, True), repeat=10):
        e = ExecutionClosureEvidence(
            **dict(zip(fields,bits)),
            implementation_map_hash="i",
            fault_injection_report_hash="f",
            verifier_report_hash="v",
            freeze_manifest_consistency_hash="m",
            payload_materialization_report_hash="p"
        )
        claim = all(bits)
        vm = replace(good_v, execution_chain_closed=claim, execution_evidence=e)
        allowed = True
        try:
            freeze_to_real(base, vm)
        except Blocked:
            allowed = False
        assert allowed == all(bits)
        closure_cases += 1
        closure_allowed += allowed

    # Whole virtual-maturity state space: exactly one vector can enter Reality.
    freeze_cases = freeze_allowed = 0
    for bits in product((False, True), repeat=16):
        valid,reality,mature,spec,chain,external,tstar,hashmatch,capsule,adapterok,timecontract,provenance,reread_policy,phase_real,unused,gptok = bits
        state = base if unused else replace(base, used_freezes=frozenset({"F"}))
        vm = VirtualMature(
            valid,reality,mature,spec,chain,good_e,gptok,"gpt",external,
            1000.0 if tstar else 0.0,"F","h","h" if hashmatch else "x",
            capsule,Adapter.CODEX,"CHAT" if adapterok else "EXEC",
            timecontract,provenance,reread_policy,
            Phase.REAL if phase_real else Phase.VIRTUAL
        )
        allowed = True
        try:
            freeze_to_real(state, vm)
        except Blocked:
            allowed = False
        assert allowed == all(bits)
        freeze_cases += 1
        freeze_allowed += allowed

    # REAL PASS matrix.
    real_cases = real_allowed = 0
    for bits in product((False, True), repeat=7):
        start,end,tval,verifier,evidence,order,within = bits
        r = RealResult(
            verifier,evidence,
            1000.0 if start else None,
            (2000.0 if order else 500.0) if end else None,
            (1000.0 if within else 2000.0) if tval else None
        )
        allowed = True
        try:
            real_pass(real, r)
        except Blocked:
            allowed = False
        assert allowed == all(bits)
        real_cases += 1
        real_allowed += allowed

    adapter_cases = 0
    modes = ("CHAT","EXEC","POWERSHELL","SHELL","NATIVE_BROWSER","UI_AGENT","FROZEN_RUNNER","UNKNOWN")
    for a in Adapter:
        for mode in modes:
            assert adapter_policy_pass(a, mode) == (mode in ALLOWED_MODES[a])
            adapter_cases += 1

    failure_cases = 0
    for attempt in range(1,7):
        rs = replace(real, attempt=attempt)
        for structural in (False,True):
            out = real_fail(rs, RealResult(False,False,None,None,None,"delta",structural))
            if structural or attempt == 6:
                assert out.generation == rs.generation + 1 and out.attempt == 1
            else:
                assert out.generation == rs.generation and out.attempt == attempt + 1
            failure_cases += 1

    evidence_hash_cases = 0
    for field in ("implementation_map_hash","fault_injection_report_hash","verifier_report_hash","freeze_manifest_consistency_hash","payload_materialization_report_hash"):
        e = replace(good_e, **{field:""})
        assert not execution_closure_pass(e)
        evidence_hash_cases += 1
    assert not virtual_complete_pass(replace(good_v, gpt_verification_report_hash=""))
    evidence_hash_cases += 1

    determinism_cases = 0
    samples = (
        lambda: freeze_to_real(base, good_v),
        lambda: real_pass(real, RealResult(True,True,1000.0,1500.0,500.0)),
        lambda: real_fail(real, RealResult(False,False,None,None,None,"delta",False)),
        lambda: virtual_complete_pass(good_v),
        lambda: execution_closure_pass(good_e),
    )
    for fn in samples:
        first = repr(fn())
        for _ in range(4):
            assert repr(fn()) == first
        determinism_cases += 1

    total = 2 + closure_cases + freeze_cases + real_cases + adapter_cases + failure_cases + evidence_hash_cases + determinism_cases
    assert closure_cases == 1024 and closure_allowed == 1
    assert freeze_cases == 65536 and freeze_allowed == 1
    assert real_cases == 128 and real_allowed == 1
    assert adapter_cases == 32
    assert failure_cases == 12
    assert evidence_hash_cases == 6
    assert determinism_cases == 5
    assert total == 66745
    return {
        "TOTAL": total,
        "CLOSURE_CASES": closure_cases,
        "FREEZE_CASES": freeze_cases,
        "REAL_CASES": real_cases,
        "ADAPTER_CASES": adapter_cases,
        "FAILURE_CASES": failure_cases,
        "EVIDENCE_HASH_CASES": evidence_hash_cases,
        "DETERMINISM_CASES": determinism_cases,
    }

def run_reality_certificate():
    """Minimal target-environment certificate for the exact blob already exhaustively proved in Virtual."""
    checks = 0
    def ok(cond):
        nonlocal checks
        assert cond
        checks += 1
    def blocked(fn):
        nonlocal checks
        try:
            fn()
        except Blocked:
            checks += 1
            return
        raise AssertionError("expected block")

    base = EngineState("整体闭环极限时间引擎5.0.2版", "v5.0.2虚拟成熟现实认证", 5, 5, Phase.VIRTUAL, 1000.0)
    good_e = ExecutionClosureEvidence(
        True,True,True,True,True,True,True,True,True,True,
        "impl","fault","verify","manifest","materialize"
    )
    good_v = VirtualMature(
        True,True,True,True,True,good_e,True,"gpt",True,1000.0,
        "F","h","h",True,Adapter.CODEX,"CHAT",True,True,True,Phase.REAL
    )
    good_real = RealResult(True,True,1000.0,1500.0,500.0)

    ok(execution_closure_pass(good_e))
    ok(virtual_complete_pass(good_v))
    ok(render_locator(base).endswith("｜05-05｜虚】 极限锚00:01.000"))
    real = freeze_to_real(base, good_v)
    ok(real.phase == Phase.REAL and not real.done)

    bool_fields = (
        "behavior_implementation_mapped","behavior_locations_resolved",
        "exception_classification_implemented","recovery_fallback_implemented",
        "executable_path_verified","fault_injection_passed","verifier_discriminates",
        "capsule_contains_implementation","freeze_manifest_consistent",
        "payload_materialization_verified"
    )
    for field in bool_fields:
        e = replace(good_e, **{field:False})
        ok(not execution_closure_pass(e))
        blocked(lambda e=e: freeze_to_real(base, replace(good_v, execution_evidence=e)))

    hash_fields = (
        "implementation_map_hash","fault_injection_report_hash","verifier_report_hash",
        "freeze_manifest_consistency_hash","payload_materialization_report_hash"
    )
    for field in hash_fields:
        e = replace(good_e, **{field:""})
        ok(not execution_closure_pass(e))
        blocked(lambda e=e: freeze_to_real(base, replace(good_v, execution_evidence=e)))

    blocked(lambda: freeze_to_real(base, replace(good_v, spec_complete=False)))
    blocked(lambda: freeze_to_real(base, replace(good_v, gpt_verification_pass=False)))
    blocked(lambda: freeze_to_real(base, replace(good_v, gpt_verification_report_hash="")))
    blocked(lambda: freeze_to_real(base, replace(good_v, external_dependencies_closed=False)))
    blocked(lambda: freeze_to_real(base, replace(good_v, reread_hash="x")))
    blocked(lambda: freeze_to_real(base, replace(good_v, real_capsule_self_contained=False)))
    blocked(lambda: freeze_to_real(base, replace(good_v, dispatch_mode="EXEC")))
    blocked(lambda: freeze_to_real(base, replace(good_v, time_contract_ready=False)))
    blocked(lambda: freeze_to_real(base, replace(good_v, provenance_scoped=False)))
    blocked(lambda: freeze_to_real(base, replace(good_v, remote_claim_requires_reread=False)))
    blocked(lambda: freeze_to_real(base, replace(good_v, real_task_phase=Phase.VIRTUAL)))
    blocked(lambda: freeze_to_real(replace(base, used_freezes=frozenset({"F"})), good_v))

    final = real_pass(real, good_real)
    ok(final.done)
    blocked(lambda: real_pass(real, replace(good_real, verifier_pass=False)))
    blocked(lambda: real_pass(real, replace(good_real, evidence_consistent=False)))
    blocked(lambda: real_pass(real, replace(good_real, t_valid_real_ms=2000.0)))
    blocked(lambda: real_pass(real, replace(good_real, real_start_ms=None)))
    blocked(lambda: real_fail(real, replace(good_real, reality_delta=None)))

    retry = real_fail(real, replace(good_real, reality_delta="delta"))
    ok(retry.phase == Phase.VIRTUAL and retry.generation == 5 and retry.attempt == 6)
    structural = real_fail(real, replace(good_real, reality_delta="delta", structural_failure=True))
    ok(structural.phase == Phase.VIRTUAL and structural.generation == 6 and structural.attempt == 1)
    sixth = real_fail(replace(real, attempt=6), replace(good_real, reality_delta="delta"))
    ok(sixth.generation == 6 and sixth.attempt == 1)

    ok(adapter_policy_pass(Adapter.CODEX,"CHAT"))
    ok(adapter_policy_pass(Adapter.PLAYWRIGHT,"NATIVE_BROWSER"))
    ok(adapter_policy_pass(Adapter.REASONIX,"UI_AGENT"))
    ok(adapter_policy_pass(Adapter.LOCAL_FROZEN,"FROZEN_RUNNER"))
    ok(not adapter_policy_pass(Adapter.CODEX,"EXEC"))
    ok(not adapter_policy_pass(Adapter.CODEX,"POWERSHELL"))
    ok(not adapter_policy_pass(Adapter.CODEX,"SHELL"))

    assert checks == 62, checks
    return {"TOTAL": checks, "PASS": checks}

if __name__ == "__main__":
    t0 = perf_counter_ns()
    result = run_verifier()
    elapsed_ms = (perf_counter_ns() - t0) / 1_000_000
    print(f"TOTAL={result['TOTAL']}/{result['TOTAL']} PASS")
    print(f"T_VALID_MS={elapsed_ms:.6f}")
