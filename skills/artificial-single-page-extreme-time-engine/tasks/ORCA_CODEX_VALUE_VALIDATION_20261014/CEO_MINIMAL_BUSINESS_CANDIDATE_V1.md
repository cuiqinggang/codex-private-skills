# 最小业务候选 V1：官方组件、单任务、明确权限
状态：准备候选，未冻结、未部署、未执行。不是重发旧GitHub运行时预检。
方法：本任务三人行V2 C002；执行桥当前V7，C首选、A暂停。
官方源码固定：stablyai/orca@2bb20586ebc39d605e16d95f57420e20a16e7485（v1.4.224）。

## 本轮已缩小的缺口
- runtime-home-service-sync.ts（blob b4df4e3521f9cc8e39285db835ae991cde350f48）：系统默认真实home分支提前return，位于captureSystemDefaultSnapshot及镜像写入之前；不能外推为所有启动服务零副作用。
- legacy-shared-auth-migration.ts（a9ecd4c2ea5f97f733e6c808f430b5974c38482a）：无activeHostAccountId或不匹配托管账号立即return。新状态、空托管账号可避开该项auth/MCP凭据迁移，不能靠删除保护标记实现。
- runtime-home-service-legacy-migration.ts（dcb337cac29a2f3acbb6dc155114c42f5c76086b）：无旧托管home时仍写一次migration-v1.json。这是预期的任务隔离状态写入，不应当要求整个程序零写入。
- runtime-home-service-paths.ts（de13c208566d73338301fc19670ade5286681a5d）：迁移元数据和托管账号根位于app.userData之下。必须核实实际app.userData解析，不能只看父环境。
- agent-workspace-trust-spawn.ts（f893529b53b8dcdfc11512bf1b5bb61bbeb3315c）：agentWorkspaceTrustEnabled=false时PTY与structured两入口都提前返回，避免本模块的预信任写入。
- codex-hook-reconcile.ts（085d5aa3a42271bab10da7396145676aa6cbc7cd）：config为空或isEnabled=false时reconcileOnce直接返回。此前笼统“关闭hooks仍必写全局配置”过强；应按实际入口区分，设置切换清理与其他hook调用尚需单独核对。
- default-global-settings.ts：hooks与预信任默认true，终端模式默认experimentalNativeChat=false，托管账号默认空。不能省略显式受限配置。
- profile-state-offline-settings.ts（708424cd6367e910c83da7ec35f6e45db5be2089）：官方提供带维护所有权/版本冲突保护的离线hooks更新机制；仅此函数不涵盖完整agent参数和预信任设置，不能据此手写数据库。
搜索只作路径发现，固定提交404的orcad-managed-agent-hooks.ts未引用为版本证据。

## 新任务的具体范围
单个Orca任务，单个Codex worker，在本任务下新隔离工作目录处理T03原始BAD源码的一个全新重放副本；不修改已验收恢复副本。修复空数据报告并保留正常输出，运行该任务对应的既有外部验证，回传补丁、测试结果与完成状态。
这是单任务集成烟测，不是三任务完整Reality，不计入连续十轮或AB配对。
输入需从已有固定清单核对摘要；不能临时造简单算术替代真实业务。

## 部署约束
仅新Orca数据目录，不导入旧profile、账号、pane或数据库；复用官方二进制。保留真实用户环境，不设置替代HOME/USERPROFILE，不复制凭据；若既有CODEX_HOME导致镜像分支，停下分析，不偷偷覆盖。
显式系统默认账号、hooks关闭、预信任关闭、终端worker；Codex固定0.160.0/gpt-6.1-sol/ultra，workspace-write及原审批策略不放宽，禁止默认bypass参数。
只允许本机127.0.0.1、关闭外部配对；保持原资源边界。
任务超时不自动重派；已生成产物先对账。允许正常Codex登录刷新，禁止代理脚本导出/上传/镜像凭据。
旧Orca进程归属及会话对账尚缺，不启动重复协调者。

## 必须补齐后才能冻结
1. 固定版本headless实际设置入口与存储位置，确认启动前全部限制生效；不得凭字段名直接改SQLite。
2. headless hooks入口、initializeLastSyncedState及环境解析的剩余链路。
3. 本机旧任务状态对账、具体可执行文件及最终子进程参数/权限的可验证回执设计。
4. 明确计时覆盖派发、执行、验证、最终文件写入与回读。
5. 对具体执行请求进行正常平台检查。旧被拒预检仍不重发；本候选尚未提交运行检查，不称已获平台批准或再次被拒。
当前正式Reality=0，连续十轮=0/10，AB=0/10；效率未知。
