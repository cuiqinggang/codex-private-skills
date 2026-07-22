#!/usr/bin/env python3
import hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
manifest=ROOT/'FILE_MANIFEST_SHA256.txt'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
if '--write' in sys.argv:
    files=[p for p in ROOT.rglob('*') if p.is_file() and not any(x in p.parts for x in ('.git','node_modules','dist','__pycache__')) and p.suffix!='.tsbuildinfo' and p.name!='FILE_MANIFEST_SHA256.txt']
    manifest.write_text('\n'.join(f'{digest(p)} *{p.relative_to(ROOT).as_posix()}' for p in sorted(files))+'\n',encoding='utf-8')
    print(f'HASH_MANIFEST_WRITE=PASS count={len(files)}');sys.exit(0)
errors=[]
for line in manifest.read_text(encoding='utf-8').splitlines():
    expected,rel=line.split(' *',1);p=ROOT/rel
    if not p.exists() or digest(p)!=expected:errors.append(rel)
print('HASH_VERIFY='+('PASS' if not errors else 'FAIL'))
for e in errors:print('MISMATCH='+e)
sys.exit(1 if errors else 0)
