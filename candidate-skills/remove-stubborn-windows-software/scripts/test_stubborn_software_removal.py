#!/usr/bin/env python3
"""Cross-platform fixture and static policy tests; performs no uninstall."""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = list((ROOT / "scripts").glob("*.ps1"))


def classify(evidence: dict) -> str:
    if evidence["products"] or evidence["activeComponents"]:
        return "ACTIVE_PRODUCT"
    if evidence["unknown"]:
        return "UNKNOWN_BLOCKER"
    if evidence["knownSignedResidue"]:
        return "KNOWN_VENDOR_RESIDUE"
    return "ABSENT"


def vendor_allowed(publisher: str, thumbprint: str, executable: str, approvals: dict[str, set[str]]) -> bool:
    lolbins = {"powershell.exe", "pwsh.exe", "cmd.exe", "wscript.exe", "cscript.exe", "mshta.exe", "rundll32.exe", "regsvr32.exe"}
    return Path(executable).name.lower() not in lolbins and thumbprint.upper() in approvals.get(publisher, set())


def main() -> int:
    all_text = "\n".join(path.read_text(encoding="utf-8") for path in SCRIPTS)
    required = ["ApprovePlanHash", "Get-AuthenticodeSignature", "Get-FileHash", "rebootRequest", "NOT_VERIFIED_REINVENTORY_REQUIRED", "signerThumbprint", "LOLBin"]
    for token in required:
        assert token in all_text, token
    forbidden = [
        r"\bRestart-Computer\b",
        r"\bStop-Computer\b",
        r"Invoke-Expression",
        r"\biex\b",
        r"\btakeown\b",
        r"\bicacls\b",
        r"\bpnputil\b.+/delete-driver",
        r"Remove-Item[^\r\n]+-Recurse",
        r"sc(?:\.exe)?\s+delete",
        r"reg(?:\.exe)?\s+delete",
    ]
    for pattern in forbidden:
        assert not re.search(pattern, all_text, re.IGNORECASE), pattern

    assert classify({"products": ["A"], "activeComponents": [], "unknown": [], "knownSignedResidue": []}) == "ACTIVE_PRODUCT"
    assert classify({"products": [], "activeComponents": [], "unknown": ["x.sys"], "knownSignedResidue": []}) == "UNKNOWN_BLOCKER"
    assert classify({"products": [], "activeComponents": [], "unknown": [], "knownSignedResidue": ["vendor.sys"]}) == "KNOWN_VENDOR_RESIDUE"
    assert classify({"products": [], "activeComponents": [], "unknown": [], "knownSignedResidue": []}) == "ABSENT"
    approvals = {"Real Vendor": {"AA11"}}
    assert vendor_allowed("Real Vendor", "AA11", r"C:\Vendor\uninstall.exe", approvals)
    assert not vendor_allowed("Spoofed HKCU Publisher", "SYSTEMCERT", r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe", approvals)
    baseline = {
        "products": [{"displayName": "Product A", "installLocation": "C:\\Vendor\\A"}],
        "servicesAndDrivers": [{"evidenceId": "service:vendorfilter", "name": "VendorFilter", "state": "Running"}],
    }
    after_arp_removed = {
        "products": [],
        "servicesAndDrivers": [baseline["servicesAndDrivers"][0]],
    }
    assert not after_arp_removed["products"]
    assert classify({
        "products": after_arp_removed["products"],
        "activeComponents": after_arp_removed["servicesAndDrivers"],
        "unknown": [],
        "knownSignedResidue": [],
    }) == "ACTIVE_PRODUCT"
    inventory_text = (ROOT / "scripts" / "Get-StubbornSoftwareInventory.ps1").read_text(encoding="utf-8")
    compare_text = (ROOT / "scripts" / "Compare-StubbornSoftwareInventory.ps1").read_text(encoding="utf-8")
    for token in ["BaselineInventoryPath", "baselineServiceNames", "baselineInventorySha256", "ComponentIdentityManifestPath", "cannot contain wildcards"]:
        assert token in inventory_text, token
    for token in ["ACTIVE_PRODUCT", "KNOWN_VENDOR_RESIDUE", "UNKNOWN_BLOCKER", "ABSENT", "Current inventory was not captured from this exact baseline"]:
        assert token in compare_text, token

    fixture = {
        "schemaVersion": 1,
        "kind": "stubborn-software-removal-plan",
        "computer": "fixture",
        "userSid": "fixture",
        "actions": [
            {"type": "VendorUninstaller", "displayName": "Product A", "sha256": hashlib.sha256(b"a").hexdigest()},
            {"type": "MSI", "displayName": "Product B", "productCode": "{00000000-0000-0000-0000-000000000000}"},
        ],
        "requiresReboot": True,
        "nextStep": "reinventory-and-verify",
    }
    with tempfile.TemporaryDirectory(prefix="stubborn-removal-fixture-") as folder:
        path = Path(folder) / "plan.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        loaded = json.loads(path.read_text(encoding="utf-8"))
        assert len(loaded["actions"]) == 2 and loaded["requiresReboot"]
    print(json.dumps({"overall": "PASS", "level": "STATIC_VERIFIED", "skill": ROOT.name}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
