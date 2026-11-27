# R70–R75 本机证据与复用配方

原始证据目录为 Windows `<历史工作区>`。冻结短任务和校验器散列见 `COMPARISON-FREEZE.json`。GUI 基线为同一合成预约数据 r11，各路线使用独立前端、后端和数据目录，实际使用 OMP 18.18.0 与正式浏览器入口。

## 单轮诊断数据

| 场景与计时范围 | Temporal | Conductor | Agent-Autoloop | 验收 |
|---|---:|---:|---:|---|
| 发票正常，调度提交至签收 | 01:02.645 | 00:49.491 | 01:14.513 | 7/7 |
| Pi 进程退出，调度提交至签收 | 01:17.503 | 01:17.769 | 01:48.583 | 7/7 |
| 写后回执前服务重启，重启至原记录可读 | 00:00.635 | 01:29.852 | 00:05.833 | 最终均 7/7 |
| 同上，调度提交至独立签收 | 00:45.134 | 02:40.863 | 01:21.805 | 最终均 7/7 |
| 写后回执前 Worker 退出，故障至独立签收 | 00:11.864 | 00:15.452 | 00:07.976 | 7/7 |
| 同上，调度提交至独立签收 | 01:39.601 | 01:05.509 | 02:00.931 | 7/7 |
| 真实预约 GUI，调度提交至独立签收 | 02:47.226 | 03:01.251 | 05:49.341 | 15/15 |

Conductor 的真实 GPT 裁决轮用时 05:04.002、独立校验 4/4，原 Pi 会话继续。由当前 GPT 对话根据冻结业务规则签发文件回执，适用范围为活跃 GPT 协调。服务重启是测试注入后的受控重启，证据覆盖应用接续。Worker 中断在 Pi 完成、调度器尚未收到回执时注入。三路线短试通过后继续验证活跃业务阶段的接管和整机或生产级故障恢复。表中时间均为诊断，正式 T_VALID 待统一入口及同合同长任务通过。

## 原始回执索引

| 场景 | Temporal | Conductor | Agent-Autoloop |
|---|---|---|---|
| 正常 | `temporal-direct-r71-result.json` | `conductor-l1-clean-result.json` | `autoloop-pi-r72-verified/receipt.json` |
| Pi 退出 | `temporal-pi-loss-r71-result.json` | `conductor-pi-loss-r71-result.json` | `autoloop-pi-loss-r72/receipt.json` |
| 服务重启 | `temporal-ack-gap-r73b-result.json` | `conductor-ack-gap-r73c-result.json` | `autoloop-ack-gap-r73/receipt.json` |
| Worker 退出 | `temporal-worker-ack-loss-r73b/receipt.json` | `conductor-worker-ack-loss-r73/receipt.json` | `autoloop-worker-ack-loss-r73/receipt.json` |
| GUI | `temporal-gui-r73-result.json` | `conductor-gui-r73-result.json` | `autoloop-gui-r73b/receipt.json` |

GPT 裁决见 `conductor-gpt-r73-result.json`、`gpt-composite-r73/receipt.json` 和同目录等待及权威来源记录。首轮失败、人工对账及修正后新试次分别保留。

## 复用与故障诊断

- Temporal 优先使用原生 Activity 直返。遇服务重启中断长轮询，重新连接同一个存储并读回同一 workflow/run。若 Activity 已完成，允许仅恢复工作流 Worker 收尾。独立 Worker 故障沿官方心跳与重试方式，复核原提交和产物，重试从核账开始。旧连接断开及 SDK 启动探针超时分别处理。原开发服务使用 SQLite，生产存储需另验。
- Conductor 3.33.0 使用原生 Worker 轮询和任务回传。旧 ACK 路径返回 404 后按该版本接口适配。隔离容器重启后读回实际回环端口，等待健康，验证原工作流及任务。区分启动期连接断开和 HTTP 应用错误。首次人工补回执的轮次保留为恢复证据。
- Agent-Autoloop 固定 v1.8.2，使用官方命令插件和隔离 Hub/Worker。命令由脚本目录定位冻结输入，完成时输出明确结论。若业务已完成而回执缺失，先核账并阻止重复执行。用原工作目录、原轮次、原回执继续。
- Cadence Go 官方样例 2/2；Python 样例收尾出现 gRPC 事件循环异常。Go 实际派发 Pi 时 Windows 拒绝访问 ACL 锁文件，暂停作为本轮比较路线。
- GUI 应用 r11 还原必须绑定各自后端。先用可见按钮完成两条新增和一次改期，按正式导航刷新。用下载事件捕获或冻结的有界候选读回收集真正导出的 CSV，核验逐格 XLSX、完整摘要、真实浏览器轨迹及原标签保留。首轮 GUI 有真实产物但违反轨迹和摘要合同，采用隔离复验。
- 真实 GPT 裁决沿 R75 当前对话文件交接模式，等待同任务的实际请求后签发。绑定原请求、输入及裁决散列，独立读回同一原生 Pi 会话和产物。

## R74 Temporal 组合复测

`temporal-composite-r74-result.json` 记录同一 Temporal Workflow 内依次完成真实 GPT 裁决与预约 GUI。账目阶段由当前 GPT 对话答复原请求，Pi 在同一原生会话完成，独立验收 4/4（`gpt-composite-r74/receipt.json`，02:42.393）。GUI 由独立测试实例运行，原生按钮操作、刷新、实际 CSV 与 XLSX 及浏览器轨迹验收 15/15（`gui-temporal-r74/audit/browser/FINAL.json`）。

调度提交至最后签收 **06:28.431**，包含本轮实际 GPT 等待及 GUI 准备和执行。此轮由 Temporal 测试入口提交，属于组合诊断时间。正式同合同长测仍需统一增强 Pi 入口路由、小时级代表任务及逐路线同合同结果。活跃 GPT 协调的通过证据限于同一请求回执与原会话接续。

## R74 Conductor 组合复测与核账

同一冻结输入的真实 GPT 请求及原 Pi 会话验收 4/4（`gpt-conductor-r74/receipt.json`，02:21.871）。首次 GUI 程序验收的标签检查重复统计浏览器回复中的 `Open tabs` 附录。根据冻结前后成功列表的索引和网址独立重算，连同原产物复核为 15/15（`gui-conductor-r74/audit/browser/FINAL-TAB-RECONCILED.json`）。复用检查块见 `r74-browser-tab-audit-block.txt`。

使用官方 Workflow Retry 在原工作流上接续，读取已签收的 GUI 和账目结果，仅补交调度回执。原业务没有重跑（`conductor-composite-r74-reconciled.json`）。调度提交至最后签收 **07:36.561**，包含人工核账与恢复，保留为组合诊断数据。

## 正式长测准入核查

- 正式增强 Pi 入口 `pi-capability-enhancement-20261028/Open-Pi.cmd` 调用同目录 `launch_pi.py`。该启动器仅有已验收的归档批量分支，其他请求直入原生 Pi。三条调度路线需在该入口完成同一冻结合同的接单和路由验收。
- 小时级 Louez 候选有原项目的有限范围交付先例。F015 终态 `long/F015-TERMINAL-20261111.json` 两组均构建通过、独立宿主验收失败、GUI 未运行。后续 `long-ecc312-r2/ROOT-CAUSE-REVIEW.md` 记录两组安装目录联接与生产打包器解析问题，另有宿主状态文件替换失败。两组均无构建完成与独立签收回执。
- 若继续复用 Louez，先用成功参考的固定源码、锁文件、工具及账户在隔离新目录验证实际生产构建与产物，再验原业务、恢复和真实 GUI 的参考合同。此项准备单独取证，再从统一入口按同一故障点派工并计时。正式比较只纳入最终独立签收合格的轮次。
- 可复用的构建对照位于 `long/reference/R/build_local.py` 与 `build-results.json`。语音构建、网页类型检查和网页生产构建依次退出 0，分别为 02:42.899、11:21.973 和 06:41.237。该回执证明参考实例构建完成。隔离新目录的构建、恢复和最终签收仍需各自原始回执。

## R74 Agent-Autoloop 组合复测

同一冻结输入的真实 GPT 请求及原 Pi 会话验收 4/4（`gpt-autoloop-r74/receipt.json`，04:44.913）。预约实例从冻结修订 11 启动。原生 Pi 的浏览器记录仅有列标签操作，连接原浏览器后仍超时。试次退出 1，无 CSV、XLSX 和 GUI 签收。退出后独立复核业务修订及快照与冻结基线一致，确认没有发生预约写入。保留 `gui-autoloop-r74/audit/browser/EXECUTION.json` 及 `autoloop-composite-r74/home/worker/runs/1-1/stderr-1.log`。同一原浏览器可读版本信息，核对仅本试次占用后，用既有入口重建共享 MCP 传输；原浏览器身份保持一致。后续先通过同入口的只读列标签验证，再接续 GUI，复用已签收的账目产物。此轮无合格组合时间。

恢复后，沿既有 `localhost:8927/mcp` 的独立 MCP SDK 探针能初始化会话，但同一 `browser_tabs list` 仍返回工具错误。HTTP 就绪和浏览器版本探针均不能作为 GUI 就绪证据。此时保留原浏览器和账目回执，暂停 GUI 重派，待同一正式入口先证明只读列表恢复。


## R75 继续实测范围

Temporal OSS 与 Conductor OSS 继续做同合同测试。R74 组合诊断记录为 Temporal 06:28.431，账目 4/4、GUI 15/15；Conductor 07:36.561，账目 4/4、GUI 核账后 15/15，包含人工恢复。Agent-Autoloop 账目 4/4，GUI 未通过，暂停当轮资格。三条路线历史结果全部保留。共享浏览器接入失败属于已观察到的环境故障，现有证据不足以归因于 Agent-Autoloop 调度器。

MH 测试依次核对双路入口、公共 GUI 的只读就绪、小时级基线及相同节点的故障注入。正式排名只使用实际增强 Pi 接单到最终独立签收的同合同完整时间。先验隔离入口兼容及发票 7/7，再进入共同长任务。

R75 已从生产 `Open-Pi.cmd` 复制同一入口到 `enhanced-pi-mh-r75`，加入显式测试分支，回退路径仍返回 OMP 18.18.0。两条路线顺序执行同一冻结发票和 7 项独立校验。Temporal 的隔离增强 Pi 接单至读回签收 01:17.678，调度至签收 01:07.494，工作流 `reality-mh-r75-temporal-normal`。Conductor 分别为 00:51.704 和 00:51.156，工作流 `<RUN_OR_SESSION_ID_11>`。回执见 `temporal-mh-r75-result.json`、`conductor-mh-r75-result.json` 及隔离入口目录的原控制台日志。Temporal 的本轮接单时间含开发服务冷启动，Conductor 复用已就绪容器，两者是入口诊断。共享浏览器沿原入口的只读列标签探针重新通过。

### MH 后续接续记录

- 同一隔离入口的组合轮已提交两条路线，二者的真实 GPT 裁决分别绑定本轮请求，原 Pi 会话账目各 4/4。Temporal 的预约工具在实际运行时复现 CDP 接入超时；新标签请求虽超时，读回证实只开了一个测试标签，原 Pi 随后继续操作。
- Conductor 在等待浏览器前，包装程序对二进制日志写入字符串而退出。已修正写入类型，独立查到原工作流 `<RUN_OR_SESSION_ID_12>`、原任务 `<RUN_OR_SESSION_ID_13>` 仍在执行，沿原任务接续并复用账目。共享桌面一次仅执行一个 GUI，第二路等待原 GUI Worker 退出的时间如实留在诊断回执。
- Louez 隔离基线核对原档案 3548 个文件，其中三个差异映射为参考锁文件与两份已从参考移除的非运行文件。按原参考命令锁定安装，pnpm 10.27.0 退出 0，锁文件散列不变，网页工作区的 `@louez/config` 链接实际指向本组源目录。DB/对象存储隔离就绪，语音构建 00:05.842、网页类型检查 02:09.981 均退出 0。原始证据在 `louez-mh-r75-baseline/INSTALL-RESULT.json` 与 `BUILD-STAGES.json`。第三段生产构建及后续独立业务验收另查终态。

- R75 Temporal 组合试次已退出 0，原工作流 `reality-mh-r75-temporal-composite`，账目 4/4、真实预约 GUI 15/15。单次导出事件等待超时，复用该次实际下载文件，独立核对 CSV、XLSX、三次预约变更及原标签。隔离增强 Pi 接单至终态读回 32:26.662，调度提交至签收 32:01.161。GUI 记录 15 次已恢复工具错误。含本地服务启动、重试及与基线准备并行的主机负载，仅供诊断。原回执 `temporal-composite-mh-r75-result.json`、`gui-temporal-mh-r75/audit/browser/FINAL.json`、`enhanced-pi-mh-r75/temporal-composite-console.log`。退出后共享浏览器已释放，Conductor 已从原工作流进入 GUI 实例准备。

### 第 76 轮复核和中文口径

- “租赁预约长任务的共同起点”指 Louez 的固定源码、依赖、隔离测试数据、网络条件和验收程序。“锁定安装”只确认依赖按固定版本装好。修正网络后，独立合成业务校验 15/15，数据库备份和独立还原均通过。两条调度路线的正式长任务仍待同条件派发和独立签收。
- Conductor 第 75 轮独立终态为失败，界面 11/15。CSV 数据行与工作簿明细通过，汇总字段、单次导出证据、禁用页面求值和原标签保留失败。00:51.704 对应此前独立发票短测 7/7。失败的组合轮无完整合格时间。
- 第 76 轮在新隔离数据上通过原 Conductor 接口派发界面专项复测。真实 GPT 针对失败证据给出操作规则。账目沿用上一轮已独立核验的回执。第 75 轮数据和失败记录保留，专项复测单独验收。
- 外部生产证据包括 [Netflix 原始 Conductor 工程记录](https://netflixtechblog.com/netflix-conductor-a-microservices-orchestrator-2e8d4771bf40)、[持续维护的开源 Conductor](https://github.com/conductor-oss/conductor/releases)、[Uber 的 Cadence 生产规模与场景](https://www.uber.com/it/en/blog/announcing-cadence/)、[DBOS 的 Orderful 案例](https://www.dbos.dev/case-studies/orderful-resilient-edi-at-scale)和[开源 Python 实现](https://github.com/dbos-inc/dbos-transact-py)。Cadence 仍须解决本机接入问题，DBOS 尚无本机同合同回执。两者外部证据用于决定是否进入本机验证，完整合格时间仍以实际签收为准。
- 第 76 轮终态已确认：Conductor 工作流 `<RUN_OR_SESSION_ID_14>` 正常结束，真实界面独立验收 15/15，调度提交至完成 03:34.117。原始回执 `conductor-mh-r76-result.json` 与 `gui-conductor-mh-r76/audit/browser/FINAL.json`。该时间仅覆盖新隔离数据上的界面专项，不合并进第 75 轮，不用于正式长任务排名。
