"""Thin subprocess failover entry over frozen order_runtime + filelock + continuity.
No daemon, peer repair, new scheduler, or model on the healthy primary path.
"""
import argparse
import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid
from filelock import FileLock


def load_runtime(config):
    config = Path(config).resolve()
    if config.name != 'config.json' or not config.is_file():
        raise RuntimeError('EXACT_EXISTING_CONFIG_JSON_REQUIRED')
    sys.path.insert(0, str(config.parent))
    spec = importlib.util.spec_from_file_location('delivery_runtime', config.parent / 'order_runtime.py')
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    if Path(r.CFG['workspace']).resolve() != config.parent.parent:
        raise RuntimeError('CONFIG_WORKSPACE_MISMATCH')
    for path, expected in r.CFG['dependency_sha256'].items():
        if r.digest(path) != expected:
            raise RuntimeError('FROZEN_DEPENDENCY_CHANGED')
    return r


def worker(a, r):
    scope, task, job = r.job_ref({'scope': a.scope, 'task_id': a.task_id}, False)
    with FileLock(str(job / 'request.lock'), timeout=0):
        meta = json.loads((job / 'accepted.json').read_text(encoding='utf-8'))
        if r.committed(job):
            return
        if a.role == 'primary' and a.fault == 'primary_timeout':
            time.sleep(20)
        if a.role == 'primary' and a.fault == 'checkpoint_counter_gap':
            original_checkpoint = r.continuity.save_checkpoint
            def crash_after_checkpoint(*args, **kwargs):
                value = original_checkpoint(*args, **kwargs)
                if args[2] == 1:
                    os._exit(86)
                return value
            r.continuity.save_checkpoint = crash_after_checkpoint
        if a.role == 'primary':
            if a.fault in ('primary_exit', 'force_native_backup'):
                os._exit(86)
            r.generate(scope, task, job)
        else:
            r.backup(scope, task, job, meta)
        if a.role == 'primary' and a.fault == 'after_generation':
            os._exit(86)
        # The confirmed checkpoint plus hashed generation record is authoritative.
        # Recover the old recipe's crash window before its bookkeeping count was saved.
        r.checked_generated(scope, task, job)
        meta = json.loads((job / 'accepted.json').read_text(encoding='utf-8'))
        if meta['generation_count'] == 0:
            r.write_json(job / 'counter-reconciled.json', {'prior': 0, 'corrected': 1, 'reason': 'confirmed generation checkpoint and artifact hashes'})
            meta['generation_count'] = 1
            r.write_json(job / 'accepted.json', meta)
        r.verify(scope, task, job, meta)
        if a.role == 'primary' and a.fault == 'after_qa':
            os._exit(86)
        d = r.commit(scope, task, job, meta)
        if a.role == 'primary' and a.fault == 'after_commit':
            os._exit(86)
        if d['status'] != 'CONFIRMED_COMMITTED':
            raise RuntimeError('NOT_COMMITTED')


def run_worker(a, r, job, role):
    args = [sys.executable, str(Path(__file__).resolve()), '--config', str(Path(a.config).resolve()),
            '--task-id', a.task_id, '--scope', a.scope, '--role', role, '--fault', a.fault]
    started = time.perf_counter()
    with (job / (role + '-worker.stdout.log')).open('w', encoding='utf-8') as out, (job / (role + '-worker.stderr.log')).open('w', encoding='utf-8') as err:
        env = dict(os.environ, PYTHONIOENCODING='utf-8')
        for key in ('OPENAI_API_KEY', 'CODEX_API_KEY', 'ANTHROPIC_API_KEY'):
            env.pop(key, None)
        proc = subprocess.Popen(args, stdout=out, stderr=err, stdin=subprocess.DEVNULL, env=env)
        timed_out = False
        termination_exit_code = None
        try:
            code = proc.wait(timeout=(.5 if a.scope == 'test' and a.fault == 'primary_timeout' else (480 if role == 'backup' else 45)))
        except subprocess.TimeoutExpired:
            timed_out = True
            if os.name == 'nt':
                termination_exit_code = subprocess.run(['taskkill', '/PID', str(proc.pid), '/T', '/F'], capture_output=True, timeout=15).returncode
            else:
                proc.kill()
            code = proc.wait(timeout=15)
        rec = {'role': role, 'pid': proc.pid, 'exit_code': code, 'timed_out': timed_out,
               'termination_exit_code': termination_exit_code, 'confirmed_exited': proc.poll() is not None, 'seconds': time.perf_counter() - started}
    rec['completed_artifacts'] = {n: {'sha256': r.digest(job / 'out' / n), 'mtime_ns': (job / 'out' / n).stat().st_mtime_ns} for n in r.NAMES if (job / 'out' / n).is_file()}
    rec['qa_mtime_ns'] = (job / 'qa.json').stat().st_mtime_ns if (job / 'qa.json').exists() else None
    r.write_json(job / (role + '-worker-process.json'), rec)
    if timed_out:
        r.write_json(job / 'reconciliation-required.json', {'task_id': a.task_id, 'status': 'STOPPED_FOR_RECONCILIATION', 'reason': 'timeout: verify process tree and partial outputs before handoff', 'worker': rec})
        raise RuntimeError('TIMEOUT_STOPPED_RECONCILE_PROCESS_TREE_BEFORE_HANDOFF')
    return rec


def submit(a, r):
    started = time.perf_counter()
    raw = Path(a.input).read_bytes()
    payload = {'scope': a.scope, 'task_id': a.task_id,
               'csv_base64': base64.b64encode(raw).decode('ascii'),
               'fault': 'force_dsh_backup' if a.fault == 'force_native_backup' else 'none'}
    scope, task, job = r.job_ref(payload)
    with FileLock(str(job / 'launcher.lock'), timeout=0):
        with FileLock(str(job / 'request.lock'), timeout=0):
            scope, task, job, meta = r.prepare(payload)
            prior = r.committed(job)
        attempts = []
        reconciled = bool(prior)
        if not prior:
            first = a.prefer
            attempts.append(run_worker(a, r, job, first))
            # Always read back under the same lock before deciding to transfer ownership.
            with FileLock(str(job / 'request.lock'), timeout=0):
                prior = r.committed(job)
            if not prior and first == 'primary':
                if attempts[-1]['exit_code'] == 0:
                    raise RuntimeError('SUCCESS_WITHOUT_RECEIPT_REQUIRES_RECONCILIATION')
                if not attempts[-1]['confirmed_exited']:
                    raise RuntimeError('OLD_OWNER_NOT_FENCED')
                attempts.append(run_worker(a, r, job, 'backup'))
                with FileLock(str(job / 'request.lock'), timeout=0):
                    prior = r.committed(job)
            elif prior and attempts[-1]['exit_code'] != 0:
                reconciled = True
        if not prior:
            raise RuntimeError('NOT_COMMITTED_RETAIN_ORIGINAL_TASK_AND_RECONCILE')
        with FileLock(str(job / 'request.lock'), timeout=0):
            prior = r.committed(job)
            # Independent readback validation, not worker exit code or model self-report.
            qa = r.checker.verify(job / 'out', job / 'input.csv')
            if not qa['pass'] or qa['count'] != 20:
                raise RuntimeError('READBACK_QA_FAILED')
            if r.digest(job / 'input.csv') != hashlib.sha256(raw).hexdigest():
                raise RuntimeError('INPUT_CHANGED')
            if prior['generation_count'] != 1:
                raise RuntimeError('DUPLICATE_GENERATION')
        result = {'task_id': task, 'status': 'CONFIRMED_COMMITTED', 'scope': scope,
                  'execution_mode': 'independent_process_checkpoint_handoff',
                  'peer_restart': False, 'attempts': attempts,
                  'reconciled_without_regeneration': reconciled,
                  'seconds_input_to_independent_readback': time.perf_counter() - started,
                  'human_takeovers_after_injected_fault': 0,
                  'qa_pass': qa['pass'], 'qa_checks': qa['count'], 'delivery': prior,
                  'cost_status': 'NOT_MEASURED_INFRASTRUCTURE_AND_LABOR'}
        r.write_json(job / ('independent-replay.json' if (job / 'independent-receipt.json').exists() else 'independent-receipt.json'), result)
        return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--config', required=True, type=Path)
    p.add_argument('--input', type=Path)
    p.add_argument('--task-id', default='order-' + uuid.uuid4().hex[:20])
    p.add_argument('--scope', choices=['test', 'prod'], default='prod')
    p.add_argument('--prefer', choices=['primary', 'backup'], default='primary')
    p.add_argument('--role', choices=['primary', 'backup'])
    p.add_argument('--fault', choices=['none', 'primary_exit', 'after_generation', 'after_qa', 'after_commit', 'force_native_backup', 'checkpoint_counter_gap', 'primary_timeout'], default='none')
    a = p.parse_args()
    if a.fault != 'none' and a.scope != 'test':
        p.error('fault injection requires isolated test scope')
    r = load_runtime(a.config)
    if a.role:
        worker(a, r)
    else:
        if not a.input:
            p.error('--input required')
        print(json.dumps(submit(a, r), ensure_ascii=True))


if __name__ == '__main__':
    main()
