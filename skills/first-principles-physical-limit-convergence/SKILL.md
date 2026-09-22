---
name: first-principles-physical-limit-convergence
description: 第一性原理极限短时间引擎 v4.1.0。“一虚一实”成熟协议：当前方法只有虚拟成熟与实际验证两步；正式标签第四字段只写“虚”或“实”。唯一锚定物始终是 T*=min(T_VALID)，即极限短时间/极限效率。虚拟成熟动态读取版本化 Reality Foundation、重新检索成熟方案并完成组合/淘汰/攻击/验证/冻结；实际验证只执行冻结合同并回传 Reality Delta。每个任务结束必须执行 Foundation 吸收检查。自动化一步化明确延后，待两步真实案例成熟后再适配既有 gpt-codex-convergence-orchestrator。
metadata:
  version: "4.1.0"
  short-description: 一虚一实成熟协议·虚/实标签·任务后资产吸收·自动化延后
  lineage: first-principles-physical-limit-convergence@4.1.0 <- @4.0.0 <- @3.1.9 <- @3.x <- @2.x <- @1.x
---

# 第一性原理极限短时间引擎 v4.1.0

## 0. 唯一锚定物

所有设计、搜索、Twin、验证器、JEV、缓存、GPU、自动化、部署，都只允许服务一个目标：

```text
VALID = 正确性/质量/安全/权限/成本/资源等硬门全部通过
T_VALID = 从任务开始到第一个现实 VALID 结果出现的端到端时间
T* = min(T_VALID)
```

“极限效率”只是“极限短时间”的物理解释，不形成第二指标。

任何动作若既不帮助 VALID，也不能降低 T_VALID，则默认删除。

---

# 1. 当前方法：一虚一实

逻辑上只有两步：

```text
虚 -> 实
↑    |
|____|
Reality Delta
```

## 虚 = 虚拟成熟

职责：**现实之前把方案做成熟，并冻结唯一值得现实执行的方案。**

输入：
- 版本化本地 Reality Foundation；
- 动态成熟方案池；
- 历史 Reality / failure evidence；
- 当前任务 VALID 合同。

内部可以使用：
- Reality Anchor；
- Exact Reality Twin；
- 广域成熟方案检索；
- Virtual-99；
- verifier 攻击；
- JEV 概率判断；
- GPT/DeepSeek 高智能推理；
- 确定性代码。

它们都只是“虚”内部能力，不得重新升级成第三步。

“虚”的标准动作：

```text
READ_REALITY
-> DISCOVER_MATURE
-> COPY/ADAPT/COMPOSE
-> DELETE
-> ATTACK
-> VERIFY
-> TIME_COMPARE
-> FREEZE S*
```

冻结输出至少包含：

```text
SOLUTION_FROZEN=YES
FROZEN_SOLUTION=S*
PREDICTED_T_VALID=T*
VALID_CONTRACT=<hard gates>
VERIFIER_CONTRACT=<deterministic verifier>
EXECUTION_CONTRACT=<deterministic real execution>
EXPECTED_REALITY=<minimum sufficient reality assumptions>
```

## 实 = 实际验证

职责：**实打实执行冻结 S*，证明现实 VALID 和现实 T_VALID。**

Codex / Reasonix / 本地执行器只允许：
- 读取冻结合同；
- 执行；
- 测时；
- verifier；
- 采集最小充分 Reality Delta；
- 回传；
- STOP。

禁止：
- 自己修；
- 自己重新设计；
- 自己搜索替代路线；
- 自己更换模型/阈值/路由/fallback；
- 失败后“再试一个办法”。

结果：

```text
PASS
-> VALID=PASS
-> T_VALID_REAL=<value>
-> REALITY_DELTA=NONE
-> 当前现实证据完成

FAIL
-> REALITY_DELTA=<minimum sufficient delta>
-> STOP
-> RETURN_TO=虚
```

失败不是第三阶段，只是：

```text
实 -> 虚
```

---

# 2. 正式标签：只写“虚 / 实”

正式执行命令保持四字段定位：

```text
【<实际页面名>｜<具体任务名>｜<序号>｜<属性>】
```

第四字段只允许：

```text
虚
实
```

含义：

```text
虚 = 虚拟成熟
实 = 实际验证
```

不用再写“虚拟成熟 / 实际验证”，因为第四字段只承担任务属性定位。

以下在 v4.1 当前正式命令中全部禁止：

```text
极限短时间
成熟方案集群
高智能虚拟成熟
虚拟成熟
实际验证
CORE_*
STEP_*
修复
优化
验收
任何第三属性
```

“极限短时间”不是属性字段，它是所有动作共同的唯一锚定物。

---

# 3. 动态成熟方案池

成熟方案池不是一次建立永久不变。

每个新任务或重大 Reality Delta，虚拟成熟都允许重新发现现实世界更成熟/更短的方案。

默认：

```text
WORLD_SOLVED=YES
OLD_WINNER_IS_CANDIDATE_NOT_AUTHORITY
```

重新搜索必须有目的：
- 可能缩短 T_VALID；
- 当前成熟池缺关键能力；
- 已知现实发生变化；
- 新成熟实现可能替代旧实现。

禁止为了“搜索完整”而无限搜索。

---

# 4. 本地 Reality Foundation：版本化永久资产

入口：

```text
local-ai-reality-foundation
```

它不是第三步，而是“虚”的长期现实输入。

## 每个任务结束都必须做吸收检查

```text
FOUNDATION_ABSORB_CHECK=REQUIRED
```

只问：

> 本任务产生的新现实事实、时间数据、失败原因、环境边界或成熟资产，未来是否能减少达到 min(T_VALID) 的时间，或避免重复现实采集/重复踩坑？

如果 NO：

```text
FOUNDATION_ABSORB=NO
FOUNDATION_VERSION_UNCHANGED=YES
```

如果 YES：

```text
FOUNDATION_ABSORB=YES
-> 只吸收最低必要信息
-> 形成新版本
-> 保存完整当前快照
-> 写明本版新增/修正
-> 保留来源证据
-> 旧版本不覆盖
```

## Foundation 版本规则

```text
PATCH：现实数据/时间/状态增量，不改变结构
MINOR：新增现实域、新资产类别、新吸收能力
MAJOR：Foundation 合同/结构发生不兼容改变
```

每个版本必须自包含：
- 当前完整有效资产；
- 当前 Reality Fingerprints；
- 当前关键现实时间基线；
- 当前不可改变约束；
- 本版 delta；
- evidence pointer；
- previous_version。

目标不是信息最多，而是：

```text
MINIMUM_SUFFICIENT_REALITY_FOR_MIN_T_VALID
```

---

# 5. v4.x 成熟顺序

当前明确不直接跳“一键自动化”。

先把两步做成熟：

```text
阶段 A：一虚一实逻辑正确
阶段 B：多个真实案例跑顺
阶段 C：Reality Delta 回虚修复稳定
阶段 D：Foundation 任务后吸收稳定
阶段 E：JEV 等加速器证明能进一步缩短 T_VALID
阶段 F：两步本身达到现实极限短时间
```

只有这些成熟后，才进入未来“一步化”。

---

# 6. 未来一步化：复用现成自动化，不从零开发

已有候选承载层：

```text
gpt-codex-convergence-orchestrator@1.5.2
branch=codex/gpt-codex-convergence-orchestrator-v1.5.2-freeze-closeout
```

现有能力：
- GPT 决策 / Codex 确定性执行；
- GitHub 共同工作区优先；
- A/B/C 三条简单 transport 路径；
- 用户中间复制粘贴目标为 0；
- 受控 A/B/C toy 现实验证已有证据。

但它当前仍：
- 依赖旧 first-principles@3.1.2；
- 真实业务证明范围有限；
- 自然 A->B->C failover 尚待未来真实故障证据。

因此：

```text
V4_1_AUTOMATION_ATTACH=DEFERRED
REINVENT_AUTOMATION=NO
FUTURE_CARRIER=gpt-codex-convergence-orchestrator
```

未来只有在“一虚一实”本身成熟后，才允许把 Orchestrator 升级为 v4.x 合同承载层，并讨论 first-principles 的下一大版本。

---

# 7. 历史与台阶

v4.0.0 保留为“一虚一实”的第一版架构台阶。
v3.1.9 及以前继续完整保留。

历史只作为：
- EVIDENCE
- MATURE_SOLUTION_SOURCE
- FAILURE_HISTORY
- REALITY_BASELINE

不得覆盖当前 v4.1 方法。

---

# 8. 一句话

> **v4.1：只有“虚”和“实”。虚负责把方案做到成熟且预测最短；实负责物理证明。每个任务结束后，只有能帮助未来更快达到 min(T_VALID) 的现实知识才进入版本化 Foundation；等这两步真实跑成熟，再把现成 GPT↔Codex Orchestrator 接上做未来一步化。**
