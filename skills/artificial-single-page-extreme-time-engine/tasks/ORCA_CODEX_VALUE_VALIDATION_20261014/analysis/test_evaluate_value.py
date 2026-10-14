"""仅验证离线判定逻辑的合成单元测试；绝非Orca或Codex业务执行记录。"""
import copy
import hashlib
import math
import unittest
from evaluate_value import evaluate, SCOPE


def fixture():
    pairs = []
    for n in range(1, 11):
        p = {'pair_id': n, 'order': ['A', 'B'] if n % 2 else ['B', 'A']}
        for arm, elapsed in [('A', 1000), ('B', 800)]:
            p[arm] = dict(input_sha256='a'*64, quality_contract_sha256='b'*64,
                model='SYNTHETIC_MODEL_NOT_CALLED', effort='same', service_tier='same',
                concurrency=1, cache_policy='same', workflow_freeze='F_'+arm,
                receipt_sha256=hashlib.sha256(f'SYNTHETIC:{n}:{arm}'.encode()).hexdigest(),
                full_suite=True, independent_acceptance=True, unexpected_failures=0,
                unresolved_effects=False, full_wall_ms=elapsed, timing_scope=SCOPE)
        pairs.append(p)
    return dict(task_id='SYNTHETIC_UNIT_FIXTURE_ONLY', pairs=pairs,
        final_versions={'A':'F_A','B':'F_B'}, extra_costs=dict(complete=True,
        setup_and_migration_ms=500, unembedded_failures_and_maintenance_ms=100,
        overlaps_suite_time=False))


class EvidenceGateTests(unittest.TestCase):
    def test_real_current_missing_b_is_not_pass(self):
        r=evaluate({'pairs':[]}); self.assertFalse(r['ten_round_gate_passed']); self.assertIsNone(r['net_time_savings_ms'])
    def test_arithmetic_on_synthetic_fixture(self):
        r=evaluate(fixture()); self.assertEqual(r['local_suite_savings_ms'],2000); self.assertEqual(r['net_time_savings_ms'],1400)
    def test_nine_pairs_cannot_count_ten(self):
        d=fixture(); d['pairs'].pop(); self.assertFalse(evaluate(d)['ten_round_gate_passed'])
    def test_health_checks_are_not_full_suite(self):
        d=fixture(); d['pairs'][0]['B']['full_suite']=False; self.assertFalse(evaluate(d)['ten_round_gate_passed'])
    def test_partial_timer_refused(self):
        d=fixture(); d['pairs'][0]['B']['timing_scope']='model_only'; self.assertFalse(evaluate(d)['time_comparison_valid'])
    def test_reused_receipt_refused(self):
        d=fixture(); d['pairs'][1]['B']['receipt_sha256']=d['pairs'][0]['B']['receipt_sha256']; self.assertFalse(evaluate(d)['time_comparison_valid'])
    def test_mixed_version_refused(self):
        d=fixture(); d['pairs'][3]['B']['workflow_freeze']='older'; r=evaluate(d); self.assertFalse(r['ten_round_gate_passed']); self.assertEqual(r['declared_B_final_version_consecutive_passes'],6)
    def test_quality_not_relaxed(self):
        d=fixture(); d['pairs'][0]['B']['quality_contract_sha256']='c'*64; self.assertFalse(evaluate(d)['time_comparison_valid'])
    def test_model_not_changed(self):
        d=fixture(); d['pairs'][0]['B']['model']='different'; self.assertFalse(evaluate(d)['time_comparison_valid'])
    def test_nan_timer_refused(self):
        d=fixture(); d['pairs'][0]['B']['full_wall_ms']=math.nan; self.assertFalse(evaluate(d)['time_comparison_valid'])
    def test_unknown_cost_does_not_become_zero(self):
        d=fixture(); d['extra_costs']['complete']=False; r=evaluate(d); self.assertIsNone(r['net_time_savings_ms']); self.assertFalse(r['deployment_recommended'])
    def test_failure_resets_consecutive_count(self):
        d=fixture(); d['pairs'][5]['B']['unexpected_failures']=1; r=evaluate(d); self.assertEqual(r['declared_B_final_version_consecutive_passes'],4); self.assertFalse(r['ten_round_gate_passed'])
    def test_setup_cost_can_make_faster_product_not_worthwhile(self):
        d=fixture(); d['extra_costs']['setup_and_migration_ms']=4000; r=evaluate(d); self.assertGreater(r['local_suite_savings_ms'],0); self.assertLess(r['net_time_savings_ms'],0); self.assertFalse(r['deployment_recommended'])
    def test_overlapping_cost_refused(self):
        d=fixture(); d['extra_costs']['overlaps_suite_time']=True; r=evaluate(d); self.assertEqual(r['decision'],'COST_OVERLAP_UNRESOLVED'); self.assertIsNone(r['net_time_savings_ms'])
    def test_p95_is_sample_max_with_ten(self):
        d=fixture(); d['pairs'][9]['A']['full_wall_ms']=5000; self.assertEqual(evaluate(d)['statistics']['A']['sample_p95_nearest_rank_ms'],5000)
    def test_unknown_effects_refused(self):
        d=fixture(); d['pairs'][0]['B']['unresolved_effects']=True; self.assertFalse(evaluate(d)['time_comparison_valid'])
    def test_preregistered_order_preserved(self):
        d=fixture(); d['pairs'][1]['order']=['A','B']; self.assertFalse(evaluate(d)['time_comparison_valid'])
    def test_duplicate_pair_id_refused(self):
        d=fixture(); d['pairs'][1]['pair_id']=1; self.assertFalse(evaluate(d)['time_comparison_valid'])

if __name__=='__main__': unittest.main(verbosity=2)
