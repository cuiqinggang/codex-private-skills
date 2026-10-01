# 成熟方案竞争 R3｜GPT CORE + 可替换执行层｜极限短时间自动化闭环 v2.0

```ini
ROUND=R3
DATE=2026-10-01
STATE=10

CORE_BRAIN=GPT
CORE_BRAIN_FIXED=YES
EXISTING_PAID_CAPACITY_ALLOWED=YES
NEW_INCREMENTAL_PAID_DEPENDENCY=FORBIDDEN_BY_DEFAULT

CODEX=PRIMARY_EXECUTOR_CANDIDATE
CODEX_FIXED=NO

MANUS_2=BENCHMARK_ONLY
BACKUP_PATH=REQUIRED
PRIMARY_WINNER=NOT_YET_CERTIFIED
```

## 1. R3 修正

R2 的 FREE-FIRST 过度收紧，错误地把用户已经付费拥有的 GPT / Codex 能力当成需要排除的收费依赖。

R3 正式修正为：

```text
已经拥有的强能力 → 充分使用
新增长期付费依赖 → 默认不加
```

## 2. 当前核心结构

### 固定核心
**GPT = 超级大脑**

负责：
- 目标理解；
- Reality Contract；
- 世界成熟方案检索；
- 决策与组合；
- 故障归因；
- 重新选路；
- FINAL_VALID 判断；
- 整体 T_VALID 收敛。

### 执行层
**Codex = 当前第一执行候选，但不是固定核心。**

它必须与其他成熟执行方式在 Reality 中比较。

Codex 如果：
- T_VALID 最短；
- 可靠；
- 人工介入少；
- 与 GPT 交接成本低；

则保留。

否则可被成熟替代路径部分或全部替换。

## 3. 主链候选

### P1｜GPT + Codex
当前最值得先跑 Reality 的路径。

原因：
- GPT 提供核心最高智能；
- Codex 已是成熟工程执行器；
- 用户已经拥有两者；
- 当前项目已有大量 GPT↔Codex 现实经验与资产；
- 真正问题集中在“自动交接 / 自动恢复 / 自动验收”，不是缺一个新 Agent。

### P2｜GPT + 最小成熟执行能力组合
若 Codex 在某类任务不是最佳：
- Browser：JEV-native / Playwright / 其他成熟 Browser；
- deterministic automation：n8n；
- GitHub / APIs / MCP / CLI；
- OpenClaw 可作为已有成熟 Agent / automation 壳层候选；
- 其他未来成熟执行器。

原则：按任务只启用最小有效组合。

## 4. Manus 2.0

```ini
PRODUCTION=NO
BENCHMARK=YES
USE_EXISTING_CREDITS_ONLY=YES
```

输出：
`T_REF_MANUS`

它只用于回答：
> 一个成熟完整商业产品对同一 Reality 可以做到多快？

不进入未来正式主链。

## 5. Backup｜独立备份路径

正式方案最终还必须有 Backup。

要求：
- 不要求 GPT 与 Codex 同时正常；
- 可以在主链服务异常时恢复最低可用工作能力；
- 只由成熟现成能力组成；
- 平时不与主链并行消耗资源；
- 只在故障或灾备 Reality 中启用。

候选可从：
- OpenClaw；
- 其他成熟模型 / Agent；
- 现有本地模型与免费模型池；
- n8n CE；
- JEV-native；
- 其他成熟平台
中竞争。

当前不提前选定。

## 6. 现在真正应该测什么

不是继续做功能列表，而是三个 Reality：

```text
A. GPT + Codex 主链
   → T_VALID_PRIMARY

B. Manus 2.0 Benchmark
   → T_REF_MANUS

C. 独立成熟 Backup
   → T_VALID_BACKUP
```

当前顺序先 A+B。

原因：
A 是真正未来主链候选；
B 提供成熟参考极限；
C 等 A 的结构明确后再选，避免提前为备份搭系统。

## 7. 下一步

```text
① 固定同一个真实任务 Reality
② 跑 GPT + Codex
③ 跑 Manus 2.0 对照
④ 比较完整 T_VALID 和人工胶水
⑤ 定位 GPT+Codex 最大损失点
⑥ 只引入成熟能力攻击这个损失点
⑦ 重跑 GPT 主链
⑧ 主链稳定后，再选择并验证 Backup
```

不新增架构；不因为 Codex 是当前默认执行器就保护它。
