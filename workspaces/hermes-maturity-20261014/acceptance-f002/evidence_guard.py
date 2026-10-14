"""Read-only acceptance evidence guard for HERMES-ECO-20261014, F002.

This does not run Hermes, repair code, create checkpoints, or certify a workstation.
Synthetic tests of this guard are NOT Hermes runtime acceptance evidence.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import statistics
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

TASK_ID = 'HERMES-ECO-20261014'
CONTRACT = 'F002'
REQUIRED = {
    1: {'immutable_inputs', 'independent_tests', 'actual_tool_calls',
        'real_independent_children', 'no_unexpected_tool_errors', 'vision_result',
        'repair_receipt', 'gate_review', 'research_source', 'handoff'},
    2: {'immutable_inputs', 'independent_tests', 'resume_tool_call', 'no_code_rework',
        'closed_after_resume', 'checkpoint_hash_chain', 'handoff_hash', 'resume_event'},
}


def _read(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding='utf-8-sig'))
    if not isinstance(obj, dict):
        raise ValueError(f'not an object: {path.name}')
    return obj


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _check_event_errors(path: Path, run_id: str, expected_test_path: Path, phase: int) -> bool:
    """Only one deliberate baseline-test failure is allowed, not all terminal errors."""
    pending = defaultdict(deque)
    terminal_index = 0
    errors = []
    saw_event = False
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        if not line.startswith('data: '):
            continue
        if line[6:].strip() == '[DONE]':
            continue
        event = json.loads(line[6:])
        if not isinstance(event, dict) or event.get('run_id') != run_id:
            return False
        saw_event = True
        kind, tool = event.get('event'), event.get('tool')
        if kind == 'tool.started':
            if tool == 'terminal':
                terminal_index += 1
            pending[tool].append((terminal_index, str(event.get('preview') or '')))
        elif kind == 'tool.completed':
            if not pending[tool] or type(event.get('error')) is not bool:
                return False
            index, preview = pending[tool].popleft()
            if event['error']:
                errors.append((tool, index, preview))
    if not saw_event or any(pending.values()):
        return False
    if phase == 2:
        return not errors
    if len(errors) != 1 or errors[0][0] != 'terminal':
        return False
    normalize = lambda text: text.replace('\\\\', '\\').replace('\\', '/').lower()
    return normalize(str(expected_test_path)) in normalize(errors[0][2])


def inspect_round(root: Path, number: int, config_sha: str, fixture_sha: str) -> dict[str, Any]:
    """A missing/partial/malformed receipt is UNKNOWN, never an invitation to rerun."""
    directory = root / f'R{number:02d}'
    errors: list[str] = []
    elapsed = None
    sessions: list[str] = []
    run_ids: list[str] = []
    try:
        receipt = _read(directory / 'round-result.json')
        if receipt.get('round') != number or receipt.get('pass') is not True:
            errors.append('ROUND_NOT_PASSED')
        if receipt.get('contract_ref') != CONTRACT:
            errors.append('CONTRACT_MISMATCH')
        if receipt.get('config_sha256') != config_sha or receipt.get('fixture_sha256') != fixture_sha:
            errors.append('SNAPSHOT_MISMATCH')
        elapsed = receipt.get('full_wall_ms')
        if isinstance(elapsed, bool) or not isinstance(elapsed, (float, int)) or not math.isfinite(elapsed) or elapsed <= 0:
            errors.append('INVALID_WALL_CLOCK')
            elapsed = None
        if receipt.get('error') or receipt.get('error_type'):
            errors.append('ROUND_ERROR_PRESENT')
        for phase in (1, 2):
            grade = _read(directory / f'grade-{phase}.json')
            checks = grade.get('checks')
            if not isinstance(checks, dict) or not REQUIRED[phase].issubset(checks):
                errors.append(f'P{phase}_MISSING_CHECKS')
            elif not all(value is True for value in checks.values()):
                errors.append(f'P{phase}_FAILED_CHECK')
            if grade.get('phase') != phase or grade.get('pass') is not True:
                errors.append(f'P{phase}_GRADE_FAILED')
            ack = _read(directory / f'ack-{phase}.json')
            run = _read(directory / f'run-{phase}.json')
            replay = _read(directory / f'idempotency-{phase}.json')
            rid = ack.get('run_id')
            if not isinstance(rid, str) or not rid.startswith('run_'):
                errors.append(f'P{phase}_MISSING_RUN_ID')
            elif run.get('run_id') != rid or replay.get('run_id') != rid:
                errors.append(f'P{phase}_RUN_ID_MISMATCH')
            else:
                run_ids.append(rid)
            if not _check_event_errors(directory / f'events-{phase}.sse', rid, directory / 'run-tests.cmd', phase):
                errors.append(f'P{phase}_UNEXPECTED_OR_UNVERIFIED_TOOL_ERROR')
            if run.get('status') != 'completed':
                errors.append(f'P{phase}_RUN_NOT_COMPLETED')
            if replay.get('replayed') is not True or replay.get('same_run_id') is not True:
                errors.append(f'P{phase}_IDEMPOTENCY_NOT_VERIFIED')
            sid = run.get('session_id')
            if not isinstance(sid, str) or not sid:
                errors.append(f'P{phase}_SESSION_NOT_OBSERVED')
            else:
                sessions.append(sid)
            # Different request aliases must not conceal an actual model/provider change.
            runtime = run.get('runtime') or {}
            if not isinstance(runtime, dict) or runtime.get('provider') != 'openrouter' or runtime.get('model') != 'deepseek/deepseek-v4.1-flash':
                errors.append(f'P{phase}_ACTUAL_RUNTIME_UNVERIFIED')
        if len(sessions) == 2 and sessions[0] == sessions[1]:
            errors.append('RESUME_DID_NOT_USE_NEW_SESSION')
        if len(run_ids) == 2 and run_ids[0] == run_ids[1]:
            errors.append('PHASES_REUSE_SAME_RUN')
        if errors:
            return {'round': number, 'status': 'NOT_ACCEPTED', 'errors': errors, 'full_wall_ms': elapsed}
        return {'round': number, 'status': 'PASS', 'errors': [], 'full_wall_ms': elapsed, 'run_ids': run_ids}
    except (OSError, ValueError, TypeError, AttributeError) as error:
        return {'round': number, 'status': 'UNKNOWN_RECONCILE_FIRST',
                'errors': [type(error).__name__], 'full_wall_ms': elapsed}


def inspect_batch(root: Path, through: int = 5) -> dict[str, Any]:
    if isinstance(through, bool) or not isinstance(through, int) or not 1 <= through <= 5:
        raise ValueError('through must be 1..5')
    result: dict[str, Any] = {
        'task_id': TASK_ID, 'contract_ref': CONTRACT, 'evidence_level': 'RECEIPT_AUDIT_ONLY',
        'required_rounds': 5, 'reviewed_rounds': through, 'consecutive_pass': 0,
        'five_round_contract_pass': False, 'whole_station_final_valid': False,
        'reboot_verified': False, 'full_browser_chat_e2e_verified': False,
        'long_duration_verified': False, 'physical_optimum_verified': False,
        'automatic_retry_permitted': False, 'rounds': [],
    }
    try:
        freeze = _read(root / 'REALITY-F002.json')
        if freeze.get('task_id') != TASK_ID or freeze.get('contract_ref') != CONTRACT:
            raise ValueError('wrong freeze')
        config_sha, fixture_sha = freeze['config_sha256'], freeze['fixtures_sha256']
        for digest in (config_sha, fixture_sha):
            if not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
                raise ValueError('invalid digest')
        if _sha(root / 'FIXTURE-MANIFEST.json') != fixture_sha:
            raise ValueError('fixture manifest changed')
        result['rounds'] = [inspect_round(root, n, config_sha, fixture_sha) for n in range(1, through + 1)]
        all_run_ids: set[str] = set()
        for row in result['rounds']:
            ids = set(row.get('run_ids', []))
            if ids & all_run_ids:
                row.update(status='NOT_ACCEPTED', errors=row['errors'] + ['CROSS_ROUND_RUN_ID_REUSED'])
            all_run_ids |= ids
            result['consecutive_pass'] = result['consecutive_pass'] + 1 if row['status'] == 'PASS' else 0
        result['five_round_contract_pass'] = through == 5 and result['consecutive_pass'] == 5
        good_times = [r['full_wall_ms'] for r in result['rounds'] if r['status'] == 'PASS']
        result['valid_sample_count'] = len(good_times)
        result['failed_or_unknown_count'] = len(result['rounds']) - len(good_times)
        if good_times:
            result['observed_time_ms'] = {'min': min(good_times), 'median': statistics.median(good_times), 'max': max(good_times)}
        result['status'] = 'FIVE_ROUND_CONTRACT_PASS' if result['five_round_contract_pass'] else 'NOT_ACCEPTED'
    except (OSError, ValueError, KeyError, TypeError) as error:
        result.update(status='UNKNOWN_RECONCILE_FIRST', errors=[type(error).__name__])
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--through', type=int, default=5)
    parser.add_argument('--require-current-pass', action='store_true')
    args = parser.parse_args()
    report = inspect_batch(args.root, args.through)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    current_pass = bool(report['rounds']) and report['rounds'][-1]['status'] == 'PASS'
    raise SystemExit(0 if (current_pass if args.require_current_pass else report['five_round_contract_pass']) else 2)
