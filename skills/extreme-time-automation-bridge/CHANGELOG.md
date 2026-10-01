# CHANGELOG

## 0.1.1 - 2026-10-02

- 首次真实触发 GitHub Actions 执行桥工作流。
- contract-static：PowerShell解析 PASS。
- contract-static：任务合同 PASS。
- Windows Reality job 已 queued，Run ID=36899361139。
- 发现唯一现实缺口：目标 Windows 尚无在线 self-hosted runner。
- 新增 Windows runner 一次性 bootstrap 脚本。
- bootstrap 默认使用交互用户会话 + 计划任务常驻，避免 Windows 服务 session 0 对桌面/剪贴板类任务的限制。
- 仍未 Reality 认证，不冻结。

## 0.1.0 - 2026-10-02

- 建立无决策权自动执行桥。
- 删除正式路径中的人工 GPT↔Windows 中继。
- 最小入口固定为 GitHub任务JSON。
- 实现 Windows PowerShell执行器、GitHub Actions、artifact回传与可选回调。
- 加入 ETAL-BRIDGE-SMOKE-001。
