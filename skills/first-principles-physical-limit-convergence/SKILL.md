---
name: first-principles-physical-limit-convergence
description: 整体闭环极限短时间引擎 v5.0。用确定性状态机约束“什么允许发生”，用智能核心完成“虚”，用现实执行核心完成“实”。唯一优化目标仍是 min(T_VALID)。
metadata:
  version: "5.0.0"
  display_name: "整体闭环极限短时间引擎"
---

# 整体闭环极限短时间引擎 v5.0

## 唯一目标
在所有有效条件通过的前提下：`T* = min(T_VALID)`。
时间是唯一优化目标；正确性、安全、商用等只定义“有效/无效”。

## 架构：两个工作核心 + 一个确定性控制内核

### 虚拟成熟核心
负责真正“想清楚事情”，不是状态机替你思考。
必须得到：有效完成定义、现实事实与约束、可复用成熟方案、未知事实的最低成本获取方式、各有效候选的时间竞争、失败路径/Reality Delta攻击、唯一冻结方案与本任务T*。

原则：
`已知->直接用`
`未知->最小成本取得事实`
`成熟方案->优先复用`
`多方案->有效门通过后只比较T_VALID`

### 现实执行核心
只执行冻结方案，不现场重新设计。
`执行冻结动作 -> 记录真实时间 -> 验证 -> PASS/FAIL`
FAIL：`Reality Delta -> STOP -> 回虚 -> 新冻结 -> 再实`

### 确定性状态机内核
只负责当前唯一状态、唯一合法转换、非法状态阻断、自动渲染定位首行、决定任务有没有执行资格。
它不替代虚拟成熟核心的推理能力。

## 状态
方法阶段永远只有：`虚`、`实`。
完成不是第三阶段，只是`done=true`。

最小状态字段：
PAGE_NAME、TASK_NAME、GENERATION、ATTEMPT、PHASE、T_STAR_MS、FREEZE_ID、REAL_ADAPTER、DISPATCH_MODE、DONE。

## 状态机自动首行
首行不得由模型自由书写，由状态对象确定性渲染：
`【页面名｜任务名｜NN-NN｜虚/实】 极限锚MM:SS.mmm`
缺页面、任务、状态或T*时，任务不得继续。

## 唯一合法主循环
`虚 -> 虚拟成熟 -> 冻结/发布/回读 -> 自包含现实胶囊 -> 状态机检查 -> 实 -> 执行/计时/验证`

成功：`实 + PASS -> done=true`
失败：`实 + FAIL -> Reality Delta -> 虚`

同一方案代现实尝试只允许01–06；07永久非法。
第6次失败强制下一方案代01；第1–5次结构性错误可提前换代。

## 虚→实硬门
只有全部成立才允许转换：
VALID已定义；现实事实已就绪；成熟方案已选定；执行链已闭合；外部依赖已闭合；本任务新T*合法；新FREEZE_ID；Freeze发布后回读哈希一致；现实胶囊自包含；现实执行适配器与模式合法；时间合同完整；来源范围明确；远程声明已回读；现实任务自身标记为“实”。

任一失败：保持“虚”，零现实执行。

## 执行适配器
当前注册：
- CODEX -> 仅CHAT（Codex页面/会话自然语言模式）
- PLAYWRIGHT -> NATIVE_BROWSER
- REASONIX -> UI_AGENT
- LOCAL_FROZEN -> FROZEN_RUNNER

对CODEX：`codex exec / PowerShell / Shell`均不属于合法发送模式，直接BLOCK。
新增工具只扩展适配器注册表，不改主状态机。

## 现实通过硬门
REAL PASS必须同时有：
REAL_START、REAL_END、T_VALID_REAL_MS、verifier=PASS、证据一致、`T_VALID_REAL_MS <= 本任务冻结T*`。
缺真实时间，即使功能成功，也不能PASS。
同一FREEZE_ID只能被一次正式现实消费。

## 现实失败转换
普通失败且attempt<6：`同方案下一attempt｜虚 + 新Freeze`
结构性失败或attempt=6：`下一方案代-01｜虚`
Reality Delta缺失时，不允许失败转换。

## 运行时原则
v4.x有效经验已归约为状态字段、转换门、不变量、适配器策略；历史文字保留在Git历史，不作为v5.0运行时依赖。

## 对外说明
陌生人使用说明：`docs/first-principles/v5.0/PRODUCT-GUIDE-ZH.md`
说明书属于产品解释层，不参与运行时验收。

## 一句话
智能核心负责“把事情想成熟并真正能做”；状态机负责“只有唯一合法动作能发生”；现实执行核心负责“按冻结方案做、计时、验证”。
