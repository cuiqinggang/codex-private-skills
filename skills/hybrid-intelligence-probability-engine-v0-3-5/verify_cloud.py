from pathlib import Path
import json, hashlib, zipfile, sys
root = Path(__file__).resolve().parent
seal = root / 'freeze'
digest = lambda data: hashlib.sha256(data).hexdigest()
aliases = {'定位与冻结记录.md': 'location-and-freeze.md', '长期定位条目.md': 'durable-location-note.md'}
receipt_bytes = (seal / 'SEAL-RECEIPT.json').read_bytes()
receipt_hash = (seal / 'SEAL-RECEIPT.sha256').read_text(encoding='utf-8').split()[0]
assert digest(receipt_bytes) == receipt_hash, 'SEAL_RECEIPT_MISMATCH'
receipt = json.loads(receipt_bytes)
for name, expected in receipt['sealed_artifacts'].items():
    assert digest((seal / aliases.get(name, name)).read_bytes()) == expected, name
manifest = json.loads((seal / 'SHA256-MANIFEST.json').read_bytes())
with zipfile.ZipFile(seal / 'HIPE-v0.3.5-FROZEN.zip') as z:
    expected_names = {'hipe-v0.3.5/' + x['path'] for x in manifest['files']}
    assert set(z.namelist()) == expected_names and len(z.namelist()) == len(expected_names), 'ZIP_FILE_SET_MISMATCH'
    for x in manifest['files']:
        assert digest(z.read('hipe-v0.3.5/' + x['path'])) == x['sha256'], 'ZIP:' + x['path']
        assert digest((root / x['path']).read_bytes()) == x['sha256'], 'SOURCE:' + x['path']
print(json.dumps({'result': 'PASS', 'freeze_id': manifest['freeze_id'], 'original_files': len(manifest['files']),
                  'archive_bytes_match': True, 'sealed_artifacts_match': True}, ensure_ascii=False, indent=2))
