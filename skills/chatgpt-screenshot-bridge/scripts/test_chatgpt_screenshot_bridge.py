from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import chatgpt_screenshot_bridge as bridge
from PIL import Image, ImageDraw


class ScreenshotBridgeUnitTests(unittest.TestCase):
    def test_choose_bottommost_prefers_last_lowest_match(self) -> None:
        matches = [
            bridge.Match(20, 100, 10, 10, 0.9, "copy_a.png"),
            bridge.Match(10, 200, 10, 10, 0.9, "copy_b.png"),
            bridge.Match(50, 200, 10, 10, 0.9, "copy_c.png"),
        ]
        self.assertEqual(bridge.choose_bottommost(matches).template, "copy_c.png")

    def test_clipboard_change_rejects_sentinel_empty_and_prompt(self) -> None:
        sentinel = "__SENTINEL__"
        prompt = "hello"
        self.assertFalse(bridge.is_valid_clipboard_change(None, sentinel, prompt))
        self.assertFalse(bridge.is_valid_clipboard_change("", sentinel, prompt))
        self.assertFalse(bridge.is_valid_clipboard_change(sentinel, sentinel, prompt))
        self.assertFalse(bridge.is_valid_clipboard_change(prompt, sentinel, prompt))
        self.assertTrue(bridge.is_valid_clipboard_change("answer", sentinel, prompt))

    def test_rect_regions_are_clamped_and_absolute(self) -> None:
        rect = bridge.Rect(100, 50, 800, 600)
        self.assertEqual(rect.as_region(), (100, 50, 800, 600))
        self.assertEqual(rect.lower_region(0.35).as_region(), (100, 440, 800, 210))
        self.assertEqual(rect.right_region(0.25).as_region(), (700, 50, 200, 600))
        self.assertEqual(rect.clamp_child(760, 570, 100, 100).as_region(), (860, 620, 40, 30))
        self.assertEqual(rect.point(0.5, 0.5), (500, 350))

    def test_composer_focus_points_stay_inside_region(self) -> None:
        region = bridge.Rect(100, 200, 800, 160)
        points = bridge.composer_focus_points(region, (500, 280))
        self.assertGreaterEqual(len(points), 3)
        self.assertEqual(points[0], (500, 280))
        for x, y in points:
            self.assertGreaterEqual(x, region.left)
            self.assertLessEqual(x, region.left + region.width)
            self.assertGreaterEqual(y, region.top)
            self.assertLessEqual(y, region.top + region.height)

    def test_safety_gate_blocks_when_real_input_is_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = bridge.run_bridge(
                bridge.BridgeOptions(prompt="hello", run_root=Path(tmp), allow_real_input=False)
            )
            self.assertEqual(result.status, bridge.BridgeStatus.REAL_INPUT_DISABLED)
            self.assertTrue(Path(result.run_dir, "events.jsonl").exists())
            self.assertTrue(Path(result.run_dir, "result.json").exists())

    def test_cli_defaults_to_allowing_workspace_bridge_input(self) -> None:
        args = bridge.parse_args(["--prompt", "hello"])
        self.assertTrue(args.allow_real_input)
        args = bridge.parse_args(["--prompt", "hello", "--disallow-real-input"])
        self.assertFalse(args.allow_real_input)

    def test_cli_defaults_to_browser_window_visual_fallback(self) -> None:
        args = bridge.parse_args(["--prompt", "hello"])
        self.assertTrue(args.allow_browser_window_fallback)
        args = bridge.parse_args(["--prompt", "hello", "--no-browser-window-fallback"])
        self.assertFalse(args.allow_browser_window_fallback)
        args = bridge.parse_args(["--prompt", "hello", "--allow-browser-window-fallback"])
        self.assertTrue(args.allow_browser_window_fallback)

    def test_locate_dark_round_button_finds_composer_action(self) -> None:
        image = Image.new("RGB", (500, 400), "white")
        draw = ImageDraw.Draw(image)
        draw.rectangle((20, 20, 220, 70), fill="black")
        draw.ellipse((420, 320, 460, 360), fill="black")
        draw.line((440, 331, 440, 349), fill="white", width=3)
        draw.line((440, 331, 432, 339), fill="white", width=3)
        draw.line((440, 331, 448, 339), fill="white", width=3)
        match = bridge.locate_dark_round_button(image, bridge.Rect(100, 200, 500, 400))
        self.assertIsNotNone(match)
        self.assertTrue(abs(match.center[0] - 540) <= 2)
        self.assertTrue(abs(match.center[1] - 540) <= 3)
        self.assertEqual(bridge.classify_dark_button_icon(image, match, bridge.Rect(100, 200, 500, 400)), "send")

    def test_voice_button_is_not_send_button(self) -> None:
        image = Image.new("RGB", (500, 400), "white")
        draw = ImageDraw.Draw(image)
        draw.ellipse((420, 320, 460, 360), fill="black")
        for x in (432, 440, 448):
            draw.line((x, 332, x, 350), fill="white", width=3)
        match = bridge.locate_dark_round_button(image, bridge.Rect(100, 200, 500, 400))
        self.assertIsNotNone(match)
        self.assertEqual(bridge.classify_dark_button_icon(image, match, bridge.Rect(100, 200, 500, 400)), "voice")
        self.assertIsNone(bridge.locate_send_button(image, bridge.Rect(100, 200, 500, 400)))

    def test_stop_generation_button_is_visible_state(self) -> None:
        image = Image.new("RGB", (500, 400), "white")
        draw = ImageDraw.Draw(image)
        draw.ellipse((420, 320, 460, 360), fill="black")
        draw.rectangle((436, 336, 444, 344), fill="white")
        window = bridge.Rect(100, 200, 500, 400)
        match = bridge.locate_dark_round_button(image, window)
        self.assertIsNotNone(match)
        self.assertEqual(bridge.classify_dark_button_icon(image, match, window), "unknown")
        self.assertTrue(bridge.is_stop_generation_button_visible(image, window))

    def test_locate_copy_icon_from_toolbar_finds_leftmost_icon_row(self) -> None:
        image = Image.new("RGB", (500, 300), "white")
        draw = ImageDraw.Draw(image)
        draw.text((150, 75), "ANSWER_TEXT", fill=(20, 20, 20))
        for x in (130, 165, 200, 235):
            draw.rectangle((x, 150, x + 14, 164), outline=(90, 90, 90), width=2)
        match = bridge.locate_copy_icon_from_toolbar(image, bridge.Rect(1000, 500, 500, 300))
        self.assertIsNotNone(match)
        self.assertEqual(match.center, (1137, 657))

    def test_centered_toolbar_can_be_zoomed_and_relocated(self) -> None:
        image = Image.new("RGB", (900, 500), "white")
        draw = ImageDraw.Draw(image)
        draw.text((360, 120), "TASK_ID: smoke", fill=(20, 20, 20))
        for x in (330, 370, 410, 450, 490):
            draw.rectangle((x, 190, x + 14, 204), outline=(92, 92, 92), width=2)
        region = bridge.Rect(200, 100, 900, 500)

        match = bridge.locate_copy_icon_from_toolbar(image, region)
        self.assertIsNotNone(match)
        self.assertEqual(match.center, (537, 297))

        zoom_region = bridge.zoom_copy_toolbar_region_from_image(image, region)
        self.assertIsNotNone(zoom_region)
        crop = image.crop(
            (
                zoom_region.left - region.left,
                zoom_region.top - region.top,
                zoom_region.left - region.left + zoom_region.width,
                zoom_region.top - region.top + zoom_region.height,
            )
        )
        zoom_match = bridge.locate_copy_icon_from_toolbar(crop, zoom_region)
        self.assertIsNotNone(zoom_match)
        self.assertEqual(zoom_match.center, (537, 297))

    def test_full_window_prefers_latest_lower_toolbar(self) -> None:
        image = Image.new("RGB", (900, 700), "white")
        draw = ImageDraw.Draw(image)
        for x in (120, 160, 200, 240):
            draw.rectangle((x, 95, x + 14, 109), outline=(90, 90, 90), width=2)
        draw.text((360, 420), "TASK_ID: smoke", fill=(20, 20, 20))
        for x in (340, 380, 420, 460):
            draw.rectangle((x, 500, x + 14, 514), outline=(92, 92, 92), width=2)
        region = bridge.Rect(50, 25, 900, 700)

        match = bridge.locate_copy_icon_from_toolbar(image, region)
        self.assertIsNotNone(match)
        self.assertEqual(match.center, (397, 532))

    def test_full_window_ignores_bottom_edge_artifacts(self) -> None:
        image = Image.new("RGB", (900, 700), "white")
        draw = ImageDraw.Draw(image)
        for x in (80, 120, 160, 200):
            draw.rectangle((x, 674, x + 14, 688), outline=(90, 90, 90), width=2)
        region = bridge.Rect(50, 25, 900, 700)
        self.assertIsNone(bridge.locate_copy_icon_from_toolbar(image, region))

    def test_logger_writes_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            logger = bridge.RunLogger(Path(tmp))
            logger.event("STATE", "action", True, coordinates=(1, 2), confidence=0.91)
            lines = Path(logger.events_path).read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 1)
            item = json.loads(lines[0])
            self.assertEqual(item["state"], "STATE")
            self.assertEqual(item["coordinates"], [1, 2])


if __name__ == "__main__":
    unittest.main()
