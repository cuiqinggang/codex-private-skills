from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run(path: Path) -> int:
    proc = subprocess.run([sys.executable, str(path)], capture_output=True, text=True, encoding="utf-8")
    print(proc.stdout, end="")
    print(proc.stderr, end="", file=sys.stderr)
    return proc.returncode


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    automation = Path(__file__).resolve().parents[1]
    scripts = automation / "scripts"
    tests = Path(__file__).resolve().parent
    codes = [run(scripts / "run_static_acceptance.py"), run(tests / "simulate_manual_m1.py"), run(tests / "test_readonly_violation.py")]
    if any(codes):
        print("UF9_THREE_ROUND_TEST_FAIL")
        return 1
    print("UF9_THREE_ROUND_TEST_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
