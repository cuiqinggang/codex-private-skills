# EXP-PI-DURABLE-ENTRY-20261113-001｜原生Pi入口持久化接续与GUI限定验收

类别：CASE / ERROR / CANDIDATE_RULE；核查日2026-11-13；证据等级：同一Windows10机器、实际公开Open-Pi.cmd入口、**合成单工作流**的原生回执和独立字段/受控GUI验收。只认证 `VERIFIED_FOR_SCOPE`，不是通用生产事务安全、商业用户交付、24h无人值守或新正式稳定规则。

**触发**：原生Pi+Temporal工作流在心跳超时、worker/service重启、已写入但无回执、已验证结果重复提交、真实合成页面GUI导出与本机Excel读回之间需要核账；必须区分业务产物、确认回执、重试次数和有效签收。

**成熟节点**：原 `C:/Users/A/Documents/DSH-Workspace/pi-capability-enhancement-20261028/Open-Pi.cmd` 公开入口、原生Pi同会话、已有Temporal心跳/持久化状态、原宿主合成账目配方和独立GUI/字段核验。未自建通用调度器、状态数据库或系统恢复内核。

**LAST_GOOD→FIRST_DELTA→原任务修复及回归**：
- 11月13日19:07原`pi-comprehensive-20261113/temporal-heartbeat-restart-r83/RESULT.json`：原存储重开、原worker替换，history activity attempts=[2]、原生Pi attempt=1，业务hash/mtime保留；恢复至验收9.785秒，全段106.883秒，限定字段QA true。
- 20:39—20:41原`pi-durable-entry-r84-r86-normal/ENTRY-ACCEPTANCE.json`、`...fault/ENTRY-ACCEPTANCE.json`：正常组attempt=[1]、elapsed98.823秒；受控中断组attempt=[2]、同一workflow/run、`reused_verified_result=true`、`one_native_pi_attempt=true`、原delivery/checkpoint SHA和mtime **各组内**重试前后相等，恢复12.339秒、elapsed62.821秒。两组耗时不构成可比较加速合同，已复用结果不等于重新完成业务计算。
- **反例**：`...no-receipt/ENTRY-ACCEPTANCE.json`注入了业务副作用但没有确认回执，结果是`FAILED`、`second_execution_blocked=true`。这才是正确的UNKNOWN安全拒绝，不可写作PASS或强制重发。
- 11月13日03:03原`durable-three-route-reality-r1/conductor-mh-r76-result.json`为合成网页GUI独立完成，原数据保持、单自有tab、CSV+工作簿逐格审计与页面刷新 true、214.117秒；20:49`pi-comprehensive-20261113/matt-booking/RESULT.json`既有合成预约GUI→CSV→工作簿限定PASS、全段213.670秒并恢复4次工具错误。两个不同合同不可直接用秒数排名。
- 20:29`BROWSER-READONLY-RECOVERY-20261113.json`仅`browser_tabs/list` PASS、23.385秒，`gui_signed=false`，不能算用户业务交付。

**用途**：下一次遇已验结果与恢复状态冲突，先匹配原workflow/run、原checkpoint和原产物SHA/mtime，核历史attempt和业务唯一写入回执。三态：已证明写入不再重做；确认未写可经原接口重试；已写但回执缺失则UNKNOWN、禁止盲重发，归原项目核账。所有验收必须走原GUI/实际公开入口。

**不适用**：合成单工作流不代表真实多账户高并发、任意崩溃点恰好一次、跨OS重启、ChatGPT网页委派、完全无人值守或真实客户交付。没有相同质量/成本条件的全业务路线对照；完整`T_VALID`与记忆净收益均`NOT_MEASURED`。不将该案例新建为“成熟商业业务配方”。原项目任务约束/Freeze/持久化状态均不修改。

来源均在原C盘`C:/Users/A/Documents/DSH-Workspace/ecc-matt-pi-20261110/`，上述各独立RESULT/ENTRY-ACCEPTANCE原文件及本机Vault`01_DAILY/2026-11-13-DSE-INCREMENTAL.md`。Pi复盘原稿与GPT纠界：`pi-rules-r64-20261108/daily-review-r71/runs/20261113-210402-083610/{RESULT.json,DRAFT.json,SEMANTIC-AUDIT.json}`。分享卡未附原客户数据、凭据或大段聊天。新增稳定规则0、新真实业务配方0、共享EXP下游新采用未观察到；memory_T_VALID_gain=NOT_MEASURED。
