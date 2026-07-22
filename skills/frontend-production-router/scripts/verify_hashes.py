#!/usr/bin/env python3
import hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];M=ROOT/'FILE_MANIFEST_SHA256.txt'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def deliverable(p):return p.is_file() and not any(x in p.parts for x in ('.git','node_modules','dist','__pycache__')) and p.suffix not in ('.pyc','.tsbuildinfo') and p.name!=M.name
if '--write' in sys.argv:
 files=sorted(p for p in ROOT.rglob('*') if deliverable(p));M.write_text('\n'.join(f'{h(p)} *{p.relative_to(ROOT).as_posix()}' for p in files)+'\n',encoding='utf-8');print(f'HASH_MANIFEST_WRITE=PASS count={len(files)}');raise SystemExit
bad=[]
for line in M.read_text(encoding='utf-8').splitlines():
 expected,rel=line.split(' *',1);p=ROOT/rel
 if not p.exists() or h(p)!=expected:bad.append(rel)
print('HASH_VERIFY='+('PASS' if not bad else 'FAIL'))
for x in bad:print('MISMATCH='+x)
raise SystemExit(1 if bad else 0)

