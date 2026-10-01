# CHANGELOG

## 0.2.0 - 2026-10-02

- 新增双路执行：Desktop Commander Remote 作为默认主路，GitHub Actions + Windows self-hosted runner 作为备路。
- 主路已 Reality 验证设备发现、目录/文件读取、文件写入回读与清理、本机命令/进程执行。
- 备路恢复 `ETAL-GitHub-Actions-Runner` 用户登录计划任务常驻，runner `DESKTOP-4A1EGTM-etal` 在线。
- 新增 `DUAL_ROUTE.md`，冻结主路进入条件、备路降级条件、健康检查与双路同时失败时的处理。
- 修复 Windows checkout 长路径风险：在 `windows-reality` job 注入 `core.longpaths=true`，不依赖临时 HOME 或管理员级系统 Git 配置。
- runner 名称默认值改用 `[Environment]::MachineName`，避免 Remote 环境变量缺失导致错误名称。
- Windows Service 仅作为可选增强，不再作为备路可用的必要前置条件。

## 0.1.3 - 2026-10-02

- 修复 workflow 级 concurrency 被离线 self-hosted runner 长期占用、导致后续静态验证也 pending 的问题。
- 删除 workflow 顶层 concurrency。
- 仅对 windows-reality job 使用串行组 `extreme-time-windows-reality`。
- 静态门禁与 Windows Reality 排队解耦；旧 smoke 不重发。
- Reality 状态仍为 PARTIAL，必须等待真实 Windows runner 领取并产出 artifact 才能认证。

## 0.1.2 - 2026-10-02

- 修复非任务提交也占用 self-hosted Windows 队列的问题。
- 新增 hosted 静态阶段的任务发现输出。
- 只有 tasks/*.json 真正变化或显式 workflow_dispatch 指定任务时，才进入 Windows Reality。
- bootstrap PowerShell 也纳入静态语法门禁。

## 0.1.1 - 2026-10-02

- 首次真实触发 GitHub Actions 执行桥工作流。
- contract-static：PowerShell解析 PASS。
- contract-static：任务合同 PASS。
- Windows Reality job 已 queued，Run ID=36899361139。
- 发现唯一现实缺口：目标 Windows 尚无在线 self-hosted runner。
- 新增 Windows runner 一次性 bootstrap 脚本。
- bootstrap 默认使用交互用户会话 + 计划任务常驻。
- 仍未 Reality 认证，不冻结。

## 0.1.0 - 2026-10-02

- 建立无决策权自动执行桥。
- 删除正式路径中的人工 GPT↔Windows 中继。
- 最小入口固定为 GitHub任务JSON。
- 实现 Windows PowerShell执行器、GitHub Actions、artifact回传与可选回调。
- 加入 ETAL-BRIDGE-SMOKE-001。
