# Reality Contract｜极限短时间自动化闭环 v2.0

```ini
STATUS=WORKING_BASELINE_R3_EXISTING_PAID_CORE
STATE=10
PURPOSE=定义现实必须发生什么，并允许充分使用已经付费拥有的成熟能力
MATURE_SOLUTION_EXISTS=TRUE
NO_NEW_IMPLEMENTATION_ESCAPE=TRUE
OBJECTIVE=T*=min(T_VALID)

CORE_BRAIN=GPT
CORE_BRAIN_STATUS=FIXED_PRIMARY
EXISTING_PAID_CAPACITY_ALLOWED=YES
NEW_INCREMENTAL_PAID_DEPENDENCY=FORBIDDEN_BY_DEFAULT

CODEX_ROLE=MATURE_EXECUTOR_CANDIDATE
CODEX_STATUS=OPTIONAL_NOT_FIXED
BACKUP_PATH_REQUIRED=YES

MANUS_2_ROLE=BENCHMARK_ONLY
MANUS_2_PRODUCTION=NO
MANUS_2_USE_EXISTING_CREDITS_ONLY=YES
```

## A. 用户现实入口

用户只需要用自然语言给出最终现实目标。

用户只在以下真正不可替代场景介入：
- 个人目标 / 价值判断；
- 只有本人知道且无法从授权来源获得的信息；
- 登录 / MFA / 验证码；
- 新增费用、付款、购买；
- 账号安全设置变化；
- 删除重要数据或不可逆高风险动作；
- 现实平台强制要求用户本人接管。

普通路径选择、执行器选择、故障恢复、结果路由、换页、继续、常规验收不得默认要求用户介入。

## B. 固定核心｜GPT 超级大脑

当前正式主链固定：

```ini
CORE_BRAIN=GPT
```

原因不是沉没成本，而是当前项目本身就是以最高等级智能分析、Reality 理解、成熟方案检索、组合、纠偏和验收为核心。用户已经拥有该能力，因此应充分使用。

GPT 负责：
- 理解最终目标；
- 定义 / 更新 Reality Contract；
- 检索和比较世界成熟解；
- 决定调用哪些成熟能力；
- 在失败时重新归因和选路；
- 判断什么才是真正 FINAL_VALID；
- 控制整体 `T*=min(T_VALID)`。

具体执行器不是核心身份，可以替换。

## C. 执行层｜Codex 是强候选，不是固定真理

Codex 当前作为最强成熟执行候选之一进入竞争：

```ini
CODEX_ROLE=MATURE_EXECUTOR_CANDIDATE
CODEX_STATUS=OPTIONAL
```

可承担：
- 编码；
- 文件与仓库操作；
- 长流程工程执行；
- 测试与现实产物生成；
- 与 GitHub / 本地开发环境的成熟执行。

但 Codex 不因“已经付费”自动永久保留。

如果现实证据证明其他成熟执行方式：
- 更快；
- 更稳定；
- 更少人工；
- 更低额外资源消耗；
- 完整 `T_VALID` 更短；

则可以替换 Codex 的对应职责。

原则：

> GPT 核心固定；Codex 是可替换执行器。

## D. 已付费能力与新增付费能力的边界

允许充分使用：
- 用户已经付费拥有的 GPT 能力；
- 用户已经付费拥有并可用的 Codex 能力；
- 已经拥有的本机硬件；
- 现有成熟技能和服务；
- 已有额度 / 已有积分用于明确 Benchmark。

默认不新增：
- 为本项目新买的长期订阅；
- 新增持续 credits 依赖；
- 已有成熟方案可以完成却额外引入的收费平台。

只有出现明确商业 ROI，且用户明确重新打开成本门时，新的收费能力才进入生产候选。

因此本项目不是 FREE-FIRST，而是：

```text
EXISTING_CAPABILITY_FIRST
+
NO_NEW_RECURRING_COST_BY_DEFAULT
```

## E. Manus 2.0 的唯一角色

```ini
MANUS_2_ROLE=PAID_MATURE_REFERENCE
PRODUCTION_CANDIDATE=NO
USE_EXISTING_CREDITS_ONLY=YES
```

Manus 2.0 用于得到成熟完整产品的现实参考：

```text
T_REF_MANUS
```

作用：
- 提供成熟整解现实基准；
- 看 GPT 主链距离成熟产品还有多少完整 T_VALID 差距；
- 帮助定位最值得继续攻击的瓶颈。

即使 Manus 更快，也不自动进入未来正式主链。

## F. 正式主链的最小抽象

```text
用户目标
→ GPT 超级大脑
→ 选择成熟执行路径
→ 执行
→ 自动回传现实结果
→ GPT / 独立成熟验证
→ FINAL_VALID
```

执行路径候选包括但不限于：
- Codex；
- 成熟 Browser；
- GitHub；
- n8n；
- OpenClaw；
- API / MCP / CLI；
- 本地成熟自动化；
- 未来出现的更成熟执行器。

只有当前任务实际需要的能力才加入本轮运行路径。

## G. 必须消除的人肉胶水

| 人工动作 | v2.0 要求 |
|---|---|
| GPT 方案手工复制给 Codex / 其他执行器 | 自动交接 |
| 执行结果人工搬回 GPT | 自动回传 |
| 页面卡住后用户恢复上下文 | 自动恢复 |
| 长任务反复提醒“继续” | 自动推进 |
| 普通错误后用户判断重试 / 换路 | 自动恢复 / 重选成熟路径 |
| 手工盯是否完成 | 自动监控 |
| 机器可验事实让用户验收 | 自动验收 |
| 手工保存阶段状态 | 自动持久化 |

## H. 独立备份路径

正式生产必须有一条独立备份：

```ini
BACKUP_PATH_REQUIRED=YES
PRIMARY_DEPENDENCY=GPT
PRIMARY_EXECUTOR_CANDIDATE=Codex
BACKUP_MUST_NOT_DEPEND_ON_GPT_AND_CODEX_BOTH_BEING_HEALTHY=TRUE
```

备份目的不是日常并行运行，而是：
- GPT 服务异常；
- Codex 服务异常；
- 登录 / 配额 /会话故障；
- 单一供应商不可用；
- 主链发生结构性故障。

备份也只能由成熟现成能力组成，不开发新的备份框架。

备份候选后续单独 Reality 竞争；当前不让它干扰主链收敛。

## I. FINAL_VALID

必须同时满足：
1. 现实结果真实存在；
2. 满足用户最终目标；
3. 能机器验收的事实已经自动验证；
4. 执行器自报 Done 不能单独构成完成；
5. 除不可替代的人类动作外，不需要用户做人肉消息总线；
6. 长任务可恢复；
7. 所有失败、等待、恢复、重试计入同一现实时间轴。

## J. 时间合同

```ini
FLOW_START=系统已拥有足够信息、可以不再等待用户澄清而开始现实推进的时间点
T_FLOW=从 FLOW_START 到当前全部现实时间
T_VALID=仅 FINAL_VALID 后产生
OBJECTIVE=T*=min(T_VALID)
```

## K. 当前要测的三个值

### 主链
```text
T_VALID_PRIMARY
= GPT + 当前最佳成熟执行路径
```

### 成熟付费参考
```text
T_REF_MANUS
= Manus 2.0 对同一 Reality 的端到端有效时间
```

### 备份路径
```text
T_VALID_BACKUP
= 独立成熟备份对同一或等价恢复任务的有效时间
```

最终正式优化目标仍只有：
`T*=min(T_VALID)`

其他值只是现实比较与瓶颈定位依据。

> 本合同是 STATE=10 工作基线，不等于项目 Freeze。
