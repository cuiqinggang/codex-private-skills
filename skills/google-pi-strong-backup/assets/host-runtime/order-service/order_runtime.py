"""Order-only adapter. n8n schedules; original continuity and filelock persist/guard.

Reuses the installed business_pack.build and independent verify_order_pack.verify.
No arbitrary commands, provider credentials, queue, scheduler or custom state machine.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import hmac
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import threading
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit
from filelock import FileLock, Timeout as LockTimeout

HERE = Path(__file__).resolve().parent
CFG = json.loads((HERE / 'config.json').read_text(encoding='utf-8'))
ROOT = Path(CFG['workspace'])
SCRIPTS = Path(CFG['recipe_scripts'])
sys.path.insert(0, str(SCRIPTS))
import business_pack as builder
import verify_order_pack as checker
spec = importlib.util.spec_from_file_location('original_continuity', CFG['continuity_file'])
continuity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(continuity)
NAMES = ('details.csv', 'summary.json', 'ledger.xlsx', 'report.docx')
ACTIVE_PORT = int(CFG['port'])


class Reject(RuntimeError):
    def __init__(self, code, http=409):
        super().__init__(code)
        self.http = http


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def stamp():
    return time.time_ns() // 1_000_000


def write_json(p, data):
    continuity.atomic_json(Path(p), data)


def job_ref(body, create=True):
    scope = body.get('scope', 'prod')
    task = body.get('task_id', '')
    if scope not in ('prod', 'test') or not isinstance(task, str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{2,63}', task):
        raise Reject('INVALID_SCOPE_OR_TASK_ID', 400)
    if scope == 'test' and not task.startswith('order-test-'):
        raise Reject('TEST_TASK_PREFIX_REQUIRED', 400)
    job = ROOT / 'jobs' / scope / task
    if create:
        job.mkdir(parents=True, exist_ok=True)
    elif not job.is_dir():
        raise Reject('TASK_NOT_FOUND', 404)
    return scope, task, job


def state_root(scope, task):
    return ROOT / 'jobs' / scope / task / 'state' / 'continuity'


def state(scope, task):
    return continuity.load_with_recovery(state_root(scope, task), task)[0]


def prepare(body):
    scope, task, job = job_ref(body)
    fault = body.get('fault', 'none')
    allowed = ('none', 'primary_unavailable', 'after_generation', 'lost_ack', 'force_dsh_backup', 'primary_and_local_unavailable', 'pause_after_generation')
    if fault not in allowed or (scope != 'test' and fault != 'none'):
        raise Reject('FAULTS_ONLY_ALLOWED_IN_ISOLATED_TEST_SCOPE', 400)
    meta_path = job / 'accepted.json'
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding='utf-8'))
        if 'csv_base64' in body:
            try:
                claimed = hashlib.sha256(base64.b64decode(body['csv_base64'], validate=True)).hexdigest()
            except Exception:
                raise Reject('INVALID_BASE64', 400)
            if claimed != meta['input_sha256'] or fault != meta['fault']:
                raise Reject('TASK_ID_REQUEST_CONFLICT')
        if digest(job / 'input.csv') != meta['input_sha256']:
            raise Reject('PROTECTED_INPUT_CHANGED')
        return scope, task, job, meta
    try:
        raw = base64.b64decode(body['csv_base64'], validate=True)
    except Exception:
        raise Reject('CSV_BASE64_REQUIRED', 400)
    if not raw or len(raw) > 16 * 1024 * 1024:
        raise Reject('EMPTY_OR_OVERSIZE_INPUT', 422)
    source = job / 'input.csv'
    if source.exists() and digest(source) != hashlib.sha256(raw).hexdigest():
        raise Reject('TASK_ID_REQUEST_CONFLICT')
    source.write_bytes(raw)
    begun = time.perf_counter()
    try:
        rows, summary = builder.load_rows(source)
    except Exception as exc:
        write_json(job / 'rejected.json', {'code': str(exc), 'at_ms': stamp(), 'retryable': False})
        raise Reject('INPUT_CONTRACT_REJECTED: ' + str(exc), 422)
    continuity.create_task(state_root(scope, task), task, '订单经营日报自动交付', 3, 'mature_recipe')
    meta = {'task_id': task, 'scope': scope, 'input_sha256': digest(source),
            'fault': fault, 'accepted_at_ms': int(body.get('accepted_at_ms') or stamp()),
            'execution_id': str(body.get('execution_id', 'direct-baseline')),
            'summary': summary, 'input_validation_seconds': time.perf_counter() - begun,
            'backup_agent_runs': 0, 'backup_seconds': 0.0, 'generation_count': 0,
            'human_interventions_during_delivery': 0, 'route': 'mature_recipe_primary'}
    write_json(meta_path, meta)
    return scope, task, job, meta


def checked_generated(scope, task, job):
    if 1 not in state(scope, task)['completed_steps']:
        raise Reject('GENERATION_NOT_CONFIRMED')
    rec = json.loads((job / 'generation.json').read_text(encoding='utf-8'))
    if rec['source_sha256'] != digest(job / 'input.csv'):
        raise Reject('GENERATION_INPUT_MISMATCH')
    for name in NAMES:
        if digest(job / 'out' / name) != rec['artifact_sha256'][name]:
            raise Reject('GENERATED_ARTIFACT_CHANGED')
    return rec


def generate(scope, task, job, engine='mature_recipe'):
    if engine == 'PI_V2':
        from method_gate import audit
        method = audit(job)
        if not method['pass']:
            raise Reject('LOAD_MISSING_NATIVE_SKILLS_BEFORE_GENERATION: ' + ','.join(method['missing']))
    if 1 in state(scope, task)['completed_steps']:
        return checked_generated(scope, task, job)
    output = job / 'out'
    if output.exists() and any(output.iterdir()):
        raise Reject('UNCONFIRMED_PARTIAL_OUTPUT_REQUIRES_RECONCILIATION')
    meta = json.loads((job / 'accepted.json').read_text(encoding='utf-8'))
    if digest(job / 'input.csv') != meta['input_sha256']:
        raise Reject('PROTECTED_INPUT_CHANGED')
    started = time.perf_counter()
    result = builder.build(job / 'input.csv', output, '订单经营日报')
    result.update({'engine': engine, 'generation_seconds': time.perf_counter() - started,
                   'artifact_sha256': {n: digest(output / n) for n in NAMES}})
    write_json(job / 'generation.json', result)
    continuity.save_checkpoint(state_root(scope, task), task, 1, 'DONE', 'four artifacts generated', engine,
                               required_files=[str(output / n) for n in NAMES])
    meta['generation_count'] += 1
    write_json(job / 'accepted.json', meta)
    return result


def committed(job):
    path = job / 'delivery.json'
    if not path.is_file():
        return None
    result = json.loads(path.read_text(encoding='utf-8'))
    task, scope = job.name, job.parent.name
    if (result.get('task_id') != task or result.get('scope') != scope
            or result.get('status') != 'CONFIRMED_COMMITTED'
            or job.resolve() != (ROOT / 'jobs' / scope / task).resolve()):
        raise Reject('COMMITTED_IDENTITY_OR_STATUS_INVALID')
    meta = json.loads((job / 'accepted.json').read_text(encoding='utf-8'))
    if (meta.get('task_id') != task or meta.get('scope') != scope
            or meta.get('generation_count') != 1 or result.get('generation_count') != 1):
        raise Reject('COMMITTED_GENERATION_IDENTITY_INVALID')
    actual_input = digest(job / 'input.csv')
    if actual_input != result.get('input_sha256') or actual_input != meta.get('input_sha256'):
        raise Reject('COMMITTED_INPUT_CHANGED')
    artifacts = result.get('artifacts', [])
    if (len(artifacts) != len(NAMES) or {f.get('name') for f in artifacts} != set(NAMES)):
        raise Reject('COMMITTED_FIXED_ARTIFACTS_REQUIRED')
    for f in artifacts:
        expected = (job / 'out' / f['name']).resolve()
        if Path(f.get('path', '')).resolve() != expected or digest(expected) != f.get('sha256'):
            raise Reject('COMMITTED_ARTIFACT_PATH_OR_HASH_INVALID')
    if Path(result.get('qa_path', '')).resolve() != (job / 'qa.json').resolve():
        raise Reject('COMMITTED_QA_PATH_INVALID')
    qa = json.loads((job / 'qa.json').read_text(encoding='utf-8'))
    if (qa.get('pass') is not True or qa.get('count') != 20
            or result.get('qa_pass') is not True or result.get('qa_checks') != 20):
        raise Reject('COMMITTED_QA_NOT_CONFIRMED')
    independent = checker.verify(job / 'out', job / 'input.csv')
    if independent.get('pass') is not True or independent.get('count') != 20:
        raise Reject('COMMITTED_INDEPENDENT_READBACK_FAILED')
    return result


def primary(scope, task, job, meta):
    done = committed(job)
    if done:
        return {'need_backup': False, 'replayed': True, 'task_id': task}
    if meta['fault'] in ('primary_unavailable', 'force_dsh_backup', 'primary_and_local_unavailable'):
        raise Reject('INJECTED_PRIMARY_HTTP_UNAVAILABLE_BEFORE_GENERATION', 503)
    generate(scope, task, job)
    if meta['fault'] == 'pause_after_generation':
        # Isolated crash drill: the coordinator kills only this owned process.
        time.sleep(30)
    if meta['fault'] == 'after_generation':
        continuity.write_handoff(state_root(scope, task), task)
        return {'need_backup': True, 'safe_boundary': 'confirmed_generation_checkpoint', 'task_id': task}
    return {'need_backup': False, 'task_id': task, 'status': 'GENERATED'}


def backup(scope, task, job, meta):
    if committed(job):
        return {'status': 'ALREADY_COMMITTED', 'replayed': True, 'task_id': task}
    continuity.resume_task(state_root(scope, task), task)
    if 1 in state(scope, task)['completed_steps']:
        checked_generated(scope, task, job)
        meta['route'] = 'checkpoint_reuse_no_regeneration'
        write_json(job / 'accepted.json', meta)
        return {'status': 'CHECKPOINT_REUSED', 'task_id': task, 'new_model_runs': 0}
    if (job / 'out').exists() and any((job / 'out').iterdir()):
        raise Reject('UNCONFIRMED_PARTIAL_OUTPUT_REQUIRES_RECONCILIATION')
    # Reuse the certified recipe in a fresh local process before invoking a model.
    # This is a bounded recovery action, not another scheduler or model engine.
    if meta['fault'] != 'force_dsh_backup' and not meta.get('local_recovery_attempts'):
        meta['local_recovery_attempts'] = 1
        write_json(job / 'accepted.json', meta)
        command = [sys.executable, str(HERE / 'order_runtime.py'), 'generate',
                   '--scope', scope, '--job', task, '--engine', 'mature_recipe_recovery']
        if meta['fault'] == 'primary_and_local_unavailable':
            command = [sys.executable, '-c', 'raise SystemExit(86)']
        started = time.perf_counter()
        try:
            local = subprocess.run(command, capture_output=True, text=True, encoding='utf-8',
                                   errors='replace', timeout=30, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            # The known generation wrapper has no child processes; run() reaps it.
            local = subprocess.CompletedProcess(command, 124, '', 'LOCAL_RECOVERY_TIMEOUT_PROCESS_TERMINATED')
        meta = json.loads((job / 'accepted.json').read_text(encoding='utf-8'))
        meta['local_recovery_seconds'] = time.perf_counter() - started
        write_json(job / 'local-recovery-process.json', {'exit_code': local.returncode,
            'seconds': meta['local_recovery_seconds'], 'stdout': local.stdout, 'stderr': local.stderr})
        if local.returncode == 0:
            checked_generated(scope, task, job)
            meta['route'] = 'fresh_process_recipe_recovery'
            write_json(job / 'accepted.json', meta)
            return {'status': 'LOCAL_RECIPE_RECOVERED', 'task_id': task, 'new_model_runs': 0}
        write_json(job / 'accepted.json', meta)
        if (job / 'out').exists() and any((job / 'out').iterdir()):
            raise Reject('UNCONFIRMED_PARTIAL_OUTPUT_REQUIRES_RECONCILIATION')
    if meta['backup_agent_runs']:
        raise Reject('BACKUP_ALREADY_ATTEMPTED_RECONCILE_BEFORE_RETRY')
    meta['backup_agent_runs'] = 1
    meta['route'] = 'pi_v2_backup'
    write_json(job / 'accepted.json', meta)
    if not (job / 'N000.json').exists():
        write_json(job / 'N000.json', {'task_id': task, 'parent_task_id': 'AIORG-ORDERS-AUTO-20261028-001',
            'contract': 'frozen generate-only substep; original independent QA and delivery are performed by the host',
            'input_sha256': meta['input_sha256'], 'existing_checkpoint_root': str(state_root(scope, task)),
            'required_native_skill_tools': ['pi-mature-routing', 'ai-automation-organization-v5',
                'dsh-extreme-effective-time', 'dsh-mature-capabilities', 'reuse-experience-brain'],
            'no_redesign_or_source_log_host_inspection': True})
    if not (job / 'CURRENT.json').exists():
        write_json(job / 'CURRENT.json', {'task_id': task, 'node': 'generation',
            'state_file': str(state_root(scope, task) / 'tasks' / task / 'task-state.json'),
            'next_action': 'load five native skills, invoke the frozen generation wrapper once, immediately finish'})
    task_file = job / 'BACKUP-TASK.txt'
    command = [sys.executable, str(HERE / 'order_runtime.py'), 'generate', '--scope', scope, '--job', task]
    task_file.write_text('已冻结的订单自动化接续任务。无需重新设计或搜索方案。'
        '先使用OMP原生read读取skill://pi-mature-routing、skill://ai-automation-organization-v5、skill://dsh-extreme-effective-time、skill://dsh-mature-capabilities、skill://reuse-experience-brain，然后只执行下面这条既有生成配方的薄调用。'
        '它仅生成本地四个文件并保存原continuity第1步检查点；独立验收由宿主下一节点完成。'
        '五项必须通过OMP原生read工具读取skill://对应名称，并保留成功事件。若命令提示缺项，先原生加载该项再执行；缺项时不会生成任何业务文件。'
        '不要读取正在写入的backup.stdout.jsonl、重读服务源码或检查主机名。不要重写生成器/校验器，不修改原技能、输入、已有状态或网络配置，不调用GPT/Codex。'
        '执行一次，成功后简短回报；不要再运行business_pack CLI造成重复生成。\n'
        + subprocess.list2cmdline(command), encoding='utf-8')
    args = [sys.executable, CFG['backup_entry'], '--task-file', str(task_file), '--cwd', str(job), '--json', '--print']
    env = dict(os.environ, PYTHONIOENCODING='utf-8', REASONIX_CONTINUITY_ROOT=str(state_root(scope, task)))
    started = time.perf_counter()
    with (job / 'backup.stdout.jsonl').open('w', encoding='utf-8') as out, (job / 'backup.stderr.log').open('w', encoding='utf-8') as err:
        proc = subprocess.Popen(args, stdout=out, stderr=err, stdin=subprocess.DEVNULL, env=env, shell=False)
        write_json(job / 'backup-process.json', {'pid': proc.pid, 'started_at_ms': stamp(), 'entry': CFG['backup_entry']})
        try:
            code = proc.wait(timeout=420)
        except subprocess.TimeoutExpired:
            subprocess.run(['taskkill', '/PID', str(proc.pid), '/T', '/F'], capture_output=True, timeout=15)
            proc.wait(timeout=15)
            raise Reject('BACKUP_TIMEOUT_NO_AUTOMATIC_RESUBMIT', 504)
    meta = json.loads((job / 'accepted.json').read_text(encoding='utf-8'))
    meta['backup_seconds'] = time.perf_counter() - started
    write_json(job / 'accepted.json', meta)
    if code:
        raise Reject('BACKUP_EXIT_' + str(code), 502)
    checked_generated(scope, task, job)
    write_json(job / 'backup-host-receipt.json', {'exit_code': code, 'seconds': meta['backup_seconds'],
        'stdout_sha256': digest(job / 'backup.stdout.jsonl'), 'input_sha256': digest(job / 'input.csv'),
        'entry': CFG['backup_entry'], 'OpenAI_required': False})
    return {'status': 'BACKUP_GENERATED', 'task_id': task}


def verify(scope, task, job, meta):
    if committed(job):
        return {'status': 'ALREADY_COMMITTED', 'task_id': task}
    checked_generated(scope, task, job)
    if 2 in state(scope, task)['completed_steps']:
        return json.loads((job / 'qa.json').read_text(encoding='utf-8'))
    started = time.perf_counter()
    qa = checker.verify(job / 'out', job / 'input.csv')
    qa['seconds'] = time.perf_counter() - started
    qa['checker_sha256'] = digest(CFG['checker_file'])
    write_json(job / 'qa.json', qa)
    if not qa['pass']:
        raise Reject('INDEPENDENT_QA_FAILED', 422)
    continuity.save_checkpoint(state_root(scope, task), task, 2, 'DONE', 'independent original checker 20/20 PASS',
                               'independent_checker', required_files=[str(job / 'qa.json')])
    return qa


def commit(scope, task, job, meta):
    prior = committed(job)
    if prior:
        return {**prior, 'replayed': True}
    generated = checked_generated(scope, task, job)
    if 2 not in state(scope, task)['completed_steps']:
        raise Reject('QA_NOT_CONFIRMED')
    qa = json.loads((job / 'qa.json').read_text(encoding='utf-8'))
    if not qa['pass'] or qa['count'] != 20:
        raise Reject('QA_NOT_ACCEPTED')
    meta = json.loads((job / 'accepted.json').read_text(encoding='utf-8'))
    artifacts = [{'name': n, 'path': str(job / 'out' / n), 'sha256': digest(job / 'out' / n),
                  'bytes': (job / 'out' / n).stat().st_size} for n in NAMES]
    result = {'task_id': task, 'scope': scope, 'status': 'CONFIRMED_COMMITTED', 'replayed': False,
        'version': 'order-independent-1.0', 'AIORG': 'V5', 'backup_version': 'V2.0',
        'route': meta['route'], 'engine': generated['engine'], 'execution_id': meta['execution_id'],
        'input_sha256': meta['input_sha256'], 'row_count': meta['summary']['row_count'],
        'total_cents': meta['summary']['total_cents'], 'qa_pass': True, 'qa_checks': qa['count'],
        'qa_path': str(job / 'qa.json'), 'artifacts': artifacts, 'delivered_at_ms': stamp(),
        'generation_count': meta['generation_count'], 'backup_agent_runs': meta['backup_agent_runs'],
        'local_recovery_attempts': meta.get('local_recovery_attempts', 0),
        'human_interventions_during_delivery': 0,
        'delivery_executor_port': ACTIVE_PORT, 'delivery_executor_pid': os.getpid(),
        'fault_monitor': 'owned subprocess exit and bounded timeout; filelock fencing',
        'peer_repair_policy': 'disabled: independent executors',
        'timings': {'input_validation_seconds': meta['input_validation_seconds'],
                    'generation_seconds': generated['generation_seconds'],
                    'independent_qa_seconds': qa['seconds'], 'backup_agent_seconds': meta['backup_seconds'],
                    'local_recovery_seconds': meta.get('local_recovery_seconds', 0.0),
                    'n8n_accept_to_manifest_seconds': (stamp() - meta['accepted_at_ms']) / 1000},
        'cost': {'incremental_platform_subscription': 0, 'primary_model_requests': 0,
                 'backup_agent_runs': meta['backup_agent_runs'],
                 'model_input_tokens': 0 if not meta['backup_agent_runs'] else None,
                 'model_output_tokens': 0 if not meta['backup_agent_runs'] else None,
                 'provider_billed_amount': 0 if not meta['backup_agent_runs'] else None,
                 'total_cost_status': 'NOT_MEASURED_INFRASTRUCTURE_AND_LABOR',
                 'backup_billing_status': 'NOT_APPLICABLE' if not meta['backup_agent_runs'] else 'BILL_NOT_OBTAINED'}}
    write_json(job / 'delivery.json', result)
    continuity.save_checkpoint(state_root(scope, task), task, 3, 'DONE', 'delivery manifest persisted',
                               'delivery_commit', required_files=[str(job / 'delivery.json')])
    continuity.close_task(state_root(scope, task), task, 'PASS', 'independent QA and four deliverables committed')
    if meta['fault'] == 'lost_ack':
        write_json(job / 'injected-ack-loss.json', {'committed': True, 'at_ms': stamp()})
        raise Reject('INJECTED_ACK_LOSS_AFTER_CONFIRMED_COMMIT', 503)
    return result


OPERATIONS = {'/primary': primary, '/backup': backup, '/verify': verify, '/commit': commit}



def repair_peer(scope, task, job):
    """Known exited executor only; a bounded start after delivery, never a general watchdog."""
    peer = int(CFG['backup_port']) if ACTIVE_PORT == int(CFG['port']) else int(CFG['port'])
    started = time.perf_counter()
    result = {'executor_port': ACTIVE_PORT, 'peer_port': peer, 'at_ms': stamp()}
    try:
        try:
            with urllib.request.urlopen('http://127.0.0.1:' + str(peer) + '/healthz', timeout=.4) as r:
                health = json.load(r)
            if health.get('version') != 'order-automation-1.2' or health.get('port') != peer:
                raise RuntimeError('PEER_PORT_BELONGS_TO_UNEXPECTED_SERVICE')
            result.update(status='ALREADY_HEALTHY', peer_pid=health['pid'])
        except (urllib.error.URLError, TimeoutError, OSError):
            process = subprocess.run([sys.executable, str(HERE / 'start_adapter.py'), '--port', str(peer)],
                capture_output=True, text=True, encoding='utf-8', timeout=15, stdin=subprocess.DEVNULL)
            result.update(status='RESTORED' if process.returncode == 0 else 'FAILED',
                          starter_exit=process.returncode, starter_result=process.stdout[-2000:],
                          starter_error=process.stderr[-1000:])
    except Exception as exc:
        result.update(status='FAILED', error=type(exc).__name__ + ': ' + str(exc))
    result['seconds_after_delivery'] = time.perf_counter() - started
    write_json(job / 'peer-repair.json', result)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def send(self, status, obj):
        if isinstance(obj, dict):
            obj = {**obj, 'responding_executor_port': ACTIVE_PORT,
                   'executor_base_url': 'http://host.docker.internal:' + str(ACTIVE_PORT)}
        data = json.dumps(obj, ensure_ascii=True).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def authorized(self):
        expected = 'Bearer ' + Path(CFG['token_file']).read_text(encoding='utf-8-sig').strip()
        return hmac.compare_digest(self.headers.get('Authorization', ''), expected)

    def do_GET(self):
        query = urlsplit(self.path)
        if query.path == '/healthz':
            return self.send(200, {'status': 'ready', 'version': 'order-automation-1.2', 'pid': os.getpid(), 'port': ACTIVE_PORT})
        if query.path != '/receipt' or not self.authorized():
            return self.send(401, {'code': 'UNAUTHORIZED'})
        try:
            q = parse_qs(query.query)
            scope, task, job = job_ref({'scope': q.get('scope', ['prod'])[0], 'task_id': q.get('task_id', [''])[0]}, False)
            with FileLock(str(job / 'request.lock'), timeout=0):
                result = committed(job)
                if result:
                    return self.send(200, {**result, 'reconciled_read_only': True})
                progress = state(scope, task)
                return self.send(202, {'status': 'NOT_COMMITTED', 'completed_steps': progress['completed_steps']})
        except LockTimeout:
            return self.send(423, {'code': 'IN_PROGRESS_DO_NOT_RESUBMIT'})
        except Reject as e:
            return self.send(e.http, {'code': str(e)})
        except Exception as e:
            return self.send(409, {'code': type(e).__name__ + ': ' + str(e)})

    def do_POST(self):
        if not self.authorized():
            return self.send(401, {'code': 'UNAUTHORIZED'})
        if self.path not in OPERATIONS:
            return self.send(404, {'code': 'UNKNOWN_OPERATION'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 24 * 1024 * 1024:
                raise Reject('INVALID_PAYLOAD_SIZE', 413)
            body = json.loads(self.rfile.read(length).decode('utf-8'))
            scope, task, job = job_ref(body)
            with FileLock(str(job / 'request.lock'), timeout=0):
                scope, task, job, meta = prepare(body)
                result = OPERATIONS[self.path](scope, task, job, meta)
            self.send(200, result)
            if CFG.get('peer_repair_enabled', False) and self.path == '/commit' and result.get('status') == 'CONFIRMED_COMMITTED' and not result.get('replayed'):
                threading.Thread(target=repair_peer, args=(scope, task, job), daemon=True).start()
            return
        except LockTimeout:
            return self.send(423, {'code': 'IN_PROGRESS_DO_NOT_RESUBMIT'})
        except Reject as e:
            return self.send(e.http, {'code': str(e), 'retryable': False})
        except Exception as e:
            return self.send(500, {'code': type(e).__name__ + ': ' + str(e), 'retryable': False})


def main():
    global ACTIVE_PORT
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=['serve', 'generate', 'baseline'])
    p.add_argument('--scope', choices=['prod', 'test'], default='test')
    p.add_argument('--job')
    p.add_argument('--input', type=Path)
    p.add_argument('--engine', choices=['PI_V2', 'mature_recipe_recovery'], default='PI_V2')
    p.add_argument('--port', type=int, choices=[int(CFG['port']), int(CFG.get('backup_port', 8795))], default=int(CFG['port']))
    a = p.parse_args()
    ACTIVE_PORT = a.port
    if a.action == 'serve':
        ROOT.mkdir(parents=True, exist_ok=True)
        with FileLock(str(ROOT / ('adapter-service-' + str(ACTIVE_PORT) + '.lock')), timeout=0):
            for path, expected in CFG['dependency_sha256'].items():
                if digest(path) != expected:
                    raise Reject('FROZEN_DEPENDENCY_CHANGED: ' + path)
            write_json(ROOT / ('service-running-' + str(ACTIVE_PORT) + '.json'), {'pid': os.getpid(), 'port': ACTIVE_PORT, 'started_at_ms': stamp()})
            ThreadingHTTPServer(('127.0.0.1', ACTIVE_PORT), Handler).serve_forever()
    elif a.action == 'generate':
        scope, task, job = job_ref({'scope': a.scope, 'task_id': a.job}, False)
        print(json.dumps(generate(scope, task, job, a.engine), ensure_ascii=True))
    else:
        started = time.perf_counter()
        body = {'scope': a.scope, 'task_id': a.job, 'accepted_at_ms': stamp(),
                'csv_base64': base64.b64encode(a.input.read_bytes()).decode('ascii')}
        scope, task, job = job_ref(body)
        with FileLock(str(job / 'request.lock'), timeout=0):
            scope, task, job, meta = prepare(body)
            generate(scope, task, job)
            verify(scope, task, job, meta)
            result = commit(scope, task, job, meta)
        result['direct_baseline_seconds'] = time.perf_counter() - started
        write_json(job / 'baseline-measurement.json', result)
        print(json.dumps(result, ensure_ascii=True))


if __name__ == '__main__':
    main()
