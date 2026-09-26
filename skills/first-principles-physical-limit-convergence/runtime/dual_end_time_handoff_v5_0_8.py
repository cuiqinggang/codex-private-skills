from dataclasses import dataclass
from math import isfinite
from typing import Optional

class DualEndTimeHandoffViolation(Exception):
    pass

@dataclass(frozen=True)
class TimeEnvelope:
    locator: str
    timeline_id: str
    t_closed_loop_elapsed_ms: float
    t_exchange_elapsed_ms: float
    t_star_ms: float
    result: str
    t_real_valid_ms: Optional[float] = None
    t_certificate_elapsed_ms: Optional[float] = None
    certificate_state: Optional[str] = None

def _require(cond: bool, reason: str) -> None:
    if not cond:
        raise DualEndTimeHandoffViolation(reason)

def _num(v) -> bool:
    return isinstance(v,(int,float)) and not isinstance(v,bool) and isfinite(float(v)) and float(v) >= 0.0

def validate_envelope(e: TimeEnvelope, previous_closed_loop_ms=None, expected_timeline_id=None, inherited_t_star_ms=None) -> None:
    _require(bool(e.locator), "LOCATOR_MISSING")
    _require(bool(e.timeline_id), "TIMELINE_ID_MISSING")
    _require(_num(e.t_closed_loop_elapsed_ms), "T_CLOSED_LOOP_INVALID")
    _require(_num(e.t_exchange_elapsed_ms), "T_EXCHANGE_INVALID")
    _require(_num(e.t_star_ms), "T_STAR_INVALID")
    _require(e.result in {"DISPATCH","PASS","FAIL","BLOCKED"}, "RESULT_INVALID")

    if previous_closed_loop_ms is not None:
        _require(e.t_closed_loop_elapsed_ms >= previous_closed_loop_ms, "CLOSED_LOOP_TIME_REVERSED")
    if expected_timeline_id is not None:
        _require(e.timeline_id == expected_timeline_id, "TIMELINE_ID_CHANGED")
    if inherited_t_star_ms is not None:
        _require(abs(e.t_star_ms - inherited_t_star_ms) <= 1e-12, "T_STAR_CHANGED_ACROSS_HANDOFF")

    if e.result == "DISPATCH":
        _require(e.t_real_valid_ms is None, "DISPATCH_MUST_NOT_HAVE_REAL_T")
        return

    _require(_num(e.t_certificate_elapsed_ms), "CERTIFICATE_TIME_MISSING")

    if e.result == "PASS":
        _require(_num(e.t_real_valid_ms), "REAL_T_VALID_MISSING")
    else:
        _require(e.t_real_valid_ms is None, "FAIL_BLOCKED_MUST_NOT_FAKE_REAL_T")
        if e.t_certificate_elapsed_ms == 0.0:
            _require(e.certificate_state == "NOT_STARTED", "ZERO_CERT_TIME_REQUIRES_NOT_STARTED")

def render_visible(e: TimeEnvelope) -> str:
    validate_envelope(e)
    core = (
        f"{e.locator}\n"
        f"【时间锚｜整体已用={e.t_closed_loop_elapsed_ms:.3f}ms"
        f"｜本次已用={e.t_exchange_elapsed_ms:.3f}ms"
        f"｜T*={e.t_star_ms:.6f}ms】"
    )
    if e.result == "PASS":
        return core + f"\nREAL_T={e.t_real_valid_ms:.6f}ms"
    if e.result in {"FAIL","BLOCKED"}:
        return core + f"\n证书计时={e.t_certificate_elapsed_ms:.3f}ms"
    return core
