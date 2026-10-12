# 《三人行 V2》C002 完善、隔离实测与修复报告

已完善线上 V2 审查候选并完成实际原生 Codex 隔离测试。V2 三次有效试次的观测最短为 **1 分 15 秒 157 毫秒**，中位数为 **1 分 26 秒 191 毫秒**；三次累计完整计时窗口折算为 **0.421 个同类任务/分钟**。这不是绝对物理极限或持续容量认证。

V2 原来已经从 V1 生成，但状态为 REVIEW_PENDING_NOT_ACTIVE，尚未冻结激活。此次修订 C001→C002，不改变整数 VERSION=SANRENXING_V2。原 C001 三份文档按原字节归档且远端 Blob 一致；V1 冻结、SKILL/START_HERE 默认指针、旧任务 METHOD_REF、Polsia 与现役 Windows runner 不由本次变更迁移。

网上正式候选：[SANRENXING_V2.md](https://github.com/cuiqinggang/codex-private-skills/blob/main/skills/artificial-single-page-extreme-time-engine/SANRENXING_V2.md)。原候选归档：[C001](https://github.com/cuiqinggang/codex-private-skills/tree/main/skills/artificial-single-page-extreme-time-engine/method-drafts/sanrenxing-v2-c001-archive-20261012)。

**实测结果与口径**

同一个固定离线任务：28个方法/安全/计时决策场景，加12行合成事件的金额、重复、冲突、UNKNOWN核算。每次使用全新无历史的原生Codex子代理，单个计时执行者串行运行；不改变模型或推理档。输入与预先固定 oracle 相同，词表已去重排序，试次禁止读取oracle、validator或其他结果。

| 指标 | 冻结 V1 | V2 C002 |
|---|---:|---:|
| 正式试次数 | 3 | 3 |
| 有效 / 无效 | 3 / 0 | 3 / 0 |
| 有效率 | 100% | 100% |
| 最低有效耗时 | 1 分 21 秒 741 毫秒 | 1 分 15 秒 157 毫秒 |
| 中位数 | 2 分 10 秒 394 毫秒 | 1 分 26 秒 191 毫秒 |
| 最大值 / 本批P95（nearest rank） | 6 分 23 秒 508 毫秒 | 4 分 26 秒 628 毫秒 |
| 三个完整窗口累计 | 9 分 55 秒 642 毫秒 | 7 分 7 秒 976 毫秒 |
| 累计独立计时窗口折算速率 | 0.302 个/分钟 | 0.421 个/分钟 |

| 配对块 | V1 完整耗时 | V2 完整耗时 | 核验 |
|---|---|---|---|
| 1 | t101：6 分 23 秒 508 毫秒 | t102：4 分 26 秒 628 毫秒 | 两次均有效 |
| 2 | t104：2 分 10 秒 394 毫秒 | t103：1 分 26 秒 191 毫秒 | 两次均有效 |
| 3 | t105：1 分 21 秒 741 毫秒 | t106：1 分 15 秒 157 毫秒 | 两次均有效 |

预先固定顺序：V1→V2、V2→V1、V1→V2。三对本批样本均为V2较快，仍只作描述性结论。各版本只有3个样本，P95实际等于最大值，不能当作稳定尾延迟估计。未进行A/A等价校准，且模型/工具等待明显波动，因此没有“统计显著更快”“适用于所有任务”或“已达极限”的声明。没有删除慢样本、重分类为失败或事后扩大等价阈值。

真实六试次批次窗口：2026-10-12 22:45:26.760 UTC+08:00 → 2026-10-12 23:03:06.310 UTC+08:00；完整窗口 **17 分 39 秒 550 毫秒**，含试次间控制等待，混合批次有效吞吐为 **0.340 个/分钟**。表中的各版本速率来自该版本三个独立完整计时窗口之和，不是连续运行的容量上限。

计时由Windows QueryPerformanceCounter / Python perf_counter_ns完成（monotonic=True，adjustable=False）。起点在输入派发前，终点是独立oracle验收接受；含方法/输入加载、工具调度、模型、写入产物、根代理核验等待。UTC只用于定位，accepted_at不得后移起点。终态result.json回执写盘在验收标记之后；本合同DONE_WHEN是独立验收完成。

本次线上定位、下载、方案修订、审核和最后证据发布是整个改善项目的一次性工作，不重复加入每个已锁源试次；所以这些样本不冒充本轮用户原始请求的整个完成时间。冻结模型依赖于已核验的线上提交及C盘隔离快照，而非每个试次重新联网读latest。

**修复与完善**

| 项 | 原问题 / 缺口 | C002 行为与证据 |
|---|---|---|
| 1 | 精确定位标签仍是强制启动门，与用户PAUSED_BY_USER冲突 | 缺标签不阻断、不猜造；现行用户策略优先；R06实际模型决策通过 |
| 2 | 历史维护摊销与当前墙钟混算 | full_wall单调起止差；历史摊销另列；R27与计时脚本复核 |
| 3 | accepted_at可后移、截去接单/排队时间 | 从received派发前起计；accepted只作分段；不受UTC回拨影响 |
| 4 | 速率与“最短值”没有明确范围 | 有效数/完整窗口，失败样本保留；观测min、中位数、P95、有效率与批次分别报告 |
| 5 | 动态latest和固定节点快照可能混读/自动迁移 | 既有METHOD_REF/NODE_RUNTIME_SNAPSHOT优先；先锁commit，再按ref读；运行层变更须原授权和安全边界 |
| 6 | “接单只判一次”可能误解为永不重判 | 目标、权限、副作用、依赖/资源实质变化才重判受影响分支，GOOD保留；R26通过 |

另外修复两项测试缺陷：旧allowed_actions顺序泄漏答案；R16把“未验收”写成NOT_DONE，可能诱发误重做。原t001/t002保留为PILOT_LEAKED_VOCAB，**不计入正式功能/速度结论**。正式PROFILE002使用25个去重、独立排序词汇，R16=NOT_ACCEPTED_REVIEW。独立审核确认整数分与全部ID集合的oracle正确。

**验证范围**

36/36旧能力有独立静态设计覆盖；这不等于36个平台动作实际通过。六个正式试次均通过28个离线模型决策与12行合成事件核算（共168个决策、72行输入），输出、方法、输入、oracle和validator SHA无漂移，顺序时钟一致。oracle自检拒绝8种坏结果：漏例、重复ID、错误总金额、浮点总额、UNKNOWN入账、重复入账、擅自恢复ROI、后移计时起点。

纯本地JSON读取加oracle校验101次：最低0.203毫秒、中位数0.214毫秒、P95 0.401毫秒，局部折算4050.9次/秒。该数字只说明本地校验速度，**不能作为Codex/GPT、整套方法或持续业务吞吐**。

已测试：本地文件产出→独立oracle核验、原生Codex子代理离线执行、源文档/修订稿/原候选归档官方GitHub回读。
未测试：GPT官网CEO跨页→Windows计划任务→Codex自动接续、浏览器标签实际归属关闭、n8n业务管理、真实发送/资金/生产、断电冷启、72小时长稳。这些不是本次隔离样本的完成要求，状态为NOT_TESTED，不借模拟决策补认证。T_PHYSICAL_LIMIT与稳定持续容量仍为UNKNOWN；全局V2激活未执行。

**复现与证据**

原始结果和SHA在 SUMMARY.json；全部40个明确路径的输入、oracle、脚本、试次原文、原始失败及持久化回执在 EVIDENCE_BUNDLE.json；独立审查在 tests/independent_review.md；原缺陷在 tests/PILOT_REPAIR.md。实际原生代理生成步骤不可由本地oracle脚本替代。

```powershell
& 'C:\Program Files\PowerShell\7\pwsh.exe' -NoLogo -NoProfile -Command "python -B 'C:\AI\Polsia-Codex-20261011\outputs\sanrenxing-v2-20261012\tests\validate_trial_v2.py' selftest"
```

正式试次不可覆盖。新复验必须创建新token，并先start，再执行同合同原生代理，最后finish；不得盲重发外部副作用或重播旧业务。

CodeGraph usage:
- MCP available: YES，已发现codegraph_explore。
- CLI available: YES，codegraph.ps1。
- .codegraph index present: NO，本项目检查False，线上仓库根目录也未提供索引。
- status checked before work: YES，代码改动前检查本地索引及MCP可用性；CLI随后只读确认。
- callers/callees/impact checked where relevant: 不适用；仅新增隔离业务oracle/计时脚本，未改生产代码、现役runner或调用链。
- sync/refresh run after meaningful code changes: NO，无可刷新索引。
- if not used, reason: 无.codegraph；采用定向读取和原生工具，未做仓库架构重构。

Knowledge Brain usage:
- INDEX checked: YES。
- ROUTING_MAP checked: YES。
- Relevant indexes checked: skills-index；补查projects-index与reports-index，未登记本方案。
- CodeGraph used where relevant: 不适用（无索引）。
- OpenHuman reference used where relevant: 不适用（非记忆架构任务）。
- Sync run before/after: 不运行全库同步；收尾kb_health_check.ps1只读执行，FINAL_RESULT=PASS。未改KB hot entries，不运行hot/deep sync。
- If not used, reason: 已使用定向预检；实际方法源由共同GitHub工作区实时确认。

未访问H/K、未计算ROI；标签与ROI暂停保持有效。所有候选及证据只使用C盘隔离目录和用户指定共同工作区。
