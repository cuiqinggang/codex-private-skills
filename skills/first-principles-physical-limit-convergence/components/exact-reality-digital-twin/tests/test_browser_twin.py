import hashlib
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


REALITY_WORKSPACE = Path(r"C:\\Users\\A\\playwright-browser-automation5-final-reality-competition-work")
COMPONENT_ROOT = Path(__file__).resolve().parents[1]
ENGINE = COMPONENT_ROOT / "ENGINE.py"
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


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class BrowserTwinAcceptance(unittest.TestCase):
    def run_mode(self, mode: str, output_dir: Path, *extra: str):
        command = [
            sys.executable,
            str(ENGINE),
            mode,
            "--workspace-root",
            str(REALITY_WORKSPACE),
            "--output-dir",
            str(output_dir),
            *extra,
        ]
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        return json.loads(completed.stdout)

    def setUp(self):
        self.output_dir = Path(__file__).parent / "_outputs" / self._testMethodName
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.assertEqual(self.output_dir.parent.name, "_outputs")
        shutil.rmtree(self.output_dir)

    def test_legacy_host_codex_selftest_remains_24_of_24(self):
        result = self.run_mode("selftest", self.output_dir)
        self.assertEqual(result["engine_version"], "1.3.0")
        self.assertEqual((result["passed"], result["case_count"]), (24, 24))
        self.assertEqual(result["virtual_contract_99"], "PASS")

    def test_browser_profile_validation_builds_required_reality_profile(self):
        result = self.run_mode("browser_validate", self.output_dir)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["profile_id"], "PLAYWRIGHT_GOLDEN_REALITY_PROFILE")
        self.assertEqual(result["critical_unknown_count"], 0)
        profile = json.loads((self.output_dir / "PLAYWRIGHT_GOLDEN_REALITY_PROFILE.json").read_text(encoding="utf-8"))
        self.assertEqual(profile["method_version"], "3.1.7")
        self.assertEqual(profile["twin_source_version"], "1.1.0")
        self.assertEqual(profile["browser_r3_fingerprint_sha256"], "9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd")
        self.assertEqual(profile["canonical_golden_sha256"], "1c67a634e0c0fc24ed057752358f4c20a6c05550be6146fd8d11b1a723f25e08")
        self.assertEqual(profile["golden_task"]["outcomes"], ["PASS", "PASS", "PASS"])
        self.assertEqual(profile["historical_t_star_real_ms"], 1525.09)
        self.assertNotIn("secret", json.dumps(profile, ensure_ascii=False).lower())

    def test_browser_replay_uses_frozen_order_and_reproduces_business_result(self):
        self.run_mode("browser_validate", self.output_dir)
        result = self.run_mode("browser_replay", self.output_dir)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual([entry["action"] for entry in result["action_sequence"]], EXPECTED_ACTIONS)
        self.assertTrue(all(entry["status"] == "PASS" for entry in result["action_sequence"]))
        self.assertEqual(result["persistent_reconnect"]["reconnect_1"], "PASS")
        self.assertEqual(result["persistent_reconnect"]["reconnect_2"], "PASS")
        self.assertEqual(result["business_result"], "PASS_3_OF_3")

    def test_browser_delta_has_no_unknown_or_material_delta(self):
        self.run_mode("browser_validate", self.output_dir)
        self.run_mode("browser_replay", self.output_dir)
        result = self.run_mode("browser_delta", self.output_dir)
        expected = {
            "SAME_TASK",
            "SAME_VALID",
            "SAME_BROWSER_PROCESS",
            "SAME_CONTEXT",
            "SAME_PROFILE",
            "SAME_ACTION_SEQUENCE",
            "SAME_DIALOG_BEHAVIOR",
            "SAME_ACTIONABILITY",
            "SAME_NETWORK_SEMANTICS",
            "SAME_RUNTIME_SEMANTICS",
            "SAME_RECONNECT_RESULT",
            "SAME_BUSINESS_RESULT",
        }
        self.assertEqual(set(result["comparisons"]), expected)
        self.assertTrue(all(value == "PASS" for value in result["comparisons"].values()))
        self.assertEqual(result["twin_critical_unknown_count"], 0)
        self.assertEqual(result["material_reality_twin_delta_count"], 0)
        self.assertEqual(result["same_critical_browser_behavior"], "PASS")

    def test_shadow_dialog_overlay_is_isolated_from_reality(self):
        self.run_mode("browser_validate", self.output_dir)
        profile_path = self.output_dir / "PLAYWRIGHT_GOLDEN_REALITY_PROFILE.json"
        before = digest(profile_path)
        overlay = self.output_dir / "overlay.json"
        overlay.write_text(json.dumps({"dialog_actionability": {"BEFORE_DIALOG": {"visible": False}}}), encoding="utf-8")
        result = self.run_mode("browser_shadow", self.output_dir, "--browser-overlay", str(overlay))
        self.assertEqual(result["shadow_delta_present"], "YES")
        self.assertEqual(result["reality_mutated"], "NO")
        self.assertIn("dialog_actionability.BEFORE_DIALOG.visible", result["changed_paths"])
        self.assertEqual(digest(profile_path), before)

    def test_replay_after_shadow_is_identical(self):
        self.run_mode("browser_validate", self.output_dir)
        before = self.run_mode("browser_replay", self.output_dir)
        overlay = self.output_dir / "overlay.json"
        overlay.write_text(json.dumps({"dialog_actionability": {"BEFORE_DIALOG": {"visible": False}}}), encoding="utf-8")
        self.run_mode("browser_shadow", self.output_dir, "--browser-overlay", str(overlay))
        overlay.unlink()
        after = self.run_mode("browser_replay", self.output_dir, "--after-shadow")
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
