from state_machine_v5_0_2 import (
    Phase, Event, Adapter, Blocked, EngineState, ExecutionClosureEvidence,
    VirtualMature, RealResult, transition, render_locator, validate_state,
    adapter_policy_pass, ALLOWED_MODES, execution_closure_pass, virtual_complete_pass
)
from dataclasses import replace
from itertools import product

base = EngineState(
    "整体闭环极限时间引擎 4.7版2",
    "v5.0.2虚拟成熟现实认证",
    5, 2, Phase.VIRTUAL, 1000.0
)
good_e = ExecutionClosureEvidence(
    True, True, True, True, True, True, True, True,
    "impl-map-sha", "fault-report-sha", "verifier-report-sha"
)
good_v = VirtualMature(
    True, True, True, True,
    True, good_e,
    True, "gpt-verify-sha",
    True, 1000.0,
    "ESTE-v5.0.2-0502-VIRTUAL-FREEZE-01",
    "freeze-sha", "freeze-sha",
    True, Adapter.CODEX, "CHAT",
    True, True, True, Phase.REAL
)
good_real = RealResult(True, True, 1000.0, 1500.0, 500.0)

directed = 0
def expect_block(fn, reason=None):
    global directed
    try: fn()
    except Blocked as e:
        if reason is not None: assert str(e) == reason, (str(e), reason)
        directed += 1; return
    raise AssertionError("expected block")
def expect_pass(fn, predicate=lambda x: True):
    global directed
    out = fn(); assert predicate(out); directed += 1; return out

assert execution_closure_pass(good_e)
assert virtual_complete_pass(good_v)
directed += 2
real = expect_pass(lambda: transition(base, Event.FREEZE_TO_REAL, good_v), lambda s: s.phase == Phase.REAL and not s.done)
expect_block(lambda: transition(base, Event.FREEZE_TO_REAL, replace(good_v, spec_complete=False)), "SPEC_NOT_COMPLETE")
expect_block(lambda: transition(base, Event.FREEZE_TO_REAL, replace(good_v, execution_chain_closed=False)), "EXECUTION_CHAIN_CLAIM_MISMATCH")
bad_e = replace(good_e, recovery_fallback_implemented=False)
expect_block(lambda: transition(base, Event.FREEZE_TO_REAL, replace(good_v, execution_evidence=bad_e)), "EXECUTION_CHAIN_CLAIM_MISMATCH")
expect_block(lambda: transition(base, Event.FREEZE_TO_REAL, replace(good_v, execution_chain_closed=False, execution_evidence=bad_e)), "EXECUTION_CHAIN_OPEN")
expect_block(lambda: transition(base, Event.FREEZE_TO_REAL, replace(good_v, gpt_verification_pass=False)), "GPT_VERIFICATION_FAIL")
expect_block(lambda: transition(base, Event.FREEZE_TO_REAL, replace(good_v, gpt_verification_report_hash="")), "GPT_VERIFICATION_EVIDENCE_MISSING")
expect_block(lambda: transition(base, Event.FREEZE_TO_REAL, replace(good_v, reread_hash="x")), "FREEZE_REREAD_HASH_MISMATCH")
expect_block(lambda: transition(base, Event.FREEZE_TO_REAL, replace(good_v, real_capsule_self_contained=False)), "REAL_CAPSULE_NOT_SELF_CONTAINED")
expect_block(lambda: transition(base, Event.FREEZE_TO_REAL, replace(good_v, dispatch_mode="EXEC")), "ADAPTER_MODE_ILLEGAL")
expect_block(lambda: transition(base, Event.FREEZE_TO_REAL, replace(good_v, dispatch_mode="POWERSHELL")), "ADAPTER_MODE_ILLEGAL")
expect_block(lambda: transition(base, Event.FREEZE_TO_REAL, replace(good_v, dispatch_mode="SHELL")), "ADAPTER_MODE_ILLEGAL")
expect_block(lambda: transition(base, Event.FREEZE_TO_REAL, replace(good_v, real_task_phase=Phase.VIRTUAL)), "REAL_TASK_PHASE_NOT_REAL")
expect_block(lambda: transition(base, Event.FREEZE_TO_REAL, replace(good_v, time_contract_ready=False)), "TIME_CONTRACT_MISSING")
expect_block(lambda: transition(base, Event.FREEZE_TO_REAL, replace(good_v, provenance_scoped=False)), "PROVENANCE_SCOPE_MISSING")
expect_block(lambda: transition(replace(base, used_freezes=frozenset({good_v.freeze_id})), Event.FREEZE_TO_REAL, good_v), "FREEZE_ID_ALREADY_USED")
expect_block(lambda: transition(base, Event.REAL_PASS, good_real), "REAL_PASS_ONLY_FROM_REAL")
expect_block(lambda: validate_state(replace(base, t_star_ms=0)), "T_STAR_INVALID")
expect_block(lambda: validate_state(replace(base, attempt=7)), "ATTEMPT_INVALID")
expect_block(lambda: transition(real, Event.REAL_PASS, replace(good_real, real_start_ms=None)), "REAL_START_MISSING")
expect_block(lambda: transition(real, Event.REAL_PASS, replace(good_real, real_end_ms=None)), "REAL_END_MISSING")
expect_block(lambda: transition(real, Event.REAL_PASS, replace(good_real, t_valid_real_ms=None)), "T_VALID_REAL_MISSING")
expect_block(lambda: transition(real, Event.REAL_PASS, replace(good_real, verifier_pass=False)), "VERIFIER_FAIL")
expect_block(lambda: transition(real, Event.REAL_PASS, replace(good_real, evidence_consistent=False)), "EVIDENCE_INCONSISTENT")
expect_block(lambda: transition(real, Event.REAL_PASS, replace(good_real, t_valid_real_ms=2000.0)), "T_STAR_NOT_MET")
final = expect_pass(lambda: transition(real, Event.REAL_PASS, good_real), lambda s: s.phase == Phase.REAL and s.done)
expect_block(lambda: transition(final, Event.REAL_FAIL, replace(good_real, reality_delta="x")), "TASK_ALREADY_DONE")
expect_block(lambda: transition(real, Event.REAL_FAIL, replace(good_real, reality_delta=None)), "REALITY_DELTA_MISSING")
expect_pass(lambda: transition(real, Event.REAL_FAIL, replace(good_real, reality_delta="x")), lambda s: s.phase == Phase.VIRTUAL and s.generation == 5 and s.attempt == 3)
expect_pass(lambda: transition(real, Event.REAL_FAIL, replace(good_real, reality_delta="x", structural_failure=True)), lambda s: s.phase == Phase.VIRTUAL and s.generation == 6 and s.attempt == 1)
expect_pass(lambda: transition(replace(real, attempt=6), Event.REAL_FAIL, replace(good_real, reality_delta="x")), lambda s: s.generation == 6 and s.attempt == 1)
assert render_locator(base) == "【整体闭环极限时间引擎 4.7版2｜v5.0.2虚拟成熟现实认证｜05-02｜虚】 极限锚00:01.000"
directed += 1

freeze_cases = freeze_allowed = 0
for bits in product([False, True], repeat=16):
    (valid,reality,mature,spec,chain,external,tstar_valid,hashmatch,selfcontained,adapterok,timecontract,provenance,remote_policy,phase_real,freeze_unused,gpt_verified)=bits
    fid="F"; state=base if freeze_unused else replace(base, used_freezes=frozenset({fid}))
    vm=VirtualMature(valid,reality,mature,spec,chain,good_e,gpt_verified,"gpt-sha",external,1234.0 if tstar_valid else 0.0,fid,"h","h" if hashmatch else "x",selfcontained,Adapter.CODEX,"CHAT" if adapterok else "EXEC",timecontract,provenance,remote_policy,Phase.REAL if phase_real else Phase.VIRTUAL)
    expected=all(bits)
    try: transition(state,Event.FREEZE_TO_REAL,vm); allowed=True
    except Blocked: allowed=False
    assert allowed==expected,(bits,allowed,expected)
    freeze_cases += 1; freeze_allowed += int(allowed)

closure_cases=closure_allowed=0
e_fields=["behavior_implementation_mapped","behavior_locations_resolved","exception_classification_implemented","recovery_fallback_implemented","executable_path_verified","fault_injection_passed","verifier_discriminates","capsule_contains_implementation"]
for bits in product([False,True],repeat=8):
    e=ExecutionClosureEvidence(**dict(zip(e_fields,bits)),implementation_map_hash="impl",fault_injection_report_hash="fault",verifier_report_hash="verify")
    claim=all(bits); vm=replace(good_v,execution_chain_closed=claim,execution_evidence=e); expected=all(bits)
    try: transition(base,Event.FREEZE_TO_REAL,vm); allowed=True
    except Blocked: allowed=False
    assert execution_closure_pass(e)==expected
    assert allowed==expected
    closure_cases += 1; closure_allowed += int(allowed)

hash_cases=0
for field in ["implementation_map_hash","fault_injection_report_hash","verifier_report_hash"]:
    e=replace(good_e,**{field:""})
    assert not execution_closure_pass(e)
    expect_block(lambda e=e: transition(base,Event.FREEZE_TO_REAL,replace(good_v,execution_evidence=e)),"EXECUTION_CHAIN_CLAIM_MISMATCH")
    hash_cases += 1
expect_block(lambda: transition(base,Event.FREEZE_TO_REAL,replace(good_v,gpt_verification_report_hash=" ")),"GPT_VERIFICATION_EVIDENCE_MISSING")
hash_cases += 1

real_cases=real_allowed=0
for bits in product([False,True],repeat=7):
    start_ok,end_ok,tval_ok,verifier,evidence,timeorder,within=bits
    rr=RealResult(verifier,evidence,1000.0 if start_ok else None,(2000.0 if timeorder else 500.0) if end_ok else None,(1000.0 if within else 2000.0) if tval_ok else None)
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
samples=[(base,Event.FREEZE_TO_REAL,good_v),(real,Event.REAL_PASS,good_real),(real,Event.REAL_FAIL,replace(good_real,reality_delta="delta")),(base,Event.FREEZE_TO_REAL,replace(good_v,execution_evidence=bad_e)),(base,Event.FREEZE_TO_REAL,replace(good_v,gpt_verification_pass=False))]
for sample in samples:
    outcomes=[]
    for _ in range(5):
        try: outcomes.append(("OK",transition(*sample)))
        except Blocked as e: outcomes.append(("BLOCK",str(e)))
    assert all(item==outcomes[0] for item in outcomes); determinism_cases += 1

total=directed+freeze_cases+closure_cases+hash_cases+real_cases+adapter_cases+failure_cases+determinism_cases
assert freeze_cases==65536 and freeze_allowed==1
assert closure_cases==256 and closure_allowed==1
assert real_cases==128 and real_allowed==1
assert adapter_cases==32
assert failure_cases==12
assert determinism_cases==5
print(f"DIRECTED={directed}")
print("FREEZE_MATRIX=65536/65536 PASS; ALLOW=1")
print("EXECUTION_CLOSURE_MATRIX=256/256 PASS; ALLOW=1")
print("REAL_PASS_MATRIX=128/128 PASS; ALLOW=1")
print(f"ADAPTER_MATRIX={adapter_cases}/{adapter_cases} PASS")
print(f"FAILURE_TRANSITIONS={failure_cases}/{failure_cases} PASS")
print(f"DETERMINISM={determinism_cases}/{determinism_cases} PASS")
print(f"TOTAL={total}/{total} PASS")
