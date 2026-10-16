import pathlib,json,time,hashlib,sys,statistics
R=pathlib.Path('C:/AI/Orca-Codex-Validation-20261014/suite-ab-20261016-r1')
label=sys.argv[1];assert label=='pilot-B' or __import__('re').fullmatch(r'p[0-9]{2}-[AB]',label)
P=R/label
r=json.loads((P/'result.json').read_text(encoding='utf-8'))
local=json.loads((P/'local-acceptance.json').read_text(encoding='utf-8'))
assert r['passed'] and local['accepted']
commit=sys.argv[2];assert __import__('re').fullmatch(r'[0-9a-f]{40}',commit)
assert local['result_sha256']==hashlib.sha256((P/'result.json').read_bytes()).hexdigest()
out=P/'ceo-acceptance.json';assert not out.exists(),'Already accepted: read existing receipt'
samples=[json.loads(x) for x in (P/'resources.jsonl').read_text().splitlines()]
good=[x for x in samples if 'rss_bytes' in x];gaps=[b['mono']-a['mono'] for a,b in zip(good,good[1:])]
receipt={'accepted':True,'label':label,'archive_commit':commit,'result_sha256':local['result_sha256'],
'started_mono':local['started_mono'],'full_wall_ms':(time.monotonic()-local['started_mono'])*1000,
'timing_scope':'input_to_independent_acceptance_and_evidence_readback',
'local_wall_ms':local['local_wall_ms'],'scope_note':'Includes setup, model, retries, independent tests, cleanup, CEO diff/test review, first remote result archive and exact readback. Excludes prior design/deployment and later summary.',
'resources':{'samples':len(samples),'errors':len(samples)-len(good),'rss_peak_bytes':max(x['rss_bytes'] for x in good),'available_min_bytes':min(x['available_bytes'] for x in good),'interval_median_s':statistics.median(gaps) if gaps else None,'interval_max_s':max(gaps) if gaps else None,'peak_limitation':'one-second sampling may miss transient spikes'}}
out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8');assert json.loads(out.read_text(encoding='utf-8'))==receipt
print(json.dumps(receipt,ensure_ascii=False))
