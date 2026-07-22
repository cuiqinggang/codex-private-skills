#!/usr/bin/env python3
import re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ALLOW={'SOURCE_MANIFEST.json','01_UPSTREAM_AUDIT.md','02_LICENSE_AND_RISK_AUDIT.md','03_CONTENT_COMPLETENESS.md','README_CN.md','update_upstream.ps1','audit_sources.py'}
hits=[]
for f in ROOT.rglob('*'):
    if not f.is_file() or any(x in f.parts for x in ('.git','bundled','tests','node_modules','dist','__pycache__')) or f.name in ALLOW or f.name=='package-lock.json': continue
    if f.suffix.lower() not in {'.md','.json','.py','.ps1'}: continue
    text=f.read_text(encoding='utf-8',errors='ignore')
    if re.search(r'https?://',text): hits.append(str(f.relative_to(ROOT)))
print('OFFLINE_DEPENDENCY_CHECK='+('PASS' if not hits else 'FAIL'))
for h in hits: print('EXTERNAL_REFERENCE='+h)
sys.exit(1 if hits else 0)
