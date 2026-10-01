# Reality Contract｜极限短时间自动化闭环 v2.0

```ini
STATUS=WORKING_BASELINE_R2_FREE_FIRST
STATE=10
PURPOSE=定义现实必须发生什么，不预设具体成熟方案
MATURE_SOLUTION_EXISTS=TRUE
NO_NEW_IMPLEMENTATION_ESCAPE=TRUE
OBJECTIVE=T*=min(T_VALID)

PRODUCTION_PAID_DEPENDENCY=FORBIDDEN
PRODUCTION_INCREMENTAL_SUBSCRIPTION_COST=0
PAID_BENCHMARK_ALLOWED=YES
PAID_BENCHMARK=Manus 2.0
COMMERCIAL_ROI_EXCEPTION=ONLY_IF_EXPLICITLY_REOPENED
```

## A. 用户现实入口

### 用户怎样提出目标
用户只需要用自然语言给出最终现实目标。

### 用户最少需要提供什么
只提供机器无法替代的内容：
- 最终想要的现实结果；
- 必要的个人偏好 / 价值判断；
- 首次授权或登录时必须由本人完成的凭据动作；
- 法律、支付、账号安全或不可逆高风险动作所需的本人确认。

### 系统必须自动恢复什么
- 当前项目和任务目标；
- 已确认的 VALID 条件；
- 已完成步骤与现实产物；
- 仍未完成的下一动作；
- 已知失败 / 恢复信息；
- 已授权工具与可用成熟能力；
- 与当前任务真正相关的历史证据。

不得要求用户重新复制旧聊天、转发执行回报、重新解释已存在的项目状态。

### 只有哪些情况必须询问用户
- 目标本身存在真正的个人价值取舍；
- 缺少只有用户本人知道且无法从授权来源取得的信息；
- 登录 / MFA / 验证码等必须本人完成；
- 新增费用、付款或购买；
- 账号安全设置变化；
- 删除重要数据或不可逆高风险动作；
- 现实平台强制要求用户接管。

普通路径选择、普通故障恢复、是否换成熟执行方式、常规验收不得默认停下来问用户。

## B. FINAL_VALID

任务只有同时满足以下条件才算完成：

1. 现实结果真实存在；
2. 结果符合合同，而不是只完成中间步骤；
3. 能机器验证的必须机器验证；
4. 执行智能体自身“PASS / Done”不能单独作为 FINAL_VALID；
5. 除 A 节允许的人类不可替代动作外，不需要用户做人肉消息总线；
6. 长任务状态可恢复；
7. 所有搜索、等待、失败、恢复、重试都计入同一 T_FLOW；
8. **正式生产路径不得依赖必须付费才能持续运行的能力。**

## C. 需要消除的人肉胶水

| 当前人工动作 | 标准自动化问题 | v2.0 要求 |
|---|---|---|
| 把 GPT 方案复制给 Codex / Manus / 其他执行器 | Agent handoff / tool orchestration | 自动完成 |
| 把执行器结果再复制回 GPT | result routing / shared task context | 自动完成 |
| 页面卡住后刷新、换页并重建上下文 | durable state / session recovery | 自动恢复 |
| 长任务期间反复提醒“继续” | background execution / resumable work | 自动继续 |
| 普通错误出现后人工判断重试还是换路 | failure recovery / mature alternative routing | 自动处理 |
| 手动打开网页、文件、应用完成普通步骤 | computer use / app action | 自动执行 |
| 人工盯任务是否结束 | monitoring / completion event | 自动监控 |
| 人工确认机器可验事实 | machine verification | 自动验收 |
| 人工保存阶段状态供下次继续 | persistent project/task state | 自动持久化 |
| 在设备之间手动同步进度 | cross-device continuation | 自动同步或成熟平台原生续接 |

## D. 权限与边界

### 可自动执行
在已授权环境内的普通研究、文件操作、编码、测试、网页操作、应用操作、Git / GitHub、工作流运行、信息整理、常规恢复与验证，可自动推进。

### 必须人工决定
- 真正的个人目标 / 价值取舍；
- 新费用、付款、购买；
- 账号安全设置变更；
- 删除重要数据；
- 法律或现实平台明确要求本人确认的高风险动作。

### 禁止改变
- Windows 关键系统不得破坏或删除；
- FlClash / Windows 网络代理配置不得改变；
- 不通过关闭安全限制换取自动化。

## E. 成本边界｜FREE-FIRST

### 正式生产 VALID 硬门
正式长期主链：

```ini
PRODUCTION_INCREMENTAL_SUBSCRIPTION_COST=0
```

允许：
- 免费版本；
- MIT / 开源 / Community Edition；
- 本机已有硬件；
- 已存在且无需新增付费的免费额度；
- 已有成熟免费模型池；
- 免费计划明确包含的能力。

不允许把以下能力作为最终生产依赖：
- 只有付费计划才开放的 Agent / Cloud / Computer Use；
- 需要持续购买 credits 才能运行的主链；
- 免费试用到期后无法继续的能力。

### Manus 2.0 特例
Manus 2.0 只作为成熟付费 Benchmark：

```ini
PRODUCTION_CANDIDATE=NO
BENCHMARK_REFERENCE=YES
USE_EXISTING_CREDITS_ONLY=YES
```

用途：
- 测一个真实成熟整解的端到端 `T_VALID`；
- 作为免费生产路径持续攻击的现实参照；
- 不因 Manus 更快而自动进入最终生产。

### 商业例外
只有未来任务产生明确商业收益，并且用户明确重开成本门时，付费能力才重新进入生产候选。

## F. 中断与恢复

- 页面 / Session 消失：从成熟平台的持久状态自动继续；
- 执行器失败：优先成熟原生 retry / resume / alternate path；
- 网络 / 服务失败：保留状态，恢复或切换另一成熟免费能力；
- 用户修改目标：只重做受影响部分；
- 同一任务身份：优先成熟平台原生 Project / Task / Run / Thread / Artifact 身份。

## G. 时间合同

```ini
FLOW_START=系统已拥有足够信息、可以不再等待用户澄清而开始现实推进的时间点
T_FLOW=从 FLOW_START 到当前的全部现实时间
T_VALID=只有 FINAL_VALID 后才产生
OBJECTIVE=T*=min(T_VALID)
```

失败、恢复、排队、免费额度限流等待都计入 T_FLOW。

## H. 成熟生产方案进入门槛

正式生产候选必须同时满足：

1. 零新增付费依赖；
2. 自然语言目标入口；
3. 项目 / 任务上下文持续；
4. Web / App / File 跨工具执行能力；
5. 后台 / 可恢复任务能力；
6. 定时 / 触发 / 监控能力，或可由成熟免费组件补齐；
7. 普通失败恢复；
8. 结果与产物回传；
9. 机器可验事实自动验收；
10. 用户离开后仍可继续；
11. 不要求用户做人肉消息总线。

关键项缺失时可使用**成熟免费组件最小组合**补齐，但不得开发新的自研框架。

## I. Benchmark 与生产比较

付费 Benchmark 不参加生产 VALID 排名。

定义：

```text
T_REF_MANUS = Manus 2.0 对同一真实任务的端到端 T_VALID
T_VALID_FREE = 免费生产候选对同一任务的端到端 T_VALID
GAP = T_VALID_FREE - T_REF_MANUS
```

GAP 只用于定位还有多少现实时间可攻击，不成为第二优化目标。

正式目标始终是：

```text
在所有满足 FREE-FIRST VALID 的成熟候选中：
T* = min(T_VALID)
```

> 本合同是 STATE=10 工作基线，不等于 Project Freeze。
