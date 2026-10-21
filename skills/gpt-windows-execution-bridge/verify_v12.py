"""Deterministic simulated route decisions, not live B/C failure tests."""
from route_v12 import decide

base = dict(task_id="V12-TEST", target_device="DESKTOP-4A1EGTM", checkpoint_safe=True)
a_fail = dict(a_probe="FAIL", a_retry="FAIL", a_failure_evidence="two real probe failures")
b_fail = dict(b_probe="FAIL", b_retry="FAIL", b_failure_evidence="two real probe failures")
cases = [
    ("A primary", dict(base, requested_route="A"), True),
    ("A available blocks B", dict(base, requested_route="B", a_probe="PASS", a_retry="FAIL", **{"a_failure_evidence":"x"}), False),
    ("A single failure blocks B", dict(base, requested_route="B", a_probe="FAIL", a_retry="UNKNOWN"), False),
    ("A verified fail allows B", dict(base, requested_route="B", **a_fail), True),
    ("B available blocks C", dict(base, requested_route="C", **a_fail, b_probe="PASS", b_retry="FAIL"), False),
    ("A+B verified fail allows C", dict(base, requested_route="C", **a_fail, **b_fail), True),
    ("unknown checkpoint blocks C", dict(base, requested_route="C", **a_fail, **b_fail, checkpoint_safe=False), False),
    ("no A evidence blocks B", dict(base, requested_route="B", a_probe="FAIL", a_retry="FAIL"), False),
]
for name, data, expected in cases:
    actual, reason = decide(data)
    assert actual == expected, (name, expected, actual, reason)
    print(("PASS" if actual == expected else "FAIL") + " " + name + ": " + reason)
print(f"V12_ROUTE_SIMULATION_PASS {len(cases)}/{len(cases)}")
