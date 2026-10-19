"""Historical T03 repair/recovery test, isolated from original validated artifact."""
import json,shutil,subprocess,sys,time,hashlib
from pathlib import Path
HERE=Path(__file__).parent
OLD=Path(r"C:\AI\Orca-Codex-Validation-20261014\business-exec-20261015-r3\recovery-r1\before\scripts\run.py")
GOOD=Path(r"C:\AI\Orca-Codex-Validation-20261014\business-exec-20261015-r3\worktrees\fixture\component\scripts\run.py")
ROOT=Path(r"C:\Users\A\Desktop\SRX_V3_ReadPack\T03_REPLAY_20261019")
CP=ROOT/"historical_replay_checkpoint.json"
def save(s):CP.write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding="utf-8")
def check():
 p=subprocess.run([sys.executable,"-m","unittest","discover","-s","tests","-p","test_run_report_offline.py","-v"],cwd=ROOT,capture_output=True,text=True,timeout=35)
 return p.returncode,p.stdout+p.stderr
def work():
 s=json.loads(CP.read_text(encoding="utf8")) if CP.exists() else {"state":"START","attempts":0,"repairs":0,"complete":False}
 if s["complete"]:print("ALREADY_DONE_NO_REPLAY",json.dumps(s));return
 if s["state"]=="START":
  shutil.copy2(OLD,ROOT/"scripts"/"run.py")
  s["state"]="OLD_INSTALLED";save(s)
 if s["state"]=="OLD_INSTALLED":
  t=time.perf_counter();rc,output=check();s["before_ms"]=round((time.perf_counter()-t)*1000,2)
  s["before_rc"]=rc;s["historical_error"]="ZeroDivisionError" in output
  assert rc!=0 and s["historical_error"],"historical fault not reproduced"
  s["state"]="FAULT_CONFIRMED";save(s)
 if s["state"]=="FAULT_CONFIRMED":
  shutil.copy2(GOOD,ROOT/"scripts"/"run.py")
  s["repairs"]+=1;s["state"]="REPAIR_APPLIED";save(s)
 if s["state"]=="REPAIR_APPLIED":
  t=time.perf_counter();rc,output=check();s["after_ms"]=round((time.perf_counter()-t)*1000,2)
  s["after_rc"]=rc;s["after_tests"]="Ran 5 tests" in output and "OK" in output
  if rc!=0:raise RuntimeError("QA failed; checkpoint retained")
  s["state"]="QA_PASSED";save(s)
 if s["state"]=="QA_PASSED":
  digest=hashlib.sha256((ROOT/"scripts"/"run.py").read_bytes()).hexdigest()
  s["sha256"]=digest;s["state"]="DONE";s["complete"]=True;save(s)
 print(json.dumps(s,ensure_ascii=False,indent=2))
if __name__=="__main__":work()
