# CEO独立来源复核与虚拟比较 V1
TASK_ID=ORCA_CODEX_VALUE_VALIDATION_20261014
AUTHOR=GPT_CEO_DIRECT_READING
REVIEW_STATE=STATIC_SOURCE_REVIEW_COMPLETE;PERFORMANCE_UNKNOWN
READ_DATE=2026-10-14
FINAL_VALID=NO

## 官方来源与固定候选
- Orca官方仓库：https://github.com/stablyai/orca
- 本次核对稳定发行v1.4.224，GitHub API published_at=2026-10-10T04:30:28Z，target_commitish=2bb20586ebc39d605e16d95f57420e20a16e7485，prerelease=false。
- Windows发行资产orca-windows-setup.exe，222555816字节，官方API digest=sha256:d192a7f1142b58a8c9bc855275fb37cd41dff7f152fd3cbac3acdd96331ec849。尚不能仅凭这个元数据宣称下载、安装或本机运行通过。
- CLI：https://www.onorca.dev/docs/cli/overview 与 https://www.onorca.dev/docs/cli/reference 。CLI随桌面应用提供，控制运行中的Orca；不是下载单独npm包即可替代完整runtime。
- 编排：https://www.onorca.dev/docs/cli/orchestration 。官方标记Experimental；Run只是持久命名空间/收件箱，本身不安排工作。旧orchestration run/run-stop/coordinator-start/coordinator-stop无效果，必须用当前Run + worker-start流程。不能照旧博客运行空命令后计成功。
- 服务器：https://www.onorca.dev/docs/remote-servers 。Remote Orca Servers为Beta；orca serve提供无桌面窗口入口，默认orcad、必要时回退Electron。文档的典型场景为Linux/服务管理VM，不等于本机Windows同样已验收。禁止为此新增远程公网接口或启动本次已停止的Ubuntu。
- 隐私：https://www.onorca.dev/docs/telemetry 。本次Orca进程局部设置ORCA_TELEMETRY_DISABLED=1或DO_NOT_TRACK=1可以关闭产品遥测；这不等于模型推理完全离线，不改系统环境变量。
- Orchestrator.inc：https://github.com/OrchestratorInc/agent-orchestrator 。Apache-2.0，原生本地daemon/任务工作区/工作树/PR和CI状态；本次只作官方能力候选，不预先安装第二套大型系统。
- Codex官方CLI：https://developers.openai.com/codex/cli/reference/ （读取时重定向learn.chatgpt.com）；非交互：https://developers.openai.com/codex/noninteractive/ 。--worktree支持本地exec；--json提供thread.started、item和usage；按指定session_id恢复。用已有登录，不读出或复制auth.json。

## 公平比较的关键差分
| 候选 | 已有成熟能力 | 额外收益须实测 | 本次决定 |
|---|---|---|---|
| A 现役Codex原生入口 | 官方工作树、精确会话恢复、JSON回执、本地工具；既有GPT CEO和线上冻结 | 现役流程管理成本和失效恢复完整耗时 | 必须作为GOOD，不故意关闭已有能力 |
| B Orca | 多工作区/终端/Agent状态、CLI、checkpoint、编排API | 减少人工切换/依赖管理/恢复的时间，扣启动、配置、常驻、适配和自身故障 | 第一隔离候选，不预定更快 |
| C Orchestrator.inc | 项目协调Agent、独立worker、工作树、任务/PR/CI闭环 | 同合同下的总时间、Windows资源、接入成本 | 静态备选；不写未实测性能 |

相同底层Codex模型、相同并发槽数时，B不是新增模型算力。其可能优势主要来自调度、隔离、恢复和管理；对于本来就能由A一次完成的任务，新增层可能反而更慢。测试要包含至少一个真实依赖/恢复/整合型任务，不能只用三个彼此无关的小修改放大或掩盖优势。
Orca支持很多记录，不证明很多活跃模型；现役机器4核且有其它进程，本次初始最多2个本任务模型进程（含协调者）只是资源保护配置，不是容量结论。

## 虚拟故障推演（未运行、不得写PASS）
1. 多任务碰同目录：使用原生Git Worktree与固定输入SHA；检查未授权文件变更及最终合并冲突。不是仅检查目录名不同。
2. 会话退出/断联：以精确session、回执和产物对账，只有NOT_DONE重试；UNKNOWN不自动重发，DONE不再执行。
3. 依赖/配额等待：持久记录任务而不同时占用所有模型进程；尊重供应商限流，不改账号/代理绕过。
4. 产品版本/界面变动：固定发行、CLI与运行时一致，不能拿main新文档假定旧二进制支持；以本机--help及真实结果核对。
5. 验收独立性：创建样本的协调者可能看过修复答案；不能据此宣称测试worker也盲测。独立worker须新会话、原始BAD源码、不含修复commit内容/答案；外部验证在其工作结束后执行。
6. 十轮后版本修复：不混版本凑通过；失败历史保留，最终冻结重新连续十轮。故障注入预期阻塞和意外故障分栏，不把预期异常视为软件零故障证明。

## 时间下界与判断边界
可用推理下界是关键依赖路径时间、总CPU工作/有效CPU能力、模型token量/合法吞吐配额等约束的最大值；这些量未实測前数值为UNKNOWN。不能用任务数除并发数当真实极限。
现有SRX run_one.ps1明确只计CLI请求→独立QA，排除GPT规划合同；原生432任务哈希/等待测试也不是模型级并发实证。两者仅各自范围的GOOD参考。
本任务最终以CONTRACT_V1.md的10轮配对、全过程和一次性成本判决。连续10轮无意外故障只支持本合同观察结论，既不证明永无bug，也不证明部署已回本。
