# Reality Contract｜极限短时间自动化闭环 v2.0

```ini
STATUS=WORKING_BASELINE_R4
STATE=10
PURPOSE=以最短完整T_VALID完成现实目标，不把流程本身当目标
MATURE_CAPABILITY_FIRST=TRUE
MINIMAL_NECESSARY_IMPLEMENTATION_ALLOWED=TRUE
OBJECTIVE=T*=min(T_VALID)

PRIMARY_BRAIN_CANDIDATE=GPT
BRAIN_REPLACEABLE_BY_REALITY=TRUE
EXISTING_PAID_CAPACITY_ALLOWED=YES
NEW_INCREMENTAL_PAID_DEPENDENCY=FORBIDDEN_BY_DEFAULT

CODEX_ROLE=STRONG_EXECUTOR_CANDIDATE
CODEX_STATUS=OPTIONAL_NOT_FIXED
BACKUP_PATH_REQUIRED=YES
```

## A. 用户现实入口

用户只需要用自然语言给出最终现实目标。

用户只在真正不可替代场景介入，例如：
- 个人目标 / 价值判断；
- 只有本人知道且无法从授权来源获得的信息；
- 登录 / MFA / 验证码；
- 新增费用、付款、购买；
- 账号安全设置变化；
- 删除重要数据或不可逆高风险动作；
- 现实平台强制要求用户本人接管。

普通路径选择、执行器选择、故障恢复、结果路由、换页、继续、常规验收不应默认要求用户做人肉消息总线。

## B. 当前主脑候选｜GPT

```ini
PRIMARY_BRAIN_CANDIDATE=GPT
```

GPT 当前适合承担：
- 理解最终目标；
- 全维度观察、搜索、组合判断；
- 定义 / 更新 Reality Contract；
- 选择当前最合适的成熟工具；
- 在失败时重新归因和选路；
- 判断 FINAL_VALID；
- 控制整体 `T*=min(T_VALID)`。

这是当前最强主路线候选，不是宪法级不可替代真理。Reality 若证明其他组合完整 T_VALID 更短，可以调整。

## C. 工具与执行层

候选包括但不限于：
- Desktop Commander Remote；
- GitHub Windows self-hosted runner；
- Codex；
- Reasonix；
- Browser / Playwright；
- API / MCP / CLI；
- n8n / OpenClaw；
- 专用模型与其他成熟执行器；
- 为解决明确根因所需的最小必要脚本或胶水。

原则：

```text
能直接完成 → 直接完成
直接工具不够 → 调最合适的成熟执行器
仍不满足 VALID → 最小必要实现
所有候选 → 用完整 T_VALID 复验
```

Codex 是强工程执行器，不是唯一执行器。

## D. 自动化不是目的

自动化只有在改善现实结果时才保留。

如果某个不可替代人工动作比建立复杂自动化更快，它可以进入本轮 VALID 路径；但可机器并行、可重复的大量任务应优先消除人工串行瓶颈。

不为“看起来自动化”增加层级。

## E. 长流程连续性

必须解决：
- 页面卡顿 / 无响应；
- 上下文过长；
- 长任务中途停止；
- 网络 / 工具暂时掉线；
- 新页面恢复当前任务。

目标结构：

```text
工作会话
→ Checkpoint
→ 权威项目状态
→ 新会话/恢复实例
→ 继续
```

页面不是唯一事实库。

## F. 独立备份路径

```ini
BACKUP_PATH_REQUIRED=YES
PRIMARY_DEPENDENCY=GPT
BACKUP_MUST_NOT_DEPEND_ON_GPT_AND_CODEX_BOTH_BEING_HEALTHY=TRUE
```

GPT 服务、登录、配额或会话故障时，必须有一条成熟独立路线可以继续关键工作。

备份可以比主路慢，但必须能达到相同现实 VALID。

## G. FINAL_VALID

必须同时满足：
1. 现实结果真实存在；
2. 满足用户最终目标；
3. 能机器验收的事实已经自动验证；
4. 执行器自报 Done 不能单独构成完成；
5. 除不可替代的人类动作外，不需要用户做人肉消息总线；
6. 长任务可恢复；
7. 所有失败、等待、恢复、重试计入同一现实时间轴。

## H. 时间合同

```ini
FLOW_START=系统已拥有足够信息、可以不再等待用户澄清而开始现实推进的时间点
T_FLOW=从 FLOW_START 到当前全部现实时间
T_VALID=仅 FINAL_VALID 后产生
OBJECTIVE=T*=min(T_VALID)
```

## I. Reality 比较

正式比较至少记录：

```text
T_VALID_PRIMARY
T_VALID_GPT_CODEX
T_VALID_MULTI_AGENT
T_VALID_BACKUP
```

只有 FINAL_VALID 的路线才进入时间比较。

其他指标用于解释瓶颈，不与 T_VALID 并列为目标。

> 本合同是 STATE=10 工作基线，不等于项目 Freeze。
