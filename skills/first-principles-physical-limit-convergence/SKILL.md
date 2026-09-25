---
name: first-principles-physical-limit-convergence
description: 整体闭环极限短时间引擎 v5.0。智能负责成熟方案，状态机负责唯一合法状态，现实执行器只执行冻结方案；唯一目标 min(T_VALID)。
metadata:
  version: "5.0.0"
  display_name: "整体闭环极限短时间引擎"
---

# 整体闭环极限短时间引擎 v5.0

## 唯一目标
所有有效门通过后，只优化：

`T* = min(T_VALID)`

## 两个工作核心
### 虚
智能核心把任务做成熟：
1. 定义“有效完成”；
2. 读取现实事实/约束；已知直接用，未知才用最低成本搜索、测量或小实验；
3. 优先复用成熟方案；
4. 在有效候选中只按 T_VALID 竞争；
5. 攻击失败路径并吸收 Reality Delta；
6. 冻结唯一方案、本任务 T*、现实胶囊。

### 实
现实执行核心只做：
`执行冻结方案 -> 真实计时 -> 验证`

不得现场重新设计。

失败：
`Reality Delta -> STOP -> 回虚 -> 新冻结`

## 确定性状态机
状态机不替代“虚”的智能，只决定什么动作有资格发生。

方法阶段永远只有：
`虚`
`实`

完成只是 `DONE=true`，不是第三阶段。

状态最小字段：
`PAGE_NAME TASK_NAME GENERATION ATTEMPT PHASE T_STAR_MS FREEZE_ID REAL_ADAPTER DISPATCH_MODE DONE`

定位首行由状态机自动渲染，模型不得自由书写：

`【页面名｜任务名｜NN-NN｜虚/实】 极限锚MM:SS.mmm`

## 唯一转换
`虚 --全部冻结门PASS--> 实`
`实 --PASS--> DONE`
`实 --FAIL+Reality Delta--> 虚`

虚→实必须同时满足：VALID、事实、成熟方案、执行链/外部依赖闭合、新T*、新Freeze、发布后回读哈希一致、自包含现实胶囊、合法执行适配器、时间合同、来源范围、现实任务标“实”。

任一缺失：保持“虚”，零现实执行。

REAL PASS必须同时有真实开始/结束/T_VALID_REAL、验证器PASS、证据一致，并满足冻结T*。

## 有限循环
每方案代现实尝试只允许01–06；07非法。
第6次失败强制下一方案代01；第1–5次结构性错误可提前换代。
同一Freeze只允许一次REAL。

## 执行适配器
当前合法：
- CODEX -> CHAT
- PLAYWRIGHT -> NATIVE_BROWSER
- REASONIX -> UI_AGENT
- LOCAL_FROZEN -> FROZEN_RUNNER

因此CODEX的 `codex exec / PowerShell / Shell` 发送方式直接阻断。

新增工具只加适配器，不改主状态机。

## 权威实现
机器权威：
- `contracts/STATE-MACHINE-v5.0.json`
- `runtime/state_machine_v5.py`

v4.x只保留为演化证据，不作为运行时依赖。

陌生人说明：
`docs/first-principles/v5.0/PRODUCT-GUIDE-ZH.md`
