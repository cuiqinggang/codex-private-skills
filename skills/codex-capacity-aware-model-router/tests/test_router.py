import importlib.util
import json
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "router.py"
if not MODULE_PATH.exists():
    MODULE_PATH = Path(__file__).resolve().parents[1] / "router.py"
SPEC = importlib.util.spec_from_file_location("capacity_router", MODULE_PATH)
router_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(router_module)


def models(*names):
    return [{"model": name, "priority": index, "is_default": index == 0,
             "supported_reasoning_levels": ["low", "medium"],
             "capability_class": "general"} for index, name in enumerate(names, 1)]


class RouterFaultInjection(unittest.TestCase):
    def setUp(self):
        workspace = Path(__file__).resolve().parents[1]
        self.root = workspace / ".router-test-state" / self._testMethodName
        self.root.mkdir(parents=True, exist_ok=True)
        if not self.root.resolve().is_relative_to(workspace):
            raise RuntimeError("test fixture escaped workspace")
        for relative in ("state/router-state.json", "state/model-health.json",
                         "state/checkpoint.json", "logs/route-events.jsonl"):
            (self.root / relative).unlink(missing_ok=True)
        self.policy = {"capacity_cooldown_seconds": 600,
                       "all_models_recheck_seconds": 300,
                       "probe_reasoning_effort": "low",
                       "preferred_models": [], "denied_models": [],
                       "min_capability_class": None}
        self.catalog = models("fixture_primary", "fixture_second", "fixture_third")
        self.answers = {}
        self.probe_calls = []
        self.now = 1000.0

        def discover():
            return list(self.catalog), {"model_discovery_source": "mock_live_model_list",
                                        "model_discovery_timestamp": "fixture_time",
                                        "model_candidate_count": len(self.catalog)}

        def probe(model, policy, neutral):
            self.probe_calls.append(model["model"])
            return self.answers.get(model["model"], "PASS")

        self.router = router_module.Router(self.root, self.policy, discover, probe,
                                           now=lambda: self.now)
        self.task = {"task_id": "H3-PAUSED", "workdir": str(self.root),
                     "branch": "fixture-branch", "last_remote_head": "fixture-head",
                     "completed_steps": ["GPU_DONE", "QC_DONE", "GIT_DONE"],
                     "do_not_repeat": ["GPU_DONE", "QC_DONE", "GIT_DONE"],
                     "next_action": "Return to GPT", "artifact_paths": ["fixture-report"]}

    def test_t1_primary_pass(self):
        result = self.router.route(self.task, "fixture_primary")
        self.assertEqual(result["router_state"], "PRIMARY_SELECTED")
        self.assertEqual(result["actual_model"], "fixture_primary")
        self.assertEqual(self.probe_calls, ["fixture_primary"])

    def test_t2_primary_capacity_second_pass(self):
        self.answers["fixture_primary"] = "CAPACITY"
        result = self.router.route(self.task, "fixture_primary")
        self.assertEqual(result["router_state"], "FALLBACK_SELECTED")
        self.assertEqual(result["actual_model"], "fixture_second")
        self.assertEqual(self.probe_calls, ["fixture_primary", "fixture_second"])
        self.assertEqual(router_module.classify_error("server_overloaded"), "CAPACITY")

    def test_t3_two_capacity_third_pass(self):
        self.answers.update({"fixture_primary": "CAPACITY", "fixture_second": "CAPACITY"})
        result = self.router.route(self.task, "fixture_primary")
        self.assertEqual(result["router_state"], "THIRD_SELECTED")
        self.assertEqual(result["actual_model"], "fixture_third")
        self.assertEqual(self.probe_calls, ["fixture_primary", "fixture_second", "fixture_third"])

    def test_t4_all_capacity_checkpoint_no_busy_loop(self):
        self.answers = {m["model"]: "CAPACITY" for m in self.catalog}
        result = self.router.route(self.task, "fixture_primary")
        self.assertEqual(result["router_state"], "ALL_MODELS_CAPACITY")
        self.assertEqual(result["task_state"], "CHECKPOINTED")
        self.assertFalse(result["local_work_replay"])
        self.assertEqual(result["next_health_check_epoch"], 1300.0)
        calls = list(self.probe_calls)
        again = self.router.route(self.task, "fixture_primary")
        self.assertEqual(again["router_state"], "ALL_MODELS_CAPACITY")
        self.assertEqual(self.probe_calls, calls)

    def test_t5_capacity_resume_preserves_completed_local_steps(self):
        task = {**self.task, "thread_id": "fixture-thread"}
        calls = []

        def remote_runner(cmd, cwd):
            calls.append(cmd)
            prompt = cmd[-1]
            self.assertIn("GPU_DONE", prompt)
            self.assertIn("QC_DONE", prompt)
            self.assertIn("GIT_DONE", prompt)
            self.assertIn('"LOCAL_WORK_REPLAY": "NO"', prompt)
            if len(calls) == 1:
                return 1, "Selected model is at capacity", ""
            return 0, json.dumps({"type": "thread.started", "thread_id": "fixture-thread"}), ""

        result = router_module.continue_task(self.router, task, "fixture_primary", remote_runner)
        self.assertEqual(result["task_state"], "CONTINUED")
        self.assertEqual(result["actual_model"], "fixture_second")
        self.assertEqual(len(calls), 2)
        checkpoint = router_module.read_json(self.router.checkpoint_path, {})
        self.assertEqual(checkpoint["completed_steps"], self.task["completed_steps"])
        self.assertEqual(checkpoint["do_not_repeat"], self.task["do_not_repeat"])
        self.assertFalse(checkpoint["local_work_replay"])

    def test_t6_route_event_required_fields(self):
        self.answers["fixture_primary"] = "CAPACITY"
        self.router.route(self.task, "fixture_primary")
        events = [json.loads(line) for line in self.router.events_path.read_text(encoding="utf-8").splitlines()]
        self.assertGreaterEqual(len(events), 2)
        for event in events:
            for field in ("REQUESTED_MODEL", "ACTUAL_MODEL", "FALLBACK_REASON",
                          "ERROR_CLASS", "PROBE_RESULT", "TIMESTAMP"):
                self.assertIn(field, event)
        self.assertEqual(events[-1]["ACTUAL_MODEL"], "fixture_second")

    def test_t7_refresh_discovers_new_model_without_code_change(self):
        self.router.route(self.task, "fixture_primary")
        self.catalog.append({"model": "fixture_newly_added", "priority": 4,
                             "is_default": False, "supported_reasoning_levels": ["low"],
                             "capability_class": "general"})
        result = self.router.route(self.task, "fixture_newly_added")
        self.assertEqual(result["actual_model"], "fixture_newly_added")
        self.assertEqual(result["model_discovery"]["model_candidate_count"], 4)
        self.assertEqual(self.probe_calls[-1], "fixture_newly_added")


if __name__ == "__main__":
    unittest.main()
