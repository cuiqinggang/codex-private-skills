---
name: hybrid-intelligence-probability-engine-v0-3-5
description: HIPE v0.3.5 常用场景生产入口；优先成熟路径，使用冻结 CODE / JEV / GPT residual 分工、合法并行和 fail-closed 验证。
version: 0.3.5
---

# HIPE v0.3.5

正式资产为本目录，历史 v0.3.4 保持原样。入口为 runtime/production.py。
本版本仅认证已覆盖的常用场景，不表示任意开放任务都能自动完成或验证。

原始任务 → Reality Solvability Gate v0.2 → 成熟解决路径 → Forward Compiler v0.2
→ CODE / JEV / GPT residual → 合法并行 → Verifier → 有效结果。

触发：HIPE、混合智能概率引擎、确定性阈值、有限 Choice、SQLite 开放查询生成、冻结混合 benchmark。
执行前读取 CURRENT_STATE.json，检查 runtime 继承文件 SHA256；禁止改动冻结依赖。
此次升级是版本化升级，未原地修改 R4、R5、Gate 或 Compiler。

## 入口判断

先查成熟直接解、成熟组合解、成熟探索/测量协议。三者均不存在，且规格完整、
证据检索完成、有来源引用、物理上允许时，才进入 FRONTIER_UNKNOWN。
first_seen 不构成未知证据。未完成检索返回 SOLUTION_SEARCH_REQUIRED。
认证目录匹配由真实任务内容判定；用户自报 DOMAIN_MATCH、benchmark 名称不能代替匹配。

Forward Compiler 优先级固定 CODE > JEV > GPT。
确定性精确整数阈值使用 CODE；状态明确、有限 Choice、冻结动作本体且可验证时使用 JEV；
开放生成、隐藏信息、需定时重试或域不匹配均回退 GPT residual。
DOMAIN_MATCH=YES 直接使用冻结快路径，不要求 GPT 重新理解全部任务。

## 支持范围与调用

- CODE：严格结构的整数 compare_threshold，operator 为 <=，返回 ALLOW/BLOCK。
- JEV：冻结 J01–J20 独立决策任务，原样匹配；J21–J24 依赖策略使用完整混合入口。
- GPT residual：冻结 G01–G08 的 SQLite 查询生成，使用原 deterministic verifier 验证。
- 混合：冻结 HIPE-E2E-V3-48，16 CODE + 24 JEV + 8 GPT，原 R4 三路合法并行。
- 未认证开放任务仍路由 GPT，但返回 GPT_RESIDUAL_REVIEW_REQUIRED。
  由 GPT 补齐语义、状态与验收合同；不把无可靠 verifier 的开放回答标成 VALID。
  这是安全交接，不能报告为该任务已完成，也不得强行转换为 JEV。
- 本运行器只生成决策及在内存 SQLite 中验 SQL，不执行发布、删除、凭据轮换等外部动作。
- 不提供无依据的通用自然语言自动拆解。调用方输入结构化原始任务；
  未匹配任务需提供经审核的 solvability 布尔事实和 evidence_refs，不能编造检索结论。

最小任务 JSON：
~~~json
{"task_family":"threshold","tasks":[{"id":"D01","operation":"compare_threshold","value":3,"limit":11,"operator":"<="}]}
~~~

在本目录运行：
~~~text
python -B runtime/production.py --task task.json --plan-only
python -B runtime/production.py --task task.json --out <新的运行目录>
python -B runtime/production.py --mixed-benchmark --out <新的运行目录>
~~~
JEV/GPT 需要调用方已授权并继承 OPENROUTER_API_KEY；不读 .env、不保存密钥。
本次发布遵从用户决定：远端调用 0；JEV/GPT/MIXED 仅复用历史真实证据。

## 结果、计时与失败入口

每次运行必须使用新目录。读取 status.json；成功必须同时有匹配的结果及通过的 R5 receipt。
candidate.json 单独存在不代表 VALID，状态/receipt 丢失或写入失败均不可提升成功。
T_VALID 包含入口判断、编译、执行/等待、验证、任务最终写入、回读和哈希。
R5 计时 receipt 与 status 是事后观察元数据，不计入任务 T_VALID，沿用已验 R5 合同。
异常只记录安全类别，不记录完整 provider 内容或凭据。无自动重试。
失败时 T_VALID=null；非零退出或无法落地状态亦视为 FAIL。RuntimeError 不产生错误 VALID。
远端失败、verifier 拒绝、结果缺失与待审任务均必须明确报告原因。

每次 status.json 就是生产使用记录，包含 task family、route、VALID/FAIL、T_VALID、
可取得的 usage/cost、external/runtime error、verifier。
不得把离线 fixture 运行的时长、结果当作真实远端实测。

## 验收与停止

COMMON-SCENARIO-ACCEPTANCE.json 固定 21 cases，A–G 各 3；历史大型证据只引用，不重跑。
CURRENT_STATE.json 保存真实证据来源、哈希、复核结果与认证范围。
30 轮性能统计不是发布门槛；PERFORMANCE_BASELINE=ACCUMULATE_FROM_REAL_USAGE。
发布后不主动升级、不启动监控、不继续优化。
只有重复出现且有实际影响的生产问题才返回 GPT 判断是否需要 v0.3.6。
偶发且明确 fail-closed 的外部异常不自动触发升级。完成即 STOP。

