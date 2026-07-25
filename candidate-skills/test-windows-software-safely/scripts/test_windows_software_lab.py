#!/usr/bin/env python3
"""Cross-platform lab contract tests; never invokes Hyper-V."""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = list((ROOT / "scripts").glob("*.ps1"))


def validate(plan: dict) -> None:
    assert plan["networkMode"] in {"None", "Private"}
    assert plan["disposableConfirmed"] is True
    assert re.fullmatch(r"[a-f0-9]{64}", plan["guestPayloadSha256"])
    assert plan["maxGuestReboots"] <= 10
    forbidden_keys = {"credential", "password", "command", "hostReboot"}
    assert not forbidden_keys.intersection(plan)


def action_gate(action: str, payload_present: bool, payload_hash_ok: bool, expired: bool) -> bool:
    if action == "Restore":
        return True
    if expired:
        return False
    if action in {"Prepare", "ExecutePayload", "RestartGuest"}:
        return payload_present and payload_hash_ok
    return True


def verify_restore(marker_exists: bool) -> None:
    assert not marker_exists


def network_isolated(mode: str, expected_ids: list[str], adapters: list[dict], private_switch_id: str | None = None) -> bool:
    if sorted(a["id"] for a in adapters) != sorted(expected_ids):
        return False
    if mode == "None":
        return all(not a["switchId"] for a in adapters)
    if mode == "Private":
        return all(a["switchType"] == "Private" and a["switchId"] == private_switch_id for a in adapters)
    return False


def main() -> int:
    text = "\n".join(path.read_text(encoding="utf-8") for path in SCRIPTS)
    for token in [
        "Checkpoint-VM", "Restore-VMSnapshot", "Disconnect-VMNetworkAdapter", "Restart-VM",
        "ApprovePlanHash", "Copy-VMFile", "Invoke-Command", "guestExitCode",
        "BASELINE_RESTORE_VERIFIED", "test marker still exists",
        "Assert-NetworkIsolation", "VM network adapter set drifted", "Private switch identity or type drifted",
    ]:
        assert token in text, token
    forbidden = [
        r"\bRestart-Computer\b",
        r"\bStop-Computer\b",
        r"New-VMSwitch.+-SwitchType\s+External",
        r"\bSet-VMHost\b",
        r"\bRemove-VM\b",
        r"Invoke-Expression",
        r"\biex\b",
        r"ExecutionPolicy\s+Bypass",
    ]
    for pattern in forbidden:
        assert not re.search(pattern, text, re.IGNORECASE), pattern

    digest = hashlib.sha256(b"benign guest fixture").hexdigest()
    plan = {
        "schemaVersion": 1,
        "kind": "windows-software-test-plan",
        "runId": "fixture",
        "host": "fixture-host",
        "vmName": "disposable-fixture",
        "vmId": "fixture-id",
        "disposableConfirmed": True,
        "scenarioName": "two-reboot-fixture",
        "networkMode": "None",
        "privateSwitchId": None,
        "initialAdapterIds": ["adapter-1"],
        "guestPayloadPath": "C:\\LabPayloads\\fixture.ps1",
        "guestPayloadSha256": digest,
        "guestPayloadDestination": "C:\\ProgramData\\WindowsSoftwareTestLab\\fixture\\payload.ps1",
        "testMarkerPath": "C:\\ProgramData\\WindowsSoftwareTestLab\\fixture\\executed.marker",
        "maxGuestReboots": 2,
    }
    validate(plan)
    assert action_gate("Restore", payload_present=False, payload_hash_ok=False, expired=True)
    assert not action_gate("ExecutePayload", payload_present=False, payload_hash_ok=True, expired=False)
    assert network_isolated("None", ["adapter-1"], [{"id": "adapter-1", "switchId": None, "switchType": None}])
    assert not network_isolated("None", ["adapter-1"], [
        {"id": "adapter-1", "switchId": None, "switchType": None},
        {"id": "adapter-evil", "switchId": "external", "switchType": "External"},
    ])
    assert not network_isolated("Private", ["adapter-1"], [{"id": "adapter-1", "switchId": "wrong", "switchType": "Private"}], "pinned")
    try:
        verify_restore(marker_exists=True)
    except AssertionError:
        pass
    else:
        raise AssertionError("restore accepted a surviving test marker")
    lab_text = (ROOT / "scripts" / "Invoke-WindowsSoftwareTestLab.ps1").read_text(encoding="utf-8")
    assert "$event.restoreAttempted=$true" in lab_text
    bad = dict(plan, networkMode="External")
    try:
        validate(bad)
    except AssertionError:
        pass
    else:
        raise AssertionError("External networking was accepted")
    with tempfile.TemporaryDirectory(prefix="windows-lab-fixture-") as folder:
        path = Path(folder) / "plan.json"
        path.write_text(json.dumps(plan), encoding="utf-8")
        validate(json.loads(path.read_text(encoding="utf-8")))
    print(json.dumps({"overall": "PASS", "level": "STATIC_VERIFIED", "skill": ROOT.name}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
