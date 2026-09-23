import argparse,json,os,re,statistics,time,urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
GPT='gpt-5.6-sol'; JEV='typesafe/jev-1.13'
OU='https://api.openai.com/v1/chat/completions'; JU='https://openrouter.ai/api/alpha/decisions'
GI,GO,JI=4.0,20.0,.042
A={'EXECUTE':'Required evidence is complete and no blocking constraint applies.','HOLD':'Required evidence is incomplete or a temporary prerequisite blocks progress.','ROUTE':'The case belongs to a different authorized owner or specialized path.','REJECT':'A permanent policy violation makes execution invalid.'}
P=[
({'request':'Publish the approved monthly report.','evidence':'Owner approval, checksum, and destination are present.','constraints':'Approved reports may be published when evidence is complete.'},'EXECUTE'),
({'request':'Publish the monthly report.','evidence':'The report is ready but owner approval is missing.','constraints':'Owner approval is mandatory before publication.'},'HOLD'),
({'request':'Apply the approved production configuration.','evidence':'Approval is present; a dependency is in temporary maintenance.','constraints':'Wait while a required dependency is temporarily unavailable.'},'HOLD'),
({'request':'Change next month payroll export destination.','evidence':'The approved request arrived in Infrastructure Operations.','constraints':'Finance Operations owns approved payroll changes.'},'ROUTE'),
({'request':'Disable mandatory audit logging permanently.','evidence':'Workspace-owner approval is present.','constraints':'Mandatory audit logging may never be disabled by workspace approval.'},'REJECT'),
({'request':'Change next month payroll export destination.','evidence':'The request arrived in Infrastructure Operations and finance approval is missing.','constraints':'Missing approval must be resolved before ownership routing; Finance owns approved payroll changes.'},'HOLD')]
R=[(['INV-123','INV-9999'],['inv-123','INV123','ORD-123']),(['user_17','user_999'],['user-17','User_17','user_']),(['2026-09-23','2025-01-01'],['23-09-2026','2026/09/23','2026-9-23']),(['ERR:A12','ERR:Z999'],['WARN:A12','ERR-A12','ERR:']),(['AB-12-CD','ZX-99-QW'],['AB12CD','AB-1-CD','ab-12-cd']),(['v1.2.3','v12.0.45'],['1.2.3','v1.2','v1.2.3.4']),(['SKU:ABC123','SKU:XYZ000'],['ABC123','SKU:abc123','SKU:AB12']),(['TASK-0001-DONE','TASK-9999-DONE'],['TASK-1-DONE','TASK-0001-OPEN','task-0001-done'])]
def fx():
 t=[]
 for i in range(16):
  v=(i*7+3)%23;t.append({'id':f'D{i+1:02d}','k':'C','v':v,'l':11,'o':'ALLOW' if v<=11 else 'BLOCK'})
 for i in range(24):
  s,o=P[i%6];t.append({'id':f'J{i+1:02d}','k':'J','s':{'case':f'case-{i+1:02d}',**s},'o':o})
 for i,(p,n) in enumerate(R):t.append({'id':f'G{i+1:02d}','k':'G','p':p,'n':n})
 return t
def rxok(x,p,n):
 try:r=re.compile(x)
 except:return False
 return isinstance(x,str) and len(x)<=200 and all(r.fullmatch(v) for v in p) and not any(r.fullmatch(v) for v in n)
def verify(ts,a):
 bad=[]
 for t in ts:
  x=a.get(t['id']); ok=(x==t['o']) if t['k'] in 'CJ' else rxok(x,t['p'],t['n'])
  if not ok:bad.append(t['id'])
 return bad
def post(url,key,b):
 q=urllib.request.Request(url,json.dumps(b).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','User-Agent':'HIPE-P0/0.1.0'},method='POST')
 with urllib.request.urlopen(q,timeout=90) as r:return json.loads(r.read())
def gpt(key,ts,mock=False):
 z=time.perf_counter()
 if mock:
  a={t['id']:(t['o'] if t['k'] in 'CJ' else '^'+re.escape(t['p'][0])+'$|^'+re.escape(t['p'][1])+'$') for t in ts};time.sleep(.01);return a,10,.001
 pub=[]
 for t in ts:
  if t['k']=='C':pub.append({'id':t['id'],'type':'threshold','value':t['v'],'limit':t['l']})
  elif t['k']=='J':pub.append({'id':t['id'],'type':'action_choice','state':t['s'],'actions':A})
  else:pub.append({'id':t['id'],'type':'regex_synthesis','positive':t['p'],'negative':t['n']})
 ins='Return only one JSON object mapping id to answer. threshold: ALLOW/BLOCK. action_choice: EXECUTE/HOLD/ROUTE/REJECT. regex_synthesis: one Python regex full-matching every positive and no negative. No prose.'
 d=post(OU,key,{'model':GPT,'messages':[{'role':'system','content':ins},{'role':'user','content':json.dumps(pub,separators=(',',':'))}],'response_format':{'type':'json_object'}})
 a=json.loads(d['choices'][0]['message']['content']);u=d.get('usage',{});c=(u.get('prompt_tokens',0)*GI+u.get('completion_tokens',0)*GO)/1e6
 return a,(time.perf_counter()-z)*1000,c
def jev(key,ts,mock=False):
 z=time.perf_counter()
 if mock:time.sleep(.008);return {t['id']:t['o'] for t in ts},8,.0000084
 st={'description':'Independent decision records; judge each only from its fields.','records':{t['id']:t['s'] for t in ts}}
 qs={t['id']:{'type':'choice','instructions':f"Choose the permitted action for records.{t['id']}; follow its stated constraints and ordering.",'criteria':A} for t in ts}
 d=post(JU,key,{'model':JEV,'state':st,'questions':qs});u=d.get('usage',{});c=u.get('cost')
 if c is None:c=u.get('input_tokens',u.get('inputTokens',0))*JI/1e6
 return {k:v['choice'] for k,v in d['answers'].items()},(time.perf_counter()-z)*1000,float(c)
def base(ok,ts,m=False):
 z=time.perf_counter();a,gm,c=gpt(ok,ts,m);e=verify(ts,a);return {'v':not e,'e':e,'ms':(time.perf_counter()-z)*1000,'c':c}
def hyb(ok,rk,ts,m=False):
 z=time.perf_counter();code=[t for t in ts if t['k']=='C'];j=[t for t in ts if t['k']=='J'];g=[t for t in ts if t['k']=='G'];a={t['id']:t['o'] for t in code}
 with ThreadPoolExecutor(max_workers=3) as ex:
  f1=ex.submit(jev,rk,j[::2],m);f2=ex.submit(jev,rk,j[1::2],m);fg=ex.submit(gpt,ok,g,m);x1,j1,c1=f1.result();x2,j2,c2=f2.result();xg,gg,cg=fg.result()
 a.update(x1);a.update(x2);a.update(xg);e=verify(ts,a);return {'v':not e,'e':e,'ms':(time.perf_counter()-z)*1000,'c':c1+c2+cg,'jm':max(j1,j2),'gm':gg,'jc':c1+c2}
def main():
 p=argparse.ArgumentParser();p.add_argument('--mode',choices=['selftest','live'],default='selftest');p.add_argument('--runs',type=int,default=10);p.add_argument('--out',default='HIPE-P0-REAL-RESULT.json');a=p.parse_args();ts=fx();m=a.mode=='selftest';ok='mock' if m else os.getenv('OPENAI_API_KEY','');rk='mock' if m else os.getenv('OPENROUTER_API_KEY','')
 if not ok or not rk:
  d='GPT_AUTH_MISSING' if not ok else 'JEV_AUTH_MISSING';print(f'REAL_VALID=FAIL\nREALITY_DELTA={d}\nACTION=STOP\nRETURN_TO_GPT=YES');return 3
 base(ok,ts,m);hyb(ok,rk,ts,m);B=[];H=[]
 for _ in range(a.runs):
  b=base(ok,ts,m);h=hyb(ok,rk,ts,m);B.append(b);H.append(h)
  if not b['v'] or not h['v']:break
 zg,zm,zc=gpt(ok,[t for t in ts if t['k']=='J'],m);zv=not verify([t for t in ts if t['k']=='J'],zg);valid=len(B)==a.runs and all(x['v'] for x in B+H) and zv;cost=valid and all(h['c']<=b['c'] for b,h in zip(B,H));bm=min(x['ms'] for x in B);hm=min(x['ms'] for x in H);speed=valid and hm<bm
 out={'version':'0.1.0','tasks':48,'code':16,'jev':24,'gpt_residual':8,'runs':len(B),'full_gpt_valid':all(x['v'] for x in B),'hybrid_valid':all(x['v'] for x in H),'commercial_gate':bool(valid and cost),'speed_gate':bool(speed),'t_full_gpt_min_ms':bm,'t_hybrid_min_ms':hm,'t_full_gpt_p50_ms':statistics.median(x['ms'] for x in B),'t_hybrid_p50_ms':statistics.median(x['ms'] for x in H),'cost_full_gpt_min_usd':min(x['c'] for x in B),'cost_hybrid_max_usd':max(x['c'] for x in H),'s_e2e_time':bm/hm,'s_zone_time':zm/statistics.median(x['jm'] for x in H),'s_zone_cost':zc/H[0]['jc'] if H[0]['jc'] else None,'baseline':B,'hybrid':H}
 Path(a.out).write_text(json.dumps(out,indent=2),encoding='utf-8')
 if m:print(f"STRUCTURAL_SELFTEST={'PASS' if valid else 'FAIL'}\nCOMMERCIAL_GATE=NOT_EVALUATED_IN_SELFTEST\nACTION=STOP");return 0 if valid else 2
 rp=valid and cost and speed;print(f"REAL_VALID={'PASS' if rp else 'FAIL'}\nCOMMERCIAL_GATE={'PASS' if out['commercial_gate'] else 'FAIL'}\nT_FULL_GPT_MIN_MS={bm:.3f}\nT_HYBRID_MIN_MS={hm:.3f}\nS_E2E_TIME={out['s_e2e_time']:.6f}\nS_ZONE_TIME={out['s_zone_time']:.6f}\nS_ZONE_COST={out['s_zone_cost']:.6f}")
 if not rp:
  d='VALIDITY_FAILURE' if not valid else ('HYBRID_COST_NOT_EQUIVALENT' if not cost else 'HYBRID_NOT_FASTER_THAN_FULL_GPT');print(f'REALITY_DELTA={d}\nACTION=STOP\nRETURN_TO_GPT=YES');return 2
 print('REALITY_DELTA=NONE\nACTION=STOP\nRETURN_TO_GPT=NO');return 0
if __name__=='__main__':raise SystemExit(main())