from pathlib import Path
import json,re,hashlib,urllib.request
R=Path('C:/AI/TenYears-Animatic-20261030');D=R/'R9';cfg=json.loads((D/'config.json').read_text(encoding='utf-8'))
p=cfg['P']['prompt'];start=p.find('exact single incoming text ');end=p.find(' Nothing on the display',start)
assert start>=0 and end>start
cfg['P']['prompt']=p[:start]+'exact single incoming text \u8001\u516c\uff0c\u60f3\u4f60\u4e86\u3002'+p[end:]
assert '\ufffd' not in cfg['P']['prompt'];assert '\u8001\u516c\uff0c\u60f3\u4f60\u4e86\u3002' in cfg['P']['prompt']
(D/'config-corrected-next-run.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2),encoding='utf-8')
review={'observed':'Historical P prompt in config contains Unicode replacement characters in the text literal. Original guide image has correct text, but native generated display still changes. Not treated as sole cause of prior bowl/action issues.','fix':'Keep historical config/workflow unchanged for traceability. Correct next-run config and require exact Unicode preflight. Current film text handled by deterministic tracked screen composition; no new GPU submission.','preflight':'PASS: exact codepoints present and U+FFFD absent in corrected P prompt','generation_repeated':False}
(D/'unicode-cause-and-fix.json').write_text(json.dumps(review,indent=2),encoding='utf-8')
rows=[]
for p in [D/'A',D/'P']+[D/'RESTORE'/x for x in ['A','P','B_AV','C']]:
 f=p/'telemetry.json';ts=json.loads(f.read_text(encoding='utf-8')) if f.exists() else []
 rows.append({'phase':str(p.relative_to(D)),'samples':len(ts),'max_ram_percent':max([x['ram_percent'] for x in ts],default=None),'last_sample_elapsed':ts[-1]['elapsed'] if ts else None,'guard_stop_exists':(p/'guard-stop.json').exists(),'guard_finished_exists':(p/'guard-finished.json').exists()})
(D/'resource-summary.json').write_text(json.dumps({'admission':90,'runtime_stop':95,'scope':'this film only','phases':rows,'queue':json.load(urllib.request.urlopen('http://127.0.0.1:8197/queue'))},indent=2),encoding='utf-8')
print(json.dumps(rows),flush=True)
