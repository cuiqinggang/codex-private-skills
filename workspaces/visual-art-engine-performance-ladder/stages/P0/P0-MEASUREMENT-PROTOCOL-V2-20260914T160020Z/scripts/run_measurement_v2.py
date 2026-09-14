#!/usr/bin/env python3
from __future__ import annotations

import argparse, asyncio, hashlib, itertools, json, math, os, platform, random, struct, sys, time, uuid, zlib
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from typing import Any

EXPECTED_SIZE=(256,256)
FIXTURE_NAME="p0-control-black-256.png"
PATTERNS=("ABBA","BAAB")

def utc_now(): return datetime.now(timezone.utc).isoformat()
def sha_bytes(b:bytes): return hashlib.sha256(b).hexdigest()
def sha_file(p:Path): return sha_bytes(p.read_bytes())
def q(v:list[float],p:float):
    s=sorted(v); x=(len(s)-1)*p; a=math.floor(x); b=math.ceil(x)
    return s[a] if a==b else s[a]+(s[b]-s[a])*(x-a)
def mad(v:list[float]):
    m=median(v); return median([abs(x-m) for x in v])
def stats(v:list[float]):
    return {"n":len(v),"min_ms":min(v),"median_ms":median(v),"p95_ms":q(v,.95),"max_ms":max(v),"mad_ms":mad(v),"mad_scaled_ms":1.4826*mad(v)}

def validate_png(data:bytes)->dict[str,Any]:
    if not data.startswith(b"\x89PNG\r\n\x1a\n"): raise ValueError("invalid PNG signature")
    pos=8; width=height=depth=color=interlace=None; idat=bytearray(); iend=False
    while pos+12<=len(data):
        n=struct.unpack(">I",data[pos:pos+4])[0]; kind=data[pos+4:pos+8]; end=pos+8+n; crc=end+4
        if crc>len(data): raise ValueError("truncated PNG chunk")
        payload=data[pos+8:end]
        if (zlib.crc32(kind+payload)&0xffffffff)!=struct.unpack(">I",data[end:crc])[0]: raise ValueError("PNG CRC mismatch")
        if kind==b"IHDR": width,height,depth,color,_,_,interlace=struct.unpack(">IIBBBBB",payload)
        elif kind==b"IDAT": idat.extend(payload)
        elif kind==b"IEND": iend=True; break
        pos=crc
    if not iend or width is None or not idat: raise ValueError("PNG missing required chunks")
    if interlace!=0 or color not in {0,2,3,4,6} or depth not in {8,16}: raise ValueError("unsupported PNG")
    raw=zlib.decompress(bytes(idat)); channels={0:1,2:3,3:1,4:2,6:4}[color]
    expected=height*(1+math.ceil(width*channels*depth/8))
    if len(raw)!=expected: raise ValueError("incomplete zlib decode")
    if (width,height)!=EXPECTED_SIZE: raise ValueError("unexpected dimensions")
    return {"valid_png":True,"width":width,"height":height,"decoded_bytes":len(raw),"sha256":sha_bytes(data)}

class Log:
    def __init__(self,path:Path,buffered:bool):
        self.path=path; self.buffered=buffered; self.rows=[]; self.h=None if buffered else path.open("w",encoding="utf-8",newline="\n")
    def write(self,kind,payload):
        row={"utc":utc_now(),"monotonic_ns":time.perf_counter_ns(),"kind":kind,"payload":payload}
        if self.buffered: self.rows.append(row)
        else: self.h.write(json.dumps(row,ensure_ascii=False,separators=(",",":"))+"\n"); self.h.flush()
    def close(self):
        if self.buffered:
            with self.path.open("w",encoding="utf-8",newline="\n") as h:
                for r in self.rows: h.write(json.dumps(r,ensure_ascii=False,separators=(",",":"))+"\n")
        elif self.h: self.h.close()

def workflow(path:Path,prefix:str):
    w=json.loads(path.read_text(encoding="utf-8"))
    if {n["class_type"] for n in w.values()}!={"LoadImage","SaveImage"}: raise ValueError("workload changed")
    if w["1"]["inputs"]["image"]!=FIXTURE_NAME or w["2"]["inputs"]["filename_prefix"]!="__P0_RUN_PREFIX__": raise ValueError("workflow identity changed")
    w["2"]["inputs"]["filename_prefix"]=prefix; return w

def schedule(seed:int,blocks:int):
    if blocks%2: raise ValueError("blocks must be even")
    pats=["ABBA"]*(blocks//2)+["BAAB"]*(blocks//2); random.Random(seed).shuffle(pats); return pats

def bracket_schedule(blocks:int): return ["ABA"]*blocks

def artifact_identity(strategy:str,attempt:int,nonce:str):
    phase="warmup" if attempt<0 else "measured"
    token=f"{phase}-{abs(attempt):03d}-{nonce}"
    return {
        "token":token,
        "run_prefix":f"p0-v2/{strategy}/{token}",
        "raw_event_name":f"{token}.jsonl",
        "output_copy_name":f"{token}.png",
        "history_name":f"{token}.json",
        "equivalence_name":f"{token}.png",
    }

ARM_LABEL_SENTINELS=("measured-A","measured-B","warmup-A","warmup-B")

def label_leak_count(*values):
    text=json.dumps(values,ensure_ascii=False,sort_keys=True)
    return sum(text.count(token) for token in ARM_LABEL_SENTINELS)

def normalized_workflow_sha(value):
    clone=json.loads(json.dumps(value))
    clone["2"]["inputs"]["filename_prefix"]="__OPAQUE_RUN_TOKEN__"
    return sha_bytes(json.dumps(clone,sort_keys=True,separators=(",",":")).encode())

def block_pairs(rows:list[dict],patterns:list[str]):
    out=[]
    for bi,pat in enumerate(patterns):
        r=rows[bi*4:bi*4+4]
        idx=((0,1),(3,2)) if pat=="ABBA" else ((1,0),(2,3))
        ds=[]
        for pi,(ai,bi2) in enumerate(idx):
            d=r[ai]["t_ms"]-r[bi2]["t_ms"]; ds.append(d)
            out.append({"block":bi+1,"pair":pi+1,"pattern":pat,"a_attempt":r[ai]["attempt"],"b_attempt":r[bi2]["attempt"],"a_ms":r[ai]["t_ms"],"b_ms":r[bi2]["t_ms"],"delta_ms":d})
    return out,[out[i:i+2] for i in range(0,len(out),2)]

def bootstrap_ci(blocks,reps,seed):
    rng=random.Random(seed); vals=[]
    for _ in range(reps):
        sample=[blocks[rng.randrange(len(blocks))] for _ in blocks]
        vals.append(median([x["delta_ms"] for b in sample for x in b]))
    return [q(vals,.025),q(vals,.975)]

def null_rates_pass(pos,any_reject,cfg):
    pos_tol=cfg["positive_false_keep_tolerance"]; any_tol=cfg["any_direction_rejection_tolerance"]
    return pos_tol[0]<=pos<=pos_tol[1] and any_tol[0]<=any_reject<=any_tol[1]

def formal_statistical_pipeline(blocks,rules):
    values=[median([x["delta_ms"] for x in b]) for b in blocks]
    effect=median(values); residuals=[v-effect for v in values]; cfg=rules["null_calibration"]
    def sign_distribution(seed):
        rng=random.Random(seed); out=[]
        for _ in range(cfg["iterations"]): out.append(median([(1 if rng.random()<.5 else -1)*v for v in residuals]))
        return out
    calibration=sign_distribution(cfg["calibration_seed"])
    null=sign_distribution(cfg["validation_seed"])
    loerr=q(calibration,cfg["alpha"]/2); hierr=q(calibration,1-cfg["alpha"]/2)
    ci=[effect-hierr,effect-loerr]
    pos=sum(x-hierr>0 for x in null)/len(null)
    neg=sum(x-loerr<0 for x in null)/len(null)
    any_reject=sum((x-hierr>0) or (x-loerr<0) for x in null)/len(null)
    null_pass=null_rates_pass(pos,any_reject,cfg)
    grid=[]; x=rules["mde"]["grid_start_ms"]
    while x<=rules["mde"]["grid_stop_ms"]+1e-9: grid.append(round(x,10)); x+=rules["mde"]["grid_step_ms"]
    curve=[{"gain_ms":gain,"observed_power":sum(x+gain-hierr>0 for x in null)/len(null)} for gain in grid]
    hit=next((x for x in curve if x["observed_power"]>=rules["mde"]["power"]),None) if null_pass else None
    return {"method":"BLOCK_SIGN_RANDOMIZATION_LOCATION_CI","cluster_statistic":"median_of_two_paired_deltas_per_four_run_block_then_median_across_blocks","effect_ms":effect,"ci_95_ms":ci,"calibration_error_quantiles_ms":[loerr,hierr],"null_calibration_pass":null_pass,"null_positive_false_keep_rate":pos,"null_negative_false_reject_rate":neg,"null_any_direction_rejection_rate":any_reject,"null_simulation_iterations":cfg["iterations"],"null_calibration_seed":cfg["calibration_seed"],"null_validation_seed":cfg["validation_seed"],"noise_floor_ms":q([abs(x) for x in null],.95),"null_distribution_ms":null,"mde_ms":None if hit is None else hit["gain_ms"],"mde_target_power":rules["mde"]["power"],"mde_observed_power":None if hit is None else hit["observed_power"],"power_curve":curve}

def estimate_mde(blocks,rules):
    result=formal_statistical_pipeline(blocks,rules)
    return {"mde_ms":result["mde_ms"],"achieved_power":result["mde_observed_power"],"iterations":result["null_simulation_iterations"],"alpha":rules["null_calibration"]["alpha"],"target_power":result["mde_target_power"],"seed":result["null_validation_seed"],"power_curve":result["power_curve"],"null_calibration_pass":result["null_calibration_pass"],"null_positive_false_keep_rate":result["null_positive_false_keep_rate"],"null_any_direction_rejection_rate":result["null_any_direction_rejection_rate"]}

def order_effect_analysis(blocks,rules):
    vals=[median([x["delta_ms"] for x in b]) for b in blocks]; labels=[b[0]["pattern"] for b in blocks]
    def contrast(lab):
        return median([v for v,z in zip(vals,lab) if z=="ABBA"])-median([v for v,z in zip(vals,lab) if z=="BAAB"])
    obs=contrast(labels); cfg=rules["order_effect"]; rng=random.Random(cfg["seed"]); boots=[]
    av=[v for v,z in zip(vals,labels) if z=="ABBA"]; bv=[v for v,z in zip(vals,labels) if z=="BAAB"]
    for _ in range(cfg["bootstrap_repetitions"]):
        aa=[av[rng.randrange(len(av))] for __ in av]; bb=[bv[rng.randrange(len(bv))] for __ in bv]; boots.append(median(aa)-median(bb))
    ci=[q(boots,.025),q(boots,.975)]; n=len(vals); k=len(av); combos=math.comb(n,k)
    if combos<=300000:
        hit=0
        for ix in itertools.combinations(range(n),k):
            aset=set(ix); lab=["ABBA" if i in aset else "BAAB" for i in range(n)]
            if abs(contrast(lab))>=abs(obs)-1e-12: hit+=1
        p=hit/combos; method="EXACT"
    else:
        hit=0; lab=list(labels)
        for _ in range(cfg["randomization_repetitions"]):
            rng.shuffle(lab); hit+=abs(contrast(lab))>=abs(obs)-1e-12
        p=(hit+1)/(cfg["randomization_repetitions"]+1); method="RANDOMIZATION"
    return {"ORDER_EFFECT_MS":obs,"ORDER_EFFECT_BOOTSTRAP_95CI":ci,"ORDER_EFFECT_EXACT_PERMUTATION_P":p if method=="EXACT" else None,"ORDER_EFFECT_PERMUTATION_P":p,"permutation_method":method,"permutation_space":combos}

def theil_sen(v):
    slopes=[(v[j]-v[i])/(j-i) for i in range(len(v)) for j in range(i+1,len(v))]
    s=median(slopes); return {"slope_ms_per_attempt":s,"projected_span_ms":s*(len(v)-1),"early_minus_late_ms":median(v[:max(1,len(v)//4)])-median(v[-max(1,len(v)//4):])}

def trend_permutation(v,reps,seed):
    observed=abs(theil_sen(v)["slope_ms_per_attempt"]); rng=random.Random(seed); hits=0; shuffled=list(v)
    for _ in range(reps):
        rng.shuffle(shuffled)
        if abs(theil_sen(shuffled)["slope_ms_per_attempt"])>=observed: hits+=1
    return (hits+1)/(reps+1)

async def run_once(session,endpoint,wf_path,fixture,outroot,evidence,label,arm,strategy,attempt,artifact,ws_pool,client_ids):
    effective="BASELINE" if arm=="A" or strategy=="AA" else strategy
    buffered=(effective=="E7")
    raw=evidence/"raw-events"/artifact["raw_event_name"]; prefix=artifact["run_prefix"]
    if label_leak_count(prefix,raw.name,artifact): raise ValueError("TIMED_PATH_LABEL_LEAK")
    log=Log(raw,buffered); marks={}; pid=None; ws=None; owns=False
    try:
        wsurl=endpoint.replace("http://","ws://").replace("https://","wss://")
        if effective=="E5":
            if "B" not in ws_pool: ws_pool["B"]=await session.ws_connect(f"{wsurl}/ws?clientId={client_ids['B']}",timeout=10)
            ws=ws_pool["B"]
        else:
            ws=await session.ws_connect(f"{wsurl}/ws?clientId={client_ids[arm]}",timeout=10); owns=True
        submitted_workflow=workflow(wf_path,prefix)
        if label_leak_count(submitted_workflow): raise ValueError("WORKFLOW_LABEL_LEAK")
        log.write("WS_READY",{"arm":arm,"effective":effective}); marks["REQUEST_START"]=time.perf_counter_ns()
        async with session.post(f"{endpoint}/prompt",json={"prompt":submitted_workflow,"client_id":client_ids[arm]}) as resp:
            txt=await resp.text(); log.write("PROMPT_RESPONSE",{"status":resp.status,"body":txt}); resp.raise_for_status(); pid=json.loads(txt)["prompt_id"]
        marks["QUEUE_ACK"]=time.perf_counter_ns()
        while True:
            msg=await ws.receive(timeout=15)
            if msg.type.name=="TEXT":
                ev=json.loads(msg.data); log.write("WS_TEXT",ev); data=ev.get("data",{})
                if data.get("prompt_id")!=pid: continue
                if ev.get("type")=="executing":
                    if data.get("node") is not None: marks.setdefault("EXECUTION_START",time.perf_counter_ns())
                    else: marks.setdefault("EXECUTING_NONE",time.perf_counter_ns()); marks.setdefault("SAVE_DONE",time.perf_counter_ns()); break
                if ev.get("type")=="executed" and str(data.get("node"))=="2": marks["SAVE_DONE"]=time.perf_counter_ns()
                if ev.get("type")=="execution_success": marks.setdefault("EXECUTION_SUCCESS",time.perf_counter_ns())
                if ev.get("type") in {"execution_error","execution_interrupted"}: raise RuntimeError(str(ev))
            elif msg.type.name in {"CLOSED","CLOSE","ERROR"}: raise RuntimeError("websocket ended early")
        if owns and effective!="E4": await ws.close(); owns=False
        marks["HISTORY_GET_START"]=time.perf_counter_ns()
        async with session.get(f"{endpoint}/history/{pid}") as resp:
            marks["HISTORY_HEADERS"]=time.perf_counter_ns()
            history_raw=await resp.text(); marks["HISTORY_BODY_DONE"]=time.perf_counter_ns(); resp.raise_for_status(); h=json.loads(history_raw)
        entry=h.get(pid)
        status=entry.get("status",{}) if entry else {}
        if not entry or status.get("completed") is not True or status.get("status_str")!="success": raise ValueError("matching explicitly successful history missing")
        images=entry.get("outputs",{}).get("2",{}).get("images",[])
        if len(images)!=1: raise ValueError("not exactly one output")
        log.write("HISTORY_CONFIRMED",{"http_status":200,"prompt_id":pid,"completed":True,"status_str":"success","output_count":1,"entry_sha256":sha_bytes(json.dumps(entry,sort_keys=True,separators=(",",":")).encode())})
        image=images[0]
        if image.get("type","output")!="output": raise ValueError("unexpected output type")
        params={"filename":image["filename"],"subfolder":image.get("subfolder",""),"type":"output"}
        if label_leak_count(params): raise ValueError("HTTP_LABEL_LEAK")
        if effective=="TRACK_B_LOCAL_FILE_V2":
            candidate=(outroot/params["subfolder"]/Path(params["filename"]).name).resolve()
            if not candidate.is_relative_to(outroot.resolve()): raise ValueError("output path escape")
            data=candidate.read_bytes(); source="LOCAL_HISTORY_BOUND"
        else:
            marks["VIEW_GET_START"]=time.perf_counter_ns()
            async with session.get(f"{endpoint}/view",params=params) as resp:
                marks["VIEW_HEADERS"]=time.perf_counter_ns()
                data=await resp.read(); marks["VIEW_BODY_DONE"]=time.perf_counter_ns(); resp.raise_for_status()
            source="HTTP_VIEW"
        marks["PNG_VERIFY_START"]=time.perf_counter_ns()
        val=validate_png(data)
        marks["PNG_VERIFY_DONE"]=time.perf_counter_ns()
        copy=evidence/"outputs"/artifact["output_copy_name"]
        marks["EVIDENCE_COPY_START"]=time.perf_counter_ns()
        copy.write_bytes(data)
        marks["EVIDENCE_COPY_DONE"]=time.perf_counter_ns()
        marks["RESULT_READY"]=time.perf_counter_ns()
        history_path=evidence/"history"/artifact["history_name"]; history_path.write_text(history_raw,encoding="utf-8"); history_raw_sha=sha_bytes(history_raw.encode("utf-8"))
        if owns: await ws.close(); owns=False
        equivalence=None
        if effective=="TRACK_B_LOCAL_FILE_V2":
            async with session.get(f"{endpoint}/view",params=params) as resp:
                http=await resp.read(); resp.raise_for_status()
            equivalence={"local_sha256":sha_bytes(data),"http_sha256":sha_bytes(http),"bytes_equal":data==http}
            if not equivalence["bytes_equal"]: raise ValueError("HTTP/local equivalence failed")
            (evidence/"equivalence-http"/artifact["equivalence_name"]).write_bytes(http)
        return {"attempt":attempt,"label":label,"arm":arm,"run_token":artifact["token"],"effective_strategy":effective,"prompt_id":pid,"run_prefix":prefix,"marks_monotonic_ns":marks,"t_ms":(marks["RESULT_READY"]-marks["REQUEST_START"])/1e6,"history":{"exact_prompt_id_match":True,"completed":True,"status_str":"success","output_count":1,"raw_snapshot":str(history_path),"raw_sha256":history_raw_sha,"entry_sha256":sha_bytes(json.dumps(entry,sort_keys=True,separators=(",",":")).encode())},"output_identity":image,"validation":val,"result_source":source,"same_prompt_equivalence":equivalence,"valid":True,"utc_done":utc_now()}
    except Exception as e:
        return {"attempt":attempt,"label":label,"arm":arm,"effective_strategy":effective,"prompt_id":pid,"marks_monotonic_ns":marks,"valid":False,"error":repr(e),"utc_done":utc_now()}
    finally:
        if owns and ws is not None: await ws.close()
        log.close()

async def execute(args):
    import aiohttp
    evidence=Path(args.evidence_dir).resolve(); evidence.mkdir(parents=True,exist_ok=False)
    for d in ("raw-events","outputs","history","equivalence-http"): (evidence/d).mkdir()
    wf=Path(args.workflow).resolve(); fixture=Path(args.fixture).resolve(); outroot=Path(args.output_root).resolve()
    fixture_data=fixture.read_bytes(); validate_png(fixture_data)
    rules=json.loads(Path(args.rules).read_text(encoding="utf-8"))
    if args.design=="BRACKET" and args.strategy=="AA": raise ValueError("AA requires PAIRED design")
    patterns=schedule(args.order_seed,args.blocks) if args.design=="PAIRED" else bracket_schedule(args.blocks)
    results=[]; endpoint=args.endpoint.rstrip("/"); ws_pool={}; shared_client=str(uuid.uuid4())
    client_ids={"A":shared_client,"B":str(uuid.uuid4()) if args.strategy=="E5" else shared_client}
    planned=args.blocks*(4 if args.design=="PAIRED" else 3)
    warm_artifacts=[artifact_identity(args.strategy,-i,uuid.uuid4().hex[:12]) for i in range(1,4)]
    measured_artifacts=[artifact_identity(args.strategy,i,uuid.uuid4().hex[:12]) for i in range(1,planned+1)]
    if label_leak_count(warm_artifacts,measured_artifacts): raise ValueError("TIMED_PATH_LABEL_LEAK")
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=180)) as session:
        async with session.get(f"{endpoint}/object_info") as r:
            oi=await r.json(); r.raise_for_status()
        if not {"LoadImage","SaveImage"}<=set(oi): raise RuntimeError("required nodes missing")
        form=aiohttp.FormData(); form.add_field("image",fixture_data,filename=FIXTURE_NAME,content_type="image/png"); form.add_field("type","input"); form.add_field("overwrite","true")
        async with session.post(f"{endpoint}/upload/image",data=form) as r: upload=await r.json(); r.raise_for_status()
        warm=["A","B","B"]
        for i,arm in enumerate(warm,1): results.append(await run_once(session,endpoint,wf,fixture,outroot,evidence,f"warmup-{arm}",arm,args.strategy,-i,warm_artifacts[i-1],ws_pool,client_ids))
        attempt=0
        for pat in patterns:
            for arm in pat:
                attempt+=1; results.append(await run_once(session,endpoint,wf,fixture,outroot,evidence,f"measured-{arm}-{attempt:03d}",arm,args.strategy,attempt,measured_artifacts[attempt-1],ws_pool,client_ids))
        for ws in ws_pool.values(): await ws.close()
    with (evidence/"raw-runs.jsonl").open("w",encoding="utf-8") as h:
        for r in results: h.write(json.dumps(r,ensure_ascii=False,separators=(",",":"))+"\n")
    measured=[r for r in results if r["attempt"]>0]; valid=[r for r in measured if r["valid"]]
    summary={"protocol":"P0-MEASUREMENT-PROTOCOL-V2","batch_id":args.batch_id,"strategy":args.strategy,"design":args.design,"order_seed":args.order_seed,"blocks":args.blocks,"patterns":patterns,"planned_attempts":planned,"valid_attempts":len(valid),"failures":[r for r in measured if not r["valid"]],"warmups":results[:3],"client_identity_policy":"shared_for_AA_E4_E7_TRACK_B; isolated_for_E5_persistent_WS","client_ids_equal":client_ids["A"]==client_ids["B"],"label_blinding_policy":"A_B_LABEL_METADATA_ONLY; submitted workflow and timed paths use preassigned arm-blind opaque tokens","A_NORMALIZED_WORKFLOW_SHA":normalized_workflow_sha(workflow(wf,warm_artifacts[0]["run_prefix"])),"B_NORMALIZED_WORKFLOW_SHA":normalized_workflow_sha(workflow(wf,warm_artifacts[1]["run_prefix"])),"TIMED_PATH_LABEL_LEAK":label_leak_count(warm_artifacts,measured_artifacts),"WORKFLOW_LABEL_LEAK":0,"HTTP_LABEL_LEAK":0,"identity":{"runner_sha256":sha_file(Path(__file__)),"workflow_sha256":sha_file(wf),"fixture_sha256":sha_file(fixture),"A_impl_sha256":sha_file(Path(__file__)),"B_impl_sha256":sha_file(Path(__file__)) if args.strategy=="AA" else f"strategy:{args.strategy}"},"upload":upload}
    if len(valid)==planned:
        if args.design=="BRACKET":
            from bracket_summary import build as build_brackets
            bracket_result=build_brackets(measured,rules["bootstrap_repetitions"],rules["bootstrap_seed"]+args.seed_offset)
            summary["bracket"]=bracket_result
            (evidence/"bracket-summary.json").write_text(json.dumps(bracket_result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        else:
            a=[r["t_ms"] for r in measured if r["arm"]=="A"]; b=[r["t_ms"] for r in measured if r["arm"]=="B"]; pairs,blocks=block_pairs(measured,patterns); ds=[x["delta_ms"] for x in pairs]
            formal=formal_statistical_pipeline(blocks,rules); ci=formal["ci_95_ms"]
            drift=theil_sen(a); drift["permutation_p_two_sided"]=trend_permutation(a,10000,rules["bootstrap_seed"]+900+args.seed_offset)
            summary.update({"arm_A":stats(a),"arm_B":stats(b),"current_local_baseline_ms":median(a),"candidate_median_ms":median(b),"paired":{**stats(ds),"formal_effect_ms":formal["effect_ms"],"cluster_randomization_95ci_ms":ci,"bootstrap_95ci_ms":ci,"formal_method":formal["method"],"p95_arm_delta_ms":q(a,.95)-q(b,.95),"pairs":pairs},"drift_A":drift,"pattern_effect_ms":median([x["delta_ms"] for x in pairs if x["pattern"]=="ABBA"])-median([x["delta_ms"] for x in pairs if x["pattern"]=="BAAB"])})
            if args.strategy=="AA":
                floor=formal["noise_floor_ms"]; mde=formal["mde_ms"]; order=order_effect_analysis(blocks,rules)
                if not formal["null_calibration_pass"]:
                    bound=None; order_state="NOT_ADJUDICATED_NULL_CALIBRATION_FAIL"; drift_fail=False; state="NOT_AUTHORITATIVE"
                else:
                    bound=.5*mde; oci=order["ORDER_EFFECT_BOOTSTRAP_95CI"]
                    if oci[0]>=-bound and oci[1]<=bound: order_state="PASS"
                    elif oci[0]>bound or oci[1]<-bound: order_state="FAIL"
                    else: order_state="INCONCLUSIVE"
                    drift_fail=(abs(drift["projected_span_ms"])>mde and drift["permutation_p_two_sided"]<0.05)
                    base_fail=not(ci[0]<=0<=ci[1]) or abs(formal["effect_ms"])>floor or drift_fail or summary["identity"]["A_impl_sha256"]!=summary["identity"]["B_impl_sha256"]
                    state="FAIL" if base_fail or order_state=="FAIL" else ("PASS" if order_state=="PASS" else "INCONCLUSIVE")
                mde_result=estimate_mde(blocks,rules)
                summary["aa_calibration"]={"status":state,"noise_floor_ms":floor,"minimum_detectable_effect_ms":mde,"order_equivalence_bound_ms":bound,"order_effect":{**order,"state":order_state},"null_calibration_pass":formal["null_calibration_pass"],"null_positive_false_keep_rate":formal["null_positive_false_keep_rate"],"null_any_direction_rejection_rate":formal["null_any_direction_rejection_rate"],"mde_simulation":mde_result,"environment_drift_fail":drift_fail,"stop_candidate_adjudication":state!="PASS"}
                (evidence/"null-calibration.json").write_text(json.dumps({k:v for k,v in formal.items() if k not in {"null_distribution_ms","power_curve"}},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
                (evidence/"null-distribution.json").write_text(json.dumps({"method":formal["method"],"iterations":formal["null_simulation_iterations"],"values_ms":formal["null_distribution_ms"]},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
                (evidence/"false-positive-summary.json").write_text(json.dumps({"status":"PASS" if formal["null_calibration_pass"] else "FAIL","NULL_POSITIVE_FALSE_KEEP_RATE":formal["null_positive_false_keep_rate"],"NULL_ANY_DIRECTION_REJECTION_RATE":formal["null_any_direction_rejection_rate"],"positive_tolerance":rules["null_calibration"]["positive_false_keep_tolerance"],"any_direction_tolerance":rules["null_calibration"]["any_direction_rejection_tolerance"]},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
                (evidence/"mde-power-curve.json").write_text(json.dumps({"status":"PASS" if mde is not None else "BLOCKED_NULL_CALIBRATION_FAIL","FINAL_MDE_MS":mde,"target_power":formal["mde_target_power"],"observed_power":formal["mde_observed_power"],"curve":formal["power_curve"]},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (evidence/"paired-results.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (evidence/"environment.json").write_text(json.dumps({"captured_at":utc_now(),"platform":platform.platform(),"python":sys.executable,"python_version":sys.version,"aiohttp":aiohttp.__version__,"endpoint":endpoint,"output_root":str(outroot)},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (evidence/"output-hashes.json").write_text(json.dumps([{"attempt":r["attempt"],"sha256":r.get("validation",{}).get("sha256")} for r in measured],indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:summary.get(k) for k in ("batch_id","strategy","valid_attempts","current_local_baseline_ms","candidate_median_ms","aa_calibration")},ensure_ascii=False,indent=2))
    return 0 if len(valid)==planned else 2

def selftest(args):
    rules_path=Path(args.rules).resolve() if args.rules else Path(__file__).resolve().parent.parent/"decision-rules.json"
    rules=json.loads(rules_path.read_text(encoding="utf-8"))
    pats=schedule(args.order_seed,args.blocks)
    assert len(pats)==args.blocks and pats.count("ABBA")==args.blocks//2 and pats.count("BAAB")==args.blocks//2
    wf_path=Path(__file__).resolve().parent.parent/"contracts"/"p0-workflow.json"
    a_artifact=artifact_identity("AA",1,"0123456789ab")
    b_artifact=artifact_identity("AA",2,"fedcba987654")
    a_workflow=workflow(wf_path,a_artifact["run_prefix"])
    b_workflow=workflow(wf_path,b_artifact["run_prefix"])
    a_normalized_workflow_sha=normalized_workflow_sha(a_workflow)
    b_normalized_workflow_sha=normalized_workflow_sha(b_workflow)
    timed_path_label_leak=label_leak_count(a_artifact,b_artifact)
    workflow_label_leak=label_leak_count(a_workflow,b_workflow)
    http_label_leak=label_leak_count("/prompt","/history/{opaque_prompt_id}","/view",{"filename":"opaque-output.png","subfolder":"p0-v2\\AA","type":"output"})
    assert a_normalized_workflow_sha==b_normalized_workflow_sha
    assert timed_path_label_leak==0 and workflow_label_leak==0 and http_label_leak==0
    rows=[]; n=0
    for p in pats:
        for arm in p: n+=1; rows.append({"attempt":n,"arm":arm,"t_ms":10 if arm=="A" else 9})
    pairs,blocks=block_pairs(rows,pats); assert len(pairs)==args.blocks*2 and all(abs(x["delta_ms"]-1)<1e-9 for x in pairs)
    rng=random.Random(2026091513)
    synthetic=[]
    for i in range(80):
        v=rng.gauss(0,2); synthetic.append([{"delta_ms":v-.1,"pattern":"ABBA" if i<40 else "BAAB"},{"delta_ms":v+.1,"pattern":"ABBA" if i<40 else "BAAB"}])
    formal=formal_statistical_pipeline(synthetic,rules); again=formal_statistical_pipeline(synthetic,rules)
    assert formal["null_calibration_pass"] and formal["null_distribution_ms"]==again["null_distribution_ms"]
    assert formal["mde_ms"] is not None and formal["mde_observed_power"]>=rules["mde"]["power"]
    small=next(x for x in formal["power_curve"] if x["gain_ms"]==.25)
    near=next(x for x in formal["power_curve"] if x["gain_ms"]==formal["mde_ms"])
    large=formal["power_curve"][-1]
    assert small["observed_power"]<near["observed_power"] and large["observed_power"]>=.95
    from bracket_summary import build as build_brackets
    bracket_arms="".join(bracket_schedule(2)); assert bracket_arms=="ABAABA"
    bracket_rows=[{"attempt":i+1,"prompt_id":f"p{i+1}","arm":arm,"t_ms":t} for i,(arm,t) in enumerate(zip(bracket_arms,[10,9,10,11,10,11]))]
    br=build_brackets(bracket_rows,1000,2026091514)
    assert br["batch"]["n"]==2 and br["batch"]["bootstrap_unit"]=="complete_ABA_triple"
    for bad in ([{"attempt":i+1,"arm":arm,"t_ms":10} for i,arm in enumerate("ABBA")], bracket_rows[:3]+[{**x,"prompt_id":"p1"} for x in bracket_rows[3:]]):
        try: build_brackets(bad,10,1); raise AssertionError("invalid/shared bracket accepted")
        except ValueError: pass
    bad_rules=json.loads(json.dumps(rules)); bad_rules["null_calibration"]["positive_false_keep_tolerance"]=[0,0]; bad_formal=formal_statistical_pipeline(synthetic,bad_rules)
    assert not bad_formal["null_calibration_pass"] and bad_formal["mde_ms"] is None
    cfg=rules["null_calibration"]
    assert null_rates_pass(cfg["positive_false_keep_tolerance"][0],cfg["any_direction_rejection_tolerance"][1],cfg)
    assert not null_rates_pass(cfg["positive_false_keep_tolerance"][0]-.0001,cfg["any_direction_rejection_tolerance"][1],cfg)
    drift_values=[10+i*.2 for i in range(24)]; drift=theil_sen(drift_values); drift_p=trend_permutation(drift_values,2000,2026091515)
    assert drift["projected_span_ms"]>2 and drift_p<.05
    ob=[]
    for i in range(12):
        pat="ABBA" if i<6 else "BAAB"; v=(3+i*.01) if pat=="ABBA" else (-3+i*.01)
        ob.append([{"delta_ms":v-.1,"pattern":pat},{"delta_ms":v+.1,"pattern":pat}])
    oe=order_effect_analysis(ob,rules); assert oe["ORDER_EFFECT_MS"]>5 and oe["ORDER_EFFECT_PERMUTATION_P"]<.05
    try: validate_png(b"not png"); raise AssertionError("bad PNG accepted")
    except ValueError: pass
    result={"status":"PASS","production_function":"formal_statistical_pipeline","fixed_seed_reproducible":True,"A_NORMALIZED_WORKFLOW_SHA":a_normalized_workflow_sha,"B_NORMALIZED_WORKFLOW_SHA":b_normalized_workflow_sha,"TIMED_PATH_LABEL_LEAK":timed_path_label_leak,"WORKFLOW_LABEL_LEAK":workflow_label_leak,"HTTP_LABEL_LEAK":http_label_leak,"NULL_GAIN_0":{"positive_false_keep_rate":formal["null_positive_false_keep_rate"],"any_direction_rejection_rate":formal["null_any_direction_rejection_rate"]},"NULL_FAIL_BLOCKS_MDE":"PASS","TOLERANCE_BOUNDARIES":"PASS","SMALL_KNOWN_GAIN":{"gain_ms":.25,"observed_power":small["observed_power"]},"MDE_NEAR_GAIN":{"gain_ms":formal["mde_ms"],"observed_power":near["observed_power"]},"LARGE_KNOWN_GAIN":{"gain_ms":large["gain_ms"],"observed_power":large["observed_power"]},"INDEPENDENT_ABA_CLUSTERED_BRACKET":"PASS","INVALID_OR_SHARED_BRACKET_REJECTED":"PASS","SYNTHETIC_DRIFT":"PASS","ORDER_EFFECT":"PASS"}
    if args.selftest_output: Path(args.selftest_output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False)); return 0

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--selftest",action="store_true"); ap.add_argument("--selftest-output"); ap.add_argument("--execute",action="store_true"); ap.add_argument("--acknowledge-protocol")
    ap.add_argument("--strategy",choices=["AA","E4","E5","E7","TRACK_B_LOCAL_FILE_V2"],default="AA"); ap.add_argument("--batch-id",default="AA-CALIBRATION")
    ap.add_argument("--design",choices=["PAIRED","BRACKET"],default="PAIRED")
    ap.add_argument("--endpoint",default="http://127.0.0.1:8188"); ap.add_argument("--workflow",required=False); ap.add_argument("--fixture",required=False); ap.add_argument("--output-root",default=r"C:\AI\ComfyUI_Aaki_v3\data\output"); ap.add_argument("--evidence-dir"); ap.add_argument("--rules"); ap.add_argument("--order-seed",type=int,default=2026091501); ap.add_argument("--seed-offset",type=int,default=0); ap.add_argument("--blocks",type=int,default=40)
    a=ap.parse_args()
    if a.selftest: return selftest(a)
    if not a.execute or a.acknowledge_protocol!="P0-MEASUREMENT-PROTOCOL-V2": ap.error("formal run requires --execute --acknowledge-protocol P0-MEASUREMENT-PROTOCOL-V2")
    for x in ("workflow","fixture","evidence_dir","rules"):
        if not getattr(a,x): ap.error(f"--{x.replace('_','-')} required")
    return asyncio.run(execute(a))

if __name__=="__main__": raise SystemExit(main())
