import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
from acceptance_isolation_guard_v1 import classify_event, review_claim, isolation_gate, wait_gate

AUTO = dict(verified=True, source_kind="TOOL_TRACE", evidence_ref="fixture:send1",
            actor="AUTOMATION", purpose="TRANSFER", within_loop=True)
HUMAN = dict(AUTO, source_kind="ATTRIBUTABLE_ACTION_RECORD", actor="HUMAN")
SESSION = dict(control_context="daily", test_context="native", control_conversation="old",
               test_conversation="new", control_title="讨论页", test_title="独立测试页",
               creation_verified=True)

class Tests(unittest.TestCase):
    def test_01_bare_count_is_not_proof(self):
        self.assertEqual(review_claim(1, []), "REVIEW_UNSUPPORTED_MANUAL_CLAIM")
    def test_02_automatic_paste_not_human(self):
        self.assertEqual(classify_event(AUTO), "NOT_INTERVENTION")
    def test_03_user_role_is_not_actor_proof(self):
        self.assertEqual(classify_event(dict(HUMAN, source_kind="MESSAGE_ROLE")), "UNVERIFIED")
    def test_04_model_summary_is_not_actor_proof(self):
        self.assertEqual(classify_event(dict(HUMAN, source_kind="MODEL_SUMMARY")), "UNVERIFIED")
    def test_05_actual_human_event_is_not_waived(self):
        self.assertEqual(review_claim(1, [HUMAN]), "MANUAL_FAILURE_SUPPORTED")
    def test_06_user_dispute_requires_review(self):
        self.assertEqual(review_claim(1, [dict(HUMAN, disputed=True)]), "REVIEW_CONFLICT")
    def test_07_initial_request_is_not_in_loop_takeover(self):
        e = dict(HUMAN, purpose="TASK_SUBMISSION", within_loop=False, permitted_entry=True)
        self.assertEqual(classify_event(e), "NOT_INTERVENTION")
    def test_08_in_loop_relay_not_relabelled_as_initial(self):
        self.assertEqual(classify_event(dict(HUMAN, purpose="TASK_SUBMISSION")), "UNVERIFIED")
    def test_09_two_displays_do_not_duplicate_action(self):
        self.assertEqual(review_claim(1, [HUMAN, dict(HUMAN)]), "MANUAL_FAILURE_SUPPORTED")
    def test_10_ambiguous_duplicate_requires_review(self):
        self.assertEqual(review_claim(1, [AUTO, HUMAN]), "REVIEW_CONFLICT")
    def test_11_new_isolated_session_passes_only_isolation(self):
        self.assertEqual(isolation_gate(**SESSION), "ISOLATION_PASS_NOT_ACTOR_PROOF")
    def test_12_other_browser_same_conversation_rejected(self):
        self.assertEqual(isolation_gate(**dict(SESSION, test_conversation="old")), "REJECT_REUSED_CONVERSATION")
    def test_13_same_context_rejected(self):
        self.assertEqual(isolation_gate(**dict(SESSION, test_context="daily")), "REJECT_SHARED_BROWSER_CONTEXT")
    def test_14_rename_alone_not_new_conversation(self):
        self.assertEqual(isolation_gate(**dict(SESSION, test_conversation="old", test_title="另一个标题")), "REJECT_REUSED_CONVERSATION")
    def test_15_same_title_rejected_for_this_test(self):
        self.assertEqual(isolation_gate(**dict(SESSION, test_title="讨论页")), "REJECT_AMBIGUOUS_TITLE")
    def test_16_new_tab_without_identity_not_ready(self):
        self.assertEqual(isolation_gate(**dict(SESSION, test_conversation="")), "REVIEW_MISSING_IDENTITY")
    def test_17_bare_new_page_claim_not_verified(self):
        self.assertEqual(isolation_gate(**dict(SESSION, creation_verified=False)), "REVIEW_NEW_CONVERSATION_NOT_VERIFIED")
    def test_18_timeout_then_ack_is_delivered(self):
        self.assertEqual(wait_gate(matching_ack_verified=True, progress_verified=False, timeout=True), "DELIVERED_DO_NOT_RESEND")
    def test_19_progress_after_threshold_is_not_failure(self):
        self.assertEqual(wait_gate(matching_ack_verified=False, progress_verified=True, timeout=True), "IN_PROGRESS_DO_NOT_INTERRUPT")
    def test_20_timeout_without_state_requires_check(self):
        self.assertEqual(wait_gate(matching_ack_verified=False, progress_verified=False, timeout=True), "CHECK_STATE_DO_NOT_AUTO_FAIL_OR_RESEND")
    def test_21_absence_not_full_zero_certificate(self):
        self.assertEqual(review_claim(0, []), "NO_CONFIRMED_EVENT_NOT_ZERO_CERTIFICATION")
    def test_22_missing_ref_not_human_proof(self):
        self.assertEqual(classify_event(dict(HUMAN, evidence_ref="")), "UNVERIFIED")

if __name__ == "__main__":
    unittest.main(verbosity=2)
