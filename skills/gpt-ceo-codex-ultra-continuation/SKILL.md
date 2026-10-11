---
name: gpt-ceo-codex-ultra-continuation
description: GPT CEO 授权、Codex Ultra长流程、动态并行、Windows原生持续监控、事故记录与合法恢复。Polsia等多模块大任务可直接复用。
---

# GPT CEO＋Codex Ultra 连续运行技能｜V4

SKILL_VERSION=V4
METHOD_VERSION=V4
VERSION_POLICY=INTEGER_ONLY
ENGINE=28_FOR_CURRENT_POLSIA_UNCHANGED
LIVE_WINDOWS_RUNTIME=3.1.0_UNCHANGED

**唯一权威索引**：`cuiqinggang/codex-private-skills/main` 中 `skills/artificial-single-page-extreme-time-engine/GPT_CODEX_ULTRA_CONTINUATION_INDEX.md`。

**当前正式方法**：`skills/artificial-single-page-extreme-time-engine/GPT_CODEX_ULTRA_CONTINUATION_V4.md`。旧 `GPT_CODEX_ULTRA_CONTINUATION_V3_2_2.md` 保留为启动双门和故障复盘历史，不再作为最新方法版本。

## V4 首先执行
1. 从GitHub精确读取索引、任务CURRENT/VERSION_CURRENT、最后Freeze、CEO授权，随后核验Windows真实任务和SHA。历史DONE不重播，UNKNOWN先对账。
2. 大型任务维持九类Polsia能力加跨系统集成共十条逻辑分支。READY按合法授权与依赖派工，BLOCKED不阻断其他分支。每条分支独立目录与回执，母指针只能由CEO单写者更新。
3. 依据任务类型确定并发：本机CPU/文件任务先2后4，等待型任务先4后8，必须以相同有效结果总时间和故障率验证净收益。Codex真实多Agent并行上限未知，不擅自启动十个重型CLI。
4. 监控必须始终存在，且将RUNNING、READY、BLOCKED、WAITING_CEO、ERROR、STALE、DONE区分显示；故障修复后清除当前报警但保留原事件；不得把状态窗口Running当业务PASS。
5. 无法确定业务结果时，禁止盲重启或自动重新发送。安全隔离Git夹具可做原生恢复并SHA核验；付款、客户消息、广告发布、生产及凭据相关操作必须另有授权。
6. 任何新Codex自然节点都需验证CEO_APPROVED正式授权、Windows本地实际NEXT合同与当前定位标签。未获批只能WAITING_CEO，不得启动。

## V4 原生监控入口
- Windows实际目录：`C:\AI\Polsia-Unified-V4\`
- 桌面入口：`Polsia Codex - Live Status`，单屏汇总十条分支和母任务。
- 后台采集：原生计划任务 `Polsia-Unified-Monitor-V4` 每分钟执行项目专用collect.ps1，业务执行器完全独立。
- 快照：`snapshot.json`；事故与恢复流水：`incidents.jsonl`；10模块定义：`config.json`；安装及试点证据：`installation.json`、`pilot-results.json`。
- 正式脚本备份：本技能目录 `v4/config.json`、`v4/collect.ps1`、`v4/dashboard.ps1`、`v4/pilot.ps1`、`v4/install.ps1`。
- ChatGPT每小时条件巡检：有新真实事故、监控失联或新的决策需求才提醒；不能宣称秒级GPT自动接管。
- V008 `MOTHER_NEEDS_GPT.flag` 的 `CEO_NEXT_SCOPE_DECISION_REQUIRED` 属正常审批等待；n8n HTTP401属于WORKFLOW分支权限阻塞。

## 当前验收和未验
2026-10-12，原生计划任务创建PASS，10分支快照PASS，桌面快捷方式和登录启动PASS；ENG隔离只读128项SHA全通过，RECOVERY隔离Git损坏检测+自动restore通过；监控测试注入ALERT→CLEARED，四条测试事件仍可回读。GitHub方法和源代码逐一精确回读。
**未认证**：九类完整公司能力、真实Codex多Agent数量最优、未知生产故障自动修复、断电冷启动、72小时和最终优化10轮。Polsia最新业务V008，MOTHER_FINAL_VALID=NO。

**不改动**：`C:\AI\Polsia-Codex-20261011\CONTINUE_EXISTING_CODEX.ps1`、原计划任务 `Polsia-Codex-Mother-Continue`、FlClash/代理、浏览器与原不可变Freeze。
