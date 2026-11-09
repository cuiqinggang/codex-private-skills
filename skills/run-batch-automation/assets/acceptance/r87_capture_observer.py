"""Observe metadata capture/lookup on temporary fixtures; never run business commands."""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time


def observe(package):
    started = time.perf_counter()
    checks = {}
    spec = importlib.util.spec_from_file_location('capture', package / 'scripts/capture_flow.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    registry = package / 'references/recipes.json'
    with tempfile.TemporaryDirectory(prefix='r87-capture-') as folder:
        root = Path(folder)
        workspace = root / 'task'; workspace.mkdir()
        library = root / 'library'
        source_bytes = b'# observation fixture, not a certified business programme\r\n'
        (workspace / 'original.py').write_bytes(source_bytes)
        (workspace / 'QA.json').write_text('{"fixture_check":true}', encoding='utf-8')
        record = {'task_id': 'metadata-observation', 'batch_id': '1', 'decision': 'NEW_CANDIDATE',
                  'workspace': str(workspace), 'contains_secrets': False,
                  'title': '校验样例快捷入口', 'category': '文件与备份', 'search_terms': ['校验样例'],
                  'contract': {'goal': 'fixture.only', 'inputs': 'fixture', 'semantics': 'unchanged bytes',
                               'outputs': 'fixture', 'acceptance': 'metadata observation only'},
                  'original': {'identity': 'fixture-v1', 'entry': {'argv_template': ['NEVER_EXECUTE_FIXTURE']},
                               'files': [{'path': 'original.py', 'copy': True}]},
                  'environment': {'context': 'host'},
                  'qa': {'passed': True, 'evidence_files': [{'path': 'QA.json'}]},
                  'timing': {'scope': 'metadata fixture', 'total_s': None, 'user_e2e_s': None}}
        first = module.capture(record, library, registry)
        catalog = lambda: json.loads((library / 'recipes.json').read_text(encoding='utf-8'))
        row = catalog()['recipes'][0]
        stored = library / row['original']['files'][0]['stored_copy']
        checks['candidate_indexed_and_original_bytes_preserved'] = (
            first['status'] == 'NEW_CANDIDATE' and row['verification']['deployment']['state'] == 'CANDIDATE'
            and stored.read_bytes() == source_bytes and first['executable_added'] is False)
        again = module.capture(record, library, registry)
        checks['same_batch_exactly_once'] = again['status'] == 'NO_CHANGE' and len(list((library / 'records').glob('*.json'))) == 1
        second = deepcopy(record); second['batch_id'] = '2'; second['qa']['passed'] = False
        failed = module.capture(second, library, registry)
        checks['same_contract_deduplicated_and_failed_batch_retained'] = (
            failed['recipe_id'] == first['recipe_id'] and len(catalog()['recipes']) == 1
            and len(catalog()['uses'][first['recipe_id']]) == 2
            and json.loads(Path(failed['record']).read_text(encoding='utf-8'))['qa']['passed'] is False)
        def rejects(value, test_library=library):
            try:
                module.capture(value, test_library, registry)
                return False
            except (ValueError, OSError):
                return True
        conflict = deepcopy(record); conflict['timing']['total_s'] = 1
        checks['same_batch_conflict_preserves_old_record'] = rejects(conflict) and json.loads(Path(first['record']).read_text(encoding='utf-8'))['timing']['total_s'] is None
        mismatch = deepcopy(record); mismatch['batch_id'] = 'bad-hash'; mismatch['original']['files'][0]['sha256'] = '0' * 64
        escape = deepcopy(record); escape['batch_id'] = 'escape'; escape['original']['files'][0]['path'] = '../outside.py'
        checks['changed_source_and_outside_paths_rejected'] = rejects(mismatch) and rejects(escape)
        lock = library / '.capture.lock'; lock.write_text('other writer', encoding='utf-8')
        busy = deepcopy(record); busy['batch_id'] = 'busy'
        checks['active_writer_lock_respected'] = rejects(busy) and lock.read_text(encoding='utf-8') == 'other writer'
        lock.unlink()
        empty = deepcopy(record); empty.update(batch_id='no-reuse', decision='NO_REUSABLE_FLOW', reason='No reusable fixture steps')
        checks['no_reusable_check_recorded_without_new_flow'] = module.capture(empty, library, registry)['status'] == 'NO_REUSABLE_FLOW' and len(catalog()['recipes']) == 1
        reused = deepcopy(record); reused.update(batch_id='reuse', decision='REUSED', recipe_id='files-exact-archive')
        checks['existing_recipe_gets_usage_without_duplicate'] = module.capture(reused, library, registry)['status'] == 'REUSED' and len(catalog()['recipes']) == 1 and len(catalog()['uses']['files-exact-archive']) == 1
        reused_candidate = deepcopy(record)
        reused_candidate.update(batch_id='reuse-candidate', decision='REUSED', recipe_id=first['recipe_id'])
        checks['previously_captured_entry_can_be_reused_without_extra_registry_argument'] = module.capture(reused_candidate, library, registry)['status'] == 'REUSED' and len(catalog()['recipes']) == 1
        def query(*args):
            run = subprocess.run([sys.executable, '-X', 'utf8', str(package / 'scripts/query.py'),
                                  '--learned', str(library / 'recipes.json'), *args],
                                 capture_output=True, text=True, encoding='utf-8')
            return run.returncode, json.loads(run.stdout)
        rc, found = query('校验样例', '--kind', 'local')
        _, ready = query('校验样例', '--ready')
        checks['next_lookup_finds_candidate_but_ready_filter_excludes_it'] = rc == 0 and found['results'][0]['id'] == first['recipe_id'] and not ready['results']
        _, sources = query('--kind', 'source', '--category', 'API与集成')
        checks['source_catalogs_findable_by_business_category'] = len(sources['results']) > 0
        _, media = query('批次链接', '--kind', 'local')
        checks['new_native_operation_findable_but_not_ready'] = any(x['id'] == 'native-yt-dlp-batch-download' and x['deployment']['state'] == 'NOT_CONFIGURED' for x in media['results'])
        for item in json.loads((package / 'references/executable-flows.json').read_text(encoding='utf-8'))['source_files']:
            assert hashlib.sha256((package / item['path']).read_bytes()).hexdigest() == item['sha256']
        checks['all_seven_R86_frozen_programme_fingerprints_unchanged'] = True
    return {'passed': all(checks.values()), 'checks': checks, 'elapsed_s': time.perf_counter() - started,
            'scope': 'Metadata capture, idempotence, original-byte copy, lookup and frozen source integrity only; no new business/model/GUI tests.',
            'business_commands_executed': 0, 'model_calls': 0}


if __name__ == '__main__':
    package = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
    result = observe(package)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['passed'] else 1)
