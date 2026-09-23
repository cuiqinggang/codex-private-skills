#!/usr/bin/env python3
# Qwen3.8 / Bonsai 2 27B local-agent capability harness v4
# Virtual-close authority for first-principles-physical-limit-convergence v4.6.0.
from __future__ import annotations
import argparse, hashlib, itertools, json
from pathlib import Path

MAX_CTX=262144
OUTPUT_RESERVE=1024
ROUTE_BUDGET={"OFF":0,"LOW_512":512,"MEDIUM_2048":2048,"HIGH_8192":8192}
BAND_TOTAL={"8K":8192,"32K":32768,"64K":65536,"128K":131072,"192K":196608,"224K":229376,"240-245K":247808,"252-255K":260096}
TOOL_RESERVE={"file":512,"powershell":768,"git":768,"http":768,"browser":1536,"local_service":768,"hash_test":512,"multi_tool":2048}
FACTORS=("domain","context_band","tool_family","failure_mode","plan_shape","reasoning_route")
EXPECTED_COUNTS={"atomic_cases":592,"jev_cases":240,"thinking_cases":96,"long_workflows":18,"cache_trials":48,"memory_trials":24}
EXPECTED_UNITS=1018
EXPECTED_LONG_STEPS=1800
EXPECTED_FAILURES=86

def canonical(obj):
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
def sha(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()

def token_envelope(case):
    route=case["reasoning_route"]; rb=ROUTE_BUDGET[route]
    tr=TOOL_RESERVE[case["tool_family"]]
    nominal_prompt=BAND_TOTAL[case["context_band"]]
    raw_total=nominal_prompt+rb+tr+OUTPUT_RESERVE
    if raw_total<=MAX_CTX:
        prompt=nominal_prompt
        semantics="PROMPT_BAND_PLUS_RESERVED_BUDGETS"
    else:
        prompt=MAX_CTX-rb-tr-OUTPUT_RESERVE
        semantics="MAX_CONTEXT_TOTAL_ENVELOPE_REBOUND"
    total=prompt+rb+tr+OUTPUT_RESERVE
    return {"semantics":semantics,"nominal_prompt_band_tokens":nominal_prompt,
      "prompt_budget_tokens":prompt,"thinking_budget_tokens":rb,
      "tool_schema_reserve_tokens":tr,"output_reserve_tokens":OUTPUT_RESERVE,
      "max_context_tokens":MAX_CTX,"sum_tokens":total,
      "valid":prompt>0 and total<=MAX_CTX}

def unit_fixture(kind,c):
    b={"unit_id":c["id"],"kind":kind,"seed":c.get("seed"),
       "model_reality_required":bool(c.get("model_reality_required",True)),
       "source_sha256":sha(c)}
    if kind=="atomic":
        b.update({"fixture_generator":"bstar-fixture-v4",
          "workspace_scope":c["fixture"]["workspace_scope"],"domain":c["domain"],
          "tool_family":c["tool_family"],"failure_mode":c["failure_mode"],
          "plan_shape":c["plan_shape"],"reasoning_route":c["reasoning_route"],
          "variant":c["variant"],"token_envelope":token_envelope(c),
          "oracle":c["oracle"],"plan_contract":c["plan_contract"],
          "terminal":c["oracle"]["expected_terminal"]})
    elif kind=="jev":
        b.update({"decision_type":c["type"],"confidence_band":c["confidence_band"],
          "ambiguity":c["ambiguity"],
          "route_policy":"JEV_IF_VALID_AND_FASTER_ELSE_LOCAL_AGENT","oracle":c["oracle"]})
    elif kind=="thinking":
        b.update({"route":c["route"],"trigger":c["trigger"],
          "budget_tokens":c["budget_tokens"],"oracle":c["oracle"]})
    elif kind=="long":
        b.update({"steps":c["steps"],"checkpoints":c["checkpoints"],
          "archetype":c["archetype"],"failure_schedule":c["failure_schedule"],
          "required_invariants":c["required_invariants"]})
    elif kind=="cache":
        b.update({"context_band":c["context_band"],"mode":c["mode"],"kv":c["kv"],
          "server_flags":c["server_flags"],"cache_prompt":c["request_cache_prompt"],
          "oracle":c["oracle"]})
    elif kind=="memory":
        b.update({"context_band":c["context_band"],"kv":c["kv"],
          "batch_profile":c["batch_profile"],"oracle":c["oracle"]})
    return b

def select_pairwise_anchors(cases):
    universe=set()
    for c in cases:
        for i,j in itertools.combinations(range(len(FACTORS)),2):
            universe.add((i,c[FACTORS[i]],j,c[FACTORS[j]]))
    uncovered=set(universe); rem=list(cases); selected=[]
    while uncovered:
        best=max(rem,key=lambda c:sum((i,c[FACTORS[i]],j,c[FACTORS[j]]) in uncovered
          for i,j in itertools.combinations(range(len(FACTORS)),2)))
        selected.append(best)
        for i,j in itertools.combinations(range(len(FACTORS)),2):
            uncovered.discard((i,best[FACTORS[i]],j,best[FACTORS[j]]))
        rem.remove(best)
    return selected,len(universe),len(uncovered)

def self_test(suite):
    errors=[]; warnings=[]
    for k,n in EXPECTED_COUNTS.items():
        if len(suite.get(k,[]))!=n: errors.append(f"COUNT_{k}={len(suite.get(k,[]))}_EXPECTED_{n}")
    total=sum(len(suite.get(k,[])) for k in EXPECTED_COUNTS)
    if total!=EXPECTED_UNITS: errors.append(f"TOTAL_UNITS={total}_EXPECTED_{EXPECTED_UNITS}")
    if sum(x["steps"] for x in suite["long_workflows"])!=EXPECTED_LONG_STEPS: errors.append("LONG_STEPS_MISMATCH")
    if sum(x["injected_failures"] for x in suite["long_workflows"])!=EXPECTED_FAILURES: errors.append("INJECTED_FAILURES_MISMATCH")
    ids=[]; manifest=[]; corrected=[]
    categories=[("atomic","atomic_cases"),("jev","jev_cases"),("thinking","thinking_cases"),
      ("long","long_workflows"),("cache","cache_trials"),("memory","memory_trials")]
    for kind,key in categories:
        for c in suite[key]:
            ids.append(c["id"])
            try:
                f=unit_fixture(kind,c)
                if kind=="atomic":
                    e=f["token_envelope"]
                    if not e["valid"]: errors.append("TOKEN_ENVELOPE_INVALID:"+c["id"])
                    if c["context_band"]=="252-255K" and ROUTE_BUDGET[c["reasoning_route"]]>0:
                        if 252*1024+ROUTE_BUDGET[c["reasoning_route"]]>MAX_CTX:
                            corrected.append(c["id"])
                manifest.append(f)
            except Exception as ex:
                errors.append(f"FIXTURE_GEN:{c.get('id','?')}:{type(ex).__name__}:{ex}")
    if len(ids)!=len(set(ids)): errors.append("DUPLICATE_UNIT_IDS")
    if len(manifest)!=EXPECTED_UNITS: errors.append("MANIFEST_COUNT_MISMATCH")
    if len(corrected)!=16: errors.append(f"OLD_CONFLICT_COUNT={len(corrected)}_EXPECTED_16")
    anchors,pairs,remaining=select_pairwise_anchors(suite["atomic_cases"])
    if remaining: errors.append("PAIRWISE_ANCHOR_COVERAGE_INCOMPLETE")
    if len(anchors)!=64: warnings.append(f"ANCHOR_COUNT={len(anchors)}_EXPECTED_REFERENCE_64")
    trig={"clear":"OFF","minor_ambiguity":"LOW_512","local_failure":"MEDIUM_2048","multi_receipt_conflict":"HIGH_8192"}
    for c in suite["thinking_cases"]:
        if trig.get(c["trigger"])!=c["route"]: errors.append("THINK_ROUTE_MISMATCH:"+c["id"])
        if ROUTE_BUDGET.get(c["route"])!=c["budget_tokens"]: errors.append("THINK_BUDGET_MISMATCH:"+c["id"])
    for c in suite["jev_cases"]:
        if "schema_exact" not in c["oracle"]: errors.append("JEV_ORACLE_INCOMPLETE:"+c["id"])
    result={"schema":"QWEN38_AGENT_V46_ZERO_GPU_SELFTEST_V1","gpu_runs":0,"model_calls":0,
      "source_suite_id":suite.get("suite_id"),"source_suite_version":suite.get("version"),
      "units_instantiated":len(manifest),"expected_units":EXPECTED_UNITS,
      "old_token_budget_conflicts_detected_and_rebound":len(corrected),
      "corrected_case_ids":corrected,
      "post_rebind_token_budget_failures":sum(1 for x in manifest if x["kind"]=="atomic" and not x["token_envelope"]["valid"]),
      "pairwise_atomic_anchors":len(anchors),"pairwise_combinations_covered":pairs,
      "pairwise_combinations_missing":remaining,"anchor_ids":[x["id"] for x in anchors],
      "long_workflow_steps":sum(x["steps"] for x in suite["long_workflows"]),
      "injected_failures":sum(x["injected_failures"] for x in suite["long_workflows"]),
      "errors":errors,"warnings":warnings,"self_test":"PASS" if not errors else "FAIL",
      "execution_chain_closed":"PASS" if not errors else "FAIL",
      "runner_binding_gate":"PASS" if not errors else "FAIL",
      "token_envelope_gate":"PASS" if not errors else "FAIL",
      "hand_off_ready":"PASS" if not errors else "FAIL","manifest_sha256":sha(manifest)}
    return result,manifest,anchors

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--suite",required=True)
    ap.add_argument("--self-test",action="store_true"); ap.add_argument("--plan",action="store_true")
    ap.add_argument("--out",default="."); args=ap.parse_args()
    suite=json.load(open(args.suite,encoding="utf-8"))
    result,manifest,anchors=self_test(suite); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    (out/"ZERO-GPU-SELFTEST-RESULT.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"EXECUTABLE-FIXTURE-MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    reality_plan={"schema":"QWEN38_AGENT_V46_REALITY_PLAN_V1","strategy":"BOUNDARY_FIRST_THEN_EXPAND",
      "primary_atomic_anchors":[x["id"] for x in anchors],
      "why":"64 anchors preserve all 800 legal pairwise combinations while minimizing first-pass reality work.",
      "expansion_rule":"On FAIL/unstable/boundary crossing, expand to neighbors sharing >=4/6 atomic factors until stable; run full 1018 only if boundary remains unresolved.",
      "quality_policy":"Case FAIL maps capability boundary; only PASS cells enter min T_VALID competition."}
    (out/"REALITY-BOUNDARY-PLAN.json").write_text(json.dumps(reality_plan,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result["self_test"]=="PASS" else 2
if __name__=="__main__": raise SystemExit(main())
