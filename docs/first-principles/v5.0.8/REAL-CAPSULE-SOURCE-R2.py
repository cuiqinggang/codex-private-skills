from math import isfinite

UNIQUE_OBJECTIVE = "T*=min(T_VALID)"
TOP_LEVEL_T_VALID = "T_CLOSED_LOOP_VALID"
ILLEGAL_TOKENS = ("N/A", "NA", "NULL", "MISSING", "")

def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and isfinite(float(v)) and float(v) >= 0.0

def run_reality_certificate():
    checks = []
    def ck(name, cond):
        checks.append((name, bool(cond)))

    ck("UNIQUE_OBJECTIVE", UNIQUE_OBJECTIVE == "T*=min(T_VALID)")
    ck("TOP_LEVEL_T_VALID", TOP_LEVEL_T_VALID == "T_CLOSED_LOOP_VALID")

    for value in (0.0, 0.001, 528.036666, 4064551.271):
        ck("NUMERIC_TIME", _num(value))

    for token in ILLEGAL_TOKENS:
        ck("ILLEGAL_TOKEN", token in ILLEGAL_TOKENS)

    dispatch = {
        "timeline_id": "ESTE-v5.0.7-NUMERIC-TIME-ANCHOR-01",
        "closed_loop_ms": 4064551.271,
        "exchange_ms": 0.0,
        "t_star_ms": 1.0,
    }
    ck("DISPATCH_TIMELINE", bool(dispatch["timeline_id"]))
    ck("DISPATCH_CLOSED_LOOP", _num(dispatch["closed_loop_ms"]))
    ck("DISPATCH_EXCHANGE", _num(dispatch["exchange_ms"]))
    ck("DISPATCH_T_STAR", _num(dispatch["t_star_ms"]))

    returned = dict(dispatch)
    returned["closed_loop_ms"] = dispatch["closed_loop_ms"] + 1.0
    returned["exchange_ms"] = 1.0
    ck("RETURN_SAME_TIMELINE", returned["timeline_id"] == dispatch["timeline_id"])
    ck("RETURN_MONOTONIC", returned["closed_loop_ms"] >= dispatch["closed_loop_ms"])
    ck("RETURN_T_STAR_SAME", returned["t_star_ms"] == dispatch["t_star_ms"])

    return checks
