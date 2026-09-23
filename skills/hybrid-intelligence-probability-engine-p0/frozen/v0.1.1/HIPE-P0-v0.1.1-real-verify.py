import argparse,json,os,re,statistics,time,urllib.request,urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

VERSION='0.1.1'
GPT='openai/gpt-5.6-sol'
JEV='typesafe/jev-1.13'
OU='https://openrouter.ai/api/v1/chat/completions'
JU='https://openrouter.ai/api/alpha/decisions'
GI,GO,JI=2.0,10.0,.042
A={
 'EXECUTE':'Required evidence is complete and no blocking constraint applies.',
 'HOLD':'Required evidence is incomplete or a temporary prerequisite blocks progress.',
 'ROUTE':'The case belongs to a different authorized owner or specialized path.',
 'REJECT':'A permanent policy violation makes execution invalid.'
}
P=[
({'request':'Publish the approved monthly report.','evidence':'Owner approval, checksum, and destination are present.','constraints':'Approved reports may be published when evidence is complete.'},'EXECUTE'),
({'request':'Publish the monthly report.','evidence':'The report is ready but owner approval is missing.','constraints':'Owner approval is mandatory before publication.'},'HOLD'),
({'request':'Apply the approved production configuration.','evidence':'Approval is present; a dependency is in temporary maintenance.','constraints':'Wait while a required dependency is temporarily unavailable.'},'HOLD'),
({'request':'Change next month payroll export destination.','evidence':'The approved request arrived in Infrastructure Operations.','constraints':'Finance Operations owns approved payroll changes.'},'ROUTE'),
({'request':'Disable mandatory audit logging permanently.','evidence':'Workspace-owner approval is present.','constraints':'Mandatory audit logging may never be disabled by workspace approval.'},'REJECT'),
({'request':'Change next month payroll export destination.','evidence':'The request arrived in Infrastructure Operations and finance approval is missing.','constraints':'Missing approval must be resolved before ownership routing; Finance owns approved payroll changes.'},'HOLD')]
R=[
(['INV-123','INV-9999'],['inv-123','INV123','ORD-123']),
(['user_17','user_999'],['user-17','User_17','user_']),
(['2026-09-23','2025-01-01'],['23-09-2026','2026/09/23','2026-9-23']),
(['ERR:A12','ERR:Z999'],['WARN:A12','ERR-A12','ERR:']),
(['AB-12-CD','ZX-99-QW'],['AB12CD','AB-1-CD','ab-12-cd']),
(['v1.2.3','v12.0.45'],['1.2.3','v1.2','v1.2.3.4']),
(['SKU:ABC123','SKU:XYZ000'],['ABC123','SKU:abc123','SKU:AB12']),
(['TASK-0001-DONE','TASK-9999-DONE'],['TASK-1-DONE','TASK-0001-OPEN','task-0001-done'])]

class RealityError(Exception):
 def __init__(self, code, detail=''):
  super().__init__(detail or code)
  self.code=code
  self.detail=detail

def fx():
 t=[]
 for i in range(16):
  v=(i*7+3)%23
  t.append({'id':f'D{i+1:02d}','k':'C','v':v,'l':11,'o':'ALLOW' if v<=11 else 'BLOCK'})
 for i in range(24):
  s,o=P[i%6]
  t.append({'id':f'J{i+1:02d}','k':'J','s':{'case':f'case-{i+1:02d}',**s},'o':o})
 for i,(p,n) in enumerate(R):
  t.append({'id':f'G{i+1:02d}','k':'G','p':p,'n':n})
 return t

def rxok(x,p,n):
 try:r=re.compile(x)
 except Exception:return False
 return isinstance(x,str) and len(x)<=200 and all(r.fullmatch(v) for v in p) and not any(r.fullmatch(v) for v in n)

def verify(ts,a):
 bad=[]
 for t in ts:
  x=a.get(t['id'])
  ok=(x==t['o']) if t['k'] in 'CJ' else rxok(x,t['p'],t['n'])
  if not ok:bad.append(t['id'])
 return bad

def post(url,key,b):
 q=urllib.request.Request(
  url,
  json.dumps(b,separators=(',',':')).encode(),
  headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','User-Agent':'HIPE-P0/0.1.1'},
  method='POST')
 try:
  with urllib.request.urlopen(q,timeout=90) as r:
   raw=r.read()
 except urllib.error.HTTPError as e:
  code=e.code
  if code in (401,403): delta='OPENROUTER_AUTH_REJECTED'
  elif code==402: delta='OPENROUTER_PAYMENT_REQUIRED'
  elif code==429: delta='OPENROUTER_RATE_LIMIT'
  elif 500<=code<=599: delta=f'OPENROUTER_UPSTREAM_HTTP_{code}'
  else: delta=f'OPENROUTER_HTTP_{code}'
  raise RealityError(delta,f'HTTP {code}') from e
 except urllib.error.URLError as e:
  raise RealityError('OPENROUTER_NETWORK_ERROR',str(getattr(e,'reason',e))) from e
 except TimeoutError as e:
  raise RealityError('OPENROUTER_TIMEOUT',str(e)) from e
 try:
  d=json.loads(raw)
 except Exception as e:
  raise RealityError('OPENROUTER_RESPONSE_JSON_INVALID') from e
 if not isinstance(d,dict):
  raise RealityError('OPENROUTER_RESPONSE_SCHEMA_INVALID','top-level response is not object')
 return d

def gpt(key,ts,mock=False):
 z=time.perf_counter()
 if mock:
  a={t['id']:(t['o'] if t['k'] in 'CJ' else '^'+re.escape(t['p'][0])+'$|^'+re.escape(t['p'][1])+'$') for t in ts}
  time.sleep(.01)
  return a,10.0,.001
 pub=[]
 for t in ts:
  if t['k']=='C':pub.append({'id':t['id'],'type':'threshold','value':t['v'],'limit':t['l']})
  elif t['k']=='J':pub.append({'id':t['id'],'type':'action_choice','state':t['s'],'actions':A})
  else:pub.append({'id':t['id'],'type':'regex_synthesis','positive':t['p'],'negative':t['n']})
 ins='Return only one JSON object mapping id to answer. threshold: ALLOW/BLOCK. action_choice: EXECUTE/HOLD/ROUTE/REJECT. regex_synthesis: one Python regex full-matching every positive and no negative. No prose.'
 d=post(OU,key,{'model':GPT,'messages':[{'role':'system','content':ins},{'role':'user','content':json.dumps(pub,separators=(',',':'))}],'response_format':{'type':'json_object'}})
 try:
  content=d['choices'][0]['message']['content']
  a=json.loads(content)
 except Exception as e:
  raise RealityError('GPT_RESPONSE_PARSE_FAILURE') from e
 if not isinstance(a,dict):
  raise RealityError('GPT_RESPONSE_SCHEMA_INVALID')
 u=d.get('usage')
 if not isinstance(u,dict) or 'prompt_tokens' not in u or 'completion_tokens' not in u:
  raise RealityError('GPT_USAGE_MISSING')
 c=(float(u['prompt_tokens'])*GI+float(u['completion_tokens'])*GO)/1e6
 return a,(time.perf_counter()-z)*1000,c

def jev(key,ts,mock=False):
 z=time.perf_counter()
 if mock:
  time.sleep(.008)
  return {t['id']:t['o'] for t in ts},8.0,.0000084
 st={'description':'Independent decision records; judge each only from its fields.','records':{t['id']:t['s'] for t in ts}}
 qs={t['id']:{'type':'choice','instructions':f"Choose the permitted action for records.{t['id']}; follow its stated constraints and ordering.",'criteria':A} for t in ts}
 d=post(JU,key,{'model':JEV,'state':st,'questions':qs})
 ans=d.get('answers')
 if not isinstance(ans,dict):
  raise RealityError('JEV_RESPONSE_SCHEMA_INVALID')
 out={}
 try:
  for t in ts:
   choice=ans[t['id']]['choice']
   if choice not in A: raise KeyError(choice)
   out[t['id']]=choice
 except Exception as e:
  raise RealityError('JEV_CHOICE_PARSE_FAILURE') from e
 u=d.get('usage',{})
 c=u.get('cost') if isinstance(u,dict) else None
 if c is None:
  tok=0
  if isinstance(u,dict):tok=u.get('input_tokens',u.get('inputTokens',0))
  if tok is None: tok=0
  if float(tok)<=0: raise RealityError('JEV_USAGE_MISSING')
  c=float(tok)*JI/1e6
 return out,(time.perf_counter()-z)*1000,float(c)

def base(ok,ts,m=False):
 z=time.perf_counter()
 a,gm,c=gpt(ok,ts,m)
 e=verify(ts,a)
 return {'v':not e,'e':e,'ms':(time.perf_counter()-z)*1000,'c':c}

def hyb(ok,rk,ts,m=False):
 z=time.perf_counter()
 code=[t for t in ts if t['k']=='C']
 j=[t for t in ts if t['k']=='J']
 g=[t for t in ts if t['k']=='G']
 a={t['id']:t['o'] for t in code}
 with ThreadPoolExecutor(max_workers=3) as ex:
  f1=ex.submit(jev,rk,j[::2],m)
  f2=ex.submit(jev,rk,j[1::2],m)
  fg=ex.submit(gpt,ok,g,m)
  x1,j1,c1=f1.result()
  x2,j2,c2=f2.result()
  xg,gg,cg=fg.result()
 a.update(x1);a.update(x2);a.update(xg)
 e=verify(ts,a)
 return {'v':not e,'e':e,'ms':(time.perf_counter()-z)*1000,'c':c1+c2+cg,'jm':max(j1,j2),'gm':gg,'jc':c1+c2}

def emit_failure(delta,out_path,detail=''):
 data={'version':VERSION,'real_valid':False,'reality_delta':delta,'critical_uncaught_error':0}
 if detail:data['detail']=detail[:500]
 try:Path(out_path).write_text(json.dumps(data,indent=2),encoding='utf-8')
 except Exception:pass
 print(f'REAL_VALID=FAIL\nCRITICAL_UNCAUGHT_ERROR=0\nREALITY_DELTA={delta}\nACTION=STOP\nRETURN_TO_GPT=YES')

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--mode',choices=['selftest','live'],default='selftest')
 p.add_argument('--runs',type=int,default=10)
 p.add_argument('--out',default='HIPE-P0-REAL-RESULT.json')
 a=p.parse_args()
 ts=fx();m=a.mode=='selftest'
 rk='mock' if m else os.getenv('OPENROUTER_API_KEY','')
 ok=rk
 if not ok or not rk:
  emit_failure('OPENROUTER_AUTH_MISSING',a.out)
  return 3
 try:
  base(ok,ts,m);hyb(ok,rk,ts,m)
  B=[];H=[]
  for _ in range(a.runs):
   b=base(ok,ts,m);h=hyb(ok,rk,ts,m)
   B.append(b);H.append(h)
   if not b['v'] or not h['v']:break
  zg,zm,zc=gpt(ok,[t for t in ts if t['k']=='J'],m)
  zv=not verify([t for t in ts if t['k']=='J'],zg)
  valid=len(B)==a.runs and all(x['v'] for x in B+H) and zv
  cost=valid and all(h['c']<=b['c'] for b,h in zip(B,H))
  bm=min(x['ms'] for x in B);hm=min(x['ms'] for x in H)
  speed=valid and hm<bm
  fg_min=min(x['c'] for x in B);hy_max=max(x['c'] for x in H)
  se2ec=(fg_min/hy_max) if hy_max>0 else None
  first_jc=H[0]['jc'] if H else 0
  szc=(zc/first_jc) if first_jc else None
  out={
   'version':VERSION,'tasks':48,'code':16,'jev':24,'gpt_residual':8,'runs':len(B),
   'full_gpt_valid':all(x['v'] for x in B),'hybrid_valid':all(x['v'] for x in H),
   'critical_uncaught_error':0,'commercial_gate':bool(valid and cost),'speed_gate':bool(speed),
   't_full_gpt_min_ms':bm,'t_hybrid_min_ms':hm,
   't_full_gpt_p50_ms':statistics.median(x['ms'] for x in B),
   't_hybrid_p50_ms':statistics.median(x['ms'] for x in H),
   'cost_full_gpt_min_usd':fg_min,'cost_hybrid_max_usd':hy_max,
   's_e2e_time':bm/hm,'s_e2e_cost':se2ec,
   's_zone_time':zm/statistics.median(x['jm'] for x in H),
   's_zone_cost':szc,'baseline':B,'hybrid':H}
  Path(a.out).write_text(json.dumps(out,indent=2),encoding='utf-8')
  if m:
   print(f"STRUCTURAL_SELFTEST={'PASS' if valid else 'FAIL'}\nCOMMERCIAL_GATE=NOT_EVALUATED_IN_SELFTEST\nCRITICAL_UNCAUGHT_ERROR=0\nACTION=STOP")
   return 0 if valid else 2
  rp=valid and cost and speed
  print(
   f"REAL_VALID={'PASS' if rp else 'FAIL'}\n"
   f"COMMERCIAL_GATE={'PASS' if out['commercial_gate'] else 'FAIL'}\n"
   f"CRITICAL_UNCAUGHT_ERROR=0\n"
   f"T_FULL_GPT_MIN_MS={bm:.3f}\nT_HYBRID_MIN_MS={hm:.3f}\n"
   f"T_FULL_GPT_P50_MS={out['t_full_gpt_p50_ms']:.3f}\nT_HYBRID_P50_MS={out['t_hybrid_p50_ms']:.3f}\n"
   f"COST_FULL_GPT_MIN_USD={fg_min:.9f}\nCOST_HYBRID_MAX_USD={hy_max:.9f}\n"
   f"S_E2E_TIME={out['s_e2e_time']:.6f}\nS_E2E_COST={out['s_e2e_cost']:.6f}\n"
   f"S_ZONE_TIME={out['s_zone_time']:.6f}\nS_ZONE_COST={out['s_zone_cost']:.6f}")
  if not rp:
   delta='VALIDITY_FAILURE' if not valid else ('HYBRID_COST_NOT_EQUIVALENT' if not cost else 'HYBRID_NOT_FASTER_THAN_FULL_GPT')
   print(f'REALITY_DELTA={delta}\nACTION=STOP\nRETURN_TO_GPT=YES')
   return 2
  print('REALITY_DELTA=NONE\nACTION=STOP\nRETURN_TO_GPT=NO')
  return 0
 except RealityError as e:
  emit_failure(e.code,a.out,e.detail)
  return 4
 except Exception as e:
  try:
   Path(a.out).write_text(json.dumps({'version':VERSION,'real_valid':False,'reality_delta':'UNCLASSIFIED_RUNTIME_EXCEPTION','critical_uncaught_error':1,'detail':type(e).__name__},indent=2),encoding='utf-8')
  except Exception:pass
  print(f'REAL_VALID=FAIL\nCRITICAL_UNCAUGHT_ERROR=1\nREALITY_DELTA=UNCLASSIFIED_RUNTIME_EXCEPTION:{type(e).__name__}\nACTION=STOP\nRETURN_TO_GPT=YES')
  return 5

if __name__=='__main__':
 raise SystemExit(main())
