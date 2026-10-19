import csv,json,hashlib,os,sys,time,subprocess
from pathlib import Path
R=Path(__file__).parent/"acceptance_results"
def write(p,x):
 t=p.with_suffix(".tmp");t.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding="utf8");os.replace(t,p)
def read(p):return json.loads(p.read_text(encoding="utf8"))
def run(p,fault=""):
 cp=p/"checkpoint.json";out=p/"result.csv";events=p/"events.jsonl"
 s=read(cp) if cp.exists() else dict(state="START",round=0,commits=0)
 def evt(x):
  with events.open("a",encoding="utf8") as f:f.write(x+"\n")
 if s["state"]=="DONE":evt("DONE_ALREADY_SKIP");return s
 if s["state"]=="UNKNOWN":
  if out.exists() and hashlib.sha256(out.read_bytes()).hexdigest()==s["sha"]:
   s["state"]="DONE";write(cp,s);evt("UNKNOWN_RECONCILED");return s
  raise RuntimeError("UNKNOWN_REQUIRES_RECONCILIATION")
 if s["state"]=="STOP_GATE":evt("STOP_ALREADY_SKIP");return s
 for state in ["S0_CONTRACT","S1_REAL_BASELINE","S2_PHYS_BOUND","S3_THREE_MATURE","S4_COMPOSE","S5_ATTACK","S6_VIRTUAL"]:
  s["state"]=state;write(cp,s);evt(state)
 for i in range(s["round"],3):
  s["round"]=i+1;s["state"]="S7_VALIDATE";write(cp,s);evt("ROUND_"+str(i+1))
  if fault=="transient" and i==0:evt("FAULT_IO_RETRY");continue
  if fault=="all_fail":evt("CANDIDATE_FAIL");continue
  with (p/"orders.csv").open(newline="") as f:rows=list(csv.DictReader(f))
  rows.sort(key=lambda v:(-float(v["amount"]),v["id"]))
  temp=p/"result.pending"
  with temp.open("w",newline="") as f:
   w=csv.DictWriter(f,fieldnames=["id","amount"]);w.writeheader();w.writerows(rows)
  assert len(rows)==20 and all(float(rows[j]["amount"])>=float(rows[j+1]["amount"]) for j in range(19))
  os.replace(temp,out);s["commits"]+=1;s["sha"]=hashlib.sha256(out.read_bytes()).hexdigest()
  s["state"]="UNKNOWN" if fault=="crash" else "DONE";write(cp,s);evt("COMMITTED")
  if fault=="crash":raise SystemExit(37)
  evt("QA_PASS");return s
 s["state"]="STOP_GATE";write(cp,s);evt("STOP_GATE");return s
def case(name,fault,expected,rounds):
 p=R/name;p.mkdir(exist_ok=True)
 with (p/"orders.csv").open("w",newline="") as f:
  w=csv.writer(f);w.writerow(["id","amount"])
  for i in range(20):w.writerow([f"X{i:03d}",(i*37)%101])
 t=time.perf_counter()
 if fault=="crash":
  q=subprocess.run([sys.executable,__file__,"worker",str(p),"crash"],capture_output=True)
  assert q.returncode==37
  fault=""
 s=run(p,fault)
 if name=="unknown_reconcile":
  s["state"]="UNKNOWN";write(p/"checkpoint.json",s);s=run(p)
 before=s["commits"];s=run(p)
 assert s["commits"]==before
 good=s["state"]==expected and s["round"]==rounds and (expected!="DONE" or s["commits"]==1)
 return dict(case=name,pass_=good,final=s["state"],rounds=s["round"],commits=s["commits"],milliseconds=round((time.perf_counter()-t)*1000,2))
if __name__=="__main__":
 if len(sys.argv)>1 and sys.argv[1]=="worker":run(Path(sys.argv[2]),sys.argv[3]);sys.exit(0)
 R.mkdir(exist_ok=True)
 tests=[("real_clean","","DONE",1),("transient_recovery","transient","DONE",2),("exhaust_three","all_fail","STOP_GATE",3),("commit_crash_resume","crash","DONE",1),("unknown_reconcile","","DONE",1)]
 results=[]
 for t in tests:
  try:results.append(case(*t))
  except Exception as ex:results.append(dict(case=t[0],pass_=False,error=str(ex)))
 write(R/"summary.json",results)
 print(json.dumps(results,indent=2))
 if not all(x["pass_"] for x in results):sys.exit(1)
