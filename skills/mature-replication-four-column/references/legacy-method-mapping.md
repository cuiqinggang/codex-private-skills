# 旧版成熟复刻四列法 → V4.0 兼容映射

V4.0 更换了终极参照系，但保留旧版在修复成熟系统时的局部证据纪律。

| 旧版概念 | V4.0 位置 | 处理 |
|---|---|---|
| 当前成熟能力 | `CURRENT` 与上一阶段 `FROZEN MATURE BASELINE` | 保留为真实起点，不再作为终极参照 |
| 实际缺口 | `T_CURRENT - T_EXTERNAL`、`T_CURRENT - T_PHY` 或分段时间损失 | 必须量化为时间差并保持 TASK |
| 缺口原因 | `ITERATIVE CONVERGENCE` 中的诊断 | 五类标签仍可辅助局部归因 |
| 复用的成熟解决方案 | `EXTERNAL FRONTIER` 提供的可复制路径 | 先验证可比性，只复制有效部分 |

旧版标签 `MISSING / EXISTING_BUT_BYPASSED / FALSE_POSITIVE / EXTERNAL_FAILURE / UNVERIFIED` 继续用于解释局部异常，但不再占据 V4.0 的四列结构。

兼容原则：恢复正式入口、控制最小变更、保留健康模块、使用原失败对象复测和区分证据状态仍然有效。若这些原则与固定 TASK 或真实计时发生冲突，以 V4.0 的固定任务合同和 `T_PHY` 参照为准。
