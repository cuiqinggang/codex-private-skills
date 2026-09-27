from dataclasses import dataclass, asdict
from enum import IntEnum
import importlib.util
from pathlib import Path

class State(IntEnum):
    NEW = 0
    VIRTUAL = 10
    VIRTUAL_MATURE = 20
    FROZEN = 30          # transient: cannot be returned to user
    REAL_DISPATCHED = 40
    BLOCKED = 90
    FINAL_VALID = 100

class FSMViolation(Exception):
    pass

@dataclass
class Machine:
    state: int = int(State.NEW)
    last_result: str = "NONE"
    cycle: int = 0
    freeze_id: str = ""
    timeline_id: str = ""

    def snapshot(self):
        data = asdict(self)
        data["state_name"] = State(self.state).name
        return data

def _require(cond, reason):
    if not cond:
        raise FSMViolation(reason)

def _scope_gate():
    runtime_dir = Path(__file__).resolve().parent
    path = runtime_dir / "scope_gate_v5_2_2.py"
    _require(path.exists(), "SCOPE_GATE_NOT_FOUND")
    spec = importlib.util.spec_from_file_location("scope_gate_v5_2_2", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def start(machine: Machine) -> Machine:
    _require(machine.state == State.NEW, "START_REQUIRES_NEW")
    machine.state = int(State.VIRTUAL)
    machine.cycle += 1
    return machine

def mark_virtual_mature(machine: Machine) -> Machine:
    _require(machine.state == State.VIRTUAL, "VIRTUAL_MATURE_REQUIRES_VIRTUAL")
    machine.state = int(State.VIRTUAL_MATURE)
    return machine

def freeze_and_dispatch(machine: Machine, **dispatch_kwargs):
    """
    Atomic control boundary:
      VIRTUAL_MATURE -> FROZEN -> REAL_DISPATCHED

    There is deliberately no freeze_only() API.
    Once Freeze succeeds, this function MUST build and validate the complete
    Reality Dispatch before returning.
    """
    _require(machine.state == State.VIRTUAL_MATURE, "FREEZE_REQUIRES_VIRTUAL_MATURE")
    freeze_id = str(dispatch_kwargs.get("freeze_id", "")).strip()
    timeline_id = str(dispatch_kwargs.get("timeline_id", "")).strip()
    _require(freeze_id, "FREEZE_ID_REQUIRED")
    _require(timeline_id, "TIMELINE_ID_REQUIRED")

    machine.state = int(State.FROZEN)
    machine.freeze_id = freeze_id
    machine.timeline_id = timeline_id

    gate = _scope_gate()
    try:
        out = gate.build_in_scope_real_dispatch(**dispatch_kwargs)
        gate.enforce_in_scope_final_output(out.text)
    except Exception:
        # Freeze cannot be exposed as a successful terminal state if dispatch fails.
        machine.state = int(State.VIRTUAL)
        machine.last_result = "DISPATCH_BUILD_FAIL"
        raise

    machine.state = int(State.REAL_DISPATCHED)
    machine.last_result = "DISPATCHED"
    return machine, out

def apply_reality_result(machine: Machine, result: str) -> Machine:
    _require(machine.state == State.REAL_DISPATCHED, "REAL_RESULT_REQUIRES_REAL_DISPATCHED")
    r = str(result).upper().strip()
    _require(r in {"PASS", "FAIL", "BLOCKED"}, "UNKNOWN_REAL_RESULT")
    machine.last_result = r

    if r == "PASS":
        machine.state = int(State.FINAL_VALID)
    elif r == "FAIL":
        machine.state = int(State.VIRTUAL)
        machine.cycle += 1
        machine.freeze_id = ""
    else:
        machine.state = int(State.BLOCKED)

    return machine

def resume_blocked(machine: Machine) -> Machine:
    _require(machine.state == State.BLOCKED, "RESUME_REQUIRES_BLOCKED")
    machine.state = int(State.VIRTUAL)
    machine.cycle += 1
    machine.freeze_id = ""
    return machine

def may_end_user_reply(machine: Machine) -> bool:
    """
    Mechanical end gate.
    A reply MUST NOT end while virtual maturity has been reached but Reality
    has not been dispatched. FROZEN is internal-only and can never be terminal.
    """
    return machine.state not in {int(State.VIRTUAL_MATURE), int(State.FROZEN)}

def require_reply_may_end(machine: Machine) -> str:
    _require(may_end_user_reply(machine), "REPLY_END_FORBIDDEN_BEFORE_REAL_DISPATCH")
    return "REPLY_END_ALLOWED"
