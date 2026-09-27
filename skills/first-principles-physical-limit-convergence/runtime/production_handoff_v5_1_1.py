from dataclasses import dataclass
from datetime import datetime, timezone
import re

class ProductionHandoffViolation(Exception):
    pass

_TIME_ANCHOR_RE = re.compile(
    r"【时间锚｜整体已用=\\d+(?:\\.\\d+)?ms｜本次已用=\\d+(?:\\.\\d+)?ms｜T\\*=\\d+(?:\\.\\d+)?ms】"
)
_LOCATOR_RE = re.compile(r"【[^\\n｜]+｜[^\\n｜]+｜(?:0[1-6]|[1-6])｜实】")

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

def _fmt_ms(value: float, *, decimals: int = 3) -> str:
    _require(value >= 0, "NEGATIVE_TIME_FORBIDDEN")
    s = f"{value:.{decimals}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if "." not in s:
        s += ".000"
    return s

def _validate_rendered_dispatch(text: str) -> None:
    _require(_LOCATOR_RE.search(text) is not None, "REAL_LOCATOR_MISSING")
    _require(_TIME_ANCHOR_RE.search(text) is not None, "NUMERIC_TIME_ENVELOPE_MISSING")
    for marker in (
        "TIMELINE_ID=",
        "TIME_ORIGIN_UTC=",
        "DISPATCH_UTC=",
        "FREEZE_ID=",
        "REALITY_VALID_CONTRACT=",
        "REALITY_TIMING_BOUNDARY=",
        "RETURN_TO_GPT=YES",
    ):
        _require(marker in text, marker.rstrip("=") + "_MISSING")
    _require("PASS / FAIL / BLOCKED" in text, "RETURN_RESULT_CONTRACT_MISSING")
    _require("FINAL_VALID/DONE 禁止由 Reality 执行器宣布" in text, "FINAL_OWNERSHIP_MISSING")

def close_virtual_and_build_real_dispatch(
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
    frozen_assets: str,
    reality_valid_contract: str,
    reality_timing_boundary: str,
    t_star_ms: float,
    t_star_source: str,
    executor_task: str,
) -> ProductionHandoff:
    """
    唯一生产 Reality Dispatch 出口。

    一旦 VIRTUAL_MATURE=YES 且 SOLUTION_FROZEN=YES 且 REAL_STARTED=NO，
    本函数不返回“冻结完成/等待下一步”，而是直接生成完整的 Codex CHAT 实命令。
    """
    _require(virtual_mature, "VIRTUAL_MATURE_REQUIRED")
    _require(solution_frozen, "SOLUTION_FROZEN_REQUIRED")
    _require(not real_started, "REAL_ALREADY_STARTED")
    _require(1 <= int(task_no) <= 6, "TASK_NO_OUT_OF_RANGE_01_06")
    _require(bool(timeline_id.strip()), "TIMELINE_ID_REQUIRED")
    _require(bool(freeze_id.strip()), "FREEZE_ID_REQUIRED")
    _require(bool(frozen_assets.strip()), "FROZEN_ASSETS_REQUIRED")
    _require(bool(reality_valid_contract.strip()), "REALITY_VALID_CONTRACT_REQUIRED")
    _require(bool(reality_timing_boundary.strip()), "REALITY_TIMING_BOUNDARY_REQUIRED")
    _require(bool(t_star_source.strip()), "T_STAR_SOURCE_REQUIRED")
    _require(bool(executor_task.strip()), "EXECUTOR_TASK_REQUIRED")

    origin = _parse_utc(time_origin_utc)
    turn_start = _parse_utc(turn_start_utc)
    dispatch = _parse_utc(dispatch_utc)
    _require(dispatch >= origin, "DISPATCH_BEFORE_TIME_ORIGIN")
    _require(dispatch >= turn_start, "DISPATCH_BEFORE_TURN_START")

    elapsed_ms = (dispatch - origin).total_seconds() * 1000.0
    turn_elapsed_ms = (dispatch - turn_start).total_seconds() * 1000.0

    locator = f"【{page_name}｜{task_name}｜{int(task_no):02d}｜实】"
    anchor = (
        "【时间锚｜整体已用="
        + _fmt_ms(elapsed_ms)
        + "ms｜本次已用="
        + _fmt_ms(turn_elapsed_ms)
        + "ms｜T*="
        + _fmt_ms(float(t_star_ms), decimals=6)
        + "ms】"
    )

    text = f"""{locator}
{anchor}
TIMELINE_ID={timeline_id}
TIME_ORIGIN_UTC={_fmt_utc(origin)}
DISPATCH_UTC={_fmt_utc(dispatch)}
FREEZE_ID={freeze_id}
VIRTUAL_MATURE=YES
SOLUTION_FROZEN=YES
REAL_STARTED=YES
T_STAR_SOURCE={t_star_source}
FROZEN_ASSETS={frozen_assets}
REALITY_VALID_CONTRACT={reality_valid_contract}
REALITY_TIMING_BOUNDARY={reality_timing_boundary}

执行任务：
{executor_task}

返回合同：
- 只允许 PASS / FAIL / BLOCKED 三种 Reality 结果。
- 三种结果都必须保留同一 TIMELINE_ID，并给出真实起止时间与毫秒。
- PASS / FAIL / BLOCKED 均必须 RETURN_TO_GPT=YES。
- FINAL_VALID/DONE 禁止由 Reality 执行器宣布；最终收口权属于 GPT。
RETURN_TO_GPT=YES
"""
    _validate_rendered_dispatch(text)
    return ProductionHandoff(
        text=text,
        elapsed_ms=elapsed_ms,
        turn_elapsed_ms=turn_elapsed_ms,
        dispatch_utc=_fmt_utc(dispatch),
    )
