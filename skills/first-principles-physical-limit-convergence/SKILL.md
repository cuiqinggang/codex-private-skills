---
name: first-principles-physical-limit-convergence
description: 第一性原理极限短时间引擎 v4.0.0。当前方法从 v3.x 三核心/三关压缩为“一虚一实”：虚拟成熟负责读取底层现实资产、动态检索成熟方案、组合/淘汰/攻击/验证并冻结唯一最短方案；实际验证只执行冻结合同、测量现实 T_VALID、回传 Reality Delta。唯一锚定物始终是 T*=min(T_VALID)，即极限短时间/极限效率。v1-v3.1.9 全部历史保留但不再拥有当前方法权。
metadata:
  version: "4.0.0"
  short-description: 一虚一实·极限短时间唯一锚定·现实失败回虚拟成熟
  lineage: first-principles-physical-limit-convergence@4.0.0 <- @3.1.9 <- @3.1.8 <- @3.1.7 <- @3.1.6 <- @3.1.5 <- @3.1.4 <- @3.1.3 <- @3.1.2 <- @3.1.1 <- @3.1.0 <- @3.0.0 <- @2.0.0 <- @1.x
---

# 第一性原理极限短时间引擎 v4.0.0

## 0. 唯一锚定物

任何任务只有一个优化目标：

```text
VALID = 所有正确性/质量/安全/权限/成本/资源等硬门通过
T_VALID = 从任务开始到第一个 VALID 现实结果出现的端到端时间
T* = min(T_VALID)
```

“极限效率”是“极限短时间”的物理含义，不建立第二指标。

任何动作、技能、Twin、JEV、缓存、并行、成熟方案、验证器、部署器，如果不能：
1. 让 VALID 成立；或
2. 在 VALID 不下降的前提下降低 T_VALID；

则默认删除，不得因为“完整、先进、成熟、方便”而保留。

---

# 1. 当前方法：一虚一实

v4.0.0 当前方法只有两步。

## 第一步：虚拟成熟

机器别名：

```text
STEP=VIRTUAL_MATURITY
ZH=虚拟成熟
```

职责：**决定现实中唯一值得执行的冻结方案是什么。**

它一次性读取和组合：

```text
A. 底层永久资产
   - Exact Reality Twin / Reality Fingerprint
   - 浏览器/网络/宿主/运行时现实事实
   - GPU / 本地模型 / ComfyUI / 视觉环境
   - 已认证历史现实证据

B. 动态成熟方案池
   - 已有技能
   - 已验证成熟插件/脚本/运行时
   - 当前可获得的新成熟方案
   - 历史成功/失败案例

C. 高智能求解
   - COPY / ADAPT / COMPOSE
   - DELETE
   - CONFLICT_RESOLVE
   - ATTACK
   - SIMULATE
   - VERIFY
   - TIME_RANK
   - FREEZE
```

输出必须是唯一冻结合同：

```text
SOLUTION_FROZEN=YES
FROZEN_SOLUTION=S*
PREDICTED_T_VALID=T_VALID*
HARD_GATES=PASS
EXECUTION_CONTRACT=<确定性现实执行合同>
VERIFIER_CONTRACT=<确定性 VALID 合同>
EXPECTED_REALITY_FINGERPRINT=<现实环境预期>
```

### 虚拟成熟内部不是额外步骤

Reality Anchor、成熟方案搜索、JEV、Virtual-99、故障注入等全部降为内部能力。

它们可以被调用，但不得重新升级成与“虚拟成熟 / 实际验证”并列的方法步骤。

### 动态成熟方案池规则

```text
WORLD_SOLVED=DEFAULT_YES
```

每个新任务、环境变化、重大现实失败都允许重新检索成熟方案。
旧“最佳方案”只是候选和历史证据，不自动成为永久最佳。

成熟池的目的只有：

```text
找到能让最终 T_VALID 更短的现实可用部件
```

若成熟世界已有答案，禁止从零重造。

### 底层永久资产刷新规则

底层资产默认复用，不每次全量重建。

只在以下条件触发相关部分增量刷新：

```text
REALITY_FINGERPRINT_DRIFT=YES
关键事实缺失
硬件/驱动/Runtime/模型/浏览器/网络状态变化
Reality Certification 返回未建模 Reality Delta
用户明确要求重新锚定
```

刷新只更新变化域，不默认重新采集整台机器。

---

## 第二步：实际验证

机器别名：

```text
STEP=REAL_VERIFY
ZH=实际验证
```

职责：**证明冻结方案在物理现实中是否真的达到 VALID 和现实 T_VALID。**

执行器（Codex / Reasonix / 本地执行器）只允许：

```text
读取冻结合同
执行冻结合同
测量 T_VALID
运行冻结 verifier
采集事实
记录 Reality Delta
回传
停止
```

禁止：

```text
现场重新设计
现场搜索新路线
自行改变模型/阈值/参数/路由/fallback
自行修 verifier
自行做“再试一个办法”
把现实失败解释成继续探索的权限
```

现实验证结果只有两种：

### PASS

```text
VALID=PASS
T_VALID_REAL=<现实时间>
REALITY_DELTA=NONE
ACTION=FREEZE_OR_UPDATE_REAL_BEST
```

### FAIL

```text
VALID=FAIL 或 冻结合同与现实不符
REALITY_DELTA=<最小充分差异>
ACTION=STOP
RETURN_TO=VIRTUAL_MATURITY
```

固定闭环：

```text
虚拟成熟
-> 冻结 S*
-> 实际验证
-> PASS: 结束/刷新现实最优
-> FAIL: Reality Delta -> STOP -> 回虚拟成熟
```

现实端不存在“修复阶段”。

---

# 2. 一虚一实为什么是最小有效闭环

从第一性原理看，要得到“现实世界最短有效时间”至少需要两个不同逻辑：

1. **求解**：从现实约束和成熟方案中决定执行什么；
2. **物理证明**：至少一次现实执行，确认预测不是虚构。

把求解拆成“现实锚定 / 成熟方案池 / 虚拟成熟”三个外部步骤不是物理必需。
只要现实事实和成熟方案都已经成为虚拟成熟的输入资产，它们可以在一次求解中完成。

但“实际验证”不能被纯虚拟永久删除，因为：

```text
Virtual Reality != Physical Reality
```

所以 v4.0.0 的最简有效结构固定为：

```text
1 Virtual + 1 Real
一虚一实
```

---

# 3. 当前任务定位门禁

正式执行命令仍保留四字段结构，兼容既有定位习惯：

```text
【<实际页面名>｜<具体任务名>｜<序号>｜<阶段>】
```

第四字段从 v3.x 的“三核心”改为 v4.0.0 的两阶段，且只允许：

```text
虚拟成熟
实际验证
```

禁止使用：

```text
极限短时间
成熟方案集群
高智能虚拟成熟
CORE_1 / CORE_2 / CORE_3
STEP 1 / STEP 2 / STEP 3
修复 / 补丁 / 优化 / 验收
任何自造第三阶段
```

说明：
- “极限短时间”不再作为一个步骤名，因为它已经提升为所有步骤共同的唯一锚定物；
- “成熟方案集群”和“高智能虚拟成熟”合并进入“虚拟成熟”；
- “现实验证”正式成为第二步“实际验证”。

页面名规则不变：用户给出则原样使用；系统可读则使用真实标题；否则不猜。

---

# 4. 执行器权限边界

## GPT / 高智能侧

拥有：
- 动态成熟方案搜索；
- Reality Twin / 永久资产解释；
- 组合、删除、攻击、修复、再冻结；
- verifier 设计；
- 冻结合同设计。

## Codex / Reasonix / 本地执行器

拥有：
- 冻结合同确定性执行；
- 现实计时；
- 现实验证；
- 文件/部署/测试等被冻结的确定性动作；
- Reality Delta 采集。

没有：
- 自主方案设计；
- 自主修复；
- 自主换路线；
- 自主继续攻击；
- 自主改变冻结合同。

---

# 5. 底层永久资产

v4.0.0 的默认现实底座入口：

```text
local-ai-reality-foundation
```

它是资产索引，不是第三步。

权威资产至少包括：

```text
reality-execution-environment-anchor@1.3.0
exact-reality-digital-twin@1.3.0
Browser Reality R3 / Reality Fingerprint
Playwright 专用浏览器现实能力
本地 GPU / Bonsai2 256K 现实数据
ComfyUI / 视觉生成现实能力
OpenHands Canvas 等本地自动化入口
网络代理不变约束
```

资产必须逐次追加证据和版本，不覆盖历史快照。

---

# 6. JEV 的地位

JEV 不是第三步，也不是必经流程。

只在虚拟成熟中证明：

```text
T_JEV + 状态构造 + 适配 + 验证
<
替代路线的 T_VALID
```

且 HARD_GATES 不下降时，才进入冻结 S*。

否则删除。

---

# 7. 历史版本地位

v1.x 到 v3.1.9 全部保留。

历史只允许：

```text
EVIDENCE
MATURE_SOLUTION_SOURCE
FAILURE_HISTORY
REALITY_BASELINE
```

历史不再拥有 v4 当前方法权。

权威历史索引：

```text
HISTORY-v1-v3.1.9.md
```

旧分支保持不变，尤其：

```text
codex/first-principles-physical-limit-convergence-v3.1.9
```

---

# 8. 完成即交接

虚拟成熟一旦输出：

```text
VIRTUAL_MATURITY=PASS
SOLUTION_FROZEN=YES
```

且下一个动作是现实执行，则同一回复直接给最短实际验证命令。

目标：

```text
HANDOFF_EXTRA_USER_TURN=0
ONE_EXECUTION_SOURCE_OF_TRUTH=YES
```

---

# 9. 最终一句话

> **一虚一实：虚拟成熟负责把 Reality Twin + 动态成熟方案池一次求解成唯一最短冻结方案；实际验证只负责在物理世界证明它。失败从“实”返回“虚”，永远围绕同一个锚定物：T*=min(T_VALID)。**
