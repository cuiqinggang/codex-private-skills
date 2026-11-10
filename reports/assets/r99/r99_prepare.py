from pathlib import Path
import json,hashlib,ast,time
B=Path(__file__).resolve().parent;O=B/'r99-parallel-input';OLD=B/'r98-two-step'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not O.exists(),'Existing run: reconcile, no duplicate'
f=json.loads((OLD/'FREEZE.json').read_text())
assert all(sha(OLD/n)==h for n,h in f['source_sha256'].items())
s=(OLD/'benchmark.py').read_text(encoding='utf-8')
def one(a,b):
 global s
 assert s.count(a)==1,(a,s.count(a))
 s=s.replace(a,b)
one('R=B/"r98-two-step/run";L=B/"r98-two-step/snapshot"','R=B/"r99-parallel-input/run";L=B/"r98-two-step/snapshot"')
one('import concurrent.futures,datetime,hashlib,json,shutil,subprocess,sys,time,zipfile,itertools','import concurrent.futures,datetime,hashlib,json,shutil,subprocess,sys,time,itertools,threading')
s=s.replace('PI-R98-TWO-STEP-20261111','PI-R99-PARALLEL-INPUT-20261111')
lo=s.index('        requests=[]\n        for i in range(N):');end=s.index('        task=f"""',lo)
block=s[lo:end];body=block[block.index('        for i in range(N):\n')+len('        for i in range(N):\n'):block.index('        manifest=')]
body=body.replace('requests.append(str(rp))','events.append({"index":i,"thread":threading.get_ident(),"start":began,"end":time.perf_counter()});return str(rp)')
helper='''    def prepare_batch(W,workers,prep_workers):
        events=[];prep_started=time.perf_counter()
        def prepare_one(i):
            began=time.perf_counter()
'''+body+'''        if prep_workers==1:requests=list(map(prepare_one,range(N)))
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=prep_workers) as pool:
                requests=list(pool.map(prepare_one,range(N)))
        assert len(requests)==len(set(requests))==N
        assert {x["index"] for x in events}==set(range(N))
        manifest=W/"requests.json";manifest.write_text(json.dumps(requests))
        metrics={"prep_workers":prep_workers,"threads":len({x["thread"] for x in events}),"jobs":N,"copy_wall_s":time.perf_counter()-prep_started,"events":events}
        (W/"PREP-METRICS.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
        return requests,manifest
'''
s=s[:lo]+'        requests,manifest=prepare_batch(W,workers,4)\n'+s[end:]
insert='''    controls=[]
    Q=R/"prep-controls";Q.mkdir()
    for n,pw in enumerate([1,4,4,1]):
        begin=time.perf_counter();w=Q/f"case-{n:02d}-p{pw}";w.mkdir()
        prepare_batch(w,4,pw)
        metric=json.loads((w/"PREP-METRICS.json").read_text())
        assert metric["threads"]==pw
        controls.append({"case":w.name,"prep_workers":pw,"wall_s":time.perf_counter()-begin,"metric":metric})
        (Q/"RESULTS.json").write_text(json.dumps(controls,indent=2),encoding="utf-8")
        print(json.dumps({"PREP_CONTROL":{k:v for k,v in controls[-1].items() if k!="metric"}}),flush=True)
'''
one('    rows=[]\n',helper+insert+'    rows=[]\n')
lo=s.index('            def verify_job(i):');hi=s.index('            assert all(sha(Path(p))',lo)
s=s[:lo]+'''            def verify_job(i):
                ex=intervals[i];w=W/f"lane-{i//(N//workers)}"/f"job-{i:02d}"
                # Compare already computed immutable per-item observations to frozen fixture expectations. No payload rescan.
                observed={Path(n).relative_to("input").as_posix():h for n,h in ex["input_hashes"].items()}
                assert observed==expected_by_id[i],("INPUT_EXPECTATION",i)
                item=ex["item_acceptance"]
                assert item and Path(item["workspace"]).resolve()==w.resolve() and item["files"]==len(expected)
                assert item["original_checks"]["pass"] and all(item["original_checks"]["checks"].values())
                return json.loads(ex["stdout"])["local_accepted_seconds"]
            business=[verify_job(i) for i in range(N)]
'''+s[hi:]
one('"independent_qa_s":time.perf_counter()-qa_start','"completion_reconcile_s":time.perf_counter()-qa_start,"independent_qa_s":0.0')
one('"qa_s":result["independent_qa_s"]','"completion_reconcile_s":result["completion_reconcile_s"],"qa_s":0.0')
one('"file_checks":N*len(expected)','"files_accepted":N*len(expected)')
s=s.replace('original QA, fixed 4-worker independent QA and RESULT readback','original per-item QA, lightweight already-computed result reconciliation and RESULT readback; no second batch content audit')
s=s.replace('original business and external independent QA','original per-item business QA and metadata completion checks')
ast.parse(s)
O.mkdir();(O/'benchmark.py').write_text(s,encoding='utf-8')
plan={'task_id':'PI-R99-PARALLEL-INPUT-20261111','created_epoch':time.time(),'virtual_mature':True,'prep_control_order':[1,4,4,1],'business_order':[1,4,4,1],'both_business_modes_prep_workers':4,'mature_composition':'original shutil.copytree/copy2 behavior; stdlib ThreadPoolExecutor.map over128 independent job directories; existing R98 entry and per-item checks unchanged','invariants':['unique task IDs, disjoint output paths, list(map) preserves request order and propagates exceptions','no changed sandbox, symlinks, hardlinks or unchecked copy cache','source template read-only; each copied marker unique; no business begins before preparation completes','original archive performs full input pre/during/post, ZIP byte/path/count/CRC QA; existing item verifier binds manifest/source/output hashes and receipt','completion uses already-computed input hashes to compare frozen expected fixtures and checks all128 task identities, counts and per-item QA results','no second input-tree or ZIP payload audit; source and request fingerprints retained','all slow/failures retained; exactly4 business batches; prep controls are fixtures only, not additional accepted deliveries'],'audit_inheritance':'R98 same immutable per-item business chain previously passed512 jobs and4 corruption preflights plus full independent external audit; present change only to independent fixture preparation and duplicate benchmark observer removal','fairness':'Both single-business-lane and four-business-lane use4 identical prep threads; separate1/4 prep-only controls measure preparation benefit without giving different preparation to business modes','clocks':'primary total_with_fixture_s = real input preparation + CLI/per-item QA + lightweight receipt/expected-fingerprint reconciliation + RESULT readback; production_s also recorded; excludes the separate preparation-control research probes from per-batch timings; all research probe time retained separately','limits':'Two runs per mode only, no stable physical-limit or universal speed guarantee; control probes validate exception/ID/thread completion, not business outputs','source_reference_freeze_sha256':sha(OLD/'FREEZE.json'),'reference_source_sha256':{str(OLD/n):h for n,h in f['source_sha256'].items()},'benchmark_sha256':sha(O/'benchmark.py'),'prepare_sha256':sha(Path(__file__))}
(O/'FREEZE.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
print(json.dumps({'prepared':True,'freeze_sha256':sha(O/'FREEZE.json'),'native_business_unchanged':True,'prep_control_order':plan['prep_control_order']}),flush=True)
