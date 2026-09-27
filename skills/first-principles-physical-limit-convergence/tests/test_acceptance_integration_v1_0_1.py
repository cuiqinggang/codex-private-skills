import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'runtime'))
from acceptance_supervisor_v5_3_3 import acceptance_result, acceptance_wait
from acceptance_review_v1_0_1 import STAGES, PASS_GATES

EXPECTED = dict(task_id='test-task-02', timeline_id='test-timeline-02', run_id='run-02', conversation_id='test-conversation-02')
SESSION = dict(control_context='daily-profile', test_context='dedicated-profile',
               control_conversation='control-conversation', test_conversation=EXPECTED['conversation_id'],
               control_title='极限短时间 v5.3.3冒烟 R2', test_title='极限短时间 v5.3.3冒烟 R2｜独立测试02', creation_verified=True)
def valid():
    e = dict(EXPECTED, session=copy.deepcopy(SESSION), provenance_disputed=False, reported_human_count=0)
    e['events'] = [dict(EXPECTED, verified=True, source_kind='TOOL_TRACE', evidence_ref='synthetic:'+stage,
                        actor='AUTOMATION', purpose='TRANSFER' if stage!='BUSINESS_EXECUTION' else 'EXECUTION',
                        within_loop=True, stage=stage) for stage in sorted(STAGES)]
    e.update({key: True for key in PASS_GATES})
    return e

def call(e=None,r='PASS',f='NONE'):
    return acceptance_result(r, f, expected=EXPECTED, evidence=e)

def hold(test, value):
    test.assertFalse(value.startswith('FSM_'),value)
    test.assertNotIn('SUPERVISOR_RECOVER',value)
    test.assertNotIn('CONFIRMED_HUMAN',value)

class EntryIntegration(unittest.TestCase):
    def test_01_legacy_bare_fail_cannot_reach_recovery(self):
        hold(self, acceptance_result('FAIL','TRANSPORT'))
    def test_02_legacy_bare_pass_cannot_finalize(self):
        hold(self, acceptance_result('PASS','NONE'))
    def test_03_old_report_of_one_without_action_not_fail(self):
        e=valid();e['reported_human_count']=1;e['events']=[]
        hold(self,call(e,'FAIL','MANUAL_HANDOFF'))
    def test_04_auto_input_full_chain_passes(self):
        self.assertEqual(call(valid()),'FSM_PASS_TO_FINAL_VALID')
    def test_05_actual_human_takeover_detected(self):
        e=valid();e['events'].append(dict(e['events'][0],actor='HUMAN',source_kind='ATTRIBUTABLE_ACTION_RECORD',evidence_ref='synthetic:human'))
        self.assertEqual(call(e),'ACCEPTANCE_FAIL_CONFIRMED_HUMAN_NO_PRODUCT_CHANGE')
    def test_06_dispute_blocks_circular_report_proof(self):
        e=valid();e['provenance_disputed']=True
        hold(self,call(e,'FAIL','MANUAL_HANDOFF'))
    def test_07_other_task_events_never_count(self):
        e=valid();e['events'][0]['task_id']='other';e['events'][0]['actor']='HUMAN'
        hold(self,call(e))
    def test_08_other_timeline_rejected(self):
        e=valid();e['timeline_id']='old';hold(self,call(e))
    def test_09_old_conversation_reuse_rejected(self):
        e=valid();e['session']['test_conversation']=e['session']['control_conversation'];hold(self,call(e))
    def test_10_title_rename_is_not_new_identity(self):
        e=valid();e['session']['creation_verified']=False;hold(self,call(e))
    def test_11_different_context_without_full_chain_not_pass(self):
        e=valid();e['events']=[];hold(self,call(e))
    def test_12_same_action_displayed_twice_deduplicates(self):
        e=valid();e['events'].append(dict(e['events'][0]));self.assertEqual(call(e),'FSM_PASS_TO_FINAL_VALID')
    def test_13_conflicting_actor_for_same_event_held(self):
        e=valid();e['events'].append(dict(e['events'][0],actor='HUMAN'));hold(self,call(e))
    def test_14_user_role_is_not_manual_evidence(self):
        e=valid();e['events'][0].update(actor='HUMAN',source_kind='MESSAGE_ROLE');hold(self,call(e))
    def test_15_missing_individual_final_gates_all_held(self):
        for key in PASS_GATES:
            with self.subTest(key=key):
                e=valid();e[key]=False;hold(self,call(e))
    def test_16_display_events_cannot_fake_auto_coverage(self):
        e=valid();e['events'][0]['purpose']='DISPLAY_ONLY';hold(self,call(e))
    def test_17_normal_predefined_initial_request_not_takeover(self):
        e=valid();e['events'].append(dict(e['events'][0],actor='HUMAN',source_kind='EXPLICIT_OPERATOR_STATEMENT',evidence_ref='synthetic:entry',purpose='TASK_SUBMISSION',within_loop=False,permitted_entry=True))
        self.assertEqual(call(e),'FSM_PASS_TO_FINAL_VALID')
    def test_18_inloop_initial_request_cannot_be_exempted(self):
        e=valid();e['events'][0].update(actor='HUMAN',purpose='TASK_SUBMISSION',permitted_entry=True);hold(self,call(e))
    def test_19_timeout_is_not_failed_send(self):
        e=valid();e.update(failure_verified=True,failure_evidence_ref='synthetic:timeout',failure_basis='TIMEOUT_ONLY');hold(self,call(e,'FAIL','TRANSPORT'))
    def test_20_late_matching_ack_prevents_resend(self):
        o=dict(EXPECTED,evidence_ref='synthetic:ack',matching_ack_verified=True,timeout=True)
        self.assertEqual(acceptance_wait(expected=EXPECTED,observation=o),'DELIVERED_DO_NOT_RESEND')
    def test_21_progress_prevents_interruption(self):
        o=dict(EXPECTED,evidence_ref='synthetic:progress',progress_verified=True,timeout=True)
        self.assertEqual(acceptance_wait(expected=EXPECTED,observation=o),'IN_PROGRESS_DO_NOT_INTERRUPT')
    def test_22_wrong_conversation_ack_not_accepted(self):
        o=dict(EXPECTED,evidence_ref='synthetic:ack',matching_ack_verified=True,conversation_id='old')
        self.assertEqual(acceptance_wait(expected=EXPECTED,observation=o),'CHECK_STATE_DO_NOT_AUTO_FAIL_OR_RESEND')
    def test_23_verified_product_failure_preserved(self):
        e=valid();e.update(failure_verified=True,failure_evidence_ref='synthetic:bad-file',failure_basis='HASH_MISMATCH')
        self.assertEqual(call(e,'FAIL','PRODUCT'),'FSM_FAIL_TO_VIRTUAL_REMATURE_REFREEZE')
    def test_24_boolean_report_count_not_integer_one(self):
        e=valid();e['reported_human_count']=True;hold(self,call(e))
    def test_25_automatic_claim_does_not_override_human_record(self):
        e=valid();e['events'][0].update(actor='HUMAN',source_kind='ATTRIBUTABLE_ACTION_RECORD')
        self.assertEqual(call(e),'ACCEPTANCE_FAIL_CONFIRMED_HUMAN_NO_PRODUCT_CHANGE')
    def test_26_verified_string_is_not_true(self):
        e=valid();e['events'][0]['verified']='true';hold(self,call(e))
    def test_27_no_expected_binding_is_held(self):
        hold(self,acceptance_result('PASS','NONE',evidence=valid()))
    def test_28_session_and_report_conversations_must_match(self):
        e=valid();e['session']['test_conversation']='some-other-new';hold(self,call(e))

if __name__=='__main__':
    unittest.main(verbosity=2)
