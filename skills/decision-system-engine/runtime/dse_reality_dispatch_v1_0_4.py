from dataclasses import dataclass
import importlib.util
from pathlib import Path

DSE_VERSION = "1.0.4"

class DSEDispatchViolation(Exception):
    pass

@dataclass(frozen=True)
class DSEDispatch:
    text: str
    elapsed_ms: float
    turn_elapsed_ms: float
    dispatch_utc: str

def _require(cond, reason):
    if not cond:
        raise DSEDispatchViolation(reason)

def _load_parent_renderer():
    skills_dir = Path(__file__).resolve().parents[2]
    parent = (
        skills_dir
        / "first-principles-physical-limit-convergence"
        / "runtime"
        / "production_handoff_v5_2_0.py"
    )
    _require(parent.exists(), "PARENT_RENDERER_NOT_FOUND")
    spec = importlib.util.spec_from_file_location("este_production_handoff", parent)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def validate_dse_dispatch(text: str) -> str:
    parent = _load_parent_renderer()
    parent.validate_rendered_dispatch(text)

    _require(f"DSE_VERSION={DSE_VERSION}" in text, "DSE_VERSION_MISSING")
    _require("DSE_LOGIC_FREEZE_ID=" in text, "DSE_LOGIC_FREEZE_ID_MISSING")
    _require("T_STAR_STATUS=" in text, "T_STAR_STATUS_MISSING")
    _require("\n\n执行：\n" in text, "EXECUTION_BODY_MISSING")

    body = text.split("\n\n执行：\n", 1)[1].split("\n\n返回：", 1)[0].strip()
    _require(bool(body), "EXECUTION_BODY_EMPTY")
    _require(
        "RESULT=PASS|FAIL|BLOCKED" in text
        and "RETURN_TO_GPT=YES" in text
        and "NO_FINAL_VALID_DONE=YES" in text,
        "RETURN_CONTRACT_INCOMPLETE",
    )
    return "DSE_DISPATCH_VALID"

def build_dse_real_dispatch(
    *,
    task_name: str,
    task_no: int,
    timeline_id: str,
    time_origin_utc: str,
    turn_start_utc: str,
    dispatch_utc: str,
    integration_freeze_id: str,
    freeze_ref: str,
    contract_ref: str,
    dse_logic_freeze_id: str,
    t_star_reference_ms: float,
    executor_task: str,
) -> DSEDispatch:
    parent = _load_parent_renderer()
    base = parent.build_real_dispatch(
        page_name="决策系统引擎1",
        task_name=task_name,
        task_no=task_no,
        virtual_mature=True,
        solution_frozen=True,
        real_started=False,
        timeline_id=timeline_id,
        time_origin_utc=time_origin_utc,
        turn_start_utc=turn_start_utc,
        dispatch_utc=dispatch_utc,
        freeze_id=integration_freeze_id,
        freeze_ref=freeze_ref,
        contract_ref=contract_ref,
        t_star_ms=float(t_star_reference_ms),
        executor_task=executor_task,
    )

    insert = (
        f"CONTRACT_REF={contract_ref}\n"
        f"DSE_VERSION={DSE_VERSION}\n"
        f"DSE_LOGIC_FREEZE_ID={dse_logic_freeze_id}\n"
        "T_STAR_STATUS=VIRTUAL_REFERENCE_PENDING_REAL_USAGE_TEST\n"
    )
    text = base.text.replace(f"CONTRACT_REF={contract_ref}\n", insert, 1)
    validate_dse_dispatch(text)
    return DSEDispatch(
        text=text,
        elapsed_ms=base.elapsed_ms,
        turn_elapsed_ms=base.turn_elapsed_ms,
        dispatch_utc=base.dispatch_utc,
    )
