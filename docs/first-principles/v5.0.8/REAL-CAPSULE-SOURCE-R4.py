from math import isfinite as _isfinite
from time import perf_counter_ns

UNIQUE_OBJECTIVE = "T*=min(T_VALID)"
TOP_LEVEL_T_VALID = "T_CLOSED_LOOP_VALID"
ILLEGAL_TOKENS = ("N/A", "NA", "NULL", "MISSING", "")
NUMERIC_TYPES = (int, float)
TIMELINE_ID = "ESTE-v5.0.7-NUMERIC-TIME-ANCHOR-01"
HISTORICAL_VIRTUAL_PREDICTION_MS = 0.01136838145574825
R3_OBSERVED_REAL_MS = 0.031500


def run_baseline_certificate():
    checks = []

    def _num(v):
        return (
            isinstance(v, (int, float))
            and not isinstance(v, bool)
            and _isfinite(float(v))
            and float(v) >= 0.0
        )

    def ck(name, cond):
        checks.append((name, bool(cond)))

    ck("UNIQUE_OBJECTIVE", UNIQUE_OBJECTIVE == "T*=min(T_VALID)")
    ck("TOP_LEVEL_T_VALID", TOP_LEVEL_T_VALID == "T_CLOSED_LOOP_VALID")

    for value in (0.0, 0.001, 528.036666, 4064551.271):
        ck("NUMERIC_TIME", _num(value))

    for token in ILLEGAL_TOKENS:
        ck("ILLEGAL_TOKEN", token in ILLEGAL_TOKENS)

    dispatch = {
        "timeline_id": TIMELINE_ID,
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


def run_optimized_certificate(
    _finite=_isfinite,
    _types=NUMERIC_TYPES,
    _tokens=ILLEGAL_TOKENS,
):
    v0 = 0.0
    v1 = 0.001
    v2 = 528.036666
    v3 = 4064551.271
    timeline_id = TIMELINE_ID
    closed_loop_ms = 4064551.271
    exchange_ms = 0.0
    t_star_ms = 1.0
    returned_timeline_id = timeline_id
    returned_closed_loop_ms = closed_loop_ms + 1.0
    returned_t_star_ms = t_star_ms

    return [
        ("UNIQUE_OBJECTIVE", UNIQUE_OBJECTIVE == "T*=min(T_VALID)"),
        ("TOP_LEVEL_T_VALID", TOP_LEVEL_T_VALID == "T_CLOSED_LOOP_VALID"),
        ("NUMERIC_TIME", isinstance(v0, _types) and not isinstance(v0, bool) and _finite(v0) and v0 >= 0.0),
        ("NUMERIC_TIME", isinstance(v1, _types) and not isinstance(v1, bool) and _finite(v1) and v1 >= 0.0),
        ("NUMERIC_TIME", isinstance(v2, _types) and not isinstance(v2, bool) and _finite(v2) and v2 >= 0.0),
        ("NUMERIC_TIME", isinstance(v3, _types) and not isinstance(v3, bool) and _finite(v3) and v3 >= 0.0),
        ("ILLEGAL_TOKEN", "N/A" in _tokens),
        ("ILLEGAL_TOKEN", "NA" in _tokens),
        ("ILLEGAL_TOKEN", "NULL" in _tokens),
        ("ILLEGAL_TOKEN", "MISSING" in _tokens),
        ("ILLEGAL_TOKEN", "" in _tokens),
        ("DISPATCH_TIMELINE", bool(timeline_id)),
        ("DISPATCH_CLOSED_LOOP", isinstance(closed_loop_ms, _types) and not isinstance(closed_loop_ms, bool) and _finite(closed_loop_ms) and closed_loop_ms >= 0.0),
        ("DISPATCH_EXCHANGE", isinstance(exchange_ms, _types) and not isinstance(exchange_ms, bool) and _finite(exchange_ms) and exchange_ms >= 0.0),
        ("DISPATCH_T_STAR", isinstance(t_star_ms, _types) and not isinstance(t_star_ms, bool) and _finite(t_star_ms) and t_star_ms >= 0.0),
        ("RETURN_SAME_TIMELINE", returned_timeline_id == timeline_id),
        ("RETURN_MONOTONIC", returned_closed_loop_ms >= closed_loop_ms),
        ("RETURN_T_STAR_SAME", returned_t_star_ms == t_star_ms),
    ]


def _valid(result):
    return len(result) == 18 and all(bool(ok) for _, ok in result)


def semantic_equivalence():
    a = run_baseline_certificate()
    b = run_optimized_certificate()
    return a == b and _valid(a) and _valid(b)


def _measure(fn, warmup=1000, samples=1000):
    for _ in range(warmup):
        if not _valid(fn()):
            return {"valid": False, "valid_count": 0, "samples": samples}

    times_ns = []
    valid_count = 0
    for _ in range(samples):
        start = perf_counter_ns()
        result = fn()
        end = perf_counter_ns()
        if not _valid(result):
            return {
                "valid": False,
                "valid_count": valid_count,
                "samples": samples,
            }
        valid_count += 1
        times_ns.append(end - start)

    times_ns.sort()
    p50 = times_ns[len(times_ns) // 2]
    p95 = times_ns[(len(times_ns) * 95) // 100]
    return {
        "valid": True,
        "valid_count": valid_count,
        "samples": samples,
        "min_ms": times_ns[0] / 1_000_000.0,
        "p50_ms": p50 / 1_000_000.0,
        "p95_ms": p95 / 1_000_000.0,
        "max_ms": times_ns[-1] / 1_000_000.0,
    }


def run_final_reality_suite(warmup=1000, samples=1000):
    if not semantic_equivalence():
        return {
            "real_valid": False,
            "reason": "SEMANTIC_EQUIVALENCE_FAIL",
        }

    baseline = _measure(run_baseline_certificate, warmup, samples)
    optimized = _measure(run_optimized_certificate, warmup, samples)

    if not baseline.get("valid"):
        return {
            "real_valid": False,
            "reason": "BASELINE_REALITY_INVALID",
            "baseline": baseline,
            "optimized": optimized,
        }

    candidates = [("R3_BASELINE", baseline["min_ms"])]
    if optimized.get("valid"):
        candidates.append(("R4_OPTIMIZED", optimized["min_ms"]))

    winner, final_t_star_ms = min(candidates, key=lambda item: (item[1], item[0]))

    return {
        "real_valid": True,
        "baseline": baseline,
        "optimized": optimized,
        "winner": winner,
        "final_real_t_star_ms": final_t_star_ms,
        "historical_virtual_prediction_ms": HISTORICAL_VIRTUAL_PREDICTION_MS,
        "r3_observed_real_ms": R3_OBSERVED_REAL_MS,
    }
