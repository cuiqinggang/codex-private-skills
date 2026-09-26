"""CPU fixtures only: never load a model or access the user's C drive."""
import ast
import copy
import hashlib
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "ASSET-RECOVERY.py"
NS = {"__name__": "h3_recovery_fixture"}
exec(compile(SOURCE.read_text(encoding="utf-8"), str(SOURCE), "exec"), NS)

class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.assets = self.root / "inputs"
        self.assets.mkdir()
        for key, _, kind, _ in NS["ASSETS"]:
            (self.assets/key).write_bytes(b'{"1":{"class_type":"SaveVideo","inputs":{}}}' if kind == "json" else b"non-secret fixture source\n")

    def tearDown(self):
        self.tmp.cleanup()

    def inspect(self, raw, kind="text", expected=None):
        (self.assets/"x").write_bytes(raw)
        return NS["inspect_asset"](("x", "fixture-only", kind, expected), self.assets)

    def test_01_nine_exact_inputs(self):
        self.assertEqual(len(NS["ASSETS"]), 9)
        self.assertEqual(len({x[0] for x in NS["ASSETS"]}), 9)

    def test_02_read_and_hash(self):
        data = b"valid text"
        row = self.inspect(data)
        self.assertEqual(row["status"], "READ_OK")
        self.assertEqual(row["sha256"], hashlib.sha256(data).hexdigest())

    def test_03_expected_hash_match(self):
        data = b"same"
        self.assertEqual(self.inspect(data, expected=hashlib.sha256(data).hexdigest())["status"], "READ_OK")

    def test_04_expected_hash_mismatch_recorded(self):
        self.assertEqual(self.inspect(b"changed", expected="0"*64)["status"], "HASH_MISMATCH")

    def test_05_missing_is_not_ready(self):
        r = NS["inspect_asset"](("absent", "fixture-only", "text", None), self.assets)
        self.assertEqual(r["status"], "MISSING")

    def test_06_empty(self):
        self.assertEqual(self.inspect(b"")["status"], "EMPTY")

    def test_07_invalid_json(self):
        self.assertEqual(self.inspect(b"{oops", "json")["status"], "INVALID_JSON")

    def test_08_bom_json(self):
        r = self.inspect(b'\xef\xbb\xbf{"2":{"class_type":"AudioNode"}}', "json")
        self.assertEqual(r["status"], "READ_OK")
        self.assertEqual(r["node_classes"], ["AudioNode"])

    def test_09_bad_utf8(self):
        self.assertEqual(self.inspect(b"\xff\xfe\xff")["status"], "INVALID_UTF8")

    def test_10_size_guard(self):
        with patch.dict(NS, MAX_TEXT_BYTES=8):
            self.assertEqual(self.inspect(b"123456789")["status"], "TOO_LARGE")

    def test_11_secret_omitted(self):
        r = self.inspect(b"sk-"+b"X"*24)
        self.assertEqual(r["status"], "POTENTIAL_SECRET_CONTENT_OMITTED")
        self.assertNotIn("content", r)

    def test_12_model_metadata_does_not_read(self):
        with patch.object(Path, "open", side_effect=AssertionError("no model read allowed")):
            r = NS["inspect_asset"](NS["ASSETS"][5], self.assets)
        self.assertEqual(r["status"], "PRESENT_METADATA_ONLY")
        self.assertNotIn("sha256", r)
        self.assertFalse(r["content_verified"])

    def test_13_directory_refused(self):
        (self.assets/"dir").mkdir()
        r = NS["inspect_asset"](("dir", "fixture-only", "text", None), self.assets)
        self.assertEqual(r["status"], "NOT_REGULAR_FILE")

    def test_14_permission_error(self):
        with patch.object(Path, "open", side_effect=PermissionError("injected")):
            r = NS["inspect_asset"](NS["ASSETS"][0], self.assets)
        self.assertEqual(r["status"], "ACCESS_DENIED")

    def test_15_no_overwrite_and_sources_unchanged(self):
        before = {x.name: x.read_bytes() for x in self.assets.iterdir()}
        out = self.root/"out"
        receipt = NS["recover"](out, self.assets)
        with self.assertRaises(FileExistsError):
            NS["recover"](out, self.assets)
        self.assertEqual(before, {x.name: x.read_bytes() for x in self.assets.iterdir()})
        self.assertEqual(receipt["context"], "GPT_FIXTURE")
        self.assertIsNone(receipt["p1_t_valid_ms"])
        self.assertGreater(receipt["real_end_ns"], receipt["real_start_ns"])
        self.assertEqual(receipt["snapshot_sha256"], hashlib.sha256((out/"ASSET-SNAPSHOT.json").read_bytes()).hexdigest())

    def test_16_verifier_attacks(self):
        out = self.root/"out"
        NS["recover"](out, self.assets)
        original = json.loads((out/"ASSET-SNAPSHOT.json").read_bytes())
        self.assertTrue(NS["run_verifier"](original))
        for key, value in (("version", "9.0.0"), ("scope", "P1_GENERATION_PASS"), ("p1_virtual_complete", True), ("p1_real_generation_runs", 1), ("p1_real_generation_runs", False), ("p1_t_valid_ms", 1.0), ("context", "UNKNOWN")):
            with self.subTest(key=key, value=value):
                bad = copy.deepcopy(original); bad[key] = value
                self.assertFalse(NS["run_verifier"](bad))
        bad = copy.deepcopy(original); bad["assets"][0]["content"] += "tampered"
        self.assertFalse(NS["run_verifier"](bad))
        bad = copy.deepcopy(original); bad["assets"].reverse()
        self.assertFalse(NS["run_verifier"](bad))

    def test_17_write_failure_not_pass(self):
        with patch.object(Path, "mkdir", side_effect=PermissionError("injected")):
            with self.assertRaises(PermissionError):
                NS["recover"](self.root/"out", self.assets)

    def test_18_real_target_guard(self):
        with patch.object(NS["os"], "name", "posix"):
            with self.assertRaisesRegex(RuntimeError, "WINDOWS_TARGET_REQUIRED"):
                NS["run_reality"]()

    def test_19_fresh_namespace_entrypoints(self):
        clean = {"__name__": "fixture"}
        exec(compile(SOURCE.read_text(encoding="utf-8"), "immutable-capsule", "exec"), clean)
        self.assertTrue(callable(clean["run_reality"]))
        self.assertTrue(callable(clean["run_verifier"]))

    def test_20_no_network_process_or_recursive_scan(self):
        tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
        forbidden_modules = {"subprocess", "socket", "urllib", "requests", "http", "torch", "shutil"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                self.assertFalse(any(a.name.split(".")[0] in forbidden_modules for a in node.names))
            if isinstance(node, ast.ImportFrom):
                self.assertNotIn((node.module or "").split(".")[0], forbidden_modules)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                self.assertNotIn(node.func.attr, {"rglob", "glob", "walk", "unlink", "remove", "rmdir", "system", "popen"})

if __name__ == "__main__":
    start_utc, start_ns = NS["stamp"](), time.perf_counter_ns()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RecoveryTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    end_ns = time.perf_counter_ns()
    report = {"version": "1.0.0", "scope": "ASSET_RECOVERY_CPU_FIXTURES_ONLY", "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "passed": result.wasSuccessful(), "start_utc": start_utc, "end_utc": NS["stamp"](), "start_ns": start_ns, "end_ns": end_ns, "elapsed_ms": (end_ns-start_ns)/1e6, "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(), "tests_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "windows_target_tested": False, "gpu_calls": 0, "paid_api_calls": 0, "p1_generation_certified": False, "p1_virtual_complete": False, "p1_t_valid_ms": None}
    (ROOT/"GPT-SELFTEST-RESULT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    raise SystemExit(0 if result.wasSuccessful() else 1)
