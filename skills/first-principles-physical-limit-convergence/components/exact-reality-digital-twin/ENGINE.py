#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""现实执行环境精确数字孪生唯一版 v1.2.0 — Browser/Network Unified Twin."""
from __future__ import annotations
import argparse, copy, hashlib, json, math, statistics, time
from pathlib import Path
from typing import Any

VERSION = "1.2.0"
SCHEMA_VERSION = "browser-network-unified-twin-2.0"
HOST_R2_FP = "9bdd4430596e306cf6f8061069659e2680d8a1b66bd69d7bb3e45fe4cfd63dd8"
UNKNOWN = "UNKNOWN"

OBS_REQUIRED = (
    "HOST_NETWORK","BROWSER_ENVIRONMENT","AUTH_STORAGE_SAFE","PAGE_FRAME_GRAPH",
    "ACTIONABILITY","BROWSER_NETWORK","RUNTIME_EVENTS","GOLDEN_TASK_RESULT",
    "TRACE_HASH","CDP_EVIDENCE","DOM_SNAPSHOT_HASH",
)

def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canon(v: Any) -> str:
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def sha_json(v: Any) -> str:
    return sha_bytes(canon(v).encode("utf-8"))

def read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8-sig"))

def read_jsonl(p: Path | None) -> list[dict[str, Any]]:
    if not p or not p.exists(): return []
    out=[]
    for i,line in enumerate(p.read_text(encoding="utf-8-sig").splitlines(),1):
        if not line.strip(): continue
        try: x=json.loads(line)
        except Exception as e:
            out.append({"type":"PARSE_ERROR","line":i,"error_sha256":sha_bytes(str(e).encode())}); continue
        out.append(x if isinstance(x,dict) else {"type":"NON_OBJECT","value_sha256":sha_json(x)})
    return out

def first(root: Path, *rels: str) -> Path | None:
    for rel in rels:
        p=root/rel
        if p.exists(): return p
    return None

def get(d: Any, *keys: str, default=None):
    cur=d
    for k in keys:
        if not isinstance(cur,dict) or k not in cur: return default
        cur=cur[k]
    return cur

def artifact_hash(golden: Any, suffix: str) -> str | None:
    arts=golden.get("artifacts") if isinstance(golden,dict) else None
    if not isinstance(arts,dict): return None
    for k,v in arts.items():
        if str(k).replace("\\","/").endswith(suffix) and isinstance(v,dict):
            h=v.get("sha256")
            if isinstance(h,str) and len(h)==64: return h.lower()
    return None

def etype(e: dict[str,Any]) -> str:
    return str(e.get("type", e.get("method","UNKNOWN_EVENT")))

def sort_timeline(events: list[dict[str,Any]], cdp: list[dict[str,Any]]) -> list[dict[str,Any]]:
    staged=[]; seq=0
    for origin,arr in (("playwright",events),("cdp",cdp)):
        for raw in arr:
            seq+=1; e=copy.deepcopy(raw); e["_origin"]=origin; e["_sequence"]=seq
            staged.append((str(e.get("ts") or "9999-99-99T99:99:99.999999Z"),seq,e))
    staged.sort(key=lambda x:(x[0],x[1]))
    return [x[2] for x in staged]

def classify(events: list[dict[str,Any]]) -> dict[str,list[dict[str,Any]]]:
    out={"network":[],"runtime":[],"lifecycle":[],"other":[]}
    for e in events:
        t=etype(e).lower()
        if any(x in t for x in ("request","response","network.","websocket","eventsource","webtransport")): out["network"].append(e)
        elif any(x in t for x in ("console","pageerror","exception","crash","javascriptdialog")): out["runtime"].append(e)
        elif any(x in t for x in ("frame","load","lifecycle","domcontent")): out["lifecycle"].append(e)
        else: out["other"].append(e)
    return out

def actionability(probe: Any) -> dict[str,Any]:
    if not isinstance(probe,dict): return {"status":"UNKNOWN_ACTIONABILITY","reason":"MISSING_PROBE"}
    n=probe.get("locator_count")
    if n is None: return {"status":"UNKNOWN_ACTIONABILITY","reason":"LOCATOR_COUNT_UNKNOWN"}
    if n==0: return {"status":"NOT_ACTIONABLE","reason":"ELEMENT_NOT_FOUND"}
    if n!=1: return {"status":"NOT_ACTIONABLE","reason":"STRICTNESS_MULTIPLE_ELEMENTS","count":n}
    checks={"visible":probe.get("visible"),"stable":probe.get("stable_approx_two_animation_frames"),
            "receives_events":probe.get("receives_events_approx"),"enabled":probe.get("enabled")}
    missing=[k for k,v in checks.items() if v is None]
    if missing: return {"status":"UNKNOWN_ACTIONABILITY","reason":"CHECKS_UNKNOWN","missing":missing}
    if checks["visible"] is not True: return {"status":"NOT_ACTIONABLE","reason":"NOT_VISIBLE"}
    if checks["stable"] is not True: return {"status":"NOT_ACTIONABLE","reason":"UNSTABLE"}
    if checks["receives_events"] is not True:
        return {"status":"NOT_ACTIONABLE","reason":"EVENT_INTERCEPTED","hit_target":probe.get("hit_target")}
    if checks["enabled"] is not True: return {"status":"NOT_ACTIONABLE","reason":"DISABLED"}
    return {"status":"ACTIONABLE","reason":"ALL_REQUIRED_CHECKS_PASS"}

def last_probe(x: Any):
    return x[-1] if isinstance(x,list) and x and isinstance(x[-1],dict) else None

def net_summary(events):
    failed=[e for e in events if "fail" in etype(e).lower() or "error" in etype(e).lower()]
    ws=[e for e in events if "websocket" in etype(e).lower()]
    responses=[e for e in events if "response" in etype(e).lower()]
    statuses=[]
    for e in responses:
        s=e.get("status")
        if s is None: s=get(e,"params","response","status")
        if isinstance(s,(int,float)): statuses.append(int(s))
    return {"event_count":len(events),"failure_count":len(failed),"websocket_event_count":len(ws),
            "response_event_count":len(responses),"http_statuses":sorted(statuses)}

def runtime_summary(events):
    names=[etype(e).lower() for e in events]
    return {"event_count":len(events),
            "pageerror_or_exception_count":sum("pageerror" in n or "exception" in n for n in names),
            "crash_count":sum("crash" in n for n in names),
            "dialog_event_count":sum("dialog" in n for n in names),
            "console_event_count":sum("console" in n for n in names)}

def golden_outcome(g: Any) -> str:
    if not isinstance(g,dict): return UNKNOWN
    r=g.get("result")
    if isinstance(r,dict):
        for k in ("outcome","status","result"):
            if r.get(k) is not None: return str(r[k])
    for k in ("outcome","status"):
        if g.get(k) is not None: return str(g[k])
    return UNKNOWN

def obs_identity(env: Any) -> dict[str,Any]:
    if not isinstance(env,dict): return {"task_id":UNKNOWN,"target_selector":UNKNOWN,"fingerprint":UNKNOWN}
    rt=env.get("runtime") if isinstance(env.get("runtime"),dict) else {}
    safe={"url":rt.get("href",UNKNOWN),
          "user_agent_sha256":sha_bytes(str(rt.get("userAgent",UNKNOWN)).encode()),
          "platform":rt.get("platform",UNKNOWN),"timezone":rt.get("timezone",UNKNOWN),
          "dpr":rt.get("dpr",UNKNOWN),
          "context_page_count":len(env.get("context_pages",[])) if isinstance(env.get("context_pages"),list) else UNKNOWN}
    return {"task_id":env.get("task_id",UNKNOWN),"target_selector":env.get("target_selector",UNKNOWN),
            "identity_safe":safe,"fingerprint":sha_json(safe) if UNKNOWN not in safe.values() else UNKNOWN}

def ingest_observability(root_s: str | Path) -> dict[str,Any]:
    root=Path(root_s)
    hp=first(root,"safe/host-network.json","safehost-network.json")
    ep=first(root,"safe/environment.json")
    ap=first(root,"safe/actionability.json")
    evp=first(root,"safe/events.jsonl")
    cp=first(root,"safe/cdp.jsonl")
    gp=first(root,"safe/golden-task-result.json")
    host=read_json(hp) if hp else None; env=read_json(ep) if ep else None
    acts=read_json(ap) if ap else None; events=read_jsonl(evp); cdp=read_jsonl(cp)
    golden=read_json(gp) if gp else None
    timeline=sort_timeline(events,cdp); cls=classify(timeline)
    presence={"HOST_NETWORK":isinstance(host,dict) and bool(host),
              "BROWSER_ENVIRONMENT":isinstance(env,dict) and bool(env),
              "AUTH_STORAGE_SAFE":isinstance(get(env,"storage_state_safe"),dict),
              "PAGE_FRAME_GRAPH":isinstance(get(env,"frames"),list),
              "ACTIONABILITY":isinstance(acts,list) and bool(acts),
              "BROWSER_NETWORK":bool(cls["network"]),
              "RUNTIME_EVENTS":bool(events) or bool(cdp),
              "GOLDEN_TASK_RESULT":isinstance(golden,dict) and bool(golden),
              "TRACE_HASH":artifact_hash(golden,"trace.zip") is not None,
              "CDP_EVIDENCE":bool(cdp) or artifact_hash(golden,"cdp.jsonl") is not None,
              "DOM_SNAPSHOT_HASH":artifact_hash(golden,"dom-snapshot.json") is not None}
    unknowns=[x for x in OBS_REQUIRED if not presence.get(x,False)]
    state={"kind":"OBSERVABILITY","schema_version":SCHEMA_VERSION,"engine_version":VERSION,
           "host":{"r2_fingerprint":HOST_R2_FP,"network_safe":host if host is not None else UNKNOWN},
           "identity":obs_identity(env),
           "browser":{"environment_safe":env if env is not None else UNKNOWN,
                      "actionability":acts if acts is not None else UNKNOWN,
                      "actionability_eval":actionability(last_probe(acts))},
           "network":{"summary":net_summary(cls["network"])},
           "runtime":{"summary":runtime_summary(cls["runtime"])},
           "timeline":timeline,
           "golden_task":{"outcome":golden_outcome(golden),"raw_safe":golden if golden is not None else UNKNOWN},
           "module_presence":presence,"critical_unknowns":unknowns,"source_policy":"OBSERVED_ONLY_NO_GUESSING"}
    state["state_fingerprint"]=sha_json({k:state[k] for k in ("host","identity","browser","network","runtime","golden_task","module_presence")})
    return state

def ingest_timing(root_s: str | Path) -> dict[str,Any]:
    root=Path(root_s); p=first(root,"safe/timing-run.json","timing-run.safe.json")
    raw=read_json(p) if p else None
    if not isinstance(raw,dict):
        return {"kind":"TIMING","status":"FAIL","errors":["TIMING_RUN_MISSING"],"source":str(root)}
    state={"kind":"TIMING","schema_version":SCHEMA_VERSION,"engine_version":VERSION,
           "task_id":raw.get("task_id",UNKNOWN),"run_id":raw.get("run_id",UNKNOWN),
           "target_selector":raw.get("target_selector",UNKNOWN),"outcome":str(raw.get("outcome",UNKNOWN)),
           "duration_ms":raw.get("duration_ms",UNKNOWN),"identity_fingerprint":raw.get("identity_fingerprint",UNKNOWN),
           "heavy_observability":raw.get("heavy_observability",UNKNOWN),"trace":raw.get("trace",UNKNOWN),
           "cdp":raw.get("cdp",UNKNOWN),"dom_snapshot":raw.get("dom_snapshot",UNKNOWN),
           "network_listeners_added":raw.get("network_listeners_added",UNKNOWN),"raw_safe":raw}
    state["state_fingerprint"]=sha_json(state)
    return state

def validate_timing(s: dict[str,Any]) -> dict[str,Any]:
    e=[]
    if s.get("kind")!="TIMING": e.append("NOT_TIMING_STATE")
    if s.get("task_id") in (None,UNKNOWN): e.append("TASK_ID_UNKNOWN")
    if s.get("run_id") in (None,UNKNOWN): e.append("RUN_ID_UNKNOWN")
    if s.get("target_selector") in (None,UNKNOWN): e.append("TARGET_SELECTOR_UNKNOWN")
    if s.get("outcome") in (None,UNKNOWN): e.append("OUTCOME_UNKNOWN")
    d=s.get("duration_ms")
    if not isinstance(d,(int,float)) or not math.isfinite(float(d)) or float(d)<0: e.append("DURATION_INVALID")
    for k in ("heavy_observability","trace","cdp","dom_snapshot","network_listeners_added"):
        if s.get(k) is not False: e.append(f"TIMING_CONTAMINATED_{k.upper()}")
    if s.get("identity_fingerprint") in (None,UNKNOWN): e.append("IDENTITY_UNKNOWN")
    return {"status":"PASS" if not e else "FAIL","errors":e}

def validate_observability(s: dict[str,Any]) -> dict[str,Any]:
    e=[]
    if s.get("kind")!="OBSERVABILITY": e.append("NOT_OBSERVABILITY_STATE")
    if get(s,"host","r2_fingerprint")!=HOST_R2_FP: e.append("HOST_R2_FINGERPRINT_MISMATCH")
    unknowns=s.get("critical_unknowns")
    if not isinstance(unknowns,list) or unknowns: e.append("CRITICAL_UNKNOWNS_NONZERO")
    if get(s,"golden_task","outcome") in (None,UNKNOWN): e.append("GOLDEN_OUTCOME_UNKNOWN")
    if get(s,"browser","actionability_eval","status") in (None,"UNKNOWN_ACTIONABILITY"): e.append("ACTIONABILITY_UNKNOWN")
    if get(s,"identity","task_id") in (None,UNKNOWN): e.append("TASK_ID_UNKNOWN")
    if get(s,"identity","fingerprint") in (None,UNKNOWN): e.append("IDENTITY_UNKNOWN")
    return {"status":"PASS" if not e else "FAIL","errors":e,
            "critical_unknown_count":len(unknowns) if isinstance(unknowns,list) else UNKNOWN}

def semantic_signature(obs: dict[str,Any]) -> dict[str,Any]:
    return {"golden_outcome":get(obs,"golden_task","outcome",default=UNKNOWN),
            "actionability":get(obs,"browser","actionability_eval","status",default=UNKNOWN),
            "actionability_reason":get(obs,"browser","actionability_eval","reason",default=UNKNOWN),
            "network_failure_count":get(obs,"network","summary","failure_count",default=UNKNOWN),
            "runtime_exception_count":get(obs,"runtime","summary","pageerror_or_exception_count",default=UNKNOWN),
            "crash_count":get(obs,"runtime","summary","crash_count",default=UNKNOWN),
            "dialog_event_count":get(obs,"runtime","summary","dialog_event_count",default=UNKNOWN)}

def certify(timing: list[dict[str,Any]], obs: dict[str,Any]) -> dict[str,Any]:
    if len(timing)!=3:
        return {"status":"FAIL","errors":["TIMING_RUN_COUNT_NOT_3"],"timing_run_count":len(timing)}
    tv=[validate_timing(x) for x in timing]; ov=validate_observability(obs); errors=[]
    if any(x["status"]!="PASS" for x in tv): errors.append("TIMING_RUN_VALIDATION_FAILED")
    if ov["status"]!="PASS": errors.append("OBSERVABILITY_VALIDATION_FAILED")
    task_ids=[x.get("task_id") for x in timing]; selectors=[x.get("target_selector") for x in timing]
    outcomes=[x.get("outcome") for x in timing]; ids=[x.get("identity_fingerprint") for x in timing]
    if len(set(task_ids))!=1: errors.append("TIMING_TASK_ID_DRIFT")
    if len(set(selectors))!=1: errors.append("TIMING_SELECTOR_DRIFT")
    if len(set(outcomes))!=1: errors.append("TIMING_OUTCOME_DRIFT")
    if len(set(ids))!=1: errors.append("TIMING_IDENTITY_DRIFT")
    if task_ids and get(obs,"identity","task_id")!=task_ids[0]: errors.append("OBS_TASK_ID_MISMATCH")
    if selectors and get(obs,"identity","target_selector")!=selectors[0]: errors.append("OBS_SELECTOR_MISMATCH")
    if outcomes and get(obs,"golden_task","outcome")!=outcomes[0]: errors.append("OBS_OUTCOME_MISMATCH")
    obs_id=get(obs,"identity","fingerprint")
    if ids and obs_id not in (UNKNOWN,None) and ids[0]!=obs_id: errors.append("OBS_IDENTITY_MISMATCH")
    durations=[float(x["duration_ms"]) for x in timing if isinstance(x.get("duration_ms"),(int,float))]
    certified=not errors and len(durations)==3
    timing_result={"run_duration_ms":durations,
                   "t_valid_ms":min(durations) if certified else UNKNOWN,
                   "median_ms":statistics.median(durations) if len(durations)==3 else UNKNOWN,
                   "max_ms":max(durations) if len(durations)==3 else UNKNOWN,
                   "certification_evidence_time_ms":sum(durations) if certified else UNKNOWN,
                   "t_valid_definition":"minimum T1/T2/T3 duration after 3/3 timing semantics plus O1 observability gates pass",
                   "o1_counts_toward_t_valid":False}
    out={"status":"PASS" if certified else "FAIL","errors":errors,
         "timing_validations":tv,"observability_validation":ov,
         "golden_task_reproduced":"3_OF_3" if certified else "NO",
         "timing":timing_result,
         "canonical_signature":semantic_signature(obs) if ov["status"]=="PASS" else UNKNOWN,
         "observability_state_fingerprint":obs.get("state_fingerprint"),
         "timing_state_fingerprints":[x.get("state_fingerprint") for x in timing],
         "critical_unknown_count":ov.get("critical_unknown_count",UNKNOWN)}
    out["fusion_fingerprint"]=sha_json({k:out[k] for k in ("canonical_signature","observability_state_fingerprint","timing_state_fingerprints","timing")})
    return out

def replay(cert: dict[str,Any]) -> dict[str,Any]:
    if cert.get("status")!="PASS":
        return {"status":"BLOCKED_INVALID_REALITY_INPUT","unknowns_preserved":True,"errors":cert.get("errors",[])}
    return {"status":"REPLAYED","reality_mutated":False,
            "semantic_signature":copy.deepcopy(cert["canonical_signature"]),
            "timing":copy.deepcopy(cert["timing"]),"fusion_fingerprint":cert["fusion_fingerprint"]}

def diff_reality_twin(cert: dict[str,Any], rp: dict[str,Any]) -> dict[str,Any]:
    a=cert.get("canonical_signature"); b=rp.get("semantic_signature"); deltas={}
    if isinstance(a,dict) and isinstance(b,dict):
        for k in sorted(set(a)|set(b)):
            if a.get(k)!=b.get(k): deltas[k]={"reality":a.get(k),"twin":b.get(k)}
    else: deltas["semantic_signature"]={"reality":a,"twin":b}
    return {"status":"PASS" if not deltas and rp.get("status")=="REPLAYED" else "FAIL",
            "delta_count":len(deltas),"deltas":deltas}

def merge(base: Any, overlay: Any) -> Any:
    if isinstance(base,dict) and isinstance(overlay,dict):
        out=copy.deepcopy(base)
        for k,v in overlay.items(): out[k]=merge(out[k],v) if k in out else copy.deepcopy(v)
        return out
    return copy.deepcopy(overlay)

def shadow(cert: dict[str,Any], overlay: dict[str,Any]) -> dict[str,Any]:
    base=copy.deepcopy(cert); hyp=merge(base,overlay); fp=sha_json(base)
    return {"status":"HYPOTHETICAL_SHADOW","reality_mutated":False,
            "delta_present":canon(base)!=canon(hyp),
            "reality_fingerprint_before":fp,"reality_fingerprint_after":fp,"shadow_state":hyp}

def benchmark(cert: dict[str,Any], repeats=1000) -> dict[str,Any]:
    if cert.get("status")!="PASS": return {"status":"BLOCKED_INVALID_REALITY_INPUT"}
    xs=[]
    for _ in range(repeats):
        a=time.perf_counter_ns(); r=replay(cert); b=time.perf_counter_ns()
        if r.get("status")!="REPLAYED": return {"status":"FAIL_REPLAY"}
        xs.append((b-a)/1_000_000)
    s=sorted(xs)
    return {"status":"PASS","repeats":repeats,
            "replay_overhead_ms":{"min":min(xs),"p50":s[len(s)//2],
                                  "p95":s[min(len(s)-1,math.ceil(len(s)*.95)-1)],"max":max(xs)},
            "note":"Twin local replay overhead only; not real browser T_VALID."}

def probe(reason="ACTIONABLE"):
    x={"locator_count":1,"visible":True,"enabled":True,"stable_approx_two_animation_frames":True,
       "receives_events_approx":True,"hit_target":{"tag":"BUTTON","id":"dialog"}}
    if reason=="MISSING": x["locator_count"]=0
    elif reason=="MULTIPLE": x["locator_count"]=2
    elif reason=="NOT_VISIBLE": x["visible"]=False
    elif reason=="UNSTABLE": x["stable_approx_two_animation_frames"]=False
    elif reason=="INTERCEPTED": x["receives_events_approx"]=False; x["hit_target"]={"tag":"DIV","id":"overlay"}
    elif reason=="DISABLED": x["enabled"]=False
    return x

def timing_fixture(run_id,duration=100.0,outcome="PASS",identity="I",heavy=False):
    s={"kind":"TIMING","schema_version":SCHEMA_VERSION,"engine_version":VERSION,
       "task_id":"GOLDEN","run_id":run_id,"target_selector":"#dialog","outcome":outcome,
       "duration_ms":duration,"identity_fingerprint":identity,"heavy_observability":heavy,
       "trace":False,"cdp":False,"dom_snapshot":False,"network_listeners_added":False}
    s["state_fingerprint"]=sha_json(s); return s

def obs_fixture(outcome="PASS",action_reason="ACTIONABLE",identity="I",unknowns=None,network_fail=0,runtime_exc=0,dialog=0):
    acts=[probe(action_reason)]
    net=[{"type":"request"}]+[{"type":"requestfailed"} for _ in range(network_fail)]
    rt=[{"type":"pageerror"} for _ in range(runtime_exc)]+[{"type":"javascriptdialogopening"} for _ in range(dialog)]
    s={"kind":"OBSERVABILITY","schema_version":SCHEMA_VERSION,"engine_version":VERSION,
       "host":{"r2_fingerprint":HOST_R2_FP,"network_safe":{"mode":"fixture"}},
       "identity":{"task_id":"GOLDEN","target_selector":"#dialog","fingerprint":identity},
       "browser":{"environment_safe":{"fixture":True},"actionability":acts,"actionability_eval":actionability(acts[-1])},
       "network":{"summary":net_summary(net)},"runtime":{"summary":runtime_summary(rt)},
       "timeline":net+rt,"golden_task":{"outcome":outcome,"raw_safe":{"fixture":True}},
       "module_presence":{x:True for x in OBS_REQUIRED},"critical_unknowns":unknowns or [],
       "source_policy":"VIRTUAL_FIXTURE_ONLY"}
    s["state_fingerprint"]=sha_json(s); return s

def run_selftest():
    cases=[]
    def ck(n,v): cases.append({"name":n,"pass":bool(v)})
    exp={"MISSING":"ELEMENT_NOT_FOUND","MULTIPLE":"STRICTNESS_MULTIPLE_ELEMENTS","NOT_VISIBLE":"NOT_VISIBLE",
         "UNSTABLE":"UNSTABLE","INTERCEPTED":"EVENT_INTERCEPTED","DISABLED":"DISABLED"}
    for k,v in exp.items(): ck("action_"+k.lower(),actionability(probe(k)).get("reason")==v)
    ck("action_pass",actionability(probe()).get("status")=="ACTIONABLE")
    ts=[timing_fixture("T1",100.0),timing_fixture("T2",101.0),timing_fixture("T3",99.5)]
    ob=obs_fixture(); cert=certify(ts,ob)
    ck("timing_validate_all",all(validate_timing(x)["status"]=="PASS" for x in ts))
    ck("obs_validate",validate_observability(ob)["status"]=="PASS")
    ck("cert_pass",cert["status"]=="PASS")
    ck("3_of_3",cert["golden_task_reproduced"]=="3_OF_3")
    ck("t_valid_min",abs(cert["timing"]["t_valid_ms"]-99.5)<1e-9)
    ck("median",abs(cert["timing"]["median_ms"]-100.0)<1e-9)
    ck("cert_cost",abs(cert["timing"]["certification_evidence_time_ms"]-300.5)<1e-9)
    ck("o1_not_metric",cert["timing"]["o1_counts_toward_t_valid"] is False)
    rp=replay(cert); ck("replay",rp["status"]=="REPLAYED")
    d=diff_reality_twin(cert,rp); ck("delta_zero",d["status"]=="PASS" and d["delta_count"]==0)
    sh=shadow(cert,{"canonical_signature":{"golden_outcome":"FAIL"}})
    ck("shadow_isolation",sh["reality_mutated"] is False and sh["reality_fingerprint_before"]==sh["reality_fingerprint_after"])
    ck("reject_2_runs",certify(ts[:2],ob)["status"]=="FAIL")
    x=copy.deepcopy(ts); x[2]["outcome"]="FAIL"; ck("reject_outcome_drift",certify(x,ob)["status"]=="FAIL")
    x=copy.deepcopy(ts); x[2]["identity_fingerprint"]="J"; ck("reject_identity_drift",certify(x,ob)["status"]=="FAIL")
    x=copy.deepcopy(ts); x[2]["target_selector"]="#other"; ck("reject_selector_drift",certify(x,ob)["status"]=="FAIL")
    x=copy.deepcopy(ts); x[1]["task_id"]="OTHER"; ck("reject_task_drift",certify(x,ob)["status"]=="FAIL")
    x=copy.deepcopy(ts); x[0]["heavy_observability"]=True; ck("reject_heavy_timing",certify(x,ob)["status"]=="FAIL")
    ck("reject_obs_unknown",certify(ts,obs_fixture(unknowns=["TRACE_HASH"]))["status"]=="FAIL")
    ck("reject_obs_outcome",certify(ts,obs_fixture(outcome="FAIL"))["status"]=="FAIL")
    ck("reject_obs_identity",certify(ts,obs_fixture(identity="J"))["status"]=="FAIL")
    bad=obs_fixture(); bad["host"]["r2_fingerprint"]="0"*64; ck("reject_host_fp",certify(ts,bad)["status"]=="FAIL")
    nf=obs_fixture(network_fail=2); ck("network_fail_count",nf["network"]["summary"]["failure_count"]==2)
    rr=obs_fixture(runtime_exc=2,dialog=1); ck("runtime_exc_count",rr["runtime"]["summary"]["pageerror_or_exception_count"]==2)
    ck("dialog_count",rr["runtime"]["summary"]["dialog_event_count"]==1)
    ck("semantic_sig",semantic_signature(rr)["dialog_event_count"]==1)
    for reason,want in (("INTERCEPTED","EVENT_INTERCEPTED"),("UNSTABLE","UNSTABLE"),
                        ("DISABLED","DISABLED"),("NOT_VISIBLE","NOT_VISIBLE")):
        ck("semantic_"+reason.lower(),obs_fixture(action_reason=reason)["browser"]["actionability_eval"]["reason"]==want)
    cert2=certify(copy.deepcopy(ts),copy.deepcopy(ob)); ck("deterministic_fusion",cert["fusion_fingerprint"]==cert2["fusion_fingerprint"])
    ck("unknown_block_replay",replay({"status":"FAIL","errors":["UNKNOWN"]})["unknowns_preserved"] is True)
    ob2=copy.deepcopy(ob); ob2["golden_task"]["diagnostic_duration_ms"]=999999
    ck("o1_duration_ignored",certify(ts,ob2)["timing"]["t_valid_ms"]==99.5)
    passed=sum(x["pass"] for x in cases)
    return {"engine_version":VERSION,"schema_version":SCHEMA_VERSION,"case_count":len(cases),
            "passed":passed,"failed":len(cases)-passed,
            "virtual_fusion_selftest":"PASS" if passed==len(cases) else "FAIL",
            "scope":"Virtual fixtures only; real Browser R3/Environment-99 not certified.","cases":cases}

def load_cert(timing_paths, obs_path):
    ts=[ingest_timing(x) for x in timing_paths]; ob=ingest_observability(obs_path)
    return ts,ob,certify(ts,ob)

def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest="mode",required=True)
    sp.add_parser("selftest")
    for name in ("validate","replay","benchmark","shadow"):
        q=sp.add_parser(name); q.add_argument("--timing",action="append",required=True); q.add_argument("--observability",required=True)
        if name=="benchmark": q.add_argument("--repeats",type=int,default=1000)
        if name=="shadow": q.add_argument("--overlay",required=True)
    a=p.parse_args()
    if a.mode=="selftest": result=run_selftest()
    else:
        ts,ob,cert=load_cert(a.timing,a.observability)
        if a.mode=="validate": result={"timing":[validate_timing(x) for x in ts],"observability":validate_observability(ob),"certification":cert}
        elif a.mode=="replay":
            rp=replay(cert); result={"certification":cert,"replay":rp,"reality_twin_diff":diff_reality_twin(cert,rp)}
        elif a.mode=="benchmark": result=benchmark(cert,a.repeats)
        else: result=shadow(cert,read_json(Path(a.overlay)))
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
