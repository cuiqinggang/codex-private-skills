---
name: resume-windows-task-after-reboot
description: "Persist and safely resume a Windows task or Loop workflow across one or more operating-system reboots with an AtStartup scheduled task, atomic checkpoints, boot-identity checks, bounded retries, pinned code hashes, and duplicate-start protection. Use when an existing workflow is blocked on a required Windows reboot and must continue at an exact next step without human reconstruction, including a Loop goal that returns REBOOT_REQUIRED. Keep the adapter task-agnostic; do not put the task's business logic, arbitrary commands, software-removal logic, or VM lifecycle logic into the checkpoint."
---

# 跨重启任务续接

只解决一个关节：`保存状态 → 重启 → 读取状态 → 调回原任务下一步`。不要重写原任务。

## 固定合同

1. 先读取 [运行合同](references/runtime-contract.md)。
2. 把代码固定到不可变提交与 SHA-256；禁止以 SYSTEM 下载并执行 `latest`。
3. checkpoint 只保存 `EntryPointId`，不得保存命令行。入口必须存在于管理员安装的 allowlist manifest。
4. 用临时文件、flush、同卷替换原子写入；写入和回读失败时不得请求重启。
5. 用 `Win32_OperatingSystem.LastBootUpTime` 区分启动。boot id 未变化时不得续接。
6. 启动时使用全局 mutex；同一 state revision 最多消费一次。
7. 网络、哈希、schema、revision 或入口校验失败时停止并保留证据，不推进 `ResumeStep`。
8. 达到 `MaxAttempts` 时转 `BLOCKED`；完成时注销启动任务并将状态置 `COMPLETED`。

## 与 Loop 对接

需要让 Loop 跨重启继续时，读取 [Loop 适配合同](references/loop-adapter.md)。保持两套状态：

- Loop 的 `STATE.json` 保存任务事实、游标、下一动作和完成条件。
- 本适配器的 `%ProgramData%\RebootResumeAdapter\state.json` 只保存一次启动交接。

Loop 先原子保存状态并追加日志，再输出 `REBOOT_REQUIRED`；调用方随后执行 `Arm`，验证 `REBOOT_PENDING` 后才可请求重启。开机入口只运行一轮 Loop。若该轮仍需重启，必须生成新 revision 并重新 `Arm`，不得在入口内无限循环。

## 工作流

### 1. 安装最小 bootstrap

准备只包含固定入口的 manifest，再预演：

```powershell
.\scripts\Invoke-RebootResumeAdapter.ps1 -Action Install `
  -ConfigPath C:\ProgramData\RebootResumeAdapter\config.json `
  -StatePath C:\ProgramData\RebootResumeAdapter\state.json `
  -EntryPointManifestPath .\entrypoints.json `
  -CodeCommit <immutable-commit> -PackageSha256 <sha256> -WhatIf
```

核对后再移除 `-WhatIf`。安装只复制 bootstrap/config 并注册 `AtStartup` 任务，不触发重启。

### 2. 在原任务的重启关口 Arm

```powershell
.\scripts\Invoke-RebootResumeAdapter.ps1 -Action Arm `
  -ConfigPath C:\ProgramData\RebootResumeAdapter\config.json `
  -StatePath C:\ProgramData\RebootResumeAdapter\state.json `
  -RunId <run-id> -ResumeStep <next-step> -EntryPointId <allowlisted-id>
```

只有输出 `REBOOT_PENDING` 且原任务已验证 checkpoint 后，原任务才可自行请求重启。适配器不调用 `Restart-Computer`。

### 3. 启动续接与收尾

Task Scheduler 调用 `-Action Resume`。原任务成功后调用 `-Action Complete`；无法继续时保留 `BLOCKED` 状态和日志。查看状态用 `-Action Status`，安全卸载 hook 用 `-Action Disarm`。

## 验证

先运行不接触系统任务或重启的静态/fixture 测试：

```bash
python3 scripts/test_reboot_resume_adapter.py
```

与 Loop 的最小两次重启案例使用：

```powershell
.\scripts\Invoke-TwoRebootLoopFixture.ps1 -Action Initialize
```

它在初始启动后要求两次外部 guest reboot，并在第三个不同 boot id 上输出 `TWO_REBOOT_LOOP_FIXTURE_PASS`；脚本自身绝不调用重启。测试步骤和证据要求见 [Loop 适配合同](references/loop-adapter.md)。

在 disposable Windows VM 中再运行 `scripts/Test-RebootResumeAdapter.ps1` 和两次重启 Loop 夹具。必须完成两次真实 guest reboot、重复启动和断网负例后，才可把能力从 `STATIC_VERIFIED` 提升为 Windows 实测通过。

本技能不卸载软件、不控制虚拟机。顽固卸载只通过标准 reboot request 使用本技能；虚拟机生命周期交给独立测试技能。
