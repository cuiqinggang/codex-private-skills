---
name: first-principles-physical-limit-convergence
description: 第一性原理极限短时间引擎 v3.1.8。唯一方法白名单只有三个核心：极限短时间、成熟方案集群、高智能虚拟成熟。正式执行命令的定位标签必须用第四个中文字段明确标注真实核心归属；不能明确归属或任务跨多个核心时必须拆分，不得发布。Codex/Reasonix/本地执行器只有冻结方案执行权，没有修复、重新设计、虚拟成熟或自行找路线的权限；现实失败只回传差异并停止，由 GPT 页面重新进入三个核心之一处理。
metadata:
  version: "3.1.8"
  short-description: 三核心唯一白名单·四字段中文核心定位·执行器禁止自行修复
  lineage: first-principles-physical-limit-convergence@3.1.8 <- @3.1.7 <- @3.1.6 <- @3.1.5 <- @3.1.4 <- @3.1.3 <- @3.1.2 <- @3.1.1 <- @3.1.0 <- @3.0.0 <- @2.0.0 <- @1.x
---

# 第一性原理极限短时间引擎 v3.1.8

> **只走三条路：用唯一时间标准确定目标；先吸收成熟方案集群；再由高智能虚拟成熟并直接验证冻结方案。除此之外，没有第四条路。**

正式 Skill ID 不变：

`first-principles-physical-limit-convergence`

## 强制三关门禁

本技能执行流程只有三关；中文含义拥有用户可见方法权，英文只保留为机器兼容别名：

第一关 = 成熟现实（机器别名：STEP 1 / MATURE_REALITY）
只建立成熟方案、现实事实、历史证据与边界。

第二关 = 高智能虚拟成熟（机器别名：STEP 2 / VIRTUAL_99）
只由 GPT 页面完成设计、简化、组合、故障推演、程序化成熟和冻结。

第三关 = 冻结方案现实验证（机器别名：STEP 3 / REAL_VERIFY）
执行器只执行和观察第二关已经冻结好的方案，不在现实中设计、修复或找新路线。

每次 GPT 发布执行命令前必须声明：

CURRENT_STEP=<1|2|3>

命令必须属于 CURRENT_STEP。

如果命令不属于 CURRENT_STEP，
或者无法明确判断属于哪一步：

BLOCK
禁止发布或执行命令。

STEP 3 中如果发现任何需要改变冻结方案的问题：

只记录 REALITY_DELTA
STOP
RETURN_TO_STEP_2

禁止在 STEP 3 现场修改：
算法、prompt、threshold、权重、view、模型、fallback、路由或验证合同。

Codex 收到：
- 没有 CURRENT_STEP 的正式执行命令
- CURRENT_STEP 与命令实际内容冲突的命令

必须：

SKILL_GATE=BLOCKED
ACTION=STOP

不得自行补全、猜测或探索。

## 强制任务定位 / 四字段中文核心归属门禁

这不是第四核心，也不是第四步骤；它只负责把每一条正式命令锁死到三个既有核心中的一个，防止“修复、补丁、临场优化”等措辞偷偷生成第四条路。

### 唯一可见格式

```text
【<实际页面名>｜<具体任务名>｜<序号>｜<核心归属>】
```

第四字段“核心归属”只允许下面三个中文值之一：

```text
极限短时间
成熟方案集群
高智能虚拟成熟
```

禁止在第四字段使用：

```text
CORE_1 / CORE_2 / CORE_3
STEP 1 / STEP 2 / STEP 3
MATURE_REALITY / VIRTUAL_99 / REAL_VERIFY
修复 / 补丁 / 优化 / 验收
任何其他自造分类
```

示例：

```text
【playwright浏览器自动化5｜现实环境全面检查｜1｜成熟方案集群】
【playwright浏览器自动化5｜冻结极限方案｜2｜高智能虚拟成熟】
【playwright浏览器自动化5｜执行冻结方案现实验证｜3｜高智能虚拟成熟】
```

四个字段只回答四个问题：

1. `实际页面名`：工作发生在哪一个聊天页面。用户提供则原样使用；否则只有系统能读取真实标题时才使用；两者都没有则不猜。
2. `具体任务名`：当前真正要执行的具体任务，用最短中文或原有名称直接复述，不建立额外任务编码。
3. `序号`：该具体任务中的第几条 GPT 正式执行命令，只用普通整数；它只是计数，不代表“修复阶段”。
4. `核心归属`：这条命令真实属于三个核心中的哪一个；必须且只能填一个中文核心名。

### 核心归属真实性门禁

GPT 在发出正式执行命令前必须先回答：

```text
这条命令真实属于：
极限短时间？
成熟方案集群？
高智能虚拟成熟？
```

只有能够唯一、真实映射到其中一个核心时才能发布。

如果：

- 无法明确归属；
- 同一命令同时跨两个或三个核心；
- 任务名写的是执行，但正文实际要求执行器重新设计；
- 用“修复、补丁、继续优化、自己想办法”等方式绕过三个核心；

则：

```text
核心定位门禁=阻断
动作=停止
```

GPT 必须先拆分任务或在 GPT 页面完成高智能虚拟成熟，再生成新的冻结执行命令。

### Codex / Reasonix / 本地执行器权限边界

执行器只有以下权限：

```text
执行 GPT 已冻结的命令
运行已冻结程序
做确定性的读写/测试/部署/现实验证
记录事实与现实差异
按规定格式回传
停止
```

执行器没有以下权限：

```text
自行创建“修复任务”
自行决定怎么修
自行重新设计方案
自行新增路线
自行改变模型、阈值、路由、fallback、验证合同
自行进行高智能虚拟成熟
现实失败后继续试另一种办法
```

现实执行或验证中一旦发现冻结方案需要改变：

```text
记录现实差异
-> 停止
-> 返回 GPT 页面
-> 由 GPT 页面重新判断属于三个核心中的哪一个
-> 若需要，GPT 在“高智能虚拟成熟”中重新成熟并冻结
-> 再发新的执行命令
```

Codex 不得形成：

```text
失败 -> 自己修 -> 再试
```

只允许：

```text
失败 -> 记录 -> 停止 -> 返回 GPT
```

如果 GPT 已经把修正方案完整冻结，Codex 可以执行该冻结方案；但该任务性质是“执行冻结方案”或“现实验证”，不是 Codex 自己的“修复任务”。

### 序号规则

- 同一具体任务的序号单调递增。
- 序号只是 GPT 正式命令计数，不再存在“4..6 修复窗口”。
- 正常目标尽量在 1..3 条正式命令内闭环。
- 若未闭环，Codex 只能停止并回传；是否存在下一条命令由 GPT 页面决定。
- 如继续发新命令，仍必须重新通过第四字段核心归属门禁。
- 第 6 条后仍未闭环则必须 STOP，由 GPT 页面重新冻结或拆分任务；执行器不能继续自行延伸。
- 页面名、任务名、序号、核心归属四者共同构成定位键。

### 页面名来源

优先级只有三条：

```text
1. 用户提供页面名 -> 原样使用
2. 用户未提供，但系统能读取真实页面标题 -> 使用真实标题
3. 两者都没有 -> 不猜
```

禁止用任务名、技能名或项目名冒充页面名。

### 显示位置

GPT 正式命令：第一行和最后一行必须放完全相同的四字段定位标签。

Codex / Reasonix / 本地执行器最终汇报：最后一行必须原样返回同一四字段定位标签。

任一字段缺失、不一致，或第四字段不是三个允许的中文核心名：

```text
定位门禁=失败
动作=停止
```

机器匹配：

```text
LOCATOR_KEY = EXACT_PAGE_NAME + "|" + EXACT_TASK_NAME + "|" + INTEGER_SEQUENCE + "|" + EXACT_CHINESE_CORE_NAME
```

### 全局接收端兜底门禁

Codex 端全局 `~/.codex/AGENTS.md` 必须保留极短兜底规则：

```text
任何来自 GPT/用户、要求执行实际工作的正式命令，必须包含：
【页面名｜任务名｜序号｜核心归属】

核心归属只允许：
极限短时间
成熟方案集群
高智能虚拟成熟

缺失任一字段、第四字段不是上述三个中文值之一、或正文实际工作与核心归属冲突：
核心定位门禁=阻断
动作=停止
不得执行，不得猜。

Codex 只执行冻结命令；不得自行建立修复任务、重新设计、改变路线或做虚拟成熟。

现实失败或发现需要改变冻结方案：
只记录现实差异并停止，返回 GPT 页面。

有合法标签时，最终汇报最后一行必须原样返回同一标签。
```

这是接收端兜底，不替代 GPT 发送端规则。

固定闭环：

```text
GPT 页面判断三核心归属
-> GPT 完成需要的虚拟成熟与冻结
-> 四字段定位标签
-> Codex 全局接收门禁
-> Codex 简单执行
-> 回传结果/现实差异
-> 停止
```

只有发送端与接收端同时通过，才允许执行。


---

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

这不是第四核心，只是 STEP 2 虚拟成熟完成后的固定同回复收尾动作。

## 强制触发

只要 GPT 在当前回复中宣布：

```text
VIRTUAL_MATURITY=PASS
VIRTUAL_99=PASS
虚拟成熟通过
冻结方案通过
```

且已经存在可由 Codex / Reasonix / 本地执行器继续部署或现实验证的冻结方案、执行文件、技能包或仓库版本，则：

```text
SAME_REPLY_CODEX_HANDOFF_REQUIRED=YES
```

**必须在同一回复末尾直接给出一条可复制执行的最短命令。**

如果已经宣布虚拟成熟通过，但本回复没有同步给出该短命令：

```text
HANDOFF_GATE=FAIL
VIRTUAL_CLOSEOUT=INCOMPLETE
禁止把本轮写成完整收口
```

禁止回复：

```text
“下一步我可以给你命令”
“你确认后我再给 Codex”
“之后再部署验证”
```

因为这会无意义增加一个用户往返。

## 最短命令原则

如果详细执行内容已经写入 GitHub / 执行文件 / 技能包：

```text
SOURCE_OF_TRUTH = 远端文件
聊天命令 = 只给读取位置 + 执行 + 回传
```

默认：

```text
读取 <仓库/分支/文件或技能目录>。
按其中冻结规则部署并现实验证。
完成后只回传最终验收结果。
```

如果任务极短、完整正文比“读取远端”更短，则允许直接内联最小命令。

目标固定：

```text
HANDOFF_EXTRA_USER_TURN=0
HANDOFF_SAME_REPLY=YES
HANDOFF_DUPLICATE_INSTRUCTIONS=0
ONE_EXECUTION_SOURCE_OF_TRUTH=YES
```

注意：任务定位标签遵守 v3.1.5 的“实际页面名｜具体任务名｜序号｜中文核心归属”四字段规则。第四字段只能是“极限短时间 / 成熟方案集群 / 高智能虚拟成熟”之一；如果任务无法真实唯一归属，GPT 不得发布执行命令。若当前模型拿不到真实 UI 页面标题，不得猜页面名。


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

## v3.1.7 正式能力：现实锚定 → 浏览器 Reality R3 → 精确现实数字孪生唯一版

v3.1.7 不增加第四核心。在 v3.1.6 的 Host/Codex Reality 基线之上，正式补入 Browser Reality R3（浏览器现实第三轮采集），并把它纳入同一个现实锚定技能与唯一数字孪生：

```text
核心2 成熟方案集群
→ reality-execution-environment-anchor v1.2.0
→ 完整现实事实、原始字节、运行时边界、规则、指令链、沙盒、技能、Git、安全摘要
→ Reality Fingerprint（现实环境指纹）

核心3 高智能虚拟成熟
→ exact-reality-digital-twin v1.1.0
→ 先复现现实
→ Reality/Twin 差异归零
→ Shadow（影子假设）
→ 故障注入
→ 漂移检测
→ Virtual-99（虚拟99）
→ 冻结最小现实方案
```

唯一正式 Twin：
- 中文名：现实执行环境精确数字孪生唯一版
- 机器名：exact-reality-digital-twin
- 版本：1.1.0
- 正式入口：components/exact-reality-digital-twin/
- 现实输入：reality-execution-environment-anchor@1.2.0
- 当前 Reality Fingerprint V3：9bdd4430596e306cf6f8061069659e2680d8a1b66bd69d7bb3e45fe4cfd63dd8

Twin 第一原则：**先复制现实，不能先修现实。**

当前现实基线必须首先复现：

```text
TARGET Windows sandbox
→ SetTokenInformation
→ ERROR 1344
→ 3/3
→ 子进程未成功启动
→ PATH 解析 NOT_REACHED（未到达）
→ NO_RUNNING_CHILD_PROCESS_TOKEN（不存在运行中的子进程令牌）
```

Reality Mode（现实模式）只读不可修改。
Shadow Mode（影子模式）只能修改 Twin 内存中的假设状态，禁止把 Shadow 结果写回 Reality。

当前状态：

```text
REALITY_ANCHOR_COMPLETE=YES
CRITICAL_UNKNOWN_COUNT=0
CRITICAL_EXECUTION_STATE_COVERAGE_PERCENT=100.00
HOST_R2_TWIN_INPUT_READY=YES
LEGACY_TWIN_CONTRACT_SELFTEST=24/24 PASS
BROWSER_R3_COLLECTOR_CONTRACT=FROZEN
BROWSER_R3_REAL_CAPTURE=NOT_YET
BROWSER_R3_FINGERPRINT=NOT_YET
BROWSER_TWIN_INPUT_READY=NO
BROWSER_GOLDEN_REPLAY=NOT_YET
BROWSER_SHADOW_RUN=NOT_YET
ENVIRONMENT_99=NOT_YET
```

24/24 只证明旧 Host/Codex Twin 合同、差异检测、Reality/Shadow 隔离和确定性重放逻辑通过虚拟自测；不代表完整浏览器 Twin 已完成。

Browser Reality R3 现在必须把 Browser/Profile/Context/Auth/DOM/actionability/Network/Service Worker/WebSocket/Runtime/Trace/CDP/Golden Task 纳入现实输入。R2 中“网络代理对 1344 边界非阻断”的结论不得外推到浏览器 E2E。Browser R3 未在用户机器真实 Golden Task 上完成 3/3 现实采集并生成新指纹前，禁止宣称 FULL_BROWSER_TWIN=YES 或 ENVIRONMENT_99=YES。


---

## Experimental Jev shadow overlay

本分支允许一个实验性 overlay，但它不是第四核心，也不改变 v3.1.5 正式版本。

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

只有 shadow gate 与后续低风险 real gated 验证都通过后，才允许讨论升级正式 v3.1.5。

---

## Jev Virtual-99 v2（ACTIVE）

Verify-02 返回 `SAFE_BUT_NOT_TIME_99` 后，按三步规则返回第 2 步完成简化收敛。当前 ACTIVE Virtual-99 是 v2；仍然不是第四核心，也不是新技能。

它只属于：

```text
CORE_3 高智能虚拟成熟
-> JEV_VIRTUAL_99_V2_SIMPLIFIED
```

权威设计：

`references/JEV-VIRTUAL-99-v2.md`

机器合同：

`references/JEV-VIRTUAL-99-v2.json`

ACTIVE 最短职责：

```text
CODE = state + frozen contract 可唯一确定
JEV  = 仅限无法 CODE 化的闭合语义判断；最多一次 canonical typed request
GPT  = 开放问题或仍不确定的冲突
```

当前 25-case known-answer replay 已全部归 CODE；H02/H03 的 `jev` / `gpt` 是确定性路由输出，不触发真实模型调用。

历史证据（非 ACTIVE）：

- `references/JEV-PROBABILITY-ATTACK-VIRTUAL-99-v1.md/json`
- `docs/h3-p0/20260919-jev-virtual99/H3-P0-JEV-PROBABILITY-ATTACK-VERIFY-02-RESULT-v1.md/json`
- v1 freeze、Verify-02 command/runner 与 Reality Delta

下一次唯一 Real Verify 仅以 v2 内的合同草案为准；未生成可执行命令包，禁止自动开始。


---

## JEV Probability Engine P0 — v3.1.6 现实基线再收敛（ACTIVE FROZEN CASE）

本案例严格属于三核心，不创建第四核心。

现实锚：
```text
PE-P0-GENERAL-01
REAL_BASELINE_VERSION=jev-probability-engine-p0 v0.3.0
REAL_BASELINE_T_P0_MS=840.6046999999962
REAL_BASELINE_GATE=30/30 PASS
```

CORE 2 广域成熟方案池：
`references/JEV-PROBABILITY-ENGINE-P0-MATURE-POOL-v1.md`

CORE 3 GPT Virtual-99：
`references/JEV-PROBABILITY-ENGINE-P0-VIRTUAL-99-v1.md`
`references/JEV-PROBABILITY-ENGINE-P0-VIRTUAL-99-v1.json`

唯一冻结实现：
`components/jev-probability-engine-p0-extreme/`

当前门禁：
```text
MATURE_SOLUTION_CLUSTER=PASS
VIRTUAL_99=PASS
SOLUTION_FROZEN=YES
REAL_VERIFY=NOT_YET
CODEX_DESIGN_AUTHORITY=NO
CODEX_EXECUTOR_ONLY=YES
```

冻结方案固定为：Jev 1.13、一个 model barrier、2 个 dependency-affinity + runtime LPT byte-balanced shards、projected state、short state-path Choice、2 条预热 persistent connections、per-shard early release、receipt O(1) policy lookup、in-memory reducer + 单 append-only log、incremental deterministic verifier + one final gate。

现实执行若任何一项失败或 30/30 通过但最短时间未低于 840.6046999999962 ms：
`REALITY_DELTA -> STOP -> RETURN_TO_GPT`。
Codex/Reasonix/本地执行器禁止自行改变方案。


---

## v3.1.8 ACTIVE：Browser + Network 统一数字孪生虚拟成熟冻结

本升级不增加第四核心。

归属：
- 现实锚定与真实输入采集：核心2「成熟方案集群」
- Twin 的组合、冲突消解、故障推演、虚拟测试与冻结：核心3「高智能虚拟成熟」

当前 ACTIVE 组件：

```text
reality-execution-environment-anchor@1.2.0
  + browser-reality-r3-timing.mjs
  + browser-reality-r3.mjs

exact-reality-digital-twin@1.2.0
  + ENGINE.py
  + BROWSER-TWIN-INPUT-CONTRACT-v2.md
  + BROWSER-NETWORK-TWIN-REAL-VERIFY-v2.md
```

虚拟成熟结果：

```text
VIRTUAL_MATURITY=PASS
UNIFIED_TWIN_ENGINE=FROZEN
ENGINE_SCHEMA=browser-network-unified-twin-2.0
VIRTUAL_SELFTEST=39/39 PASS
```

时间唯一标准冻结为：

```text
T1/T2/T3 = 三个轻量真实计时运行
O1       = 独立重观测运行
T_VALID  = min(T1,T2,T3)
```

O1 只证明因果链和完整 Reality，不进入 T_VALID，也不能替代失败的 T1/T2/T3。

当前现实门禁仍然真实保持：

```text
REAL_BROWSER_ATTACH=BLOCKED
REAL_BROWSER_R3_INPUT=INCOMPLETE
BROWSER_TWIN_INPUT_READY=NO
FULL_BROWSER_TWIN=NO
ENVIRONMENT_99=NOT_YET
```

因此 v3.1.8 已完成第三核心的完整虚拟成熟，但没有冒充现实认证完成。
下一步只允许执行冻结现实验证；若现实 Attach 不存在或任何门禁失败，只记录 REALITY_DELTA 并 STOP。
