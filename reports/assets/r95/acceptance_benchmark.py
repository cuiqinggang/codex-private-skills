"""R90: real enhanced Pi CLI delivery; original business and external independent QA."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,shutil,subprocess,sys,time,zipfile,itertools,os,psutil
B=Path(__file__).resolve().parent.parent.parent;R=B/"r95-four-core/f2/acceptance";L=B/"r95-four-core/f2/snapshot"
ENTRY=B/"r95-four-core/four_lane_entry.py"
PY="C:/Users/A/AppData/Local/Programs/Python/Python313/python.exe"
ORDER=["A"]
N=128
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    if R.exists():raise RuntimeError("Existing run: reconcile and resume; do not duplicate")
    R.mkdir();setup=time.perf_counter()
    C=L
    T=B.parent/"pi-ready-flow-library-r86-20261110/jobs/archive-2/input"
    expected={p.relative_to(T).as_posix():sha(p) for p in T.rglob("*") if p.is_file()}
    marker_relative=sorted(expected)[0]
    expected_by_id=[]
    for task_i in range(N):
        item=dict(expected);item[marker_relative]=hashlib.sha256((T/marker_relative).read_bytes()+f"\\nR94-TASK-{task_i:03d}".encode("ascii")).hexdigest();expected_by_id.append(item)
    sources={str(p):sha(p) for p in [ENTRY,L/"scripts/archive_stream_worker.py",L/"scripts/deliver_archive_batch.py",L/"scripts/batch_handoff.py",L/"scripts/match_flow.py",C/"scripts/match_flow.py",C/"assets/ready-flows/pi-native/artifact_recipe.py"]}
    freeze={"task_id":"PI-R95-FOUR-LANE-ENTRY-ACCEPTANCE","entry":str(ENTRY),"verified_version":"omp/18.18.0","workers_order":ORDER,
      "jobs_per_batch":N,"files_per_job":len(expected),"input_hashes":expected,"unique_task_input_hashes":expected_by_id,"source_hashes":sources,
      "context_candidate":"Existing READY host archive; original per-job workspace-write sandbox retained",
      "clock":"From inputs and request contract ready, before enhanced CLI launch through complete delivery receipt, original QA, fixed 4-worker independent QA and RESULT readback; separate fixture_provision_s and total_with_fixture_s retained",
      "previous_GUI_setup":"abandoned on explicit user steering; failure retained separately, not counted as CLI benchmark",
      "setup_s":time.perf_counter()-setup,"user_message_to_final_reply_total":"NOT_MEASURED"}
    (R/"FREEZE.json").write_text(json.dumps(freeze,indent=2),encoding="utf-8")
    rows=[]
    for n,label in enumerate(ORDER):
        workers=4;pin=label in ["B","C"];parallel=label in ["C","D"]
        fixture_start=time.perf_counter();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
        case=R/f"case-{n:02d}-{label}";case.mkdir();W=case/"work";W.mkdir()
        requests=[]
        for i in range(N):
            w=W/f"lane-{i%workers}"/f"job-{i:02d}";w.mkdir(parents=True);shutil.copytree(T,w/"input")
            marker=w/"input"/marker_relative;marker.write_bytes(marker.read_bytes()+f"\\nR94-TASK-{i:03d}".encode("ascii"))
            req={"goal":"files.archive_exact","context":"host","workspace":str(w),"input_directory":"input",
              "output_profile":"zip_manifest_receipt","requirements":["relative_paths","file_bytes","zip_crc","input_integrity","fixed_readback"],"allow_write":True}
            rp=W/f"request-{i:02d}.json";rp.write_text(json.dumps(req),encoding="utf-8");requests.append(str(rp))
        manifest=W/"requests.json";manifest.write_text(json.dumps(requests))
        task=f"""任务R90-{n:02d}，成熟固定程序真实交付验收。当前工作区128项独立任务，每项48文件；每8类编号轮流分派到持续流水线（同一已验归档业务），分别归档，交付每项delivery.zip、manifest.json、delivery.json。不改输入、不改原程序、不另写归档算法。当前批完整合同已由当前GPT配置到requests.json。
使用现有{workers}路薄入口，原完整match()及原archive节点，禁止重做归档核心：
固定Python {PY} -X utf8 "{(L/'scripts/batch_handoff.py').as_posix()}" --library "{C.as_posix()}" --requests "{manifest.as_posix()}" --workers {workers} --result "{(W/'EXECUTION.json').as_posix()}"
本轮使用原READY host上下文，保留每项原workspace-write沙箱及固定检查，不改业务源码、权限、代理或模型配置。此批{workers}指业务程序通道，不是子智能体数。
执行完成必须读回128个delivery.json的原qa.pass和全部检查、核对128个ZIP/manifest存在，原程序已逐字节CRC检查；界面/CLI最终回复明确128/128与产物位置，并写COMPLETION.md。不把EXECUTED或进程退出当作验收。若失败保留错误与检查点，按原任务接续，不缩减合同；禁止修改任何验收源或r90-cli内外部审计资料。只读本任务来源，写当前work工作区。本轮当前GPT已明确此执行计划，无需重新规划或搜索其他方案。"""
        (W/"TASK.md").write_text(task,encoding="utf-8")
        instruction="Read TASK.md and complete this batch using its admitted original program path, then verify every delivery and report the real result. Do not stop at a plan."
        req_hashes={str(p):sha(p) for p in [W/"TASK.md",manifest,*[Path(p) for p in requests]]}
        memory_before=psutil.virtual_memory()._asdict()
        start=time.perf_counter();fixture_s=start-fixture_start
        (case/"ACCEPTED.json").write_text(json.dumps({"utc":utc,"qpc":start,"workers":workers,"status":"RUNNING"},indent=2))
        events=[];final_texts=[];session=None
        with (case/"stderr.log").open("wb") as err,(case/"trace.jsonl").open("wb") as log:
            proc=subprocess.Popen([PY,"-X","utf8",str(ENTRY),"--fast-archive-batch",str(manifest),"--cwd",str(W),"--library",str(C),"--stream-lanes"],
                cwd=W,env={**os.environ,"R95_PIN":"1" if pin else "0","R95_QA":"parallel" if parallel else "serial"},stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=err)
            for line in proc.stdout:
                log.write(line);log.flush();stamp=time.perf_counter()-start
                try:ev=json.loads(line)
                except (ValueError,UnicodeDecodeError):continue
                typ=ev.get("type")
                if ev.get("status")=="VALID":final_texts.append(json.dumps(ev,ensure_ascii=False))
                if typ in ["session","agent_start","turn_start","tool_execution_start","tool_execution_end","message_end","agent_end"]:
                    compact={"elapsed_s":stamp,"type":typ,"tool":ev.get("toolName"),"tool_id":ev.get("toolCallId"),"isError":ev.get("isError")}
                    events.append(compact)
                    if typ in ["tool_execution_start","tool_execution_end","agent_end"]:print(json.dumps({"case":case.name,**compact}),flush=True)
                if typ=="session":session=ev.get("id")
                if typ=="message_end":
                    m=ev.get("message",{})
                    if m.get("role")=="assistant":final_texts.append("".join(c.get("text","") for c in m.get("content",[]) if c.get("type")=="text"))
            code=proc.wait()
        cli_end=time.perf_counter();qa_start=cli_end
        failures=[];intervals=[];business=[]
        try:
            assert code==0,("CLI_EXIT",code)
            exe=json.loads((W/"EXECUTION.json").read_text(encoding="utf-8"))
            assert exe["status"]=="EXECUTED" and exe["workers"]==workers
            intervals=exe["results"];assert len(intervals)==N and all(i["exit_code"]==0 for i in intervals)
            assert {i["index"] for i in intervals}==set(range(N))
            assert len({i["pid"] for i in intervals})==4
            assert all(Path(intervals[i]["cwd"]).resolve()==(W/f"lane-{i%workers}"/f"job-{i:02d}").resolve() for i in range(N))
            lanes=exe["lane_metrics"]
            assert len(lanes)==4 and all(x["process_exit_code"]==0 and x["count"]==32 for x in lanes)
            assert all(x["pin_requested"]==pin for x in lanes)
            if pin:assert sorted(x["affinity_actual"] for x in lanes)==[[0],[1],[2],[3]]
            delivery=json.loads((W/"DELIVERY.json").read_text(encoding="utf-8"))
            assert delivery["status"]=="VALID" and delivery["accepted"]==delivery["requested"]==128 and delivery["files"]==6144
            def verify_job(i):
                w=W/f"lane-{i%workers}"/f"job-{i:02d}"
                actual={p.relative_to(w/"input").as_posix():sha(p) for p in (w/"input").rglob("*") if p.is_file()}
                assert actual==expected_by_id[i],("INPUT_CHANGED",i)
                with zipfile.ZipFile(w/"delivery.zip") as z:
                    assert len(z.namelist())==len(expected) and z.testzip() is None
                    assert {name:hashlib.sha256(z.read(name)).hexdigest() for name in z.namelist()}==expected_by_id[i]
                assert json.loads((w/"manifest.json").read_text(encoding="utf-8"))==expected_by_id[i]
                receipt=json.loads((w/"delivery.json").read_text(encoding="utf-8"))
                assert receipt["status"]=="CONTENT_ACCEPTED" and receipt["qa"]["pass"] and all(receipt["qa"]["checks"].values())
                assert all(sha(w/name)==digest for name,digest in receipt["sha256"].items())
                return json.loads(intervals[i]["stdout"])["local_accepted_seconds"]
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as qa_pool:business=list(qa_pool.map(verify_job,range(N)))
            assert all(sha(Path(p))==digest for p,digest in sources.items()),"SOURCE_CHANGED"
            assert all(sha(Path(p))==digest for p,digest in req_hashes.items()),"REQUEST_CHANGED"
            assert (W/"COMPLETION.md").is_file(),"FINAL_DELIVERY_NOTE_MISSING"
            assert final_texts and final_texts[-1].strip(),"FINAL_ASSISTANT_RECEIPT_MISSING"
            actual_cli=json.loads(final_texts[-1])
            assert actual_cli["qa_mode"]==("parallel" if parallel else "serial") and actual_cli["pin_mode"]==("1" if pin else "0")
        except Exception as e:failures.append(str(e))
        result={"label":label,"pin":pin,"parallel_final_qa":parallel,"memory_before":memory_before,"memory_after":psutil.virtual_memory()._asdict(),"lane_metrics":exe.get("lane_metrics",[]) if "exe" in locals() else [],"valid":not failures,"failures":failures,"workers":workers,"jobs":N,"file_checks":N*len(expected),"cli_exit_code":code,
         "cli_wall_s":cli_end-start,"independent_qa_s":time.perf_counter()-qa_start,"events":events,"session":session,
         "final_assistant":None,"final_cli_receipt":final_texts[-1] if final_texts else None,"business_s":business,"intervals":intervals,
         "explicit_user_entry":"Existing enhanced CLI --fast-archive-batch; explicit ready programme route; no model process or desktop GUI","candidate_source_checked":not failures}
        rp=case/"RESULT.json";rp.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
        assert json.loads(rp.read_text(encoding="utf-8"))["valid"]==result["valid"]
        row={"label":label,"case":case.name,"workers":workers,"valid":result["valid"],"total_s":time.perf_counter()-start,"fixture_provision_s":fixture_s,"total_with_fixture_s":time.perf_counter()-fixture_start,
          "cli_wall_s":result["cli_wall_s"],"qa_s":result["independent_qa_s"],"failures":failures}
        rows.append(row);(R/"PROGRESS.json").write_text(json.dumps(rows,indent=2))
        print(json.dumps({"BATCH_RESULT":row}),flush=True)
        if failures:
            print("RECONCILE_THIS_SAME_CASE_BEFORE_CONTINUING",flush=True);return 2
    import statistics
    summary={"valid":all(r["valid"] for r in rows),"rows":rows,"groups":{},"version":"omp/18.18.0","entry":"existing enhanced launch_pi.py"}
    for label in ["A"]:
        v=[r["total_s"] for r in rows if r["label"]==label]
        summary["groups"][label]={"mean_s":statistics.mean(v),"range_s":[min(v),max(v)]}
    (R/"SUMMARY.json").write_text(json.dumps(summary,indent=2))
    print(json.dumps({"FINAL":summary}),flush=True)
    return 0
if __name__=="__main__":sys.exit(main())

