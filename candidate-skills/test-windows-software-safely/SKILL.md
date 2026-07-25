---
name: test-windows-software-safely
description: "Plan, run, evidence, and roll back Windows software tests in a dedicated Hyper-V virtual machine with prerequisite checks, exact-VM binding, isolated networking, checkpoints, guest boot-identity verification, bounded reboot waits, and failure-safe restoration. Use for potentially disruptive installers, uninstallers, security software, driver-bearing applications, or workflows that must prove they resume through multiple Windows guest reboots. Do not treat a container as a Windows kernel/reboot test, operate a production VM, expose the host, or run unpinned guest payloads."
---

# Windows 软件安全虚拟测试

只管理测试环境生命周期：`检查 → 计划 → 隔离 → checkpoint → guest 操作/重启 → 证据 → 回滚`。先读 [实验室安全合同](references/lab-safety-contract.md)。

## 固定规则

1. 只使用明确标记为 disposable 的专用 Windows VM；不得使用宿主、生产 VM 或用户日常 VM。
2. 容器、WSL 和进程沙箱不能证明 Windows 内核驱动卸载或真实重启。
3. 默认 `None` 网络并断开所有 VM 网卡；需要互联时只允许事先验证的 Private switch。External switch 不通过。
4. 禁用共享文件夹、宿主凭据复用和不必要的增强会话。guest 凭据只在运行时传入，不写计划或日志。
5. guest payload 必须固定 SHA-256；未固定或哈希漂移时停止。
6. 所有变更绑定 `planHash`，默认只预演；`-Execute` 才操作 VM。
7. checkpoint、guest boot id、退出码、超时和证据哈希必须记录。失败默认恢复 baseline。
8. 本技能不包含软件卸载逻辑，也不实现跨重启任务状态机；只承载它们的隔离测试。

## 工作流

### 1. 只读前提检查

```powershell
.\scripts\Test-WindowsSoftwareLabPrerequisites.ps1 -VmName <disposable-vm>
```

确认 Windows Pro/Enterprise、Hyper-V 模块、管理员权限、VM 状态、磁盘空间、PowerShell Direct 与网络类型。

### 2. 生成安全计划

```powershell
.\scripts\New-WindowsSoftwareTestPlan.ps1 `
  -VmName <disposable-vm> -ScenarioName two-reboot-fixture `
  -NetworkMode None -GuestPayloadPath .\fixture.ps1 `
  -EvidenceRoot C:\LabEvidence -OutputPath .\lab-plan.json -ConfirmDisposable
```

计划绑定宿主、VM ID、payload hash、baseline checkpoint 名、有效期和最大 guest reboot 次数。向用户展示 `planHash`。

### 3. 预演、执行和回滚

```powershell
.\scripts\Invoke-WindowsSoftwareTestLab.ps1 `
  -Action Prepare -PlanPath .\lab-plan.json -ApprovePlanHash <hash>
```

先逐个预演 `Prepare`、`ExecutePayload`、`RestartGuest`、`CollectEvidence`、`Restore`。核对后增加 `-Execute`，并仅在运行时传入 guest 凭据。`ExecutePayload` 用 PowerShell Direct 把固定哈希脚本复制到 guest、再次校验哈希、执行并记录退出码。guest reboot 只调用 `Restart-VM`，绝不重启宿主。

任一执行阶段失败时自动尝试恢复 baseline 并写入恢复结果。显式 `Restore` 不受 payload 丢失、哈希漂移或计划过期阻断；恢复后必须通过 PowerShell Direct 证明 baseline 前不存在的 test marker 已消失。

调用顽固卸载技能时，让 guest 任务产生 reboot request；由跨重启技能保存任务状态，由本技能执行并验证 guest reboot。

## 验证

```bash
python3 scripts/test_windows_software_lab.py
```

跨平台测试只验证合同、manifest 和危险边界。Windows 实测必须先运行 bundled fixture，在两次 guest reboot 后观察三个不同 boot id，并成功恢复 baseline。360 双产品只能在合法来源、固定哈希、隔离 VM 和可回滚 checkpoint 下测试。

当前环境未完成真实 Hyper-V guest 测试时，只能标记 `STATIC_VERIFIED`。
