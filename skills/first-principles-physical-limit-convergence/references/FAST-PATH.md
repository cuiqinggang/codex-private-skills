# 最短执行路径 — v1.9.0

英文：`FAST PATH（最短路径）`

## 先确认身份

```text
技能ID = first-principles-physical-limit-convergence
版本 = 1.9.0
正式分支 = codex/first-principles-physical-limit-convergence-v1.9.0
```

## 第1步：物理极限

```text
固定任务
+ 当前硬件边界
→ T_PHY_TOTAL_REFERENCE（端到端物理极限参照）
```

只保留一个正式物理极限数字或区间。

## 第2步：本机现实最优区间

```text
历史真实数据
+ MRE（最小真实执行）
+ 本机硬件/软件/模型约束
→ REAL_STATE_OPTIMUM_RANGE（本机现实最优区间）
```

## 第3步：GPT虚拟99

```text
成熟方案矩阵
→ 多方案虚拟吸收
→ 处理重叠收益和冲突
→ 反复虚拟攻击剩余差距
→ 达到停止点
→ VIRTUAL_99_FINAL_PLAN（虚拟99最终方案）
```

**循环只放在这里。**

## 第4步：Codex完整执行命令包

```text
读取完整命令包
→ 按顺序执行全部既定候选
→ 按规则保留/回滚
→ 完成最终认证
→ Git提交/推送
→ 远端核验
→ 停止并返回GPT
```

正常的通过、失败、回滚不需要每一步返回 GPT。

## Codex 灵活性的唯一边界

```text
执行形式可以等价调整 = YES
方案内容自行调整 = NO
```

允许：换等价命令写法、改为独立 `.ps1`、使用等价路径、按既定规则恢复同一个任务。

禁止：换模型、换版本、换候选、改参数、改 seed（种子）、加运行、改阈值、开性能剖析、增加研究路线。

如果既定动作不能在这个边界内完成：

```text
保存证据 → 安全停止 → 返回GPT
```

## 禁止

```text
Codex自行加候选 = NO
Codex自行改顺序 = NO
Codex自行加运行 = NO
Codex自行profile（性能剖析） = NO
真实执行层V1→Vn式循环 = NO
```

## 新发现的路线

如果当前主流程之外又发现明显有价值的新方向：

```text
记录为独立99路径
→ 当前主流程照常收口
→ 以后单独再走四步法
```

不要把新路线重新插入当前流程。

## 最后

```text
Final Certification（最终认证）通过
+ Remote Verify（远端核验）通过
→ 99 / Freeze（99分 / 冻结）
```