# Orca 成熟部署路线收敛 V1
日期：2026-10-15（北京时间）
方法：三人行 V2 C002，本任务锁定；执行桥 V6.0，C→A→B。
状态：候选方案已收敛；未部署、未启动、未冻结为可执行版本。正式业务 0，连续通过 0/10，A/B 0/10。
承接：CEO_CHILD_PROCESS_CONTRACT_REVIEW_V1.md、CONTRACT_V1.md、CURRENT.md。

## 结论与具体选择
当前首选候选：Windows 原生、原交互用户、已有官方 Orca 后台和捆绑 Node、单独 Orca 数据目录、Codex System default、显式受限权限、终端 worker、官方 Run/Task/Dispatch/worktree 管理。
不新增调度器、不重装 Codex、不迁移 WSL、不添加网络通道、不替换现役系统。
这是依据当前约束选择的最小改动候选，不是已证明的全局最优或极限时间。

## 已获得的实际差分
本轮 C 通道 list_devices 发现 DESKTOP-4A1EGTM 在线；真实读取本任务目录与 CEO_START_ORCA_LOCAL.ps1 成功。未运行状态/help/模型命令。
启动器第10–12行将 USERPROFILE、HOME、APPDATA、LOCALAPPDATA 指向 CEO_assets/home；第14行同时设置 ORCA_USER_DATA_PATH 与 ORCA_USER_DATA 为 profile。
固定官方源码 orcad-app-paths.ts 的 resolveUserDataPath 优先读取 ORCA_USER_DATA，而 home 独立返回 os.homedir()。因此隔离 Orca 状态本身不要求改掉真实用户 home。
官方 Codex 文档说明 System default 使用真实 ~/.codex；官方 remote 文档说明执行端使用执行端的 PATH/home/登录。
推断：旧方案在“隔离软件状态”之外额外隔离了用户环境，可能引入登录、配置、CLI 解析差分。尚未启动业务，因此不能称这是已复现业务失败的唯一根因。

## 三个成熟候选的轻筛
| 候选 | 已有机制与代价 | 处置 |
| --- | --- | --- |
| 原生 Codex 入口 | 已有业务产物；无 Orca 管理层开销 | 保留公平比较基线，可能最终胜出 |
| Windows 原生 Orca，状态与用户环境分离 | 复用现有官方组件、原登录、官方 worktree/worker；减少环境适配 | 当前首选候选 |
| 官方桌面标准安装/运行 | 官方将本地桌面作为日常默认；UI配置直观，但有桌面/浏览器、全局状态和重复安装影响 | 本合同不优先；若后台不可行再核对隔离启动边界，不盲目安装 |
不增加 WSL/容器/远程服务器候选：与现有原生路径相比有迁移、认证及运行成本，当前没有收益证据。这里的三候选是部署路线轻筛，不取代原合同的 Orchestrator.inc 静态比较项。

## 最小部署差分清单（尚未应用）
1. 复用官方固定 v1.4.224 与原文件摘要。先核实原任务进程和 session 的真实结束/归属，UNKNOWN 不重启、不建第二实例。
2. 候选进程继承真实 Windows A 用户环境；不再重写 HOME/USERPROFILE/APPDATA/LOCALAPPDATA。只把 ORCA_USER_DATA 指向本任务新的独立候选数据根，CLI/daemon 对应的数据根也必须一致。旧 profile 和历史证据保留，不在未知活跃数据库上改文件。
3. 沿用已核实的官方本机绑定路径、127.0.0.1、关闭配对。不使用顶层 serve 的通配绑定来替代；不新增 Tailscale、SSH 或代理。
4. 候选隔离设置：experimentalNativeChat=false，明确终端 worker；agentDefaultArgs.codex 必须存在并采用保持原 sandbox/approval 的明确值；不得缺键落回 bypass。agentWorkspaceTrustEnabled=false，禁止自动预信任改写全局配置。此处只是官方字段规格，不是可直接覆盖全量配置文件。
5. Codex System default 复用原登录，不调用 account add/import、不复制 auth。必须进一步核对真实 home 下启动时旧镜像迁移/hook reconcile 会不会写原配置；关闭 trust 或 hooks 不足以证明零副作用。此缺口是上线前实质阻塞。
6. 固定 Codex 绝对路径与0.160.0版本；每个 worker 明确模型 gpt-6.1-sol、effort ultra。priority 请求通过已核对的真实配置入口落实，不虚构 worker tier 参数。启动回执和有效值分别记录。
7. 使用官方 run-create、task-create、worker-start 与 worker_done/taskId/dispatchId；完成后独立验收，再按官方释放机制回收。本轮没有执行这些命令。官方 Run 仅为持久命名空间，不会自动调度/推进所有任务；必须把有界协调成本计入，不能宣称创建Run就自动完成1000任务。
8. 初始最多2个本任务模型进程含协调者，最多1个CPU重构建，至少4GB系统空闲；复用官方依赖推进与事件等待，避免反复启动、密集轮询、重复桥接和重复模型审核。具体运行并发以合同和资源回执为准。

## 成熟性与失败推演
官方“Orchestration”页面明确标为 Experimental；使用成熟官方实现不等于该模块已在本环境验收稳定。
- 用户环境与数据目录分离：解决配置定位问题，但不是安全沙箱；原workspace-write必须保留。
- 运行用户若是NETWORK SERVICE：不能把其home当A用户；应停在归属核验，不复制凭据解决。
- 缺失 agentDefaultArgs.codex：拒绝冻结，不能接受默认跳过审批/沙箱。
- terminal模式回执不符：本轮失败并对账，不能悄悄切structured后合并计时。
- hooks/迁移触及原全局配置：不执行；继续寻找官方可禁用/无写入路径，不能改源码绕过审查。
- 超时/断连：按task/dispatch/session对账，保留失败成本；不使用新Run掩盖未知执行。
- 若官方编排无净节时或不能满足边界：保留原生Codex。项目目标是有效交付更快，不是强制采用Orca。

## 极限短时间的可检验路线
目标是同质量同权限的完整有效时间，不降低ultra或关闭审批换取假提速。
已有证据不足以提供物理秒数、提速百分比、容量或回本承诺。

按任务DAG的关键路径，可以给出形式下界：
T下界 ≥ max(最长串行依赖路径耗时, 必须完成的模型工作量/有效并发容量) + 不可重叠的独立验收与交付耗时。
各项尚缺同合同实测，数值保持UNKNOWN；不能把网络推理时间假定为常数。

应一次性冻结：真实三任务输入、固定模式/模型/权限、官方组件摘要、工作树策略、依赖缓存政策、事件等待、完整计时修正、故障/恢复矩阵、双方同等GPT修复预算、证据回读。
再进行一次正式Reality，成功后按原合同交错AB/BA十组；冷启动与暖运行分开报告。采用持久运行只减少已测可复用启动成本，不改变每轮干净输入，不复用上一轮答案。部署/维护/失败/人工成本全部保留；全程净收益≤0则不引入Orca。
目前只完成路线收敛，VIRTUAL_MATURE、STOP_GATE、物理最优及FINAL_VALID均未通过。

## 执行边界与下一步
原GitHub运行时预检曾被平台安全检查屏蔽，只有通用拒绝文字，无具体原因。此次只读源码、现有文件与文档归档，不借C通道重发该请求，也没有把全部项目停住。
本轮未修改启动器、隔离配置或现役服务。当前尚缺：
- 官方设置落点及最小更新方式的完整核对；
- 原用户home下auth迁移/hooks零越界证明；
- 原任务进程/会话归属对账；
- 平台允许的执行/审批条件与具体冻结清单；
- 实际子进程与全链业务回执。
这些是部署执行条件，不要求用户重复提供截图。源代码发现的可行分离机制不自动解除平台拒绝。

## 来源
固定来源提交：2bb20586ebc39d605e16d95f57420e20a16e7485。当前main搜索仅用于发现文件名；其中三份较新文件在固定提交不存在，已弃用，未纳入证据。
- [docs/site/content/docs/ways-to-run.mdx](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/docs/site/content/docs/ways-to-run.mdx)；Git blob e35b63eae906e9e88033ec3b60797ea41d2492f0
- [docs/site/content/docs/agents/codex.mdx](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/docs/site/content/docs/agents/codex.mdx)；Git blob 5ecf8281d2c7f80cfc4faee732e6b9e5d39bdbd6
- [docs/site/content/docs/settings.mdx](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/docs/site/content/docs/settings.mdx)；Git blob 4fac0564d48c728e4391dc1212e009c5018b821c
- [docs/site/content/docs/remote-servers.mdx](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/docs/site/content/docs/remote-servers.mdx)；Git blob 25ad464f0028f1a854f16e15001c147f7440a255
- [docs/site/content/docs/cli/orchestration.mdx](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/docs/site/content/docs/cli/orchestration.mdx)；Git blob 88355cb8c825d11999fe3cade3017e49b5242495
- [src/main/orcad/orcad-app-paths.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/main/orcad/orcad-app-paths.ts)；Git blob 7b31404e9ddf01d3672de43850f8aa2a23ed4f7c
- [src/shared/structured-native-chat-launch-route.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/shared/structured-native-chat-launch-route.ts)；Git blob 284737c987c90bc33d1472e25096cf10978e2586
- [src/shared/global-settings-types.ts](https://github.com/stablyai/orca/blob/2bb20586ebc39d605e16d95f57420e20a16e7485/src/shared/global-settings-types.ts)；Git blob a456af45b833abc11144dc2ee9afb49b0ecb0d5d
