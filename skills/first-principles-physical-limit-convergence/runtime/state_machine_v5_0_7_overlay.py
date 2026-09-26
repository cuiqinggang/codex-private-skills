from dataclasses import dataclass
from math import isfinite
from typing import Mapping

ILLEGAL_TEXT = {"N/A", "NA", "NULL", "MISSING", ""}
UNIQUE_OBJECTIVE = "T*=min(T_VALID)"
TOP_LEVEL_T_VALID = "T_CLOSED_LOOP_VALID"

class NumericTimeAnchorViolation(Exception):
    pass

@dataclass(frozen=True)
class NumericTimeAnchor:
    t_closed_loop_elapsed_ms: float
    t_stage_elapsed_ms: float
    t_stage_star_ms: float

def _require(cond: bool, reason: str) -> None:
    if not cond:
        raise NumericTimeAnchorViolation(reason)

def _finite_nonnegative_number(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and isfinite(float(v)) and float(v) >= 0.0

def validate_numeric_time_anchor(anchor: NumericTimeAnchor) -> None:
    values = {
        "T_CLOSED_LOOP_ELAPSED_MS": anchor.t_closed_loop_elapsed_ms,
        "T_STAGE_ELAPSED_MS": anchor.t_stage_elapsed_ms,
        "T_STAGE_STAR_MS": anchor.t_stage_star_ms,
    }
    for name, value in values.items():
        _require(_finite_nonnegative_number(value), f"TIME_ANCHOR_VALUE_INVALID:{name}")
    _require(
        anchor.t_closed_loop_elapsed_ms >= anchor.t_stage_elapsed_ms,
        "CLOSED_LOOP_LT_STAGE_ELAPSED"
    )

def validate_dispatch_visible_snapshot(snapshot: Mapping[str, object]) -> None:
    for name in ("T_CLOSED_LOOP_ELAPSED_MS", "T_STAGE_ELAPSED_MS", "T_STAGE_STAR_MS"):
        _require(name in snapshot, f"TIME_ANCHOR_VALUE_MISSING:{name}")
        value = snapshot[name]
        if isinstance(value, str):
            _require(value not in ILLEGAL_TEXT, f"TIME_ANCHOR_MODEL_VIOLATION:{name}")
        _require(_finite_nonnegative_number(value), f"TIME_ANCHOR_VALUE_INVALID:{name}")
    _require(snapshot.get("UNIQUE_OBJECTIVE") == UNIQUE_OBJECTIVE, "UNIQUE_OBJECTIVE_INVALID")
    _require(snapshot.get("TOP_LEVEL_T_VALID") == TOP_LEVEL_T_VALID, "TOP_LEVEL_T_VALID_INVALID")

def render_numeric_time_tag(snapshot: Mapping[str, object]) -> str:
    validate_dispatch_visible_snapshot(snapshot)
    return (
        "【时间锚｜"
        f"闭环已用={float(snapshot['T_CLOSED_LOOP_ELAPSED_MS']):.3f}ms｜"
        f"本段已用={float(snapshot['T_STAGE_ELAPSED_MS']):.3f}ms｜"
        f"T*={float(snapshot['T_STAGE_STAR_MS']):.6f}ms"
        "】"
    )
