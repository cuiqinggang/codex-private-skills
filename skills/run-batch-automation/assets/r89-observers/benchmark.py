"""Frozen paired comparison: unchanged original archive, whole local batch through independent QA/readback."""
from pathlib import Path
import hashlib,json,os,shutil,statistics,subprocess,sys,time,zipfile
ROOT=Path(__file__).resolve().parent
LIB=ROOT.parent/"pi-rules-r64-20261108/runtime/skills/run-batch-automation"
TEMPLATE=ROOT.parent/"pi-ready-flow-library-r86-20261110/jobs/archive-2/input"
PY="C:/Users/A/AppData/Local/Programs/Python/Python313/python.exe"
COUNT=8
ORDER=[("original",1),("batch",1),("batch",2),("batch",2),("batch",1),("original",1),("batch",1),("original",1),("batch",2)]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    if (ROOT/"FREEZE.json").exists():raise RuntimeError("Existing experiment: reconcile instead of rerunning")
    sources={str(p.relative_to(LIB)):sha(p) for p in [LIB/"scripts/match_flow.py",LIB/"scripts/invoke_flow.py",*list((LIB/"assets/ready-flows/pi-native").glob("*.py"))]}
    expected={p.relative_to(TEMPLATE).as_posix():sha(p) for p in TEMPLATE.rglob("*") if p.is_file()}
    freeze={"jobs":COUNT,"files_per_job":len(expected),"order":ORDER,"source_hashes":sources,
      "input_hashes":expected,"quality":"same original archive checks plus external ZIP CRC, paths, bytes, manifest, receipt hashes and unchanged input",
      "clock":"before input preparation and request creation through original invocation, independent QA and delivery readback; excludes this experiment development, network tools and GUI",
      "candidate":"stdlib ThreadPoolExecutor + original match() in same process; original argv, workspace-write sandbox and business sources unchanged",
      "no_model_calls":True,"gui_acceptance":"NOT_MEASURED"}
    (ROOT/"FREEZE.json").write_text(json.dumps(freeze,indent=2),encoding="utf-8")
    rows=[]
    for n,(mode,workers) in enumerate(ORDER):
        start=time.perf_counter();case=ROOT/f"case-{n:02d}-{mode}-{workers}";case.mkdir()
        reqs=[];jobs=[];prep_start=time.perf_counter()
        for i in range(COUNT):
            w=case/f"job-{i:02d}";w.mkdir();shutil.copytree(TEMPLATE,w/"input")
            req={"goal":"files.archive_exact","context":"host","workspace":str(w),"input_directory":"input",
              "output_profile":"zip_manifest_receipt","requirements":["relative_paths","file_bytes","zip_crc","input_integrity","fixed_readback"],"allow_write":True}
            rp=case/f"request-{i:02d}.json";rp.write_text(json.dumps(req),encoding="utf-8");reqs.append(str(rp));jobs.append(w)
        manifest=case/"requests.json";manifest.write_text(json.dumps(reqs),encoding="utf-8")
        prep_s=time.perf_counter()-prep_start;execution=time.perf_counter();intervals=[]
        if mode=="original":
            for i,rp in enumerate(reqs):
                t=time.perf_counter()
                proc=subprocess.Popen([PY,"-X","utf8",str(LIB/"scripts/invoke_flow.py"),"--request",rp],
                  cwd=case,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                out,err=proc.communicate();intervals.append({"index":i,"pid":proc.pid,"start":t,"end":time.perf_counter(),"exit_code":proc.returncode})
                (case/f"job-{i:02d}.stdout").write_bytes(out);(case/f"job-{i:02d}.stderr").write_bytes(err)
                assert proc.returncode==0,err.decode("utf-8","replace")
        else:
            proc=subprocess.run([PY,"-X","utf8",str(ROOT/"batch_handoff.py"),"--library",str(LIB),"--requests",str(manifest),
               "--workers",str(workers),"--result",str(case/"EXECUTION.json")],cwd=case,capture_output=True)
            (case/"batch.stdout").write_bytes(proc.stdout);(case/"batch.stderr").write_bytes(proc.stderr)
            assert proc.returncode==0,proc.stderr.decode("utf-8","replace")
            intervals=json.loads((case/"EXECUTION.json").read_text(encoding="utf-8"))["results"]
        execution_s=time.perf_counter()-execution;qa=time.perf_counter()
        business_s=[]
        for i,w in enumerate(jobs):
            actual_in={p.relative_to(w/"input").as_posix():sha(p) for p in (w/"input").rglob("*") if p.is_file()}
            assert actual_in==expected
            with zipfile.ZipFile(w/"delivery.zip") as z:
                assert len(z.namelist())==len(expected) and z.testzip() is None
                assert {name:hashlib.sha256(z.read(name)).hexdigest() for name in z.namelist()}==expected
            assert json.loads((w/"manifest.json").read_text(encoding="utf-8"))==expected
            receipt=json.loads((w/"delivery.json").read_text(encoding="utf-8"))
            assert receipt["status"]=="CONTENT_ACCEPTED" and receipt["qa"]["pass"] and all(receipt["qa"]["checks"].values())
            assert receipt["file_count"]==len(expected) and receipt["model_calls"]==0
            assert all(sha(w/name)==digest for name,digest in receipt["sha256"].items())
            stdout=(case/f"job-{i:02d}.stdout").read_text(encoding="utf-8") if mode=="original" else intervals[i]["stdout"]
            parsed=json.loads(stdout);assert parsed["status"]=="CONTENT_ACCEPTED"
            business_s.append(parsed.get("local_accepted_seconds"))
        assert all(sha(LIB/p)==v for p,v in sources.items())
        result={"valid":True,"mode":mode,"workers":workers,"jobs":COUNT,"file_checks":COUNT*len(expected),
          "prep_s":prep_s,"execution_s":execution_s,"qa_s":time.perf_counter()-qa,"business_s":business_s,
          "intervals":intervals,"model_calls":0,"scope":freeze["clock"]}
        result_path=case/"RESULT.json";result_path.write_text(json.dumps(result,indent=2),encoding="utf-8")
        assert json.loads(result_path.read_text())["valid"]
        total=time.perf_counter()-start
        row={"case":case.name,"mode":mode,"workers":workers,"total_s":total,**{k:result[k] for k in ["prep_s","execution_s","qa_s","jobs","file_checks","valid"]}}
        rows.append(row);(ROOT/"PROGRESS.json").write_text(json.dumps(rows,indent=2),encoding="utf-8")
        print(json.dumps(row),flush=True)
    summary={"valid":all(r["valid"] for r in rows),"rows":rows,"groups":{},"source_unchanged":True,"gui_acceptance":"NOT_MEASURED"}
    for mode,workers in [("original",1),("batch",1),("batch",2)]:
        values=[r["total_s"] for r in rows if r["mode"]==mode and r["workers"]==workers]
        summary["groups"][f"{mode}-{workers}"]={"mean_s":statistics.mean(values),"median_s":statistics.median(values),"range_s":[min(values),max(values)]}
    (ROOT/"SUMMARY.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps({"FINAL":summary["groups"],"valid":summary["valid"]}),flush=True)
if __name__=="__main__":run()
