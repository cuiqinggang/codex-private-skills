"""Offline regressions for scripts/run.py; no credentials or verifier API."""

import importlib.util
import io
from pathlib import Path
import shutil
import sys
from contextlib import redirect_stdout
from types import SimpleNamespace
import unittest
from unittest import mock
from uuid import uuid4


ROOT = Path(__file__).resolve().parents[1]
with mock.patch.object(sys, "path", [str(ROOT), *sys.path]):
    from llm_verifier import fine_grained_reward as reward

    # run.py loads .env at import time. Suppress that before importing it.
    with mock.patch.object(reward, "load_dotenv"):
        spec = importlib.util.spec_from_file_location(
            "run_report_offline", ROOT / "scripts" / "run.py")
        run = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(run)


class ReportTests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        # Use inherited directory permissions in restricted Windows sandboxes.
        self.root = (Path(__file__).resolve().parent /
                     f"t03-offline-{uuid4().hex}")
        self.root.mkdir()
        self.addCleanup(self.remove_test_directory)
        self.cfg = SimpleNamespace(
            name="Offline benchmark",
            results="results/default.txt",
            cache="cache/scores.json",
            loader="offline",
            data={},
            prompts="unused",
            criteria=["correctness"],
            n_evaluations=4,
            pivots=2,
            seed=7,
            max_workers=1,
        )
        self.metrics = dict(
            n_tasks=6, n_runs=3, n_swing=3,
            criteria_ids=["correctness"], n_reps=4, k=2, seed=7,
            pass1=2.5, verifier=4, oracle=5, avg_cmp=5.25,
            usage=reward.TokenUsage(), comparisons=15,
        )
        self.metrics["usage"].add(
            input_tokens=1200, cached_input_tokens=300,
            output_tokens=80, reasoning_tokens=20, calls=2)
        root_patch = mock.patch.object(run, "ROOT_DIR", str(self.root))
        root_patch.start()
        self.addCleanup(root_patch.stop)
        # Any accidental credential loading or client access fails offline.
        for name in ("load_dotenv", "create_client", "create_gemini_client",
                     "create_openai_client", "create_deepseek_client"):
            guard = mock.patch.object(
                reward, name, side_effect=AssertionError(
                    "credentials and verifier clients are forbidden"))
            guard.start()
            self.addCleanup(guard.stop)
        lazy_guard = mock.patch.object(
            reward.LazyClient, "get",
            side_effect=AssertionError("real verifier access is forbidden"))
        lazy_guard.start()
        self.addCleanup(lazy_guard.stop)

    def remove_test_directory(self):
        self.root.resolve().relative_to(Path(__file__).resolve().parent)
        shutil.rmtree(self.root)

    def render(self, metrics=None, **kwargs):
        output = io.StringIO()
        with redirect_stdout(output):
            run.report(self.cfg, **(self.metrics if metrics is None else metrics),
                       **kwargs)
        return output.getvalue()

    def assert_saved_report(self, stdout, path):
        text = path.read_text()
        # print adds one newline; the final save acknowledgement is stdout-only.
        body, marker, saved_path = stdout.rpartition("Results saved: ")
        self.assertEqual(marker, "Results saved: ")
        self.assertEqual(body, text + "\n")
        self.assertEqual(Path(saved_path.rstrip("\n")), path)
        return text

    def test_empty_report_saves_all_unavailable_rates(self):
        metrics = dict(
            self.metrics, n_tasks=0, n_swing=0, pass1=0,
            verifier=0, oracle=0, avg_cmp=0, comparisons=0,
            usage=reward.TokenUsage())
        stdout = self.render(metrics)
        text = self.assert_saved_report(
            stdout, self.root / "results" / "default.txt")
        self.assertIn(
            "  tasks=0  swing=0  N(trials)=3  comparisons/task=0.0\n", text)
        self.assertEqual(text.splitlines()[8:11], [
            "Pass@1                          0.00/0       --",
            "LLM-as-a-Verifier                  0/0       --",
            "Oracle (Bo3)                       0/0       --",
        ])
        self.assertIn("Verifier tokens (0 verifier calls)", text)

    def test_nonempty_report_preserves_complete_format_and_values(self):
        stdout = self.render()
        text = self.assert_saved_report(
            stdout, self.root / "results" / "default.txt")
        self.assertEqual(text, "\n".join([
            "",
            "=" * 72,
            "Offline benchmark",
            "  g20  criteria=['correctness']  K=4  pivots=2  seed=7",
            "  tasks=6  swing=3  N(trials)=3  comparisons/task=5.2",
            "=" * 72,
            "Method                               Score     Rate",
            "-" * 72,
            "Pass@1                          2.50/6    41.7%",
            "LLM-as-a-Verifier                  4/6    66.7%",
            "Oracle (Bo3)                       5/6    83.3%",
            "-" * 72,
            "Verifier tokens (2 verifier calls)",
            "  input                                1,200",
            "    cached input                         300  (25.0% hit rate)",
            "    uncached input                       900",
            "  output                                  80",
            "    reasoning                             20",
            "",
        ]))

    def test_nonempty_zero_and_full_rates(self):
        stdout = self.render(dict(
            self.metrics, n_tasks=1, n_swing=1,
            pass1=0.5, verifier=0, oracle=1))
        text = self.assert_saved_report(
            stdout, self.root / "results" / "default.txt")
        self.assertEqual(text.splitlines()[8:11], [
            "Pass@1                          0.50/1    50.0%",
            "LLM-as-a-Verifier                  0/1     0.0%",
            "Oracle (Bo3)                       1/1   100.0%",
        ])

    def test_results_file_overrides_config_for_relative_and_absolute_paths(self):
        for override in ("chosen/nested/report.txt",
                         str(self.root / "absolute" / "report.txt")):
            with self.subTest(results_file=override):
                stdout = self.render(results_file=override)
                path = Path(override)
                if not path.is_absolute():
                    path = self.root / path
                self.assert_saved_report(stdout, path)
                self.assertFalse((self.root / self.cfg.results).exists())

    def test_empty_benchmark_completes_phases_and_saves_requested_file(self):
        criteria = [{"id": "correctness"}]
        with mock.patch.object(run, "LOADERS", {
                "offline": mock.Mock(return_value=({}, 0))}), \
                mock.patch.object(run, "load_prompts", return_value=("", criteria)), \
                mock.patch.object(run, "select_criteria", return_value=criteria), \
                mock.patch.object(run, "score_directed_pairs", return_value={}) as scorer:
            progress = io.StringIO()
            with redirect_stdout(progress):
                result = run.run_benchmark(
                    self.cfg, results_file="chosen/empty.txt")
        self.assertEqual(scorer.call_count, 2)
        for call in scorer.call_args_list:
            self.assertEqual(call.args[1], {})
            self.assertEqual(call.args[2], {})
        self.assertIn("Phase A: ring pass", progress.getvalue())
        self.assertIn("Phase B: pivot rounds", progress.getvalue())
        self.assertEqual(result["n_tasks"], 0)
        self.assertEqual(result["results_file"], "chosen/empty.txt")
        stdout = self.render(result)
        text = self.assert_saved_report(stdout, self.root / "chosen" / "empty.txt")
        self.assertTrue(all(line.endswith("--") for line in text.splitlines()[8:11]))
        self.assertFalse((self.root / self.cfg.results).exists())


if __name__ == "__main__":
    unittest.main()