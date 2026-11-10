"""Read-only R95 analysis, then persist a compact evidence receipt. No benchmark rerun."""
from pathlib import Path
import json,hashlib,statistics,time
B=Path(__file__).resolve().parent;R=B/"r95-four-core";F=R/"f2";RUN=F/"run"
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
s=read(RUN/"SUMMARY.json");freeze=read(F/"EXPERIMENT-FREEZE.json")
assert s["valid"] and len(s["rows"])==8 and [r["label"] for r in s["rows"]]==freeze["order"]
source_check={n:sha(F/n)==v for n,v in freeze["snapshot_after"].items()};assert all(source_check.values())
rows=[]
for row in s["rows"]:
 C=RUN/row["case"];r=read(C/"RESULT.json");e=read(C/"work/EXECUTION.json");d=read(C/"work/DELIVERY.json");jobs=e["results"];lanes=e["lane_metrics"];cli=json.loads(r["final_cli_receipt"])
 assert r["valid"] and not r["failures"] and r["jobs"]==128 and r["file_checks"]==6144
 assert d["status"]=="VALID" and d["accepted"]==d["requested"]==128 and d["files"]==6144
 assert len(lanes)==4 and all(x["count"]==32 and x["process_exit_code"]==0 for x in lanes)
 assert sorted(x["index"] for x in jobs)==list(range(128))
 assert len({x["pid"] for x in jobs})==4 and all(x["exit_code"]==0 for x in jobs)
 span=max(x["end"] for x in jobs)-min(x["start"] for x in jobs);busy=sum(x["end"]-x["start"] for x in jobs);cpu=sum(x["cpu_s"] for x in jobs)
 peak=active=0
 for _,delta in sorted([(x["start"],1) for x in jobs]+[(x["end"],-1) for x in jobs]):active+=delta;peak=max(peak,active)
 rows.append({**row,"minimum_files_checked":6144,"actual_pin":cli["pin_mode"],"actual_qa":cli["qa_mode"],
 "worker_pids":[x["pid"] for x in lanes],"tasks_per_lane":[x["count"] for x in lanes],
 "affinity_actual":[x["affinity_actual"] for x in lanes],"worker_span_s":span,"overlap_peak":peak,"slot_occupancy":busy/(4*span),
 "worker_job_cpu_s":cpu,"partial_cpu_reference_s":cpu/4,"job_mean_wall_s":busy/128,"match_mean_wall_s":statistics.mean(x["match_s"] for x in jobs),
 "handoff_s":e["elapsed_s"],"header_preflight_s":e["match_s"],"lane_setup_remainder_s":e["elapsed_s"]-e["match_s"]-span,
 "internal_final_qa_s":cli["final_qa_s"],"entry_and_return_s":row["cli_wall_s"]-e["elapsed_s"]-cli["final_qa_s"],
 "external_qa_s":row["qa_s"],"result_tail_s":row["total_s"]-row["cli_wall_s"]-row["qa_s"],
 "worker_peak_wset_bytes":[x["peak_wset_bytes"] for x in lanes],"worker_rss_bytes":[x["rss_bytes"] for x in lanes],
 "system_available_before_bytes":r["memory_before"]["available"],"system_available_after_bytes":r["memory_after"]["available"],
 "receipts":{str(p.relative_to(F)):sha(p) for p in [C/"RESULT.json",C/"work/EXECUTION.json",C/"work/DELIVERY.json",C/"work/COMPLETION.md",C/"trace.jsonl"]}})
groups={}
for label in ["A","B","C","D"]:
 v=[r for r in rows if r["label"]==label]
 keys=["total_s","total_with_fixture_s","worker_span_s","worker_job_cpu_s","partial_cpu_reference_s","job_mean_wall_s","match_mean_wall_s","slot_occupancy","internal_final_qa_s","external_qa_s","entry_and_return_s","header_preflight_s","lane_setup_remainder_s"]
 groups[label]={k:statistics.mean(x[k] for x in v) for k in keys}
 groups[label]["times_s"]=[r["total_s"] for r in v]
 groups[label]["relative_to_A"]=groups["A"]["total_s"]/groups[label]["total_s"]
winner=min(groups,key=lambda k:groups[k]["total_s"])
f1=read(R/"run/PROGRESS.json")
f1first=read(R/"run/case-00-A/ACCEPTED.json")
last=read(RUN/"case-07-A/ACCEPTED.json")
qpc_span=last["qpc"]+rows[-1]["total_s"]-f1first["qpc"]
out={"task_id":freeze["task_id"],"valid":True,"jobs_accepted":1024,"file_checks":49152,"groups":groups,"selected":winner,"rows":rows,
 "source_check":source_check,"freeze_sha256":sha(F/"EXPERIMENT-FREEZE.json"),"f1_preserved":f1,
 "recorded_span_from_F1_A_start_to_F2_last_readback_s":qpc_span,
 "recorded_span_scope":"Includes F1 A/B, failed affinity, diagnosis, probe, F2 setup, all F2 batches and interposed waiting; excludes earlier task receipt,initial searching and later audit/publish. NOT complete TASK_ACCEPTED to final reply.",
 "physical_reference_scope":"worker CPU/4 only: not whole physical lower bound; excludes Node/controller/QA/OS work and mandatory I/O; CPU speed/work assumptions apply",
 "memory_scope":"worker lifetime high-water working set, not simultaneous whole process-tree peak; system before/after only",
 "method_ref":"skills/artificial-single-page-extreme-time-engine/SANRENXING_V5.md"}
p=F/"ANALYSIS.json"
if p.exists():raise RuntimeError("Existing analysis: reconcile, do not overwrite")
p.write_text(json.dumps(out,indent=2),encoding="utf-8");assert read(p)==out
print(json.dumps({"selected":winner,"groups":groups,"jobs":1024,"files":49152,"recorded_span_s":qpc_span,"sha256":sha(p)}))
