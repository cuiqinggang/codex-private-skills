# 无界面接入虚拟审查 V2
时间：2026-10-16（北京时间）
方法：三人行V2 C002，本任务固定；桥V7，C优先，A暂停。
范围：Orca v1.4.224，源码2bb20586ebc39d605e16d95f57420e20a16e7485。
结论：最小测试方案已具体化，配置与关键分支离线检查9/9；整套VIRTUAL_MATURE仍NOT_PASSED，不能据此批准业务执行或宣布极限优化完成。
本轮未调用Windows执行、未启动后台或模型、未重发历史被拒预检。没有新的平台拒绝。

## 重要纠偏
此前把桌面CodexRuntimeHomeService的迁移/镜像流程持续作为orcad主要阻塞，缺乏实际入口对应。
固定orcad-entry.ts（384642b924712da477a5d7da86c6504a37520bd8）调用registerHeadlessPtyRuntime时Codex Home与Claude Auth回调均传undefined；register-headless-runtime.ts（424cb40facdb81f4ab79a7f4d956b4c0cd45af5d）如实转交。runtime/spawn-preflight.ts（c82b0656a377017f0cdf15bf1ea8aaf1311e41bb）可选Home回调不存在时取null。
这闭合的是直接注册链路，不是用注释证明整个模块图不存在其他副作用。后续无需为桌面构造器继续无边界展开；应围绕实际headless链路与继承环境取证。
旧迁移标记不删除，旧profile不导入，新Orca目录不重定向真实HOME/USERPROFILE/APPDATA。

## 设置入口收敛
settings.update的固定schema（client-settings-params.ts，4f70beb9973906d1620cbb4817aec68a8960adbe）允许agentDefaultArgs、agentDefaultEnv、agentStatusHooksEnabled，但不含agentWorkspaceTrustEnabled和experimentalNativeChat。不能假造全量RPC写入。
新目录采用官方首次JSON导入机制：
profiles/local-default/orca-data.json → createOrcadProfileStateStartup → createProfileStateStoreForStartup → bootstrapProfileStateAuthority(json-only) → prepareLegacyProfileState → 官方SQLite迁移。
profile-state-authority-bootstrap.ts=8f784714687d11056834cca87bbc3d117c2ab80d；
profile-state-legacy-import.ts=9eb5219ee6b4573779c1ea83cbb18a27df6323ac；
normalize-loaded-global-settings.ts=acf5a485ddd0ef57c22e3d02a6a0bce899bfc66b。
仅新建且确认无既有状态/锁/数据库的本任务新目录可用；不覆盖SQLite authority，不反复回写旧JSON，不关闭保护机制。
已备配置：analysis/headless-v2/orca-new-profile-seed.json。它是候选输入，未导入本机；根解析通过不等于完整Store导入通过。

## 配置与参数合同
- agentDefaultArgs.codex明确--sandbox workspace-write --ask-for-approval on-request；保留原审批策略，不添加bypass或自动批准提示。
- agentDefaultEnv.codex为空对象；agentYoloDefaultsMigrated=true是官方设置迁移字段，用于维持手动权限默认，不是关闭安全审查。
- hooks=false、工作区预信任=false、experimentalNativeChat=false。
- 空托管账号，系统默认登录；Windows runtime={kind:windows-host}、PowerShell；不启动WSL。
- worker-start明确agent=codex、model=gpt-6.1-sol、effort=ultra；CLI handler会先检查runtime capability。不支持就失败，不能静默降级模型。
- 本配置没有填入未验证的priority参数；原合同priority请求的准确传递仍须补齐。服务端实际tier保持UNKNOWN，不能仅凭请求推断。
- Home环境：官方只在CODEX_HOME与ORCA_CODEX_HOME相同时清理继承的Orca覆盖；用户自定义CODEX_HOME保留。不能把“未设置”与“子进程最终为空”混为一谈。
- 后台的hook server即使hooks=false仍可能建立本机服务；该设置控制hook行为，不等于不启动任何监听。服务、数据库及日志只允许本任务范围；外部配对关闭。
- orcad停止不保证daemon及PTY全部退出：固定入口明确daemon用于持久终端，回滚必须按本任务真实资源身份处理，不能仅杀父进程或删除锁。

## 协调者与派发链
terminal-identity.ts（8cc4f3357e03b04295d7b6aeffa4850613e68d3a）要求真实调用者终端或会话身份。外部GPT不能臆造--from，也不能借别的任务终端。
由Orca在本任务工作区创建专属协调终端，将计划提交到该终端内部；官方注入身份后run-create/task-create/worker-start按回执取得runId/taskId/dispatchId。协调终端不必额外启动第二个推理模型，GPT仍是三人行母任务唯一CEO，Orca负责执行管理。
任务创建不等于自动调度；worker-start.state=ready不等于修复成功。模型真正完成后仍需外部验证。
调用者或运行结果UNKNOWN时使用官方request-show/worker-show及产物对账，不制造新请求ID盲目重派。
实际协调终端注册与派发尚未端到端执行；本轮只验证接口源码，不宣称自动CEO闭环已经运行。

## 一次最小业务测试边界
在新副本重放T03原始BAD，不改GOOD_003_CEO_RECOVERY。一个Codex worker，使用已有固定输入/验证器；对空数据及正常报告均检查。运行前必须具体绑定输入摘要、工作目录、可执行文件、旧会话状态和任务身份。
从输入交付开始计时，到外部验证及最终回执持久化回读结束；部署与准备单列，失败/等待不删；不以9项离线检查耗时计算业务提速。
通过只说明单任务接入；三任务正式Reality、10轮和AB仍分别为0。

## 虚拟失败推演与处理
| 情形 | 处理 |
|---|---|
| 新目录意外已有DB/锁/历史pane | 停止新建，先核对归属；不删锁强开 |
| 官方JSON导入拒绝或设置被归一化改变 | 保留错误和新目录，回虚拟修正；不启动模型 |
| 缺少Codex参数键、出现bypass | 拒绝派发；显式限制写入后重新冻结 |
| 模型/effort能力不支持 | 失败保留，不换模型美化结果 |
| 实际Home/可执行文件/审批与合同不同 | 停止派发，定位首个差分；不复制登录补洞 |
| 协调终端身份不明 | 不借旧handle；创建/确认本任务真实身份 |
| 超时或连接断开 | 先查询原dispatch及产物，UNKNOWN不重复 |
| hooks关闭导致状态不更新 | 结合官方worker状态、终端输出和外部验证；不能伪造completed |
| 任务失败或验证不通过 | 保留BAD与成本，回虚拟修正，重新冻结 |
| 后台退出但daemon/worker仍存在 | 按任务资源回执清理；不关其他业务 |
| 新具体调用被平台拒绝 | 停止该动作，保留原文；不换通道重发 |

## 本轮实际离线证据
analysis/headless-v2/含固定源码快照、上游LICENSE、配置、virtual-v2-check.mjs、virtual-v2-result.json。
在Linux Node v24.19.0执行，源blob逐个核验；官方函数9项检查通过，包含缺键回落危险默认值的负例。依赖替身仅覆盖所列配置/早退分支，未测试完整Store/SQLite/PTY/模型。
原11项home-routing和本9项不是20次业务，不相加冒充稳定性。

## 尚未闭合，下一步只做这些
1. 完整官方Store→SQLite首次导入以及最终settings保留的验证；目前只有调用链和函数检查。
2. priority请求及最终模型/权限/环境从设置到实际子进程的完整证据安排。
3. coordinator→worker的实际接口参数、身份/回执完整绑定与旧会话现场对账。
上述没有被历史平台拒绝一概禁止，但不能把尚缺的工程实证写为PASS。本次不再展开与headless无关的桌面迁移代码。
