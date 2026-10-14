"""Orca 本任务的离线证据判定器；不启动任务，不接触账户，不代替独立验收。"""
from __future__ import annotations
import argparse
import json
import math
import re
import statistics
from pathlib import Path
from typing import Any

SCOPE = 'input_to_independent_acceptance_and_evidence_readback'
MATCH = ('input_sha256', 'quality_contract_sha256', 'model', 'effort',
         'service_tier', 'concurrency', 'cache_policy')
SHA = re.compile(r'[0-9a-f]{64}\Z')

def number(value: Any, *, positive: bool = False) -> bool:
    return (not isinstance(value, bool) and isinstance(value, (int, float))
            and math.isfinite(value) and (value > 0 if positive else value >= 0))

def evaluate(data: dict[str, Any]) -> dict[str, Any]:
    """只核对已交付证据的完整性/算术；真实回执与业务质量仍须外部核验。"""
    required = 10
    pairs = data.get('pairs', [])
    errors: list[str] = []
    totals: dict[str, list[float]] = {'A': [], 'B': []}
    seen_pairs: set[int] = set()
    seen_receipts: set[str] = set()
    trailing_b = 0
    checked_pairs = 0
    final_versions = data.get('final_versions', {})
    if len(pairs) != required:
        errors.append(f'需要10组完整配对，当前记录{len(pairs)}组')
    for position, pair in enumerate(pairs, 1):
        pair_errors: list[str] = []
        pair_id = pair.get('pair_id')
        if pair_id != position or pair_id in seen_pairs:
            pair_errors.append('配对序号缺失、重复或未按原顺序登记')
        if isinstance(pair_id, int):
            seen_pairs.add(pair_id)
        order = ['A', 'B'] if position % 2 else ['B', 'A']
        if pair.get('order') != order:
            pair_errors.append('不符合预登记AB/BA交错顺序')
        lanes = {arm: pair.get(arm, {}) for arm in ('A', 'B')}
        for key in MATCH:
            a, b = lanes['A'].get(key), lanes['B'].get(key)
            if a is None or b is None or a != b:
                pair_errors.append(f'控制条件不同或缺失:{key}')
        for arm, lane in lanes.items():
            ok = (lane.get('full_suite') is True and lane.get('independent_acceptance') is True
                  and lane.get('unexpected_failures') == 0 and lane.get('unresolved_effects') is False)
            version = final_versions.get(arm)
            if not version or lane.get('workflow_freeze') != version:
                ok = False
                pair_errors.append(f'{arm}:不是指定最终冻结版本')
            if not ok:
                pair_errors.append(f'{arm}:全流程/独立验收/无故障证据不足')
            receipt = lane.get('receipt_sha256', '')
            if not isinstance(receipt, str) or not SHA.fullmatch(receipt) or receipt in seen_receipts:
                pair_errors.append(f'{arm}:回执SHA缺失、非法或重复使用')
            else:
                seen_receipts.add(receipt)
            elapsed = lane.get('full_wall_ms')
            if not number(elapsed, positive=True) or lane.get('timing_scope') != SCOPE:
                pair_errors.append(f'{arm}:完整耗时无效或仅为局部计时')
            elif ok:
                totals[arm].append(float(elapsed))
            if arm == 'B':
                trailing_b = trailing_b + 1 if ok else 0
        if pair_errors:
            errors.extend(f'配对{position}:{e}' for e in pair_errors)
        else:
            checked_pairs += 1
    result: dict[str, Any] = {
        'task_id': data.get('task_id'), 'required_pairs': required,
        'recorded_pairs': len(pairs), 'schema_checked_full_pairs': checked_pairs,
        'declared_B_final_version_consecutive_passes': trailing_b,
        'time_comparison_valid': False, 'ten_round_gate_passed': False,
        'local_suite_savings_ms': None, 'local_suite_savings_percent': None,
        'net_time_savings_ms': None, 'break_even_suites_estimate': None,
        'cash_cost_savings': None, 'deployment_recommended': False,
        'decision': 'EVIDENCE_INCOMPLETE', 'errors': errors,
        'scope': '结构与算术核对；不是源回执真实性、模型执行或全局最优认证',
        'context': data.get('observed_context', {})}
    if errors or checked_pairs != required:
        return result
    a, b = sum(totals['A']), sum(totals['B'])
    delta = a - b
    result.update(time_comparison_valid=True, ten_round_gate_passed=trailing_b >= required,
                  local_suite_savings_ms=delta, local_suite_savings_percent=100 * delta / a)
    result['statistics'] = {
        arm: {'total_ms': sum(v), 'mean_ms': statistics.mean(v), 'median_ms': statistics.median(v),
              'sample_p95_nearest_rank_ms': sorted(v)[math.ceil(.95 * len(v)) - 1],
              'p95_note': '10样本时为最大观测值，不是生产P95保证'}
        for arm, v in totals.items()}
    costs = data.get('extra_costs', {})
    setup, prior = costs.get('setup_and_migration_ms'), costs.get('unembedded_failures_and_maintenance_ms')
    if costs.get('complete') is not True or not number(setup) or not number(prior):
        result['decision'] = 'TIMING_COMPARED_COST_INCOMPLETE'
        return result
    if costs.get('overlaps_suite_time') is not False:
        result['decision'] = 'COST_OVERLAP_UNRESOLVED'
        return result
    result['net_time_savings_ms'] = delta - setup - prior
    if delta > 0:
        result['break_even_suites_estimate'] = math.ceil((setup + prior) / (delta / required))
    result['deployment_recommended'] = delta - setup - prior > 0 and trailing_b >= required
    result['decision'] = 'POSITIVE_MEASURED_TIME_VALUE' if result['deployment_recommended'] else 'NO_POSITIVE_NET_TIME_VALUE'
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = evaluate(json.loads(args.input.read_text(encoding='utf-8-sig')))
    text = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(text, encoding='utf-8')
    print(text, end='')
