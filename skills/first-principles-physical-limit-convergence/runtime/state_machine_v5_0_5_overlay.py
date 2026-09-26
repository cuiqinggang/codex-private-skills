from dataclasses import dataclass
from typing import Optional, Tuple

from state_machine_v5_0_3 import (
    Phase, Event, Blocked, EngineState,
    transition as _preserved_transition,
    validate_state as _preserved_validate_state,
)

UNIQUE_OBJECTIVE = "T*=min(T_VALID)"
TOP_LEVEL_T_VALID = "T_CLOSED_LOOP_VALID"
ILLEGAL_TIME_VALUES = frozenset({"N/A", "NA", "NULL", "MISSING", "空值", ""})
REMOTE_UNAVAILABLE = frozenset({
    "NETWORK_UNAVAILABLE",
    "AUTH_UNAVAILABLE",
    "REPOSITORY_UNAVAILABLE",
})


@dataclass(frozen=True)
class SegmentTimeAnchor:
    segment_id: str
    elapsed_ms: float
    extreme_state: str
    local_t_star_ms: Optional[float] = None


@dataclass(frozen=True)
class TimeMasterContext:
    unique_objective: str
    top_level_t_valid: str
    closed_loop_elapsed_ms: float
    anchor_state: str
    virtual_time_closeout_pass: bool
    segments: Tuple[SegmentTimeAnchor, ...]
    remote_status: str = "AVAILABLE"
    source_mode: str = "REMOTE_SHARED_REPO_DIRECT"
    fallback_freeze_explicit: bool = False


def _require(cond: bool, reason: str) -> None:
    if not cond:
        raise Blocked(reason)


def _illegal(v) -> bool:
    return isinstance(v, str) and v in ILLEGAL_TIME_VALUES


def validate_segment_anchor(a: SegmentTimeAnchor, require_frozen: bool = False) -> None:
    _require(bool(a.segment_id), "SEGMENT_ID_MISSING")
    _require(not _illegal(a.extreme_state), "TIME_ANCHOR_MODEL_VIOLATION")
    _require(a.extreme_state in {"PENDING", "SOLVING", "VIRTUAL_FROZEN", "REAL_CERTIFIED"}, "LOCAL_EXTREME_STATE_INVALID")
    _require(a.elapsed_ms >= 0, "LOCAL_ELAPSED_INVALID")
    if require_frozen:
        _require(a.extreme_state in {"VIRTUAL_FROZEN", "REAL_CERTIFIED"}, "LOCAL_TIME_NOT_VIRTUAL_FROZEN")
        _require(a.local_t_star_ms is not None and a.local_t_star_ms >= 0, "LOCAL_T_STAR_MISSING")
    if a.local_t_star_ms is not None:
        _require(a.local_t_star_ms >= 0, "LOCAL_T_STAR_INVALID")


def validate_source_policy(c: TimeMasterContext, phase: Phase) -> None:
    if c.remote_status == "AVAILABLE":
        _require(c.source_mode == "REMOTE_SHARED_REPO_DIRECT", "REMOTE_SOURCE_PRIMARY_PATH_VIOLATION")
        _require(not c.fallback_freeze_explicit, "FALLBACK_NOT_ALLOWED_WHEN_REMOTE_AVAILABLE")
        return
    _require(c.remote_status in REMOTE_UNAVAILABLE, "REMOTE_STATUS_INVALID")
    if phase == Phase.REAL:
        raise Blocked("REMOTE_REPO_UNAVAILABLE_RETURN_TO_GPT")
    if c.source_mode in {"DOWNLOAD_PACKAGE", "LOCAL_COPY", "INLINE_COPY"}:
        _require(c.fallback_freeze_explicit, "FALLBACK_REQUIRES_NEW_EXPLICIT_FREEZE")


def validate_time_master(c: TimeMasterContext, phase: Phase, event: Optional[Event] = None) -> None:
    _require(c.unique_objective == UNIQUE_OBJECTIVE, "UNIQUE_OBJECTIVE_INVALID")
    _require(c.top_level_t_valid == TOP_LEVEL_T_VALID, "TOP_LEVEL_T_VALID_INVALID")
    _require(not _illegal(c.anchor_state), "TIME_ANCHOR_MODEL_VIOLATION")
    _require(c.anchor_state in {"PENDING", "SOLVING", "VIRTUAL_FROZEN", "REAL_CERTIFIED"}, "ANCHOR_STATE_INVALID")
    _require(c.closed_loop_elapsed_ms >= 0, "CLOSED_LOOP_ELAPSED_INVALID")
    _require(len(c.segments) > 0, "TIME_SEGMENT_SET_EMPTY")
    validate_source_policy(c, phase)

    require_frozen = event == Event.FREEZE_TO_REAL
    for seg in c.segments:
        validate_segment_anchor(seg, require_frozen=require_frozen)

    if event == Event.FREEZE_TO_REAL:
        _require(c.virtual_time_closeout_pass, "VIRTUAL_TIME_CLOSEOUT_REQUIRED")
        _require(c.anchor_state == "VIRTUAL_FROZEN", "VIRTUAL_ANCHOR_NOT_FROZEN")


def _assert_preserved_transition(before: EngineState, event: Event, after: EngineState) -> None:
    if event == Event.FREEZE_TO_REAL:
        _require(before.phase == Phase.VIRTUAL and after.phase == Phase.REAL, "STATE_MACHINE_PRESERVATION_BREACH")
    elif event == Event.REAL_PASS:
        _require(before.phase == Phase.REAL and after.phase == Phase.REAL and after.done, "STATE_MACHINE_PRESERVATION_BREACH")
    elif event == Event.REAL_FAIL:
        _require(before.phase == Phase.REAL and after.phase == Phase.VIRTUAL, "STATE_MACHINE_PRESERVATION_BREACH")
        _require(before.timeline_id == after.timeline_id, "TIMELINE_REBUILD_FORBIDDEN")
        _require(before.time_origin_utc == after.time_origin_utc, "TIME_ORIGIN_REBUILD_FORBIDDEN")


def transition(s: EngineState, event: Event, payload, time_master: TimeMasterContext):
    """
    v5.0.5 is an additive guard over the v5.0.3 state machine.
    The preserved transition executes unchanged; time control may block,
    but may never rewrite the legal transition result.
    """
    _preserved_validate_state(s)
    validate_time_master(time_master, s.phase, event)
    out = _preserved_transition(s, event, payload)
    _assert_preserved_transition(s, event, out)
    return out
