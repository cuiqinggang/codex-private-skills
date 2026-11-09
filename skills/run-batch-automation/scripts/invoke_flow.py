"""Thin handoff: accepted contract arguments to the unchanged original recipe."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='strict')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request', type=Path, required=True)
    args = parser.parse_args()
    matched = subprocess.run(
        [sys.executable, '-X', 'utf8', str(Path(__file__).with_name('match_flow.py')),
         '--request', str(args.request.resolve(strict=True))],
        capture_output=True, text=True, encoding='utf-8', stdin=subprocess.DEVNULL)
    if matched.returncode:
        sys.stderr.write(matched.stderr)
        return matched.returncode
    plan = json.loads(matched.stdout)
    if plan['status'] != 'MATCH':
        print(matched.stdout, end='')
        return 2
    return subprocess.run(plan['argv'], cwd=plan['cwd'],
                          env={**os.environ, **plan['env']},
                          stdin=subprocess.DEVNULL).returncode

if __name__ == '__main__':
    raise SystemExit(main())
