---
name: first-principles-physical-limit-convergence
description: 极限短时间引擎 v4.5.6。唯一锚定物改为“从问题进入到问题第一次最终有效解决”的总 T_VALID；所有虚拟、验证、失败、回退、修复、重跑均计时且不得重置。新增时间锚定强制规则。
metadata:
  version: "4.5.6"
  display_name: "极限短时间引擎"
---

# 极限短时间引擎 v4.5.6

## 根基：现实底座

```text
本地 AI 现实底座永久资产
local-ai-reality-foundation
当前版本=v1.1.1
```

它不是第三步，而是“虚/实”共同的现实根基。

虚开始前必须读取与任务有关的最小充分现实；缺少会影响最终有效性或总 T_VALID 的关键现实事实时，虚未完成。

实结束后必须做现实底座吸收检查：只有能缩短未来总 T_VALID 或避免重复失败/重复测量的新现实事实才吸收，否则不吸收、不升版。

# 唯一锚定物：问题总解决时间

```text
T_VALID_ACTIVE
= measure(UNION(AGENT_ACTIVE_INTERVALS))

T*
= min(T_VALID_ACTIVE)
```

中文：

```text
T_VALID_ACTIVE
= 从“问题/目标正式进入”
  到“该问题第一次得到最终有效解决并完成收口”之间，
  GPT、Codex 及其直接执行工具真正处于解决该问题状态的
  全部有效工作区间之并集时间。

用户离开、休息、现实事务造成的空档不计入主锚定时间。
```

## 同一只钟，禁止重置

从 PROBLEM_ENTRY 建立任务计时编号，直到 FINAL_VALID_SOLUTION 才关闭该任务编号。主时间不是简单墙钟差，而是该编号下所有 AGENT_ACTIVE_INTERVAL 的时间并集。

中间以下时间全部属于同一个 T_VALID：

```text
现实事实读取
虚拟成熟
成熟方案检索/组合/淘汰
预测与验证
冻结闭环验收
现实执行
现实前置检查
失败等待
失败诊断
Reality Delta 归因
返回虚拟成熟
规则修正
重新冻结
重新执行
重试
GPT/Codex 为解决问题发生的必要执行等待
最终验收与收口
```

发生失败、回虚、换 runner、换路径、重试时：

```text
TIMER_RESET=FORBIDDEN
```

因此任何“单次运行很快但导致返工”的方案，都不能借重置计时制造虚假的极限短时间。

## 子时间只允许诊断，不允许取代锚定物

例如：

```text
T_ATTEMPT_REAL
T_RUNNER
T_FETCH
T_VERIFY
T_VIRTUAL
```

都可以记录，用于定位瓶颈。

但它们只能是：

```text
ROLE=DIAGNOSTIC_ONLY
```

不得用来替代：

```text
T*=min(T_VALID)
```

不得用“某一步更短”证明整体方案更优。

# 时间锚定强制规则

讨论、设计、修复、增加或删除任何东西时，第一判断必须是：

```text
它对总 T_VALID 的净影响是什么？
```

任何新增步骤 g，只允许在以下条件成立时加入：

```text
E[T_VALID | WITH_g]
<
E[T_VALID | WITHOUT_g]
```

等价理解：

```text
新增步骤自身耗时
<
它所避免的预期返工 / 修复 / 重跑 / 等待总时间
```

更完整地：

```text
NET_TIME_GAIN(g)
= Expected_Avoided_Rework_Time
- Added_Gate_Time
- Added_Maintenance_Time

ADD_g iff NET_TIME_GAIN(g) > 0
```

这里没有第二指标，所有项最终都折算回同一个“问题总解决时间”。

## 一次性任务

对一次性任务：

```text
比较当前问题从进入到最终解决的 T_VALID。
```

## 可复用规则/永久资产

对会反复使用的规则、门禁、缓存、技能资产：

```text
总时间
= 一次性建立时间
+ 后续每次额外检查时间
+ 后续仍残留的返工时间
```

与“不建立该规则”时未来重复发生的返工总时间比较。

即：

```text
ADD_REUSABLE_RULE
iff
BUILD_TIME
+ REPEATED_GATE_OVERHEAD
+ RESIDUAL_REWORK_TIME
<
REPEATED_REWORK_TIME_WITHOUT_RULE
```

所以：

```text
增加一步
!= 时间一定变差

删除一步
!= 时间一定变好
```

真正判断永远是：

```text
最终总 T_VALID 是否更短。
```

若概率或返工成本无法精确知道，不伪造精确数字：

```text
若保守下界收益仍大于新增成本 -> 加
若乐观上界收益仍小于新增成本 -> 不加
否则 -> 回虚做最小验证以缩小不确定性
```


# 全局计时落地

主时钟必须真正记录，不得只停留在概念定义。

每个新问题进入引擎时，立即记录：

```text
TASK_TIME_ID=<唯一任务计时编号>
PROBLEM_ENTRY_NETWORK_TIMESTAMP=<网络时间或可追溯事件>
GLOBAL_TIMER_STATE=RUNNING
GLOBAL_TIME_ANCHOR=T_VALID_ACTIVE
```

问题最终有效解决并完成收口时记录：

```text
FINAL_VALID_TIMESTAMP=<精确时间戳或可追溯事件>
GLOBAL_TIMER_STATE=STOPPED
T_VALID_ACTIVE_GLOBAL
= measure(UNION(AGENT_ACTIVE_INTERVALS))
```

网络时间只负责给任务入口、出口和每个有效工作区间提供可追溯时间戳。主计时口径为 ACTIVE_AGENT_ELAPSED（智能体有效工作经过时间），不再直接使用“结束墙钟 - 开始墙钟”。

用户离开、休息、现实事务造成的空档：
```text
HUMAN_IDLE=EXCLUDED
```

GPT、Codex 以及它们直接调用的执行工具正在解决该问题时：
```text
AGENT_ACTIVE=INCLUDED
```

失败诊断、回虚、修正、重跑只要智能体正在实际处理，仍全部计入；不得因为失败而重置累计时间。

若问题进入时没有可靠的精确时间戳：

```text
不得倒推或伪造。
START_TIME_CONFIDENCE=UNKNOWN
```

从第一次能够可靠建立时间锚的时点开始记录，并明确说明此前区间未被精确计量。


## 任务时间编号与有效工作区间

每个问题第一次进入时必须立即生成唯一编号：

```text
TASK_TIME_ID=ESTE-YYYYMMDD-NNN
```

每次 GPT、Codex 或其直接执行工具开始实际解决该问题时，记录：

```text
SEGMENT_ID=SNNN
AGENT=GPT|CODEX
ACTIVE_START_NETWORK_TIMESTAMP=<网络时间>
```

该段工作结束、等待用户下一次输入或任务交给另一智能体时，记录：

```text
ACTIVE_END_NETWORK_TIMESTAMP=<网络时间>
ACTIVE_DURATION=<结束-开始>
```

主锚定物：

```text
T_VALID_ACTIVE_GLOBAL
= 所有有效工作区间的时间并集
```

当前 GPT 与 Codex 串行工作时，近似等于：

```text
T_GPT_ACTIVE + T_CODEX_ACTIVE
```

若以后并行，重叠时间只计一次；各智能体各自累计时间保留作诊断，不得重复加入主锚。

GPT 只有在冻结的 FINAL_VALID_CONDITION 已满足并通过最终验收时，才允许写入：

```text
FINAL_VALID=YES
GLOBAL_TIMER_STATE=STOPPED
```

GPT 不得仅凭“看起来完成”自行提前停表。

## 局部时间：只用于瓶颈定位

允许同时记录：

```text
T_VIRTUAL
T_REAL
T_FETCH
T_RUNNER
T_VERIFY
T_FAILURE_DIAGNOSIS
T_REWORK
T_WAIT
T_HANDOFF
```

用途：

```text
定位瓶颈
比较局部方案
解释总 T_VALID 为什么变化
```

限制：

```text
LOCAL_TIMER_ROLE=DIAGNOSTIC_ONLY
LOCAL_TIMER_CANNOT_REPLACE_GLOBAL_T_VALID=YES
```

局部更快但导致总 T_VALID 更长的方案，判为整体更差。

## 时间检查点

每个具有决策意义的阶段结束后记录一次：

```text
CHECKPOINT_NAME=<阶段>
CHECKPOINT_TIMESTAMP=<时间>
ELAPSED_FROM_PROBLEM_ENTRY=<累计时间>
BOTTLENECK_IF_ANY=<瓶颈或 NONE>
```

检查点只提供可观测性，不创建新的优化目标。



# 整体闭环极限时间：禁止局部最快替代整体最快

唯一锚定物的中文正式名称：

```text
整体闭环极限时间
WHOLE_LOOP_VALID_ACTIVE_TIME
```

完整边界：

```text
GPT 接收问题
-> GPT 虚拟成熟并冻结
-> Codex 接手现实执行
-> Codex 调用 PowerShell/浏览器/本机工具取得现实证据
-> Codex 返回正式现实结果
-> GPT 重新读取并判断 TASK_COMPLETED
-> GPT 最终确认 FINAL_VALID
```

只有上面完整闭环完成，任务才有资格产生有效总时间。

```text
T_VALID_ACTIVE_GLOBAL
= measure(UNION(REQUIRED_LOOP_ACTIVE_INTERVALS))

T*
= min(T_VALID_ACTIVE_GLOBAL)
subject to TASK_COMPLETED=TRUE
```

## Codex 执行器不可被局部优化删除

当前自动化架构固定：

```text
REASONING_BRAIN=GPT
EXECUTOR=CODEX
DETERMINISTIC_TOOL=PowerShell/Browser/Local Tools
FINAL_JUDGE=GPT
```

PowerShell 是 Codex 可调用的确定性工具，不是完整闭环执行器的替代物。

只有当整个任务合同明确不需要 Codex 执行/证据回传时，才允许省略 Codex；对于本技能默认自动化闭环：

```text
CODEX_EXECUTOR_REQUIRED=YES
```

因此不得因为：

```text
PowerShell 局部执行更快
```

就推导：

```text
删除 Codex
```

必须比较的是完整闭环的 T_VALID_ACTIVE_GLOBAL。

## Codex 时间接力

GPT -> Codex 交接时必须由命令外壳记录：

```text
CODEX_HANDOFF_START_TIMESTAMP
CODEX_PROCESS_ACTIVE_MS
CODEX_PROCESS_END_TIMESTAMP
```

计时覆盖整个 `codex exec` 进程，包括模型启动、推理、工具调用、现实执行和结果输出。

Codex 结束后，结果回到 GPT；GPT 的重新读取与最终裁决继续计入同一 TASK_TIME_ID，不重置。

# 两步状态机：唯一结构

方法层级永远只有两个步骤：

```text
1. 虚
2. 实
```

任何检索、组合、冻结、闭环检查、时间检查点、失败分类、产物固定，全部只是“虚”的内部动作或日志，不得编号为 V1/V2/V3，也不得成为新的方法步骤。

任何现实执行、验收、Reality Delta 记录，全部只是“实”的内部动作或日志，不得编号为 R1/R2/R3，也不得成为新的方法步骤。

唯一允许的状态转换：

```text
VIRTUAL -> REAL
REAL PASS -> FINAL
REAL FAIL -> VIRTUAL
```

失败返回虚时，方法仍然只有两步，累计有效时间不重置。

# 虚

```text
【页面名｜任务名｜序号｜虚】
```

虚的目标不是“做出一个能跑的方案”，而是：

```text
在当前现实底座下，
冻结预测总 T_VALID 最短的有效方案。
```

## 虚开始时必须先声明时间锚

每次问题进入虚阶段，先固定：

```text
PROBLEM_ENTRY=<时间点或可追溯事件>
FINAL_VALID_CONDITION=<什么才算问题真正解决>
TIME_ANCHOR=T_VALID
OBJECTIVE=min(T_VALID)
```

如果无法回答 FINAL_VALID_CONDITION，则问题边界未定义，禁止优化局部时间。



## Codex 执行环境兼容性预检

只要“实”由 Codex 执行，虚冻结前必须把现实底座中的 Codex 约束注册表作为硬输入，并完成：

```text
CODEX_REALITY_CONSTRAINTS_LOADED=PASS
CODEX_POLICY_COMPATIBILITY=PASS
SHELL_INTERPOLATION_SAFE=PASS
EXECUTABLE_STAGING_SAFE=PASS
TIMING_PATH_SAFE=PASS
PROMPT_ROUNDTRIP_EQUIVALENCE=PASS
NO_KNOWN_CONSTRAINT_VIOLATION=PASS
```

含义：

- 已知会被安全策略拒绝的写入/覆盖路径，不得再次冻结。
- 含 PowerShell 代码的 GPT -> Codex 文本，必须使用 literal-safe（字面安全）传输；冻结前要检查关键 `$变量` 在交给 Codex 前后没有被调用方 Shell 展开或改写。
- 计时器必须在 Codex 进程外层启动并在进程结束后停止；主持续时间使用 `Stopwatch`，不得把权限敏感的时间源查询作为硬依赖。
- 如果某个动作的 Codex 安全策略兼容性未知，而且存在更安全等价路径，优先冻结更安全路径。
- 不允许为了绕过安全策略而设计规避路径；目标是选择本来就符合现实权限边界的成熟执行方式。

任一项不是 PASS：

```text
VIRTUAL_COMPLETE=NO
FREEZE=BLOCK
```

这仍然只是“虚”的内部硬门，不是第三步。

## 冻结闭环门

冻结不是“方案写完”，而是虚阶段最后一个验收动作。

现实执行链必须先展开为完整步骤图；每一个会在“实”中发生的步骤，在冻结前都必须满足：

```text
输入=已知或已冻结
动作=已定义
成功后置条件=已定义
失败差异=可分类
下一步=唯一
外部依赖=已证明或已有冻结兜底
产物=可定位且可校验
时间影响=已映射到总 T_VALID
```

任一步缺一项：

```text
FREEZE=BLOCK
VIRTUAL_COMPLETE=NO
```

尤其是 GitHub、模型 API、浏览器、账号、网络、文件、GPU、外部服务等：

```text
若外部依赖不是任务本身必须测量的对象：
    不得成为现实启动的单点硬依赖；
    必须在虚阶段预先物化/缓存/固定不可变标识，
    并冻结无需该外部服务也能启动的本地或内联兜底。

若外部依赖本身就是任务有效性的组成部分：
    必须把其可用性与失败分类写入有效门，
    不能当作默认成立的环境假设。
```

冻结前必须运行一次独立闭环验收：

```text
TIME_ANCHOR_DEFINED=PASS
FINAL_VALID_CONDITION_DEFINED=PASS
EXECUTION_CHAIN_CLOSED=PASS
EXTERNAL_DEPENDENCIES_CLOSED=PASS
IMMUTABLE_ARTIFACT_PINNED=PASS
CODEX_REALITY_CONSTRAINTS_LOADED=PASS
CODEX_POLICY_COMPATIBILITY=PASS
SHELL_INTERPOLATION_SAFE=PASS
EXECUTABLE_STAGING_SAFE=PASS
TIMING_PATH_SAFE=PASS
PROMPT_ROUNDTRIP_EQUIVALENCE=PASS
NO_KNOWN_CONSTRAINT_VIOLATION=PASS
FREEZE_CLOSURE_VERIFIER=PASS
```

全部 PASS 后才允许：

```text
FROZEN_SOLUTION=YES
```

## 虚完成条件

```text
现实底座=足够
总 T_VALID 边界=已定义
最终有效条件=已定义
有效门=通过
预测总 T_VALID=有
执行链闭合=通过
外部依赖闭合=通过
不可变产物=已固定
冻结闭环验收=通过
冻结方案=有
共同工作区发布=完成
实入口命令=已经生成并在虚结束时直接交付
```

### 虚 -> 实交接规则

交接不是第三步，而是“虚”的完成条件。

```text
VIRTUAL_COMPLETE=YES
iff
FROZEN_SOLUTION=YES
AND SHARED_WORKSPACE_PUBLISHED=PASS
AND REAL_ENTRY_COMMAND_READY=PASS
AND REAL_ENTRY_COMMAND_EMITTED=YES
```

现阶段默认最短交接：

```text
共同 GitHub 工作区保存不可变冻结执行文件
+
虚结束的同一条回复直接给唯一 Codex 执行命令
```

禁止把以下动作留给下一轮：

```text
另行下载桌面
再次询问如何执行
再次生成执行命令
手工搬运冻结文件
```

因为这些动作不提高有效性，只增加 T_VALID_ACTIVE_GLOBAL。

# 实

```text
【页面名｜任务名｜序号｜实】
```

严格执行冻结方案。

“实”的局部现实时间可以作为诊断数据记录，但不能重新起一只用于优化的主时钟。

主时钟始终是：

```text
PROBLEM_ENTRY
→ ...
→ FINAL_VALID_SOLUTION
```

现实阶段不得补设计、补依赖、补兜底；这些都属于虚阶段未完成。

如果现实失败：

```text
记录最小 Reality Delta
→ STOP
→ 回虚
→ 修正
→ 再冻结
→ 再实
```

但：

```text
主 T_VALID 继续累计
不得从第二次尝试重新计时
```

# 规则升级判据

发现一次错误后，不以“把当前错误修掉”为完成条件。

必须继续问：

```text
为什么原冻结/规则没有在更早处阻止它？
```

如果存在一个低成本、可复用的检查或闭环规则，且其预期避免的返工时间大于自身时间成本，则吸收为永久规则。

如果新增规则不能证明能缩短当前或未来问题总 T_VALID，则不加入。

# 收口

```text
答不出 PROBLEM_ENTRY -> 未开始正确计时
答不出 FINAL_VALID_CONDITION -> 未定义真正完成
失败/回退后重置主时钟 -> T_VALID 无效
只优化局部步骤时间 -> 不能证明极限短时间
新增规则不比较净总时间收益 -> 不允许加入
虚无闭合执行链/冻结闭环验收/冻结方案 -> 未完成
最终没有现实有效解决 -> T_VALID 未完成
```

只有“虚/实”，无第三步。

唯一标准始终只有一个：

```text
T*=min(
  从问题进入
  到问题最终有效解决
  的全部端到端时间
)
```
