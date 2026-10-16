import pathlib,json,time,psutil
R=pathlib.Path('C:/AI/Orca-Codex-Validation-20261014/suite-ab-20261016-r3')
rows=[]
for p in sorted(R.iterdir()):
 if not p.is_dir():continue
 row={'attempt':p.name,'receipts':[f.name for f in p.glob('*.json')]}
 for n in ['input','local-acceptance']:
  if (p/(n+'.json')).exists():row[n]=json.loads((p/(n+'.json')).read_text(encoding='utf-8'))
 if 'input' in row:row['elapsed_s']=round(time.monotonic()-row['input']['started_mono'],1)
 for label in ['initial','resume']:
  e=p/(label+'-events.jsonl');events=[]
  if e.exists():
   for line in e.read_text(encoding='utf-8',errors='replace').splitlines():
    try:events.append(json.loads(line))
    except ValueError:pass
   row[label]={'events':len(events),'sessions':[x.get('thread_id') for x in events if x.get('type')=='thread.started'],'errors':[x for x in events if x.get('type') in ['error','turn.failed']][-3:],'completed_turns':sum(x.get('type')=='turn.completed' for x in events),'last_item_types':[x.get('item',{}).get('type') for x in events[-5:]],'latest_message':[x.get('item',{}).get('text','')[:1200] for x in events if x.get('item',{}).get('type')=='agent_message'][-1:]}
 if (p/'result.json').exists():
  j=json.loads((p/'result.json').read_text(encoding='utf-8'));row['result']={k:j.get(k) for k in ['passed','error','remaining_cleanup','remaining_task_processes']}
 for e in p.glob('*-error.json'):row[e.name]=json.loads(e.read_text(encoding='utf-8'))
 rows.append(row)
print(json.dumps({'available_GiB':round(psutil.virtual_memory().available/1024**3,2),'attempts':rows},ensure_ascii=False))
