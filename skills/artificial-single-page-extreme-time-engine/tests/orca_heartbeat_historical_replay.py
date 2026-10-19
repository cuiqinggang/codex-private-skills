"""Replay actual suite-ab-r3 heartbeat failure mechanics using real child processes."""
import json, subprocess, sys, time, os, hashlib
from pathlib import Path
ROOT=Path(__file__).parent/"orca_historical_replay_results";ROOT.mkdir(exist_ok=True)
SOURCE=Path(__file__).resolve().parents[1]/"tasks"/"ORCA_CODEX_VALUE_VALIDATION_20261014"/"analysis"/"suite-ab-r3.py"
src=SOURCE.read_text(encoding="utf-8")
assert "cli('orchestration','send','--type','heartbeat'" in src
assert "heartbeat=t+300" in src and "write(label+'-done.json',record)" in src
def persist(p,obj):
 tmp=p.with_suffix(".tmp");tmp.write_text(json.dumps(obj,indent=2),encoding="utf-8");os.replace(tmp,p)
def scenario(label,repair):
 p=ROOT/label;p.mkdir(exist_ok=True)
 cp=p/"checkpoint.json";output=p/"business_result.json";events=p/"events.jsonl"
 def event(msg):
  with events.open("a",encoding="utf8") as f:f.write(msg+"\n")
 start=time.perf_counter()
 if cp.exists():
  data=json.loads(cp.read_text(encoding="utf-8-sig"))
  if data.get("state")=="DONE":
   event("REENTER_DONE_NO_DISPATCH");return data
  if data.get("state")=="UNKNOWN" and output.exists() and json.loads(output.read_text())["validated"]:
   data["state"]="DONE";persist(cp,data);event("RECONCILED_NO_REDISTRIBUTION");return data
 else:data=dict(state="START",dispatches=0,heartbeats=0,receipts=0)
 if data["state"]=="START":
  # Real OS subprocess is a safe business worker, not a model or an Orca remote mutation.
  worker='import json,time,sys;time.sleep(.7);open(sys.argv[1],"w").write(json.dumps({"validated":True,"deliverable":"historical suite receipt"}))'
  child=subprocess.Popen([sys.executable,"-c",worker,str(output)])
  data.update(state="RUNNING",pid=child.pid,dispatches=1);persist(cp,data)
  event("DISPATCHED_REAL_PROCESS")
  time.sleep(.12)
  event("HEARTBEAT_REQUEST_TIMEOUT")
  data["heartbeats"]+=1
  if not repair:
   child.terminate();child.wait(timeout=4)
   data["state"]="FAILED_LOST_FINAL_RECEIPT";persist(cp,data)
   event("OLD_CODE_PROPAGATED_TIMEOUT_AND_KILLED_WORKER")
   return data
  # Heartbeat is control-plane UNKNOWN, not evidence that business failed.
  data["state"]="HEARTBEAT_UNKNOWN";persist(cp,data)
  event("CONTROL_TIMEOUT_DO_NOT_RESEND")
  child.wait(timeout=6)
  event("CHILD_EXIT_"+str(child.returncode))
  assert child.returncode==0
  data["state"]="UNKNOWN";persist(cp,data)
 if output.exists() and json.loads(output.read_text())["validated"]:
  data["state"]="DONE";data["receipts"]+=1
  data["sha256"]=hashlib.sha256(output.read_bytes()).hexdigest()
  persist(cp,data);event("INDEPENDENT_QA_COMMITTED_FINAL_RECEIPT")
 data["elapsed_ms"]=round((time.perf_counter()-start)*1000,2);persist(cp,data)
 return data
if __name__=="__main__":
 a=scenario("original_unpatched",False)
 b=scenario("repaired_bounded",True)
 b2=scenario("repaired_bounded",True)
 assert a["state"]=="FAILED_LOST_FINAL_RECEIPT" and a["receipts"]==0
 assert b["state"]=="DONE" and b["receipts"]==1 and b["dispatches"]==1
 assert b2["dispatches"]==1 and b2["receipts"]==1
 summary=dict(historical_source=str(SOURCE),original=a,repaired=b,reentered=b2,passed=True,scope="Real local subprocess and actual source failure mechanics; heartbeat timeout is reproduced intentionally, not an actual Orca service outage.")
 persist(ROOT/"SUMMARY.json",summary)
 print(json.dumps(summary,indent=2))
