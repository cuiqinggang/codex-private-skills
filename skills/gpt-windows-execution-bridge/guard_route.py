#!/usr/bin/env python3
"""Fail-closed route decision gate; does NOT probe connectivity itself."""
import json,sys
def decide(d):
    route=d.get("requested_route")
    if route not in ("C","A","B"): return False,"INVALID_ROUTE"
    if not d.get("task_id") or not d.get("target_device"): return False,"MISSING_IDENTITY"
    if route=="C": return True,"C_FIRST"
    statuses=[d.get(k) for k in ("c_discovery","c_ping","c_probe","retry_discovery","retry_ping","retry_probe")]
    if "PASS" in statuses: return False,"C_AVAILABLE"
    if "UNKNOWN" in statuses or any(v not in ("FAIL","PASS") for v in statuses): return False,"C_NOT_PROVEN_FAILED"
    if not d.get("c_failure_evidence") or not d.get("retry_failure_evidence"): return False,"NO_FAILURE_EVIDENCE"
    if d.get("checkpoint_safe") is not True: return False,"UNSAFE_CHECKPOINT"
    if route=="B" and (d.get("a_status")!="FAIL" or not d.get("a_failure_evidence")): return False,"A_NOT_PROVEN_FAILED"
    return True,"DOCUMENTED_FALLBACK"
if __name__=="__main__":
    try:
        with open(sys.argv[1],encoding="utf-8") as f:d=json.load(f)
        ok,reason=decide(d)
        print(json.dumps({"decision":"ALLOW" if ok else "DENY","route":d.get("requested_route"),"task_id":d.get("task_id"),"reason":reason},ensure_ascii=False))
        sys.exit(0 if ok else 3)
    except (IndexError,OSError,ValueError) as e:
        print(json.dumps({"decision":"DENY","reason":"INVALID_INPUT","error":str(e)}))
        sys.exit(3)
