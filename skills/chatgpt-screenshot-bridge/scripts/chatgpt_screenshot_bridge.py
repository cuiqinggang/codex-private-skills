from __future__ import annotations

import argparse
import dataclasses
import enum
import hashlib
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path
from typing import Iterable, Sequence


class BridgeStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REAL_INPUT_DISABLED = "REAL_INPUT_DISABLED"
    NEEDS_USER_INTERVENTION = "NEEDS_USER_INTERVENTION"
    MISSING_DEPENDENCY = "MISSING_DEPENDENCY"
    EXPECTATION_FAILED = "EXPECTATION_FAILED"


@dataclasses.dataclass(frozen=True)
class Rect:
    left: int
    top: int
    width: int
    height: int

    def as_region(self) -> tuple[int, int, int, int]:
        return (self.left, self.top, self.width, self.height)

    def lower_region(self, fraction: float = 0.35) -> "Rect":
        fraction = min(max(fraction, 0.05), 1.0)
        top = self.top + int(self.height * (1.0 - fraction))
        return Rect(self.left, top, self.width, self.top + self.height - top)

    def right_region(self, fraction: float = 0.25) -> "Rect":
        fraction = min(max(fraction, 0.05), 1.0)
        left = self.left + int(self.width * (1.0 - fraction))
        return Rect(left, self.top, self.left + self.width - left, self.height)

    def clamp_child(self, left: int, top: int, width: int, height: int) -> "Rect":
        child_left = min(max(self.left + left, self.left), self.left + self.width - 1)
        child_top = min(max(self.top + top, self.top), self.top + self.height - 1)
        child_right = min(max(child_left + width, child_left + 1), self.left + self.width)
        child_bottom = min(max(child_top + height, child_top + 1), self.top + self.height)
        return Rect(child_left, child_top, child_right - child_left, child_bottom - child_top)

    def point(self, x_fraction: float, y_fraction: float) -> tuple[int, int]:
        return (
            self.left + int(self.width * x_fraction),
            self.top + int(self.height * y_fraction),
        )


@dataclasses.dataclass(frozen=True)
class Match:
    x: int
    y: int
    width: int
    height: int
    confidence: float | None = None
    template: str | None = None

    @property
    def center(self) -> tuple[int, int]:
        return (self.x + self.width // 2, self.y + self.height // 2)

    @property
    def bottom(self) -> int:
        return self.y + self.height


@dataclasses.dataclass
class BridgeOptions:
    prompt: str
    expect_contains: str | None = None
    window_title_pattern: str = "ChatGPT|chatgpt.com"
    run_root: Path = Path.cwd() / "runs" / "chatgpt_screenshot_bridge"
    template_dir: Path = Path(__file__).resolve().parents[1] / "assets" / "templates"
    timeout_start: float = 30.0
    timeout_finish: float = 180.0
    stable_frames_required: int = 3
    stable_interval: float = 0.8
    confidence_send: float = 0.88
    confidence_copy: float = 0.86
    timeout_copy: float = 30.0
    preflight_only: bool = False
    preflight_require_composer: bool = False
    allow_real_input: bool = True
    allow_enter_send_fallback: bool = True
    allow_keyboard_copy_fallback: bool = False
    allow_active_window_fallback: bool = False
    allow_browser_window_fallback: bool = True
    paste_retries: int = 3
    manual_copy_timeout: float = 0.0
    restore_clipboard: bool = False


@dataclasses.dataclass
class BridgeResult:
    status: BridgeStatus
    answer: str | None
    run_dir: str
    elapsed_ms: int
    events: list[dict]
    error: str | None = None

    def to_json(self) -> str:
        data = dataclasses.asdict(self)
        data["status"] = self.status.value
        return json.dumps(data, ensure_ascii=False, indent=2)


class RunLogger:
    def __init__(self, run_root: Path) -> None:
        stamp = time.strftime("%Y%m%d-%H%M%S")
        self.run_dir = run_root / f"{stamp}-{uuid.uuid4().hex[:8]}"
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.events_path = self.run_dir / "events.jsonl"
        self.events: list[dict] = []
        self._image_index = 0

    def screenshot_path(self, label: str) -> Path:
        self._image_index += 1
        safe_label = re.sub(r"[^a-zA-Z0-9_-]+", "-", label).strip("-").lower()
        return self.run_dir / f"{self._image_index:03d}_{safe_label}.png"

    def event(
        self,
        state: str,
        action: str,
        success: bool,
        coordinates: tuple[int, int] | None = None,
        confidence: float | None = None,
        retry_count: int = 0,
        error: str | None = None,
        before_screenshot: str | None = None,
        after_screenshot: str | None = None,
    ) -> None:
        item = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "state": state,
            "action": action,
            "coordinates": coordinates,
            "confidence": confidence,
            "elapsed_ms": None,
            "success": success,
            "retry_count": retry_count,
            "error": error,
            "before_screenshot": before_screenshot,
            "after_screenshot": after_screenshot,
        }
        self.events.append(item)
        with self.events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")


def choose_bottommost(matches: Iterable[Match]) -> Match | None:
    items = list(matches)
    if not items:
        return None
    return sorted(items, key=lambda m: (m.bottom, m.x, m.width * m.height))[-1]


def is_valid_clipboard_change(new_text: str | None, sentinel: str, prompt: str) -> bool:
    if new_text is None:
        return False
    text = new_text.strip()
    if not text:
        return False
    if text == sentinel:
        return False
    if text == prompt.strip():
        return False
    return True


def image_digest(image) -> str:
    data = image.convert("RGB").tobytes()
    return hashlib.sha256(data).hexdigest()


def locate_dark_round_button(image, window_rect: Rect, min_y_fraction: float = 0.25) -> Match | None:
    try:
        import cv2  # type: ignore
        import numpy as np  # type: ignore
    except Exception:
        return None

    array = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)
    _, mask = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates: list[Match] = []
    min_y = int(image.height * min_y_fraction)
    for contour in contours:
        x, y, width, height = cv2.boundingRect(contour)
        area = width * height
        if y < min_y:
            continue
        if area < 450 or area > 4000:
            continue
        if width < 22 or height < 22 or width > 80 or height > 80:
            continue
        ratio = width / max(height, 1)
        if ratio < 0.70 or ratio > 1.30:
            continue
        if x < int(image.width * 0.35):
            continue
        candidates.append(
            Match(
                window_rect.left + int(x),
                window_rect.top + int(y),
                int(width),
                int(height),
                None,
                "dark-round-button",
            )
        )
    return choose_bottommost(candidates)


def classify_dark_button_icon(image, match: Match, window_rect: Rect) -> str:
    left = max(0, match.x - window_rect.left)
    top = max(0, match.y - window_rect.top)
    crop = image.crop((left, top, left + match.width, top + match.height)).convert("L")
    import numpy as np

    arr = np.array(crop)
    height, width = arr.shape
    yy, xx = np.ogrid[:height, :width]
    circle = (xx - width / 2) ** 2 + (yy - height / 2) ** 2 <= (min(width, height) * 0.48) ** 2
    light = (arr > 150) & circle
    if light.sum() < 8:
        return "unknown"
    ys, xs = np.where(light)
    if ys.size:
        upper = int((ys < height * 0.38).sum())
        lower = int((ys > height * 0.62).sum())
        middle = int(((ys >= height * 0.38) & (ys <= height * 0.62)).sum())
        top_width = len(set(xs[ys < height * 0.38]))
        middle_width = len(set(xs[(ys >= height * 0.38) & (ys <= height * 0.62)]))
        bottom_width = len(set(xs[ys > height * 0.62]))
        col_counts = light.sum(axis=0)
        strong_cols = int((col_counts >= max(4, height * 0.30)).sum())
        if (
            upper > 0
            and middle > upper
            and lower <= upper
            and middle_width > top_width
            and bottom_width < top_width
            and strong_cols <= 4
        ):
            return "send"
        if strong_cols >= 2:
            return "voice"
    return "unknown"


def locate_send_button(image, window_rect: Rect) -> Match | None:
    button = locate_dark_round_button(image, window_rect)
    if not button:
        return None
    return button if classify_dark_button_icon(image, button, window_rect) == "send" else None


def is_stop_generation_button_visible(image, window_rect: Rect) -> bool:
    button = locate_dark_round_button(image, window_rect)
    if not button:
        return False
    return classify_dark_button_icon(image, button, window_rect) == "unknown"


def locate_copy_icon_from_toolbar(image, region: Rect) -> Match | None:
    row = locate_copy_toolbar_row(image)
    if not row:
        return None
    x, y, width, height = row[0]
    return Match(region.left + x, region.top + y, width, height, None, "visual-copy-toolbar")


def locate_copy_toolbar_row(image) -> list[tuple[int, int, int, int]] | None:
    try:
        import cv2  # type: ignore
        import numpy as np  # type: ignore
    except Exception:
        return None

    array = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)
    mask = cv2.inRange(gray, 45, 190)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes: list[tuple[int, int, int, int]] = []
    min_x_fraction = 0.03 if image.width < 350 else 0.20
    for contour in contours:
        x, y, width, height = cv2.boundingRect(contour)
        area = width * height
        if y < int(image.height * 0.08):
            continue
        if y > int(image.height * 0.94):
            continue
        if x < int(image.width * min_x_fraction) or x > int(image.width * 0.82):
            continue
        if width < 7 or height < 7 or width > 35 or height > 35:
            continue
        if area < 45 or area > 900:
            continue
        boxes.append((int(x), int(y), int(width), int(height)))

    rows: list[list[tuple[int, int, int, int]]] = []
    for box in sorted(boxes, key=lambda item: item[1]):
        for row in rows:
            if abs(row[0][1] - box[1]) <= 10:
                row.append(box)
                break
        else:
            rows.append([box])

    candidates: list[tuple[int, int, int, int]] = []
    for row in rows:
        row = sorted(row, key=lambda item: item[0])
        if len(row) < 3:
            continue
        first_width = row[0][2]
        first_height = row[0][3]
        if first_width < 12 or first_height < 12:
            continue
        if abs(first_width - first_height) > 6:
            continue
        if row[0][0] < int(image.width * min_x_fraction) or row[0][0] > int(image.width * 0.80):
            continue
        span = row[-1][0] + row[-1][2] - row[0][0]
        if span < 60 or span > 420:
            continue
        gaps = [row[index + 1][0] - (row[index][0] + row[index][2]) for index in range(len(row) - 1)]
        if sum(1 for gap in gaps if gap >= 18) < 2:
            continue
        candidates.append(row)

    if not candidates:
        return None
    return sorted(candidates, key=lambda item: (item[0][1], item[0][0]))[-1]


def zoom_copy_toolbar_region_from_image(image, region: Rect) -> Rect | None:
    row = locate_copy_toolbar_row(image)
    if not row:
        return None
    left = max(0, row[0][0] - 28)
    top = max(0, row[0][1] - 28)
    right = min(image.width, row[-1][0] + row[-1][2] + 42)
    bottom = min(image.height, max(item[1] + item[3] for item in row) + 32)
    return region.clamp_child(left, top, right - left, bottom - top)


def composer_from_send_like_button(window_rect: Rect, button: Match) -> tuple[Rect, tuple[int, int]]:
    top = max(window_rect.top, button.y - 70)
    bottom = min(window_rect.top + window_rect.height, button.bottom + 70)
    left = max(window_rect.left, button.center[0] - int(window_rect.width * 0.32))
    right = min(window_rect.left + window_rect.width, button.center[0] + 90)
    region = Rect(left, top, right - left, bottom - top)
    click_x = max(left + 80, button.center[0] - int(region.width * 0.55))
    click_y = button.center[1]
    return region, (click_x, click_y)


def composer_focus_points(composer_region: Rect, primary_point: tuple[int, int]) -> list[tuple[int, int]]:
    y = primary_point[1]
    candidates = [
        primary_point,
        (composer_region.left + int(composer_region.width * 0.30), y),
        (composer_region.left + int(composer_region.width * 0.45), y),
        (composer_region.left + int(composer_region.width * 0.20), y),
        (composer_region.left + int(composer_region.width * 0.60), y),
    ]
    points: list[tuple[int, int]] = []
    for x, y0 in candidates:
        point = (
            min(max(int(x), composer_region.left + 12), composer_region.left + composer_region.width - 12),
            min(max(int(y0), composer_region.top + 12), composer_region.top + composer_region.height - 12),
        )
        if point not in points:
            points.append(point)
    return points


def load_prompt(args: argparse.Namespace) -> str:
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8")
    if args.prompt is not None:
        return args.prompt
    raise SystemExit("Either --prompt or --prompt-file is required.")


def import_live_dependencies():
    try:
        import pyautogui  # type: ignore
        import pyperclip  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on machine setup
        return None, None, str(exc)
    return pyautogui, pyperclip, None


def detect_chatgpt_window(pattern: str, logger: RunLogger, pyautogui=None, allow_browser_window_fallback: bool = False) -> Rect | None:
    try:
        import pygetwindow  # type: ignore
    except Exception as exc:  # pragma: no cover - optional dependency
        logger.event(
            "ACTIVATE_CHATGPT_WINDOW",
            "pygetwindow unavailable; using active screen fallback",
            True,
            error=str(exc),
        )
        return None

    regex = re.compile(pattern, re.IGNORECASE)
    windows = [w for w in pygetwindow.getAllWindows() if w.title and regex.search(w.title)]
    if not windows and allow_browser_window_fallback and pyautogui is not None:
        browser_regex = re.compile(r"(Google Chrome|Microsoft Edge|ChatGPT)", re.IGNORECASE)
        browser_windows = [
            w for w in pygetwindow.getAllWindows()
            if w.title and browser_regex.search(w.title) and w.width > 400 and w.height > 400
        ]
        for window in sorted(browser_windows, key=lambda w: (w.width * w.height, -abs(w.left)), reverse=True):
            try:
                window.activate()
                time.sleep(0.5)
                rect = Rect(int(window.left), int(window.top), int(window.width), int(window.height))
                image = pyautogui.screenshot(region=rect.as_region())
                if locate_dark_round_button(image, rect):
                    logger.event(
                        "ACTIVATE_CHATGPT_WINDOW",
                        f"activated browser window by visual ChatGPT composer fallback: {window.title}",
                        True,
                    )
                    return rect
            except Exception as exc:
                logger.event(
                    "ACTIVATE_CHATGPT_WINDOW",
                    f"browser fallback rejected {window.title}",
                    False,
                    error=str(exc),
                )
        logger.event("ACTIVATE_CHATGPT_WINDOW", "no matching ChatGPT window and no visual browser fallback matched", False)
        return None
    if not windows:
        logger.event("ACTIVATE_CHATGPT_WINDOW", "no matching ChatGPT window", False)
        return None
    window = sorted(windows, key=lambda w: w.width * w.height)[-1]
    try:
        window.activate()
    except Exception:
        pass
    time.sleep(0.5)
    rect = Rect(int(window.left), int(window.top), int(window.width), int(window.height))
    logger.event("ACTIVATE_CHATGPT_WINDOW", f"activated {window.title}", True)
    return rect


def screenshot(pyautogui, logger: RunLogger, label: str, region: Rect | None = None):
    path = logger.screenshot_path(label)
    kwargs = {"region": region.as_region()} if region else {}
    image = pyautogui.screenshot(str(path), **kwargs)
    return image, path


def template_paths(template_dir: Path, names: Sequence[str]) -> list[Path]:
    paths: list[Path] = []
    for theme in ("light", "dark", ""):
        base = template_dir / theme if theme else template_dir
        for name in names:
            path = base / name
            if path.exists():
                paths.append(path)
    return paths


def locate_template(
    pyautogui,
    template_dir: Path,
    names: Sequence[str],
    region: Rect,
    confidence: float,
) -> Match | None:
    matches: list[Match] = []
    for path in template_paths(template_dir, names):
        try:
            boxes = pyautogui.locateAllOnScreen(
                str(path),
                region=region.as_region(),
                confidence=confidence,
            )
            for box in boxes:
                matches.append(
                    Match(
                        int(box.left),
                        int(box.top),
                        int(box.width),
                        int(box.height),
                        confidence,
                        str(path),
                    )
                )
        except Exception:
            continue
    return choose_bottommost(matches)


def wait_for_screen_change(pyautogui, region: Rect, baseline_digest: str, timeout: float) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(0.4)
        current = pyautogui.screenshot(region=region.as_region())
        if image_digest(current) != baseline_digest:
            return True
    return False


def wait_for_stable_screen(
    pyautogui,
    region: Rect,
    timeout: float,
    interval: float,
    stable_frames_required: int,
) -> bool:
    deadline = time.time() + timeout
    previous: str | None = None
    stable = 0
    while time.time() < deadline:
        current = pyautogui.screenshot(region=region.as_region())
        digest = image_digest(current)
        if digest == previous:
            stable += 1
            if stable >= stable_frames_required:
                return True
        else:
            stable = 1
            previous = digest
        time.sleep(interval)
    return False


def wait_for_generation_complete(
    pyautogui,
    window_rect: Rect,
    timeout: float,
    interval: float,
    stable_frames_required: int,
) -> bool:
    deadline = time.time() + timeout
    previous: str | None = None
    stable = 0
    while time.time() < deadline:
        current = pyautogui.screenshot(region=window_rect.as_region())
        if is_stop_generation_button_visible(current, window_rect):
            previous = None
            stable = 0
            time.sleep(interval)
            continue
        digest = image_digest(current)
        if digest == previous:
            stable += 1
            if stable >= stable_frames_required:
                return True
        else:
            previous = digest
            stable = 1
        time.sleep(interval)
    return False


def wait_clipboard_change(pyperclip, sentinel: str, prompt: str, timeout: float) -> str | None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        text = pyperclip.paste()
        if is_valid_clipboard_change(text, sentinel, prompt):
            return text
        time.sleep(0.2)
    return None


def write_result(logger: RunLogger, result: BridgeResult) -> BridgeResult:
    (logger.run_dir / "result.json").write_text(result.to_json(), encoding="utf-8")
    return result


def run_bridge(options: BridgeOptions) -> BridgeResult:
    start = time.time()
    logger = RunLogger(options.run_root)

    if not options.allow_real_input and not options.preflight_only:
        logger.event("SAFETY_GATE", "real desktop input disabled for this run", False)
        return write_result(
            logger,
            BridgeResult(
                status=BridgeStatus.REAL_INPUT_DISABLED,
                answer=None,
                run_dir=str(logger.run_dir),
                elapsed_ms=int((time.time() - start) * 1000),
                events=logger.events,
                error="Real desktop input was disabled for this run. Remove --disallow-real-input or use --preflight-only.",
            ),
        )

    pyautogui, pyperclip, dep_error = import_live_dependencies()
    if dep_error:
        logger.event("IMPORT_DEPENDENCIES", "import pyautogui/pyperclip", False, error=dep_error)
        return write_result(
            logger,
            BridgeResult(
                status=BridgeStatus.MISSING_DEPENDENCY,
                answer=None,
                run_dir=str(logger.run_dir),
                elapsed_ms=int((time.time() - start) * 1000),
                events=logger.events,
                error=dep_error,
            ),
        )

    old_mouse = pyautogui.position()
    old_clipboard = pyperclip.paste()
    answer: str | None = None
    status = BridgeStatus.FAILED
    error: str | None = None

    try:
        window_rect = detect_chatgpt_window(
            options.window_title_pattern,
            logger,
            pyautogui=pyautogui,
            allow_browser_window_fallback=options.allow_browser_window_fallback,
        )
        if window_rect is None:
            if not options.allow_active_window_fallback:
                status = BridgeStatus.NEEDS_USER_INTERVENTION
                raise RuntimeError(
                    "No matching ChatGPT window found. Re-run with a better --window-title-pattern "
                    "or explicitly pass --allow-active-window-fallback after confirming the active "
                    "window is ChatGPT."
                )
            screen_w, screen_h = pyautogui.size()
            window_rect = Rect(0, 0, int(screen_w), int(screen_h))
            logger.event(
                "ACTIVATE_CHATGPT_WINDOW",
                "falling back to active full screen by explicit request",
                True,
            )

        ready_image, ready_path = screenshot(pyautogui, logger, "ready", window_rect)
        logger.event("CAPTURE_READY_SCREEN", "captured ChatGPT window region", True, after_screenshot=str(ready_path))

        if options.preflight_only and options.preflight_require_composer:
            local_window = Rect(0, 0, ready_image.width, ready_image.height)
            composer_action = locate_dark_round_button(ready_image, local_window)
            if composer_action is None:
                logger.event(
                    "PREFLIGHT_REQUIRE_COMPOSER",
                    "composer action button not visible in ChatGPT window; page is not ready",
                    False,
                    after_screenshot=str(ready_path),
                )
                status = BridgeStatus.NEEDS_USER_INTERVENTION
                raise RuntimeError("ChatGPT composer is not visible.")
            logger.event(
                "PREFLIGHT_REQUIRE_COMPOSER",
                "composer action button visible; ChatGPT page is ready",
                True,
                coordinates=composer_action.center,
                after_screenshot=str(ready_path),
            )

        if options.preflight_only:
            logger.event("PREFLIGHT_ONLY", "window activation and screenshot completed; no input sent", True)
            return write_result(
                logger,
                BridgeResult(
                    status=BridgeStatus.SUCCESS,
                    answer=None,
                    run_dir=str(logger.run_dir),
                    elapsed_ms=int((time.time() - start) * 1000),
                    events=logger.events,
                    error=None,
                ),
            )

        composer_scan_image, composer_scan_path = screenshot(pyautogui, logger, "composer_scan", window_rect)
        visual_button = locate_dark_round_button(composer_scan_image, window_rect)
        if visual_button:
            composer_region, composer_point = composer_from_send_like_button(window_rect, visual_button)
            logger.event(
                "LOCATE_COMPOSER",
                "located dark round composer action button",
                True,
                coordinates=visual_button.center,
                after_screenshot=str(composer_scan_path),
            )
        else:
            composer_region = window_rect.lower_region(0.45)
            composer_point = composer_region.point(0.50, 0.50)
            logger.event(
                "LOCATE_COMPOSER",
                "dark round composer action button not found; using center-lower fallback",
                False,
                coordinates=composer_point,
                after_screenshot=str(composer_scan_path),
            )
        send_region = composer_region.right_region(0.35)
        response_region = Rect(window_rect.left, window_rect.top + int(window_rect.height * 0.20), window_rect.width, int(window_rect.height * 0.72))

        composer_match = locate_template(
            pyautogui,
            options.template_dir,
            ("composer_empty.png", "composer.png"),
            composer_region,
            0.82,
        )
        composer_point = composer_match.center if composer_match else composer_point
        focus_points = composer_focus_points(composer_region, composer_point)
        send_match = None
        send_button = None
        baseline = None
        pasted_path = None
        max_attempts = max(1, options.paste_retries)
        for attempt in range(1, max_attempts + 1):
            focus_point = focus_points[min(attempt - 1, len(focus_points) - 1)]
            pyautogui.click(*focus_point)
            time.sleep(0.12)
            focus_image, focus_path = screenshot(pyautogui, logger, "focus_composer", composer_region)
            logger.event(
                "FOCUS_COMPOSER",
                "click composer text area before clipboard paste",
                True,
                retry_count=attempt - 1,
                coordinates=focus_point,
                confidence=composer_match.confidence if composer_match else None,
                after_screenshot=str(focus_path),
            )

            pyperclip.copy(options.prompt)
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.05)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.35)
            pasted_image, pasted_path = screenshot(pyautogui, logger, "prompt_pasted", composer_region)
            logger.event(
                "PASTE_PROMPT_FROM_CLIPBOARD",
                "ctrl+a then ctrl+v; require send-arrow before clicking",
                True,
                retry_count=attempt - 1,
                after_screenshot=str(pasted_path),
            )
            baseline = image_digest(pasted_image)

            deadline = time.time() + 1.5
            while time.time() < deadline and not (send_match or send_button):
                send_match = locate_template(
                    pyautogui,
                    options.template_dir,
                    ("send_enabled.png", "send_button_enabled.png", "send.png"),
                    send_region,
                    options.confidence_send,
                )
                if send_match:
                    break
                send_scan = pyautogui.screenshot(region=window_rect.as_region())
                send_button = locate_send_button(send_scan, window_rect)
                if send_button:
                    break
                time.sleep(0.15)

            if send_match or send_button:
                break

            local_button = locate_dark_round_button(
                pasted_image,
                Rect(0, 0, pasted_image.width, pasted_image.height),
                min_y_fraction=0,
            )
            icon_state = (
                classify_dark_button_icon(pasted_image, local_button, Rect(0, 0, pasted_image.width, pasted_image.height))
                if local_button
                else "missing"
            )
            logger.event(
                "WAIT_SEND_ARROW_AFTER_PASTE",
                "send arrow not visible; retrying paste instead of clicking voice/stop control",
                False,
                retry_count=attempt - 1,
                error=f"composer action icon={icon_state}",
                after_screenshot=str(pasted_path),
            )

        if send_match:
            pyautogui.click(*send_match.center)
            action = f"clicked send template {send_match.template}"
            coordinates = send_match.center
            confidence = send_match.confidence
        elif send_button:
            pyautogui.click(*send_button.center)
            action = "clicked visually detected send-arrow button"
            coordinates = send_button.center
            confidence = None
        else:
            raise RuntimeError("Prompt paste did not produce a send-arrow. Refusing to click voice/stop controls.")

        sent_image, sent_path = screenshot(pyautogui, logger, "send_clicked", composer_region)
        logger.event("CLICK_SEND", action, True, coordinates=coordinates, confidence=confidence, after_screenshot=str(sent_path))

        changed = wait_for_screen_change(pyautogui, composer_region, baseline, options.timeout_start)
        gen_image, gen_path = screenshot(pyautogui, logger, "generation_started", composer_region)
        logger.event("WAIT_GENERATION_STARTED", "composer region changed", changed, after_screenshot=str(gen_path))

        stable = wait_for_generation_complete(
            pyautogui,
            window_rect,
            options.timeout_finish,
            options.stable_interval,
            options.stable_frames_required,
        )
        done_image, done_path = screenshot(pyautogui, logger, "generation_done", window_rect)
        logger.event("WAIT_GENERATION_FINISHED", "stop button gone and full window stable", stable, after_screenshot=str(done_path))
        if not stable:
            raise RuntimeError("Timed out waiting for the stop-generation button to disappear and the window to stabilize.")

        copy_search_region = window_rect
        sentinel = f"__CHATGPT_SCREENSHOT_BRIDGE_SENTINEL_{uuid.uuid4().hex}__"
        pyperclip.copy(sentinel)
        copy_match = None
        visual_copy = locate_copy_icon_from_toolbar(done_image, copy_search_region)
        zoom_region = zoom_copy_toolbar_region_from_image(done_image, copy_search_region)
        if zoom_region:
            zoom_image, zoom_path = screenshot(pyautogui, logger, "copy_toolbar_zoom", zoom_region)
            logger.event("ZOOM_COPY_TOOLBAR", "crop small screenshot around visually detected assistant toolbar", True, coordinates=zoom_region.point(0.5, 0.5), after_screenshot=str(zoom_path))
            zoom_copy = locate_copy_icon_from_toolbar(zoom_image, zoom_region)
            if zoom_copy:
                visual_copy = zoom_copy
        elif visual_copy:
            logger.event("ZOOM_COPY_TOOLBAR", "toolbar row found but zoom region could not be derived", False, coordinates=visual_copy.center)

        hover_image = None
        hover_path = None
        hover_points = [
            copy_search_region.point(0.42, 0.18),
            copy_search_region.point(0.42, 0.30),
            copy_search_region.point(0.50, 0.45),
            copy_search_region.point(0.62, 0.65),
            copy_search_region.point(0.62, 0.82),
        ]
        copy_deadline = time.time() + options.timeout_copy
        hover_attempt = 0
        while not (copy_match or visual_copy) and time.time() < copy_deadline:
            hover_point = hover_points[min(hover_attempt, len(hover_points) - 1)]
            pyautogui.moveTo(*hover_point, duration=0.1)
            hover_image, hover_path = screenshot(pyautogui, logger, "copy_hover", copy_search_region)
            logger.event("REVEAL_COPY_BUTTON", "hover candidate assistant toolbar region and re-screenshot", True, coordinates=hover_point, retry_count=hover_attempt, after_screenshot=str(hover_path))
            copy_match = locate_template(
                pyautogui,
                options.template_dir,
                ("copy_button.png", "copy.png"),
                copy_search_region,
                options.confidence_copy,
            )
            visual_copy = locate_copy_icon_from_toolbar(hover_image, copy_search_region)
            zoom_region = zoom_copy_toolbar_region_from_image(hover_image, copy_search_region)
            if zoom_region:
                zoom_image, zoom_path = screenshot(pyautogui, logger, "copy_toolbar_zoom", zoom_region)
                logger.event("ZOOM_COPY_TOOLBAR", "crop small screenshot around candidate assistant toolbar after hover", True, coordinates=zoom_region.point(0.5, 0.5), retry_count=hover_attempt, after_screenshot=str(zoom_path))
                zoom_copy = locate_copy_icon_from_toolbar(zoom_image, zoom_region)
                if zoom_copy:
                    visual_copy = zoom_copy
            if copy_match or visual_copy:
                break
            hover_attempt += 1
            if hover_attempt >= len(hover_points):
                pyautogui.scroll(-2)
            time.sleep(1.0)

        if copy_match:
            pyautogui.click(*copy_match.center)
            copy_action = f"clicked copy template {copy_match.template}"
            copy_coordinates = copy_match.center
            copy_confidence = copy_match.confidence
        elif visual_copy:
            pyautogui.click(*visual_copy.center)
            copy_action = "clicked visually detected first assistant toolbar copy icon"
            copy_coordinates = visual_copy.center
            copy_confidence = None
        elif options.allow_keyboard_copy_fallback:
            pyautogui.hotkey("ctrl", "shift", "c")
            copy_action = "pressed Ctrl+Shift+C fallback"
            copy_coordinates = None
            copy_confidence = None
        else:
            raise RuntimeError("Copy button not found before timeout.")

        answer = None
        verify_deadline = time.time() + options.timeout_copy
        while time.time() < verify_deadline:
            copied_image, copied_path = screenshot(pyautogui, logger, "copy_clicked", copy_search_region)
            logger.event("CLICK_COPY_BUTTON", copy_action, True, coordinates=copy_coordinates, confidence=copy_confidence, after_screenshot=str(copied_path))
            candidate = wait_clipboard_change(pyperclip, sentinel, options.prompt, 3.0)
            if candidate and (not options.expect_contains or options.expect_contains in candidate):
                answer = candidate
                break
            logger.event(
                "VERIFY_CLIPBOARD_CHANGED",
                "clipboard changed but did not contain expected text; retrying copy",
                False,
                error=None if candidate else "clipboard did not change",
            )
            pyperclip.copy(sentinel)
            if copy_coordinates:
                pyautogui.click(*copy_coordinates)
            elif options.allow_keyboard_copy_fallback:
                pyautogui.hotkey("ctrl", "shift", "c")
            time.sleep(0.5)

        if answer is None and options.manual_copy_timeout > 0:
            logger.event("VERIFY_CLIPBOARD_CHANGED", "waiting for manual copy fallback", False)
            answer = wait_clipboard_change(pyperclip, sentinel, options.prompt, options.manual_copy_timeout)

        if answer is None:
            if options.expect_contains:
                status = BridgeStatus.EXPECTATION_FAILED
                error = f"Clipboard never contained expected text: {options.expect_contains!r}"
            else:
                raise RuntimeError("Clipboard did not change to a new non-empty answer.")
        else:
            logger.event("VERIFY_CLIPBOARD_CHANGED", "clipboard changed from sentinel and matched expectation", True)
            status = BridgeStatus.SUCCESS

    except Exception as exc:  # pragma: no cover - live UI path
        error = str(exc)
        logger.event("FAILED", "bridge failed", False, error=error)
    finally:
        try:
            pyautogui.moveTo(*old_mouse, duration=0.1)
        except Exception:
            pass
        if options.restore_clipboard:
            try:
                pyperclip.copy(old_clipboard)
            except Exception:
                pass

    return write_result(
        logger,
        BridgeResult(
            status=status,
            answer=answer,
            run_dir=str(logger.run_dir),
            elapsed_ms=int((time.time() - start) * 1000),
            events=logger.events,
            error=error,
        ),
    )


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Screenshot-first ChatGPT web send/copy bridge.")
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--expect-contains")
    parser.add_argument("--window-title-pattern", default="ChatGPT|chatgpt.com")
    parser.add_argument("--run-root", default=str(Path.cwd() / "runs" / "chatgpt_screenshot_bridge"))
    parser.add_argument("--template-dir", default=str(Path(__file__).resolve().parents[1] / "assets" / "templates"))
    parser.add_argument("--timeout-start", type=float, default=30.0)
    parser.add_argument("--timeout-finish", type=float, default=180.0)
    parser.add_argument("--stable-frames-required", type=int, default=3)
    parser.add_argument("--stable-interval", type=float, default=0.8)
    parser.add_argument("--confidence-send", type=float, default=0.88)
    parser.add_argument("--confidence-copy", type=float, default=0.86)
    parser.add_argument("--timeout-copy", type=float, default=30.0)
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--preflight-require-composer", action="store_true")
    parser.add_argument("--manual-copy-timeout", type=float, default=0.0)
    real_input = parser.add_mutually_exclusive_group()
    real_input.add_argument("--allow-real-input", dest="allow_real_input", action="store_true")
    real_input.add_argument("--disallow-real-input", dest="allow_real_input", action="store_false")
    parser.set_defaults(allow_real_input=True)
    parser.add_argument("--allow-active-window-fallback", action="store_true")
    parser.add_argument("--allow-browser-window-fallback", action="store_true", default=True)
    parser.add_argument("--no-browser-window-fallback", dest="allow_browser_window_fallback", action="store_false")
    parser.add_argument("--no-enter-send-fallback", action="store_true")
    parser.add_argument("--allow-keyboard-copy-fallback", action="store_true")
    parser.add_argument("--paste-retries", type=int, default=3)
    parser.add_argument("--restore-clipboard", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    options = BridgeOptions(
        prompt=load_prompt(args),
        expect_contains=args.expect_contains,
        window_title_pattern=args.window_title_pattern,
        run_root=Path(args.run_root),
        template_dir=Path(args.template_dir),
        timeout_start=args.timeout_start,
        timeout_finish=args.timeout_finish,
        stable_frames_required=args.stable_frames_required,
        stable_interval=args.stable_interval,
        confidence_send=args.confidence_send,
        confidence_copy=args.confidence_copy,
        timeout_copy=args.timeout_copy,
        preflight_only=args.preflight_only,
        preflight_require_composer=args.preflight_require_composer,
        allow_real_input=args.allow_real_input,
        allow_enter_send_fallback=not args.no_enter_send_fallback,
        allow_keyboard_copy_fallback=args.allow_keyboard_copy_fallback,
        allow_active_window_fallback=args.allow_active_window_fallback,
        allow_browser_window_fallback=args.allow_browser_window_fallback,
        paste_retries=args.paste_retries,
        manual_copy_timeout=args.manual_copy_timeout,
        restore_clipboard=args.restore_clipboard,
    )
    result = run_bridge(options)
    print(result.to_json())
    return 0 if result.status == BridgeStatus.SUCCESS else 1


if __name__ == "__main__":
    raise SystemExit(main())
