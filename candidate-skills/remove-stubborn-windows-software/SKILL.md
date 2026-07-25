---
name: remove-stubborn-windows-software
description: "Audit, plan, remove, and verify stubborn Windows desktop software with exact product identity, vendor or MSI uninstallers first, hash-bound human approval, residual evidence, and explicit reboot handoff. Use when ordinary Apps & Features removal fails, software reappears after reboot, multiple security products protect each other, or processes, services, drivers, tasks, startup entries, and files may remain. Default to read-only evidence collection; never force-delete unknown drivers, broadly match names, take ownership, weaken ACLs, or claim success while active product evidence remains."
---

# 顽固软件安全卸载

按 `审计 → 计划 → 精确批准 → 厂商卸载 → 重启交接 → 复验` 工作。先读取 [安全政策](references/safety-policy.md)。

## 固定规则

1. 默认只读。用户笼统说“卸载”只授权审计和计划；执行必须绑定本轮 `planHash`。
2. 按精确 `DisplayName` 与 `Publisher` 识别产品；不要按“360”“safe”等宽泛字符串批量删除。
3. 优先 Windows 设置、厂商卸载器或 MSI。只执行 inventory 捕获、有效签名且 SHA-256 未变化的入口。
4. 厂商自保护开关、验证码、交互式卸载或许可证提示属于 human gate。
5. 不停止或删除未知服务/驱动，不直接清 DriverStore，不夺取所有权，不放宽 ACL，不运行注册表清理器。
6. 需要重启时只输出 `rebootRequest`；由 `$resume-windows-task-after-reboot` 保存续接状态。本技能不注册启动任务、不调用重启。
7. 重启后重新 inventory。只有目标产品及其活跃证据均不存在才判 `ABSENT`。
8. 已知签名残留可判 `KNOWN_VENDOR_RESIDUE`，但不等于彻底删除；未知证据必须判 `UNKNOWN_BLOCKER`。

## 工作流

### 1. 只读 inventory

```powershell
.\scripts\Get-StubbornSoftwareInventory.ps1 `
  -DisplayName '360安全卫士','360杀毒' `
  -Publisher '北京奇虎科技有限公司' `
  -OutputPath .\inventory.json
```

检查产品、卸载入口、签名、进程、服务/驱动、计划任务和路径证据。360 双产品案例另读 [360 案例](references/360-safe-guard-antivirus-case.md)。

如果已从厂商材料或人工审计得到系统目录驱动等精确身份，用 `-ComponentIdentityManifestPath` 传入只含精确安装根、进程路径、服务名、任务 ID 和启动项 ID 的 JSON；通配符会被拒绝。它只扩展观察范围，不授权删除。

### 2. 生成精确计划

```powershell
.\scripts\New-StubbornSoftwareRemovalPlan.ps1 `
  -InventoryPath .\inventory.json -OutputPath .\plan.json `
  -ApprovedPublisherThumbprintsPath .\approved-publishers.json
```

向用户展示目标、卸载入口、human gates、预计重启和 `planHash`。计划绑定机器、当前用户和 24 小时有效期。

### 3. 预演与执行

先预演：

```powershell
.\scripts\Invoke-StubbornSoftwareRemoval.ps1 `
  -PlanPath .\plan.json -ApprovePlanHash <hash>
```

用户确认相同输出后才添加 `-Execute`。执行器只启动固定卸载入口；不删除残留。输出 reboot request 后停止，由跨重启适配器接回“重新 inventory”步骤。

### 4. 复验

每次重启后把卸载前 inventory 作为 baseline 重新扫描：

```powershell
.\scripts\Get-StubbornSoftwareInventory.ps1 `
  -DisplayName '360安全卫士','360杀毒' -Publisher '北京奇虎科技有限公司' `
  -BaselineInventoryPath .\inventory-before.json -OutputPath .\inventory-after.json
.\scripts\Compare-StubbornSoftwareInventory.ps1 `
  -BaselineInventoryPath .\inventory-before.json -CurrentInventoryPath .\inventory-after.json
```

baseline 固定先前 install roots 和精确组件身份，因此 ARP 消失后仍检查原进程路径、服务/驱动名、任务和启动项。不要用“卸载器退出码 0”代替验收。

## 验证

```bash
python3 scripts/test_stubborn_software_removal.py
```

该测试只使用 fixture。必须在 disposable Windows VM 内完成两个产品同时安装、官方卸载、多次 guest reboot、残留核查与回滚，才能宣称 360 组合通过；真实机器不安装该组合用于测试。

本技能不负责 VM 生命周期，也不实现跨重启状态机。
