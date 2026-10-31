"""Native OMP skill-read gate; completed events only, no model self-report."""
import json
from pathlib import Path
REQUIRED={'pi-mature-routing','ai-automation-organization-v5','dsh-extreme-effective-time','dsh-mature-capabilities','reuse-experience-brain'}
def audit(directory):
    p=Path(directory)/'backup.stdout.jsonl';es=[]
    if p.exists():
        for line in p.read_text(encoding='utf-8-sig',errors='replace').splitlines():
            try:
                e=json.loads(line)
                if isinstance(e,dict):es.append(e)
            except ValueError:pass
    done={e.get('toolCallId') for e in es if e.get('type')=='tool_execution_end' and not e.get('isError')}
    loaded=set()
    for e in es:
        if e.get('type')=='tool_execution_start' and e.get('toolName')=='read' and e.get('toolCallId') in done:
            path=e.get('args',{}).get('path','')
            for name in REQUIRED:
                if path=='skill://'+name or path.startswith('skill://'+name+'/'):loaded.add(name)
    return {'pass':REQUIRED.issubset(loaded),'loaded':sorted(loaded),'missing':sorted(REQUIRED-loaded),'session_ids':[e['id'] for e in es if e.get('type')=='session']}
