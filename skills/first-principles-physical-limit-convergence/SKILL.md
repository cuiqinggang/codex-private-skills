---
name: first-principles-physical-limit-convergence
description: 整体闭环极限短时间引擎 v5.1.1。唯一目标 T*=min(T_VALID)；顶层永久只有“虚→实”；测试从真实用户正式使用路径反推，真实用户旅程是最高级验收，低层测试只负责快速发现与防回归。
metadata:
  version: "5.1.1"
  display_name: "整体闭环极限短时间引擎"
  release_state: "RULE_FROZEN_REAL_USAGE_VALIDATION_PENDING"
---

# 整体闭环极限短时间引擎 v5.1.1

## 0. v5.1.1 当前冻结规则

当前页面名称：

`整体闭环极限时间引擎 5.1.1版`

当前版本：

`5.1.1`

前代 v5.0.8 / v5.0.9 / v5.1.0 只作为历史演化与 Reality Delta 证据，不再作为当前版本。

### 0.1 测试第一性原理

测试的唯一目的：在正式交付前，以最短有效时间发现“用户正式使用时会失败”的问题。

当前最高级测试原则固定为：

1. **正式怎么用，测试就怎么测。**
2. **测试对象是用户真正看到和得到的结果，不是内部状态或实现。**
3. **测试器只观察，不帮助系统补步骤、补字段、推进状态或调用正式运行不会自己调用的逻辑。**
4. **真实使用发现的错误：记录 → 找根因 → 修复 → 下沉为低层回归测试 → 重新完整真实任务。**

形式化要求：

`TEST_ENTRY == PRODUCTION_ENTRY`

`TEST_PATH == PRODUCTION_PATH`

`TEST_OUTPUT == USER_VISIBLE_PRODUCTION_OUTPUT`

任一不成立：

`TEST_IS_NOT_RELEASE_EVIDENCE`

### 0.2 最高级验收：真实用户旅程

最高级验收采用少量、完整、与正式使用同构的真实任务，不允许以测试专用入口替代。

最低覆盖三类真实旅程：

- 正常：`虚 → 实 → PASS → FINAL_VALID`
- 差异：`虚 → 实 → FAIL → 回虚`
- 阻断：`虚 → 实 → BLOCKED → RETURN_TO_GPT`

测试必须从用户正常自然语言任务开始，完整经过真实 GPT 输出、真实时间显示、真实 Freeze、真实 Codex CHAT 自然语言派发、真实返回和 GPT 最终收口。

只要途中需要人工提醒系统“补时间、补 Locator、补 Timeline、继续进入实、修正 RETURN_TO_GPT”等，整轮真实用户旅程即判 FAIL。

### 0.3 低层测试的正确角色

单元测试、状态矩阵、随机测试、Mutation、故障注入、组件集成测试全部保留，但只用于：

- 快速定位错误；
- 提前发现已知错误；
- 防止现实失败复发；
- 缩短真实用户旅程失败后的修复时间。

它们不能单独签发：

- `REAL_CERTIFIED=YES`
- `LIVE_E2E_ENFORCED=YES`
- `FINAL_VALID=YES`
- `DONE=YES`

真实用户旅程是最终裁决对象。

### 0.4 现实失败回流

当真实用户旅程发现错误：

`真实失败 → Reality Delta → 根因 → 修复 → 低层回归 → 新 Freeze → 从 TASK_ACCEPTED 重新完整真实任务`

禁止在正在验收的同一轮任务中现场补丁后继续算 PASS。

### 0.5 当前状态

`RULE_FROZEN=YES`

`REAL_USAGE_VALIDATION=PENDING`

`SEVEN_STAR_CERTIFIED=NO`

`FINAL_VALID=NO`

`DONE=NO`

v5.1.1 是否有效，只允许由下一次正式使用方式的真实用户旅程证明，不预先宣布“七星”。

---

## 1. 唯一目标

唯一优化目标永久只有：

`T* = min(T_VALID)`

其中：
- 正确性、安全、质量、完整性、任务要求、证据要求决定结果是否进入 `VALID` 集合；
- 只有进入 `VALID` 集合的现实结果，才允许按 `T_VALID` 比较快慢；
- 不再引入“时间+质量+成本+安全”的第二评分轴。

顶层 `T_VALID` 固定为：

`T_CLOSED_LOOP_VALID`

即从 `TASK_ACCEPTED` 到 `FINAL_VALID` 的整体闭环有效时间。

---

## 2. 顶层状态机

顶层永久只有两步：

`虚 -> 实`

### 虚
负责：
- 设计；
- 成熟方案吸收；
- 实现物化；
- GPT 独立验证；
- 故障注入；
- 等价性验证；
- Freeze；
- Reality Capsule；
- 时间收口。

### 实
只执行已经冻结的 Reality。

现实失败只能：

`Reality Delta -> STOP -> 回虚 -> 吸收差异 -> 新 Freeze -> 再实`

禁止在当前 Freeze 下现场修改、现场修复、原地重试或换路线。

---

## 3. Reality 的最终判定规则

### 3.1 现实有效性优先

现实结果先判断：

`REAL_VALID = YES / NO`

现实有效的基本要求由当前任务冻结合同决定，例如：
- 语义/功能检查全部通过；
- 冻结资产一致；
- Reality 前置物化通过；
- 必要安全与证据门通过。

### 3.2 虚拟性能预测不是现实硬门

虚拟阶段得到的性能预测、估算值、跨环境换算值，只能作为：
- 优化目标；
- 假设；
- Reality 前的参考锚；
- Reality Delta 对照值。

除非时间本身是外部任务明确规定的硬约束，否则：

`REAL_T > VIRTUAL_PREDICTION`

不得自动推出：

`REAL_VALID = NO`

Reality 的职责是让现实修正虚拟模型，不是让虚拟预测否定现实。

### 3.3 现实 T* 的最终来源

最终性能锚必须来自现实有效结果：

`REAL_T* = min(REAL_VALID_T)`

如果存在多个现实有效候选：
- 保证任务语义等价；
- 使用冻结的同一测量协议；
- 比较现实有效候选的实际测量结果；
- 最短有效现实时间成为最终 `T*`。

---

## 4. 最终优化收口规则

当首次 Reality 已经证明：
- 功能正确；
- 现实可执行；
- 但仍存在明确、低成本、可证明的性能浪费；

允许：

`一次明确优化 -> 一个新 Freeze -> 一次最终 Reality`

禁止无限追求虚拟预测值。

最终 Reality 推荐：
- 保留现实有效基线作为候选 A；
- 加入语义等价优化版作为候选 B；
- 每个候选先预热，再进行固定次数正式现实测量；
- 所有正式样本必须满足任务有效性；
- 优化版无效时只淘汰优化版，不否定有效基线；
- 所有现实有效候选中，最短实际时间成为最终 `T*`；
- 最终 Reality 完成后必须收口，不进入无休止优化循环。

v5.0.8 最终 Reality 使用：

`warmup=1000`

`samples=1000`

并记录：
- MIN
- P50
- P95
- MAX

唯一排序指标仍然是有效样本中的最短现实时间；P50/P95/MAX 用于诊断稳定性，不构成第二优化目标。

---

## 5. v5.0.8 最终现实认证结果

最终冻结：

`ESTE-v5.0.8-REALITY-FIRST-FINAL-CLOSEOUT-VIRTUAL-FREEZE-R4`

Freeze 一致性：

`31/31 PASS`

两个候选均通过现实有效性：

### R3 基线
- VALID：1000/1000
- MIN：0.0074 ms
- P50：0.0077 ms
- P95：0.0093 ms
- MAX：0.6865 ms

### R4 优化版
- VALID：1000/1000
- MIN：0.0027 ms
- P50：0.0028 ms
- P95：0.0030 ms
- MAX：52.2077 ms

最终赢家：

`R4_OPTIMIZED`

最终现实认证：

`CERTIFIED_REAL_T_STAR_MS = 0.0027 ms`

即：

`2.7 微秒`

历史虚拟预测：

`0.01136838145574825 ms`

只保留为历史预测证据：

`HISTORICAL_PREDICTION_IS_GATE = NO`

---

## 6. 整体闭环最终时间

当前正式 Timeline：

`ESTE-v5.0.7-NUMERIC-TIME-ANCHOR-01`

最终：

`FINAL_CLOSED_LOOP_T_VALID_MS = 9983551.271 ms`

即：

`02:46:23.551271`

最终状态：

`FINAL_VALID = YES`

`REAL_CERTIFIED = YES`

`DONE = YES`

---

## 7. 时间连续性

每个任务首次进入建立且以后不可更换：
- `TIMELINE_ID`
- `TIME_ORIGIN_UTC`

所有虚/实转换只向同一账本追加事件。

关键控制边界必须显式携带数值时间：
- TASK_ACCEPTED
- DECISION_COMMIT
- VIRTUAL_MATURITY_TIME_CLOSEOUT
- FREEZE_COMMIT
- REAL_DISPATCH
- EXECUTOR_RETURN_PASS
- EXECUTOR_RETURN_FAIL
- EXECUTOR_RETURN_BLOCKED
- RETURN_TO_VIRTUAL
- FINAL_VALID

规则固定：

`ALWAYS COUNT + PRINT AT CONTROL BOUNDARY`

禁止：
- N/A
- NA
- NULL
- MISSING
- Infinity
- NaN
- 空值

状态词不能代替时间数字。

---

## 8. Freeze 与 Reality 资产规则

正常权威源：

`REMOTE_SHARED_REPO_DIRECT`

Reality 必须按冻结的：
- repository
- branch/commit
- path
- blob

读取权威资产。

共同私库正常时禁止：
- 下载包中转；
- 让用户重新找本地位置；
- 无目的扫描本地磁盘；
- 现场切备用路径。

Freeze 后任何冻结资产变化，旧 Freeze 不再代表新资产。

认证过的 Freeze 必须保持不可变；后续文档/发布说明更新不得改写历史 Reality 证据。

---

## 9. Reality 物化规则

可执行 Reality Capsule 使用无损物化路径。

v5.0.8 最终采用：
- Git 原生对象字节；
- Python subprocess 参数数组；
- `shell=False`；
- `text=False`；
- 原始 bytes；
- 精确 Git blob 校验；
- ASCII-only；
- `compile(bytes)`；
- fresh namespace exec；
- callable 检查。

禁止依赖：
- btoa
- atob
- Buffer
- JavaScript Base64 转码
- PowerShell 文本管道重新编码冻结源码

前置物化属于 Reality 前置门，不混入核心证书计时。

---

## 10. 执行器与固定约束

执行适配器：
- CODEX -> CHAT
- PLAYWRIGHT -> NATIVE_BROWSER
- REASONIX -> UI_AGENT
- LOCAL_FROZEN -> FROZEN_RUNNER

对 Codex：
- 只发送 Codex CHAT 自然语言任务；
- 禁止 PowerShell/Shell/`codex exec` 作为用户派发模式；
- Locator 固定使用：
  `【页面名｜任务名｜序号｜虚/实】`
- 同一连续 Reality 任务序号最多 01–06；
- 第 6 次仍未完成必须 STOP -> 回虚；
- 结构性 Reality Delta 可提前回虚，不必机械耗尽 6 次。

禁止修改：
- FlClash
- Windows 代理
- 系统网络设置

---

## 11. 真实回复执行绑定与结束门

v5.0.8 的状态机、时间信封和校验器只有在**真实回复结束前被调用**时才构成有效控制。

必须区分两种认证：

- `COMPONENT_CERTIFIED`：状态机/校验器在显式调用时行为正确；
- `LIVE_E2E_ENFORCED`：真实 GPT/Codex 使用流程确实经过这些门并产生要求的控制交换。

组件测试通过不得自动推出真实端到端执行约束已经生效。

### 虚拟成熟后的强制结束门

一旦同时满足：

`VIRTUAL_MATURE=PASS`

`SOLUTION_FROZEN=YES`

`REAL_STARTED=NO`

则当前回复**不得以总结、状态说明或 Freeze 结论结束**。

必须继续完成：

`VIRTUAL_MATURITY_TIME_CLOSEOUT -> FREEZE_COMMIT -> FREEZE_TO_REAL -> REAL_DISPATCH`

并在同一回复中输出可直接交给目标执行器的 Reality Dispatch。

Reality Dispatch 至少必须显式包含：

1. `【页面名｜任务名｜序号｜实】`
2. `【时间锚｜整体已用=<数字>ms｜本次已用=<数字>ms｜T*=<数字>ms】`
3. `TIMELINE_ID`
4. `TIME_ORIGIN_UTC`
5. `DISPATCH_UTC`
6. `FREEZE_ID`
7. 冻结资产/路径/版本
8. Reality VALID 条件
9. Reality 计时边界
10. PASS / FAIL / BLOCKED 返回合同
11. `RETURN_TO_GPT=YES`

如果真实可审计的 `TIMELINE_ID / TIME_ORIGIN_UTC` 从未建立：

- 必须 BLOCK；
- 不得伪造整体已用时间；
- 先建立或恢复可审计 Timeline，再允许 REAL_DISPATCH。

### 控制权规则

Reality 执行器不得自行宣布整个任务 `FINAL_VALID/DONE`。

无论 PASS / FAIL / BLOCKED，现实执行结束后均必须：

`RETURN_TO_GPT=YES`

由 GPT 验证时间连续性、Reality 结果和最终收口。

### 机械回归门

权威实现：
- `contracts/FINAL-RESPONSE-ENFORCEMENT-v5.0.8.json`
- `runtime/final_response_gate_v5_0_8.py`
- `tests/test_final_response_gate_v5_0_8.py`

DSE v1.0.3 的真实失效回复已经作为回归反例：
- 有 REAL Locator，但没有数值时间信封；
- 没有 TIMELINE_ID / TIME_ORIGIN_UTC / DISPATCH_UTC；
- 成功路径写成 `RETURN_TO_GPT=NO`。

该反例必须被结束门拒绝。

> 注意：纯 Skill 文本和 Python 校验器本身不能证明宿主 ChatGPT/Codex 一定调用该 gate。最终 `LIVE_E2E_ENFORCED=YES` 只能由新的真实使用测试证明。

---

## 12. 最终权威证据

最终 Reality 报告：

`docs/first-principles/v5.0.8/FINAL-REALITY-REPORT-R4.json`

最终证书：

`docs/first-principles/v5.0.8/FINAL-VALID-CERTIFICATE.json`

最终 Reality Freeze：

`docs/first-principles/v5.0.8/FREEZE-MANIFEST-R4.json`

认证分支保持不可变：

`codex/first-principles-physical-limit-convergence-v5.0.8-r4-virtual-freeze`

v5.0.8 最终发布规则以本文件为准；历史 v5.0.2/v5.0.3/v5.0.5/v5.0.7/v5.0.8 R2/R3 文件保留为演化与 Reality Delta 证据，不得覆盖最终规则。
