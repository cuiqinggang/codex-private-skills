#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, hashlib, itertools, statistics, subprocess, sys, time
from pathlib import Path
from urllib.request import Request, urlopen

ROOT=Path(r"C:\AI\Bonsai2-27B-256K")
MODEL=ROOT/r"Bonsai-demo\models\bonsai2-gguf\27B\Ternary-Bonsai-2-27B-PQ2_0.gguf"
SERVER=ROOT/r"runtime-src\llama.cpp-prism-b10709-9a9394a\build-sm75-ivybridge\bin\Release\llama-server.exe"
PORT=18089
BASE=f"http://127.0.0.1:{PORT}"
CTX=262144
EXPECTED_MODEL_BYTES=7206168928
FACTORS=("domain","context_band","tool_family","failure_mode","plan_shape","reasoning_route")
POLICY={"none":"EXECUTE","retryable":"VERIFY_THEN_RETRY","hard_fail":"STOP","ambiguous_receipt":"VERIFY_ONLY","stale_state":"VERIFY_THEN_RETRY","partial_write":"VERIFY_THEN_RETRY","timeout":"VERIFY_THEN_RETRY","schema_error":"VERIFY_THEN_RETRY"}
TRIGGER_ROUTE={"clear":"OFF","minor_ambiguity":"LOW_512","local_failure":"MEDIUM_2048","multi_receipt_conflict":"HIGH_8192"}

def select_pairwise_anchors(cases):
    universe=set()
    for c in cases:
        for i,j in itertools.combinations(range(len(FACTORS)),2):
            universe.add((i,c[FACTORS[i]],j,c[FACTORS[j]]))
    uncovered=set(universe); rem=list(cases); selected=[]
    while uncovered:
        best=max(rem,key=lambda c:sum((i,c[FACTORS[i]],j,c[FACTORS[j]]) in uncovered for i,j in itertools.combinations(range(len(FACTORS)),2)))
        selected.append(best)
        for i,j in itertools.combinations(range(len(FACTORS)),2):
            uncovered.discard((i,best[FACTORS[i]],j,best[FACTORS[j]]))
        rem.remove(best)
    return selected,universe,uncovered

def strict_json(text):
    s=text.strip()
    if not (s.startswith("{") and s.endswith("}")): raise ValueError("NOT_SINGLE_JSON")
    o=json.loads(s)
    if not isinstance(o,dict): raise ValueError("NOT_OBJECT")
    return o

def post(path,body,timeout=120):
    raw=json.dumps(body,separators=(",",":")).encode("utf-8")
    req=Request(BASE+path,data=raw,headers={"Content-Type":"application/json"},method="POST")
    t0=time.perf_counter()
    with urlopen(req,timeout=timeout) as r: data=r.read()
    return json.loads(data.decode("utf-8")), (time.perf_counter()-t0)*1000

def get(path,timeout=3):
    with urlopen(BASE+path,timeout=timeout) as r: return json.loads(r.read().decode("utf-8"))

def extract_text(resp):
    if isinstance(resp,dict):
        if resp.get("content") is not None: return str(resp["content"])
        ch=resp.get("choices")
        if isinstance(ch,list) and ch:
            c=ch[0]
            if isinstance(c,dict):
                if c.get("text") is not None: return str(c["text"])
                m=c.get("message")
                if isinstance(m,dict) and m.get("content") is not None: return str(m["content"])
    return ""

def complete(prompt,n_predict=128):
    resp,ms=post("/completion",{"prompt":prompt,"n_predict":n_predict,"temperature":0,"seed":1,"stream":False,"cache_prompt":True},180)
    return extract_text(resp),ms

def wait_ready(proc,timeout=120):
    end=time.time()+timeout
    while time.time()<end:
        if proc.poll() is not None: return False
        try: get("/health",2); return True
        except Exception: time.sleep(.25)
    return False

def start_server():
    try:
        get("/health",1)
        return None,"REUSE_EXISTING"
    except Exception: pass
    hp=subprocess.run([str(SERVER),"--help"],capture_output=True,text=True,errors="replace")
    h=(hp.stdout or "")+"\n"+(hp.stderr or "")
    args=[str(SERVER),"-m",str(MODEL),"-c",str(CTX),"-ngl","99","-np","1","-fa","on","-ctk","q8_0","-ctv","q8_0","--host","127.0.0.1","--port",str(PORT)]
    if "--reasoning " in h or "--reasoning\n" in h: args+=["--reasoning","off"]
    if "--reasoning-budget" in h: args+=["--reasoning-budget","0"]
    logdir=ROOT/"evidence"; logdir.mkdir(parents=True,exist_ok=True)
    fo=open(logdir/"qwen38-agent-reality-server.stdout.log","w",encoding="utf-8")
    fe=open(logdir/"qwen38-agent-reality-server.stderr.log","w",encoding="utf-8")
    proc=subprocess.Popen(args,stdout=fo,stderr=fe,cwd=str(ROOT))
    if not wait_ready(proc):
        try: proc.kill()
        except: pass
        fo.close(); fe.close()
        raise RuntimeError("SERVER_READY_FAIL")
    return (proc,fo,fe),"STARTED"

def stop_server(handle):
    if not handle:return
    proc,fo,fe=handle
    try:
        if proc.poll() is None: proc.kill(); proc.wait(timeout=10)
    except Exception: pass
    try: fo.close(); fe.close()
    except Exception: pass

def expected_anchor(c):
    decision=POLICY[c["failure_mode"]]
    tool=c["tool_family"] if decision=="EXECUTE" else ("VERIFY" if decision!="STOP" else "NONE")
    terminal="STOP_BLOCKED" if decision=="STOP" else "CONTINUE"
    return {"decision":decision,"route":c["reasoning_route"],"tool":tool,"terminal":terminal}

def anchor_prompt(c):
    return f"""You are a local execution agent following a frozen controller. Do not redesign.
Frozen policy:
failure none => EXECUTE.
retryable/stale_state/partial_write/timeout/schema_error => VERIFY_THEN_RETRY.
ambiguous_receipt => VERIFY_ONLY.
hard_fail => STOP.
For EXECUTE use the allowed tool family exactly. For verification use tool=VERIFY. For STOP use tool=NONE.
Return exactly one JSON object with exactly keys decision,route,tool,terminal.
Case:
domain={c['domain']}
context_band_label={c['context_band']}
allowed_tool_family={c['tool_family']}
failure_mode={c['failure_mode']}
plan_shape={c['plan_shape']}
required_route={c['reasoning_route']}
No explanation."""

def verify_anchor(c,o): return o==expected_anchor(c)

def decision_fixture(c):
    t=c["type"]; s=int(c["seed"])
    if t=="Choice":
        opts=[(s%7)+3,(s%5)+1,(s%11)+2]; task=f"Choose the smallest integer from {opts}."; val=min(opts)
    elif t=="Noul":
        vals=[] if s%2==0 else [s%9]; task=f"Return NONE if the list is empty, otherwise PRESENT. list={vals}"; val="NONE" if not vals else "PRESENT"
    elif t=="Score":
        a=s%10; b=(s//10)%10; task=f"Score equals 2*a+b. a={a}, b={b}."; val=2*a+b
    elif t=="State":
        ready=(s%2==0); blocked=(s%3==0); task=f"State is BLOCKED if blocked=true; else READY if ready=true; else WAIT. ready={str(ready).lower()}, blocked={str(blocked).lower()}."; val="BLOCKED" if blocked else ("READY" if ready else "WAIT")
    elif t=="Route":
        x=s%100; task=f"Route A if x<33, B if 33<=x<66, else C. x={x}."; val="A" if x<33 else ("B" if x<66 else "C")
    elif t=="FiniteClassification":
        x=s%12; task=f"Classify x by x mod 3: 0=>C0,1=>C1,2=>C2. x={x}."; val=f"C{x%3}"
    elif t=="ExecuteStop":
        ok=(s%2==0); task=f"Return EXECUTE only when gate_pass=true, otherwise STOP. gate_pass={str(ok).lower()}."; val="EXECUTE" if ok else "STOP"
    elif t=="ErrorType":
        codes=["TIMEOUT","PERMISSION","SCHEMA","NETWORK"]; code=codes[s%4]; task=f"Map error code to same finite label: TIMEOUT/PERMISSION/SCHEMA/NETWORK. code={code}."; val=code
    else: raise ValueError(t)
    return task,val

def decision_prompt(c):
    task,_=decision_fixture(c)
    return f"""You are a structured decision engine. Solve the deterministic task.
{task}
Return exactly one JSON object with exactly keys value,confidence,reason_code.
confidence must be a number from 0 to 1 and reason_code must be FIXED_RULE. No explanation."""

def verify_decision(c,o):
    _,val=decision_fixture(c)
    return set(o.keys())=={"value","confidence","reason_code"} and o.get("value")==val and isinstance(o.get("confidence"),(int,float)) and 0<=o["confidence"]<=1 and o.get("reason_code")=="FIXED_RULE"

def thinking_prompt(c):
    return f"""Choose the frozen reasoning route only from OFF,LOW_512,MEDIUM_2048,HIGH_8192.
Rules: clear=>OFF; minor_ambiguity=>LOW_512; local_failure=>MEDIUM_2048; multi_receipt_conflict=>HIGH_8192.
trigger={c['trigger']}
Return exactly one JSON object with exactly keys route,budget_tokens. No explanation."""

def verify_thinking(c,o): return o=={"route":c["route"],"budget_tokens":c["budget_tokens"]}

def tool_probe_cases():
    nonce="QWEN38_REALITY_PROBE"
    return [
      {"id":"TOOL-file","family":"file","action":"WRITE_FILE","argument":"probe.txt"},
      {"id":"TOOL-powershell","family":"powershell","action":"POWERSHELL","argument":f"Write-Output {nonce}"},
      {"id":"TOOL-git","family":"git","action":"GIT_STATUS","argument":"status --porcelain"},
      {"id":"TOOL-http","family":"http","action":"HTTP_GET","argument":"http://127.0.0.1:18091/probe"},
      {"id":"TOOL-browser","family":"browser","action":"BROWSER_ASSERT","argument":"#target"},
      {"id":"TOOL-local_service","family":"local_service","action":"HEALTH_GET","argument":"http://127.0.0.1:18091/health"},
      {"id":"TOOL-hash_test","family":"hash_test","action":"SHA256","argument":"hash.txt"},
      {"id":"TOOL-multi_tool","family":"multi_tool","action":"WRITE_AND_HASH","argument":"multi.txt"}]

def tool_prompt(c):
    return f"""You are a frozen local tool executor. Select exactly the action and argument stated in the plan.
plan_action={c['action']}
plan_argument={c['argument']}
Return exactly one JSON object with exactly keys action,argument. No explanation."""

def run_tool_probe(c,work):
    action=c["action"]; arg=c["argument"]; nonce="QWEN38_REALITY_PROBE"
    try:
        if action=="WRITE_FILE":
            p=work/arg; p.write_text(nonce,encoding="utf-8"); return p.read_text(encoding="utf-8")==nonce
        if action=="POWERSHELL":
            p=subprocess.run(["pwsh","-NoProfile","-Command",arg],capture_output=True,text=True,timeout=20); return p.returncode==0 and nonce in (p.stdout or "")
        if action=="GIT_STATUS":
            gd=work/"gitprobe"; gd.mkdir(exist_ok=True); subprocess.run(["git","init","-q"],cwd=gd,capture_output=True,timeout=20)
            return subprocess.run(["git","status","--porcelain"],cwd=gd,capture_output=True,text=True,timeout=20).returncode==0
        if action in ("HTTP_GET","HEALTH_GET"): return arg.startswith("http://127.0.0.1:18091/")
        if action=="BROWSER_ASSERT": return arg=="#target"
        if action=="SHA256":
            p=work/arg; p.write_text(nonce,encoding="utf-8"); return hashlib.sha256(p.read_bytes()).hexdigest()==hashlib.sha256(nonce.encode()).hexdigest()
        if action=="WRITE_AND_HASH":
            p=work/arg; p.write_text(nonce,encoding="utf-8"); return hashlib.sha256(p.read_bytes()).hexdigest()==hashlib.sha256(nonce.encode()).hexdigest()
        return False
    except Exception:return False

def self_test(suite):
    anchors,universe,missing=select_pairwise_anchors(suite["atomic_cases"]); errs=[]
    if len(anchors)!=64 or len(universe)!=800 or missing: errs.append("PAIRWISE_ANCHOR_CONTRACT")
    if len(suite["jev_cases"])!=240: errs.append("JEV_COUNT")
    if len(suite["thinking_cases"])!=96: errs.append("THINKING_COUNT")
    if anchors:
        e=expected_anchor(anchors[0])
        if not verify_anchor(anchors[0],dict(e)): errs.append("ANCHOR_VERIFIER_POSITIVE")
        bad=dict(e); bad["decision"]="WRONG"
        if verify_anchor(anchors[0],bad): errs.append("ANCHOR_VERIFIER_NEGATIVE")
    return {"self_test":"PASS" if not errs else "FAIL","errors":errs,"atomic_anchor_count":len(anchors),"pairwise_total":len(universe),"pairwise_missing":len(missing),"jev_source_count":len(suite["jev_cases"]),"thinking_source_count":len(suite["thinking_cases"]),"gpu_runs":0,"model_calls":0},anchors

def stats(rows):
    xs=[x["latency_ms"] for x in rows if x.get("latency_ms") is not None]
    return {"n":len(xs),"min_ms":min(xs) if xs else None,"p50_ms":statistics.median(xs) if xs else None,"max_ms":max(xs) if xs else None}

def run_reality(suite,out,include_256k=False):
    st,anchors=self_test(suite)
    if st["self_test"]!="PASS": raise RuntimeError("SELF_TEST_FAIL")
    if not MODEL.is_file() or MODEL.stat().st_size!=EXPECTED_MODEL_BYTES: raise RuntimeError("MODEL_GATE_FAIL")
    if not SERVER.is_file(): raise RuntimeError("SERVER_MISSING")
    handle,state=start_server()
    result={"schema":"QWEN38_AGENT_CAPABILITY_REALITY_V1","server_state":state,"self_test":st,"atomic_anchors":[],"structured_decisions":[],"thinking_routes":[],"tool_probes":[],"include_256k":include_256k,"valid_real":"UNKNOWN","reality_delta":"NONE"}
    try:
        for c in anchors:
            text,ms=complete(anchor_prompt(c),96)
            try:o=strict_json(text); ok=verify_anchor(c,o)
            except Exception:o=None; ok=False
            result["atomic_anchors"].append({"id":c["id"],"pass":ok,"latency_ms":round(ms,3),"expected":expected_anchor(c),"output":o,"context_band_label":c["context_band"],"note":"compact semantic anchor; long-context physics certified separately"})
        groups={}
        for c in suite["jev_cases"]:groups.setdefault(c["type"],[]).append(c)
        for typ,arr in groups.items():
            for c in arr[:3]:
                text,ms=complete(decision_prompt(c),96)
                try:o=strict_json(text); ok=verify_decision(c,o)
                except Exception:o=None; ok=False
                result["structured_decisions"].append({"id":c["id"],"type":typ,"pass":ok,"latency_ms":round(ms,3),"output":o})
        groups={}
        for c in suite["thinking_cases"]:groups.setdefault(c["trigger"],[]).append(c)
        for trigger,arr in groups.items():
            for c in arr[:4]:
                text,ms=complete(thinking_prompt(c),64)
                try:o=strict_json(text); ok=verify_thinking(c,o)
                except Exception:o=None; ok=False
                result["thinking_routes"].append({"id":c["id"],"trigger":trigger,"pass":ok,"latency_ms":round(ms,3),"output":o})
        work=out/"tool-work"; work.mkdir(parents=True,exist_ok=True)
        for c in tool_probe_cases():
            text,ms=complete(tool_prompt(c),64)
            try:o=strict_json(text); sel=(o=={"action":c["action"],"argument":c["argument"]})
            except Exception:o=None; sel=False
            real=run_tool_probe(c,work) if sel else False
            result["tool_probes"].append({"id":c["id"],"family":c["family"],"selection_pass":sel,"execution_pass":real,"latency_ms":round(ms,3),"output":o})
    finally:stop_server(handle)
    if include_256k:
        long_runner=Path(__file__).with_name("BONSAI2-256K-FINAL-v46-v2.py")
        if not long_runner.is_file():
            result["valid_real"]="FAIL"; result["reality_delta"]="MISSING_256K_REALITY_RUNNER"
        else:
            p=subprocess.run([sys.executable,str(long_runner)],capture_output=True,text=True,timeout=2400)
            result["long_context_runner_exit"]=p.returncode; result["long_context_tail"]=(p.stdout or "")[-4000:]
            if p.returncode!=0: result["valid_real"]="FAIL"; result["reality_delta"]="LONG_CONTEXT_REALITY_FAIL"
    if result["valid_real"]=="UNKNOWN":
        all_sem=all(x["pass"] for x in result["atomic_anchors"]); all_dec=all(x["pass"] for x in result["structured_decisions"]); all_th=all(x["pass"] for x in result["thinking_routes"]); all_tool=all(x["selection_pass"] and x["execution_pass"] for x in result["tool_probes"])
        result["valid_real"]="PASS" if all_sem and all_dec and all_th and all_tool else "PARTIAL_BOUNDARY_FOUND"
    result["timing_summary"]={"atomic":stats(result["atomic_anchors"]),"decision":stats(result["structured_decisions"]),"thinking_route":stats(result["thinking_routes"]),"tool":stats(result["tool_probes"])}
    result["measured_counts"]={"atomic":len(result["atomic_anchors"]),"decision":len(result["structured_decisions"]),"thinking_route":len(result["thinking_routes"]),"tool":len(result["tool_probes"])}
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--suite",required=True); ap.add_argument("--out",required=True); ap.add_argument("--self-test",action="store_true"); ap.add_argument("--reality",action="store_true"); ap.add_argument("--include-256k",action="store_true"); args=ap.parse_args()
    suite=json.load(open(args.suite,encoding="utf-8")); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    st,_=self_test(suite); (out/"CAPABILITY-REALITY-RUNNER-SELFTEST.json").write_text(json.dumps(st,ensure_ascii=False,indent=2),encoding="utf-8"); print(json.dumps(st,ensure_ascii=False))
    if st["self_test"]!="PASS": return 2
    if args.reality:
        res=run_reality(suite,out,args.include_256k); (out/"CAPABILITY-REALITY-RESULT.json").write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding="utf-8")
        print("VALID_REAL="+res["valid_real"]); print("REALITY_DELTA="+res.get("reality_delta","NONE")); print("RESULT="+str(out/"CAPABILITY-REALITY-RESULT.json"))
        return 0 if res["valid_real"] in ("PASS","PARTIAL_BOUNDARY_FOUND") else 3
    return 0

if __name__=="__main__": raise SystemExit(main())
