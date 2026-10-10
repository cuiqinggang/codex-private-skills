"""Semantic equivalent of the synthetic create/save/copy demonstration."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    target = args.out.expanduser().resolve()
    if target.drive.upper() != 'C:':
        parser.error('Only an explicitly authorized new C-drive directory is supported')
    if target.exists():
        parser.error('Output already exists; refusing to overwrite')
    target.mkdir(parents=True, exist_ok=False)
    original = target / 'notes/演示.txt'
    copy = target / 'archive/演示副本.txt'
    original.parent.mkdir()
    copy.parent.mkdir()
    data = '安全操作演示\n仅测试文件。\n'.encode('utf-8')
    with original.open('xb') as stream:
        stream.write(data)
    shutil.copyfile(original, copy)
    assert original.read_bytes() == data == copy.read_bytes()
    manifest = {'status': 'PASS', 'mode': 'semantic-equivalent', 'files': [
        {'path': p.relative_to(target).as_posix(), 'bytes': p.stat().st_size,
         'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in (original, copy)]}
    with (target / 'manifest.json').open('x', encoding='utf-8') as stream:
        json.dump(manifest, stream, ensure_ascii=False, indent=2)
    print(json.dumps(manifest, ensure_ascii=True))


if __name__ == '__main__':
    main()