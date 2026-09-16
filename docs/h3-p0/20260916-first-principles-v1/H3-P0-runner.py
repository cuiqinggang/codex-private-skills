#!/usr/bin/env python3
"""H3-P0 isolated benchmark: one server, one candidate, reversible timer."""
import argparse, hashlib, json, math, socket, subprocess, time, urllib.request, uuid
from pathlib import Path

ROOT=Path(r"C:\AI\MiniMax-H3")
COMFY=ROOT/"ComfyUI"
PY=ROOT/".venv/Scripts/python.exe"
SAMPLERS=COMFY/"comfy/samplers.py"
CANONICAL=ROOT/"projects/H3-05-xuejing-dukou/06-WORKFLOWS/STATIC-PROBE/k3-fl2va-5f-20step-api.json"
OUTPUT=ROOT/"projects/H3-05-xuejing-dukou/07-RENDERS/e-preflight-output"
INPUT=ROOT/"projects/H3-05-xuejing-dukou/02-EVIDENCE"
TEMP=ROOT/"projects/H3-05-xuejing-dukou/11-ARCHIVE/e-preflight-temp"
BASE="http://127.0.0.1:8194"
CANONICAL_SHA="89B6A40B13485A6633191F1350DB472556359CDB6407E5272C9ED109698FD0F5"
NEEDLE=b"        samples = self.sampler_function(model_k, noise, sigmas, extra_args=extra_args, callback=k_callback, disable=disable_pbar, **self.extra_options)"
PATCH=b"\n".join([
 b"        import time as _p0_time, json as _p0_json",
 b"        _p0_start = torch.cuda.Event(enable_timing=True)",
 b"        _p0_end = torch.cuda.Event(enable_timing=True)",
 b"        torch.cuda.synchronize()",
 b"        _p0_wall = _p0_time.perf_counter()",
 b"        _p0_begin_epoch_ns = _p0_time.time_ns()",
 b"        _p0_start.record()",
 NEEDLE,
 b"        _p0_end.record()",
 b"        _p0_end.synchronize()",
 b"        _p0_end_epoch_ns = _p0_time.time_ns()",
 b"        print('H3_P0_TIMER ' + _p0_json.dumps({'seed': extra_args.get('seed'), 'cuda_ms': _p0_start.elapsed_time(_p0_end), 'wall_ms': (_p0_time.perf_counter()-_p0_wall)*1000, 'start_epoch_ns': _p0_begin_epoch_ns, 'end_epoch_ns': _p0_end_epoch_ns}), flush=True)"
])
def digest(b): return hashlib.sha256(b).hexdigest().upper()
def write(path,obj):
 path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8")
def listen(port):
 with socket.socket() as s:
  s.settimeout(.25); return s.connect_ex(("127.0.0.1",port))==0
def api(path,data=None,timeout=30):
 body=None if data is None else json.dumps(data).encode()
 req=urllib.request.Request(BASE+path,data=body,headers={"Content-Type":"application/json"} if body else {})
 with urllib.request.urlopen(req,timeout=timeout) as response:
  return json.loads(response.read().decode())
def pct(a,q):
 a=sorted(a); x=(len(a)-1)*q; i=int(x)
 return a[i]+(a[min(i+1,len(a)-1)]-a[i])*(x-i)
def restore(evidence):
 backup=evidence/"samplers.py.before"
 if not backup.exists(): raise RuntimeError("missing sampler backup")
 original=backup.read_bytes(); SAMPLERS.write_bytes(original)
 return digest(original)
def graph(evidence,phase,seed,index):
 raw=CANONICAL.read_bytes()
 if digest(raw)!=CANONICAL_SHA: raise RuntimeError("canonical workflow SHA mismatch")
 p=json.loads(raw)
 p["7"]["inputs"].update(width=32,height=32,length=5,prompt="static frame")
 p["7"]["inputs"].pop("first_frame",None); p["7"]["inputs"].pop("last_frame",None)
 del p["5"]; p["11"]["inputs"]["steps"]=1; p["8"]["inputs"]["noise_seed"]=seed
 p["16"]["inputs"]["filename_prefix"]=f"H3-P0/{evidence.name}/{phase}-{index}-{seed}"
 if p["10"]["inputs"]["sampler_name"]!="res_multistep" or p["11"]["inputs"]["scheduler"]!="beta": raise RuntimeError("workflow contract drift")
 if index==0 and phase=="cold": write(evidence/"H3-P0-V1-workflow.json",p)
 return p
def locate(item):
 for value in item.get("outputs",{}).get("16",{}).values():
  if isinstance(value,list):
   for f in value:
    if isinstance(f,dict) and str(f.get("filename","")).lower().endswith(".mp4"):
     return OUTPUT/f.get("subfolder","")/f["filename"]
 raise RuntimeError("node 16 SaveVideo MP4 absent from history")
def qc(path):
 probe=subprocess.run(["ffprobe","-v","error","-count_frames","-show_entries","stream=codec_type,width,height,nb_read_frames","-of","json",str(path)],capture_output=True,text=True,timeout=30,check=True)
 streams=json.loads(probe.stdout).get("streams",[])
 video=[v for v in streams if v.get("codec_type")=="video"]
 if len(video)!=1 or (int(video[0].get("width",0)),int(video[0].get("height",0)),int(video[0].get("nb_read_frames",0)))!=(32,32,5):
  raise RuntimeError(f"video contract mismatch: {streams}")
 raw=subprocess.run(["ffmpeg","-v","error","-i",str(path),"-map","0:v:0","-pix_fmt","rgb24","-f","rawvideo","-"],capture_output=True,timeout=30,check=True).stdout
 if len(raw)!=15360: raise RuntimeError(f"decoded bytes mismatch: {len(raw)}")
 frames=[raw[i:i+3072] for i in range(0,len(raw),3072)]
 means=[sum(f)/3072 for f in frames]
 ranges=[max(f)-min(f) for f in frames]
 stds=[(sum((v-m)**2 for v in f)/3072)**.5 for f,m in zip(frames,means)]
 if any(m<2 for m in means): raise RuntimeError(f"black frame: {means}")
 if any(r<8 or sd<1.5 for r,sd in zip(ranges,stds)): raise RuntimeError(f"flat frame: ranges={ranges}, stds={stds}")
 return {"file":str(path),"sha256":digest(path.read_bytes()),"bytes":path.stat().st_size,"frame_means":means,"frame_ranges":ranges,"frame_stds":stds}
def timer(log,seed):
 found=[]
 for line in log.read_text(encoding="utf-8",errors="replace").splitlines():
  if "H3_P0_TIMER " in line:
   try:
    v=json.loads(line.split("H3_P0_TIMER ",1)[1])
    if v.get("seed")==seed: found.append(v)
   except ValueError: pass
 if len(found)!=1: raise RuntimeError(f"timer count seed={seed}: {len(found)}")
 return found[0]
def one(evidence,phase,seed,index,log):
 p=graph(evidence,phase,seed,index)
 begin=time.perf_counter(); submit_epoch_ns=time.time_ns(); log_offset=log.stat().st_size
 response=api("/prompt",{"prompt":p,"client_id":str(uuid.uuid4())},60)
 if "prompt_id" not in response: raise RuntimeError(f"prompt rejected: {response}")
 pid=response["prompt_id"]; deadline=time.monotonic()+1800
 item=None; output=None
 while time.monotonic()<deadline:
  history=api("/history/"+pid,timeout=10)
  item=history.get(pid,{})
  status=item.get("status",{})
  if any(m and m[0]=="execution_error" for m in status.get("messages",[])):
   raise RuntimeError(f"execution error: {status['messages']}")
  if status.get("completed") is True:
   output=locate(item)
   if output.exists() and output.stat().st_size>0:
    ready=time.perf_counter(); ready_epoch_ns=time.time_ns(); break
  time.sleep(.05)
 else: raise TimeoutError(pid)
 quality=qc(output)
 t=timer(log,seed); generation=t["cuda_ms"]/1000; total=ready-begin
 stages=[]
 with log.open("r",encoding="utf-8",errors="replace") as stage_log:
  stage_log.seek(log_offset)
  for line in stage_log:
   if "H3_P0_STAGE " in line:
    try: stages.append(json.loads(line.split("H3_P0_STAGE ",1)[1]))
    except ValueError: pass
 if not 0<generation<total*1.1: raise RuntimeError(f"inconsistent timer: generation={generation}, total={total}")
 result={"phase":phase,"index":index,"seed":seed,"prompt_id":pid,"total_s":total,"generation_cuda_s":generation,"generation_wall_s":t["wall_ms"]/1000,"path_s":total-generation,"result_ready":"history_completed_and_mp4_exists","submit_epoch_ns":submit_epoch_ns,"ready_epoch_ns":ready_epoch_ns,"path_stage_events":stages,"generation_start_epoch_ns":t["start_epoch_ns"],"generation_end_epoch_ns":t["end_epoch_ns"],"qc":quality,"task_completed":True}
 write(evidence/"runs"/phase/f"run-{index}-{seed}.json",result)
 with (evidence/"runs.jsonl").open("a",encoding="utf-8") as f: f.write(json.dumps(result,ensure_ascii=False)+"\n")
 print(json.dumps({k:result[k] for k in ("phase","seed","total_s","generation_cuda_s","path_s")}),flush=True)
 return result
def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("--evidence",type=Path,required=True)
 parser.add_argument("--phase",default="V1")
 parser.add_argument("--reserve",type=float,default=3.5)
 parser.add_argument("--pinned",choices=("disabled","enabled"),default="disabled")
 parser.add_argument("--runs",type=int,default=3)
 parser.add_argument("--cold",action="store_true")
 parser.add_argument("--restore-only",action="store_true")
 parser.add_argument("--launch-id",default=None)
 args=parser.parse_args(); e=args.evidence; e.mkdir(parents=True,exist_ok=True)
 if args.restore_only:
  print(json.dumps({"samplers_sha_after":restore(e)})); return
 if listen(8194) or listen(8195): raise RuntimeError("8194/8195 listener exists")
 current=SAMPLERS.read_bytes(); backup=e/"samplers.py.before"
 if backup.exists() and backup.read_bytes()!=current: raise RuntimeError("sampler backup mismatch; restore manually")
 if current.count(NEEDLE)!=1 or b"H3_P0_TIMER " in current: raise RuntimeError("sampler boundary drift or already patched")
 if not backup.exists(): backup.write_bytes(current)
 before=digest(current)
 write(e/"sampler-identity.json",{"sha_before":before,"backup":str(backup)})
 SAMPLERS.write_bytes(current.replace(NEEDLE,PATCH,1))
 (e/"instrumentation.patch").write_text(PATCH.decode()+"\n",encoding="utf-8")
 cmd=[str(PY),"-s",str(COMFY/"main.py"),"--listen","127.0.0.1","--port","8194","--output-directory",str(OUTPUT),"--input-directory",str(INPUT),"--temp-directory",str(TEMP),"--fast-disk","--reserve-vram",str(args.reserve)]
 if args.pinned=="disabled": cmd.append("--disable-pinned-memory")
 write(e/f"launch-{args.phase}.json",{"command":cmd,"cwd":str(COMFY)})
 log=e/f"server-{args.phase}.log"; server=None
 try:
  with log.open("w",encoding="utf-8") as handle:
   server=subprocess.Popen(cmd,cwd=COMFY,stdout=handle,stderr=subprocess.STDOUT,creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
   deadline=time.monotonic()+300
   while time.monotonic()<deadline:
    if server.poll() is not None: raise RuntimeError(f"server exited: {server.returncode}")
    try:
     api("/system_stats",timeout=3); break
    except Exception: time.sleep(1)
   else: raise TimeoutError("server startup")
   seeds=([910001] if args.cold else [])+[910002]+([910100,910102,910103,910104,910105,910106,910107,910108,910109,910110][:args.runs])
   results=[]
   for i,seed in enumerate(seeds):
    phase="cold" if args.cold and i==0 else ("warmup" if seed==910002 else args.phase)
    results.append(one(e,phase,seed,i,log))
   valid=[r for r in results if r["phase"]==args.phase]
   summary={"phase":args.phase,"reserve_vram_gib":args.reserve,"pinned_memory":args.pinned,"percentile_method":"linear_interpolation_n_minus_1","valid_warm_runs":len(valid)}
   for name,key in (("generation","generation_cuda_s"),("path","path_s"),("total","total_s")):
    summary[name+"_p50_s"]=pct([r[key] for r in valid],.5)
    summary[name+"_p95_s"]=pct([r[key] for r in valid],.95)
   write(e/f"summary-{args.phase}.json",summary)
   print(json.dumps(summary),flush=True)
 finally:
  if server is not None and server.poll() is None:
   server.terminate()
   try: server.wait(30)
   except subprocess.TimeoutExpired: server.kill(); server.wait(15)
  after=restore(e)
  write(e/"instrumentation-restore-proof.json",{"sha_before":before,"sha_after":after,"restored":before==after})
if __name__=="__main__": main()
