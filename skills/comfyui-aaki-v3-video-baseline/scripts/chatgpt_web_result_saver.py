from __future__ import annotations

import argparse
import dataclasses
import json
import sys
import time
import uuid
from pathlib import Path
from typing import Sequence

import cv2  # type: ignore
import numpy as np  # type: ignore
from PIL import Image, ImageStat


TEXT_BRIDGE = Path(r"C:\Users\A\.codex\skills\chatgpt-screenshot-bridge\scripts")
if str(TEXT_BRIDGE) not in sys.path:
    sys.path.insert(0, str(TEXT_BRIDGE))

import chatgpt_screenshot_bridge as text_bridge  # type: ignore


class SaveStatus:
    PASS_IMAGE_SAVED = "RESULT_PASS_IMAGE_SAVED"
    FAIL_NO_CHATGPT_WINDOW = "RESULT_FAIL_NO_CHATGPT_WINDOW"
    FAIL_NO_IMAGE_REGION = "RESULT_FAIL_NO_IMAGE_REGION"
    FAIL_RESULT_COUNT_MISMATCH = "RESULT_FAIL_RESULT_COUNT_MISMATCH"
    FAIL_EXCEPTION = "RESULT_FAIL_EXCEPTION"


@dataclasses.dataclass
class SaveResult:
    status: str
    run_dir: str
    output_file: str | None
    elapsed_ms: int
    error: str | None = None
    evidence: dict[str, str] = dataclasses.field(default_factory=dict)
    output_files: list[str] = dataclasses.field(default_factory=list)
    mappings: list[dict] = dataclasses.field(default_factory=list)


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def save_zoom(image: Image.Image, path: Path, scale: int = 2) -> None:
    image.resize((image.width * scale, image.height * scale)).save(path)


def image_is_blank(image: Image.Image) -> bool:
    stat = ImageStat.Stat(image.convert("L"))
    return bool(stat.mean and stat.mean[0] < 3 and stat.stddev[0] < 3)


def screenshot_window(pyautogui, window: text_bridge.Rect) -> Image.Image:
    try:
        import mss  # type: ignore

        with mss.mss() as sct:
            shot = sct.grab(
                {
                    "left": int(window.left),
                    "top": int(window.top),
                    "width": max(1, int(window.width)),
                    "height": max(1, int(window.height)),
                }
            )
            return Image.frombytes("RGB", shot.size, shot.rgb)
    except Exception:
        return pyautogui.screenshot(region=window.as_region())


def ensure_visible_chatgpt_window(pyautogui, window_rect: text_bridge.Rect) -> text_bridge.Rect:
    screen_w, screen_h = pyautogui.size()
    if window_rect.left >= 0 and window_rect.top >= 0 and window_rect.width >= 700 and window_rect.height >= 500:
        return window_rect
    try:
        import pygetwindow as gw  # type: ignore

        candidates = [w for w in gw.getAllWindows() if w.title and ("ChatGPT" in w.title or "chatgpt" in w.title.lower())]
        visible = [w for w in candidates if w.left >= 0 and w.top >= 0 and w.width >= 600 and w.height >= 500]
        target = visible[0] if visible else (candidates[0] if candidates else None)
        if target:
            if target.isMinimized:
                target.restore()
            target.moveTo(0, 0)
            target.resizeTo(min(1600, screen_w), min(1200, screen_h))
            target.activate()
            time.sleep(1.0)
            return text_bridge.Rect(0, 0, min(1600, screen_w), min(1200, screen_h))
    except Exception:
        pass
    return text_bridge.Rect(0, 0, screen_w, screen_h)


def find_largest_image_like_region(image: Image.Image) -> tuple[int, int, int, int] | None:
    regions = find_image_like_regions(image, max_results=1)
    return regions[0] if regions else None


def find_image_like_regions(image: Image.Image, max_results: int = 10) -> list[tuple[int, int, int, int]]:
    arr = np.array(image.convert("RGB"))
    h, w = arr.shape[:2]
    # Ignore browser chrome/sidebar and focus on conversation content.
    x0 = int(w * 0.22)
    y0 = int(h * 0.10)
    crop = arr[y0:int(h * 0.92), x0:int(w * 0.96)]
    gray = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 40, 120)
    kernel = np.ones((7, 7), np.uint8)
    closed = cv2.dilate(edges, kernel, iterations=2)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates: list[tuple[float, int, int, int, int]] = []
    for contour in contours:
        x, y, bw, bh = cv2.boundingRect(contour)
        area = bw * bh
        if area < 30_000:
            continue
        if bw < 120 or bh < 120:
            continue
        ratio = bw / max(bh, 1)
        if ratio < 0.25 or ratio > 4.0:
            continue
        # Avoid giant full-page regions.
        if bw > crop.shape[1] * 0.95 or bh > crop.shape[0] * 0.85:
            continue
        region = crop[y:y + bh, x:x + bw]
        region_gray = gray[y:y + bh, x:x + bw]
        white_fraction = float(np.mean(region_gray > 238))
        dark_fraction = float(np.mean(region_gray < 40))
        color_std = float(np.std(region))
        edge_fraction = float(np.mean(edges[y:y + bh, x:x + bw] > 0))
        # Text bubbles are usually mostly white with sparse black glyph edges.
        if white_fraction > 0.70 and dark_fraction < 0.12:
            continue
        if color_std < 22 and edge_fraction < 0.06:
            continue
        score = area * max(color_std, 1.0) * (1.0 - min(white_fraction, 0.95))
        candidates.append((score, x0 + x, y0 + y, bw, bh))
    regions: list[tuple[int, int, int, int]] = []
    pad = 4
    # Prefer visual order for mapping: top-to-bottom, then left-to-right.
    for _, x, y, bw, bh in sorted(candidates, key=lambda item: (item[2], item[1])):
        left = max(0, x - pad)
        top = max(0, y - pad)
        right = min(w, x + bw + pad)
        bottom = min(h, y + bh + pad)
        overlaps = False
        for old_left, old_top, old_right, old_bottom in regions:
            inter_left = max(left, old_left)
            inter_top = max(top, old_top)
            inter_right = min(right, old_right)
            inter_bottom = min(bottom, old_bottom)
            if inter_right > inter_left and inter_bottom > inter_top:
                inter = (inter_right - inter_left) * (inter_bottom - inter_top)
                area = (right - left) * (bottom - top)
                if inter / max(area, 1) > 0.35:
                    overlaps = True
                    break
        if not overlaps:
            regions.append((left, top, right, bottom))
        if len(regions) >= max_results:
            break
    return regions


def load_source_names(path: str | None) -> list[str]:
    if not path:
        return []
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [Path(str(item)).stem for item in data]
    files = data.get("files", []) if isinstance(data, dict) else []
    names = []
    for item in files:
        if isinstance(item, dict):
            names.append(Path(str(item.get("source") or item.get("local_copy") or item.get("path"))).stem)
        else:
            names.append(Path(str(item)).stem)
    return [name for name in names if name]


def run(args: argparse.Namespace) -> SaveResult:
    start = time.time()
    run_root = Path(args.run_root).resolve()
    run_dir = run_root / f"{time.strftime('%Y%m%d-%H%M%S')}_result_save_{uuid.uuid4().hex[:6]}"
    outputs = run_dir / "local_outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    evidence: dict[str, str] = {}
    try:
        screenshot_path = run_dir / "state_result_full.png"
        if args.screenshot_file:
            img = Image.open(args.screenshot_file).convert("RGB")
        else:
            pyautogui, _, dep_error = text_bridge.import_live_dependencies()
            if dep_error:
                raise RuntimeError(dep_error)
            logger = text_bridge.RunLogger(run_dir / "_detect")
            window = text_bridge.detect_chatgpt_window(
                args.window_title_pattern,
                logger,
                pyautogui=pyautogui,
                allow_browser_window_fallback=True,
            )
            if window is None:
                return SaveResult(
                    SaveStatus.FAIL_NO_CHATGPT_WINDOW,
                    str(run_dir),
                    None,
                    int((time.time() - start) * 1000),
                    "No visible ChatGPT window found.",
                    evidence,
                )
            window = ensure_visible_chatgpt_window(pyautogui, window)
            img = screenshot_window(pyautogui, window)
        img.save(screenshot_path)
        evidence["state_result_full"] = str(screenshot_path)
        if image_is_blank(img):
            return SaveResult(
                SaveStatus.FAIL_NO_IMAGE_REGION,
                str(run_dir),
                None,
                int((time.time() - start) * 1000),
                "ChatGPT result screenshot is blank/black; target window was not visually capturable.",
                evidence,
            )
        regions = find_image_like_regions(img, max_results=args.max_results)
        if not regions:
            return SaveResult(
                SaveStatus.FAIL_NO_IMAGE_REGION,
                str(run_dir),
                None,
                int((time.time() - start) * 1000),
                "No large image-like region found in ChatGPT window.",
                evidence,
            )
        source_names = load_source_names(args.source_manifest)
        output_files: list[str] = []
        mappings: list[dict] = []
        for index, region in enumerate(regions, start=1):
            crop = img.crop(region)
            source_stem = source_names[index - 1] if index - 1 < len(source_names) else f"result_{index:02d}"
            if args.max_results == 1 and args.output_name:
                name = args.output_name
            else:
                name = f"{index:02d}_{source_stem}_repaired.png"
            out_file = outputs / name
            crop.save(out_file)
            output_files.append(str(out_file))
            zoom_file = run_dir / f"{index:02d}_{source_stem}_saved_result_zoom.png"
            save_zoom(crop, zoom_file, 2)
            mappings.append(
                {
                    "index": index,
                    "source_stem": source_stem,
                    "output_file": str(out_file),
                    "region": list(region),
                    "zoom": str(zoom_file),
                }
            )
        evidence["saved_result"] = output_files[0]
        evidence["saved_results_dir"] = str(outputs)
        if args.require_count and len(output_files) < args.require_count:
            result = SaveResult(
                SaveStatus.FAIL_RESULT_COUNT_MISMATCH,
                str(run_dir),
                output_files[0],
                int((time.time() - start) * 1000),
                f"Expected at least {args.require_count} image results, saved {len(output_files)}.",
                evidence,
                output_files,
                mappings,
            )
            write_json(run_dir / "result_manifest.json", dataclasses.asdict(result))
            return result
        result = SaveResult(
            SaveStatus.PASS_IMAGE_SAVED,
            str(run_dir),
            output_files[0],
            int((time.time() - start) * 1000),
            None,
            evidence,
            output_files,
            mappings,
        )
        write_json(run_dir / "result_manifest.json", dataclasses.asdict(result))
        return result
    except Exception as exc:
        result = SaveResult(
            SaveStatus.FAIL_EXCEPTION,
            str(run_dir),
            None,
            int((time.time() - start) * 1000),
            str(exc),
            evidence,
        )
        write_json(run_dir / "result_manifest.json", dataclasses.asdict(result))
        return result


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Save the current visible ChatGPT image result into local_outputs.")
    parser.add_argument("--run-root", default=str(Path.cwd() / "runs" / "chatgpt_web_result_saver"))
    parser.add_argument("--window-title-pattern", default="ChatGPT|chatgpt.com|Bridge validation|Edit Image")
    parser.add_argument("--output-name", default="saved_result.png")
    parser.add_argument("--max-results", type=int, default=1)
    parser.add_argument("--require-count", type=int, default=0)
    parser.add_argument("--source-manifest")
    parser.add_argument("--screenshot-file")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    result = run(parse_args(argv or sys.argv[1:]))
    print(json.dumps(dataclasses.asdict(result), ensure_ascii=False, indent=2))
    return 0 if result.status == SaveStatus.PASS_IMAGE_SAVED else 2


if __name__ == "__main__":
    raise SystemExit(main())
