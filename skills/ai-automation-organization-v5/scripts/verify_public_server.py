"""Verify the public HTTPS route against actual local files; keep failures as evidence."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=os.environ.get("AIORG_PUBLIC_ROOT", r"C:\AI\Public-Server"))
    parsed = parser.parse_args()
    root = Path(parsed.root)
    state = json.loads(subprocess.check_output([
        sys.executable, str(root / "public_server.py"), "status"], text=True))
    if state["status"] != "RUNNING":
        raise RuntimeError("Origin and tunnel must be ready before acceptance")
    base = state["public_url"]
    checks = []
    evidence = root / "acceptance.json"
    if evidence.exists():
        archived = root / ("acceptance-" + str(time.time_ns()) + ".json")
        shutil.copy2(evidence, archived)

    def fetch(path, method="GET"):
        started = time.perf_counter()
        request = urllib.request.Request(base + path, method=method)
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return {"path": path, "method": method, "status": response.status,
                        "body": response.read(), "cache_control": response.headers.get("Cache-Control"),
                        "edge": response.headers.get("CF-Ray", "").split("-")[-1],
                        "ms": round((time.perf_counter() - started) * 1000, 3)}
        except urllib.error.HTTPError as response:
            return {"path": path, "method": method, "status": response.code,
                    "body": response.read(), "ms": round((time.perf_counter() - started) * 1000, 3)}

    for path, expected in [("/", (200,)), ("/demo/", (200,)),
                           ("/config.json", (404,)), ("/public_server.py", (404,)),
                           ("/logs/tunnel.log", (404,)), ("/../config.json", (400, 403, 404))]:
        result = fetch(path)
        result["pass"] = result["status"] in expected
        if path == "/":
            result["sha256"] = hashlib.sha256(result["body"]).hexdigest()
            result["pass"] = result["pass"] and result["sha256"] == hashlib.sha256(
                (root / "public" / "index.html").read_bytes()).hexdigest()
        else:
            result["pass"] = result["pass"] and b'"target"' not in result["body"]
        result.pop("body")
        checks.append(result)

    nonce = "LIVE-FROM-LOCAL-PC-" + str(time.time_ns())
    proof = root / "public" / "live-check.txt"
    for text in [nonce, nonce + "-UPDATED"]:
        proof.write_text(text, encoding="ascii")
        result = fetch("/live-check.txt")
        result["pass"] = result["status"] == 200 and result["body"] == text.encode("ascii")
        result.pop("body")
        checks.append(result)
    result = fetch("/", "POST")
    result["pass"] = result["status"] == 501
    result.pop("body")
    checks.append(result)
    report = {"task_id": "AIORG-PUBLICWEB-20261029-001", "version": "1.0.0",
              "scope": "LOCAL_PC_THROUGH_PUBLIC_HTTPS_ROUTE", "public_url": base,
              "checked_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "checks": checks, "passed": sum(item["pass"] for item in checks),
              "total": len(checks), "all_pass": all(item["pass"] for item in checks),
              "independent_external_network": "NOT_VERIFIED_EXECUTOR_EGRESS_BLOCKED"}
    evidence.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True), flush=True)
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
