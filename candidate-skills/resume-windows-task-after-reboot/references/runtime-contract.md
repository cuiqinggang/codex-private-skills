# 运行合同

## 状态

允许状态只有：

- `READY`
- `REBOOT_PENDING`
- `RESUMING`
- `COMPLETED`
- `BLOCKED`

checkpoint 的最小 schema：

```json
{
  "schemaVersion": 1,
  "runId": "opaque-run-id",
  "status": "REBOOT_PENDING",
  "resumeStep": "next-step",
  "entryPointId": "allowlisted-id",
  "previousBootId": "20260725091500.000000-000",
  "attempt": 0,
  "maxAttempts": 3,
  "codeCommit": "immutable-commit",
  "packageSha256": "64 lowercase hex characters",
  "stateRevision": 1,
  "updatedAt": "2026-07-25T09:16:00.0000000Z",
  "lastErrorCode": null
}
```

状态文件不得含 shell、PowerShell、可执行路径、参数串或凭据。

## 原子性与重放

`Arm` 必须在返回前完成：序列化到同目录临时文件、flush、原子替换、重新读取、逐字段验证。调用方配置远端只读镜像时，还必须先发布镜像，再回读相同的身份字段。失败时转为带 `lastErrorCode` 的 `BLOCKED`，不得请求重启。

`Resume` 必须：

1. 获取全局 mutex。
2. 验证 schema 与不可变代码身份。
3. 比较当前 boot id 与 `previousBootId`。
4. 原子写入本地 `RESUMING` 并递增 attempt。
5. 从管理员安装的 manifest 解析 `entryPointId`，验证入口脚本 SHA-256。
6. 只传递 checkpoint 路径；原任务自行读取允许字段并继续。

非 `REBOOT_PENDING` 的本地状态、同一 boot id 或 mutex 冲突不得再次调用入口。远端镜像只在本地仍为 `REBOOT_PENDING` 时参与校验，永远不能覆盖本地 `RESUMING/COMPLETED/BLOCKED`。

## 本地与在线边界

Windows 启动必须依靠本地最小 bootstrap 和 Task Scheduler；在线仓库不能自行在主机开机时触发。在线仓库保存版本化代码、入口 manifest 和可选只读状态镜像。本地 config 固定 commit、包哈希及远端位置。调用方负责发布镜像；本技能只回读验证，不实现远端写入或远端 compare-and-set。网络、revision、schema 或身份不一致时转 `BLOCKED`，不执行入口。

本地安装根固定为管理员控制的 `%ProgramData%\RebootResumeAdapter`。config、state、bootstrap、installed manifest 和复制后的 allowlisted entry scripts 必须全部在该根内，不得经过 reparse point。安装时 `PackageSha256` 必须等于当前 bootstrap 实际 SHA-256；每个源入口先按 manifest 校验哈希再复制。根 ACL 关闭继承，只允许 SYSTEM 与 Builtin Administrators 写入；注册 SYSTEM 任务前以及每次 Resume 前回读关键路径、ACL 和哈希。

不要给计划任务或状态文件开放普通用户写权限。不要把仓库凭据写入状态。需要私有仓库认证时，使用系统既有凭据提供方，并把认证失败视为 `BLOCKED`。

## 完成定义

只有原任务对自己的后置条件给出 PASS，才调用 `Complete`。适配器本身只能证明“准确续接”，不能证明原任务业务目标完成。
