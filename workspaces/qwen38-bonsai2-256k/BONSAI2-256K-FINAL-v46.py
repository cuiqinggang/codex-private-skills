#!/usr/bin/env python3
import ctypes, json, subprocess, threading, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(r"C:\AI\Bonsai2-27B-256K")
MODEL = ROOT / r"Bonsai-demo\models\bonsai2-gguf\27B\Ternary-Bonsai-2-27B-PQ2_0.gguf"
SERVER = ROOT / r"runtime-src\llama.cpp-prism-b10709-9a9394a\build-sm75-ivybridge\bin\Release\llama-server.exe"
PRIOR_RUN = ROOT / r"evidence\reality-anchor-extreme-time-20260922-060009"
PROMPT_FILE = PRIOR_RUN / "prompt-242k.txt"
PORT = 18088
BASE = f"http://127.0.0.1:{PORT}"
CTX = 262144
EXPECTED_PROMPT_TOKENS = 242054
EXPECTED_MODEL_BYTES = 7206168928
EXPECTED = {"begin":3817,"middle":6241,"end":9053,"sum":42}
RUN_ID = datetime.now().strftime("%Y%m%d-%H%M%S")
OUT = ROOT / "evidence" / f"bonsai2-256k-v46-final-{RUN_ID}"
OUT.mkdir(parents=True, exist_ok=True)
RESULT = OUT / "RESULT.json"
SERVER_OUT = OUT / "llama-server.stdout.log"
SERVER_ERR = OUT / "llama-server.stderr.log"
MONITOR_CSV = OUT / "resource-monitor.csv"

result = {
    "task":"Bonsai2 256K v4.6 final reality closeout",
    "run_id":RUN_ID,
    "root":str(ROOT),
    "model":str(MODEL),
    "server":str(SERVER),
    "prompt_file":str(PROMPT_FILE),
    "validity":{},
    "server_state":{},
    "timing":{},
    "reuse":{},
    "decode":{"runs":[]},
    "resources":{},
    "reality_delta":"NONE",
    "action":"STOP"
}

def save():
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

def fail(code, message):
    result["validity"]["final"]="FAIL"
    result["validity"]["failure_code"]=code
    result["validity"]["failure_message"]=message
    result["reality_delta"]=code
    save()
    print(f"REALITY_DELTA={code}")
    print(f"DETAIL={message}")
    print("VALID_REAL=FAIL")
    print("ACTION=STOP")
    raise SystemExit(2)

def post(path, body, timeout=1800):
    data=json.dumps(body, separators=(",",":")).encode("utf-8")
    req=Request(BASE+path, data=data, headers={"Content-Type":"application/json"}, method="POST")
    t0=time.perf_counter()
    with urlopen(req, timeout=timeout) as r:
        raw=r.read()
    return json.loads(raw.decode("utf-8")), (time.perf_counter()-t0)*1000.0

def get(path, timeout=10):
    with urlopen(BASE+path, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))

def obj_field(o, name, default=None):
    return o.get(name, default) if isinstance(o, dict) else default

def timing_field(resp, name):
    return obj_field(obj_field(resp, "timings", {}), name, None)

def cached_tokens(resp):
    if isinstance(resp, dict) and "tokens_cached" in resp:
        return int(resp["tokens_cached"])
    usage=obj_field(resp, "usage", {})
    details=obj_field(usage, "prompt_tokens_details", {})
    if isinstance(details, dict) and "cached_tokens" in details:
        return int(details["cached_tokens"])
    return -1

def extract_text(resp):
    if isinstance(resp, dict):
        if resp.get("content") is not None:
            return str(resp["content"])
        choices=resp.get("choices")
        if isinstance(choices, list) and choices:
            c=choices[0]
            if isinstance(c, dict):
                m=c.get("message")
                if isinstance(m, dict) and m.get("content") is not None:
                    return str(m["content"])
                if c.get("text") is not None:
                    return str(c["text"])
    return ""

def strict_verify(text):
    t0=time.perf_counter()
    parsed=None
    reason=""
    try:
        s=text.strip()
        if not (s.startswith("{") and s.endswith("}")):
            raise ValueError("OUTPUT_NOT_SINGLE_JSON_OBJECT")
        parsed=json.loads(s)
        if not isinstance(parsed, dict):
            raise ValueError("JSON_NOT_OBJECT")
        if set(parsed.keys()) != set(EXPECTED.keys()) or len(parsed) != 4:
            raise ValueError("KEY_SET_MISMATCH")
        for k,v in EXPECTED.items():
            if type(parsed.get(k)) is not int or parsed.get(k) != v:
                raise ValueError(f"TYPE_OR_VALUE_MISMATCH_{k}")
        ok=True
    except Exception as e:
        ok=False
        reason=str(e)
    return {"pass":ok,"verify_ms":round((time.perf_counter()-t0)*1000,3),
            "parsed":parsed,"reason":reason}

def validator_selftest():
    cases=[
      ("GOOD_JSON",'{"begin":3817,"middle":6241,"end":9053,"sum":42}',True),
      ("WRONG_BEGIN",'{"begin":3818,"middle":6241,"end":9053,"sum":42}',False),
      ("WRONG_MIDDLE",'{"begin":3817,"middle":6242,"end":9053,"sum":42}',False),
      ("WRONG_END",'{"begin":3817,"middle":6241,"end":9054,"sum":42}',False),
      ("WRONG_SUM",'{"begin":3817,"middle":6241,"end":9053,"sum":43}',False),
      ("MISSING_KEY",'{"begin":3817,"middle":6241,"end":9053}',False),
      ("EXTRA_KEY",'{"begin":3817,"middle":6241,"end":9053,"sum":42,"x":1}',False),
      ("EXTRA_OUTER_TEXT",'answer: {"begin":3817,"middle":6241,"end":9053,"sum":42}',False),
      ("INVALID_JSON",'{"begin":3817,"middle":6241,"end":9053,"sum":}',False),
      ("STRING_NUMBERS",'{"begin":"3817","middle":"6241","end":"9053","sum":"42"}',False),
    ]
    rows=[]
    passed=0
    for name,text,expect in cases:
        got=bool(strict_verify(text)["pass"])
        ok=(got==expect)
        rows.append({"name":name,"expected":expect,"got":got,"pass":ok})
        passed += 1 if ok else 0
    result["validity"]["validator_selftest"]=rows
    result["validity"]["validator_selftest_pass"]=f"{passed}/{len(cases)}"
    save()
    print(f"VALIDATOR_SELFTEST={passed}/{len(cases)} PASS" if passed==len(cases) else f"VALIDATOR_SELFTEST={passed}/{len(cases)} FAIL")
    if passed != len(cases):
        fail("VALIDATOR_SELFTEST_FAIL", f"{passed}/{len(cases)}")

class MemStatus(ctypes.Structure):
    _fields_=[("dwLength",ctypes.c_ulong),("dwMemoryLoad",ctypes.c_ulong),
              ("ullTotalPhys",ctypes.c_ulonglong),("ullAvailPhys",ctypes.c_ulonglong),
              ("ullTotalPageFile",ctypes.c_ulonglong),("ullAvailPageFile",ctypes.c_ulonglong),
              ("ullTotalVirtual",ctypes.c_ulonglong),("ullAvailVirtual",ctypes.c_ulonglong),
              ("ullAvailExtendedVirtual",ctypes.c_ulonglong)]

def avail_ram_mib():
    s=MemStatus(); s.dwLength=ctypes.sizeof(MemStatus)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(s)):
        return None
    return s.ullAvailPhys/1024/1024

def gpu_identity():
    p=subprocess.run(["nvidia-smi","--query-gpu=name,memory.total,memory.used,utilization.gpu",
                      "--format=csv,noheader,nounits"],capture_output=True,text=True)
    line=(p.stdout or "").strip().splitlines()
    if not line: return None
    vals=[x.strip() for x in line[0].split(",")]
    if len(vals)<4:return None
    try:return {"name":vals[0],"total_mib":float(vals[1]),"used_mib":float(vals[2]),"util_pct":float(vals[3])}
    except:return None

def gpu_line():
    p=subprocess.run(["nvidia-smi","--query-gpu=memory.used,utilization.gpu,temperature.gpu,power.draw",
                      "--format=csv,noheader,nounits"],capture_output=True,text=True)
    line=(p.stdout or "").strip().splitlines()
    if not line: return None
    vals=[x.strip() for x in line[0].split(",")]
    if len(vals)<4:return None
    try:return float(vals[0]),float(vals[1]),float(vals[2]),float(vals[3])
    except:return None

stop_mon=threading.Event()
samples=[]
def monitor():
    MONITOR_CSV.write_text("utc,gpu_mem_used_mib,gpu_util_pct,gpu_temp_c,gpu_power_w,avail_ram_mib\n",encoding="utf-8")
    while not stop_mon.is_set():
        g=gpu_line(); a=avail_ram_mib()
        if g:
            row=(datetime.now(timezone.utc).isoformat(),*g,a)
            samples.append(row)
            with MONITOR_CSV.open("a",encoding="utf-8") as f:
                f.write(",".join("" if x is None else str(x) for x in row)+"\n")
        stop_mon.wait(1.0)

def wait_health(proc, timeout=120):
    end=time.time()+timeout
    while time.time()<end:
        if proc.poll() is not None:
            return False
        try:
            if get("/health",2):
                return True
        except Exception:
            pass
        time.sleep(0.25)
    return False

def start_server(kv):
    hp=subprocess.run([str(SERVER),"--help"],capture_output=True,text=True,errors="replace")
    help_text=(hp.stdout or "") + "\n" + (hp.stderr or "")
    required=["--ctx-checkpoints","--checkpoint-min-step","--cache-ram","--cache-idle-slots","--cache-reuse"]
    missing=[x for x in required if x not in help_text]
    if missing:
        fail("CTX_CHECKPOINT_FLAG_UNAVAILABLE", ",".join(missing))
    args=[str(SERVER),"-m",str(MODEL),"-c",str(CTX),"-ngl","99","-np","1","-fa","on",
          "-ctk",kv,"-ctv",kv,
          "--ctx-checkpoints","32","--checkpoint-min-step","8192",
          "--cache-ram","0","--no-cache-idle-slots","--cache-reuse","0",
          "--host","127.0.0.1","--port",str(PORT),"--metrics"]
    if "--device" in help_text: args += ["--device","CUDA0"]
    if "--reasoning " in help_text or "--reasoning\n" in help_text: args += ["--reasoning","off"]
    if "--reasoning-budget" in help_text: args += ["--reasoning-budget","0"]
    if "--reasoning-format" in help_text: args += ["--reasoning-format","none"]
    so=open(SERVER_OUT,"w",encoding="utf-8")
    se=open(SERVER_ERR,"w",encoding="utf-8")
    t0=time.perf_counter()
    proc=subprocess.Popen(args,stdout=so,stderr=se,cwd=str(ROOT))
    ready=wait_health(proc,120)
    ms=(time.perf_counter()-t0)*1000
    if not ready:
        try: proc.kill()
        except: pass
        so.close(); se.close()
        logs=""
        try: logs=SERVER_ERR.read_text(encoding="utf-8",errors="replace")
        except: pass
        return None,ms,args,logs
    return (proc,so,se),ms,args,""

def completion(tokens, name, n_predict=128, cache_prompt=True, ignore_eos=False):
    body={"prompt":tokens,"n_predict":n_predict,"temperature":0,"seed":1,
          "cache_prompt":cache_prompt,"stream":False,"ignore_eos":ignore_eos}
    resp,e2e=post("/completion",body,1800)
    return {
      "name":name,"e2e_ms":round(e2e,3),"response":resp,
      "prompt_ms":timing_field(resp,"prompt_ms"),
      "prompt_per_second":timing_field(resp,"prompt_per_second"),
      "predicted_ms":timing_field(resp,"predicted_ms"),
      "predicted_per_second":timing_field(resp,"predicted_per_second"),
      "cached_tokens":cached_tokens(resp),
      "output":extract_text(resp)
    }

def main():
    validator_selftest()
    for p,n in [(MODEL,"MODEL"),(SERVER,"SERVER"),(PROMPT_FILE,"PROMPT")]:
        if not p.is_file(): fail(f"{n}_MISSING",str(p))
    if MODEL.stat().st_size != EXPECTED_MODEL_BYTES:
        fail("MODEL_SIZE_MISMATCH",str(MODEL.stat().st_size))
    g0=gpu_identity()
    if not g0:
        fail("GPU_PROBE_FAIL","No parseable nvidia-smi semantic output")
    result["server_state"]["gpu_prestart"]=g0
    if "RTX 2080 Ti" not in g0["name"] or g0["total_mib"] < 22000:
        fail("GPU_REALITY_MISMATCH",json.dumps(g0,ensure_ascii=False))
    if g0["used_mib"] > 2500:
        fail("GPU_PRESTART_BUSY",json.dumps(g0,ensure_ascii=False))
    try:
        get("/health",2)
        fail("PORT_IN_USE",BASE)
    except SystemExit:
        raise
    except Exception:
        pass

    mon=threading.Thread(target=monitor,daemon=True); mon.start()
    srv=None
    try:
        started,ready_ms,args,logs=start_server("q8_0")
        kv="q8_0"
        if started is None:
            ll=logs.lower()
            if any(x in ll for x in ["out of memory","failed to allocate","not enough memory"]):
                started,ready_ms,args,logs=start_server("q4_0"); kv="q4_0"
            if started is None: fail("SERVER_READY_FAIL",logs[-3000:])
        proc,so,se=started; srv=(proc,so,se)
        result["server_state"].update({
          "ready_ms":round(ready_ms,3),"kv_mode":kv,"args":args,
          "ctx_checkpoints":32,"checkpoint_min_step":8192,
          "cache_ram_mib":0,"cache_idle_slots":False,"cache_reuse":0
        })
        props=get("/props",10)
        nctx=obj_field(obj_field(props,"default_generation_settings",{}),"n_ctx",None)
        result["server_state"]["props_n_ctx"]=nctx
        if int(nctx or 0) != CTX: fail("CONTEXT_262144_REALITY_GATE_FAIL",str(nctx))
        g1=gpu_identity()
        if not g1:
            fail("GPU_POSTLOAD_PROBE_FAIL","No parseable nvidia-smi semantic output")
        result["server_state"]["gpu_postload"]=g1
        result["server_state"]["gpu_used_delta_mib"]=round(g1["used_mib"]-g0["used_mib"],1)
        if result["server_state"]["gpu_used_delta_mib"] < 5500:
            fail("FULL_GPU_OFFLOAD_REALITY_GATE_FAIL",json.dumps(result["server_state"],ensure_ascii=False))

        prompt_text=PROMPT_FILE.read_text(encoding="utf-8")
        tok_resp,tok_ms=post("/tokenize",{"content":prompt_text,"add_special":True,
                                          "parse_special":True,"with_pieces":False},300)
        toks=tok_resp.get("tokens",[])
        result["timing"]["tokenize_ms"]=round(tok_ms,3)
        result["timing"]["prompt_tokens"]=len(toks)
        if len(toks) != EXPECTED_PROMPT_TOKENS:
            fail("PROMPT_TOKEN_COUNT_DRIFT",f"{len(toks)} != {EXPECTED_PROMPT_TOKENS}")

        print(f"STAGE_START=seed TOKENS={len(toks)}")
        seed=completion(toks,"cold_full_seed",1,True,True)
        result["timing"]["seed"]={k:v for k,v in seed.items() if k!="response"}
        save()
        print(f"STAGE_DONE=seed PROMPT_MS={seed['prompt_ms']} E2E_MS={seed['e2e_ms']}")

        def run_hot(name, tokens):
            print(f"STAGE_START={name}")
            x=completion(tokens,name,128,True,False)
            ver=strict_verify(x["output"])
            x["verify"]=ver
            x["valid"]=bool(ver["pass"])
            x.pop("response",None)
            result["reuse"][name]=x
            save()
            print(f"STAGE_DONE={name} VALID={x['valid']} CACHED={x['cached_tokens']} PROMPT_MS={x['prompt_ms']} E2E_MS={x['e2e_ms']}")
            if not x["valid"]: fail(name.upper()+"_VALIDITY_FAIL",ver["reason"]+" OUTPUT="+x["output"][:500])
            return x

        hot100=run_hot("hot100",list(toks))

        def variant(ratio,repl_index):
            v=list(toks); prefix=int(len(v)*ratio); repl=v[repl_index]
            if repl==v[prefix]: repl=v[repl_index+1]
            v[prefix]=repl
            return v,prefix

        v98,p98=variant(0.98,41); result["reuse"]["hot98_intended_prefix"]=p98
        hot98=run_hot("hot98",v98)
        v95,p95=variant(0.95,53); result["reuse"]["hot95_intended_prefix"]=p95
        hot95=run_hot("hot95",v95)

        for i in range(1,4):
            short=f"Decode benchmark run {i}. Continue with deterministic plain text tokens."
            tr,_=post("/tokenize",{"content":short,"add_special":False,"parse_special":True,"with_pieces":False},60)
            d=completion(tr.get("tokens",[]),f"decode_{i}",128,False,True)
            d.pop("response",None); d.pop("output",None)
            result["decode"]["runs"].append(d); save()

        pps=[float(x["predicted_per_second"]) for x in result["decode"]["runs"] if x.get("predicted_per_second") is not None]
        if len(pps)!=3: fail("DECODE_TIMING_INCOMPLETE",str(pps))
        result["decode"]["median_tps"]=sorted(pps)[1]
        result["decode"]["max_tps"]=max(pps)
        result["validity"]["hot100"]=hot100["valid"]
        result["validity"]["hot98"]=hot98["valid"]
        result["validity"]["hot95"]=hot95["valid"]
        result["validity"]["final"]="PASS"
        save()
    finally:
        if srv:
            proc,so,se=srv
            if proc.poll() is None:
                try: proc.kill(); proc.wait(timeout=10)
                except: pass
            try: so.close(); se.close()
            except: pass
        stop_mon.set()
        try: mon.join(timeout=3)
        except: pass
        if samples:
            result["resources"]={
              "samples":len(samples),
              "peak_gpu_mem_mib":max(x[1] for x in samples),
              "peak_gpu_util_pct":max(x[2] for x in samples),
              "peak_gpu_temp_c":max(x[3] for x in samples),
              "peak_gpu_power_w":max(x[4] for x in samples),
              "min_avail_ram_mib":min(x[5] for x in samples if x[5] is not None)
            }
        save()

    print(f"RUN_DIR={OUT}")
    print(f"RESULT_JSON={RESULT}")
    print(f"KV_MODE={result['server_state'].get('kv_mode')}")
    print(f"SEED_PROMPT_MS={result['timing']['seed'].get('prompt_ms')}")
    for n in ["hot100","hot98","hot95"]:
        x=result["reuse"][n]
        print(f"{n.upper()}_VALID={x['valid']}")
        print(f"{n.upper()}_CACHED_TOKENS={x['cached_tokens']}")
        print(f"{n.upper()}_PROMPT_MS={x['prompt_ms']}")
        print(f"{n.upper()}_E2E_MS={x['e2e_ms']}")
    print(f"DECODE_MEDIAN_TPS={result['decode']['median_tps']}")
    print(f"DECODE_MAX_TPS={result['decode']['max_tps']}")
    print("JEV_A_B=SKIPPED_NOT_CRITICAL_PATH")
    print("VALID_REAL=PASS")
    print("REALITY_DELTA=NONE")
    print("ACTION=STOP")

if __name__=="__main__":
    main()
