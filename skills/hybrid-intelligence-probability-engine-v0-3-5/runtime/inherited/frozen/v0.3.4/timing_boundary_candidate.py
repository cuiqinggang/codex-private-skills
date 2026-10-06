"""Offline-reviewed timing component, NOT an integrated HIPE Reality capsule.

A caller must supply the entire synchronous path, including all its verification
and final output writes. Returned elapsed_ms is an observation, not a HIPE
certification. Observer receipts are separate from unmodified task outputs.
"""
from __future__ import annotations
import hashlib
import inspect
import json
import os
import time
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

COMPONENT_ID = 'HIPE-v0.3.4-R5-TIMING-COMPONENT-01'

class BoundaryError(RuntimeError):
    """No candidate may be promoted when this exception is raised."""
    def __init__(self, category: str, observation: dict | None = None):
        super().__init__(category)
        self.category = category
        self.observation = observation

class SystemClock:
    simulation = False
    @staticmethod
    def mono_ns() -> int:
        return time.perf_counter_ns()
    @staticmethod
    def wall_ns() -> int:
        return time.time_ns()

SYSTEM_CLOCK = SystemClock()

def utc_iso(epoch_ns: int) -> str:
    secs, ns = divmod(epoch_ns, 1_000_000_000)
    return datetime.fromtimestamp(secs, timezone.utc).strftime('%Y-%m-%dT%H:%M:%S') + f'.{ns:09d}+00:00'

def fingerprint(path: Path) -> dict:
    # The reads below are INSIDE the observed interval when called by observe_path.
    digest = hashlib.sha256()
    count = 0
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
            count += len(block)
    return {'path': str(path), 'bytes': count, 'sha256': digest.hexdigest()}

def _store_receipt(path: Path, receipt: dict) -> None:
    # Exclusive creation protects historical receipts; a failed write is NOT usable.
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(receipt, ensure_ascii=False, indent=2, allow_nan=False)
    with path.open('x', encoding='utf-8') as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())

def observe_path(operation: Callable[[], Mapping[str, Any]], *, run_id: str,
                 path_name: str, variant: int, phase: str,
                 required_outputs: Sequence[Path | str], receipt_path: Path | str,
                 clock: Any = SYSTEM_CLOCK) -> tuple[Mapping[str, Any], dict]:
    """Observe one COMPLETE synchronous path. Never rewrites its output/result.

    Every expected output must be new: reusing an old R4 output is not a rerun.
    Input validation, operation, validation of its return, and output hashing are
    timed. The observation receipt is persisted after the end timestamp; failure
    to persist it raises, so no usable timing observation is returned.
    """
    start_wall = clock.wall_ns()
    start = clock.mono_ns()
    result = None
    snapshots = []
    issue = None
    paths = []
    target = Path(receipt_path).resolve()
    try:
        if not isinstance(run_id, str) or not run_id.strip():
            raise BoundaryError('INVALID_RUN_ID')
        if path_name not in ('FULL_GPT', 'HYBRID'):
            raise BoundaryError('INVALID_PATH_NAME')
        if phase not in ('WARMUP', 'MEASURED', 'OFFLINE_TEST'):
            raise BoundaryError('INVALID_PHASE')
        if type(variant) is not int or variant < 0:
            raise BoundaryError('INVALID_VARIANT')
        paths = [Path(p).resolve() for p in required_outputs]
        if not paths or len(set(paths)) != len(paths) or target in paths:
            raise BoundaryError('INVALID_OUTPUT_SET')
        if target.exists() or any(p.exists() for p in paths):
            raise BoundaryError('PREEXISTING_OUTPUT_OR_RECEIPT')
        result = operation()
        if inspect.isawaitable(result):
            if inspect.iscoroutine(result):
                result.close()
            raise BoundaryError('ASYNCHRONOUS_RETURN_NOT_SUPPORTED')
        if not isinstance(result, Mapping):
            raise BoundaryError('RESULT_NOT_MAPPING')
        if result.get('valid') is not True or result.get('errors') != []:
            raise BoundaryError('PATH_CORRECTNESS_NOT_PASS')
        if result.get('path') != path_name or result.get('variant') != variant:
            raise BoundaryError('RESULT_IDENTITY_MISMATCH')
        snapshots = [fingerprint(p) for p in paths]
    except Exception as exc:
        # Do not store exception text; it can contain credentials/response content.
        issue = exc.category if isinstance(exc, BoundaryError) else type(exc).__name__
    end = clock.mono_ns()
    end_wall = clock.wall_ns()
    if type(start) is not int or type(end) is not int or end < start:
        issue = 'INVALID_MONOTONIC_CLOCK'
    delta = end - start if type(start) is int and type(end) is int else None
    record = {
        'component_id': COMPONENT_ID, 'run_id': run_id, 'path': path_name,
        'variant': variant, 'phase': phase,
        'REAL_START': utc_iso(start_wall), 'REAL_END': utc_iso(end_wall),
        'REAL_START_EPOCH_NS': start_wall, 'REAL_END_EPOCH_NS': end_wall,
        'REAL_START_MONO_NS': start, 'REAL_END_MONO_NS': end,
        'clock': 'INJECTED_TEST_CLOCK' if clock is not SYSTEM_CLOCK else 'time.perf_counter_ns',
        'simulation': clock is not SYSTEM_CLOCK,
        'wall_clock_reversed': end_wall < start_wall,
        'elapsed_ns': delta, 'elapsed_ms': delta / 1e6 if delta is not None and delta >= 0 else None,
        'path_complete_and_correct': issue is None,
        'error_category': issue, 'outputs': snapshots,
        'required_output_paths': [str(p) for p in paths],
        'T_VALID_REAL_MS': None,
        'HIPE_REALITY_CERTIFIED': False,
        'integration_with_R4_verified': False,
        'boundary': 'wrapper entry through synchronous operation return, return checks, and required-output readback/hashes',
        'receipt_write_in_elapsed': False,
        'receipt_role': 'observer-only metadata; never substitutes for any required task result or operational evidence',
    }
    if target in paths:
        # Bad configuration must not create observer metadata at a task-output path.
        raise BoundaryError(issue or 'INVALID_OUTPUT_SET', record)
    try:
        _store_receipt(target, record)
    except Exception as exc:
        raise BoundaryError('OBSERVER_RECEIPT_NOT_PERSISTED', record) from exc
    if issue:
        raise BoundaryError(issue, record)
    return result, record

def verify_observation(receipt_path: Path | str, *, run_id: str, path_name: str,
                       variant: int, phase: str) -> dict:
    """Check current evidence consistency. Does NOT prove arbitrary callback code."""
    r = json.loads(Path(receipt_path).read_text(encoding='utf-8'))
    if any(r.get(k) != v for k, v in {'run_id': run_id, 'path': path_name,
                                     'variant': variant, 'phase': phase,
                                     'component_id': COMPONENT_ID}.items()):
        raise BoundaryError('OBSERVATION_IDENTITY_MISMATCH')
    if r.get('path_complete_and_correct') is not True or r.get('error_category') is not None:
        raise BoundaryError('OBSERVATION_NOT_SUCCESSFUL')
    a, b, d = r.get('REAL_START_MONO_NS'), r.get('REAL_END_MONO_NS'), r.get('elapsed_ns')
    if any(type(x) is not int for x in (a, b, d)) or b < a or d != b - a or r.get('elapsed_ms') != d / 1e6:
        raise BoundaryError('OBSERVATION_TIME_INCONSISTENT')
    for prefix in ('REAL_START', 'REAL_END'):
        if type(r.get(prefix + '_EPOCH_NS')) is not int or r.get(prefix) != utc_iso(r[prefix + '_EPOCH_NS']):
            raise BoundaryError('OBSERVATION_WALL_CLOCK_INCONSISTENT')
    if r.get('T_VALID_REAL_MS') is not None or r.get('HIPE_REALITY_CERTIFIED') is not False or r.get('integration_with_R4_verified') is not False:
        raise BoundaryError('UNSUPPORTED_CERTIFICATION_CLAIM')
    outputs = r.get('outputs')
    if not isinstance(outputs, list) or not outputs or [x['path'] for x in outputs] != r.get('required_output_paths'):
        raise BoundaryError('OBSERVATION_OUTPUT_SET_MISMATCH')
    for item in outputs:
        if fingerprint(Path(item['path'])) != item:
            raise BoundaryError('TASK_OUTPUT_CHANGED')
    return {'component_evidence_consistent': True,
            'HIPE_REALITY_CERTIFIED': False, 'elapsed_ms': r['elapsed_ms']}
