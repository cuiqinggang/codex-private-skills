import argparse,json,math,os,re,sqlite3,statistics,time,urllib.request,urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

VERSION='0.3.0';FAMILY='HIPE-E2E-V3-48';ONTOLOGY=['EXECUTE','HOLD','ROUTE','REJECT']
CRITERIA={
'EXECUTE':'Choose EXECUTE only when the requested action is permitted now and every mandatory prerequisite is satisfied.',
'HOLD':'Choose HOLD when the action may be allowed later but a mandatory prerequisite, timing condition, evidence item, or temporary dependency is not satisfied now.',
'ROUTE':'Choose ROUTE when the request requires a specialist, review path, security response, tax/privacy/billing review, or specialized executor before completion.',
'REJECT':'Choose REJECT when the requested action is prohibited, must never be performed by this workflow, or a permanent failure makes automatic execution impermissible.'}
GPT_URL='https://openrouter.ai/api/v1/chat/completions';JEV_URL='https://openrouter.ai/api/alpha/decisions'
ROOT=Path(__file__).resolve().parent
PUBLIC=ROOT/'PUBLIC-BENCHMARK-v0.3.0.json';PRIVATE=ROOT/'PRIVATE-ORACLE-v0.3.0.json'

def load():return json.loads(PUBLIC.read_text(encoding='utf-8')),json.loads(PRIVATE.read_text(encoding='utf-8'))
def qchoice(s):return {'type':'choice','instructions':s,'criteria':CRITERIA}
def route(t):
 if t.get('operation')=='compare_threshold' and t.get('operator')=='<=' and type(t.get('value')) is int and type(t.get('limit')) is int:return 'CODE'
 if all(isinstance(t.get(k),str) and t[k].strip() for k in ('request','current_state','evidence','constraints')) and t.get('allowed_actions')==ONTOLOGY and isinstance(t.get('dependency_ids'),list) and len(t['dependency_ids'])<=1:return 'JEV'
 if isinstance(t.get('question'),str) and isinstance(t.get('schema'),list) and t.get('dialect')=='sqlite' and t.get('output_contract')=='single SELECT/WITH query only':return 'GPT'
 return 'GPT'
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

def jev_payloads(b):
 j=compile_b(b)['JEV'];ids={x['id'] for x in j};qs={}
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

def gpt_body(b,residual=False):
 provider={'sort':'throughput','require_parameters':True}
 if residual:
  tasks=[t for t in compile_b(b)['GPT'] if t['id'].startswith('G')]
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
 req=urllib.request.Request(url,json.dumps(body,separators=(',',':')).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','User-Agent':'HIPE/0.3.0'},method='POST');t=time.perf_counter_ns()
 try:
  with urllib.request.urlopen(req,timeout=120) as r:d=json.loads(r.read())
 except urllib.error.HTTPError as e:raise RuntimeError('OPENROUTER_AUTH_OR_HTTP_'+str(e.code)) from e
 except Exception as e:raise RuntimeError('OPENROUTER_NETWORK_OR_JSON') from e
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
def run_full(key,base,o,v,outdir):
 t0=time.perf_counter_ns();b=variant(base,v);b=json.loads(json.dumps(b));d,net=post(GPT_URL,key,gpt_body(b));a=gparse(d);bad=verify(a,b,o,v);u=usage(d);r={'path':'FULL_GPT','variant':v,'valid':not bad,'errors':bad,'network_ms':net,'usage':u};p=write(outdir,f'v{v:02d}-full',r);r['e2e_ms']=(time.perf_counter_ns()-t0)/1e6;p.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');return r
def run_hybrid(key,base,o,v,outdir):
 t0=time.perf_counter_ns();b=variant(base,v);b=json.loads(json.dumps(b));c=compile_b(b);a={t['id']:('ALLOW' if t['value']<=t['limit'] else 'BLOCK') for t in c['CODE']};jp=jev_payloads(b);gb=gpt_body(b,True)
 def jc(p):d,m=post(JEV_URL,key,p);return jparse(d,list(p['questions'])),m,usage(d)
 def gc():d,m=post(GPT_URL,key,gb);return gparse(d),m,usage(d)
 with ThreadPoolExecutor(max_workers=3) as ex:
  f1,f2,fg=ex.submit(jc,jp[0]),ex.submit(jc,jp[1]),ex.submit(gc);x1,m1,u1=f1.result();x2,m2,u2=f2.result();xg,mg,ug=fg.result()
 a.update(x1);a.update(x2);a.update(xg);bad=verify(a,b,o,v);r={'path':'HYBRID','variant':v,'valid':not bad,'errors':bad,'component_ms':{'jev_shard_1':m1,'jev_shard_2':m2,'gpt_residual':mg},'usage':{'jev_1':u1,'jev_2':u2,'gpt_residual':ug},'cost_usd':u1['cost_usd']+u2['cost_usd']+ug['cost_usd']};p=write(outdir,f'v{v:02d}-hybrid',r);r['e2e_ms']=(time.perf_counter_ns()-t0)/1e6;p.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');return r
def pair(key,base,o,v,outdir):
 if v%2==0:f=run_full(key,base,o,v,outdir);h=run_hybrid(key,base,o,v,outdir)
 else:h=run_hybrid(key,base,o,v,outdir);f=run_full(key,base,o,v,outdir)
 return {'variant':v,'full':f,'hybrid':h,'pair_valid':f['valid'] and h['valid'],'cost_gate':h['cost_usd']<=f['usage']['cost_usd']}
def q95(x):return sorted(x)[math.ceil(.95*len(x))-1]

def selftest(out):
 b,o=load();c=compile_b(b);structural=(len(c['CODE'])==16 and len(c['JEV'])==24 and len(c['GPT'])==8 and sum(len(x['questions']) for x in jev_payloads(b))==32)
 sql_tests=0;sql_pass=0
 for x in o['sql_cases']:
  for q,w in [(x['reference'],True),('DELETE FROM x',False),('SELECT 1',False),(x['reference']+'; SELECT 1',False),('',False),('PRAGMA table_info(x)',False),('CREATE TABLE z(x)',False),('WITH x AS (SELECT 1) SELECT * FROM missing',False)]:sql_tests+=1;sql_pass+=sqlok(q,x)==w
 result={'version':VERSION,'mode':'selftest','family':FAMILY,'routes':{k:len(v) for k,v in c.items()},'jev_questions':sum(len(x['questions']) for x in jev_payloads(b)),'structural_pass':structural,'sql_tests':{'pass':sql_pass,'total':sql_tests},'paid_network_calls':0};Path(out).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if structural and sql_pass==sql_tests else 2

def live(args):
 key=os.getenv('OPENROUTER_API_KEY','').strip()
 if not key:print('现实有效性=未测试\n现实差异=缺少OpenRouter授权\n动作=停止并返回GPT');return 3
 base,o=load();outdir=Path(args.output_dir);outdir.mkdir(parents=True,exist_ok=True)
 try:
  for v in range(args.warmups):pair(key,base,o,90+v,outdir)
  ps=[]
  for v in range(args.runs):
   p=pair(key,base,o,v,outdir);ps.append(p)
   if not p['pair_valid'] or not p['cost_gate']:break
 except Exception as e:
  final={'version':VERSION,'real_valid':False,'reality_delta':str(e),'pairs_completed':len(locals().get('ps',[]))};Path(args.out).write_text(json.dumps(final,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(final,ensure_ascii=False,indent=2));return 4
 fv=[p['full']['e2e_ms'] for p in ps];hv=[p['hybrid']['e2e_ms'] for p in ps];valid=len(ps)==args.runs and all(p['pair_valid'] for p in ps);cost=valid and all(p['cost_gate'] for p in ps);speed=valid and min(hv)<min(fv)
 final={'version':VERSION,'family':FAMILY,'runs':len(ps),'full_gpt_valid':valid and all(p['full']['valid'] for p in ps),'hybrid_valid':valid and all(p['hybrid']['valid'] for p in ps),'critical_uncaught_error':0,'cost_gate':cost,'speed_gate':speed,'t_full_gpt_min_ms':min(fv) if fv else None,'t_hybrid_min_ms':min(hv) if hv else None,'t_full_gpt_p50_ms':statistics.median(fv) if fv else None,'t_hybrid_p50_ms':statistics.median(hv) if hv else None,'t_full_gpt_p95_ms':q95(fv) if fv else None,'t_hybrid_p95_ms':q95(hv) if hv else None,'s_e2e_time':min(fv)/min(hv) if fv and hv else None,'cost_full_gpt_total_usd':sum(p['full']['usage']['cost_usd'] for p in ps),'cost_hybrid_total_usd':sum(p['hybrid']['cost_usd'] for p in ps),'pairs':ps};final['s_e2e_cost']=final['cost_full_gpt_total_usd']/final['cost_hybrid_total_usd'] if final['cost_hybrid_total_usd'] else None;final['real_valid']=bool(valid and cost and speed);final['reality_delta']='NONE' if final['real_valid'] else ('VALIDITY_FAILURE' if not valid else ('HYBRID_COST_NOT_EQUIVALENT' if not cost else 'HYBRID_NOT_FASTER_THAN_FULL_GPT'));Path(args.out).write_text(json.dumps(final,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in final.items() if k!='pairs'},ensure_ascii=False,indent=2));return 0 if final['real_valid'] else 2

def main():
 p=argparse.ArgumentParser();p.add_argument('--mode',choices=['selftest','live'],default='selftest');p.add_argument('--runs',type=int,default=30);p.add_argument('--warmups',type=int,default=3);p.add_argument('--out',default='HIPE-v0.3.0-REAL-RESULT.json');p.add_argument('--output-dir',default='reality-output-v0.3.0');a=p.parse_args();return selftest(a.out) if a.mode=='selftest' else live(a)
if __name__=='__main__':raise SystemExit(main())
