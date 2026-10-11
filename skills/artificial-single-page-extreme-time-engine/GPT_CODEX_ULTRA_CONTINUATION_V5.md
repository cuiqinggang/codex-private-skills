# GPT CEO＋Codex Ultra｜动态并行、双层监控、故障诊断与恢复｜V5

METHOD_VERSION=V5
PREVIOUS_METHOD_VERSION=V4
VERSION_POLICY=INTEGER_ONLY
STATUS=METHOD_AND_SKILL_DOCUMENTATION_RELEASE
ENGINE=28_UNCHANGED
WINDOWS_BUSINESS_RUNTIME=3.1.0_UNCHANGED
ACTIVE_TASK=POLSIA_CAPABILITY_REPLICATION_20261011
LAST_CONFIRMED_BUSINESS_FREEZE=V008
FREEZE_ID=POLSIA-MOTHER-V008-F001
MOTHER_FINAL_VALID=NO
N8N_INDEPENDENT_SKILL_VERSION=1.0.2_UNCHANGED
SOURCE_REPOSITORY=cuiqinggang/codex-private-skills
EVIDENCE_CUTOFF=2026-10-12_BEIJING_TIME_PREVIOUSLY_VERIFIED
LIVE_REALITY_THIS_RELEASE=NOT_RECHECKED_REMOTE_DEVICE_USAGE_LIMIT

## 一、V5 定位及继承

V5 是对已完成监控部署、轻量化、故障声音、并发容量试验的**方法／技能包整数升级**，不是重新执行 V001–V008，更不是 Polsia 母任务最终通过。继承 V4 的 CEO 唯一授权入口、十个逻辑方向、动态并行、单写者更新、Exactly-once、异常记录、双门启动和历史故障修复规则。旧 V4 方法及五个旧脚本继续保留，便于差分回退；不得重新套用 V4 旧 dashboard 或安装程序覆盖已选择的轻量监控入口。

本机现役业务脚本：`C:\AI\Polsia-Codex-20261011\CONTINUE_EXISTING_CODEX.ps1`，版本 v3.1.0；原母任务计划任务 `Polsia-Codex-Mother-Continue` 不变。方法升级绝不隐式批准 CODEX-009。原引擎第28版、历史 Freeze、代理 FlClash、现有登录浏览器及 n8n 独立技能包均不修改。

## 二、成熟组件优先的执行与并发

1. 先从 GitHub 统一索引→方法文件→当前任务 CURRENT/VERSION_CURRENT→最后不可变 Freeze→CEO 授权合同读取权威事实，再以 Windows 实际文件、SHA、进程和回执核对；结果冲突按 UNKNOWN，不凭口述、单个日志或窗口颜色判定。
2. 十个方向是研发、营销、客服、销售、财务、多智能体工作流、监控、恢复、持续学习、跨系统集成的**逻辑队列**，不是同时启动十个重型 Codex。每条分支需要合法任务合同、唯一 TASK_ID、工作目录、幂等键／副作用判断、时限、真实回执、独立复核、Freeze。
3. 拆分→根据依赖动态安排可以并行的分支→局部集成→再拆分。某一 BLOCKED 分支只暂停相应依赖，不得让无关分支全部空转。READY 表示候选，非已授权或已启动。
4. Windows PS7 原生 `ForEach-Object -Parallel`／运行空间复用是已实测成熟执行基线。本地计算、短文件任务**初始 2 并行**，有实证净收益再试 4；等待型初始 4，有净收益再试 8。大量独立 PowerShell 进程短任务启动开销已实测不划算。
5. 容量证据：i5-3570／4核4逻辑／32GB；36轮、432任务回执、134144次 SHA256，全测试通过；轻任务运行空间 1路 0.700s、2路 0.461s、4路 0.434s；模拟350ms等待 1路 4.754s、4路 1.547s、8路 0.951s；重哈希 2路均值 2.209s、4路 2.444s、8路 2.147s，**不足以认定8路全面最优**。依据 `tasks/POLSIA_CAPABILITY_REPLICATION_20261011/benchmarks/POLSIA_PARALLEL_CAPACITY_20261012.md`。
6. **Codex 模型级 1/2/3 Agent 尚未公平实测**。不得把原生运行空间效率推断为真实 Agent 并行收益。扩容／缩容仅比较相同合同、相同验收标准的有效交付总时间，计入派发、模型等待、审核、失败恢复、整合和监控资源；没有净收益就回退。

## 三、日常默认采用纯中文轻量故障监控

- 监控不是派发器。原生计划任务 `Polsia-Unified-Monitor-V4` 每分钟调用 `C:\AI\Polsia-Unified-V4\collect.ps1`；使用 `config.json`、`snapshot.json`、`incidents.jsonl`、`branches\*\status.json`。原状态机和业务保存点不受显示方式影响。
- 唯一**默认日常显示**：`C:\AI\Polsia-Unified-V4\dashboard-lite.ps1`。桌面 `Polsia Codex - Live Status` 快捷方式、登录自动启动，指向此轻量命令行监控，约每60秒刷新。仅显示母任务中文状态、保存点是否登记、执行中／待派发／阻塞数、采样时效与最多三条异常。
- 面向用户的窗口／测试文字／语音一律中文；只在文件路径、内部技术字段和代码中允许原有英文。正常 `WAITING_CEO` 无需报警，业务 `BLOCKED` 如 n8n 权限问题要清晰展示但不得假装新故障。
- 采样时间戳超过150秒或文件不可读视为监控异常。新故障首次出现或故障集合变化才报警：独特两段提示音＋ Windows 现成“微软慧慧”中文语音；稳定相同故障不在每次刷新时重播。用户扬声器实际听感**尚无独立听觉确认**，API 调用成功不能替代现场听到。
- 已验证限界：正常视图纯中文、隔离注入异常的中文显示与语音引擎执行、解除故障、历史保留；最新一次复核旧窗口替换后，轻量监控单个实际窗口进程存在，约100.6MB工作集，Grafana进程0，母任务仍 V008/WAITING_CEO。此前轻量工作集观察约92.7–111.7MB，仅为不同时点采样。
- 底层采集和历史记录须在**聊天关闭、监控窗口关闭时仍运行**；但若用户注销，声音／窗口不保证可见，长期无登录、断电、采集任务自身失效须另行验收。

## 四、完整版 Grafana 保留为未来多节点选项，不默认常驻

- 成熟产品：Grafana OSS 13.2.3＋Infinity 数据源插件 4.1.1；9面板、10方向、左右分组、中文字段映射、最近事件与60秒读取接口的限定范围测试通过。
- 已停止完整版 Grafana 服务并取消登录自动启动。完整版软件位于 `C:\AI\Polsia-Observability-Grafana\grafana-13.2.3\`，**22项**部署、诊断、历史证据、快捷方式、备份已搬到 `C:\AI\Polsia-Observability-Grafana\历史方案-完整监控-20261012\`，并记录文件校验与恢复说明。日常 `C:\AI\Polsia-Unified-V4\` 只放运行所需轻量文件、业务监测数据与既有试点；保留旧脚本 `dashboard.ps1` 作历史基线，但不作为默认入口。
- 完整版曾在不同时点占用工作集约501.5MB、停止前351.5MB；轻量监控约100MB。以上是独立观测，**不构成精确节约多少内存、能多运行一个 Agent 的证明**。移动文件仅减少工作目录杂乱和恢复路径冲突，不等于释放磁盘容量；停止重型服务才会释放运行资源。
- 以后若监控对象从十个逻辑方向扩张到实际多阶段、多节点、跨系统追踪，先评估业务净收益与资源开销，获准后复用既有完整 Grafana，不自研替代监控框架。重新接通已停用的 Grafana JSON 发布适配、检查插件／健康接口／数据源／新Freeze动态映射，重新做真实端到端验收；仅开启 Grafana 不代表自动获得新业务数据。

## 五、诊断、保存点及事故恢复

故障处理沿用**GOOD基线→BAD可复现→第一处差分→成熟现成修复→最小变更→重新验证→独立审核→保存点／Freeze**。只对隔离、已授权、结果可核对、不会造成重复副作用的情况自动恢复。生产结果 UNKNOWN 先对账，禁止自动重发；DONE 不重做。监控 `ALERT` 与业务 `BLOCKED`、`WAITING_CEO` 必须分开；`DETECTED`／`CLEARED` 历史不能删除。

**双门仍为硬条件**：CEO 在正式仓库中批准明确业务范围，且 Windows 的真实 NEXT 合同和页面精确定位标签通过后，才能启动下一 Codex 执行器。母任务 CURRENT/VERSION_CURRENT 只有受控单写者合并；任何新的 V009 必须先核对新Freeze/SHA，并升级采集器的 V008 特定校验逻辑，否则不得声称监控已覆盖 V009。

已知修正规则、详细现物路径、测试回执、局限及未来复验清单，见 `skills/gpt-ceo-codex-ultra-continuation/v5/KNOWN_ISSUES_AND_ACCEPTANCE.md` 与 `v5/README.md`。临时故障注入只允许在干净无真实报警的隔离场景，发生错误必须 finally 清除测试标志并恢复快照。

## 六、不可扩大解释的验收边界

已实测限界：原生并行容量比较；两项隔离试点（V008 128份清单SHA校验、Git原生隔离修复）；每分钟采样；轻量纯中文状态；一次受控故障→特殊提示音／中文语音引擎成功返回→清除→保留发现和恢复事件；Windows 窗口有效启动；完整版归档。

尚未认证：九类公司能力完整业务闭环、CODEX-009正式审批、真实Codex Agent最优数量、首次GPT主动远程报警处理、生产未知故障自动修复、用户现场听觉确认、V009监控动态适配、72小时／冷启动／断电恢复、完整T_VALID／最终Reality／优化10轮。n8n 健康200而管理接口401的旧阻塞仍是需合法授权的工作流问题。

**安全边界**：禁止未经授权真实付款、退款、营销投放、客户发送、公网发布、生产改动、凭据读取；不改FlClash／网络代理、不增开或关闭现有登录浏览器，不改原Codex v3.1.0业务运行器、原计划任务、引擎28或历史不可变冻结。