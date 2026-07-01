import argparse
import json
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_ROOT / "scripts"
DEFAULT_OUT = SKILL_ROOT / "captures" / "wgc-latest.png"


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def run_json(command: list[str]) -> tuple[int, dict | None, str]:
    proc = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    combined = (proc.stdout or "") + (proc.stderr or "")
    try:
        return proc.returncode, json.loads(proc.stdout), combined
    except json.JSONDecodeError:
        return proc.returncode, None, combined


def capture_windows_capture(args) -> tuple[dict, str]:
    command = [
        sys.executable,
        str(SCRIPTS_DIR / "capture_wgc_once.py"),
        "--out",
        str(args.out),
        "--cursor",
        "true" if args.cursor else "false",
        "--monitor-index",
        str(args.monitor_index),
    ]
    code, data, raw = run_json(command)
    if code != 0 or not data or not data.get("ok"):
        error = data.get("error") if data else raw.strip()
        return {
            "ok": False,
            "backend": "windows-capture",
            "image_path": str(args.out),
            "analysis": None,
            "error": error or "windows-capture failed",
        }, raw
    return data, raw


def analyze(path: Path) -> tuple[dict | None, str]:
    command = [sys.executable, str(SCRIPTS_DIR / "analyze_capture.py"), str(path)]
    code, data, raw = run_json(command)
    if code != 0 and data is None:
        return None, raw
    return data, raw


def main() -> int:
    parser = argparse.ArgumentParser(description="Hermes screenshot capture router.")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output PNG path.")
    parser.add_argument("--backend", default="windows-capture", choices=["windows-capture", "auto", "dxcam", "legacy"])
    parser.add_argument("--cursor", type=parse_bool, default=True, help="Capture cursor: true/false.")
    parser.add_argument("--monitor-index", type=int, default=0, help="0 means primary/auto.")
    parser.add_argument(
        "--allow-legacy",
        action="store_true",
        help="Allow pyautogui/mss legacy fallback. Default is disabled and not implemented here.",
    )
    args = parser.parse_args()
    args.out = Path(args.out).expanduser().resolve()
    args.out.parent.mkdir(parents=True, exist_ok=True)

    if args.backend in {"dxcam", "legacy"}:
        result = {
            "ok": False,
            "backend": args.backend,
            "image_path": str(args.out),
            "analysis": None,
            "error": f"{args.backend} is not enabled. dxcam is not auto-installed; legacy pyautogui/mss is disabled by default.",
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    capture_data, raw_capture = capture_windows_capture(args)
    if not capture_data.get("ok"):
        result = capture_data
        if args.backend == "auto":
            result["error"] = (
                f"{result['error']}; dxcam fallback is available only after explicit installation and is not auto-installed."
            )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    analysis_data, raw_analysis = analyze(args.out)
    ok = bool(analysis_data and analysis_data.get("ok"))
    result = {
        "ok": ok,
        "backend": "windows-capture",
        "image_path": str(args.out),
        "analysis": analysis_data,
        "error": None if ok else (raw_analysis.strip() or "capture analysis failed"),
        "capture": capture_data,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

