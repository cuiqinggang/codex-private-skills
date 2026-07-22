import json
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_ROOT / "scripts"
REPORT_PATH = SKILL_ROOT / "reports" / "verification-result.md"
CAPTURE_PATH = SKILL_ROOT / "captures" / "wgc-latest.png"
ANALYSIS_REPORT = SKILL_ROOT / "reports" / "verification-analysis.json"


def run(command: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return proc.returncode, proc.stdout or "", proc.stderr or ""


def load_json(text: str) -> dict | None:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def main() -> int:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    router_cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "capture_router.py"),
        "--out",
        str(CAPTURE_PATH),
    ]
    router_code, router_stdout, router_stderr = run(router_cmd)
    router_json = load_json(router_stdout)

    analyze_cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "analyze_capture.py"),
        str(CAPTURE_PATH),
        "--report",
        str(ANALYSIS_REPORT),
    ]
    analyze_code, analyze_stdout, analyze_stderr = run(analyze_cmd)
    analysis_json = load_json(analyze_stdout)

    checks = {
        "router_exit_0": router_code == 0,
        "router_ok": bool(router_json and router_json.get("ok")),
        "analysis_exit_0": analyze_code == 0,
        "analysis_ok": bool(analysis_json and analysis_json.get("ok")),
        "png_exists": CAPTURE_PATH.exists(),
        "not_white_screen": bool(analysis_json and not analysis_json.get("suspected_white_screen")),
    }
    pass_all = all(checks.values())

    lines = [
        "# Verification Result",
        "",
        f"Status: {'PASS' if pass_all else 'FAIL'}",
        "",
        "## Checks",
        "",
    ]
    for key, value in checks.items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Capture",
            "",
            f"- Path: {CAPTURE_PATH}",
            f"- Width: {analysis_json.get('width', 0) if analysis_json else 0}",
            f"- Height: {analysis_json.get('height', 0) if analysis_json else 0}",
            f"- File size: {analysis_json.get('file_size', 0) if analysis_json else 0}",
            f"- Suspected white screen: {analysis_json.get('suspected_white_screen') if analysis_json else None}",
            "",
            "## Commands",
            "",
            "```text",
            " ".join(router_cmd),
            " ".join(analyze_cmd),
            "```",
            "",
            "## Router JSON",
            "",
            "```json",
            json.dumps(router_json if router_json else {"stdout": router_stdout, "stderr": router_stderr}, ensure_ascii=False, indent=2),
            "```",
            "",
            "## Analysis JSON",
            "",
            "```json",
            json.dumps(analysis_json if analysis_json else {"stdout": analyze_stdout, "stderr": analyze_stderr}, ensure_ascii=False, indent=2),
            "```",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(str(REPORT_PATH))
    return 0 if pass_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
