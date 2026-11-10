"""Thin batch handoff to the existing full matcher and unchanged sandboxed entries."""
from pathlib import Path
import argparse, concurrent.futures, importlib.util, json, os, subprocess, sys, time

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--library",type=Path,required=True)
    p.add_argument("--requests",type=Path,required=True)
    p.add_argument("--workers",type=int,choices=[1,2],default=1)
    p.add_argument("--result",type=Path,required=True)
    a=p.parse_args()
    began=time.perf_counter()
    spec=importlib.util.spec_from_file_location("original_flow_matcher",a.library/"scripts/match_flow.py")
    matcher=importlib.util.module_from_spec(spec);spec.loader.exec_module(matcher)
    registry=json.loads(matcher.DEFAULT_REGISTRY.read_text(encoding="utf-8-sig"))
    paths=json.loads(a.requests.read_text(encoding="utf-8-sig"))
    if not isinstance(paths,list) or not paths: raise ValueError("Nonempty request path list required")
    requests=[json.loads(Path(f).read_text(encoding="utf-8-sig")) for f in paths]
    workspaces=[os.path.normcase(str(Path(r["workspace"]).resolve(strict=True))) for r in requests]
    if len(set(workspaces))!=len(workspaces): raise ValueError("Shared workspace needs serial reconciliation; duplicate rejected")
    # Full original contract, source, input and dependency checks; no reduced matcher or cached MATCH.
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as preflight_pool:
        plans=list(preflight_pool.map(lambda r: matcher.match(r,registry),requests))
    match_s=time.perf_counter()-began
    def execute(item):
        i,plan=item;t=time.perf_counter()
        proc=subprocess.Popen(plan["argv"],cwd=plan["cwd"],env={**os.environ,**plan["env"]},
            stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err=proc.communicate()
        return {"index":i,"cwd":plan["cwd"],"pid":proc.pid,"start":t,"end":time.perf_counter(),
            "exit_code":proc.returncode,"stdout":out.decode("utf-8","replace"),
            "stderr":err.decode("utf-8","replace")}
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
        results=list(pool.map(execute,enumerate(plans)))
    result={"status":"EXECUTED" if all(r["exit_code"]==0 for r in results) else "EXECUTION_FAILED",
        "workers":a.workers,"match_s":match_s,"elapsed_s":time.perf_counter()-began,"results":results,
        "acceptance":"Original business checks remain in each unchanged entry; independent delivery QA still required"}
    with a.result.open("x",encoding="utf-8") as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({"status":result["status"],"result":str(a.result)},ensure_ascii=True),flush=True)
    return 0 if result["status"]=="EXECUTED" else 1
if __name__=="__main__":
    try:sys.exit(main())
    except Exception as e:
        print(type(e).__name__+": "+str(e),file=sys.stderr);sys.exit(2)
