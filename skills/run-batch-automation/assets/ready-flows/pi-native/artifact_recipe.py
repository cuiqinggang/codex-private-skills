"""Bounded adapters over stdlib ZIP and the previously accepted installed document reader."""
import argparse
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys
import time
import zipfile

HOME = pathlib.Path(__file__).resolve().parent
MAX_FILE = 64 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inside(root, raw, exists=True):
    path = (root / raw).resolve(strict=exists)
    if not path.is_relative_to(root):
        raise ValueError('Path is outside the current authorized workspace')
    return path

def fresh(root, names):
    if any((root / name).exists() for name in names):
        raise ValueError('Prior output exists; reconcile it instead of repeating')

def save(path, value):
    with path.open('x', encoding='utf-8') as output:
        json.dump(value, output, ensure_ascii=False, indent=2)

def archive(root, raw):
    names = ['delivery.zip', 'manifest.json', 'delivery.json']
    fresh(root, names)
    source = inside(root, raw)
    if source == root or not source.is_dir():
        raise ValueError('Archive input must be a proper subdirectory')
    files = sorted(path for path in source.rglob('*') if path.is_file())
    if not 1 <= len(files) <= 10000:
        raise ValueError('Archive requires 1..10000 files')
    total = 0
    expected = {}
    for path in files:
        if path.is_symlink() or not path.resolve(strict=True).is_relative_to(source):
            raise ValueError('Symlink or redirected input is not enabled')
        size = path.stat().st_size
        total += size
        if size > MAX_FILE or total > MAX_TOTAL:
            raise ValueError('Input exceeds the bounded resource contract')
        expected[path.relative_to(source).as_posix()] = sha(path)
    with zipfile.ZipFile(root / 'delivery.zip', 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as output:
        for name, digest in expected.items():
            data = (source / name).read_bytes()
            if hashlib.sha256(data).hexdigest() != digest:
                raise ValueError('Input changed while archiving')
            output.writestr(name, data)
    current = {path.relative_to(source).as_posix(): sha(path) for path in source.rglob('*') if path.is_file()}
    with zipfile.ZipFile(root / 'delivery.zip') as output:
        actual = {name: hashlib.sha256(output.read(name)).hexdigest() for name in output.namelist()}
        checks = {
            'all_original_paths_and_bytes': actual == expected,
            'no_duplicate_members': len(output.namelist()) == len(expected),
            'crc': output.testzip() is None,
            'input_unchanged': current == expected,
        }
    if not all(checks.values()):
        raise ValueError('Independent archive readback failed')
    save(root / 'manifest.json', expected)
    return names, checks, {'file_count': len(files), 'input_bytes': total, 'scope': 'Exact relative paths, original file bytes, ZIP CRC and unchanged input; bounded local files only'}

def ingest(root, raw_files):
    names = ['extracted.json', 'delivery.json']
    fresh(root, names)
    if not 1 <= len(raw_files) <= 40:
        raise ValueError('Batch requires 1..40 explicit local files')
    files = [inside(root, raw) for raw in raw_files]
    if len(set(files)) != len(files):
        raise ValueError('Repeated input paths are ambiguous')
    enabled = {'.docx', '.xlsx', '.pptx', '.pdf', '.txt', '.md', '.html', '.csv'}
    if any(not path.is_file() or path.suffix.lower() not in enabled or path.stat().st_size > MAX_FILE for path in files):
        raise ValueError('Input format or size is outside the enabled contract')
    if sum(path.stat().st_size for path in files) > MAX_TOTAL:
        raise ValueError('Batch exceeds bounded input bytes')
    before = {str(path.relative_to(root)): sha(path) for path in files}
    result = subprocess.run([sys.executable, str(HOME / 'mixed_reader.py'), '--root', str(root), *map(str, files)],
                            cwd=root, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)
    if result.returncode:
        raise RuntimeError('Existing installed reader failed: ' + result.stderr.decode('utf-8', 'replace')[-1500:])
    data = json.loads(result.stdout)
    data = [data] if isinstance(data, dict) else data
    checks = {
        'one_result_per_input': len(data) == len(files),
        'source_order_exact': [pathlib.Path(row['source']).resolve() for row in data] == files,
        'text_and_route_recorded': all(isinstance(row.get('markdown'), str) and isinstance(row.get('route'), str) for row in data),
        'input_unchanged': all(sha(path) == before[str(path.relative_to(root))] for path in files),
    }
    if not all(checks.values()):
        raise ValueError('Extraction structure/input integrity failed')
    save(root / 'extracted.json', data)
    reread = json.loads((root / 'extracted.json').read_text(encoding='utf-8'))
    if reread != data:
        raise ValueError('Extracted file readback failed')
    return names, checks, {'input_sha256': before, 'file_count': len(files), 'scope': 'Installed text extraction with source provenance and complete file serialization; not OCR, layout fidelity or semantic correctness certification'}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('kind', choices=['archive', 'ingest'])
    parser.add_argument('--cwd', required=True)
    parser.add_argument('--input')
    parser.add_argument('--files-json')
    args = parser.parse_args()
    root = pathlib.Path(args.cwd).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('cwd must be a directory')
    start = time.perf_counter()
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if args.kind == 'archive':
        if not args.input or args.files_json:
            raise ValueError('Archive requires only an explicit input directory')
        names, checks, details = archive(root, args.input)
    else:
        if not args.files_json or args.input:
            raise ValueError('Ingest requires only an explicit files array')
        files = json.loads(args.files_json)
        if not isinstance(files, list) or any(not isinstance(item, str) for item in files):
            raise ValueError('Files must be strings')
        names, checks, details = ingest(root, files)
    receipt = {'status': 'CONTENT_ACCEPTED', 'recipe': args.kind, 'started_utc': started,
               'files': names, 'sha256': {name: sha(root / name) for name in names if name != 'delivery.json'},
               'qa': {'pass': True, 'checks': checks}, 'model_calls': 0, **details}
    save(root / 'delivery.json', receipt)
    if json.loads((root / 'delivery.json').read_text(encoding='utf-8')) != receipt:
        raise ValueError('Delivery receipt readback failed')
    receipt['local_accepted_seconds'] = round(time.perf_counter() - start, 3)
    print(json.dumps(receipt, ensure_ascii=True), flush=True)

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('NOT_VALID ' + type(exc).__name__ + ': ' + str(exc), file=sys.stderr)
        sys.exit(1)
