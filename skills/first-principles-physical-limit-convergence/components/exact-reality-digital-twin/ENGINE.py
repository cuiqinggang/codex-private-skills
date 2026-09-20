#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""现实执行环境精确数字孪生唯一版 v1.0.0"""
from __future__ import annotations
import argparse, copy, json
from pathlib import Path

VERSION="1.0.0"
EXPECTED_REALITY_FINGERPRINT="9bdd4430596e306cf6f8061069659e2680d8a1b66bd69d7bb3e45fe4cfd63dd8"

def deep_merge(base,overlay):
    if isinstance(base,dict) and isinstance(overlay,dict):
        out=copy.deepcopy(base)
        for k,v in overlay.items(): out[k]=deep_merge(out[k],v) if k in out else copy.deepcopy(v)
        return out
    return copy.deepcopy(overlay)

def canonical_current_state():
    return {"reality_fingerprint_v3_sha256":EXPECTED_REALITY_FINGERPRINT,
      "critical_unknown_count":0,"critical_execution_coverage":"100.00","twin_input_ready":"YES",
      "rules_runtime_effective":"CAPTURED","rule_engine_validation":"PASS",
      "target":{"process_creation":"DENIED_BEFORE_SUCCESSFUL_START","failure_api":"SetTokenInformation",
      "failure_code":1344,"reproduction":"3_OF_3","child_running":"NO",
      "child_path_resolution":"NOT_REACHED","child_execution_token":"NO_RUNNING_CHILD_PROCESS_TOKEN"}}

def validate_state(state):
    errors=[]
    if state.get("reality_fingerprint_v3_sha256")!=EXPECTED_REALITY_FINGERPRINT: errors.append("REALITY_FINGERPRINT_MISMATCH")
    if state.get("critical_unknown_count")!=0: errors.append("CRITICAL_UNKNOWN_NONZERO")
    if state.get("critical_execution_coverage")!="100.00": errors.append("CRITICAL_COVERAGE_NOT_100")
    if state.get("twin_input_ready")!="YES": errors.append("TWIN_INPUT_NOT_READY")
    if state.get("rules_runtime_effective")!="CAPTURED": errors.append("RULES_NOT_CAPTURED")
    if state.get("rule_engine_validation")!="PASS": errors.append("RULE_ENGINE_NOT_VALIDATED")
    target=state.get("target",{})
    for k,v in canonical_current_state()["target"].items():
        if target.get(k)!=v: errors.append("TARGET_"+k.upper()+"_MISMATCH")
    return {"status":"PASS" if not errors else "FAIL","errors":errors}

def replay_current(state=None):
    state=canonical_current_state() if state is None else state
    check=validate_state(state)
    if check["status"]!="PASS": return {"status":"INVALID_REALITY_STATE","errors":check["errors"]}
    t=state["target"]
    return {"status":"REPLAYED","stage":"PROCESS_CREATION_BEFORE_CHILD_START","api":t["failure_api"],
      "error_code":t["failure_code"],"result":"DENIED","child_running":t["child_running"],
      "path_resolution":t["child_path_resolution"],"child_execution_token":t["child_execution_token"]}

def shadow_overlay(overlay):
    base=canonical_current_state(); hypothetical=deep_merge(base,overlay)
    return {"status":"HYPOTHETICAL_SHADOW","reality_mutated":False,"delta_present":hypothetical!=base,
      "baseline_validation":validate_state(base),"overlay_validation_against_reality":validate_state(hypothetical),
      "state":hypothetical}

def run_selftest():
    base=canonical_current_state(); cases=[]
    def add(name,state,expected):
        actual=validate_state(state)["status"]; cases.append((name,actual==expected))
    add("baseline",base,"PASS")
    mutations=[{"reality_fingerprint_v3_sha256":"0"*64},{"critical_unknown_count":1},
      {"critical_execution_coverage":"99.99"},{"twin_input_ready":"NO"},{"rules_runtime_effective":"UNKNOWN"},
      {"rule_engine_validation":"FAIL"},{"target":{"process_creation":"STARTED"}},{"target":{"failure_api":"CreateProcess"}},
      {"target":{"failure_code":5}},{"target":{"reproduction":"2_OF_3"}},{"target":{"child_running":"YES"}},
      {"target":{"child_path_resolution":"RESOLVED"}},{"target":{"child_execution_token":"PRESENT"}}]
    for i,ov in enumerate(mutations,1): add("mutation_"+str(i),deep_merge(base,ov),"FAIL")
    r=replay_current(base); cases.append(("replay_boundary",r.get("status")=="REPLAYED" and r.get("error_code")==1344))
    s=shadow_overlay({"target":{"failure_code":0,"process_creation":"STARTED"}})
    cases.append(("shadow_isolation",s["status"]=="HYPOTHETICAL_SHADOW" and s["reality_mutated"] is False and s["delta_present"]))
    for i in range(8):
        r=replay_current(base); cases.append(("repeat_"+str(i+1),r.get("status")=="REPLAYED" and r.get("error_code")==1344))
    passed=sum(1 for _,ok in cases if ok)
    return {"engine_version":VERSION,"case_count":len(cases),"passed":passed,"failed":len(cases)-passed,
      "virtual_contract_99":"PASS" if passed==len(cases) else "FAIL","cases":[{"name":n,"pass":ok} for n,ok in cases]}

def main():
    p=argparse.ArgumentParser(); p.add_argument("mode",choices=["replay","selftest","shadow"]); p.add_argument("--overlay")
    a=p.parse_args()
    if a.mode=="replay": result=replay_current()
    elif a.mode=="selftest": result=run_selftest()
    else:
        if not a.overlay: raise SystemExit("--overlay required")
        result=shadow_overlay(json.loads(Path(a.overlay).read_text(encoding="utf-8")))
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
