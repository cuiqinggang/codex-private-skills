# Orca 集成操作流程 1.1｜有界等待与原任务恢复
日期：2026-10-16 北京时间
METHOD=三人行第2版 C002；BRIDGE=V7.0 C优先/A暂停/B备用。
范围：项目操作规程小修订，不修改方法整数版本、桥版本、现役Windows脚本或正式融合包发布状态。本轮只做固定源码审查、既有证据复核和纸面故障推演；没有新Windows业务测试。

## 直接采用的成熟组合
GPT负责决策及独立验收；Orca提供官方隔离工作树、终端及任务记录；Codex采用官方exec标准输入和精确session resume。
已接受的业务成果为CEO_EXEC_RECOVERY_TEST_V4.md与evidence/EXEC_R3_RECOVERED/：外部3/3、模型离线5/5，原BAD2/3。该成果DONE，禁止重做。原worker-start无产物入口退出当前候选，不宣称其根因已修好。
管理接入候选固定为官方context-only dispatch --return-preamble（不加--inject）→原文stdin→worker_done→官方状态回读→外部QA。该模式是unsupervised/context_only，不能宣传成Orca自动监督、自动恢复或完整自动调度。不要另写通用调度器。

## 有界等待：先区分三种超时
1. 工具返回running + call_id/PID：只取原调用结果，不重发命令。工具等待窗口不是业务失败判据。
2. 模型请求暂时超时：允许官方客户端在当前预算内恢复；retry日志、heartbeat及ready不能重置任务总截止时间，也不证明业务进展。
3. 派发/完成回执超时：可能已经提交。先查同一run/task/dispatch及mutation request，不能创建新派发或重跑业务。

### 下一次小任务验证的预算候选（尚未部署、尚未证明最优）
保留既有初次360秒、最多一次同会话恢复600秒；整个单任务节点1200秒硬截止（从输入交付的单调时钟开始）。恢复不重置总截止；启动、取证、退避、清理、验收与回读都计入。余额不足以完成剩余动作时保全证据并记BUDGET_EXHAUSTED，不自动加时。1200秒是本项目选定上限，不是厂商推荐值，不保证所有任务能完成。
普通只读CLI沿用25秒上限；worker_done不得套用25秒：固定源码内置120秒runtime_unavailable重试，候选外层150秒且受全局剩余预算约束。单次RPC/后验查询也耗时，150秒不承诺结算必完成；到时转UNKNOWN，回读对账。
当前两个脚本仍使用统一25秒run_cli；此次仅指出下一适配必须分层，不声称脚本已经修改或安装了自动恢复。
没有模型输出不能单凭静默秒数判定卡死；在360秒预算内结合真实工具调用/文件差分观察。明确退出或不可恢复拒绝可提前结束；预算到达则停止本任务所属执行并对账，不无限等日志。

## 超时后的确定动作
- 首先固化原session/run/task/dispatch/request ID、输入摘要、worktree、有效模型/权限、现有文件差分、退出回执及UTC/单调时间。身份信息只记录必要非敏感值，不输出令牌或认证文件。
- DONE且外部QA接受：只补缺失归档/管理回执，不再启动模型。
- 仍有本任务进程：先读取原结果；若到截止，仅按已核验归属关闭自身终端/进程树；未确认退出不得resume或新派。
- UNKNOWN：核对实际进程、退出码、原会话事件、文件及官方dispatch/task状态；不能因连接断开就认定未执行。
- 确认未完成且原进程已退出：保留已有成果及恢复前副本，官方exec resume 精确UUID继续，最多一次。禁止resume --last、换会话重新做、重新派相同业务。
- 会话不存在、工作树/输入变了、身份不符、权限拒绝：返回整体分析，只修复首个差分；不扩大权限或循环重启。
- 已完成业务但worker_done结果UNKNOWN：先查原dispatch/task；只在确需恢复时原正文配原--retry-request，不能使用新request ID。没有原身份或ID时保留UNKNOWN，不冒用其他terminal、不改数据库、不预填completed。
- 恢复预算耗尽：记录已有产物、未完成项和确切故障，回到虚拟成熟；禁止第二次自动恢复。本任务独立合法准备可继续。

## 官方管理身份及结算
在真实Orca创建的专属终端内部执行CLI，让官方注入身份随子进程继承；不得从终端列表挑别人handle或伪造ORCA_PANE_KEY。resolveCoordinatorTerminalHandle会核验活跃身份；structured无自身身份时拒绝推断，遵守拒绝。
dispatch必须绑定真实run、ready task、真实assignee，保存官方返回preamble与ctx ID。不以ctx_dryrun/ctx_preview占位进入业务。
worker_done携带准确taskId、dispatchId与outcome；heartbeat同样绑定两ID。官方五分钟heartbeat是存活信号，不是延长任务时限的理由。
完成发送要检查lifecycle结算；仅“Sent”或队列accepted不是最终接受。官方requireWorkerDoneSettlement在必要时同时核对dispatch、task和worker_report来源，UNKNOWN保留原mutation身份。
Orca worker报告成功与CEO外部业务QA是两个层次：外部QA失败则CEO不得验收，即使Orca显示completed。不得为凑通过而修改验证器。
context-only不自动关闭操作者pane；结果归档后显式关闭本任务终端并独立核对所属进程。

## 虚拟故障推演（静态推演，非执行测试）
| 输入情况 | 唯一下一动作 | 禁止动作 |
|---|---|---|
| ready/turn_started但无业务产物 | 在固定预算内看事件，截止对账 | 标成功或反复补Enter |
| request timed out后有工具事件 | 在原预算内继续 | 每次重连重置计时 |
| 360秒到达且只完成测试文件 | 停止所属进程、确认退出、保留差分后精确resume | 从BAD重做 |
| 超时但原进程仍存活 | 处理原进程并回读 | 并发resume |
| exec exit0无产物或QA失败 | 业务未接受，定位最小差分 | 以exit0验收 |
| 产物已QA接受，回执连接超时 | 只恢复管理结算 | 重跑业务 |
| worker_done短暂runtime_unavailable | 官方同ID指数退避，上限15秒间隔/120秒窗口 | 25秒外层提前杀或自建重试循环 |
| worker_done operation_unknown | 查task/dispatch，必要时原request恢复 | 新ID再次提交 |
| 身份过期/缺失 | 官方自身身份解析，不能解析则停止该动作 | 借用其他pane |
| 恢复预算/全局预算耗尽 | 保全证据，返回分析 | 无限制第二轮恢复 |
| 新任务profile可能恢复旧启动命令 | 复用已验新隔离profile与现有工作树方式，重新核对管理绑定 | 携旧dispatch冒称原身份 |
| C返回异步调用 | 原call_id取结果、完整解析后归档 | 把running文本当成果或重发 |
结论：上述处理规则已完成静态一致性审查；不是Windows自动恢复实现通过，也不是整套优化STOP_GATE通过。

## 固定来源与证据
Orca固定提交2bb20586ebc39d605e16d95f57420e20a16e7485：
- src/cli/handlers/orchestration/message-send-handler.ts，blob3b024de2cffa535329d735a47eb41614404d9b02：worker_done 120000ms重试、身份拒绝、senderPaneKey及结算。
- src/cli/handlers/orchestration/mutation-request.ts，blob2e9836c20efa78a83ade88dd81228221b94883e0：同request ID，1秒起指数退避、15秒上限，只对runtime_unavailable自动重试。
- src/cli/handlers/orchestration-worker-settlement.ts，blob4a71d88e7b730469cfafd907237115b69d386e73：后验结算与--retry-request。
- src/cli/handlers/orchestration/terminal-identity.ts，blob8cc4f3357e03b04295d7b6aeffa4850613e68d3a：自身身份解析/拒绝猜测。
- src/main/runtime/rpc/methods/orchestration/runs/dispatch-methods.ts，blob041ae7fff3834892a4e91041328c6b9aa66d1aa9：context-only真实dispatch及官方preamble。
- src/main/runtime/orchestration/preamble.ts，blob8af6aa756bb8a07f363886a3aa62c86427bf2a04：task/dispatch绑定、五分钟heartbeat、worker_done后停止。
Codex rust-v0.160.0，codex-rs/exec/src/lib.rs，blob0bfa07bd5587f6913b21d137874430a982824c15：官方thread/resume及有效权限传递。实际有效策略以既有V4 turn_context证据为准。
本轮初次猜测message-handlers.ts路径404，随后仅用搜索发现路径，再回读固定提交message-send-handler.ts；没有以最新分支替换固定版本。

## 验收边界与下一差分
本次交付：成熟官方恢复机制选定、已验GOOD固化、分层超时规程及12种故障纸面推演完成。
尚待虚拟闭合：服务端context-only身份/launch-token结算全链及恢复时旧dispatch与新终端的合法归属，不能以CLI身份检查替代服务端审查；候选适配脚本的分层deadline与完整计时尚未实现审查。
后续先完成这两处具体静态差分，再冻结一次管理链验证；此次按用户要求不做实际探索。整个项目FINAL_VALID=NO、正式三任务Reality=0、十轮=0/10、AB=0/10；不宣称网络已根治、全局最快或正式融合发布。
