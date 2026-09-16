#!/usr/bin/env python3
"""V11 GPU/CPU operator diagnostic for the unchanged V3 workload."""
import argparse, importlib.util, json, sys
from pathlib import Path
BASE=Path(__file__).with_name("H3-P0-runner.py")
PHASE="V11_OP_PROFILE"
def pct(a,q):
    a=sorted(a);p=(len(a)-1)*q;i=int(p);return a[i]+(a[min(i+1,len(a)-1)]-a[i])*(p-i)
def analyze(e):
    rows=[]
    for path in sorted((e/"runs"/PHASE).glob("run-*.json")):
        r=json.loads(path.read_text(encoding="utf-8"))
        if not r.get("task_completed") or len(r["qc"]["frame_ranges"])!=5 or min(r["qc"]["frame_ranges"])<8: raise RuntimeError("QC failure")
        ev=[v for v in r["path_stage_events"] if v.get("stage")=="T_GENERATION_OP_PROFILE" and v.get("seed")==r["seed"]]
        if len(ev)!=1: raise RuntimeError("profiler record missing")
        item=ev[0]
        rows.append({"seed":r["seed"],"total_s":r["total_s"],"generation_cuda_s":r["generation_cuda_s"],"path_s":r["path_s"],"operator_profile":item,"qc":r["qc"]})
    if len(rows)!=3 or sorted(r["seed"] for r in rows)!=[910100,910102,910103]: raise RuntimeError("three fixed formal seeds required")
    report={"phase":PHASE,"basis":"V3_RESERVE1 reserve-vram=1.0 GiB pinned disabled","definition":"torch.profiler operator attribution is diagnostic; overlapping streams and profiling overhead prevent summing operator self times into authoritative CUDA Event generation","qc_pass":True,"rows":rows,"summary":{"generation_p50_s":pct([r["generation_cuda_s"] for r in rows],.5),"path_p50_s":pct([r["path_s"] for r in rows],.5)}}
    (e/f"op-profile-{PHASE}.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    return report
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--evidence",type=Path,required=True);ap.add_argument("--phase",required=True)
    ap.add_argument("--reserve",type=float,required=True);ap.add_argument("--pinned",required=True)
    ap.add_argument("--runs",type=int,required=True);ap.add_argument("--launch-id")
    a=ap.parse_args();e=a.evidence
    if (a.phase,a.reserve,a.pinned,a.runs)!=(PHASE,1.0,"disabled",3): raise RuntimeError("V3 fixed contract required")
    report=e/f"op-profile-{PHASE}.json"
    if report.exists() and json.loads(report.read_text(encoding="utf-8")).get("qc_pass"):
        print("OP_PROFILE_ALREADY_COMPLETE");return
    spec=importlib.util.spec_from_file_location("h3_p0_base_runner",BASE)
    base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
    if base.PATCH.count(base.NEEDLE)!=1: raise RuntimeError("base sampler timer boundary drift")
    wrapped=(b"        with torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU,torch.profiler.ProfilerActivity.CUDA], record_shapes=False, profile_memory=False) as _h3_prof:\n"+b"    "+base.NEEDLE)
    base.PATCH=base.PATCH.replace(base.NEEDLE,wrapped,1)
    needle=b"        _p0_end.synchronize()"
    after=b"\n".join([
      needle,
      b"        _h3_events=_h3_prof.key_averages()",
      b"        _h3_top_cuda=sorted(_h3_events,key=lambda x:x.self_device_time_total,reverse=True)[:40]",
      b"        _h3_top_cpu=sorted(_h3_events,key=lambda x:x.self_cpu_time_total,reverse=True)[:20]",
      b"        _h3_op=lambda x:{'key':x.key,'count':x.count,'self_device_ms':x.self_device_time_total/1000,'self_cpu_ms':x.self_cpu_time_total/1000}",
      b"        print('H3_P0_STAGE '+_p0_json.dumps({'stage':'T_GENERATION_OP_PROFILE','seed':extra_args.get('seed'),'top_cuda':[_h3_op(x) for x in _h3_top_cuda],'top_cpu':[_h3_op(x) for x in _h3_top_cpu],'all_self_device_ms':sum(x.self_device_time_total for x in _h3_events)/1000,'all_self_cpu_ms':sum(x.self_cpu_time_total for x in _h3_events)/1000,'operator_count':len(_h3_events)}),flush=True)"
    ])
    if base.PATCH.count(needle)!=1: raise RuntimeError("base sync boundary drift")
    base.PATCH=base.PATCH.replace(needle,after,1)
    compile("def f():\n"+base.PATCH.decode("utf-8")+"\n","timer_patch","exec")
    sys.argv=[str(BASE),"--evidence",str(e),"--phase",PHASE,"--reserve","1.0","--pinned","disabled","--runs","3"]
    if a.launch_id: sys.argv.extend(["--launch-id",a.launch_id])
    base.main()
    report=analyze(e)
    print(json.dumps({"phase":PHASE,"qc_pass":report["qc_pass"],"summary":report["summary"]}),flush=True)
if __name__=="__main__":main()
