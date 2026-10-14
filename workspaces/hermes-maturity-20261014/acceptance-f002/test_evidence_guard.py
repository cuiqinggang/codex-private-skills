"""Synthetic guard tests only: these are not Hermes tool, API, or Windows tests."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from evidence_guard import REQUIRED, inspect_batch

class ReceiptGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.put('FIXTURE-MANIFEST.json', {'cases': ['synthetic-only']})
        self.fixture = hashlib.sha256((self.root / 'FIXTURE-MANIFEST.json').read_bytes()).hexdigest()
        self.put('REALITY-F002.json', {'task_id': 'HERMES-ECO-20261014', 'contract_ref': 'F002',
            'config_sha256': 'a'*64, 'fixtures_sha256': self.fixture})
        for r in range(1, 6):
            self.put(f'R{r:02}/round-result.json', {'round': r, 'pass': True, 'full_wall_ms': r*1000,
                'contract_ref': 'F002', 'config_sha256': 'a'*64, 'fixture_sha256': self.fixture})
            for p in (1,2):
                base = f'R{r:02}/'; rid = f'run_{r}_{p}'
                self.put(base+f'grade-{p}.json', {'phase': p, 'pass': True, 'checks': dict.fromkeys(REQUIRED[p], True)})
                self.put(base+f'ack-{p}.json', {'run_id': rid})
                self.put(base+f'run-{p}.json', {'run_id': rid, 'session_id': f'session_{r}_{p}', 'status': 'completed',
                    'runtime': {'model': 'deepseek/deepseek-v4.1-flash', 'provider': 'openrouter'}})
                self.put(base+f'idempotency-{p}.json', {'run_id': rid, 'replayed': True, 'same_run_id': True})
                ev=[{'run_id':rid,'event':'tool.started','tool':'terminal','preview':str(self.root/base/'run-tests.cmd')},
                    {'run_id':rid,'event':'tool.completed','tool':'terminal','error':p==1}]
                self.write_events(r,p,ev)
    def put(self, name, data):
        p=self.root/name; p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data),encoding='utf-8')
    def patch(self, name, **data):
        obj=json.loads((self.root/name).read_text());obj.update(data);self.put(name,obj)
    def write_events(self,r,p,events):
        (self.root/f'R{r:02}'/f'events-{p}.sse').write_text(''.join('data: '+json.dumps(e)+'\n\n' for e in events))
    def read_events(self,r,p):
        return [json.loads(x[6:]) for x in (self.root/f'R{r:02}'/f'events-{p}.sse').read_text().splitlines() if x.startswith('data: ')]
    def assert_rejected(self):
        result=inspect_batch(self.root)
        self.assertFalse(result['five_round_contract_pass'])
        self.assertFalse(result['whole_station_final_valid'])
        self.assertFalse(result['automatic_retry_permitted'])
        return result
    def test_complete_synthetic_receipts_only_pass_scoped_contract(self):
        r=inspect_batch(self.root)
        self.assertTrue(r['five_round_contract_pass']);self.assertEqual(r['consecutive_pass'],5)
        for k in ('whole_station_final_valid','reboot_verified','full_browser_chat_e2e_verified','long_duration_verified','physical_optimum_verified'):
            self.assertFalse(r[k])
    def test_missing_freeze(self):
        (self.root/'REALITY-F002.json').unlink();self.assertEqual(self.assert_rejected()['status'],'UNKNOWN_RECONCILE_FIRST')
    def test_foreign_freeze(self):
        self.patch('REALITY-F002.json',task_id='other');self.assert_rejected()
    def test_corrupt_freeze(self):
        (self.root/'REALITY-F002.json').write_text('{');self.assert_rejected()
    def test_fixture_changed(self):
        self.put('FIXTURE-MANIFEST.json',{'changed':True});self.assert_rejected()
    def test_missing_round(self):
        (self.root/'R03/round-result.json').unlink();self.assert_rejected()
    def test_unknown_post_cannot_count_as_success(self):
        (self.root/'R01/ack-1.json').unlink();self.assert_rejected()
    def test_string_pass_rejected(self):
        self.patch('R01/round-result.json',**{'pass':'true'});self.assert_rejected()
    def test_nonconsecutive_successes_not_five(self):
        self.patch('R03/round-result.json',**{'pass':False})
        r=self.assert_rejected();self.assertEqual(r['consecutive_pass'],2);self.assertEqual(r['failed_or_unknown_count'],1)
    def test_old_contract_rejected(self):
        self.patch('R01/round-result.json',contract_ref='F001');self.assert_rejected()
    def test_config_drift_rejected(self):
        self.patch('R01/round-result.json',config_sha256='b'*64);self.assert_rejected()
    def test_different_fixture_rejected(self):
        self.patch('R01/round-result.json',fixture_sha256='b'*64);self.assert_rejected()
    def test_negative_time_rejected(self):
        self.patch('R01/round-result.json',full_wall_ms=-1);self.assert_rejected()
    def test_nan_time_rejected(self):
        self.patch('R01/round-result.json',full_wall_ms=float('nan'));self.assert_rejected()
    def test_bool_time_rejected(self):
        self.patch('R01/round-result.json',full_wall_ms=True);self.assert_rejected()
    def test_error_cannot_be_ignored(self):
        self.patch('R01/round-result.json',error='API failed');self.assert_rejected()
    def test_empty_checks_rejected(self):
        self.patch('R01/grade-1.json',checks={});self.assert_rejected()
    def test_missing_visual_gate_rejected(self):
        c=dict.fromkeys(REQUIRED[1],True);c.pop('vision_result')
        self.patch('R01/grade-1.json',checks=c);self.assert_rejected()
    def test_failed_grade_rejected(self):
        self.patch('R01/grade-1.json',**{'pass':False});self.assert_rejected()
    def test_false_check_rejected(self):
        c=dict.fromkeys(REQUIRED[2],True);c['checkpoint_hash_chain']=False
        self.patch('R01/grade-2.json',checks=c);self.assert_rejected()
    def test_false_like_string_rejected(self):
        c=dict.fromkeys(REQUIRED[1],True);c['actual_tool_calls']='PASS'
        self.patch('R01/grade-1.json',checks=c);self.assert_rejected()
    def test_run_identity_mismatch_rejected(self):
        self.patch('R01/run-1.json',run_id='run_elsewhere');self.assert_rejected()
    def test_incomplete_run_rejected(self):
        self.patch('R01/run-1.json',status='running');self.assert_rejected()
    def test_missing_session_rejected(self):
        self.patch('R01/run-1.json',session_id=None);self.assert_rejected()
    def test_same_session_is_not_cross_session_recovery(self):
        self.patch('R01/run-2.json',session_id='session_1_1');self.assert_rejected()
    def test_replay_not_observed_rejected(self):
        self.patch('R01/idempotency-1.json',replayed=False);self.assert_rejected()
    def test_request_model_alias_not_actual_runtime(self):
        self.patch('R01/run-1.json',model='DeepSeek-V4.1-Flash',runtime={});self.assert_rejected()
    def test_actual_model_change_rejected(self):
        self.patch('R01/run-1.json',runtime={'model':'different','provider':'openrouter'});self.assert_rejected()
    def test_actual_provider_change_rejected(self):
        self.patch('R01/run-1.json',runtime={'model':'deepseek/deepseek-v4.1-flash','provider':'different'});self.assert_rejected()
    def test_duplicate_run_across_rounds_rejected(self):
        for kind in ('ack','run','idempotency'):
            self.patch(f'R02/{kind}-1.json',run_id='run_1_1')
        self.assert_rejected()
    def test_one_round_not_five(self):
        r=inspect_batch(self.root,1);self.assertEqual(r['consecutive_pass'],1);self.assertFalse(r['five_round_contract_pass'])
    def test_invalid_round_range(self):
        for n in (0,6,-1,True):
            with self.subTest(n=n),self.assertRaises(ValueError):inspect_batch(self.root,n)
    def test_readonly_does_not_modify_receipts(self):
        def snapshot(): return {str(p.relative_to(self.root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.rglob('*') if p.is_file()}
        before=snapshot();inspect_batch(self.root);self.assertEqual(before,snapshot())
    def test_missing_all_data_unknown_not_pass(self):
        other=self.root/'empty';other.mkdir()
        r=inspect_batch(other);self.assertEqual(r['status'],'UNKNOWN_RECONCILE_FIRST');self.assertFalse(r['five_round_contract_pass'])

    def test_second_terminal_failure_not_whitelisted(self):
        ev=self.read_events(1,1)
        ev += [{'run_id':'run_1_1','event':'tool.started','tool':'terminal','preview':'other.cmd'},
               {'run_id':'run_1_1','event':'tool.completed','tool':'terminal','error':True}]
        self.write_events(1,1,ev);self.assert_rejected()
    def test_unrelated_first_terminal_error_rejected(self):
        ev=self.read_events(1,1);ev[0]['preview']='unrelated.cmd'
        self.write_events(1,1,ev);self.assert_rejected()
    def test_skipped_baseline_failure_rejected(self):
        ev=self.read_events(1,1);ev[1]['error']=False
        self.write_events(1,1,ev);self.assert_rejected()
    def test_vision_failure_not_whitelisted(self):
        ev=self.read_events(1,1)
        ev += [{'run_id':'run_1_1','event':'tool.started','tool':'vision_analyze','preview':'image'},
               {'run_id':'run_1_1','event':'tool.completed','tool':'vision_analyze','error':True}]
        self.write_events(1,1,ev);self.assert_rejected()
    def test_error_in_resume_phase_rejected(self):
        ev=self.read_events(1,2);ev[1]['error']=True
        self.write_events(1,2,ev);self.assert_rejected()
    def test_malformed_sse_rejected(self):
        (self.root/'R01/events-1.sse').write_text('data: {\n');self.assert_rejected()
    def test_mismatched_event_run_rejected(self):
        ev=self.read_events(1,1);ev[1]['run_id']='run_somebody_else'
        self.write_events(1,1,ev);self.assert_rejected()
    def test_missing_sse_is_unknown(self):
        (self.root/'R01/events-1.sse').unlink();self.assert_rejected()

if __name__ == '__main__': unittest.main(verbosity=2)
