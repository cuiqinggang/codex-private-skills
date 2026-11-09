"""Minimal front door to the EXISTING mature order report recipe; not a new report generator."""
import argparse,csv,hashlib,importlib.util,json,pathlib,subprocess,sys,time
p=argparse.ArgumentParser(description="Verified deterministic order report fast path")
p.add_argument("--cwd",required=True);p.add_argument("--input",required=True)
p.add_argument("--out",default="output");p.add_argument("--title",default="订单经营日报")
a=p.parse_args()
start=time.perf_counter()
R=pathlib.Path(__file__).resolve().parent
H=R/'orders'
runner=pathlib.Path(r"C:\AI\DeepSeek-Harness-Trial\dsh-0.2.1-rc.2-isolated\node_modules\@deepseek-ai\dsh-sandbox-windows-acl\lib\runner.js")
temp=pathlib.Path(r"C:\Users\A\Documents\DSH-Workspace\pi-comparison-20261028\temp")
root=pathlib.Path(a.cwd).resolve(strict=True)
def inside(x,must_exist=False):
 target=(root/x).resolve(strict=must_exist)
 if not target.is_relative_to(root):raise ValueError("path is outside working directory")
 return target
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
try:
 source=inside(a.input,True);out=inside(a.out)
 if not source.is_file():raise ValueError("input must be a CSV file")
 if out==root or (out.exists() and any(out.iterdir())):raise ValueError("output must be a fresh empty directory")
 manifest_path=inside("delivery.json")
 if manifest_path.exists():raise ValueError("prior delivery.json exists; reconcile before repeating")
 with source.open("r",encoding="utf-8-sig",newline="") as f:
  reader=csv.DictReader(f)
  if reader.fieldnames!=["row_id","order_id","customer","amount_cents","quantity"]:raise ValueError("CSV column contract mismatch")
  rows=list(reader)
 expected=sum(int(x["amount_cents"])*int(x["quantity"]) for x in rows)
 before=sha(source)
 command=[r"C:\Program Files\nodejs\node.exe",str(runner),"--workspace",str(root),"--temp",str(temp),"--mode","workspace-write","--",sys.executable,str(H/"business_pack.py"),"--input",str(source),"--out",str(out),"--title",a.title]
 result=subprocess.run(command,cwd=root,stdin=subprocess.DEVNULL,capture_output=True,timeout=55)
 if result.returncode!=0:raise RuntimeError("business_pack failed: "+result.stderr.decode("utf-8","replace")[-500:])
 generated=json.loads(result.stdout.decode("utf-8-sig","replace").strip())
 spec=importlib.util.spec_from_file_location("independent_existing_qa",H/"verify_order_pack.py")
 oracle=importlib.util.module_from_spec(spec);spec.loader.exec_module(oracle)
 check=oracle.verify(out,source)
 summary=json.loads((out/"summary.json").read_text(encoding="utf-8"))
 if not generated.get("status")=="CONTENT_ACCEPTED" or not generated.get("qa",{}).get("pass") or not check.get("pass"):raise RuntimeError("Independent quality contract failed")
 if summary.get("row_count")!=len(rows) or summary.get("total_cents")!=expected or sha(source)!=before:raise RuntimeError("Rows, money or input integrity mismatch")
 names=["details.csv","summary.json","ledger.xlsx","report.docx"]
 if not all((out/n).is_file() for n in names):raise RuntimeError("Deliverables missing")
 doc={"status":"CONTENT_ACCEPTED","input_sha256":before,"row_count":len(rows),"total_cents":expected,"files":[str(out.relative_to(root)/n).replace("\\","/") for n in names],"quality":{"pass":True,"checks":check.get("count",len(check.get("checks",[])))}}
 manifest_path.write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding="utf-8")
 final=json.loads(manifest_path.read_text(encoding="utf-8"))
 if final.get("input_sha256")!=before or len(final["files"])!=4:raise RuntimeError("Receipt readback failed")
 doc["T_VALID_seconds"]=round(time.perf_counter()-start,3)
 print(json.dumps(doc,ensure_ascii=False))
except Exception as exc:
 print("NOT_VALID "+type(exc).__name__+": "+str(exc),file=sys.stderr)
 sys.exit(1)
