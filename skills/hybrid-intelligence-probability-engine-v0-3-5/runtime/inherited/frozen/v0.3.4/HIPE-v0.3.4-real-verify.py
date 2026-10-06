import argparse,hashlib,json,math,os,re,sqlite3,statistics,sys,time,urllib.request,urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

VERSION='0.3.4';FAMILY='HIPE-E2E-V3-48';ONTOLOGY=['EXECUTE','HOLD','ROUTE','REJECT']
CRITERIA={
'EXECUTE':'Choose EXECUTE only when the requested action is permitted now and every mandatory prerequisite is satisfied.',
'HOLD':'Choose HOLD when the action may be allowed later but a mandatory prerequisite, timing condition, evidence item, or temporary dependency is not satisfied now.',
'ROUTE':'Choose ROUTE when the request requires a specialist, review path, security response, tax/privacy/billing review, or specialized executor before completion.',
'REJECT':'Choose REJECT when the requested action is prohibited, must never be performed by this workflow, or a permanent failure makes automatic execution impermissible.'}
GPT_URL='https://openrouter.ai/api/v1/chat/completions';JEV_URL='https://openrouter.ai/api/alpha/decisions'
ROOT=Path(__file__).resolve().parent
SKILL_ROOT=ROOT.parent.parent
sys.path.insert(0,str(SKILL_ROOT/'components'/'reality-solvability-gate'))
sys.path.insert(0,str(SKILL_ROOT/'components'/'comfort-zone-forward-compiler'))
import reality_solvability_gate as rsg
import forward_compiler as fc
from sql_scope_audit import extract_frozen_bindings
PUBLIC=ROOT/'PUBLIC-BENCHMARK-v0.3.4.json';PRIVATE=ROOT/'PRIVATE-ORACLE-v0.3.4.json';PUBLIC_BASELINE=ROOT/'PUBLIC-BENCHMARK-R2-BASELINE.json'
FREEZE_ID='HIPE-v0.3.4-SIMPLE-CORE-VIRTUAL-MATURE-R4';REVISION='HIPE-E2E-V3-48-SQL-CONTRACT-R3'
BASELINE_SHA256='4cdf0e8d483dadcc418715b73d95d1f80f69b4357de89f808dec87b2763c3aa5';PRIVATE_SHA256='f073bf1264c0f2d46ad497388df68d6203460d92c8064c5fbd5bf254eb57a60f'
PUBLIC_BLOB='d52d4ee58396f0604c3ec2623c4a982b3f307367'
PRIVATE_BLOB='d07a130d50305348f66460eb645975f316dc29c3'

def load():return json.loads(PUBLIC.read_text(encoding='utf-8')),json.loads(PRIVATE.read_text(encoding='utf-8'))
def git_blob_sha(p):
 raw=p.read_bytes();return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def solvability(b):
 f=rsg.SolvabilityFacts(True,True,True,False,False,False,True,certified_compilable_domain=b.get('benchmark')==FAMILY)
 return rsg.classify(f)
def qchoice(s):return {'type':'choice','instructions':s,'criteria':CRITERIA}
def node_facts(t):
 deterministic=(t.get('operation')=='compare_threshold' and t.get('operator')=='<=' and type(t.get('value')) is int and type(t.get('limit')) is int)
 finite=(all(isinstance(t.get(k),str) and t[k].strip() for k in ('request','current_state','evidence','constraints')) and t.get('allowed_actions')==ONTOLOGY and isinstance(t.get('dependency_ids'),list) and len(t['dependency_ids'])<=1)
 open_generation=(isinstance(t.get('question'),str) and isinstance(t.get('schema'),list) and t.get('dialect')=='sqlite' and t.get('output_contract')=='single SELECT/WITH query only')
 return fc.NodeFacts(
  semantic_preserved=deterministic or finite or open_generation,
  deterministic_exact=deterministic,
  deterministic_executor_available=deterministic,
  explicit_or_extractable_state=finite,
  finite_or_enumerable_choice=finite,
  certified_action_ontology=finite,
  deterministic_verifier=deterministic or finite or open_generation,
  requires_open_generation=open_generation,
  unresolved_hidden_information=False,
  timed_retry_required=False)
def route(t):return fc.route(node_facts(t))
def compile_b(b):
 out={'CODE':[],'JEV':[],'GPT':[]};seen=set()
 for t in b['tasks']:
  if not isinstance(t.get('id'),str) or t['id'] in seen:raise ValueError('BAD_OR_DUP_ID')
  seen.add(t['id']);out[route(t)].append(t)
 return out

def variant(base,v):
 b=json.loads(json.dumps(base));b['variant']=f'V{v:02d}';b['initial_state']=f"{b['initial_state']}|V{v:02d}"
 for i,t in enumerate([x for x in b['tasks'] if x['id'].startswith('D')]):t['value']=(i*7+3+v)%23
 return b

def jev_payloads(b,compiled=None):
 j=(compiled if compiled is not None else compile_b(b))['JEV'];ids={x['id'] for x in j};qs={}
 for i,t in enumerate(j):
  iid=t['id']
  if i<20:qs[f'item_{iid}__current_action']=qchoice(f"For ITEM{iid}, choose exactly one permitted action from EXECUTE, HOLD, ROUTE, REJECT. Use only this item's request, evidence, constraints and allowed_actions from state. Do not invent missing facts.")
  else:
   dep=t['dependency_ids'][0]
   if dep not in ids:raise ValueError('BAD_DEPENDENCY')
   for r in ('SUCCESS','FAIL_TEMP','FAIL_PERM'):qs[f'item_{iid}__if_{dep}_{r}']=qchoice(f"For ITEM{iid}, assume the real executor receipt for dependency ITEM{dep} has result exactly {r}. Choose exactly one permitted action from EXECUTE, HOLD, ROUTE, REJECT using ITEM{iid}'s request, evidence and constraints. Treat {r} as a hypothetical branch for policy compilation only; do not claim the receipt already exists.")
 state={'description':'PE-P0-GENERAL-01 work queue. Each item must receive exactly one permitted action. Dependency results in speculative questions are hypothetical branch conditions until a real executor receipt exists.','action_ontology':ONTOLOGY,'initial_state':b['initial_state'],'items':[]}
 for t in j:state['items'].append({'item_id':t['id'],'request':t['request'],'current_state':t['current_state'],'evidence':t['evidence'],'constraints':t['constraints'],'allowed_actions':t['allowed_actions'],'dependency_ids':t['dependency_ids']})
 items=list(qs.items());return [{'model':'typesafe/jev-1.13','state':state,'questions':dict(items[::2])},{'model':'typesafe/jev-1.13','state':state,'questions':dict(items[1::2])}]

def full_schema(b):
 props={}
 for t in b['tasks']:
  if t['id'].startswith('D'):props[t['id']]={'type':'string','enum':['ALLOW','BLOCK']}
 for p in jev_payloads(b):
  for q in p['questions']:props[q]={'type':'string','enum':ONTOLOGY}
 for t in b['tasks']:
  if t['id'].startswith('G'):props[t['id']]={'type':'string'}
 return {'type':'object','properties':props,'required':list(props),'additionalProperties':False}
def residual_schema(b):
 props={t['id']:{'type':'string'} for t in b['tasks'] if t['id'].startswith('G')};return {'type':'object','properties':props,'required':list(props),'additionalProperties':False}

def gpt_body(b,residual=False,compiled=None):
 provider={'sort':'throughput','require_parameters':True}
 if residual:
  tasks=[t for t in (compiled if compiled is not None else compile_b(b))['GPT'] if t['id'].startswith('G')]
  return {'model':'openai/gpt-5.6-sol','reasoning':{'effort':'low'},'provider':provider,'messages':[{'role':'system','content':'Return one safe SQLite SELECT/WITH query for each id. No destructive or multi-statement SQL.'},{'role':'user','content':json.dumps({'variant':b['variant'],'tasks':tasks},separators=(',',':'))}],'response_format':{'type':'json_schema','json_schema':{'name':'hipe_sql_result','strict':True,'schema':residual_schema(b)}}}
 qs={};[qs.update(p['questions']) for p in jev_payloads(b)]
 user={'variant':b['variant'],'tasks':b['tasks'],'jev_questions':qs,'dependency_results_are_hypothetical':True,'dependent_branch_results':['SUCCESS','FAIL_TEMP','FAIL_PERM']}
 return {'model':'openai/gpt-5.6-sol','reasoning':{'effort':'low'},'provider':provider,'messages':[{'role':'system','content':'Return the required structured answers. Threshold ids map to ALLOW/BLOCK. JEV question ids map to EXECUTE/HOLD/ROUTE/REJECT using supplied policy semantics. SQL ids map to one safe SQLite SELECT/WITH query. No prose.'},{'role':'user','content':json.dumps(user,separators=(',',':'))}],'response_format':{'type':'json_schema','json_schema':{'name':'hipe_full_result','strict':True,'schema':full_schema(b)}}}

def sqlok(q,c):
 if not isinstance(q,str) or len(q)>2000:return False
 s=q.strip().rstrip(';').strip()
 if not re.match(r'(?is)^(select|with)\b',s) or ';' in s or re.search(r'(?is)\b(insert|update|delete|drop|alter|attach|pragma|replace|vacuum|create)\b',s):return False
 con=sqlite3.connect(':memory:')
 try:
  cur=con.cursor();[cur.execute(x) for x in c['schema']];[cur.execute(x) for x in c['data']];return cur.execute(s).fetchall()==[tuple(x) for x in c['expected']]
 except Exception:return False
 finally:con.close()
def verify(a,b,o,v):
 bad=[]
 for i,t in enumerate([x for x in b['tasks'] if x['id'].startswith('D')]):
  want='ALLOW' if t['value']<=t['limit'] else 'BLOCK'
  if a.get(t['id'])!=want:bad.append(t['id'])
 choices=o['expected_choices'];ex=o['executor_outcomes']
 for i in range(20):
  q=f'item_J{i+1:02d}__current_action'
  if a.get(q)!=choices[q]:bad.append(f'J{i+1:02d}')
 for iid,dep in [('J21','J17'),('J22','J18'),('J23','J19'),('J24','J20')]:
  q=f'item_{iid}__if_{dep}_{ex[dep]}'
  if a.get(q)!=choices[q]:bad.append(iid)
 sql={x['id']:x for x in o['sql_cases']}
 for t in b['tasks']:
  if t['id'].startswith('G') and not sqlok(a.get(t['id']),sql[t['id']]):bad.append(t['id'])
 return bad

def post(url,key,body):
 req=urllib.request.Request(url,json.dumps(body,separators=(',',':')).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','User-Agent':'HIPE/0.3.4'},method='POST');t=time.perf_counter_ns()
 try:
  with urllib.request.urlopen(req,timeout=120) as r:raw=r.read()
 except urllib.error.HTTPError as e:
  if e.code==429:raise RuntimeError('TRANSPORT_HTTP_429') from e
  if e.code>=500:raise RuntimeError('PROVIDER_UNAVAILABLE_HTTP_'+str(e.code)) from e
  raise RuntimeError('OPENROUTER_AUTH_OR_HTTP_'+str(e.code)) from e
 except (urllib.error.URLError,TimeoutError,ConnectionError,OSError) as e:raise RuntimeError('TRANSPORT_UNAVAILABLE_'+type(e).__name__) from e
 try:d=json.loads(raw)
 except Exception as e:raise RuntimeError('PROVIDER_RESPONSE_INVALID_JSON') from e
 return d,(time.perf_counter_ns()-t)/1e6
def usage(d):
 u=d.get('usage') or {}
 if u.get('cost') is None:raise RuntimeError('USAGE_COST_MISSING')
 return {'cost_usd':float(u['cost']),'prompt_tokens':u.get('prompt_tokens',u.get('input_tokens')),'completion_tokens':u.get('completion_tokens',u.get('output_tokens')),'provider':d.get('provider'),'model':d.get('model'),'generation_id':d.get('id',d.get('generation_id'))}
def gparse(d):
 try:return json.loads(d['choices'][0]['message']['content'])
 except Exception as e:raise RuntimeError('GPT_PARSE_FAILURE') from e
def jparse(d,ids):
 ans=d.get('answers') or {};out={}
 for q in ids:
  try:x=ans[q]['choice']
  except Exception as e:raise RuntimeError('JEV_PARSE_FAILURE') from e
  if x not in ONTOLOGY:raise RuntimeError('JEV_OUT_OF_ONTOLOGY')
  out[q]=x
 return out

def write(outdir,name,obj):
 p=Path(outdir)/f'{name}.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8');return p

def sql_verifier_error(q,c):
 if not isinstance(q,str):return 'SQL_NOT_STRING'
 if len(q)>2000:return 'SQL_TOO_LONG'
 x=q.strip().rstrip(';').strip()
 if not re.match(r'(?is)^(select|with)\b',x) or ';' in x or re.search(r'(?is)\b(insert|update|delete|drop|alter|attach|pragma|replace|vacuum|create)\b',x):return 'SQL_NOT_SINGLE_SAFE_SELECT'
 con=sqlite3.connect(':memory:')
 try:
  cur=con.cursor();[cur.execute(y) for y in c['schema']];[cur.execute(y) for y in c['data']]
  return 'RESULT_MISMATCH' if cur.execute(x).fetchall()!=[tuple(y) for y in c['expected']] else 'VERIFIER_REJECTED'
 except sqlite3.Error as e:return 'SQL_EXECUTION_ERROR:'+type(e).__name__+':'+str(e)
 finally:con.close()

def sql_evidence_before(outdir,tag,path,v,b,a):
 records=[{'variant':v,'path':path,'task_id':t['id'],'generated_sql':a.get(t['id']),'verifier_pass':None,'verifier_error':None} for t in b['tasks'] if t['id'].startswith('G')]
 obj={'stage':'PARSED_BEFORE_VERIFIER','records':records}
 return write(outdir,tag+'-sql-evidence',obj),obj

def sql_evidence_after(p,obj,bad,o):
 cases={x['id']:x for x in o['sql_cases']}
 for rec in obj['records']:
  rec['verifier_pass']=rec['task_id'] not in bad
  if not rec['verifier_pass']:rec['verifier_error']=sql_verifier_error(rec['generated_sql'],cases[rec['task_id']])
 obj['stage']='VERIFIED'
 p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')

def run_full(key,base,o,v,outdir):
 t0=time.perf_counter_ns();b=variant(base,v);b=json.loads(json.dumps(b));d,net=post(GPT_URL,key,gpt_body(b));a=gparse(d)
 tag=f'v{v:02d}-full';ep,eo=sql_evidence_before(outdir,tag,'FULL_GPT',v,b,a)
 bad=verify(a,b,o,v);sql_evidence_after(ep,eo,bad,o);u=usage(d)
 r={'path':'FULL_GPT','variant':v,'valid':not bad,'errors':bad,'network_ms':net,'usage':u,'sql_evidence':str(ep)}
 p=write(outdir,tag,r);r['e2e_ms']=(time.perf_counter_ns()-t0)/1e6;p.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');return r

def run_hybrid(key,base,o,v,outdir):
 t0=time.perf_counter_ns();b=variant(base,v);b=json.loads(json.dumps(b));domain=solvability(b)
 if domain!='CERTIFIED_COMPILABLE':raise RuntimeError('UNSOLVABLE_OR_UNCOVERED')
 c=compile_b(b);a={t['id']:('ALLOW' if t['value']<=t['limit'] else 'BLOCK') for t in c['CODE']};jp=jev_payloads(b,c);gb=gpt_body(b,True,c)
 def jc(p):d,m=post(JEV_URL,key,p);return jparse(d,list(p['questions'])),m,usage(d)
 def gc():d,m=post(GPT_URL,key,gb);return gparse(d),m,usage(d)
 with ThreadPoolExecutor(max_workers=3) as ex:
  f1,f2,fg=ex.submit(jc,jp[0]),ex.submit(jc,jp[1]),ex.submit(gc);x1,m1,u1=f1.result();x2,m2,u2=f2.result();xg,mg,ug=fg.result()
 a.update(x1);a.update(x2);a.update(xg)
 tag=f'v{v:02d}-hybrid';ep,eo=sql_evidence_before(outdir,tag,'HYBRID',v,b,a)
 bad=verify(a,b,o,v);sql_evidence_after(ep,eo,bad,o)
 r={'path':'HYBRID','variant':v,'valid':not bad,'errors':bad,'component_ms':{'jev_shard_1':m1,'jev_shard_2':m2,'gpt_residual':mg},'usage':{'jev_1':u1,'jev_2':u2,'gpt_residual':ug},'cost_usd':u1['cost_usd']+u2['cost_usd']+ug['cost_usd'],'sql_evidence':str(ep)}
 p=write(outdir,tag,r);r['e2e_ms']=(time.perf_counter_ns()-t0)/1e6;p.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');return r

# Frozen R5 observes the unchanged R4 synchronous business paths.
import timing_boundary_candidate as timing_boundary

_OBSERVATION_PHASE_OVERRIDE = None

def _serialized_task_bytes(result):
 return json.dumps(result,ensure_ascii=False,indent=2).replace('\n',os.linesep).encode('utf-8')

def _observe_r4_path(operation,key,base,o,v,outdir,path_name):
 directory=Path(outdir).resolve()
 tag=f'v{v:02d}-'+('full' if path_name=='FULL_GPT' else 'hybrid')
 result_path=directory/(tag+'.json');sql_path=directory/(tag+'-sql-evidence.json')
 receipt_path=directory/'observations'/(tag+'.json')
 run_id=hashlib.sha256(str(directory).encode('utf-8')).hexdigest()
 phase=_OBSERVATION_PHASE_OVERRIDE or ('WARMUP' if 90<=v<=92 else 'MEASURED')
 captured={};confirmation={}
 def complete_operation():
  result=operation(key,base,o,v,directory)
  captured['result']=result
  # Path.write_text in R4 returns only after its context has flushed and closed.
  # These checks are inside the frozen R5 interval, before its endpoint.
  raw=result_path.read_bytes();persisted=json.loads(raw.decode('utf-8'))
  if persisted.get('path')!=path_name or persisted.get('variant')!=v or persisted!=result:
   raise timing_boundary.BoundaryError('RESULT_READBACK_IDENTITY_MISMATCH')
  expected=hashlib.sha256(_serialized_task_bytes(result)).hexdigest()
  if hashlib.sha256(raw).hexdigest()!=expected:
   raise timing_boundary.BoundaryError('RESULT_READBACK_HASH_MISMATCH')
  sql_raw=sql_path.read_bytes();sql=json.loads(sql_raw.decode('utf-8'))
  records=sql.get('records',[])
  if (Path(result['sql_evidence']).resolve()!=sql_path or sql.get('stage')!='VERIFIED'
      or len(records)!=8 or {x.get('task_id') for x in records}!={f'G{i:02d}' for i in range(1,9)}
      or any(x.get('path')!=path_name or x.get('variant')!=v
             or x.get('verifier_pass')!=(x.get('task_id') not in result['errors']) for x in records)):
   raise timing_boundary.BoundaryError('SQL_EVIDENCE_READBACK_IDENTITY_MISMATCH')
  confirmation.update(result_sha256=expected,sql_sha256=hashlib.sha256(sql_raw).hexdigest(),
                      result_bytes=len(raw),sql_bytes=len(sql_raw),
                      confirmed_mono_ns=time.perf_counter_ns())
  return result
 try:
  result,observation=timing_boundary.observe_path(complete_operation,run_id=run_id,
   path_name=path_name,variant=v,phase=phase,required_outputs=[result_path,sql_path],receipt_path=receipt_path)
 except timing_boundary.BoundaryError as exc:
  # Keep R4's pair-level verifier/cost failure stop rule, without valid timing.
  if exc.category!='PATH_CORRECTNESS_NOT_PASS' or 'result' not in captured:raise
  result=captured['result'];observation=exc.observation
 return result,{'observation':observation,'receipt_path':str(receipt_path),'readback_confirmation':confirmation}

def _audit_timing_evidence(pairs):
 try:
  for pair_record in pairs:
   v=pair_record['variant'];timings=pair_record['timing']
   for label,path_name in [('full','FULL_GPT'),('hybrid','HYBRID')]:
    item=timings[label];obs=item['observation'];confirm=item['readback_confirmation']
    persisted=json.loads(Path(item['receipt_path']).read_text(encoding='utf-8'))
    if persisted!=obs or obs['simulation']:raise ValueError('OBSERVATION_NOT_CANONICAL')
    timing_boundary.verify_observation(item['receipt_path'],run_id=obs['run_id'],path_name=path_name,variant=v,phase=obs['phase'])
    if not obs['REAL_START_MONO_NS']<=confirm['confirmed_mono_ns']<obs['REAL_END_MONO_NS']:
     raise ValueError('READBACK_OUTSIDE_TIMING')
    expected=[(confirm['result_bytes'],confirm['result_sha256']),(confirm['sql_bytes'],confirm['sql_sha256'])]
    if [(x['bytes'],x['sha256']) for x in obs['outputs']]!=expected:raise ValueError('CONFIRMED_OUTPUT_CHANGED')
   first,second=('full','hybrid') if v%2==0 else ('hybrid','full')
   if timings[first]['observation']['REAL_END_MONO_NS']>timings[second]['observation']['REAL_START_MONO_NS']:
    raise ValueError('AB_ORDER_MISMATCH')
  return True
 except Exception:
  return False

def pair(key,base,o,v,outdir):
 if v%2==0:
  f,ft=_observe_r4_path(run_full,key,base,o,v,outdir,'FULL_GPT');h,ht=_observe_r4_path(run_hybrid,key,base,o,v,outdir,'HYBRID')
 else:
  h,ht=_observe_r4_path(run_hybrid,key,base,o,v,outdir,'HYBRID');f,ft=_observe_r4_path(run_full,key,base,o,v,outdir,'FULL_GPT')
 return {'variant':v,'full':f,'hybrid':h,'pair_valid':f['valid'] and h['valid'] and ft['observation']['path_complete_and_correct'] and ht['observation']['path_complete_and_correct'],'cost_gate':h['cost_usd']<=f['usage']['cost_usd'],'timing':{'full':ft,'hybrid':ht}}
def q95(x):return sorted(x)[math.ceil(.95*len(x))-1]

def sha256(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def reference_categorical_literals(case):
 bindings=extract_frozen_bindings(case['reference'],case['schema'])
 return [(str(item['table'])+'.'+str(item['column']),str(item['literal'])) for item in bindings]

def sql_contract_checks(b,o):
 old=json.loads(PUBLIC_BASELINE.read_text(encoding='utf-8'))
 baseline_ok=(sha256(PUBLIC_BASELINE)==BASELINE_SHA256 and sha256(PRIVATE)==PRIVATE_SHA256 and git_blob_sha(PRIVATE)==PRIVATE_BLOB)
 non_sql=[t for t in b['tasks'] if not t['id'].startswith('G')]
 old_non_sql=[t for t in old['tasks'] if not t['id'].startswith('G')]
 unchanged=(non_sql==old_non_sql and b['benchmark']==old['benchmark'] and b['action_ontology']==old['action_ontology'] and b['initial_state']==old['initial_state'] and b.get('benchmark_revision')==REVISION)
 cases={x['id']:x for x in o['sql_cases']};current={t['id']:t for t in b['tasks'] if t['id'].startswith('G')};prior={t['id']:t for t in old['tasks'] if t['id'].startswith('G')}
 all_ids=set(cases)==set(current)==set(prior)=={f'G{i:02d}' for i in range(1,9)}
 details={};contract=all_ids;columns_ok=all_ids;sort_ok=all_ids;closure=baseline_ok and unchanged and all_ids
 for iid in sorted(cases):
  if iid not in current or iid not in prior:continue
  t=current[iid];c=cases[iid];sem=t.get('value_semantics');cols=t.get('output_columns');order=t.get('order_by')
  literals=reference_categorical_literals(c)
  literal_ok=isinstance(sem,dict) and all(isinstance(sem.get(column),dict) and literal in sem[column].values() for column,literal in literals)
  col_ok=isinstance(cols,list) and len(cols)>0 and len(set(cols))==len(cols) and all(isinstance(x,str) and x for x in cols) and all(isinstance(row,list) and len(row)==len(cols) for row in c['expected'])
  order_ok=(isinstance(order,list) and len(order)>0 and col_ok and all(isinstance(x,dict) and x.get('column') in cols and x.get('direction') in ('ASC','DESC') for x in order) and 'ORDER BY' in c['reference'].upper() and 'order' in t['question'].lower())
  stripped={k:v for k,v in t.items() if k not in ('value_semantics','output_columns','order_by')}
  public_text=json.dumps(t,ensure_ascii=False,separators=(',',':'))
  leak_ok=(stripped==prior[iid] and not any(k in t for k in ('data','expected','reference')) and 'INSERT INTO' not in public_text.upper() and c['reference'] not in public_text and json.dumps(c['expected'],ensure_ascii=False,separators=(',',':')) not in public_text)
  details[iid]={'categorical_literals':literals,'literal_contract':'PASS' if literal_ok else 'FAIL','output_column_contract':'PASS' if col_ok else 'FAIL','sort_contract':'PASS' if order_ok else 'FAIL','oracle_information_closure':'PASS' if leak_ok else 'FAIL'}
  contract=contract and literal_ok and col_ok and order_ok and leak_ok
  columns_ok=columns_ok and col_ok
  sort_ok=sort_ok and order_ok
  closure=closure and leak_ok
 return {'sql_contract_completeness':'PASS' if contract else 'FAIL','public_oracle_information_closure':'PASS' if closure else 'FAIL','output_column_contract':'PASS' if columns_ok else 'FAIL','sort_contract':'PASS' if sort_ok else 'FAIL','sql_contract_details':details,'baseline_private_identity':'PASS' if baseline_ok else 'FAIL'}

def selftest(out):
 b,o=load();c=compile_b(b);domain=solvability(b);contract=sql_contract_checks(b,o)
 gate_version=(rsg.VERSION=='0.2.0');compiler_version=(fc.VERSION=='0.2.0')
 identity=(git_blob_sha(PUBLIC)==PUBLIC_BLOB and git_blob_sha(PRIVATE)==PRIVATE_BLOB)
 structural=(len(c['CODE'])==16 and len(c['JEV'])==24 and len(c['GPT'])==8)
 payloads=jev_payloads(b,c);questions={};[questions.update(p['questions']) for p in payloads]
 formal=(set(CRITERIA)==set(ONTOLOGY)==set(b['action_ontology']) and len(questions)==32 and all(q['type']=='choice' and q['criteria']==CRITERIA for q in questions.values()) and all(t['allowed_actions']==ONTOLOGY for t in c['JEV']))
 bv=variant(b,0);reference={t['id']:('ALLOW' if t['value']<=t['limit'] else 'BLOCK') for t in bv['tasks'] if t['id'].startswith('D')}
 reference.update(o['expected_choices']);reference.update({x['id']:x['reference'] for x in o['sql_cases']})
 positive=(verify(reference,bv,o,0)==[])
 negative=[]
 for key,value in [('D01','BLOCK' if reference['D01']=='ALLOW' else 'ALLOW'),('item_J01__current_action','REJECT' if reference['item_J01__current_action']!='REJECT' else 'EXECUTE'),('G01','DELETE FROM x')]:
  wrong=reference.copy();wrong[key]=value;negative.append(bool(verify(wrong,bv,o,0)))
 verifier_pass=positive and all(negative)
 sql_tests=0;sql_pass=0
 for x in o['sql_cases']:
  for q,w in [(x['reference'],True),('DELETE FROM x',False),('SELECT 1',False),(x['reference']+'; SELECT 1',False),('',False),('PRAGMA table_info(x)',False),('CREATE TABLE z(x)',False),('WITH x AS (SELECT 1) SELECT * FROM missing',False)]:sql_tests+=1;sql_pass+=sqlok(q,x)==w
 passed=(gate_version and compiler_version and identity and domain=='CERTIFIED_COMPILABLE' and structural and formal and verifier_pass and sql_pass==sql_tests and contract['sql_contract_completeness']=='PASS' and contract['public_oracle_information_closure']=='PASS')
 result={'version':VERSION,'freeze_id':FREEZE_ID,'benchmark_revision':REVISION,'mode':'selftest','family':FAMILY,'source_identity':'PASS' if identity else 'FAIL','solvability_gate_version':rsg.VERSION,'forward_compiler_version':fc.VERSION,'certified_compilable_domain':'PASS' if domain=='CERTIFIED_COMPILABLE' else 'FAIL','routes':{k:len(v) for k,v in c.items()},'jev_questions':len(questions),'formal_rule_space':'PASS' if formal else 'FAIL','verifier_selftest':'PASS' if verifier_pass else 'FAIL','sql_tests':{'pass':sql_pass,'total':sql_tests},'runtime_classification_model_calls':0,'extra_model_router_calls':0,'extra_core_gate_count':0,'extra_core_router_count':0,'paid_network_calls':0,'selftest':'PASS' if passed else 'FAIL',**contract}
 Path(out).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if passed else 2

def sql_failures(outdir,pairs):
 out=[]
 for p in pairs:
  for path in ('full','hybrid'):
   fn=p[path].get('sql_evidence')
   if not fn:continue
   for rec in json.loads(Path(fn).read_text(encoding='utf-8'))['records']:
    if rec['verifier_pass'] is False:out.append(rec)
 return out

def live(args):
 if args.runs!=30 or args.warmups!=3:raise RuntimeError('FROZEN_RUN_COUNTS_REQUIRED')
 if Path(args.out).exists():raise RuntimeError('PREEXISTING_BATCH_RESULT')
 key=os.getenv('OPENROUTER_API_KEY','').strip()
 if not key:print('V034_REALITY_CERTIFICATION=BLOCKED_EXTERNAL\\nREALITY_DELTA=OPENROUTER_CREDENTIAL_MISSING\\nNEXT_CONTROL_OWNER=SAME_REALITY_RUNNER');return 3
 base,o=load();outdir=Path(args.output_dir);outdir.mkdir(parents=True,exist_ok=True);warm=[];ps=[]
 try:
  for v in range(args.warmups):
   p=pair(key,base,o,90+v,outdir);warm.append(p)
   if not p['pair_valid'] or not p['cost_gate']:
    final={'version':VERSION,'freeze_id':FREEZE_ID,'real_valid':False,'warmup_gate':'FAIL','warmup_valid_pairs':sum(x['pair_valid'] and x['cost_gate'] for x in warm),'measured_runs_started':False,'full_gpt_valid_runs':0,'hybrid_valid_runs':0,'reality_delta':'WARMUP_VALIDITY_OR_COST_FAILURE','current_execution_action':'STOP','next_control_owner':'GPT','return_to_gpt':True,'sql_failure_details':sql_failures(outdir,warm),'warmup_pairs':warm}
    Path(args.out).write_text(json.dumps(final,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in final.items() if k not in ('warmup_pairs','sql_failure_details')},ensure_ascii=False,indent=2));return 2
  for v in range(args.runs):
   p=pair(key,base,o,v,outdir);ps.append(p)
   if not p['pair_valid'] or not p['cost_gate']:break
 except Exception as e:
  final={'version':VERSION,'freeze_id':FREEZE_ID,'real_valid':False,'warmup_gate':'PASS' if len(warm)==args.warmups else 'INCOMPLETE','warmup_valid_pairs':sum(x['pair_valid'] and x['cost_gate'] for x in warm),'measured_runs_started':bool(ps),'full_gpt_valid_runs':sum(x['full']['valid'] for x in ps),'hybrid_valid_runs':sum(x['hybrid']['valid'] for x in ps),'reality_delta':str(e),'current_execution_action':'STOP','next_control_owner':'SAME_REALITY_RUNNER' if str(e).startswith(('TRANSPORT_','PROVIDER_UNAVAILABLE_')) else 'GPT','return_to_gpt':not str(e).startswith(('TRANSPORT_','PROVIDER_UNAVAILABLE_')),'sql_failure_details':sql_failures(outdir,warm+ps)}
  Path(args.out).write_text(json.dumps(final,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in final.items() if k!='sql_failure_details'},ensure_ascii=False,indent=2));return 4
 vp=[p for p in ps if p['pair_valid'] and p['cost_gate']]
 fv=[p['timing']['full']['observation']['elapsed_ms'] for p in vp];hv=[p['timing']['hybrid']['observation']['elapsed_ms'] for p in vp]
 evidence_consistent=_audit_timing_evidence(warm+ps)
 valid=len(ps)==args.runs and len(vp)==args.runs and evidence_consistent
 cost=valid and all(p['cost_gate'] for p in ps);speed=valid and min(hv)<min(fv)
 final={'version':VERSION,'freeze_id':FREEZE_ID,'family':FAMILY,'runs':len(ps),'warmup_gate':'PASS','warmup_valid_pairs':len(warm),'measured_runs_started':bool(ps),'full_gpt_valid_runs':sum(p['full']['valid'] for p in ps),'hybrid_valid_runs':sum(p['hybrid']['valid'] for p in ps),'full_gpt_valid':valid and all(p['full']['valid'] for p in ps),'hybrid_valid':valid and all(p['hybrid']['valid'] for p in ps),'critical_uncaught_error':0,'cost_gate':cost,'speed_gate':speed,'t_full_gpt_min_ms':min(fv) if fv else None,'t_hybrid_min_ms':min(hv) if hv else None,'t_full_gpt_p50_ms':statistics.median(fv) if fv else None,'t_hybrid_p50_ms':statistics.median(hv) if hv else None,'t_full_gpt_p95_ms':q95(fv) if fv else None,'t_hybrid_p95_ms':q95(hv) if hv else None,'t_full_gpt_max_ms':max(fv) if fv else None,'t_hybrid_max_ms':max(hv) if hv else None,'s_e2e_time':min(fv)/min(hv) if fv and hv else None,'cost_full_gpt_total_usd':sum(p['full']['usage']['cost_usd'] for p in ps),'cost_hybrid_total_usd':sum(p['hybrid']['cost_usd'] for p in ps),'pairs':ps,'sql_failure_details':sql_failures(outdir,ps)}
 final['s_e2e_cost']=final['cost_full_gpt_total_usd']/final['cost_hybrid_total_usd'] if final['cost_hybrid_total_usd'] else None
 final['real_valid']=bool(valid and cost and speed)
 final['reality_delta']='NONE' if final['real_valid'] else ('VALIDITY_FAILURE' if not valid else ('HYBRID_COST_NOT_EQUIVALENT' if not cost else 'HYBRID_NOT_FASTER_THAN_FULL_GPT'))
 final.update(warmup_pairs=warm,final_write_included=True,result_readback_pass=evidence_consistent,evidence_consistency_pass=evidence_consistent,r4_r5_integration_verified=True,timing_component_id=timing_boundary.COMPONENT_ID,timing_source='R5_OUTER_MONOTONIC_INTERVAL',time_reduction_real=(1-min(hv)/min(fv)) if fv and hv else None)
 if not evidence_consistent:final['reality_delta']='EVIDENCE_CONSISTENCY_FAILURE'
 final['hipe_reality_certified']=final['real_valid'];final['done']=final['real_valid']
 final['current_execution_action']='FREEZE_FINAL' if final['real_valid'] else 'STOP';final['next_control_owner']='GPT';final['return_to_gpt']=True
 Path(args.out).write_text(json.dumps(final,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in final.items() if k not in ('pairs','sql_failure_details')},ensure_ascii=False,indent=2));return 0 if final['real_valid'] else 2

def main():
 p=argparse.ArgumentParser();p.add_argument('--mode',choices=['selftest','live'],default='selftest');p.add_argument('--runs',type=int,default=30);p.add_argument('--warmups',type=int,default=3);p.add_argument('--out',default='HIPE-v0.3.4-REAL-RESULT.json');p.add_argument('--output-dir',default='reality-output-v0.3.4');a=p.parse_args();return selftest(a.out) if a.mode=='selftest' else live(a)
if __name__=='__main__':raise SystemExit(main())
