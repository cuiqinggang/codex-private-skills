import argparse
import json
from pathlib import Path

import cv2
import numpy as np


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMAGE = SKILL_ROOT / "captures" / "wgc-latest.png"


def analyze_image(path: Path) -> dict:
    result = {
        "ok": False,
        "image_path": str(path),
        "exists": path.exists(),
        "width": 0,
        "height": 0,
        "file_size": 0,
        "mean_brightness": None,
        "white_pixel_ratio": None,
        "non_white_pixel_ratio": None,
        "suspected_white_screen": True,
        "suspected_failure": True,
        "failure_reasons": [],
    }

    if not path.exists():
        result["failure_reasons"].append("image_missing")
        return result

    result["file_size"] = path.stat().st_size
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        result["failure_reasons"].append("image_unreadable")
        return result

    height, width = image.shape[:2]
    result["width"] = int(width)
    result["height"] = int(height)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    white_mask = np.all(image >= 250, axis=2)
    white_ratio = float(np.mean(white_mask))

    result["mean_brightness"] = float(np.mean(gray))
    result["white_pixel_ratio"] = white_ratio
    result["non_white_pixel_ratio"] = float(1.0 - white_ratio)
    result["suspected_white_screen"] = white_ratio > 0.90

    if result["suspected_white_screen"]:
        result["failure_reasons"].append("white_pixel_ratio_gt_90_percent")
    if result["file_size"] < 100 * 1024:
        result["failure_reasons"].append("file_size_lt_100kb")
    if width < 1000 or height < 600:
        result["failure_reasons"].append("dimensions_lt_1000x600")

    result["suspected_failure"] = bool(result["failure_reasons"])
    result["ok"] = not result["suspected_failure"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze a captured PNG for size and white-screen failure.")
    parser.add_argument("image", nargs="?", default=str(DEFAULT_IMAGE), help="Image path to analyze.")
    parser.add_argument("--report", help="Optional JSON report path.")
    args = parser.parse_args()

    data = analyze_image(Path(args.image).expanduser().resolve())
    if args.report:
        report_path = Path(args.report).expanduser().resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

