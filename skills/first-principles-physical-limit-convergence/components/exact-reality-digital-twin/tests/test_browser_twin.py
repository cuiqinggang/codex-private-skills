import hashlib
import importlib.util
import json
import unittest
from pathlib import Path


COMPONENT_ROOT = Path(__file__).resolve().parents[1]
ENGINE_PATH = COMPONENT_ROOT / "ENGINE.py"
EVIDENCE_DIR = COMPONENT_ROOT / "reality-profiles" / "playwright-golden"

EXPECTED_BROWSER_FINGERPRINT = "9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd"
EXPECTED_GOLDEN_SHA256 = "1c67a634e0c0fc24ed057752358f4c20a6c05550be6146fd8d11b1a723f25e08"
EXPECTED_PROFILE_CANONICAL_SHA256 = "f18c1e2f8668132e936c3acebd8b2b22a0a8928363561d13752944e406db65ff"

EXPECTED_ACTIONS = [
    "TASK_IDENTITY",
    "VALID_IDENTITY",
    "BROWSER_PROCESS_IDENTITY",
    "CONTEXT_IDENTITY",
    "PROFILE_IDENTITY",
    "PAGE_FRAME_GRAPH",
    "NAVIGATION",
    "LOCATOR",
    "INPUT",
    "CLICK",
    "EXTRACT",
    "KEYBOARD",
    "DRAG_DROP",
    "UPLOAD",
    "DOWNLOAD",
    "BEFORE_DIALOG_ACTIONABILITY",
    "DIALOG_OPENING",
    "DIALOG_ACCEPT",
    "AFTER_DIALOG_ACTIONABILITY",
    "POPUP",
    "FRAME",
    "ROUTE_API",
    "ISOLATED_CONTEXT",
    "SCREENSHOT",
    "PERSISTENT_RECONNECT_1",
    "PERSISTENT_RECONNECT_2",
    "FINAL_GOLDEN_RESULT",
]


def read_json(name: str):
    return json.loads((EVIDENCE_DIR / name).read_text(encoding="utf-8"))


def canonical_hash(value) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_engine():
    spec = importlib.util.spec_from_file_location("formal_exact_reality_digital_twin", ENGINE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class BrowserTwinAcceptance(unittest.TestCase):
    def test_legacy_host_codex_selftest_remains_24_of_24(self):
        engine = load_engine()
        result = engine.run_selftest()
        self.assertEqual(engine.VERSION, "1.3.0")
        self.assertEqual(result["engine_version"], "1.3.0")
        self.assertEqual((result["passed"], result["case_count"]), (24, 24))
        self.assertEqual(result["virtual_contract_99"], "PASS")

    def test_frozen_reality_profile_is_valid_and_complete(self):
        validation = read_json("BROWSER-PROFILE-VALIDATION.json")
        profile = read_json("PLAYWRIGHT_GOLDEN_REALITY_PROFILE.json")

        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["profile_id"], "PLAYWRIGHT_GOLDEN_REALITY_PROFILE")
        self.assertEqual(validation["critical_unknown_count"], 0)
        self.assertTrue(all(validation["input_gate"].values()))
        self.assertEqual(validation["profile_sha256"], EXPECTED_PROFILE_CANONICAL_SHA256)
        self.assertEqual(canonical_hash(profile), EXPECTED_PROFILE_CANONICAL_SHA256)

        self.assertEqual(profile["method_version"], "3.1.7")
        self.assertEqual(profile["twin_source_version"], "1.1.0")
        self.assertEqual(profile["browser_r3_fingerprint_sha256"], EXPECTED_BROWSER_FINGERPRINT)
        self.assertEqual(profile["canonical_golden_sha256"], EXPECTED_GOLDEN_SHA256)
        self.assertEqual(profile["golden_task"]["outcomes"], ["PASS", "PASS", "PASS"])
        self.assertEqual(profile["historical_t_star_real_ms"], 1525.09)
        self.assertNotIn("secret", json.dumps(profile, ensure_ascii=False).lower())

    def test_frozen_browser_replay_reproduces_business_result(self):
        replay = read_json("BROWSER-REALITY-REPLAY.json")

        self.assertEqual(replay["status"], "PASS")
        self.assertEqual(replay["profile_id"], "PLAYWRIGHT_GOLDEN_REALITY_PROFILE")
        self.assertEqual([entry["action"] for entry in replay["action_sequence"]], EXPECTED_ACTIONS)
        self.assertTrue(all(entry["status"] == "PASS" for entry in replay["action_sequence"]))
        self.assertEqual(replay["persistent_reconnect"]["reconnect_1"], "PASS")
        self.assertEqual(replay["persistent_reconnect"]["reconnect_2"], "PASS")
        self.assertEqual(replay["business_result"], "PASS_3_OF_3")
        self.assertEqual(replay["twin_critical_unknown_count"], 0)

    def test_frozen_browser_delta_has_zero_material_delta(self):
        delta = read_json("BROWSER-REALITY-TWIN-DELTA.json")

        self.assertEqual(delta["status"], "PASS")
        self.assertTrue(all(value == "PASS" for value in delta["comparisons"].values()))
        self.assertEqual(delta["twin_critical_unknown_count"], 0)
        self.assertEqual(delta["material_reality_twin_delta_count"], 0)
        self.assertEqual(delta["same_critical_browser_behavior"], "PASS")
        self.assertEqual(delta["reality_delta"], "NONE")

    def test_frozen_shadow_is_isolated_from_reality(self):
        shadow = read_json("BROWSER-SHADOW-ISOLATION.json")

        self.assertEqual(shadow["status"], "PASS")
        self.assertEqual(shadow["mode"], "HYPOTHETICAL_SHADOW")
        self.assertEqual(shadow["shadow_delta_present"], "YES")
        self.assertEqual(shadow["reality_mutated"], "NO")
        self.assertEqual(shadow["reality_profile_sha256_before"], shadow["reality_profile_sha256_after"])
        self.assertIn("dialog_actionability.BEFORE_DIALOG.visible", shadow["changed_paths"])

    def test_replay_after_shadow_is_identical(self):
        before = read_json("BROWSER-REALITY-REPLAY.json")
        after = read_json("BROWSER-REALITY-REPLAY-AFTER-SHADOW.json")
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
