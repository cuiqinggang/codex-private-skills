"""R86 observer: copied mature recipes and read-only contract matcher.

Only fixtures, timing and independent readback are implemented here.
"""
from pathlib import Path
import csv,hashlib,json,os,shutil,subprocess,time,zipfile

B=Path('C:/Users/A/Documents/DSH-Workspace')
R=B/'pi-ready-flow-library-r86-20261110'
L=B/'pi-rules-r64-20261108/runtime/skills/run-batch-automation'
P=L/'assets/ready-flows/pi-native'
REG=L/'references/executable-flows.json'
PY='C:/Users/A/AppData/Local/Programs/Python/Python313/python.exe'
ENV={**os.environ,'PYTHONUTF8':'1','PYTHONIOENCODING':'utf-8'}
OLD=B/'pi-automation-index-r85-20261109'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
R.mkdir(exist_ok=False);C=R/'control';C.mkdir()
registry=read(REG)
sources={x['path']:sha(L/x['path']) for x in registry['source_files']}
assert all(sources[x['path']]==x['sha256'] for x in registry['source_files'])
save(C/'FREEZE.json',{'date_beijing':'2026-11-10','originals':sources,'business':'Three goals, two fresh batches each; original fixed QA plus independent readback.','clock':'Before input preparation through match(if used), original sandboxed recipe, fixed QA, independent content/source QA and receipt write/read. First library preparation and current GPT planning separate.','model_calls':0,'new_scheduler':False})

def setup(goal,batch,work):
 work.mkdir(parents=True);inp=work/'input'
 if goal=='office.extract_body':
  shutil.copytree(OLD/f'control/fixture-{batch}',inp)
  expected=read(OLD/'control/FREEZE.json')['batches'][str(batch)]
 elif goal=='files.archive_exact':
  inp.mkdir();expected={}
  for i in range(48):
   name=f'分组{i%6}/item-{i:03d}.txt';p=inp/name;p.parent.mkdir(exist_ok=True)
   p.write_bytes((f'R86 batch={batch} item={i} 中文订单00{i:03d}\n'.encode('utf-8')+bytes(range(256)))*4)
   expected[name]={'sha256':sha(p)}
 else:
  inp.mkdir();customers=['A','a','A*','A?','~name','>0','=12','0007','中文客户','B','C','D']
  with (inp/'orders.csv').open('w',encoding='utf-8',newline='') as f:
   w=csv.writer(f);w.writerow(['row_id','order_id','customer','amount_cents','quantity'])
   for i in range(180):
    cents=(i*137+batch)%10001
    if i%11==0:cents=-cents
    w.writerow([f'row-{i:04d}',f'{i%47:06d}',customers[i%len(customers)],str(cents),str(i%5)])
  expected={'orders.csv':{'sha256':sha(inp/'orders.csv')}}
 request={'goal':goal,'context':'host','workspace':str(work),'output_profile':next(f['output_profile'] for f in registry['flows'] if f['goal']==goal),'requirements':next(f['capabilities'] for f in registry['flows'] if f['goal']==goal),'allow_write':True}
 if goal=='files.archive_exact':request['input_directory']='input'
 else:request['inputs']=[str(p.relative_to(work)) for p in sorted(inp.iterdir())]
 if goal=='orders.report_integer_cents':request['semantics']={'amount_unit':'integer_cents','duplicates':'preserve','customer_case':'exact','identifiers':'text','numeric_text':'canonical_integer'}
 return request,expected

def original_argv(request):
 a=[PY,'-X','utf8',str(P/'launch_pi-v1.3.1-scoped-backup.py'),'--cwd',request['workspace']]
 if request['goal']=='office.extract_body':
  for f in request['inputs']:a+=['--fast-office-file',f]
 elif request['goal']=='files.archive_exact':a+=['--fast-archive-input','input']
 else:a+=['--fast-orders-input','input/orders.csv','--fast-orders-out','output']
 return a

def checks(work,goal,expected,receipt):
 q={'originals_unchanged':all(sha(L/p)==h for p,h in sources.items()),'input_hashes_unchanged':all(sha(work/'input'/n)==x['sha256'] for n,x in expected.items()),'original_status':receipt.get('status')=='CONTENT_ACCEPTED'}
 q['original_qa_pass']=receipt.get('qa',receipt.get('quality',{})).get('pass') is True
 if goal=='office.extract_body':
  data=read(work/'extracted.json');q['20_unique_results']=len(data)==20 and len({x['source'] for x in data})==20
  q['all60_content_markers']=all(all(t in x['markdown'] for t in expected[Path(x['source']).name]['markers']) for x in data)
  q['source_and_route']=all(Path(x['source']).resolve()==(work/'input'/Path(x['source']).name).resolve() and x['route']=='existing Microsoft MarkItDown; plugins and LLM disabled' for x in data)
  q['delivery_readback']=read(work/'delivery.json')['qa']['pass'] is True
 elif goal=='files.archive_exact':
  manifest=read(work/'manifest.json')
  with zipfile.ZipFile(work/'delivery.zip') as z:
   q['zip_crc']=z.testzip() is None;q['48_unique_members']=len(z.namelist())==48 and len(set(z.namelist()))==48
   q['all_paths_and_bytes']={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()}=={n:x['sha256'] for n,x in expected.items()}
  q['manifest_matches_all_input_bytes']=manifest=={n:x['sha256'] for n,x in expected.items()}
  q['delivery_readback']=read(work/'delivery.json')['qa']['pass'] is True
 else:
  q['20_original_independent_checks']=receipt['quality']['checks']==20
  q['180_original_records']=receipt['row_count']==180 and read(work/'output/summary.json')['row_count']==180
  q['four_artifacts_present']=all((work/'output'/n).is_file() for n in ['details.csv','summary.json','ledger.xlsx','report.docx'])
  q['delivery_readback']=read(work/'delivery.json')['quality']['pass'] is True
 return {'pass':all(q.values()),'checks':q}

def match_cli(request,label,reg=None):
 p=C/'requests'/(label+'.json');save(p,request)
 cmd=[PY,str(L/'scripts/match_flow.py'),'--request',str(p)]
 if reg:cmd+=['--registry',str(reg)]
 v=subprocess.run(cmd,capture_output=True,env=ENV,check=True)
 return json.loads(v.stdout.decode('utf-8'))

results=[]
for batch in [1,2]:
 for short,goal in [('office','office.extract_body'),('archive','files.archive_exact'),('orders','orders.report_integer_cents')]:
  label=f'{short}-{batch}';start=time.perf_counter();work=R/'jobs'/label;request,expected=setup(goal,batch,work)
  plan=match_cli(request,label) if batch==2 else None
  if plan:assert plan['status']=='MATCH',plan
  argv=plan['argv'] if plan else original_argv(request)
  proc=subprocess.run(argv,cwd=work,env={**ENV,**(plan['env'] if plan else {})},capture_output=True)
  save(C/'cases'/label/'COMMAND.json',argv)
  (C/'cases'/label/'STDERR.txt').write_bytes(proc.stderr)
  assert proc.returncode==0,(label,proc.stderr.decode('utf-8','replace'))
  receipt=json.loads(proc.stdout.decode('utf-8'));q=checks(work,goal,expected,receipt);assert q['pass'],q
  delivery={'label':label,'valid':q['pass'],'output_hashes':{str(p.relative_to(work)):sha(p) for p in work.rglob('*') if p.is_file() and not p.is_relative_to(work/'input')}}
  save(C/'cases'/label/'DELIVERY.json',delivery);assert read(C/'cases'/label/'DELIVERY.json')==delivery
  result={'label':label,'goal':goal,'batch':batch,'elapsed_s':time.perf_counter()-start,'matcher_s':plan['elapsed_s'] if plan else None,'qa':q,'model_calls':0,'plan':plan,'original_receipt':receipt}
  save(C/'cases'/label/'RESULT.json',result);results.append(result)
  print(json.dumps({k:result[k] for k in ['label','elapsed_s','matcher_s','model_calls','qa']},ensure_ascii=False),flush=True)
 if batch==1:
  live=read(REG)
  for f in live['flows']:
   f['state']='READY';f['entry']['host']['state']='READY';f['entry']['inside_omp_tool']['state']='CONFIGURED'
   f['acceptance']='Original fixed business checks plus independent R86 source/output readback.'
   f['host_acceptance_evidence']=str(C/'cases'/(f['id'].split('-')[0]+'-1')/'RESULT.json')
  save(REG,live)

# Fresh tasks for contract rejection checks; no business process is launched.
base_req,_=setup('office.extract_body',1,R/'matching-only/office')
order_req,_=setup('orders.report_integer_cents',1,R/'matching-only/orders')
archive_req,_=setup('files.archive_exact',1,R/'matching-only/archive')
trials=[]
def trial(label,req,status,reg=None):
 out=match_cli(req,label,reg);assert out['status']==status,(label,out)
 trials.append({'label':label,'expected':status,'observed':out,'pass':True})
trial('valid-office',base_req,'MATCH')
trial('context-not-currently-certified',{**base_req,'context':'inside_omp_tool'},'NEEDS_CONFIG')
trial('requires-OCR',{**base_req,'requirements':['ocr']},'NOT_MATCHED')
trial('requires-layout',{**base_req,'requirements':['layout_fidelity']},'NOT_MATCHED')
trial('outside-path',{**base_req,'inputs':['../escape.txt']},'NOT_MATCHED')
trial('duplicate-input',{**base_req,'inputs':[base_req['inputs'][0]]*2},'NOT_MATCHED')
trial('writes-not-authorized',{**base_req,'allow_write':False},'NOT_MATCHED')
trial('wrong-money-unit',{**order_req,'semantics':{**order_req['semantics'],'amount_unit':'decimal_dollars'}},'NOT_MATCHED')
trial('drop-duplicates-not-allowed',{**order_req,'semantics':{**order_req['semantics'],'duplicates':'drop'}},'NOT_MATCHED')
trial('archive-ACL-requirement',{**archive_req,'requirements':['acl_restore']},'NOT_MATCHED')
many=R/'matching-only/many';many.mkdir()
for i in range(41):(many/f'f{i}.txt').write_text(str(i))
trial('too-many-office-files',{**base_req,'workspace':str(many),'inputs':[p.name for p in many.iterdir()]},'NOT_MATCHED')
bad,_=setup('orders.report_integer_cents',1,R/'matching-only/noncanonical')
f=Path(bad['workspace'])/'input/orders.csv';text=f.read_text(encoding='utf-8');lines=text.splitlines();parts=lines[1].split(',');parts[3]='0001';lines[1]=','.join(parts);f.write_text('\n'.join(lines)+'\n',encoding='utf-8')
trial('noncanonical-numeric-text',bad,'NOT_MATCHED')
reg=read(REG);reg['flows'][0]['dependencies']=['r86-intentionally-uninstalled-package'];badreg=C/'dependency-missing.json';save(badreg,reg)
trial('dependency-not-installed',base_req,'NEEDS_CONFIG',badreg)
(Path(base_req['workspace'])/'extracted.json').write_text('existing output',encoding='utf-8')
trial('existing-output-preserved',base_req,'NOT_MATCHED')
save(C/'MATCH-ACCEPTANCE.json',trials)
summary={'cases':results,'match_trials':trials,'copied_source_hashes':sources,'passed':all(r['qa']['pass'] for r in results) and all(t['pass'] for t in trials),'scope':'3 copied mature workflows,2 local host batches each; no model execution, no blanket optimality or copied OMP-context certification.'}
save(C/'SUMMARY.json',summary)
print(json.dumps({'complete':summary['passed'],'business_cases':len(results),'matching_cases':len(trials),'root':str(R)},ensure_ascii=False),flush=True)
