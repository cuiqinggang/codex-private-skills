# 场景计划 schema

最小计划：

```json
{
  "schemaVersion": 1,
  "kind": "windows-software-test-plan",
  "runId": "opaque-guid",
  "host": "LAB-HOST",
  "vmName": "Disposable-Windows",
  "vmId": "guid",
  "disposableConfirmed": true,
  "scenarioName": "two-reboot-fixture",
  "networkMode": "None",
  "privateSwitchName": null,
  "privateSwitchId": null,
  "initialAdapterIds": ["adapter-guid"],
  "guestPayloadPath": "C:\\LabPayloads\\fixture.ps1",
  "guestPayloadSha256": "64 lowercase hex characters",
  "guestPayloadDestination": "C:\\ProgramData\\WindowsSoftwareTestLab\\opaque-guid\\payload.ps1",
  "testMarkerPath": "C:\\ProgramData\\WindowsSoftwareTestLab\\opaque-guid\\executed.marker",
  "evidenceRoot": "C:\\LabEvidence",
  "baselineCheckpointName": "baseline-opaque-guid",
  "maxGuestReboots": 2,
  "createdAt": "UTC ISO-8601",
  "expiresAt": "UTC ISO-8601",
  "planHash": "64 lowercase hex characters"
}
```

计划不得包含 PowerShell 表达式、任意命令、宿主重启动作、凭据或远程访问 token。`guestPayloadPath` 是预先固定的单个文件，不是通配或目录。

标准事件为 `PREPARED`、`GUEST_REBOOT_STARTED`、`GUEST_REBOOT_VERIFIED`、`EVIDENCE_COLLECTED`、`RESTORED`、`BLOCKED`。只有 boot id 发生变化且 VM 在有界时间内回到 Running 才记录 `GUEST_REBOOT_VERIFIED`。
