# Polsia 母任务：跨节点连续执行合同（2026-10-11）
TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
METHOD=ENGINE.md@28
MODE=GPT_CEO_CODEX_EXECUTOR
MOTHER_FINAL_VALID=NO
USER_DECISION=CONTINUE_ACROSS_NODES_WHILE_PC_ON;PERSIST_ON_SHUTDOWN
SOURCE_OF_TRUTH=CURRENT.md;REUSE_ONLY_V4.md;ACCEPTANCE_V2.md
STATUS=NEXT_NODE_READY

## 前节点实况
第一节点 CODEX-001 于 2026-10-11 19:27（Asia/Shanghai）正常结束、非崩溃。产物仅在本机 C:\AI\Polsia-Codex-20261011：RESULTS.md、CAPABILITY_MATRIX.md、REUSE_MAP.md、EXCEPTION_RECOVERY_POC.md、FREEZE.md/JSON、TEN_RUNS.jsonl、evidence/。前节点研究及现成文件技能发生目录已存在故障的10/10恢复验证已完成；不是 Polsia 全部能力和生产等效认证。绝不可重做这些旧场景凑次数。
原线程 01a12a8b-c267-7c23-ab70-2e2051ca5137，模型gpt-6.1-sol，effort ultra。结束后不等于母任务完成。

## 执行和接续规范
- 每次由 Windows 原生 Task Scheduler 定期启动 Codex CLI。任务启动前按固定 session ID 检查有无正在执行实例；存在则不重复。计划任务仅负责触发（成熟OS能力），不实现新队列、锁、重试系统。
- Codex 启动后先读本文件和REUSE_ONLY_V4、CURRENT以及本机实际RESULTS、CAPABILITY_MATRIX、REUSE_MAP、FREEZE；定义下一个有价值的自然执行节点，复用成熟现成产品、技能和接口。默认持续到该完整节点冻结；超长上下文利用Codex原生压缩及当前任务文件接续。优先现成一人公司平台或 n8n 已有真实业务/多智能体能力，避免新造前后端和通用系统。
- 第28版仍要求现实基线、<=3成熟候选、真实瓶颈、完整虚拟时间与STOP_GATE、Freeze后最终Reality一次，不允许逐点无序Reality；10轮是整套相同冻结合法场景的稳定性核对。不将简单文件样例10/10冒充真实公司能力。
- 每节点在结束前必须写入隔离目录最新 MOTHER_CURRENT.md：TASK_ID、NODE_ID、STATUS、已完成、缺口、证据路径、RESULT=PARTIAL/BLOCKED/DONE、NEXT，以及对整体FINAL_VALID的准确判断。能写GitHub则沿官方Contents API精确更新原任务CURRENT指针并回读；失败必须明确，不能冒充持久化成功。最少保存本地证据。
- 一次执行器完成节点后，可自然退出；下次原生计划触发自动接续。这是母任务持续运行，不强制一个上下文超长数小时。保持 GPT CEO 独立审核权。
- 母任务完整全功能真正验收之前，FINAL_VALID=NO。只有完整功能符合用户验收且真实凭证齐全后，由CEO核验最终达成；不要自称全项目成功。运行消耗较大时留存实际配额记录、时长。
- 需要生产支付/投放/外联/账号更改或明确安全拒绝，不能自动越权；对该步骤记 AUTHORIZATION_REQUIRED，其他独立合法任务可继续。若全部剩余合法任务已确证需用户介入，在隔离目录创建 MOTHER_WAITING_FOR_USER.flag 并说明，不要反复空跑。
- 遇成熟技术阻塞，用 GOOD/BAD/FIRST_DELTA，原工具回执和官方恢复方法继续，不因一次失败就退出；不改代理、FlClash或已有浏览器，不启动另一浏览器，不泄密。

## 下一最小独立节点（CODEX-002）
在保留 CODEX-001 实证成果基础上，选定一个已存在且合法可执行的真实AI公司能力端到端流程（优先 n8n 已有工作流/现有一人公司成品/公开授权的现成接口）。先只读检查可用版本、业务入口与输入输出合同，证实无副作用后做现实基线、虚拟成熟、Freeze、一次真实认证；对同合同业务再10轮稳定性。若找不到合法可运行入口，优先提升使用已安装成熟平台现成内置功能与最小配置，不自研。此节点不能因已生成“参考方案”就算完成。
