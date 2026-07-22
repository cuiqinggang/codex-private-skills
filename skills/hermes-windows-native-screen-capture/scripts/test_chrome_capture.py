import json
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_ROOT / "scripts"
REPORT_PATH = SKILL_ROOT / "reports" / "chrome-capture-test.md"
CAPTURE_PATH = SKILL_ROOT / "captures" / "chrome-capture-test.png"


def run_router() -> tuple[int, dict | None, str]:
    command = [
        sys.executable,
        str(SCRIPTS_DIR / "capture_router.py"),
        "--out",
        str(CAPTURE_PATH),
        "--backend",
        "windows-capture",
    ]
    proc = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    raw = (proc.stdout or "") + (proc.stderr or "")
    try:
        return proc.returncode, json.loads(proc.stdout), raw
    except json.JSONDecodeError:
        return proc.returncode, None, raw


def main() -> int:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    code, data, raw = run_router()
    analysis = data.get("analysis") if data else None
    ok = bool(code == 0 and data and data.get("ok") and analysis and analysis.get("ok"))

    lines = [
        "# Chrome Capture Test",
        "",
        f"PASS: {ok}",
        "",
        "This test does not open a new browser. It captures the current Windows desktop, including any currently open Chrome window, through capture_router.py.",
        "",
        "## Result",
        "",
        f"- Screenshot path: {CAPTURE_PATH}",
        f"- Dimensions: {analysis.get('width', 0) if analysis else 0}x{analysis.get('height', 0) if analysis else 0}",
        f"- File size: {analysis.get('file_size', 0) if analysis else 0} bytes",
        f"- Suspected white screen: {analysis.get('suspected_white_screen') if analysis else None}",
        f"- White pixel ratio: {analysis.get('white_pixel_ratio') if analysis else None}",
        f"- Can be Hermes default screenshot channel: {ok}",
        "",
        "## Raw Router JSON",
        "",
        "```json",
        json.dumps(data if data else {"error": raw}, ensure_ascii=False, indent=2),
        "```",
    ]
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(str(REPORT_PATH))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

