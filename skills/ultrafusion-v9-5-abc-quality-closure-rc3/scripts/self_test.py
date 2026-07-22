from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_package.py"
HASHER = ROOT / "scripts" / "hash_manifest.py"


def run(cmd):
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(cmd, text=True, capture_output=True, encoding="utf-8", env=env)


def main() -> int:
    v = run([sys.executable, str(VALIDATOR), "--root", str(ROOT)])
    h = run([sys.executable, str(HASHER), str(ROOT)]) if v.returncode == 0 else None
    result = {
        "overall": "PASS" if v.returncode == 0 and h and h.returncode == 0 else "FAIL",
        "validation": {"returncode": v.returncode, "stdout": v.stdout, "stderr": v.stderr},
        "manifest": None if h is None else {"returncode": h.returncode, "stdout": h.stdout, "stderr": h.stderr},
        "runtime_quality": "PENDING"
    }
    (ROOT / "SELF_TEST_RESULT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["overall"] == "PASS" else 2

if __name__ == "__main__":
    raise SystemExit(main())
