from pathlib import Path
import sys, json, hashlib, zipfile
base = Path(__file__).resolve().parent
manifest = json.loads((base / 'SHA256-MANIFEST.json').read_text(encoding='utf-8'))
receipt = json.loads((base / 'SEAL-RECEIPT.json').read_text(encoding='utf-8'))
digest = lambda data: hashlib.sha256(data).hexdigest()
errors = []
for name, expected in receipt['sealed_artifacts'].items():
    p = base / name
    if not p.is_file() or digest(p.read_bytes()) != expected:
        errors.append('SEAL_ARTIFACT_MISMATCH:' + name)
try:
    with zipfile.ZipFile(base / 'HIPE-v0.3.5-FROZEN.zip') as z:
        expected_names = {'hipe-v0.3.5/' + item['path'] for item in manifest['files']}
        if set(z.namelist()) != expected_names or len(z.namelist()) != len(expected_names):
            errors.append('ZIP_FILE_SET_MISMATCH')
        for item in manifest['files']:
            if digest(z.read('hipe-v0.3.5/' + item['path'])) != item['sha256']:
                errors.append('ZIP_HASH_MISMATCH:' + item['path'])
except Exception as e:
    errors.append('ZIP_UNREADABLE:' + type(e).__name__)
if '--source' in sys.argv:
    root = Path(manifest['canonical_source'])
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    if actual != {item['path'] for item in manifest['files']}:
        errors.append('SOURCE_FILE_SET_MISMATCH')
    for item in manifest['files']:
        p = root / item['path']
        if not p.is_file() or digest(p.read_bytes()) != item['sha256']:
            errors.append('SOURCE_HASH_MISMATCH:' + item['path'])
print(json.dumps({'freeze_id': manifest['freeze_id'], 'result': 'FAIL' if errors else 'PASS',
                  'files': len(manifest['files']), 'source_checked': '--source' in sys.argv,
                  'errors': errors}, ensure_ascii=False, indent=2))
sys.exit(bool(errors))
