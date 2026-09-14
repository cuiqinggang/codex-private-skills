# 第一性原理四列法 V4.0 工作表

## 固定任务合同

| 字段 | 记录 |
|---|---|
| TASK 名称与版本 | |
| 输入与输出 | |
| 成功条件 | |
| 必须保留的能力 | |
| 不可删除步骤 | |
| 安全/稳定性/质量底线 | |
| 计时起点/终点 | |
| 冷启动/热启动条件 | |
| 任何变更任务合同的结果 | `INVALID_RESULT` |

## 四列表

| 1. CURRENT | 2. EXTERNAL FRONTIER | 3. FIRST-PRINCIPLES PHYSICAL TIME | 4. ITERATIVE CONVERGENCE |
|---|---|---|---|
| `T_CURRENT`、分段时间、运行条件、次数、证据 | `T_EXTERNAL`、来源、合同/硬件/软件、可比性、可复制部分 | `T_PHY` 或 `T_PHY_RANGE`、不可避免步骤、计算式、假设、不确定性、物理瓶颈 | 当前最大损失、单一局部假设、最小改动、实测前后、保留/回滚、下一步 |

## CURRENT 分段计时

| 阶段 | 起点 | 终点 | 时间 | 证据 | 状态 |
|---|---|---|---:|---|---|
| 启动/加载/计算/传输/保存/验证/返回 | | | | | `VERIFIED / UNVERIFIED` |

`T_CURRENT =`<br>
重复次数与中位数/P95：<br>
计时噪声与环境：

## EXTERNAL FRONTIER 可比性

| 来源 | `T_EXTERNAL` | TASK 相同 | 硬件可比 | 软件/参数可比 | 证据 | 可复制部分 | 结论 |
|---|---:|---|---|---|---|---|---|
| | | | | | | | `COMPARABLE / PARTIAL / NOT_COMPARABLE / UNVERIFIED` |

若存在显著更快且真正可比的外部结果，99 门禁默认失败。

## T_PHY 推导

| 不可避免步骤/资源 | 数据量或工作量 | 可用上限 | 理论时间 | 可并行性 | 证据/假设 |
|---|---:|---:|---:|---|---|
| | | | | | `VERIFIED / INFERRED / UNVERIFIED` |

关键路径：<br>
`T_PHY_RANGE = [____, ____]`<br>
当前采用 `T_PHY =`（若可确定）：<br>
不确定性：

## 迭代日志

| 轮次 | 最大时间损失 | 局部假设 | 最小改动 | 改前 | 改后 | TASK 保持 | 结论 | 回滚点 |
|---|---|---|---|---:|---:|---|---|---|
| 01 | | | | | | `YES/NO` | `KEEP / ROLLBACK / UNVERIFIED` | |

仅当 `TASK 保持=YES` 时，时间改善才有效。

## 新增能力 ΔT

| 阶段 | 冻结基线 | 新能力 | 合理 `ΔT` 范围 | 实际 `ΔT` | 解释成立 | 结论 |
|---|---|---|---:|---:|---|---|
| Stage N+1 | Stage N = 99 | | | | `YES/NO` | `ACCEPT / PATH_ARCHITECTURE_ERROR / UNVERIFIED` |

若实际新增时间出现数量级退化，检查工作流路径、offload、模型加载、重复执行、参数、前置技能和成熟路线；不得直接接受为新 baseline。

## 99 分与冻结

| 门禁 | 结果 | 证据 |
|---|---|---|
| TASK 全部保持 | | |
| 已系统测量主要时间段 | | |
| 已调查可比外部前沿 | | |
| 已形成可审计 `T_PHY`/范围 | | |
| 已测试显著、可行、低风险候选 | | |
| 无已知可比巨大收益被忽略 | | |
| 继续修改仅剩不显著或不稳定收益 | | |
| 冻结版本可复现、可恢复 | | |

`T_99 =`<br>
`PHYSICAL_GAP = T_99 - T_PHY =`<br>
结论：`99_FROZEN / NOT_CONVERGED / INVALID_RESULT / BLOCKED`<br>
重新打开条件：

## 失败复盘入口

失败时记录失败对象、阶段、预期/实际时间、是否保持 TASK、直接证据、是否为 `PATH_ARCHITECTURE_ERROR`、回滚结果、冻结基线是否完整、下一项最小取证。需要局部故障归因时可使用旧版五类标签：`MISSING / EXISTING_BUT_BYPASSED / FALSE_POSITIVE / EXTERNAL_FAILURE / UNVERIFIED`，但不要把它们误写成 V4.0 四列。
