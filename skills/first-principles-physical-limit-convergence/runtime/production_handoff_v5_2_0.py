from dataclasses import dataclass
from datetime import datetime, timezone
import re

class ProductionHandoffViolation(Exception):
    pass

_TIME_ANCHOR_RE = re.compile(
    r"【时间锚｜整体已用=\d+(?:\.\d+)?ms｜本次已用=\d+(?:\.\d+)?ms｜T\\?\*=\d+(?:\.\d+)?ms】"
)
_LOCATOR_RE = re.compile(r"【[^\n｜]+｜[^\n｜]+｜(?:0[1-6]|[1-6])｜实】")
_MAX_HEADER_CHARS = 1200

@dataclass(frozen=True)
class ProductionHandoff:
    text: str
    elapsed_ms: float
    turn_elapsed_ms: float
    dispatch_utc: str

def _require(cond, reason):
    if not cond:
        raise ProductionHandoffViolation(reason)

def _parse_utc(value: str) -> datetime:
    _require(isinstance(value, str) and value.strip(), "UTC_TIMESTAMP_REQUIRED")
    v = value.strip()
    if v.endswith("Z"):
        v = v[:-1] + "+00:00"
    dt = datetime.fromisoformat(v)
    _require(dt.tzinfo is not None, "UTC_TIMESTAMP_MUST_BE_OFFSET_AWARE")
    return dt.astimezone(timezone.utc)

def _fmt_utc(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

def _fmt_ms(value: float, decimals: int = 3) -> str:
    _require(value >= 0, "NEGATIVE_TIME_FORBIDDEN")
    s = f"{value:.{decimals}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if "." not in s:
        s += ".000"
    return s

def validate_rendered_dispatch(text: str) -> None:
    _require(bool(text and text.strip()), "DISPATCH_EMPTY")
    _require(_LOCATOR_RE.search(text) is not None, "REAL_LOCATOR_MISSING")
    _require(_TIME_ANCHOR_RE.search(text) is not None, "NUMERIC_TIME_ENVELOPE_MISSING")
    for marker in (
        "TIMELINE_ID=",
        "TIME_ORIGIN_UTC=",
        "DISPATCH_UTC=",
        "FREEZE_ID=",
        "FREEZE_REF=",
        "CONTRACT_REF=",
        "RETURN_TO_GPT=YES",
    ):
        _require(marker in text, marker.rstrip("=") + "_MISSING")
    _require("RESULT=PASS|FAIL|BLOCKED" in text, "RETURN_RESULT_CONTRACT_MISSING")
    _require("NO_FINAL_VALID_DONE=YES" in text, "FINAL_OWNERSHIP_MISSING")
    _require("FROZEN_ASSETS=" not in text, "EXPANDED_ASSET_LIST_FORBIDDEN")
    _require("REALITY_VALID_CONTRACT=" not in text, "EXPANDED_CONTRACT_INLINE_FORBIDDEN")
    header = text.split("\n\n执行：", 1)[0]
    _require(len(header) <= _MAX_HEADER_CHARS, "CONTROL_HEADER_TOO_LONG")

def build_real_dispatch(
    *,
    page_name: str,
    task_name: str,
    task_no: int,
    virtual_mature: bool,
    solution_frozen: bool,
    real_started: bool,
    timeline_id: str,
    time_origin_utc: str,
    turn_start_utc: str,
    dispatch_utc: str,
    freeze_id: str,
    freeze_ref: str,
    contract_ref: str,
    t_star_ms: float,
    executor_task: str,
) -> ProductionHandoff:
    _require(virtual_mature, "VIRTUAL_MATURE_REQUIRED")
    _require(solution_frozen, "SOLUTION_FROZEN_REQUIRED")
    _require(not real_started, "REAL_ALREADY_STARTED")
    _require(1 <= int(task_no) <= 6, "TASK_NO_OUT_OF_RANGE_01_06")
    _require(bool(timeline_id.strip()), "TIMELINE_ID_REQUIRED")
    _require(bool(freeze_id.strip()), "FREEZE_ID_REQUIRED")
    _require(bool(freeze_ref.strip()), "FREEZE_REF_REQUIRED")
    _require(bool(contract_ref.strip()), "CONTRACT_REF_REQUIRED")
    _require(bool(executor_task.strip()), "EXECUTOR_TASK_REQUIRED")

    origin = _parse_utc(time_origin_utc)
    turn_start = _parse_utc(turn_start_utc)
    dispatch = _parse_utc(dispatch_utc)
    _require(dispatch >= origin, "DISPATCH_BEFORE_TIME_ORIGIN")
    _require(dispatch >= turn_start, "DISPATCH_BEFORE_TURN_START")

    elapsed_ms = (dispatch - origin).total_seconds() * 1000.0
    turn_elapsed_ms = (dispatch - turn_start).total_seconds() * 1000.0

    text = f"""【{page_name}｜{task_name}｜{int(task_no):02d}｜实】
【时间锚｜整体已用={_fmt_ms(elapsed_ms)}ms｜本次已用={_fmt_ms(turn_elapsed_ms)}ms｜T*={_fmt_ms(float(t_star_ms), decimals=6)}ms】
TIMELINE_ID={timeline_id}
TIME_ORIGIN_UTC={_fmt_utc(origin)}
DISPATCH_UTC={_fmt_utc(dispatch)}
FREEZE_ID={freeze_id}
FREEZE_REF={freeze_ref}
CONTRACT_REF={contract_ref}

执行：
{executor_task}

返回：
RESULT=PASS|FAIL|BLOCKED
RETURN_TO_GPT=YES
NO_FINAL_VALID_DONE=YES
"""
    validate_rendered_dispatch(text)
    return ProductionHandoff(
        text=text,
        elapsed_ms=elapsed_ms,
        turn_elapsed_ms=turn_elapsed_ms,
        dispatch_utc=_fmt_utc(dispatch),
    )
