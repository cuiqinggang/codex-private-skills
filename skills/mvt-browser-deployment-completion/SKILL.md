---
name: mvt-browser-deployment-completion
description: MVT 浏览器部署完整性与现实竞争总装技能 v1.0.0-rc1。用于在浏览器候选路线已经完成设计冻结、程序化冻结和虚拟测试之后，把“候选组件”总装成真正可直接现实运行的竞争系统。专门防止出现组件 PASS 但 run config、matrix binding、状态机、T_VALID 记录、结果流水线、能力矩阵或恢复绑定缺失的假性可执行冻结。所有方案设计与虚拟成熟由 GPT 页面完成；Codex/Reasonix/本地执行器只执行冻结总装命令、校验、现实运行和回传，不得自行修复或重新设计。
metadata:
  version: "1.0.0-rc1"
  parent_method: "first-principles-physical-limit-convergence@3.1.5"
  core_zh: "高智能虚拟成熟"
---

# MVT 浏览器部署完整性与现实竞争总装技能 v1.0.0-rc1

## 1. 定位

本技能不是新的浏览器，也不是第四核心。

它只属于：

**高智能虚拟成熟**

用途：当浏览器路线已经“设计成熟 + 组件可执行”，但现实验证暴露“总装没有接通”时，把所有现实运行必需接口在 GPT 冻结方案下补齐并做 Virtual-99，直到执行器真正只剩 RUN。

## 2. 触发条件

出现以下任一现象即触发本技能：

- 候选 package PASS，但真实 attempt = 0；
- harness 存在，但没有 route/matrix binding；
- cold/warm/reconnect 只有文字定义，没有可执行状态机；
- T_VALID 起止口径已定义，但没有统一 recorder；
- raw result / summary / winner pipeline 没接通；
- capability list 存在，但没有 case -> runner -> verifier 机器绑定；
- recovery contract 存在，但故障注入/恢复执行没有绑定。

## 3. 本次来源 Reality Delta

本技能第一版直接固化 2026-09-20 MVT Browser Automation 现实验证暴露的七个缺口：

- D001 FROZEN_REAL_RUN_CONFIG_INCOMPLETE
- D002 FROZEN_HARNESS_MATRIX_BINDING_MISSING
- D003 COLD_WARM_RECONNECT_SEMANTICS_NOT_EXECUTABLE
- D004 T_VALID_FULL_RECORD_CONTRACT_NOT_IMPLEMENTED
- D005 REQUIRED_RESULT_PIPELINE_MISSING
- D006 FROZEN_CAPABILITY_MATRIX_MISSING
- D007 RECOVERY_EXECUTION_NOT_BOUND

这些不是七条新路线，而是同一个“现实竞争总装完整性”问题的七个必须门。

## 4. 七个部署完整性门

### 门 1：现实运行配置

必须生成唯一 run-config，锁定：
- frozen source commit
- F1/F2/F3 package roots
- harness root
- output root
- task matrix
- run conditions
- repeat counts
- timing contract
- result contract
- mutation policy

### 门 2：矩阵到执行器绑定

每一个：
task family + case + condition + route

必须能唯一解析到：
- exact runner
- exact verifier
- exact fixture/workflow
- exact args/input
- exact output target

0 个匹配或 >1 个匹配都 BLOCK。
执行器不得猜。

### 门 3：COLD/WARM/RECONNECT 状态机

三种状态必须变成机器事件序列，而不是说明文字。

COLD：
task accepted -> browser absent asserted -> timer start -> launch -> run -> independent valid -> timer stop -> teardown

WARM：
ready state asserted -> task accepted -> timer start -> run -> independent valid -> timer stop -> restore next initial state outside current attempt

RECONNECT：
browser alive asserted -> controller disconnected -> task accepted -> timer start -> reconnect -> run -> independent valid -> timer stop

禁止把预热冒充 COLD。

### 门 4：统一 T_VALID_FULL 记录器

所有路线必须输出同一 schema：
- start_monotonic
- end_monotonic
- t_valid_full_ms
- condition
- route_id
- case_id
- attempt_index
- component_times
- valid
- verifier_result
- model/jev/open-agent counts
- error
- artifacts

T_VALID_FULL = end_monotonic - start_monotonic。
任何路线不得自己改边界。

### 门 5：结果流水线

唯一流水线：

runner result
-> independent verifier
-> normalized attempt record
-> append-only JSONL
-> statistics
-> provisional winner selector
-> hashes

失败 attempt 不得删除。

### 门 6：能力矩阵

每个能力必须有：
case_id -> route eligibility -> fixture/site -> request -> expected -> verifier -> repeat count

没有完整绑定的能力只能 UNKNOWN，不能声称 COMPLETE。

### 门 7：恢复绑定

每个冻结故障：
SESSION_LOST / STALE_STATE / TARGET_CHANGED / BROWSER_CRASH / NETWORK_INTERRUPTION / CONTRACT_DRIFT

必须绑定：
fault injector -> recovery runner -> verifier -> result record

正常路径 recovery overhead 必须为 0。

## 5. 总装通过定义

只有七个门全部 PASS，才允许：

DEPLOYMENT_COMPLETENESS=PASS
REALITY_COMPETITION_READY=YES

其中任何一门失败：

DEPLOYMENT_COMPLETENESS=BLOCKED
ACTION=STOP
RETURN_TO_GPT=YES

Codex 不得自行修。

## 6. 执行器权限

Codex/Reasonix/本地执行器只允许：

读取冻结源
-> 按冻结命令生成总装配置/绑定文件
-> 运行无真实浏览器/无真实模型的结构验证和模拟
-> 回读
-> hash
-> 回传
-> STOP

不得：
- 改 F1/F2/F3；
- 新增路线；
- 设计新的 fallback；
- 改 VALID；
- 改计时边界；
- 改 winner rule；
- 遇到失败后自己修。

## 7. 现实运行前置门

现实竞争命令只有在下列状态存在时才可执行：

DEPLOYMENT_COMPLETENESS=PASS
RUN_CONFIG=PASS
MATRIX_BINDING=PASS
CONDITION_STATE_MACHINE=PASS
TVALID_RECORDER=PASS
RESULT_PIPELINE=PASS
CAPABILITY_MATRIX=PASS
RECOVERY_BINDING=PASS
VIRTUAL_99=PASS

否则现实浏览器运行数必须为 0。

## 8. 经验固化

以后看到：
“组件测试都 PASS，所以现实测试一定可执行”

必须判为错误推论。

正确推论是：

组件成熟
+ 总装完整性七门 PASS
+ Virtual-99
= 才允许现实竞争。

## 9. 最终一句话

> GPT 必须把浏览器现实竞争系统做到“执行器无需补任何 glue code 就能 RUN”；否则还没有完成高智能虚拟成熟。
