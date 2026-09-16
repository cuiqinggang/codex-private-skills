#!/usr/bin/env python3
"""Independent, resumable controller for one H3-P0 GPU benchmark at a time."""
import argparse, hashlib, json, os, socket, subprocess, sys, threading, time, uuid
from pathlib import Path
import psutil

RUNNER=Path(r"C:\Users\A\Documents\Codex\codex-private-skills\docs\h3-p0\20260916-first-principles-v1\H3-P0-runner.py")
PY=Path(r"C:\AI\MiniMax-H3\.venv\Scripts\python.exe")
PROFILE=RUNNER.with_name("H3-P0-profile-runner.py")
VAE_STAGE=RUNNER.with_name("H3-P0-vae-stage-runner.py")
VAE_FULL=RUNNER.with_name("H3-P0-vae-full-runner.py")
SOFTWARE=RUNNER.with_name("H3-P0-software-runner.py")
GEN_PROFILE=RUNNER.with_name("H3-P0-generation-profile-runner.py")
OP_PROFILE=RUNNER.with_name("H3-P0-op-profile-runner.py")
PHASES=[
 {"phase":"V4_RESERVE0_5","reserve":0.5,"pinned":"disabled","reason":"K1 model residency 1.0 to 0.5 GiB"},
 {"phase":"V5_PINNED","reserve":"LAST_GOOD","pinned":"enabled","reason":"K2 pinned transfer on last stable reserve"},
 {"phase":"V6_PATH_PROFILE","reserve":1.0,"pinned":"disabled","kind":"DIAGNOSTIC","reason":"V3 PATH segmented timing only"},
 {"phase":"V7_VAE_STAGE","reserve":1.0,"pinned":"disabled","kind":"VAE_STAGE","reason":"V3 VAE stage and dynamic residency attribution"},
 {"phase":"V8_VAE_FULL_SINGLE","reserve":1.0,"pinned":"disabled","kind":"PATCHED_CANDIDATE","reason":"single GPU full VAE load to test dynamic residency cost"},
 {"phase":"V9_SOFTWARE_036","reserve":1.0,"pinned":"disabled","kind":"SOFTWARE","reason":"official ComfyUI v0.36.0 plus comfy-kitchen 0.2.34 isolated software frontier"},
 {"phase":"V10_GENERATION_PROFILE","reserve":1.0,"pinned":"disabled","kind":"GEN_PROFILE","reason":"V3 core generation CUDA event and H3 weight residency attribution"},
 {"phase":"V11_OP_PROFILE","reserve":1.0,"pinned":"disabled","kind":"OP_PROFILE","reason":"V3 torch profiler CUDA/CPU operator attribution inside DiT"},
]
STATES={"IDLE","STARTING","WARMUP","MEASURING","QC","DECIDING","KEEP","ROLLBACK","CHECKPOINTED","NEXT_ITERATION","CERTIFICATION","DONE"}
HEARTBEAT_STALE_S=120
def now(): return time.time()
def read(p,default=None):
 try: return json.loads(Path(p).read_text(encoding="utf-8"))
 except FileNotFoundError: return default
def save(p,obj):
 p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
 temp=p.with_name(p.name+f".{os.getpid()}.{threading.get_ident()}.tmp")
 temp.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8")
 for attempt in range(20):
  try:
   os.replace(temp,p); return
  except PermissionError:
   if attempt==19: raise
   time.sleep(.1)
def alive(pid,created=None):
 if not pid: return False
 try:
  proc=psutil.Process(int(pid))
  return proc.is_running() and (created is None or abs(proc.create_time()-created)<2)
 except psutil.AccessDenied: return True
 except (psutil.NoSuchProcess,ValueError): return False
def listener():
 try:
  for c in psutil.net_connections(kind="tcp"):
   if c.status=="LISTEN" and c.laddr and c.laddr.port==8194: return c.pid or -1
 except psutil.AccessDenied: pass
 with socket.socket() as sock:
  sock.settimeout(.2)
  return -1 if sock.connect_ex(("127.0.0.1",8194))==0 else None
def active_h3(e):
 found=[]
 for proc in psutil.process_iter(["pid","name"]):
  if str(proc.info.get("name","")).lower() not in ("python.exe","pythonw.exe"): continue
  try: cmd=" ".join(proc.cmdline()).lower()
  except psutil.NoSuchProcess: continue
  except psutil.AccessDenied: raise RuntimeError(f"Cannot inspect Python PID {proc.pid}; fail closed")
  if (("h3-p0-runner.py" in cmd or "h3-p0-profile-runner.py" in cmd or "h3-p0-vae-stage-runner.py" in cmd or "h3-p0-vae-full-runner.py" in cmd or "h3-p0-software-runner.py" in cmd or "h3-p0-generation-profile-runner.py" in cmd or "h3-p0-op-profile-runner.py" in cmd) and str(e).lower() in cmd) or ("minimax-h3" in cmd and "main.py" in cmd and "8194" in cmd):
   found.append(proc.pid)
 return found
def launch_matches(e,lock):
 launch_id=lock.get("launch_id") or read(e/"state.json",{}).get("launch_id")
 if not launch_id: return []
 record=read(e/f"controller-command-{lock.get('current_iteration')}.json",{})
 launched=record.get("time",0)
 matches=[]
 for proc in psutil.process_iter(["pid","name"]):
  if str(proc.info.get("name","")).lower() not in ("python.exe","pythonw.exe"): continue
  try:
   cmd=proc.cmdline()
   if launch_id in cmd and proc.create_time()>=launched-2: matches.append({"pid":proc.pid,"created":proc.create_time(),"launch_id":launch_id})
  except psutil.NoSuchProcess: continue
  except psutil.AccessDenied: raise RuntimeError(f"cannot identify launch process PID {proc.pid}")
 return matches

def recent_progress(e,seconds=HEARTBEAT_STALE_S):
 paths=list(e.glob("server-*.log"))+list(e.glob("summary-*.json"))+list((e/"runs").rglob("run-*.json"))
 return any(now()-path.stat().st_mtime<=seconds for path in paths)
def complete(e,phase):
 summary=read(e/f"summary-{phase}.json")
 if not summary or summary.get("valid_warm_runs")!=3: return False
 files=list((e/"runs"/phase).glob("run-*.json"))
 rows=[read(f,{}) for f in files]
 needed=("generation_p50_s","generation_p95_s","path_p50_s","path_p95_s","total_p50_s","total_p95_s")
 if len(rows)!=3 or sorted(r.get("seed") for r in rows)!=[910100,910102,910103]: return False
 if not all(isinstance(summary.get(k),(int,float)) and summary[k]>0 for k in needed): return False
 if not all(r.get("task_completed") is True and len(r.get("qc",{}).get("frame_ranges",[]))==5 and min(r["qc"]["frame_ranges"])>=8 for r in rows): return False
 proof=read(e/"instrumentation-restore-proof.json",{})
 if phase=="V8_VAE_FULL_SINGLE":
  candidate_proof=read(e/"v8-candidate-proof.json",{})
  if candidate_proof.get("restored") is not True or candidate_proof.get("sha_before")!=candidate_proof.get("sha_after"): return False
 if phase=="V7_VAE_STAGE":
  profile=read(e/f"vae-stage-{phase}.json",{})
  restore=read(e/"vae-stage-proof.json",{})
  if profile.get("qc_pass") is not True or restore.get("restored") is not True or not all(x.get("sha_before")==x.get("sha_after") for x in restore.get("files",[])) or not all(len(r.get("path_stage_events",[]))>=4 for r in rows): return False
 if phase=="V11_OP_PROFILE":
  profile=read(e/f"op-profile-{phase}.json",{})
  if profile.get("qc_pass") is not True or not all(any(v.get("stage")=="T_GENERATION_OP_PROFILE" for v in r.get("path_stage_events",[])) for r in rows): return False
 if phase=="V10_GENERATION_PROFILE":
  profile=read(e/f"generation-profile-{phase}.json",{})
  restore=read(e/"generation-profile-proof.json",{})
  if profile.get("qc_pass") is not True or restore.get("restored") is not True or not all(x.get("sha_before")==x.get("sha_after") for x in restore.get("files",[])) or not all(any(v.get("stage")=="T_GENERATION_PROFILE" for v in r.get("path_stage_events",[])) for r in rows): return False
 if phase=="V6_PATH_PROFILE":
  profile=read(e/f"path-profile-{phase}.json",{})
  restore=read(e/"profile-instrumentation-proof.json",{})
  if profile.get("qc_pass") is not True or restore.get("restored") is not True or not all(x.get("sha_before")==x.get("sha_after") for x in restore.get("files",[])) or not all(len(r.get("path_stage_events",[]))>=5 for r in rows): return False
 return proof.get("restored") is True and proof.get("sha_before")==proof.get("sha_after")
def status(e):
 data={name:read(e/name,{}) for name in ("state.json","pid.json","heartbeat.json","iteration.json","last-good.json")}
 data["lock_exists"]=(e/"controller.lock").exists()
 data["listener_8194_pid"]=listener()
 data["controller_alive"]=alive(data["pid.json"].get("controller_pid"),data["pid.json"].get("controller_start_time",data["pid.json"].get("controller_created")))
 data["runner_alive"]=alive(data["pid.json"].get("runner_pid"),data["pid.json"].get("runner_start_time",data["pid.json"].get("runner_created")))
 data["heartbeat_age_s"]=None if not data["heartbeat.json"] else round(now()-data["heartbeat.json"].get("time",0),1)
 return data
def transition(e,name,**extra):
 if name not in STATES: raise ValueError(name)
 value={"state":name,"updated":now(),**extra}
 save(e/"state.json",value)
 return value
def acquire(e):
 path=e/"controller.lock"
 iteration=read(e/"iteration.json",{})
 identity={"pid":os.getpid(),"created":psutil.Process().create_time(),"controller_pid":os.getpid(),"controller_start_time":psutil.Process().create_time(),"runner_pid":None,"runner_start_time":None,"launch_id":None,"current_iteration":iteration.get("phase"),"heartbeat_path":str(e/"heartbeat.json"),"token":str(uuid.uuid4()),"time":now()}
 try:
  fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL)
 except FileExistsError:
  old=read(path,{})
  if alive(old.get("pid"),old.get("created")):
   raise RuntimeError(f"controller already active pid={old.get('pid')}")
  st=status(e)
  # A STARTING state is ambiguous until both process and result evidence are checked.
  if alive(old.get("runner_pid"),old.get("runner_start_time")) or st["runner_alive"] or launch_matches(e,old) or st["listener_8194_pid"] is not None or active_h3(e):
   raise RuntimeError("stale-process gate: runner or 8194 still active")
  prior_phase=old.get("current_iteration") or read(e/"state.json",{}).get("phase")
  completed=bool(prior_phase and complete(e,prior_phase) and prior_phase in read(e/"iteration.json",{}).get("checkpointed",[]) and read(e/"state.json",{}).get("state") in ("IDLE","CHECKPOINTED"))
  if not completed:
   if st["heartbeat_age_s"] is None or st["heartbeat_age_s"]<=HEARTBEAT_STALE_S:
    raise RuntimeError("stale-process gate: heartbeat not proven stale")
   if recent_progress(e):
    raise RuntimeError("stale-process gate: result/log activity still recent")
  guard=e/"recovery.guard"
  try: gfd=os.open(guard,os.O_WRONLY|os.O_CREAT|os.O_EXCL)
  except FileExistsError: raise RuntimeError("another stale-lock recovery is in progress")
  try:
   os.close(gfd)
   locked=read(path,{})
   if alive(locked.get("pid"),locked.get("created")) or alive(locked.get("runner_pid"),locked.get("runner_start_time")) or launch_matches(e,locked) or active_h3(e) or listener() is not None or (not completed and recent_progress(e)):
    raise RuntimeError("lock recovery gate changed during recovery")
   kind="completed" if completed else "stale"
   archived=e/f"controller.lock.{kind}-{int(now())}"
   path.rename(archived)
   save(e/f"lock-recovery-{int(now())}.json",{"kind":kind,"phase":prior_phase,"archived_lock":str(archived),"time":now(),"old_owner":locked})
   fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL)
  finally:
   guard.unlink(missing_ok=True)
 with os.fdopen(fd,"w",encoding="utf-8") as f: json.dump(identity,f)
 return identity
def release(e,identity):
 if read(e/"controller.lock",{}).get("token")==identity["token"]:
  (e/"controller.lock").unlink()
def bootstrap(e):
 if (e/"state.json").exists(): return
 base=read(e/"summary-V3_RESERVE1.json")
 if not base or not complete(e,"V3_RESERVE1"): raise RuntimeError("V3 complete evidence required")
 last={"phase":"V3_RESERVE1","reserve":1.0,"pinned":"disabled","summary":base,"decision":"KEEP","updated":now()}
 save(e/"last-good.json",last)
 save(e/"iteration.json",{"index":0,"phase":PHASES[0]["phase"],"attempts":0,"checkpointed":["V1_QC","V2_RESERVE2","V3_RESERVE1"]})
 save(e/"pid.json",{"controller_pid":None,"runner_pid":None})
 save(e/"heartbeat.json",{"time":0})
 transition(e,"CHECKPOINTED",phase="V3_RESERVE1",decision="KEEP")
def runs(e,phase):
 return {r["seed"]:r for f in (e/"runs"/phase).glob("run-*.json") if (r:=read(f,{})).get("task_completed")}
def decide(e,candidate,last):
 summary=read(e/f"summary-{candidate['phase']}.json")
 prior=last["summary"]
 a,b=runs(e,last["phase"]),runs(e,candidate["phase"])
 seeds=sorted(set(a)&set(b))
 if len(seeds)!=3: return "ROLLBACK",{"reason":"three matched valid seeds absent"}
 gains=[a[s]["total_s"]-b[s]["total_s"] for s in seeds]
 ordered=sorted(gains); median=ordered[1]
 p50_gain=prior["total_p50_s"]-summary["total_p50_s"]
 accepted=p50_gain>0.5 and median>0.5 and sum(x>0 for x in gains)>=2
 return ("KEEP" if accepted else "ROLLBACK"),{"matched_seeds":seeds,"paired_total_gains_s":gains,"paired_median_gain_s":median,"p50_total_gain_s":p50_gain,"rule":"P50 and paired median >0.5s; at least 2/3 matched seeds faster; all QC pass"}
def heartbeat_loop(e,stop):
 while not stop.is_set():
  pid=read(e/"pid.json",{})
  state=read(e/"state.json",{})
  save(e/"heartbeat.json",{"time":now(),"controller_pid":os.getpid(),"runner_pid":pid.get("runner_pid"),"launch_id":pid.get("launch_id"),"state":state.get("state")})
  stop.wait(5)
def observe_runner(e,phase,proc,launched):
 warmup=e/"runs"/"warmup"/"run-0-910002.json"
 while proc.poll() is None:
  port=listener()
  pid=read(e/"pid.json",{})
  if port is not None and pid.get("server_pid")!=port:
   pid["server_pid"]=port; save(e/"pid.json",pid)
  if warmup.exists() and warmup.stat().st_mtime>=launched: transition(e,"MEASURING",phase=phase,runner_pid=proc.pid)
  elif (e/f"server-{phase}.log").exists(): transition(e,"WARMUP",phase=phase,runner_pid=proc.pid)
  time.sleep(5)
 return proc.returncode
def run_phase(e,candidate):
 phase=candidate["phase"]
 if complete(e,phase): return 0
 st=status(e)
 if st["runner_alive"] or st["listener_8194_pid"] is not None or active_h3(e):
  raise RuntimeError("GPU_EXCLUSIVE gate: another runner or 8194 listener active")
 launch_id=str(uuid.uuid4())
 cmd=[str(PY),str(OP_PROFILE if candidate.get("kind")=="OP_PROFILE" else GEN_PROFILE if candidate.get("kind")=="GEN_PROFILE" else SOFTWARE if candidate.get("kind")=="SOFTWARE" else VAE_FULL if candidate.get("kind")=="PATCHED_CANDIDATE" else VAE_STAGE if candidate.get("kind")=="VAE_STAGE" else PROFILE if candidate.get("kind")=="DIAGNOSTIC" else RUNNER),"--evidence",str(e),"--phase",phase,"--reserve",str(candidate["reserve"]),"--pinned",candidate["pinned"],"--runs","3","--launch-id",launch_id]
 launched=now()
 command_hash=hashlib.sha256(json.dumps(cmd,ensure_ascii=False,separators=(",",":")).encode()).hexdigest()
 intent={"phase":phase,"launch_id":launch_id,"controller_pid":os.getpid(),"controller_start_time":psutil.Process().create_time(),"intended_command_hash":command_hash,"runner_pid":None,"runner_start_time":None}
 transition(e,"STARTING",**intent)
 save(e/"pid.json",intent)
 lock=read(e/"controller.lock",{})
 lock.update({"runner_pid":None,"runner_start_time":None,"launch_id":launch_id,"current_iteration":phase,"intended_command_hash":command_hash,"heartbeat_path":str(e/"heartbeat.json")})
 save(e/"controller.lock",lock)
 save(e/f"controller-command-{phase}.json",{"cmd":cmd,"time":launched,**intent})
 with (e/f"controller-{phase}.log").open("a",encoding="utf-8") as log:
  proc=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
  runner_start=psutil.Process(proc.pid).create_time()
  identity={**intent,"runner_pid":proc.pid,"runner_start_time":runner_start}
  save(e/"pid.json",identity)
  lock=read(e/"controller.lock",{})
  lock.update({"runner_pid":proc.pid,"runner_start_time":runner_start,"launch_id":launch_id,"current_iteration":phase})
  save(e/"controller.lock",lock)
  return observe_runner(e,phase,proc,launched)
def execute(e):
 bootstrap(e)
 identity=acquire(e)
 stop=threading.Event()
 worker=threading.Thread(target=heartbeat_loop,args=(e,stop),daemon=True)
 worker.start()
 abnormal=False
 try:
  save(e/"pid.json",{"controller_pid":os.getpid(),"controller_start_time":psutil.Process().create_time(),"runner_pid":None})
  request=e/"stop-request.json"
  if request.exists(): request.rename(e/f"stop-request.consumed-{int(now())}.json")
  iteration=read(e/"iteration.json")
  if iteration.get("halted"):
   transition(e,"IDLE",reason="candidate failure checkpoint requires review"); return
  while iteration["index"]<len(PHASES):
   if (e/"stop-request.json").exists():
    transition(e,"IDLE",reason="stop-safe requested at checkpoint"); return
   candidate=dict(PHASES[iteration["index"]])
   last=read(e/"last-good.json")
   if candidate["reserve"]=="LAST_GOOD": candidate["reserve"]=last["reserve"]
   if iteration.get("phase")!=candidate["phase"]:
    iteration["phase"]=candidate["phase"]; save(e/"iteration.json",iteration)
   transition(e,"NEXT_ITERATION",phase=candidate["phase"],from_phase=last["phase"])
   rc=run_phase(e,candidate)
   transition(e,"QC",phase=candidate["phase"],runner_rc=rc)
   if rc!=0 or not complete(e,candidate["phase"]):
    decision="ROLLBACK"; detail={"reason":"runner failed or 3 valid QC runs absent","runner_rc":rc}
    transition(e,decision,phase=candidate["phase"],detail=detail)
    save(e/f"decision-{candidate['phase']}.json",{"decision":decision,"detail":detail,"time":now()})
    transition(e,"CHECKPOINTED",phase=candidate["phase"],decision=decision)
    iteration["attempts"]+=1; iteration["checkpointed"].append(candidate["phase"]); iteration["halted"]=True; save(e/"iteration.json",iteration)
    return
   transition(e,"DECIDING",phase=candidate["phase"])
   decision,detail=("DIAGNOSTIC_ONLY",{"reason":"diagnostic attribution; baseline V3 retained"}) if candidate.get("kind") in ("DIAGNOSTIC","VAE_STAGE","GEN_PROFILE","OP_PROFILE") else decide(e,candidate,last)
   transition(e,"CHECKPOINTED" if decision=="DIAGNOSTIC_ONLY" else decision,phase=candidate["phase"],detail=detail)
   save(e/f"decision-{candidate['phase']}.json",{"decision":decision,"detail":detail,"time":now()})
   if decision=="KEEP":
    save(e/"last-good.json",{"phase":candidate["phase"],"reserve":candidate["reserve"],"pinned":candidate["pinned"],"software":"ComfyUI v0.36.0 + comfy-kitchen 0.2.34" if candidate.get("kind")=="SOFTWARE" else "baseline","summary":read(e/f"summary-{candidate['phase']}.json"),"decision":"KEEP","updated":now()})
   iteration["attempts"]+=1; iteration["checkpointed"].append(candidate["phase"]); iteration["index"]+=1
   iteration["phase"]=PHASES[iteration["index"]]["phase"] if iteration["index"]<len(PHASES) else None
   save(e/"iteration.json",iteration)
   transition(e,"CHECKPOINTED",phase=candidate["phase"],decision=decision)
  transition(e,"IDLE",reason="planned candidates complete; gap audit required")
 except BaseException:
  abnormal=True
  raise
 finally:
  stop.set(); worker.join(10)
  if abnormal or active_h3(e) or listener() is not None:
   save(e/"controller-exit-held-lock.json",{"time":now(),"reason":"abnormal exit or child or 8194 still active","pid":read(e/"pid.json",{})})
  else:
   save(e/"pid.json",{"controller_pid":None,"runner_pid":None,"stopped":now()})
   save(e/"heartbeat.json",{"time":now(),"controller_pid":None,"runner_pid":None,"state":read(e/"state.json",{}).get("state")})
   release(e,identity)
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--evidence",type=Path,required=True)
 mode=p.add_mutually_exclusive_group(required=True)
 mode.add_argument("--resume",action="store_true")
 mode.add_argument("--status",action="store_true")
 mode.add_argument("--stop-safe",action="store_true")
 args=p.parse_args(); e=args.evidence
 if args.status:
  print(json.dumps(status(e),ensure_ascii=False,indent=2)); return
 if args.stop_safe:
  save(e/"stop-request.json",{"requested":now(),"mode":"after-current-run"})
  print(json.dumps({"stop_safe":"requested","status":status(e)},ensure_ascii=False)); return
 execute(e)
if __name__=="__main__": main()
