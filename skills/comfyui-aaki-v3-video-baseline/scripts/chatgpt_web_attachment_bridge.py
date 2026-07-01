from __future__ import annotations

import argparse
import ctypes
import dataclasses
import json
import mimetypes
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Sequence

from PIL import Image, ImageChops


TEXT_BRIDGE = Path(r"C:\Users\A\.codex\skills\chatgpt-screenshot-bridge\scripts")
if str(TEXT_BRIDGE) not in sys.path:
    sys.path.insert(0, str(TEXT_BRIDGE))

import chatgpt_screenshot_bridge as text_bridge  # type: ignore


CF_HDROP = 15
GMEM_MOVEABLE = 0x0002


class AttachmentStatus:
    PASS_RESULT_SAVED = "ATTACHMENT_PASS_RESULT_SAVED"
    BLOCKED_BROWSER_SECURITY_PROMPT = "ATTACHMENT_BLOCKED_BROWSER_SECURITY_PROMPT"
    FAIL_TOO_MANY_FILES = "ATTACHMENT_FAIL_TOO_MANY_FILES"
    FAIL_MISSING_FILE = "ATTACHMENT_FAIL_MISSING_FILE"
    FAIL_NO_CHATGPT_WINDOW = "ATTACHMENT_FAIL_NO_CHATGPT_WINDOW"
    FAIL_ATTACHMENT_NOT_VISIBLE = "ATTACHMENT_FAIL_ATTACHMENT_NOT_VISIBLE"
    FAIL_DRAG_SOURCE_NOT_FOUND = "ATTACHMENT_FAIL_DRAG_SOURCE_NOT_FOUND"
    FAIL_NO_SAFE_SEND_BUTTON = "ATTACHMENT_FAIL_NO_SAFE_SEND_BUTTON"
    FAIL_WRONG_TARGET_WINDOW = "ATTACHMENT_FAIL_WRONG_TARGET_WINDOW"
    FAIL_SEND_NOT_CONFIRMED = "ATTACHMENT_FAIL_SEND_NOT_CONFIRMED"
    FAIL_NO_NEW_RESPONSE = "ATTACHMENT_FAIL_NO_NEW_RESPONSE"
    FAIL_TIMEOUT = "ATTACHMENT_FAIL_TIMEOUT"
    FAIL_EXCEPTION = "ATTACHMENT_FAIL_EXCEPTION"


@dataclasses.dataclass
class AttachmentResult:
    status: str
    run_dir: str
    branch: str
    files: list[str]
    elapsed_ms: int
    error: str | None = None
    screenshots: dict[str, str] = dataclasses.field(default_factory=dict)


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def set_clipboard_files(paths: Sequence[Path]) -> None:
    import win32clipboard  # type: ignore

    encoded = ("\0".join(str(path) for path in paths) + "\0\0").encode("utf-16le")
    dropfiles_size = 20
    total_size = dropfiles_size + len(encoded)
    kernel32 = ctypes.windll.kernel32
    kernel32.GlobalAlloc.argtypes = [ctypes.c_uint, ctypes.c_size_t]
    kernel32.GlobalAlloc.restype = ctypes.c_void_p
    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalUnlock.restype = ctypes.c_int
    kernel32.GlobalFree.argtypes = [ctypes.c_void_p]
    kernel32.GlobalFree.restype = ctypes.c_void_p
    handle = kernel32.GlobalAlloc(GMEM_MOVEABLE, total_size)
    if not handle:
        raise RuntimeError("GlobalAlloc failed for CF_HDROP clipboard payload.")
    locked = kernel32.GlobalLock(handle)
    if not locked:
        kernel32.GlobalFree(handle)
        raise RuntimeError("GlobalLock failed for CF_HDROP clipboard payload.")
    try:
        header = (dropfiles_size).to_bytes(4, "little")
        header += (0).to_bytes(4, "little")
        header += (0).to_bytes(4, "little")
        header += (0).to_bytes(4, "little")
        header += (1).to_bytes(4, "little")
        ctypes.memmove(locked, header + encoded, total_size)
    finally:
        kernel32.GlobalUnlock(handle)

    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(CF_HDROP, handle)
        handle = 0
    finally:
        win32clipboard.CloseClipboard()
        if handle:
            kernel32.GlobalFree(handle)


def capture_region(region: text_bridge.Rect) -> Image.Image:
    try:
        import mss  # type: ignore

        with mss.mss() as sct:
            shot = sct.grab(
                {
                    "left": int(region.left),
                    "top": int(region.top),
                    "width": max(1, int(region.width)),
                    "height": max(1, int(region.height)),
                }
            )
            return Image.frombytes("RGB", shot.size, shot.rgb)
    except Exception:
        import pyautogui  # type: ignore

        return pyautogui.screenshot(region=region.as_region())


def screenshot(pyautogui, run_dir: Path, label: str, region: text_bridge.Rect):
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / f"{int(time.time() * 1000)}_{label}.png"
    image = capture_region(region)
    image.save(path)
    return image, path


def save_zoom(image, run_dir: Path, label: str, scale: int = 2) -> Path:
    path = run_dir / f"{int(time.time() * 1000)}_{label}_zoom.png"
    zoomed = image.resize((image.width * scale, image.height * scale))
    zoomed.save(path)
    return path


def image_contains_security_prompt(image) -> bool:
    try:
        import pytesseract  # type: ignore

        text = pytesseract.image_to_string(image, lang="eng+chi_sim")
    except Exception:
        return False
    needles = (
        "remote debugging",
        "Allow remote",
        "Cookie",
        "网站数据",
        "允许远程",
        "完全控制",
    )
    return any(item.lower() in text.lower() for item in needles)


def classify_files(branch: str, files: list[Path]) -> str | None:
    if branch == "image" and len(files) > 10:
        return AttachmentStatus.FAIL_TOO_MANY_FILES
    for path in files:
        if not path.exists() or not path.is_file():
            return AttachmentStatus.FAIL_MISSING_FILE
    return None


def drag_files_from_explorer(pyautogui, files: Sequence[Path], window_rect: text_bridge.Rect, wait_per_file: float) -> None:
    from pywinauto import Desktop  # type: ignore

    drop_point = window_rect.point(0.50, 0.52)
    desktop = Desktop(backend="uia")
    for path in files:
        subprocess.Popen(["explorer.exe", f"/select,{path}"])
        time.sleep(2.5)
        target_item = None
        expected_names = {path.stem, path.name}
        first_visible_item = None
        for win in desktop.windows():
            try:
                title = win.window_text()
                if not title:
                    continue
                descendants = win.descendants(control_type="ListItem")
            except Exception:
                continue
            for item in descendants:
                try:
                    rect = item.rectangle()
                    if rect.width() > 20 and rect.height() > 20 and first_visible_item is None:
                        first_visible_item = item
                    if item.window_text() in expected_names:
                        target_item = item
                        break
                except Exception:
                    continue
            if target_item:
                break
        if not target_item:
            raise RuntimeError(f"{AttachmentStatus.FAIL_DRAG_SOURCE_NOT_FOUND}: {path}")
        rect = target_item.rectangle()
        start_point = (int((rect.left + rect.right) / 2), int((rect.top + rect.bottom) / 2))
        pyautogui.moveTo(*start_point, duration=0.15)
        pyautogui.dragTo(*drop_point, duration=0.8, button="left")
        time.sleep(wait_per_file)


def wait_for_send_ready(pyautogui, window_rect: text_bridge.Rect, template_dir: Path, confidence: float, timeout: float):
    deadline = time.time() + timeout
    send_region = window_rect.lower_region(0.55).right_region(0.40)
    while time.time() < deadline:
        send_match = text_bridge.locate_template(
            pyautogui,
            template_dir,
            ("send_enabled.png", "send_button_enabled.png", "send.png"),
            send_region,
            confidence,
        )
        if send_match:
            return send_match, None
        send_scan = capture_region(window_rect)
        send_button = text_bridge.locate_send_button(send_scan, window_rect)
        if send_button:
            return None, send_button
        time.sleep(0.3)
    return None, None


def image_change_fraction(before, after) -> float:
    if before.size != after.size:
        after = after.resize(before.size)
    before_small = before.convert("L").resize((160, 100))
    after_small = after.convert("L").resize((160, 100))
    diff = ImageChops.difference(before_small, after_small)
    hist = diff.histogram()
    changed = sum(count for value, count in enumerate(hist) if value > 12)
    return changed / float(before_small.width * before_small.height)


def current_send_button(pyautogui, window_rect: text_bridge.Rect):
    image = capture_region(window_rect)
    return text_bridge.locate_send_button(image, window_rect), image


def image_result_visible(image) -> bool:
    try:
        from chatgpt_web_result_saver import find_image_like_regions  # type: ignore

        return bool(find_image_like_regions(image, max_results=1))
    except Exception:
        return False


def click_chatgpt_send(pyautogui, window_rect: text_bridge.Rect, send_match, send_button) -> None:
    if send_match:
        pyautogui.click(*send_match.center)
        return
    if send_button:
        pyautogui.click(*send_button.center)
        return
    image = capture_region(window_rect)
    local_button = text_bridge.locate_send_button(image, text_bridge.Rect(0, 0, image.width, image.height))
    if not local_button:
        local_button = text_bridge.locate_dark_round_button(image, text_bridge.Rect(0, 0, image.width, image.height))
    if not local_button:
        raise RuntimeError("No safe ChatGPT send button found inside the ChatGPT window.")
    pyautogui.click(window_rect.left + local_button.center[0], window_rect.top + local_button.center[1])


def click_send_and_confirm(
    pyautogui,
    window_rect: text_bridge.Rect,
    template_dir: Path,
    confidence: float,
    before_send_image,
    run_dir: Path,
    screenshots: dict[str, str],
    retries: int,
    confirm_timeout: float,
):
    last_image = None
    last_path = None
    for attempt in range(1, retries + 1):
        send_match, send_button = wait_for_send_ready(pyautogui, window_rect, template_dir, confidence, 3.0)
        if not send_match and not send_button:
            return False, None, "Safe send button disappeared before click."
        click_chatgpt_send(pyautogui, window_rect, send_match, send_button)
        deadline = time.time() + confirm_timeout
        while time.time() < deadline:
            time.sleep(0.5)
            image, path = screenshot(pyautogui, run_dir, f"state_send_confirm_try_{attempt}", window_rect)
            screenshots[f"state_send_confirm_try_{attempt}"] = str(path)
            last_image = image
            last_path = path
            still_send, _ = current_send_button(pyautogui, window_rect)
            changed = image_change_fraction(before_send_image, image)
            if not still_send and changed >= 0.002:
                screenshots["state_sent"] = str(path)
                return True, image, None
        # If the click did not take, loop and try a freshly detected send arrow.
    if last_path:
        screenshots["state_sent_unconfirmed"] = str(last_path)
    return False, last_image, "Send click was not confirmed: composer/send state did not change after retries."


def wait_for_new_response_then_stable(
    pyautogui,
    window_rect: text_bridge.Rect,
    sent_image,
    timeout: float,
    interval: float,
    stable_frames_required: int,
    run_dir: Path,
    screenshots: dict[str, str],
    require_image_result: bool,
):
    deadline = time.time() + timeout
    saw_new_response = False
    previous_image = None
    stable = 0
    probe_index = 0
    while time.time() < deadline:
        current = capture_region(window_rect)
        probe_index += 1
        if not saw_new_response:
            if text_bridge.locate_send_button(current, window_rect):
                return False, "Safe send arrow is still visible after click; the message appears to remain in the composer."
            changed = image_change_fraction(sent_image, current)
            if changed >= 0.002:
                path = run_dir / f"{int(time.time() * 1000)}_state_new_response_seen.png"
                current.save(path)
                screenshots["state_new_response_seen"] = str(path)
                saw_new_response = True
                previous_image = current
                stable = 0
            else:
                if probe_index in (1, 5, 10):
                    run_dir.mkdir(parents=True, exist_ok=True)
                    path = run_dir / f"{int(time.time() * 1000)}_state_waiting_for_new_response_{probe_index}.png"
                    current.save(path)
                    screenshots[f"state_waiting_for_new_response_{probe_index}"] = str(path)
                time.sleep(interval)
                continue
        if text_bridge.is_stop_generation_button_visible(current, window_rect):
            previous_image = None
            stable = 0
            time.sleep(interval)
            continue
        if previous_image is not None and image_change_fraction(previous_image, current) <= 0.0015:
            stable += 1
            if stable >= stable_frames_required:
                if require_image_result and not image_result_visible(current):
                    run_dir.mkdir(parents=True, exist_ok=True)
                    path = run_dir / f"{int(time.time() * 1000)}_state_stable_without_image_result.png"
                    current.save(path)
                    screenshots["state_stable_without_image_result"] = str(path)
                    previous_image = current
                    stable = 0
                    time.sleep(interval)
                    continue
                return True, None
        else:
            previous_image = current
            stable = 1
        time.sleep(interval)
    if not saw_new_response:
        return False, "No new ChatGPT response appeared after confirmed send."
    return False, "Timed out waiting for ChatGPT response to finish after new content appeared."


def detect_middle_screen_chatgpt_window(pyautogui, title_pattern: str, run_dir: Path, screenshots: dict[str, str]) -> text_bridge.Rect | None:
    try:
        import pygetwindow as gw  # type: ignore
        import re

        regex = re.compile(title_pattern, re.IGNORECASE)
        windows = []
        for window in gw.getAllWindows():
            title = window.title or ""
            if not title or not regex.search(title):
                continue
            if "Codex" in title:
                continue
            if "Google Chrome" not in title and "ChatGPT" not in title:
                continue
            if window.left < 0 or window.left >= 2560:
                continue
            if window.top < -100 or window.width < 800 or window.height < 700:
                continue
            windows.append(window)
        if not windows:
            return None
        target = sorted(windows, key=lambda w: -w.width * w.height)[0]
        if target.isMinimized:
            target.restore()
        target.activate()
        time.sleep(0.8)
        rect = text_bridge.Rect(int(target.left), int(target.top), int(target.width), int(target.height))
        image, path = screenshot(pyautogui, run_dir, "state_middle_screen_target", rect)
        screenshots["state_middle_screen_target"] = str(path)
        (run_dir / "target_window.txt").write_text(
            f"title={target.title}\nleft={target.left}\ntop={target.top}\nwidth={target.width}\nheight={target.height}\n",
            encoding="utf-8",
        )
        return rect
    except Exception:
        return None


def ensure_visible_chatgpt_window(pyautogui, window_rect: text_bridge.Rect) -> text_bridge.Rect:
    if window_rect.left >= 0 and window_rect.top >= 0 and window_rect.width >= 800 and window_rect.height >= 700:
        return window_rect
    raise RuntimeError(
        f"{AttachmentStatus.FAIL_WRONG_TARGET_WINDOW}: target window left={window_rect.left} "
        f"top={window_rect.top} width={window_rect.width} height={window_rect.height} "
        "is outside the verified middle-screen bounds."
    )


def paste_prompt_after_attachment(pyautogui, pyperclip, prompt: str, window_rect: text_bridge.Rect, run_dir: Path, screenshots: dict[str, str]):
    baseline = capture_region(window_rect)
    baseline_digest = text_bridge.image_digest(baseline)
    points = [
        window_rect.point(0.43, 0.68),
        window_rect.point(0.50, 0.68),
        window_rect.point(0.38, 0.68),
        window_rect.point(0.43, 0.74),
        window_rect.point(0.50, 0.74),
        window_rect.point(0.43, 0.82),
        window_rect.point(0.50, 0.82),
    ]
    pyperclip.copy(prompt)
    last_path = None
    for index, point in enumerate(points, start=1):
        pyautogui.click(*point)
        time.sleep(0.12)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.45)
        image, path = screenshot(pyautogui, run_dir, f"state_prompt_paste_try_{index}", window_rect)
        screenshots[f"state_prompt_paste_try_{index}"] = str(path)
        zoom_region = window_rect.clamp_child(
            int(window_rect.width * 0.30),
            int(window_rect.height * 0.58),
            int(window_rect.width * 0.45),
            int(window_rect.height * 0.25),
        )
        zoom_image, _ = screenshot(pyautogui, run_dir, f"composer_zoom_after_try_{index}", zoom_region)
        screenshots[f"composer_zoom_after_try_{index}"] = str(save_zoom(zoom_image, run_dir, f"composer_after_try_{index}", 3))
        last_path = path
        if text_bridge.image_digest(image) != baseline_digest:
            screenshots["state_prompt_pasted"] = str(path)
            return True, path
    if last_path:
        screenshots["state_prompt_pasted"] = str(last_path)
    return False, last_path


def paste_prompt_before_attachment(pyautogui, pyperclip, prompt: str, window_rect: text_bridge.Rect, run_dir: Path, screenshots: dict[str, str], template_dir: Path, confidence: float):
    scan_image, scan_path = screenshot(pyautogui, run_dir, "state_prompt_before_scan", window_rect)
    screenshots["state_prompt_before_scan"] = str(scan_path)
    action = text_bridge.locate_dark_round_button(scan_image, text_bridge.Rect(0, 0, scan_image.width, scan_image.height))
    if action:
        composer_region, composer_point = text_bridge.composer_from_send_like_button(
            window_rect,
            text_bridge.Match(window_rect.left + action.x, window_rect.top + action.y, action.width, action.height),
        )
        focus_points = text_bridge.composer_focus_points(composer_region, composer_point)
    else:
        focus_points = []
    # ChatGPT's bottom composer is wide; all fallback points must stay relative
    # to the verified target window to avoid pasting into Codex or another app.
    fallback_points = [
        window_rect.point(0.43, 0.925),
        window_rect.point(0.50, 0.925),
        window_rect.point(0.38, 0.925),
        window_rect.point(0.55, 0.925),
        window_rect.point(0.43, 0.900),
        window_rect.point(0.50, 0.900),
    ]
    for point in fallback_points:
        if point not in focus_points:
            focus_points.append(point)
    pyperclip.copy(prompt)
    for index, point in enumerate(focus_points, start=1):
        pyautogui.click(*point)
        time.sleep(0.12)
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.05)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)
        image, path = screenshot(pyautogui, run_dir, f"state_prompt_before_try_{index}", window_rect)
        screenshots[f"state_prompt_before_try_{index}"] = str(path)
        zoom_region = window_rect.clamp_child(
            int(window_rect.width * 0.30),
            int(window_rect.height * 0.76),
            int(window_rect.width * 0.45),
            int(window_rect.height * 0.18),
        )
        zoom_image, _ = screenshot(pyautogui, run_dir, f"composer_zoom_before_try_{index}", zoom_region)
        screenshots[f"composer_zoom_before_try_{index}"] = str(save_zoom(zoom_image, run_dir, f"composer_before_try_{index}", 3))
        send_match, send_button = wait_for_send_ready(pyautogui, window_rect, template_dir, confidence, 1.0)
        if send_match or send_button:
            screenshots["state_prompt_pasted"] = str(path)
            return True
    return False


def run(args: argparse.Namespace) -> AttachmentResult:
    start = time.time()
    files = [Path(item).resolve() for item in args.file]
    branch = args.branch
    run_root = Path(args.run_root).resolve()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    run_dir = run_root / f"{stamp}_{branch}_{args.purpose}_{uuid.uuid4().hex[:6]}"
    inputs_dir = run_dir / "inputs"
    outputs_dir = run_dir / "local_outputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)
    screenshots: dict[str, str] = {}

    prompt = Path(args.prompt_file).read_text(encoding="utf-8") if args.prompt_file else args.prompt
    (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")

    failure = classify_files(branch, files)
    if failure:
        result = AttachmentResult(failure, str(run_dir), branch, [str(p) for p in files], int((time.time() - start) * 1000))
        write_json(run_dir / "result_manifest.json", dataclasses.asdict(result))
        return result

    copied_inputs = []
    for path in files:
        target = inputs_dir / path.name
        if path != target:
            shutil.copy2(path, target)
        copied_inputs.append(target)

    write_json(
        run_dir / "input_manifest.json",
        {
            "branch": branch,
            "purpose": args.purpose,
            "files": [
                {
                    "source": str(src),
                    "local_copy": str(dst),
                    "bytes": dst.stat().st_size,
                    "mime": mimetypes.guess_type(dst.name)[0],
                }
                for src, dst in zip(files, copied_inputs)
            ],
        },
    )

    pyautogui, pyperclip, dep_error = text_bridge.import_live_dependencies()
    if dep_error:
        result = AttachmentResult(AttachmentStatus.FAIL_EXCEPTION, str(run_dir), branch, [str(p) for p in files], int((time.time() - start) * 1000), dep_error)
        write_json(run_dir / "result_manifest.json", dataclasses.asdict(result))
        return result

    old_mouse = pyautogui.position()
    try:
        window_rect = detect_middle_screen_chatgpt_window(pyautogui, args.window_title_pattern, run_dir, screenshots)
        if window_rect is None:
            result = AttachmentResult(AttachmentStatus.FAIL_WRONG_TARGET_WINDOW, str(run_dir), branch, [str(p) for p in files], int((time.time() - start) * 1000), "No verified middle-screen ChatGPT Chrome window found. Refusing to paste into another window.", screenshots)
            write_json(run_dir / "result_manifest.json", dataclasses.asdict(result))
            return result
        window_rect = ensure_visible_chatgpt_window(pyautogui, window_rect)

        before_image, before_path = screenshot(pyautogui, run_dir, "state_before", window_rect)
        screenshots["state_before"] = str(before_path)
        if image_contains_security_prompt(before_image):
            result = AttachmentResult(
                AttachmentStatus.BLOCKED_BROWSER_SECURITY_PROMPT,
                str(run_dir),
                branch,
                [str(p) for p in files],
                int((time.time() - start) * 1000),
                "Browser security prompt detected. Close/cancel it before retrying; do not click Allow automatically.",
                screenshots,
            )
            write_json(run_dir / "result_manifest.json", dataclasses.asdict(result))
            return result

        action = text_bridge.locate_dark_round_button(before_image, text_bridge.Rect(0, 0, before_image.width, before_image.height))
        if action:
            composer_region, composer_point = text_bridge.composer_from_send_like_button(window_rect, text_bridge.Match(window_rect.left + action.x, window_rect.top + action.y, action.width, action.height))
        else:
            composer_region = window_rect.lower_region(0.45)
            composer_point = composer_region.point(0.50, 0.50)

        prompt_already_pasted = False
        if args.prompt_order == "before":
            prompt_already_pasted = paste_prompt_before_attachment(
                pyautogui,
                pyperclip,
                prompt,
                window_rect,
                run_dir,
                screenshots,
                Path(args.template_dir),
                args.confidence_send,
            )
            if not prompt_already_pasted:
                result = AttachmentResult(AttachmentStatus.FAIL_NO_SAFE_SEND_BUTTON, str(run_dir), branch, [str(p) for p in files], int((time.time() - start) * 1000), "Prompt paste before attachment did not produce a safe send-ready composer.", screenshots)
                write_json(run_dir / "result_manifest.json", dataclasses.asdict(result))
                return result

        if args.upload_method == "drag":
            drag_files_from_explorer(pyautogui, copied_inputs, window_rect, args.attachment_wait)
        else:
            pyautogui.click(*composer_point)
            time.sleep(0.2)
            set_clipboard_files(copied_inputs)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(args.attachment_wait)

        attached_image, attached_path = screenshot(pyautogui, run_dir, "state_attached", window_rect)
        screenshots["state_attached"] = str(attached_path)
        if image_contains_security_prompt(attached_image):
            result = AttachmentResult(
                AttachmentStatus.BLOCKED_BROWSER_SECURITY_PROMPT,
                str(run_dir),
                branch,
                [str(p) for p in files],
                int((time.time() - start) * 1000),
                "Browser security prompt detected after file paste. Close/cancel it before retrying; do not click Allow automatically.",
                screenshots,
            )
            write_json(run_dir / "result_manifest.json", dataclasses.asdict(result))
            return result
        if text_bridge.image_digest(before_image) == text_bridge.image_digest(attached_image):
            result = AttachmentResult(AttachmentStatus.FAIL_ATTACHMENT_NOT_VISIBLE, str(run_dir), branch, [str(p) for p in files], int((time.time() - start) * 1000), "Screen did not change after file paste.", screenshots)
            write_json(run_dir / "result_manifest.json", dataclasses.asdict(result))
            return result

        send_match, send_button = wait_for_send_ready(
            pyautogui,
            window_rect,
            Path(args.template_dir),
            args.confidence_send,
            args.upload_ready_timeout,
        )
        upload_ready_image, upload_ready_path = screenshot(pyautogui, run_dir, "state_upload_ready", window_rect)
        screenshots["state_upload_ready"] = str(upload_ready_path)
        if not send_match and not send_button:
            result = AttachmentResult(AttachmentStatus.FAIL_NO_SAFE_SEND_BUTTON, str(run_dir), branch, [str(p) for p in files], int((time.time() - start) * 1000), "Safe send button not visible after waiting for attachment upload.", screenshots)
            write_json(run_dir / "result_manifest.json", dataclasses.asdict(result))
            return result

        if not prompt_already_pasted:
            pasted, prompt_path = paste_prompt_after_attachment(pyautogui, pyperclip, prompt, window_rect, run_dir, screenshots)
            if not pasted:
                result = AttachmentResult(AttachmentStatus.FAIL_NO_SAFE_SEND_BUTTON, str(run_dir), branch, [str(p) for p in files], int((time.time() - start) * 1000), "Prompt paste did not visibly change the attachment composer.", screenshots)
                write_json(run_dir / "result_manifest.json", dataclasses.asdict(result))
                return result

        send_match, send_button = wait_for_send_ready(
            pyautogui,
            window_rect,
            Path(args.template_dir),
            args.confidence_send,
            5.0,
        )
        if not send_match and not send_button:
            result = AttachmentResult(AttachmentStatus.FAIL_NO_SAFE_SEND_BUTTON, str(run_dir), branch, [str(p) for p in files], int((time.time() - start) * 1000), "Safe send button not visible after attachment and prompt paste.", screenshots)
            write_json(run_dir / "result_manifest.json", dataclasses.asdict(result))
            return result

        sent_confirmed, sent_image, send_error = click_send_and_confirm(
            pyautogui,
            window_rect,
            Path(args.template_dir),
            args.confidence_send,
            upload_ready_image,
            run_dir,
            screenshots,
            args.send_retries,
            args.send_confirm_timeout,
        )
        if not sent_confirmed or sent_image is None:
            result = AttachmentResult(AttachmentStatus.FAIL_SEND_NOT_CONFIRMED, str(run_dir), branch, [str(p) for p in files], int((time.time() - start) * 1000), send_error, screenshots)
            write_json(run_dir / "result_manifest.json", dataclasses.asdict(result))
            return result

        stable, stable_error = wait_for_new_response_then_stable(
            pyautogui,
            window_rect,
            sent_image,
            args.timeout_finish,
            args.stable_interval,
            args.stable_frames_required,
            run_dir,
            screenshots,
            branch == "image",
        )
        result_image, result_path = screenshot(pyautogui, run_dir, "state_result", window_rect)
        screenshots["state_result"] = str(result_path)
        shutil.copy2(result_path, outputs_dir / "result_screen.png")

        status = AttachmentStatus.PASS_RESULT_SAVED if stable else AttachmentStatus.FAIL_TIMEOUT
        if not stable and stable_error and stable_error.startswith("No new"):
            status = AttachmentStatus.FAIL_NO_NEW_RESPONSE
        if not stable and stable_error and "send arrow" in stable_error.lower():
            status = AttachmentStatus.FAIL_SEND_NOT_CONFIRMED
        error = None if stable else stable_error
        (run_dir / "self_check.md").write_text(
            f"# ChatGPT Web Attachment Bridge Self Check\n\n"
            f"Status: {status}\n\n"
            f"Branch: {branch}\n\n"
            f"Files: {len(files)}\n\n"
            f"Local result screenshot: {outputs_dir / 'result_screen.png'}\n",
            encoding="utf-8",
        )
        result = AttachmentResult(status, str(run_dir), branch, [str(p) for p in files], int((time.time() - start) * 1000), error, screenshots)
        write_json(run_dir / "result_manifest.json", dataclasses.asdict(result))
        return result
    except Exception as exc:
        result = AttachmentResult(AttachmentStatus.FAIL_EXCEPTION, str(run_dir), branch, [str(p) for p in files], int((time.time() - start) * 1000), str(exc), screenshots)
        write_json(run_dir / "result_manifest.json", dataclasses.asdict(result))
        return result
    finally:
        try:
            pyautogui.moveTo(*old_mouse, duration=0.1)
        except Exception:
            pass


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Screenshot-first ChatGPT web attachment bridge for image/video tests.")
    parser.add_argument("--branch", choices=("image", "video"), required=True)
    parser.add_argument("--file", action="append", required=True)
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--purpose", default="test")
    parser.add_argument("--run-root", default=str(Path.cwd() / "runs" / "chatgpt_web_attachment_bridge"))
    parser.add_argument("--window-title-pattern", default=r"(ChatGPT|chatgpt\.com|Image Repair|Request|Response).*Google Chrome")
    parser.add_argument("--template-dir", default=str(TEXT_BRIDGE.parent / "assets" / "templates"))
    parser.add_argument("--confidence-send", type=float, default=0.88)
    parser.add_argument("--attachment-wait", type=float, default=25.0)
    parser.add_argument("--upload-ready-timeout", type=float, default=60.0)
    parser.add_argument("--upload-method", choices=("drag", "clipboard"), default="drag")
    parser.add_argument("--prompt-order", choices=("before", "after"), default="before")
    parser.add_argument("--timeout-finish", type=float, default=240.0)
    parser.add_argument("--stable-frames-required", type=int, default=3)
    parser.add_argument("--stable-interval", type=float, default=0.8)
    parser.add_argument("--send-retries", type=int, default=3)
    parser.add_argument("--send-confirm-timeout", type=float, default=8.0)
    args = parser.parse_args(argv)
    if not args.prompt and not args.prompt_file:
        parser.error("Either --prompt or --prompt-file is required.")
    return args


def main(argv: Sequence[str] | None = None) -> int:
    result = run(parse_args(argv or sys.argv[1:]))
    print(json.dumps(dataclasses.asdict(result), ensure_ascii=False, indent=2))
    return 0 if result.status == AttachmentStatus.PASS_RESULT_SAVED else 2


if __name__ == "__main__":
    raise SystemExit(main())
