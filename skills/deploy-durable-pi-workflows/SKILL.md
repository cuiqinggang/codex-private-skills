---
name: deploy-durable-pi-workflows
description: 多阶段长任务、跨会话接续及写后回执丢失时优先调用本规程。复用成熟开源持久化工作流部署和增强 Pi＋GPT 的长流程复杂任务，逐级验证断点接续、调度故障、写后回执丢失、独立程序与真实 GUI 签收。用于 Temporal OSS 主测、按业务场景选用调度器、无人值守恢复、完整合格时间优化及增强 Pi＋Superpowers 桌面直跑验证，保留候选准入证据。
---

# 增强 Pi 长流程持续交付与故障恢复（Temporal 主测与 Superpowers 直跑对照）V1.26

公开阅读版。示例中的历史业务标识、运行标识和内部证据地址已脱敏。脚本的本机依赖配置见 [使用说明](README.md)。

原名「长流程复杂任务持续交付」。英文调用标识为 `deploy-durable-pi-workflows`。Oh My Pi 是桌面执行入口，本轮选用 Temporal OSS 做持久化调度。Conductor OSS 保留原实测及部署配方，遇到匹配的具体业务再选用。早期 Agent-Autoloop 的短测及暂停原因见 [R70–R76 实测回执](references/evidence-r73.md)。Superpowers 有两种组合：R170 在 Temporal 路线中加载它，另设增强 Pi＋Superpowers 桌面直跑对照。直跑的长任务交付和故障恢复分别以本路线的实机签收为准。

正式任务统一由增强 Pi 接单、执行、处理常规故障和组织独立验收。GPT 交付目标与冻结约束，按 Pi 原会话的具体求援提供裁决。Docker 与应用就绪、GUI、账本、隔离还原和独立签收由 Pi 串成一个业务闭环。已有调度任务直接交给原 Pi 接续，带上原生 Run、已完成证据及首个待验关口，原 Worker 保持业务写入所有权。

## 长流程能力复测与调用

按[并行复测与能力登记](references/parallel-retest.md)主测增强 Pi＋Temporal，仅增测增强 Pi＋Superpowers 桌面直跑。按场景登记已验能力。双智能审核遵循 GPT＋Gemini 双智能协作与 Pi 执行系统 V2.4.3。 复杂单从接单起复用[同版双签与实机验收 R2](references/final-closure-v243-r2.md)，先查桌面执行入口，再一次冻结、独立双签并回读唯一完成事件。

## 调度任务执行顺序

1. **查原任务，再选配方。** 先读原生 Run、账本、进程与已签收回执。从首个缺项接续。新任务优先复用同入口、同条件已验收的部署与业务配方，记录适用范围和必要适配。
2. **冻结并预检。** 按[正式派发及验收流程](references/formal-run.md)绑定任务号、业务键、入口、权限、目录、输入及验收指纹。实际增强 Pi 身份运行[派发程序](scripts/admission_gate.py)，逐项核对读写、调度访问、接续和观测恢复。
3. **单次提交或交接。** 走桌面的「Oh My Pi 增强 V3」。Temporal 用[原生 CLI 直投](references/temporal-native-submit.md)，Conductor 走该场景已验入口。以原生 Workflow、Run 或任务 ID 读回确认提交。接续已有任务时，由原增强 Pi 入口持久写入[接管回执](references/formal-run.md#pi-接管回执与成果报告)。提交或接管状态不明先查原身份。历史任务和隔离测试按[原入口与恢复契约](references/pi-direct-entry.md)处理。
4. **照原检查点执行。** Worker 推进业务，独立观测留存最后有效时间。写入或子进程状态不明，先核原进程树、账本、检查点和回执。可隔离的任务并行，共享 GUI 或调度依赖按实际影响排队。暂停观测或关闭页面时，工作流继续由调度器持有。
5. **独立验收并报告成果。** 以实际 GUI、账本唯一写、备份还原、产物指纹和原生终态签收。先报已签收数量和可复核产物，再报待验关口及谁负责接续。正常轮通过后，再按[双路长测](references/paired-long-run.md)验证 Worker 中断、调度重启和写后丢回执。原生失败保留终态，需要时才走唯一关联纠正。T_VALID 从正式接单到独立签收，含排队、恢复、返工和裁决。

看门狗重试耗尽时，把原单交给仍在运行的环外接管者，登记下一次原键对账、触发条件及可执行动作。遇到迟到回执、空输出、计费不明或写汇总失败时，按[原单停滞后的接管与签收](references/stalled-order-recovery.md)继续。分别记录本次修复通过数和实际跨过的业务步骤。 区分进程故障与已确认的业务等待。首波准入截止后按原 Run 继续对账，并保留首波合格后单独起算的耐力时钟。

## 增强 Pi＋Superpowers 直跑

R170 第三路冻结为 Temporal＋增强 Pi＋Superpowers。沿该轮原生 Run、原 Pi 会话和原检查点接续。

验证简化组合时，从桌面「Oh My Pi 增强 V3」直接接单并执行，核对同一 Pi 进程实际加载的 Superpowers 版本。运行链路由桌面 Pi 及其加载的 Superpowers 构成，Pi 持有任务号、进程、原会话和业务检查点。对照测试沿用同一业务合同、可比负载及真实 GUI、账本唯一写、隔离还原和独立签收要求。从桌面 Pi 正式接单到独立签收单独记录完整 T_VALID。直跑的交付及故障接续能力均待各自 Reality 实测。

## Pi 原会话求援

专用浏览器无响应时，先对齐原浏览器和目标标签，保全草稿和在途写入，再按[浏览器恢复与放行](references/browser-recovery.md)处理。恢复后由实际执行入口做只读复验，沿原 Run 接续。

把主动求援接到冻结阶段中。关键歧义时暂停受影响的写入，绑定原任务、Pi 会话和目标，使用已登录的 shared_browser MCP 提交一次。先核对工具参数及 target。发送或读回不明时按标记回查原标签，对 MCP Result 先解包再校验答复，仅补未完成步骤。保留真实请求、裁决及独立复验回执。详见[Windows 已验配方](references/windows-proven-recipes.md)。

## 复用边界

- GPT 冻结合同、裁决和审核，Pi 执行并留存原会话与写入，调度器负责持久化和接管。生产自托管按官方持久化配方，start-dev 与 SQLite 用于本机验证。两路对照使用相同业务合同和可比负载。
- 沿用既有 Docker 登录启动和健康检查，分别读回引擎、目标容器、当前端口和应用。共享服务完成签收后才注入重启。读取状态与实际执行各自取证。
- 测试不添加任务墙钟或累计 token 限额。连接探针和接管等待按各自合同执行。无法证明的关口维持待验，使用原冻结证据确认故障范围。

## 按需查阅

- 部署选型与分级验收见[路线](references/routes.md)和[手册](references/runbook.md)。
- 接续与复核见[交接合同](references/pi-comparison-handoff.md)、[派工与恢复证据](references/dispatch-recovery-evidence.md)和[定点修正](references/recovery-and-candidates.md)。
- 既有实测见[首轮证据](references/evidence-r1.md)、[R70–R75](references/evidence-r73.md)及[Windows 已验配方](references/windows-proven-recipes.md)。版本发布及本机读回见[同步规则](references/skill-sync-recovery.md)。
- R169 定点复验和三路隔离计时依据见[实测回执与对照合同](references/r169-recovery-acceptance.md)。
