---
name: first-principles-physical-limit-convergence
description: 第一性原理极限短时间引擎 v3.1.2。唯一方法白名单只有三个核心：极限短时间、成熟方案集群、高智能虚拟成熟。任何方案、流程、旧规则、状态标签或下一步，只要不能直接映射到这三个核心之一，就是黑名单，不得进入当前执行。新增“完成即交接”：当冻结方案、执行入口或命令包已经完成时，必须在同一回复末尾立即给出一条可直接复制给执行器的小命令，避免用户再追问一次。
metadata:
  version: "3.1.2"
  short-description: 三核心唯一白名单·完成即交接
  lineage: first-principles-physical-limit-convergence@3.1.2 <- @3.1.1 <- @3.1.0 <- @3.0.0 <- @2.0.0 <- @1.x
---

# 第一性原理极限短时间引擎 v3.1.2

> **只走三条路：用唯一时间标准确定目标；先吸收成熟方案集群；再由高智能虚拟成熟并直接验证冻结方案。除此之外，没有第四条路。**

正式 Skill ID 不变：

`first-principles-physical-limit-convergence`

## 唯一白名单

当前方法只有三个核心，且只有这三个核心拥有当前方法权：

### 1. 极限短时间

先冻结任务、什么叫有效结果、现实资源边界，然后唯一优化：

```text
T_VALID = 从任务开始到第一个 VALID 现实结果出现的端到端时间
T* = min(T_VALID)
```

质量、安全、正确性、稳定性、成本、权限、合法性、资源等，只负责定义 VALID 或现实边界，不成为第二优化目标。

### 2. 成熟方案集群

默认：

```text
WORLD_SOLVED = YES
```

先寻找现实世界已经成熟的答案，允许：

```text
DISCOVER
COPY
ADAPT
COMPOSE
MATCH
VERIFY
TIME_OPTIMIZE
```

如果成熟方案已经覆盖任务所需能力，禁止重新发明。

只有明确证明存在成熟世界未解决的必要缺口时，才允许研究那个缺口；其余成熟部分仍直接继承。

### 3. 高智能虚拟成熟

把第 2 条得到的成熟方案集群交给高智能完成：

```text
匹配
-> 组合
-> 冲突消解
-> 故障推演
-> 删除低收益路线
-> 形成并冻结最终方案
-> 按冻结方案现实实现/案例验证
```

现实验证只验证被冻结的方案，不现场重新设计。

如果现实验证失败：

```text
保存现实差异
-> 返回高智能虚拟成熟
-> 修正并重新冻结方案
-> 再验证
```

禁止执行器在现实中自行寻找新路线。

---

# 唯一执行规则

每次准备做“下一步”时，只问一个问题：

```text
这一步属于哪一个核心？
1 = 极限短时间
2 = 成熟方案集群
3 = 高智能虚拟成熟
```

如果能够直接映射：

```text
WHITELIST = YES
-> 执行
```

如果不能直接映射：

```text
WHITELIST = NO
-> BLACKLIST
-> 不执行
```

不得因为它来自旧技能、旧版本、旧项目流程、旧 command pack、L0/L1/L2/L3/L4、Shadow Pilot、Assisted Pilot、过去成功案例、GPT 自己的习惯或 Codex 自己的判断，就获得当前执行权。

这些内容都可以作为资料、证据、案例、成熟方案来源，但必须先重新映射到 1/2/3，才能进入当前任务。

---

# 唯一顺序

新任务默认只按：

```text
1. 极限短时间
-> 2. 成熟方案集群
-> 3. 高智能虚拟成熟
```

执行。

其中现实标定、案例测试、故障注入、最终认证等，如果需要，都只能作为这三个核心内部为了完成当前核心目标而使用的工具或证据，不能升级成新的方法层级。

尤其禁止把：

```text
L0 -> L1 -> L2 -> L3 -> L4
```

重新变成母方法流程。

---

# 完成即交接

这不是第四核心，只是固定收尾动作。

只要已经存在完整的：

~~~text
冻结方案
执行文件
命令包
技能包
~~~

并且下一步需要 Codex、Reasonix、本地模型或其他执行器执行，则聊天中的交接命令**不得重复执行正文**。

详细内容只能有一个正式来源：

~~~text
SOURCE_OF_TRUTH = 执行文件 / 技能包
~~~

聊天里的交接只负责“指路”。

默认最小格式：

~~~text
请读取：
<仓库 / 分支 / 文件>

按文件完整执行。
完成后按文件要求回传。
~~~

禁止：

~~~text
执行文件已经写完整
+
聊天里再把规则、步骤、限制、RETURN 字段完整抄一遍
~~~

原因：

~~~text
重复文本增加长度
重复文本可能版本不一致
重复文本增加理解歧义
重复文本增加执行故障率
~~~

读取失败时才使用 fallback：

~~~text
1. 优先读取本地已部署的同一技能包 / 执行文件；
2. 远端与本地都无法读取时，才允许在聊天中完整展开执行内容。
~~~

目标：

~~~text
HANDOFF_EXTRA_USER_TURN=0
HANDOFF_DUPLICATE_INSTRUCTIONS=0
ONE_EXECUTION_SOURCE_OF_TRUTH=YES
~~~

---

# 历史资料的地位

历史资料全部保留，但只有两种用途：

```text
EVIDENCE
MATURE_SOLUTION_SOURCE
```

没有第三种用途。

历史内容不能定义当前流程；当前流程永远只有三核心白名单。

---

# 随机系统与历史能力

ATTEMPT / DELIVERY、T_TFVR、verifier、checkpoint、idempotency、Capacity Router、Failure Index、H3-P0 等历史能力全部保留。

它们不是新的方法核心，只能作为三核心内部的工具：

- 帮助第 1 核心更快达到 VALID；
- 作为第 2 核心中的成熟能力；
- 被第 3 核心组合、冻结并验证。

---

# 最终一句话

> **三核心就是唯一白名单；方案完成后只发最小“读取并执行”指令，详细执行规则只保留在一个正式文件/技能包中。**

---

## Experimental Jev shadow overlay

本分支允许一个实验性 overlay，但它不是第四核心，也不改变 v3.1.2 正式版本。

它只映射到：

```text
CORE_3 高智能虚拟成熟
-> JEV_DECISION_ACCELERATOR
```

适用范围：已由高智能建立闭合答案空间、但仍需要快速语义判断的 routing / classification / gating / ranking 节点。

职责边界固定：

```text
确定事实、算术、最终验证 -> CODE
有限语义判断             -> JEV
开放式推理、方案创造     -> GPT/DeepSeek
```

H3-P0 第一验证只允许历史 known-answer shadow replay，`H3_GPU_RUNS=0`。

正式参考：

`references/JEV-DECISION-ACCELERATOR-v0.1.md`

执行命令：

`docs/h3-p0/20260919-jev-shadow/H3-P0-JEV-SHADOW-COMMAND-v1.md`

只有 shadow gate 与后续低风险 real gated 验证都通过后，才允许讨论升级正式 v3.1.3。

---

## Jev Probability-Attack Virtual-99

本分支在 Experimental Jev shadow overlay 之上新增一个已经冻结的 Virtual-99 方案；仍然不是第四核心。

它只属于：

```text
CORE_3 高智能虚拟成熟
-> JEV_PROBABILITY_ATTACK_VIRTUAL_99
```

权威设计：

`references/JEV-PROBABILITY-ATTACK-VIRTUAL-99-v1.md`

机器合同：

`references/JEV-PROBABILITY-ATTACK-VIRTUAL-99-v1.json`

冻结记录：

`docs/h3-p0/20260919-jev-virtual99/H3-P0-JEV-VIRTUAL-99-FREEZE-v1.md`

未来验证命令：

`docs/h3-p0/20260919-jev-virtual99/H3-P0-JEV-PROBABILITY-ATTACK-VERIFY-02-COMMAND-v1.md`

固定规则：先 Virtual-99，后 reality verify；现实验证只证明冻结方案，不现场重新设计。
