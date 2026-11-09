#!/usr/bin/env python3
"""Read-only contract matching for copied original flows; never execute a flow."""
from pathlib import Path, PureWindowsPath
import argparse
import csv
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import re
import sys
import time

PACKAGE = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = PACKAGE / 'references' / 'executable-flows.json'
GOALS = {'office.extract_body', 'files.archive_exact', 'orders.report_integer_cents'}
ORDER_FIELDS = ['row_id', 'order_id', 'customer', 'amount_cents', 'quantity']
ORDER_SEMANTICS = {'amount_unit': 'integer_cents', 'duplicates': 'preserve',
                   'customer_case': 'exact', 'identifiers': 'text',
                   'numeric_text': 'canonical_integer'}
REQUEST_FIELDS = {'goal', 'context', 'workspace', 'inputs', 'input_directory',
                  'output_directory', 'output_profile', 'requirements',
                  'allow_write', 'semantics', 'title'}
MIB = 1024 * 1024


class StopMatch(Exception):
    def __init__(self, status, code, detail):
        self.status, self.code, self.detail = status, code, detail


def reject(code, detail):
    raise StopMatch('NOT_MATCHED', code, detail)


def missing(code, detail):
    raise StopMatch('NEEDS_CONFIG', code, detail)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(MIB), b''):
            h.update(chunk)
    return h.hexdigest()


def redirected(path):
    return path.is_symlink() or bool(getattr(path, 'is_junction', lambda: False)())


def inside(root, value, *, exists=True):
    if not isinstance(value, str) or not value or '\x00' in value:
        reject('INVALID_RELATIVE_PATH', repr(value))
    raw = Path(value)
    win = PureWindowsPath(value)
    if raw.is_absolute() or win.is_absolute() or win.drive or '..' in value.replace('\\', '/').split('/'):
        reject('UNSAFE_PATH', value)
    current = root
    for part in raw.parts:
        current = current / part
        if redirected(current):
            reject('REDIRECTED_PATH', value)
    try:
        path = current.resolve(strict=exists)
    except (OSError, ValueError) as error:
        reject('INPUT_PATH_UNAVAILABLE', value + ': ' + str(error))
    if not path.is_relative_to(root):
        reject('OUTSIDE_WORKSPACE', value)
    return path


def fresh(root, names):
    for name in names:
        path = inside(root, name, exists=False)
        if path.exists():
            reject('OUTPUT_ALREADY_EXISTS', str(path))


def metadata_distribution(requirement):
    match = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9_.-]*)(?:==([^\s]+))?', requirement)
    if not match:
        missing('INVALID_DEPENDENCY_RECORD', requirement)
    name, version = match.groups()
    try:
        current = importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        missing('DEPENDENCY_NOT_INSTALLED', name)
    if version and current != version:
        missing('DEPENDENCY_VERSION_MISMATCH', f'{name}: expected {version}, observed {current}')


def source_checks(registry, required=None):
    records = registry.get('source_files')
    if not isinstance(records, list) or not records:
        missing('SOURCE_MANIFEST_MISSING', 'source_files')
    if required is not None:
        if not isinstance(required, list) or not required or not all(isinstance(x, str) for x in required):
            missing('ENTRY_SOURCE_CLOSURE_INVALID', required)
        wanted = set(required)
        records = [r for r in records if r.get('path') in wanted]
        if {r.get('path') for r in records} != wanted:
            missing('ENTRY_SOURCE_NOT_IN_MANIFEST', sorted(wanted))
    result = {}
    for record in records:
        try:
            path = inside(PACKAGE, record['path'], exists=False)
            expected = record['sha256']
        except StopMatch as error:
            missing('SOURCE_MANIFEST_PATH_INVALID', error.detail)
        except (KeyError, TypeError):
            missing('SOURCE_MANIFEST_INVALID', 'Each source needs package-relative path and sha256')
        if not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected):
            missing('SOURCE_HASH_INVALID', record.get('path'))
        if not path.is_file():
            missing('ORIGINAL_SOURCE_MISSING', record['path'])
        if sha(path) != expected:
            missing('ORIGINAL_SOURCE_CHANGED', record['path'])
        result[str(path)] = expected
    return result


def canonical_order_input(source, fields):
    with source.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream, strict=True)
        if reader.fieldnames != fields or fields != ORDER_FIELDS:
            reject('ORDER_COLUMNS_NOT_EXACT', {'expected': ORDER_FIELDS, 'observed': reader.fieldnames})
        for index, row in enumerate(reader, 2):
            if None in row or any(row.get(key) is None for key in fields):
                reject('MALFORMED_ORDER_ROW', index)
            if not re.fullmatch(r'0|-?[1-9][0-9]*', row['amount_cents']):
                reject('NONCANONICAL_INTEGER_CENTS', index)
            if not re.fullmatch(r'0|[1-9][0-9]*', row['quantity']):
                reject('NONCANONICAL_NONNEGATIVE_QUANTITY', index)


def original_order_validation(flow, source, verified):
    entry = flow.get('entry', {}).get('inside_omp_tool', {})
    programme = inside(PACKAGE, entry.get('programme', ''))
    if programme.name != 'business_pack.py' or str(programme) not in verified:
        missing('ORIGINAL_ORDER_VALIDATOR_MISSING', str(programme))
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('_original_order_contract', programme)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        module.load_rows(source)
    except ValueError as error:
        reject('ORIGINAL_ORDER_CONTRACT_REJECTED', str(error))


def match(request, registry):
    if not isinstance(request, dict):
        reject('REQUEST_NOT_OBJECT', 'JSON object required')
    unknown = sorted(set(request) - REQUEST_FIELDS)
    if unknown:
        reject('UNSUPPORTED_REQUEST_FIELDS', unknown)
    goal = request.get('goal')
    if goal not in GOALS:
        reject('UNSUPPORTED_GOAL', goal)
    for key in ['context', 'workspace', 'output_profile', 'requirements']:
        if key not in request:
            missing('REQUEST_FIELD_MISSING', key)
    context = request['context']
    if context not in ['host', 'inside_omp_tool']:
        reject('UNSUPPORTED_CONTEXT', context)
    if request.get('allow_write') is not True:
        reject('WRITE_NOT_AUTHORIZED', 'allow_write must explicitly be true')
    requirements = request['requirements']
    if not isinstance(request['output_profile'], str):
        reject('OUTPUT_PROFILE_NOT_STRING', request['output_profile'])
    if not isinstance(requirements, list) or not all(isinstance(x, str) for x in requirements):
        reject('REQUIREMENTS_NOT_STRING_LIST', requirements)
    candidates = [flow for flow in registry.get('flows', []) if flow.get('goal') == goal]
    if not candidates:
        reject('NO_REGISTERED_GOAL', goal)
    eligible = [f for f in candidates if f.get('output_profile') == request['output_profile']
                and set(requirements).issubset(f.get('capabilities', []))
                and context in f.get('contexts', [])]
    if not eligible:
        reject('OUTPUT_REQUIREMENTS_OR_CONTEXT_NOT_COVERED', {'output_profile': request['output_profile'], 'requirements': requirements, 'context': context})
    if len(eligible) != 1:
        missing('AMBIGUOUS_REGISTERED_FLOW', [f.get('id') for f in eligible])
    flow = eligible[0]
    count_limit = min(flow['max_files'], 40 if goal == 'office.extract_body' else 10000 if goal == 'files.archive_exact' else 1)
    file_limit = min(flow['max_file_bytes'], 16 * MIB if goal == 'orders.report_integer_cents' else 64 * MIB)
    total_limit = min(flow['max_total_bytes'], 16 * MIB if goal == 'orders.report_integer_cents' else 256 * MIB)
    raw_root = request['workspace']
    if not isinstance(raw_root, str) or not Path(raw_root).is_absolute():
        reject('WORKSPACE_NOT_ABSOLUTE', raw_root)
    root = Path(raw_root)
    if redirected(root):
        reject('REDIRECTED_WORKSPACE', raw_root)
    if not root.is_dir():
        missing('WORKSPACE_UNAVAILABLE', raw_root)
    root = root.resolve(strict=True)
    if goal != 'orders.report_integer_cents' and request.get('semantics'):
        reject('UNSUPPORTED_SEMANTICS', request['semantics'])
    if goal != 'orders.report_integer_cents' and any(key in request for key in ['output_directory', 'title']):
        reject('OUTPUT_OVERRIDE_NOT_COVERED', 'This original recipe has fixed output names and no title override')
    if goal == 'orders.report_integer_cents':
        if request.get('semantics') != ORDER_SEMANTICS:
            reject('ORDER_SEMANTICS_NOT_EXACT', {'required': ORDER_SEMANTICS, 'observed': request.get('semantics')})
        if request.get('title', '订单经营日报') != '订单经营日报':
            reject('CUSTOM_ORDER_TITLE_NOT_COVERED', request['title'])
    files = []
    directory = None
    if goal == 'files.archive_exact':
        if request.get('inputs'):
            reject('AMBIGUOUS_ARCHIVE_INPUT', 'Use only input_directory')
        if 'input_directory' not in request:
            missing('INPUT_DIRECTORY_MISSING', 'input_directory')
        directory = inside(root, request['input_directory'])
        if directory == root or not directory.is_dir():
            reject('ARCHIVE_INPUT_NOT_PROPER_SUBDIRECTORY', str(directory))
        for parent, dirs, names in os.walk(directory, followlinks=False):
            for name in dirs + names:
                path = Path(parent) / name
                if redirected(path) or not path.resolve(strict=True).is_relative_to(directory):
                    reject('REDIRECTED_ARCHIVE_MEMBER', str(path))
            files.extend(Path(parent) / n for n in names)
            if len(files) > count_limit:
                reject('FILE_COUNT_EXCEEDS_CONTRACT', len(files))
        files.sort()
        fresh(root, ['delivery.zip', 'manifest.json', 'delivery.json'])
    else:
        if request.get('input_directory'):
            reject('AMBIGUOUS_FILE_INPUT', 'Use only inputs')
        if 'inputs' not in request:
            missing('INPUT_FILES_MISSING', 'inputs')
        if not isinstance(request['inputs'], list):
            reject('INPUTS_NOT_LIST', 'inputs')
        files = [inside(root, value) for value in request['inputs']]
        if goal == 'office.extract_body':
            fresh(root, ['extracted.json', 'delivery.json'])
    if not files or len(files) > count_limit:
        reject('FILE_COUNT_OUTSIDE_CONTRACT', len(files))
    if len({os.path.normcase(str(p)) for p in files}) != len(files):
        reject('DUPLICATE_INPUT_PATHS', 'Each input path must be unique')
    enabled = {str(x).lower().lstrip('.') for x in flow.get('formats', [])}
    total = 0
    for path in files:
        if not path.is_file():
            reject('INPUT_NOT_REGULAR_FILE', str(path))
        if goal != 'files.archive_exact' and path.suffix.lower().lstrip('.') not in enabled:
            reject('FORMAT_NOT_COVERED', path.suffix)
        size = path.stat().st_size
        if size > file_limit:
            reject('FILE_TOO_LARGE', str(path))
        total += size
    if total > total_limit:
        reject('BATCH_TOO_LARGE', total)
    out = None
    if goal == 'orders.report_integer_cents':
        if len(files) != 1 or files[0].suffix.lower() != '.csv':
            reject('ORDER_INPUT_REQUIRES_ONE_CSV', len(files))
        out = inside(root, request.get('output_directory', 'output'), exists=False)
        if out == root or out in files or (out.exists() and (not out.is_dir() or any(out.iterdir()))):
            reject('ORDER_OUTPUT_NOT_FRESH_DIRECTORY', str(out))
        fresh(root, ['delivery.json', str(out.relative_to(root) / 'delivery.json')])
        canonical_order_input(files[0], flow.get('order_fields', ORDER_FIELDS))
    if flow.get('state') != 'READY':
        missing('FLOW_NOT_READY', flow.get('id'))
    if flow['entry'][context].get('state', flow['state']) != 'READY':
        missing('CONTEXT_NOT_READY', {'recipe_id': flow['id'], 'context': context})
    python = registry.get('python')
    if not isinstance(python, str) or os.path.normcase(str(Path(python).resolve())) != os.path.normcase(str(Path(sys.executable).resolve())):
        missing('FIXED_PYTHON_NOT_ACTIVE', {'required': python, 'active': sys.executable})
    if context == 'host':
        for key in ['node', 'sandbox_runner', 'sandbox_temp']:
            raw = registry.get(key)
            if not isinstance(raw, str) or not (Path(raw).is_dir() if key == 'sandbox_temp' else Path(raw).is_file()):
                missing('HOST_DEPENDENCY_UNAVAILABLE', key)
    entry = flow['entry'][context]
    for dependency in flow.get('dependencies', []) + entry.get('dependencies', []):
        metadata_distribution(dependency)
    verified = source_checks(registry, entry.get('source_files'))
    programme = inside(PACKAGE, entry['programme'])
    if str(programme) not in verified:
        missing('ENTRY_NOT_IN_FROZEN_MANIFEST', entry['programme'])
    if goal == 'orders.report_integer_cents':
        original_order_validation(flow, files[0], verified)
    base_args = entry.get('base_args', [])
    if not isinstance(base_args, list) or not all(isinstance(value, str) for value in base_args):
        missing('INVALID_ENTRY_ARGUMENTS', flow['id'])
    argv = [python, '-X', 'utf8', str(programme), *base_args]
    relatives = [str(p.relative_to(root)) for p in files]
    mode = entry['mode']
    if mode == 'legacy_office' and goal == 'office.extract_body':
        argv += ['--cwd', str(root)]
        for path in relatives:
            argv += ['--fast-office-file', path]
    elif mode == 'legacy_archive' and goal == 'files.archive_exact':
        argv += ['--cwd', str(root), '--fast-archive-input', str(directory.relative_to(root))]
    elif mode == 'legacy_orders' and goal == 'orders.report_integer_cents':
        argv += ['--cwd', str(root), '--fast-orders-input', relatives[0], '--fast-orders-out', str(out.relative_to(root))]
    elif mode == 'ingest' and goal == 'office.extract_body':
        argv += ['--cwd', str(root), '--files-json', json.dumps(relatives, ensure_ascii=True)]
    elif mode == 'archive' and goal == 'files.archive_exact':
        argv += ['--cwd', str(root), '--input', str(directory.relative_to(root))]
    elif mode == 'orders' and goal == 'orders.report_integer_cents':
        argv += ['--input', str(files[0]), '--out', str(out), '--title', '订单经营日报']
    else:
        missing('ENTRY_MODE_NOT_REGISTERED_FOR_GOAL', {'mode': mode, 'goal': goal})
    return {'status': 'MATCH', 'recipe_id': flow['id'], 'context': context,
            'argv': argv, 'cwd': str(root),
            'env': {'PYTHONUTF8': '1', 'PYTHONIOENCODING': 'utf-8'},
            'source_hashes': verified,
            'input_hashes': {str(p.relative_to(root)): sha(p) for p in files},
            'acceptance': {'original_checks': flow.get('acceptance', 'Use original recipe fixed checks and delivery readback.'),
                           'output_profile': flow['output_profile'], 'requirements': requirements},
            'performance_scope': flow.get('performance_scope'), 'missing': [], 'conflicts': []}


def main():
    started = time.perf_counter()
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='strict')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--request', type=Path, required=True)
    p.add_argument('--registry', type=Path, default=DEFAULT_REGISTRY)
    args = p.parse_args()
    result = {'status': 'NEEDS_CONFIG', 'missing': [], 'conflicts': []}
    try:
        try:
            request = json.loads(args.request.read_text(encoding='utf-8-sig'))
        except (OSError, ValueError) as error:
            missing('REQUEST_UNREADABLE', str(error))
        try:
            registry = json.loads(args.registry.read_text(encoding='utf-8-sig'))
        except (OSError, ValueError) as error:
            missing('REGISTRY_UNREADABLE', str(error))
        result = match(request, registry)
    except StopMatch as error:
        result['status'] = error.status
        key = 'conflicts' if error.status == 'NOT_MATCHED' else 'missing'
        result[key].append({'code': error.code, 'detail': error.detail})
    except (UnicodeError, csv.Error) as error:
        result.update(status='NOT_MATCHED', conflicts=[{'code': 'INPUT_ENCODING_OR_CSV_INVALID', 'detail': str(error)}])
    except Exception as error:
        result['missing'].append({'code': 'REGISTRY_OR_PREFLIGHT_ERROR', 'detail': type(error).__name__ + ': ' + str(error)})
    result['elapsed_s'] = time.perf_counter() - started
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
