"""T01 response-parsing regressions; standard library and mock clients only."""

import importlib.util
import math
from pathlib import Path
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch


MODULE_PATH = (Path(__file__).resolve().parent.parent
               / "llm_verifier" / "fine_grained_reward.py")
SPEC = importlib.util.spec_from_file_location("t01_reward", MODULE_PATH)
reward = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reward)


def position(token, probabilities=None):
    return NS(token=token, logprob=math.log(0.6), top_logprobs=[
        NS(token=letter, logprob=math.log(probability))
        for letter, probability in (probabilities or [])
    ])


def response(content=None, positions=None, **message_fields):
    return NS(choices=[NS(
        message=NS(content=content, **message_fields),
        logprobs=NS(content=positions) if positions is not None else None,
    )])


def client_for(*responses):
    create = Mock(side_effect=responses)
    return NS(chat=NS(completions=NS(create=create)))


class ResponseParsingTests(unittest.TestCase):
    def setUp(self):
        # Fail closed if a regression tries to discover credentials or connect.
        for target in ("load_dotenv", "create_client", "create_openai_client"):
            guard = patch.object(reward, target, side_effect=AssertionError(
                "offline tests must not load credentials or create clients"))
            guard.start()
            self.addCleanup(guard.stop)
        for target in ("socket.socket", "socket.create_connection"):
            guard = patch(target, side_effect=AssertionError(
                "offline tests must not connect to a service"))
            guard.start()
            self.addCleanup(guard.stop)
        usage = patch.object(reward, "USAGE", reward.TokenUsage())
        usage.start()
        self.addCleanup(usage.stop)

    def call(self, client, prompt="Analyze this result."):
        return reward.call_openai(client, prompt, model="offline-model")

    def test_content_takes_priority_and_preserves_distribution(self):
        positions = [position("<score_A>"),
                     position("B", [("A", 0.8), ("T", 0.2)]),
                     position("</score_A>")]
        client = client_for(response(
            "<score_A>B</score_A>", positions,
            reasoning="<score_A>T</score_A>",
            reasoning_content="<score_A>T</score_A>"))
        text, tokens, logprobs = self.call(client)
        self.assertEqual(text, "<score_A>B</score_A>")
        self.assertEqual(tokens, [pos.token for pos in positions])
        self.assertEqual(logprobs[1], [("A", math.log(0.8)),
                                      ("T", math.log(0.2))])
        self.assertAlmostEqual(reward.extract_score(
            text, tokens, logprobs, "<score_A>"), 0.8)
        client.chat.completions.create.assert_called_once()

    def test_reasoning_fields_supply_initial_text(self):
        for field in ("reasoning", "reasoning_content"):
            for empty_content in (None, ""):
                with self.subTest(field=field, content=empty_content):
                    client = client_for(response(
                        empty_content, **{field: "<score_A>B</score_A>"}))
                    text, tokens, logprobs = self.call(client)
                    self.assertEqual(text, "<score_A>B</score_A>")
                    self.assertIsNone(tokens)
                    self.assertIsNone(logprobs)
                    self.assertAlmostEqual(reward.extract_score(
                        text, tokens, logprobs, "<score_A>"), 18 / 19)

    def test_logprobs_only_reconstructs_initial_text_and_split_tokens(self):
        positions = [position("<score"), position("_A>"),
                     position(" B", [("A", 0.7), ("T", 0.3)]),
                     position("</score_A>")]
        client = client_for(response("", positions))
        text, tokens, logprobs = self.call(client)
        self.assertEqual(text, "<score_A> B</score_A>")
        self.assertEqual(tokens, [pos.token for pos in positions])
        self.assertAlmostEqual(reward.extract_score(
            text, tokens, logprobs, "<score_A>"), 0.7)

    def test_prefill_sources_preserve_letters_and_real_distributions(self):
        for field in ("content", "reasoning", "reasoning_content", "logprobs"):
            with self.subTest(field=field):
                replies = [response("Analysis.")]
                for letter, mass in ((" B ", 0.8), (" S ", 0.2)):
                    positions = [position(letter, [("A", mass),
                                                   ("T", 1 - mass)])]
                    if field == "logprobs":
                        replies.append(response(None, positions))
                    elif field == "content":
                        replies.append(response(
                            letter, positions, reasoning="T",
                            reasoning_content="T"))
                    else:
                        replies.append(response(
                            "", positions, **{field: letter}))
                client = client_for(*replies)
                text, tokens, logprobs = self.call(
                    client, "Emit <score_A> and <score_B>.")
                self.assertEqual(text, "Analysis.\n<score_A>B</score_A>"
                                       "\n<score_B>S</score_B>")
                self.assertEqual(tokens, ["\n<score_A>", "B", "</score_A>",
                                          "\n<score_B>", "S", "</score_B>"])
                for tag, mass in (("<score_A>", 0.8), ("<score_B>", 0.2)):
                    self.assertAlmostEqual(reward.extract_score(
                        text, tokens, logprobs, tag), mass)
                calls = client.chat.completions.create.call_args_list
                self.assertEqual(len(calls), 3)
                self.assertEqual(calls[2].kwargs["messages"][-1]["content"],
                                 "Analysis.\n<score_A>B</score_A>\n<score_B>")

    def test_prefill_uses_recovered_initial_analysis(self):
        for field in ("reasoning", "reasoning_content", "logprobs"):
            with self.subTest(field=field):
                analysis = "Recovered analysis.\n<score_A>T</score_A>"
                if field == "logprobs":
                    initial = response(None, [position(analysis)])
                else:
                    initial = response(None, **{field: analysis})
                client = client_for(initial, response("A"))
                text, tokens, logprobs = self.call(client, "Emit <score_A>.")
                self.assertEqual(text, "Recovered analysis.\n<score_A>A</score_A>")
                self.assertEqual(client.chat.completions.create.call_args
                                 .kwargs["messages"][-1]["content"],
                                 "Recovered analysis.\n<score_A>")
                self.assertEqual(reward.extract_score(
                    text, tokens, logprobs, "<score_A>"), 1.0)

    def test_prefill_empty_sampled_token_keeps_distribution(self):
        client = client_for(response("Analysis."), response(
            None, [position("", [("A", 0.8), ("T", 0.2)])]))
        result = self.call(client, "Emit <score_A>.")
        self.assertAlmostEqual(reward.extract_score(
            *result, "<score_A>"), 0.8)

    def test_plain_text_without_logprobs_still_scores(self):
        client = client_for(response("<score_A> c </score_A>"))
        result = self.call(client)
        self.assertAlmostEqual(reward.extract_score(
            *result, "<score_A>"), 17 / 19)

    def test_sampled_logprob_is_kept_without_top_alternatives(self):
        client = client_for(response(None, [
            position("<score_A>"), position("D"), position("</score_A>")]))
        text, tokens, logprobs = self.call(client)
        self.assertEqual(text, "<score_A>D</score_A>")
        self.assertEqual(logprobs[1], [("D", math.log(0.6))])
        self.assertAlmostEqual(reward.extract_score(
            text, tokens, logprobs, "<score_A>"), 16 / 19)

    def test_initial_request_retries_without_template_options(self):
        client = client_for(RuntimeError("unsupported options"),
                            response("<score_A>A</score_A>"))
        result = self.call(client)
        self.assertEqual(reward.extract_score(*result, "<score_A>"), 1.0)
        calls = client.chat.completions.create.call_args_list
        self.assertIn("extra_body", calls[0].kwargs)
        self.assertNotIn("extra_body", calls[1].kwargs)

    def test_prefill_failure_returns_analysis_with_neutral_score(self):
        client = client_for(response("Analysis."),
                            RuntimeError("prefill unsupported"))
        result = self.call(client, "Emit <score_A>.")
        self.assertEqual(result, ("Analysis.", None, None))
        self.assertEqual(reward.extract_score(*result, "<score_A>"), 0.5)

    def test_later_prefill_failure_keeps_completed_tag(self):
        client = client_for(response("Analysis."), response(
            "B", [position("B", [("A", 0.8), ("T", 0.2)])]),
            RuntimeError("second prefill failed"))
        result = self.call(client, "Emit <score_A> and <score_B>.")
        self.assertEqual(result[0], "Analysis.\n<score_A>B</score_A>")
        self.assertAlmostEqual(reward.extract_score(*result, "<score_A>"), 0.8)
        self.assertEqual(reward.extract_score(*result, "<score_B>"), 0.5)

    def test_empty_response_remains_neutral(self):
        for positions in (None, []):
            with self.subTest(positions=positions):
                result = self.call(client_for(response(None, positions)))
                self.assertEqual(result, ("", None, None))
                self.assertEqual(reward.extract_score(
                    *result, "<score_A>"), 0.5)


class TagDistributionTests(unittest.TestCase):
    def test_blank_tokens_cannot_overwrite_captured_distribution(self):
        distribution = [("A", math.log(0.8)), ("T", math.log(0.2))]
        for tag in ("<score_A>", "<score_B>"):
            for blanks in ([""], [" "], ["\t\n"], ["", " ", "\t"]):
                with self.subTest(tag=tag, blanks=blanks):
                    tokens = [tag] + blanks + ["</" + tag[1:]]
                    logprobs = [[(tag, 0.0)], distribution]
                    logprobs += [[("</" + tag[1:], 0.0)] for _ in blanks]
                    self.assertIs(reward._find_tag_logprobs(
                        tokens, logprobs, tag), distribution)
                    self.assertAlmostEqual(reward.extract_score(
                        "", tokens, logprobs, tag), 0.8)

    def test_split_and_fused_tags_keep_last_verdict_distribution(self):
        for fused in (False, True):
            with self.subTest(fused=fused):
                ending, letter = ("_A", ">B") if fused else ("_A>", "B")
                tokens = ["<score", ending, letter, "</score_A>",
                          "\n<score", ending, letter, "</score_A>"]
                logprobs = [[("unused", 0.0)] for _ in tokens]
                logprobs[2] = [(letter, math.log(0.9))]
                logprobs[6] = [(">A" if fused else "A", math.log(0.3)),
                               (">T" if fused else "T", math.log(0.7))]
                self.assertAlmostEqual(reward.extract_score(
                    "", tokens, logprobs, "<score_A>"), 0.3)

    def test_text_fallback_uses_last_verdict_and_invalid_text_is_neutral(self):
        self.assertEqual(reward.extract_score(
            "<score_A>A</score_A>\n<score_A>t</score_A>",
            None, None, "<score_A>"), 0.0)
        for text in (None, "", "No verdict.", "<score_A>invalid</score_A>"):
            with self.subTest(text=text):
                self.assertEqual(reward.extract_score(
                    text, None, None, "<score_A>"), 0.5)


if __name__ == "__main__":
    unittest.main()
