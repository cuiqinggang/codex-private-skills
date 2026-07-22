#!/usr/bin/env python3
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'capability-map.json').read_text(encoding='utf-8'));missing=[]
for key in ('clone_skill','design_skill'):
 p=Path(data[key]['path'])
 if not (p/'SKILL.md').exists():missing.append(f'{data[key]["name"]}:{p}')
print('SKILL_AVAILABILITY='+('PASS' if not missing else 'FAIL'))
for x in missing:print('MISSING='+x)
sys.exit(1 if missing else 0)

