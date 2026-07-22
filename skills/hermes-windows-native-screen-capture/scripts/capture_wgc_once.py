import argparse
import json
import time
from pathlib import Path

from windows_capture import WindowsCapture


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = SKILL_ROOT / "captures" / "wgc-latest.png"


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def effective_monitor_index(requested_index: int) -> int:
    # windows-capture 2.0.0 on the proof machine rejects index 0.
    return 1 if requested_index <= 0 else requested_index


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture one Windows Graphics Capture frame.")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output PNG path.")
    parser.add_argument("--cursor", type=parse_bool, default=True, help="Capture cursor: true/false.")
    parser.add_argument(
        "--monitor-index",
        type=int,
        default=0,
        help="Requested monitor index. 0 means primary/auto and maps to native index 1.",
    )
    args = parser.parse_args()

    image_path = Path(args.out).expanduser().resolve()
    image_path.parent.mkdir(parents=True, exist_ok=True)

    started = time.perf_counter()
    result = {
        "ok": False,
        "backend": "windows-capture",
        "image_path": str(image_path),
        "width": None,
        "height": None,
        "file_size": 0,
        "duration_ms": None,
        "requested_monitor_index": args.monitor_index,
        "effective_monitor_index": effective_monitor_index(args.monitor_index),
        "error": None,
    }

    try:
        capture = WindowsCapture(
            cursor_capture=args.cursor,
            monitor_index=result["effective_monitor_index"],
        )

        @capture.event
        def on_frame_arrived(frame, control):
            frame.save_as_image(str(image_path))
            result.update(
                {
                    "ok": True,
                    "width": int(frame.width),
                    "height": int(frame.height),
                }
            )
            control.stop()

        @capture.event
        def on_closed():
            pass

        capture.start()
        if image_path.exists():
            result["file_size"] = image_path.stat().st_size
        result["duration_ms"] = int((time.perf_counter() - started) * 1000)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1
    except Exception as exc:
        result["duration_ms"] = int((time.perf_counter() - started) * 1000)
        result["error"] = str(exc)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

