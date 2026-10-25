#!/usr/bin/env python3
"""V12 ABC route gate. Requires real probe evidence supplied by caller; does not probe itself."""
import json
import sys

def decide(d):
    route = d.get("requested_route")
    if route not in ("A", "B", "C"):
        return False, "INVALID_ROUTE"
    if not d.get("task_id") or not d.get("target_device"):
        return False, "MISSING_IDENTITY"
    if route == "A":
        return True, "A_PRIMARY"
    if d.get("checkpoint_safe") is not True:
        return False, "UNSAFE_OR_UNKNOWN_EXECUTION"
    for channel in (("A",) if route == "B" else ("A", "B")):
        ch = channel.lower()
        status, retry = d.get(ch + "_probe"), d.get(ch + "_retry")
        if "PASS" in (status, retry):
            return False, channel + "_AVAILABLE"
        if (status, retry) != ("FAIL", "FAIL"):
            return False, channel + "_NOT_PROVEN_FAILED"
        if not str(d.get(ch + "_failure_evidence") or "").strip():
            return False, channel + "_NO_EVIDENCE"
    return True, "DOCUMENTED_FALLBACK"

if __name__ == "__main__":
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            data = json.load(f)
        ok, reason = decide(data)
        print(json.dumps({"decision": "ALLOW" if ok else "DENY",
                          "route": data.get("requested_route"),
                          "task_id": data.get("task_id"), "reason": reason},
                         ensure_ascii=False))
        sys.exit(0 if ok else 3)
    except (IndexError, OSError, ValueError) as e:
        print(json.dumps({"decision": "DENY", "reason": "INVALID_INPUT",
                          "error": str(e)}, ensure_ascii=False))
        sys.exit(3)