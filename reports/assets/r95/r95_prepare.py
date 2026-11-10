"""R95: adapt R94's frozen observer; compare mature affinity and independent file-QA concurrency."""
from pathlib import Path
import hashlib,json,shutil,time
B=Path(__file__).resolve().parent
R=B/"r95-four-core"
L=B.parent/"pi-rules-r64-20261108/runtime/skills/run-batch-automation"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if R.exists():raise RuntimeError("Reconcile existing R95; never replay")
 R.mkdir()
 S=R/"snapshot";shutil.copytree(L/"scripts",S/"scripts")
 shutil.copytree(L/"assets/ready-flows/pi-native",S/"assets/ready-flows/pi-native")
 (S/"references").mkdir();shutil.copy2(L/"references/executable-flows.json",S/"references/executable-flows.json")
 before={str(p.relative_to(S)):sha(p) for p in S.rglob("*") if p.is_file()}
 worker=S/"scripts/archive_stream_worker.py";t=worker.read_text(encoding="utf-8")
 t=t.replace("import argparse,contextlib,hashlib,importlib.util,io,json,os,sys,time","import argparse,contextlib,hashlib,importlib.util,io,json,os,sys,time,psutil")
 needle=' results=[];stream_start=time.perf_counter()'
 assert t.count(needle)==1
 t=t.replace(needle,''' process=psutil.Process()
 affinity_before=process.cpu_affinity()
 pin=os.environ.get("R95_PIN","0")=="1"
 wanted=[int(lane.name.rsplit("-",1)[1])]
 if pin:process.cpu_affinity(wanted)
 affinity_actual=process.cpu_affinity()
 if pin:assert affinity_actual==wanted
 results=[];stream_start=time.perf_counter()''')
 needle=' path=lane/"STREAM-RESULTS.json"'
 t=t.replace(needle,''' metric["affinity_before"]=affinity_before
 metric["affinity_actual"]=process.cpu_affinity()
 metric["pin_requested"]=pin
 memory=process.memory_info()
 metric["rss_bytes"]=memory.rss
 metric["peak_wset_bytes"]=memory.peak_wset
 metric["peak_pagefile_bytes"]=memory.peak_pagefile
 metric["cpu_times"]=list(process.cpu_times())
'''+needle)
 worker.write_text(t,encoding="utf-8")
 delivery=S/"scripts/deliver_archive_batch.py";t=delivery.read_text(encoding="utf-8")
 t=t.replace("import argparse,hashlib,json,os,subprocess,sys,time,zipfile","import argparse,hashlib,json,os,subprocess,sys,time,zipfile,concurrent.futures")
 old=' verified=[]\n for j,req,ex in zip(jobs,requests,execution["results"]):'
 assert t.count(old)==1
 t=t.replace(old,' def verify_one(item):\n  j,req,ex=item')
 start=t.index("  verified.append(");end=t.index("\n assert all(sha(Path(n))",start)
 body=t[start:end]
 assert body.endswith(")")
 t=t[:start]+body.replace("  verified.append(","  return ",1)[:-1]+t[end:]
 needle=' assert all(sha(Path(n))==v for n,v in sources.items())'
 t=t.replace(needle,''' items=list(zip(jobs,requests,execution["results"]))
 qa_started=time.perf_counter()
 if os.environ.get("R95_QA","serial")=="parallel":
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:verified=list(pool.map(verify_one,items))
 else:verified=[verify_one(item) for item in items]
 final_qa_s=time.perf_counter()-qa_started
'''+needle)
 t=t.replace('"local_pipeline_s":time.perf_counter()-started,','"local_pipeline_s":time.perf_counter()-started,"final_qa_s":final_qa_s,')
 delivery.write_text(t,encoding="utf-8")
 original_entry=B.parent/"pi-capability-enhancement-20261028/launch_pi.py"
 t=original_entry.read_text(encoding="utf-8")
 old="library=entry.parent/'skills/run-batch-automation'"
 assert t.count(old)==1
 t=t.replace(old,"library=pathlib.Path(__file__).resolve().parent/'snapshot'")
 (R/"launch_pi.py").write_text(t,encoding="utf-8")
 t=(B/"r94_streams_128_benchmark.py").read_text(encoding="utf-8")
 begin=t.index('B=Path(');end=t.index('\nPY=',begin)
 t=t[:begin]+'B=Path(__file__).resolve().parent.parent;R=B/"r95-four-core/run";L=B/"r95-four-core/snapshot"\nENTRY=B/"r95-four-core/launch_pi.py"'+t[end:]
 t=t.replace('import concurrent.futures,datetime,hashlib,json,shutil,subprocess,sys,time,zipfile,itertools','import concurrent.futures,datetime,hashlib,json,shutil,subprocess,sys,time,zipfile,itertools,os,psutil')
 t=t.replace('ORDER=[1,2,4,8,8,4,2,1]','ORDER=["A","B","C","D","D","C","B","A"]')
 begin=t.index('    C=R/"candidate-library"');end=t.index('    T=',begin)
 t=t[:begin]+'    C=L\n'+t[end:]
 t=t.replace('for n,workers in enumerate(ORDER):','for n,label in enumerate(ORDER):\n        workers=4;pin=label in ["B","C"];parallel=label in ["C","D"]')
 t=t.replace('case=R/f"case-{n:02d}-w{workers}"','case=R/f"case-{n:02d}-{label}"')
 t=t.replace('R94-TASK-','R94-TASK-') # retain exactly the same unique 128 inputs as R94
 t=t.replace('读回8个delivery.json','读回128个delivery.json').replace('核对8个ZIP/manifest','核对128个ZIP/manifest').replace('明确8/8','明确128/128')
 t=t.replace('start=time.perf_counter();fixture_s=start-fixture_start','memory_before=psutil.virtual_memory()._asdict()\n        start=time.perf_counter();fixture_s=start-fixture_start')
 t=t.replace('cwd=W,env=None,stdin=', 'cwd=W,env={**os.environ,"R95_PIN":"1" if pin else "0","R95_QA":"parallel" if parallel else "serial"},stdin=')
 needle='            intervals=exe["results"];assert len(intervals)==N and all(i["exit_code"]==0 for i in intervals)'
 assert t.count(needle)==1
 t=t.replace(needle,needle+'''
            assert {i["index"] for i in intervals}==set(range(N))
            assert len({i["pid"] for i in intervals})==4
            assert all(Path(intervals[i]["cwd"]).resolve()==(W/f"lane-{i%workers}"/f"job-{i:02d}").resolve() for i in range(N))
            lanes=exe["lane_metrics"]
            assert len(lanes)==4 and all(x["process_exit_code"]==0 and x["count"]==32 for x in lanes)
            assert all(x["pin_requested"]==pin for x in lanes)
            if pin:assert sorted(x["affinity_actual"] for x in lanes)==[[0],[1],[2],[3]]
            delivery=json.loads((W/"DELIVERY.json").read_text(encoding="utf-8"))
            assert delivery["status"]=="VALID" and delivery["accepted"]==delivery["requested"]==128 and delivery["files"]==6144''')
 t=t.replace('result={"valid":not failures,','result={"label":label,"pin":pin,"parallel_final_qa":parallel,"memory_before":memory_before,"memory_after":psutil.virtual_memory()._asdict(),"lane_metrics":exe.get("lane_metrics",[]) if "exe" in locals() else [],"valid":not failures,')
 t=t.replace('row={"case":case.name,','row={"label":label,"case":case.name,')
 begin=t.index('    for w in [1,2,4,8]:');end=t.index('    (R/"SUMMARY.json")',begin)
 t=t[:begin]+'''    for label in ["A","B","C","D"]:
        v=[r["total_s"] for r in rows if r["label"]==label]
        summary["groups"][label]={"mean_s":statistics.mean(v),"range_s":[min(v),max(v)]}
'''+t[end:]
 # Preserve original failure stop and all fixed independent per-file QA.
 (R/"benchmark.py").write_text(t,encoding="utf-8")
 files=[p for p in S.rglob("*") if p.is_file()]+[R/"launch_pi.py",R/"benchmark.py"]
 freeze={"task_id":"PI-R95-FOUR-CORE-20261110","created_ns":time.time_ns(),"order":["A","B","C","D","D","C","B","A"],
 "variants":{"A":"OS auto / serial final QA","B":"one core per worker / serial final QA","C":"one core per worker / four-thread final QA","D":"OS auto / four-thread final QA"},
 "invariants":"128 R94 unique input tasks,48 files each,4 persistent workers,32 jobs each,original match/archive/workspace-write sandbox/all QA and independent QA(4)",
 "stop":"single frozen 8-batch comparison; no failed candidate speed ranking; no new candidate without documented mature evidence",
 "scope":"local repeated CLI delivery; development,source adaptation,network,chat are separate investment,not included in batch score",
 "snapshot_before":before,"snapshot_after":{str(p.relative_to(R)):sha(p) for p in files}}
 (R/"EXPERIMENT-FREEZE.json").write_text(json.dumps(freeze,indent=2),encoding="utf-8")
 import py_compile
 for p in [worker,delivery,R/"launch_pi.py",R/"benchmark.py"]:py_compile.compile(str(p),doraise=True)
 print(json.dumps({"prepared":True,"root":str(R),"files":len(files),"freeze":sha(R/"EXPERIMENT-FREEZE.json")}))
if __name__=="__main__":main()
