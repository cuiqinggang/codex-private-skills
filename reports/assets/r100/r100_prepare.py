from pathlib import Path
import json,hashlib,ast,time
B=Path(__file__).resolve().parent;O=B/'r100-eight-lanes';R=B/'r99-parallel-input';OLD=B/'r98-two-step'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not O.exists(),'Existing experiment: reconcile, no duplicate'
f=json.loads((R/'FREEZE.json').read_text())
assert sha(R/'benchmark.py')==f['benchmark_sha256']
assert all(sha(Path(n))==h for n,h in f['reference_source_sha256'].items())
s=(R/'benchmark.py').read_text(encoding='utf-8')
def one(a,b):
 global s
 assert s.count(a)==1,(a,s.count(a))
 s=s.replace(a,b)
one('R=B/"r99-parallel-input/run"','R=B/"r100-eight-lanes/run"')
one('ORDER=[1,4,4,1]','ORDER=[4,8]')
s=s.replace('PI-R99-PARALLEL-INPUT-20261111','PI-R100-EIGHT-LANES-20261111')
lo=s.index('    controls=[]');hi=s.index('    rows=[]',lo);s=s[:lo]+s[hi:]
lo=s.index('    for w in [1,4]:');hi=s.index('    (R/"SUMMARY.json")',lo)
s=s[:lo]+'''    for w in [4,8]:
        v=[r["total_s"] for r in rows if r["workers"]==w]
        summary["groups"][str(w)]={"mean_s":statistics.mean(v),"range_s":[min(v),max(v)]}
    summary["speedup_8_vs4_production"]=rows[0]["production_s"]/rows[1]["production_s"]
    summary["execution_reduction_percent"]=100*(1-rows[1]["production_s"]/rows[0]["production_s"])
    summary["execution_halved_observed"]=rows[1]["production_s"]<=0.5*rows[0]["production_s"]
    summary["speedup_8_vs4_with_prepare"]=rows[0]["total_with_fixture_s"]/rows[1]["total_with_fixture_s"]
'''+s[hi:]
ast.parse(s);O.mkdir();(O/'benchmark.py').write_text(s,encoding='utf-8')
plan={'task_id':'PI-R100-EIGHT-LANES-20261111','created_epoch':time.time(),'virtual_mature':True,'business_order':[4,8],'count':128,'partitions':{'4':'4 independent persistent lanes x32 tasks','8':'8 independent persistent lanes x16 tasks'},'maturity':'R94 original persistent native streams already admitted1/2/4/8; R98 unchanged per-item recipe and acceptance; R99 already accepted512 without duplicate full payload audit','changes':'only selected lane count and number of independent lane roots; no extra per-item process start, dynamic scheduler, copy algorithm, model call, or CPU pinning','same_for_both':'original 48-file unique-marker inputs, exact bytes/path/CRC/input integrity and manifest/source/output/receipt checks, sandbox boundaries, 4-thread input provisioning','complete':'all128 unique task IDs accepted once; every lane reports its own completion; parent only consolidates existing result states, no second payload scan','primary_clock':'input-ready through existing enhanced CLI per-item acceptance and batch completion receipt, production_s; preparation separately recorded; total_s adds only lightweight completion/expected-hash/source reconciliation and RESULT readback','hypothesis':'8 may overlap more waiting;4 physical CPU cores remain shared. Half-time is hypothesis not guarantee. T8<=T4/2 is observable target, not claimed until test. One pair cannot establish stable factor.','limits':'exactly two batches4then8, no1-lane or preparation controls, no discarded slow cases, no extra fastest-sample retries, stop/reconcile on real quality failure','source_reference_sha256':f['reference_source_sha256'],'benchmark_sha256':sha(O/'benchmark.py'),'prepare_sha256':sha(Path(__file__))}
(O/'FREEZE.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
print(json.dumps({'prepared':True,'order':[4,8],'freeze_sha256':sha(O/'FREEZE.json')}),flush=True)
