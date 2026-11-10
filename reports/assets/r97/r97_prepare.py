from pathlib import Path
import ast,hashlib,json,time
B=Path(__file__).resolve().parent
O=B/'r97-four-simple'
assert not O.exists(),'Existing experiment: reconcile, no duplicate'
S=B/'r96-29s-reality/snapshot'
freeze=json.loads((B/'r96-29s-reality/EXPERIMENT-FREEZE.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for n,h in freeze['snapshot_sha256'].items():
 assert sha(B/'r96-29s-reality'/n)==h,n
s=(B/'r94_streams_128_benchmark.py').read_text(encoding='utf-8')
def one(a,b):
 global s
 assert s.count(a)==1,(a,s.count(a))
 s=s.replace(a,b)
one('B=Path(__file__).resolve().parent;R=B/"r94-cli-streams-128";L=B.parent/"pi-rules-r64-20261108/runtime/skills/run-batch-automation"','B=Path(__file__).resolve().parent.parent;R=B/"r97-four-simple/run";L=B/"r96-29s-reality/snapshot"')
one('ENTRY=B.parent/"pi-capability-enhancement-20261028/launch_pi.py"','ENTRY=B/"r96-29s-reality/launch_pi.py"')
one('ORDER=[1,2,4,8,8,4,2,1]','ORDER=[1,4,4,1]')
lo=s.index('    C=R/"candidate-library"');hi=s.index('    T=B.parent/',lo)
s=s[:lo]+'    C=L\n'+s[hi:]
s=s.replace('i%workers','i//(N//workers)')
one('env=None,stdin=','env={**__import__("os").environ,"R95_QA":"serial","R95_PIN":"0"},stdin=')
one('for w in [1,2,4,8]:','for w in [1,4]:')
one('intervals=exe["results"];assert len(intervals)==N and all(i["exit_code"]==0 for i in intervals)','intervals=exe["results"];assert len(intervals)==N and all(i["exit_code"]==0 for i in intervals)\n            assert {x["index"] for x in intervals}==set(range(N))\n            assert len({x["pid"] for x in intervals})==workers\n            assert sorted(x["count"] for x in exe["lane_metrics"])==[N//workers]*workers')
one('    (R/"SUMMARY.json").write_text','    summary["speedup_mean"]=summary["groups"]["1"]["mean_s"]/summary["groups"]["4"]["mean_s"]\n    summary["speedup_pairs"]=[rows[0]["total_s"]/rows[1]["total_s"],rows[3]["total_s"]/rows[2]["total_s"]]\n    (R/"SUMMARY.json").write_text')
s=s.replace('"task_id":"R90-ENHANCED-CLI"','"task_id":"PI-R97-FOUR-SIMPLE-20261111"')
s=s.replace('必须读回8个delivery.json','必须读回128个delivery.json').replace('核对8个ZIP/manifest','核对128个ZIP/manifest').replace('明确8/8','明确128/128')
s=s.replace('每8类编号轮流分派到持续流水线（同一已验归档业务）','按连续编号简单均分为各路（同一已验归档业务，无需分类）')
ast.parse(s)
O.mkdir()
(O/'benchmark.py').write_text(s,encoding='utf-8')
plan={'task_id':'PI-R97-FOUR-SIMPLE-20261111','virtual_mature':True,'created':time.time(),'order':[1,4,4,1],'partition':'128 contiguous tasks; four independent persistent lanes of32; no work stealing','business':'same original matcher/archive and workspace-write sandbox; frozen R96 accepted serial QA success path','change':'fixture request workspace mapping only; original worker and handoff unchanged','clock':'same R94 input-ready through CLI, original QA, external independent full QA, RESULT readback; fixture copy separate','checks':'every input, ZIP bytes CRC members, manifest, delivery, request/source fingerprint preserved; 128 unique IDs and actual PID/lane counts checked','scope':'homogeneous48-file archive jobs, enhanced Pi CLI fixed recipe; not model benchmark','limits':'two runs each only; speed ratio measured, no statistical stable physical limit; keep slow/failures; stop on quality failure; no extra fastest-sample search','historical_chain_gap':'R94 exact delivery hash unavailable; use unchanged R96 A serial reference for both1 and4','benchmark_sha256':sha(O/'benchmark.py'),'reference_freeze':sha(B/'r96-29s-reality/EXPERIMENT-FREEZE.json')}
(O/'FREEZE.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
print(json.dumps(plan),flush=True)
