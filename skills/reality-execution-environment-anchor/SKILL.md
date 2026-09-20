---
name: reality-execution-environment-anchor
description: 现实执行环境精确锚定与数字孪生基线。v1.2.0 在保留 R1/R2 Windows/Codex 现实锚点的基础上新增 Browser Reality R3：完整采集 Playwright/浏览器/Profile/登录态/DOM/actionability/网络/远端响应/运行时错误/Trace/CDP，并把安全指纹交给唯一 Exact Twin。Reality 先只读采集，历史只追加，敏感原文禁止远端上传。
metadata:
  version: "1.2.0"
  status: HOST_R2_COMPLETE_BROWSER_R3_COLLECTOR_READY
---
# 现实执行环境精确锚定与数字孪生基线

本技能属于「成熟方案集群」，不是第四核心。

## 固定原则
- REALITY_FIRST：现实事实优先。
- NO_GUESSING：禁止猜测未采集状态。
- READ_ONLY_CAPTURE_FIRST：先只读采集。
- NO_ENVIRONMENT_HARDENING_DURING_CAPTURE：采集期间禁止硬化。
- GPT_DESIGNS_HARDENING：硬化方案由 GPT 冻结。
- CODEX_DETERMINISTIC_EXECUTOR_ONLY：Codex 只执行冻结采集/验证。
- HISTORY_APPEND_ONLY：历史只追加。
- SECRET_PLAINTEXT_ZERO_REMOTE：认证态、Cookie、Token、原始 HAR/Trace 不得明文进远端安全镜像。

## v1.1.0 / R1-R2 保留
R1/R2 已完成 Windows/Codex 现实锚定：
- HOST_REALITY_ANCHOR_COMPLETE=YES
- CRITICAL_EXECUTION_STATE_COVERAGE_PERCENT=100.00
- LEGACY_TWIN_INPUT_READY=YES
- Reality Fingerprint V3 =
  `9bdd4430596e306cf6f8061069659e2680d8a1b66bd69d7bb3e45fe4cfd63dd8`

权威历史仍为：
- snapshots/2026-09-21-r2/45-REALITY-ENVIRONMENT-ANCHOR-R2-FINAL.json
- snapshots/2026-09-21-r2/46-REALITY-FINGERPRINT-V3.json

这些文件和指纹不得覆盖。

## v1.2.0 / Browser Reality R3
新增浏览器现实执行环境采集合同：
- `BROWSER-REALITY-R3.md`
- `BROWSER-REALITY-R3-CONTRACT.json`
- `BROWSER-REALITY-R3-ACCEPTANCE.md`
- `collectors/browser-reality-r3.mjs`
- `collectors/browser-host-network-r3.ps1`

R3 覆盖：
Windows/宿主网络 + Node + Playwright + Browser + Browser Context + Profile/userDataDir + Cookie/LocalStorage/IndexedDB/SessionStorage + 登录态 + Page/Frame/Worker/Service Worker + DOM/Overlay/Animation + Playwright actionability + HTTP(S)/redirect/timing/TLS + WebSocket + Console/PageError + Trace/CDP + Golden Task。

关键纠正：R2 中 `NETWORK_PROXY_CAPTURE=PROVEN_NON_BLOCKING` 只对 1344 子进程预启动失败边界成立；进入浏览器 E2E 后，网络/代理/Profile/页面生命周期都升级为关键执行状态，必须通过 R3 真实采集。

当前状态：
```text
HOST_R2_REALITY_ANCHOR_COMPLETE=YES
BROWSER_R3_COLLECTOR_CONTRACT=FROZEN
BROWSER_R3_REAL_CAPTURE=NOT_YET
BROWSER_R3_FINGERPRINT=NOT_YET
BROWSER_TWIN_INPUT_READY=NO
ENVIRONMENT_99=NOT_YET
```

唯一正式 Twin 消费者：
`first-principles-physical-limit-convergence@3.1.7/components/exact-reality-digital-twin@1.1.0`。
