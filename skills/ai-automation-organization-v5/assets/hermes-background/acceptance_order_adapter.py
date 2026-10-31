"""Hermes cron adapter; reuse the frozen delivery entry, never implement a scheduler."""
from pathlib import Path
import subprocess,json,sys,os,datetime
ROOT=Path(r'C:\Users\A\Documents\DSH-Workspace\aiorg-background-20261031')
manifest=json.loads((ROOT/'JOB-CONTRACTS.json').read_text(encoding='utf-8'))
name=Path(__file__).stem
contract=manifest[name]
cmd=[r'C:\Users\A\AppData\Local\Programs\Python\Python313\python.exe',
r'C:\Users\A\Documents\DSH-Workspace\aiorg-independent-handoff-20261029-r2\service\independent_delivery.py',
'--config',r'C:\Users\A\Documents\DSH-Workspace\aiorg-independent-handoff-20261029-r2\service\config.json',
'--input',r'C:\Users\A\Documents\DSH-Workspace\aiorg-independent-handoff-20261029-r2\fixtures\orders.csv',
'--task-id',contract['task_id'],'--scope','test','--fault',contract['fault']]
env=dict(os.environ,PYTHONIOENCODING='utf-8')
for key in ('PYTHONPATH','PYTHONHOME','VIRTUAL_ENV','__PYVENV_LAUNCHER__'):
 env.pop(key,None)
p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace',env=env,timeout=600)
if p.returncode:
 print(json.dumps({'status':'FAILED','returncode':p.returncode,'detail':p.stderr[-1800:]},ensure_ascii=True));sys.exit(1)
r=json.loads(p.stdout)
assert r['status']=='CONFIRMED_COMMITTED' and r['qa_pass'] and r['qa_checks']==20
assert r['delivery']['generation_count']==1
if contract['fault'] in ('primary_exit','after_generation'):
 assert len(r['attempts'])==2 and r['attempts'][0]['confirmed_exited'] and r['attempts'][1]['role']=='backup'
(ROOT/(name+'-RESULT.json')).write_text(json.dumps(r,ensure_ascii=True,indent=2),encoding='utf-8')
print(json.dumps({'task_id':r['task_id'],'status':r['status'],'qa_checks':r['qa_checks'],'generation_count':r['delivery']['generation_count'],'fault':contract['fault'],'human_takeovers':r['human_takeovers_after_injected_fault'],'result':str(ROOT/(name+'-RESULT.json'))},ensure_ascii=True))
