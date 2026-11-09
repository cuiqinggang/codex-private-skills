"""Record a completed batch and index reusable original interfaces; never execute them."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

PACKAGE = Path(__file__).resolve().parent.parent
DEFAULT_LIBRARY = Path('C:/Users/A/Documents/DSH-Workspace/automation-flow-library') if os.name == 'nt' else PACKAGE / 'local-library'


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def object_value(value, label):
    if not isinstance(value, dict):
        raise ValueError(label + ' must be an object')
    return value


def text_value(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + ' must be nonempty text')
    return value


def scoped_file(workspace, name):
    relative = Path(text_value(name, 'source/evidence path'))
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('source/evidence must use workspace-relative paths')
    path = workspace / relative
    for part in [path, *path.parents]:
        if part == workspace:
            break
        if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
            raise ValueError('source/evidence links are not accepted')
    path = path.resolve(strict=True)
    if not path.is_relative_to(workspace) or not path.is_file():
        raise ValueError('source/evidence is outside workspace or not a file')
    if path.stat().st_size > 16 * 1024 * 1024:
        raise ValueError('capture metadata/source limit is 16 MiB per file; use original repository reference for larger files')
    return path


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(dir=path.parent, prefix='.capture-', suffix='.json')
    try:
        with os.fdopen(handle, 'wb') as stream:
            stream.write(encoded(value))
        os.replace(name, path)
    finally:
        if Path(name).exists():
            Path(name).unlink()


def capture(record, library, registry):
    record = deepcopy(object_value(record, 'record'))
    task = text_value(record.get('task_id'), 'task_id')
    batch = text_value(record.get('batch_id'), 'batch_id')
    decision = record.get('decision')
    if decision not in {'REUSED', 'NEW_CANDIDATE', 'NO_REUSABLE_FLOW'}:
        raise ValueError('decision must be REUSED, NEW_CANDIDATE or NO_REUSABLE_FLOW')
    if record.get('contains_secrets') is not False:
        raise ValueError('capture only reviewed metadata/code: contains_secrets must be false')
    workspace = Path(text_value(record.get('workspace'), 'workspace')).resolve(strict=True)
    if not workspace.is_dir():
        raise ValueError('workspace must be a directory')
    qa = object_value(record.get('qa'), 'qa')
    if not isinstance(qa.get('passed'), bool):
        raise ValueError('qa.passed must be a boolean; failed evidence is retained')
    timing = object_value(record.get('timing'), 'timing')
    text_value(timing.get('scope'), 'timing.scope')
    for key in ('total_s', 'user_e2e_s'):
        value = timing.get(key)
        if value is not None and (type(value) not in (int, float) or not 0 <= value < float('inf')):
            raise ValueError('timing.' + key + ' must be finite nonnegative seconds or null for NOT_MEASURED')
    original = object_value(record.get('original', {}), 'original')
    sources = original.get('files', [])
    evidence = qa.get('evidence_files', [])
    if not isinstance(sources, list) or not isinstance(evidence, list):
        raise ValueError('original.files and qa.evidence_files must be arrays')
    copied = {}
    for item in [*sources, *evidence]:
        object_value(item, 'file reference')
        path = scoped_file(workspace, item.get('path'))
        data = path.read_bytes()
        actual = digest(data)
        if item.get('sha256') is not None and item['sha256'] != actual:
            raise ValueError('source/evidence fingerprint changed: ' + item['path'])
        item['sha256'] = actual
        if item.get('copy') is True:
            copied[actual] = data
            item['stored_copy'] = 'sources/' + actual + '/' + path.name
    rows = json.loads(registry.read_text(encoding='utf-8'))['recipes']
    known = {row['id']: row for row in rows}
    captured_path = library / 'recipes.json'
    if captured_path.exists() and captured_path.resolve() != registry.resolve():
        for row in json.loads(captured_path.read_text(encoding='utf-8'))['recipes']:
            if row['id'] in known:
                raise ValueError('captured index must not replace a packaged recipe')
            known[row['id']] = row
    if decision == 'REUSED':
        recipe_id = text_value(record.get('recipe_id'), 'recipe_id')
        if recipe_id not in known:
            raise ValueError('REUSED requires an existing registered recipe id')
    elif decision == 'NEW_CANDIDATE':
        contract = object_value(record.get('contract'), 'contract')
        for key in ('goal', 'inputs', 'semantics', 'outputs', 'acceptance'):
            if key not in contract or contract[key] in (None, '', [], {}):
                raise ValueError('candidate contract requires ' + key)
        identity = text_value(original.get('identity'), 'original.identity')
        object_value(original.get('entry'), 'original.entry')
        for key in ('title', 'category'):
            text_value(record.get(key), key)
        terms = record.get('search_terms')
        if not isinstance(terms, list) or not terms or not all(isinstance(t, str) and t.strip() for t in terms):
            raise ValueError('candidate requires search_terms')
        fingerprint = digest(encoded({'contract': contract, 'original_identity': identity}))
        recipe_id = 'captured-' + fingerprint[:24]
        record['recipe_id'] = recipe_id
    else:
        recipe_id = None
        text_value(record.get('reason'), 'reason')
    record_id = digest(encoded([task, batch]))
    library.mkdir(parents=True, exist_ok=True)
    lock = library / '.capture.lock'
    try:
        lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise ValueError('library capture busy; reconcile current writer before retry') from None
    try:
        os.close(lock_fd)
        destination = library / 'records' / (record_id + '.json')
        if destination.exists():
            if destination.read_bytes() != encoded(record):
                raise ValueError('task/batch already recorded differently; preserve it and use a new recovery batch id')
            return {'status': 'NO_CHANGE', 'recipe_id': recipe_id, 'record': str(destination)}
        catalog_path = library / 'recipes.json'
        catalog = json.loads(catalog_path.read_text(encoding='utf-8')) if catalog_path.exists() else {'schema': 'captured-flow-index-v1', 'recipes': [], 'uses': {}}
        if decision == 'NEW_CANDIDATE':
            row = {'id': recipe_id, 'title': record['title'], 'category': record['category'],
                   'platform': 'Captured original interface', 'source_url': original.get('source_url'),
                   'search_terms': record['search_terms'], 'routing_class': 'captured_candidate',
                   'verification': {'deployment': {'state': 'CANDIDATE'}, 'qa_recorded': qa['passed'],
                                    'note': 'Capture is not execution readiness; integrate and independently accept each context.'},
                   'reference': str(destination), 'invocation': original['entry'],
                   'contract': record['contract'], 'environment': record.get('environment'),
                   'missing': record.get('missing', []), 'original': original}
            catalog['recipes'] = [item for item in catalog['recipes'] if item['id'] != recipe_id] + [row]
        if recipe_id:
            uses = catalog['uses'].setdefault(recipe_id, [])
            if str(destination) not in uses:
                uses.append(str(destination))
        for item in [*sources, *evidence]:
            if item.get('copy') is True:
                target = library / item['stored_copy']
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(copied[item['sha256']])
        atomic_json(catalog_path, catalog)
        atomic_json(destination, record)
        return {'status': decision, 'recipe_id': recipe_id, 'record': str(destination),
                'catalog': str(catalog_path), 'executable_added': False}
    finally:
        lock.unlink()


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='strict')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', type=Path, required=True)
    parser.add_argument('--library', type=Path, default=DEFAULT_LIBRARY)
    parser.add_argument('--registry', type=Path, default=PACKAGE / 'references/recipes.json')
    args = parser.parse_args()
    try:
        result = capture(json.loads(args.record.read_text(encoding='utf-8')), args.library.resolve(), args.registry)
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({'status': 'CAPTURE_ERROR', 'error': str(error), 'executable_added': False}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
