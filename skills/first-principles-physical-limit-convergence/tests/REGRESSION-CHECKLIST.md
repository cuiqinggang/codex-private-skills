# v1.9.0 回归检查

## 母技能身份

- [x] 当前技能ID正确。
- [x] 当前版本为 v1.9.0。
- [x] 当前分支与版本一致。
- [x] 历史祖先技能没有被误改。

## 四步法

- [x] 第1步只发布一个端到端物理极限。
- [x] 第2步建立本机现实最优区间。
- [x] 第3步由 GPT 完成成熟方案矩阵与虚拟99攻击迭代。
- [x] 第4步由 GPT 生成完整 Codex 命令包。
- [x] Codex 按完整命令包执行到底。

## 禁止循环

- [x] 禁止自由探索（NO_FREE_EXPLORATION）= YES。
- [x] Codex 不得新增候选。
- [x] Codex 不得改变候选顺序。
- [x] Codex 不得追加运行。
- [x] Codex 不得自行性能剖析或参数搜索。
- [x] 正常通过/失败/回滚不要求每一步返回 GPT。
- [x] 真实执行层不形成 V1→Vn 式重规划循环。
- [x] 虚拟攻击迭代只发生在 GPT 层。

## 有限执行灵活性

- [x] 允许等价命令写法、脚本封装、路径修正和既定任务恢复。
- [x] 上述灵活性只作用于“怎么执行同一个动作”。
- [x] Codex 不得改变“执行什么任务”。
- [x] Codex 不得借执行问题换模型、候选、版本、参数、运行次数、顺序、阈值或测试范围。
- [x] 既定步骤无法在允许边界内完成时，保存证据并停止返回 GPT。

## 新优化方向

- [x] 命令包外的新研究方向不插回当前主流程。
- [x] 新研究方向记录为“独立99路径”。
- [x] 独立99路径以后单独走同样四步法。

## 99与收口

- [x] Final Certification（最终认证）保留。
- [x] Remote Verify（远端核验）保留。
- [x] 质量、稳定、安全硬约束保留。

```text
METHOD_LOGIC_ACCEPTANCE=PASS
SIMPLE_FOUR_STEP_METHOD=PASS
BOUNDED_EXECUTION_FLEXIBILITY=PASS
PLAN_MUTATION_BY_CODEX=NO
NO_REAL_EXECUTION_REPLAN_LOOP=PASS
INDEPENDENT_99_PATH_RULE=PASS
RUNTIME_INSTALLATION=NOT_EXECUTED
H3_FINAL_99=NO
```
