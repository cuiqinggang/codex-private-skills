# V5 操作入口｜轻量日用＋完整监控归档＋动态并发

版本：V5（整数版本）；前一版本 V4 保留。此处为**已验证成果的复用指南**，不是再次执行或升级 Windows 服务的指令。

## 1. 最短恢复路径

权威仓库：`cuiqinggang/codex-private-skills` 的 `main`；固定索引：`skills/artificial-single-page-extreme-time-engine/GPT_CODEX_ULTRA_CONTINUATION_INDEX.md`；方法：`GPT_CODEX_ULTRA_CONTINUATION_V5.md`；正式入口：`skills/gpt-ceo-codex-ultra-continuation/SKILL.md`。

先确认业务任务 `POLSIA_CAPABILITY_REPLICATION_20261011` 的 `CURRENT.md`、`VERSION_CURRENT.md`、最新 Freeze 和本机现物。已知旧快照：业务 V008 / `POLSIA-MOTHER-V008-F001` / `WAITING_CEO` / `MOTHER_FINAL_VALID=NO`；新页面必须重新核对。方法 V5、引擎28、业务 Freeze V008、Windows业务运行器v3.1.0是**四套独立版本**，不自动同步加一。

日常 Windows 目录：`C:\AI\Polsia-Unified-V4\`。不要因文件夹叫 V4 就重新运行旧安装器；V5 方法升级并未重命名正在工作的目录。

| 用途 | 已有现物 |
|---|---|
| 后台每60秒原生采集 | Windows任务 `Polsia-Unified-Monitor-V4` → `collect.ps1` |
| 中文轻量窗口 | `dashboard-lite.ps1`；桌面 `Polsia Codex - Live Status`；登录自动启动 |
| 任务方向 | `config.json`，十个逻辑方向；不代表十个执行器 |
| 实时事实 | `snapshot.json`；每分支 `branches\<方向编号>\status.json` |
| 异常历史 | `incidents.jsonl`；新异常记发现，解除记恢复，不删除历史 |
| 旧脚本与试点 | `dashboard.ps1`、`pilot.ps1`、`pilot-results.json`；保留但禁止无故重播 DONE |
| 高级监控程序 | `C:\AI\Polsia-Observability-Grafana\grafana-13.2.3\` |
| 高级监控归档 | `C:\AI\Polsia-Observability-Grafana\历史方案-完整监控-20261012\` |
| 旧版原生源码 | 本技能 `v4/{collect.ps1,config.json,dashboard.ps1,pilot.ps1,install.ps1}` |
| V5轻量源码快照 | 本技能 `v5/dashboard-lite.ps1`；**新电脑部署前仍需现场验证** |

默认使用轻量窗口。此前现场已验证约100.6MB工作集；不将该数字当成持续基准或精确省下的资源。完整版曾观察到351.5MB（停前）和501.5MB（另一次采样），已停止进程、取消开机启动，程序和全部资料保留。归档迁移减轻目录混乱，**不自动减少磁盘占用**。

## 2. 监控状态及权限

显示规则（对用户文字纯中文，代码内部原状态仍保留）：运行、待派发、等待审批、受阻、已完成、出错、超时。只有 `alert_keys` 出现新故障或 `snapshot.json` 超过150秒不更新／无法读取才作为现场报警。原有 `WAITING_CEO` 是正常等待；`BLOCKED`（例：n8n管理接口未授权）要显示但不可擅自解除或自动开启未知权限。

报警：首次新异常或异常集合改变时，两段提示音并调用 Windows 内建中文语音；同一故障不因每60秒刷新重复播报。历史 `DETECTED` 和 `CLEARED` 持久留存；声音引擎成功退出≠用户实际听到，需现场确认扬声器。

**显示不授权执行**。CEO 先核验合法合同，Windows真实 NEXT 文件和四字段定位标签通过后，才允许启动新的 Codex。后端 `collect.ps1`、显示窗口、GitHub Freeze 互不接管权限；结果 UNKNOWN 必须先对账而不是重新提交。

## 3. 动态并发：具体条件而不是固定进程数

| 任务类型 | 起始并行 | 候选扩容 | 有效证据 |
|---|---:|---:|---|
| 本地短文件／计算 | 2 | 4 | 原生PS7运行空间线程，36轮隔离对照 |
| 等待型／受控 I/O | 4 | 8 | 模拟350毫秒等待试验，不能冒充真实网络吞吐 |
| Codex 模型 Agent | 1（仅作对照起点） | 2、3需公平试验 | **真实最优尚未验证** |

只扩大获批且彼此独立的分支。相同任务合同下对比“派发→实际执行→结果核验→集成→错误恢复→最终有效完成”的总耗时、资源、成功率；多路出现负收益则降回前一水平。不要反复对已经 DONE 的旧业务夹具做性能测试。V4 历史基线和完整统计位于 `tasks/POLSIA_CAPABILITY_REPLICATION_20261011/benchmarks/POLSIA_PARALLEL_CAPACITY_20261012.md`。

## 4. 什么时候使用完整监控平台

只有实际新增大量不同分支、可追溯工作流与跨系统事件，且全程追踪的**净收益足以覆盖额外资源**，才经CEO允许重新启用 Grafana OSS 13.2.3＋Infinity 4.1.1。先从本机归档读取：`归档清单.json`、`未来启用说明.md`、原仪表盘配置和独立故障验收报告。再复查最新授权、健康接口、数据源、中文页面、历史事件、系统资源、V009+冻结适配。

轻量切换时已经**取消 Grafana 数据发布步骤**，所以只启动完整软件不会自动更新仪表盘；必须经授权将实际数据源合法接回，运行一次隔离端到端验证。禁止无理由把历史完整版定时常驻、禁止再开发自有监控框架。

## 5. 既有测试可直接调用的证据

- `C:\AI\Polsia-Parallel-Benchmark-20261012\results.json`、`heavy.json`：PS7并行与进程开销实测，不能称 Codex Agent 竞速。
- `C:\AI\Polsia-Unified-V4\pilot-results.json`：独立试点，V008 128项哈希校验与隔离Git恢复。
- 归档 `grafana-real-acceptance.json`、`grafana-extended-acceptance.json`：9面板、10方向、真实Infinity查询、每分钟采集、注入报警与历史保留。
- 归档 `monitor-lite-alert-test.json`：轻量模式模拟故障→音效和中文播报引擎→清除→历史回读，工作集约111.7MB。
- 归档 `中文监控与归档验收记录.json`：中文显示及归档通过，但首次换窗尝试失败，**历史失败应保留**。
- 归档 `最终轻量中文模式复核.json`：后续纠正窗口启动参数、单个轻量窗口存活、完整版进程0、采集正常、业务V008不变，才构成最终这部分现场验收。
- `v5/KNOWN_ISSUES_AND_ACCEPTANCE.md`：故障症结、成熟修复路线、复验要求与未认证部分。

**验收边界：**以上均为先前实际核验记录；V5此次文档发布不等于再次对 Windows 作 Reality，也不代表用户扬声器听感、72小时连续运行、Codex 1/2/3并发或整个Polsia母任务最终PASS。