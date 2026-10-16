import pathlib,json,time,hashlib,subprocess,psutil
P=pathlib.Path('C:/AI/Orca-Codex-Validation-20261014/suite-ab-20261016-r2/p01-B')
W=P/'worktrees/fixture/suite'
j={'scope':'read-only reconciliation, no dispatch or model execution','at':time.time(),'receipts':{},'errors':[]}
for n in ['input.json','runtime-pid.json','assignment.json','worker-done.json','business-inspection.json','coordinator-error.json','main-error.json','result.json','local-acceptance.json','prior-good.json']:
 try:j['receipts'][n]=json.loads((P/n).read_text(encoding='utf-8'))
 except Exception as e:j['errors'].append({'file':n,'error':str(e)})
j['outputs']=[]
for n in ['llm_verifier/fine_grained_reward.py','llm_verifier/benchmarks.py','llm_verifier/loaders.py','scripts/run.py','tests/test_t01_offline.py','tests/test_t02_offline.py','tests/test_t03_offline.py','DELIVERY.md']:
 try:
  b=(W/n).read_bytes();j['outputs'].append({'path':n,'sha256':hashlib.sha256(b).hexdigest(),'text':b.decode('utf-8')})
 except Exception as e:j['errors'].append({'file':n,'error':str(e)})
for op,args in [('status',['status','--porcelain','--untracked-files=all']),('diff',['diff','--'])]:
 try:
  r=subprocess.run(['git',*args],cwd=W,capture_output=True,text=True,encoding='utf-8',timeout=25);j[op]={'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
 except Exception as e:j['errors'].append({'op':op,'error':str(e)})
j['processes']=[]
for p in psutil.process_iter(['pid','name','cmdline','create_time']):
 try:
  cmd=' '.join(p.info['cmdline'] or []).replace(chr(92),'/').lower()
  if str(P).replace(chr(92),'/').lower() in cmd:j['processes'].append(p.info)
 except psutil.Error:pass
j['memory_available']=psutil.virtual_memory().available
out=P/'reconciliation-v1.json';assert not out.exists(),'Existing reconciliation preserved'
out.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'output':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'errors':j['errors'],'processes':j['processes'],'memory_available':j['memory_available']},ensure_ascii=False))
