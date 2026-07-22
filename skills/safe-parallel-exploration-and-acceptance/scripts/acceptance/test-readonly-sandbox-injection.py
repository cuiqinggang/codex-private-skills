from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import time
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Inject a violation only into a sandbox copy and prove the source is unchanged.")
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--sandbox", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    sandbox = args.sandbox.resolve()
    if not source.is_file():
        raise SystemExit(f"source not found: {source}")
    if source == sandbox or sandbox == source.parent:
        raise SystemExit("sandbox must be a separate directory")
    before = sha(source)
    sandbox.mkdir(parents=True, exist_ok=True)
    target = sandbox / f"readonly-injection-{int(time.time() * 1000)}{source.suffix}"
    shutil.copy2(source, target)
    os.chmod(target, stat.S_IWRITE)
    with target.open("ab") as stream:
        stream.write(b"\nSIMULATED_READONLY_VIOLATION")
    mutated = sha(target)
    after = sha(source)
    passed = before == after and mutated != before
    result = {"status": "PASS" if passed else "FAIL", "source": str(source), "source_before": before, "source_after": after, "source_unchanged": before == after, "sandbox_copy": str(target), "sandbox_mutation_detected": mutated != before}
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())

