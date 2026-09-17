---
name: first-principles-physical-limit-convergence
description: 第一性原理物理极限收敛引擎。固定任务后，先计算唯一端到端物理极限，再根据本机真实运行状态计算现实最优区间；随后由GPT收集成熟方案并一次性完成虚拟99攻击迭代，最后生成完整Codex实测命令包并让Codex按包完整执行。禁止执行过程中逐步重新设计、反复回GPT或形成V1→Vn式探索循环。后来发现的新优化路线若确有价值，作为独立99路径单独执行，不插回当前主流程。
metadata:
  version: "1.9.0"
  short-description: 第一性原理物理极限收敛引擎·简洁四步执行版
  lineage: first-principles-physical-limit-convergence@1.8.0 <- @1.7.0 <- @1.6.0 <- @1.5.0 <- @1.4.0 <- @1.3.0 <- @1.2.0 <- @1.1.0 <- @1.0.0
---

# 第一性原理物理极限收敛引擎 v1.9.0

> 核心目标：**简单、完整、一次规划、一次执行、最后收口。**

---

# 一、最高规则

## 1. 当前母技能身份

```text
技能ID（SKILL_ID）= first-principles-physical-limit-convergence
中文名 = 第一性原理物理极限收敛引擎
版本（VERSION）= 1.9.0
正式分支（CANONICAL_BRANCH）= codex/first-principles-physical-limit-convergence-v1.9.0
```

历史 `absolute-time-fireworks-optimization` 只是祖先技能，不是当前母技能。

## 2. 禁止自由探索

```text
禁止自由探索（NO_FREE_EXPLORATION）= YES
Codex角色（CODEX_ROLE）= 确定性执行器 / 验证器
```

Codex 不允许自行：

- 增加新候选；
- 改候选顺序；
- 自己设计新实验；
- 自动追加运行次数；
- 自己开启 profiler（性能剖析）、kernel trace（内核追踪）、参数搜索、版本搜索；
- 从一次结果继续发明下一次实验。

但这条规则**不等于每一步都必须返回 GPT**。

只要 GPT 已经把完整命令包设计好，Codex 就应按命令包从头到尾执行完。

---

# 二、整个方法只保留四步

```text
第1步：物理极限
第2步：本机现实最优区间
第3步：GPT虚拟99攻击迭代
第4步：Codex完整实测命令包
```

除此之外，不在主流程继续增加新层级。

---

# 第1步：第一性原理物理极限

固定任务合同：

```text
任务（TASK）
完成条件（TASK_COMPLETED）
正确性（CORRECTNESS）
质量（QUALITY）
稳定性（STABILITY）
安全性（SAFETY）
计时边界（TIMING_BOUNDARY）
当前真实硬件边界（ACTIVE_HARDWARE_BOUNDARY）
```

最终只发布一个正式物理极限：

```text
端到端物理极限（T_PHY_TOTAL_REFERENCE）
= 一个数字或一个区间
```

Generation（生成）、Path（路径）、I/O（输入输出）、load（加载）、decode（解码）等可以内部计算，但不作为并列正式极限。

物理极限是终极参照，不等于机器当前能达到的速度，也不等于99分门槛。

---

# 第2步：本机现实最优区间

复杂任务先做一次 MRE（Minimal Real Execution，最小真实执行），取得真实机器状态。

读取：

- 已验证历史基线；
- P50 / P95；
- KEEP（保留）/ ROLLBACK（回滚）历史；
- GPU / VRAM / RAM；
- 模型大小；
- 实际驻留、加载、卸载；
- 真实生成时间与路径时间；
- 已验证成功与失败机制；
- 当前软件与硬件约束。

然后计算：

```text
本机现实最优区间（REAL_STATE_OPTIMUM_RANGE）
```

它表示：

> 在当前这台机器、当前任务、当前已知成熟技术和真实约束下，合理预计能够逼近的现实稳定时间区间。

它不是第二块物理极限板，只是第3步虚拟攻击的现实目标带。

第1步与第2步完成后，就得到两个核心数据：

```text
1）物理终极参照 = T_PHY_TOTAL_REFERENCE
2）本机现实目标 = REAL_STATE_OPTIMUM_RANGE
```

---

# 第3步：GPT完整虚拟99攻击迭代

这一阶段是整个方法真正的“循环”所在。

**循环只能发生在 GPT 虚拟层，不应发生在 Codex 实测层。**

## 3.1 成熟方案矩阵

先收集多个优秀成熟方案，不只选一个。

每个方案至少判断：

```text
来源（SOURCE）
硬件匹配（HARDWARE_MATCH）
任务匹配（TASK_MATCH）
作用机制（MECHANISM）
攻击时间块（TARGET_BLOCK）
预计收益（EXPECTED_GAIN）
质量风险（QUALITY_RISK）
稳定风险（STABILITY_RISK）
集成成本（INTEGRATION_COST）
是否可逆（REVERSIBLE）
```

不同成熟方案可以攻击不同部分，因此允许组合吸收。

## 3.2 虚拟攻击迭代

从当前真实态出发：

```text
当前真实状态
→ 成熟方案1虚拟吸收
→ 成熟方案2虚拟吸收
→ 成熟方案3虚拟吸收
→ 处理相互作用/重复收益
→ 重新计算剩余差距
→ 继续虚拟攻击
→ 达到停止点
```

这里允许多轮虚拟推演，因为它不消耗真实 GPU，不产生本机实验循环。

每一轮都对比：

```text
当前虚拟结果
↔ REAL_STATE_OPTIMUM_RANGE（本机现实最优区间）
↔ T_PHY_TOTAL_REFERENCE（物理终极参照）
```

## 3.3 虚拟停止条件

当满足以下之一即可停止：

1. 虚拟综合方案已经进入本机现实最优区间；
2. 剩余收益已经很小；
3. 剩余方案风险/成本大于收益；
4. 剩余方案不成熟或不适用于当前硬件；
5. 继续优化需要开启新的独立研究方向。

此时冻结：

```text
虚拟99综合方案（VIRTUAL_99_FINAL_PLAN）
```

然后进入第4步。

---

# 第4步：Codex完整实测命令包

GPT 根据第3步已经完成的虚拟99结果，一次性写出完整命令包。

命令包至少包含：

```text
目标（OBJECTIVE）
当前状态（CURRENT_STATE）
允许改变（ALLOWED_CHANGE）
允许文件/组件（ALLOWED_FILES_OR_COMPONENTS）
基线（BASELINE）
候选顺序（CANDIDATE_ORDER）
种子与运行次数（SEEDS_AND_RUN_COUNT）
计时边界（TIMING_BOUNDARY）
质量门禁（QC_GATE）
成功规则（SUCCESS_RULE）
失败规则（FAILURE_RULE）
回滚规则（ROLLBACK）
总GPU预算（GPU_BUDGET）
总时间预算（TIME_BUDGET）
最终认证（FINAL_CERTIFICATION）
最终远端冻结（REMOTE_FREEZE）
```

## 4.1 Codex应该怎么执行

正确方式：

```text
读取当前技能
→ 验证版本与远端工作区
→ 读取完整命令包
→ 按命令包顺序执行全部既定测试
→ 按既定规则 KEEP（保留）/ROLLBACK（回滚）
→ 完成全部计划
→ Final Certification（最终认证）
→ push（推送）
→ remote verify（远端核验）
→ STOP（停止）
→ 返回 GPT
```

**不是：**

```text
测试1
→ 回GPT
→ 再设计
→ 测试2
→ 回GPT
→ 再设计
→ 测试3……
```

只要结果属于命令包已经写明的正常 PASS（通过）/ FAIL（失败）/ ROLLBACK（回滚）分支，就继续执行命令包。

只有发生命令包完全没有覆盖的异常、任务合同失效、质量/稳定/安全失效，才停止返回 GPT。

---

# 三、独立99路径规则

如果当前主流程完成后，又发现一条新的优化方向，而且：

- 可能有明显收益；
- 需要新的模型、软件版本、内核、架构或独立研究；
- 当前命令包没有包含；

不要把它重新插回当前任务形成循环。

把它记录成：

```text
独立99路径（INDEPENDENT_99_PATH）
```

以后单独执行同样四步：

```text
第1步：该路径对应的物理/机制边界
第2步：该路径在本机的现实约束
第3步：GPT虚拟99
第4步：独立Codex命令包
```

原主路径保持冻结。

这保证：

> 新机会可以继续研究，但不会破坏已经完成的简单主流程。

---

# 四、99分定义

99分不是“距离物理极限只差1%”。

99分表示：

```text
固定任务
+ 当前真实硬件
+ 单一物理极限参照
+ 本机现实最优区间
+ 成熟方案完整吸收
+ GPT虚拟99完整推演
+ Codex完整命令包实测
+ 质量/稳定/安全通过
+ Final Certification（最终认证）
+ Remote Verify（远端核验）
= 当前稳定最优99
```

完成后冻结。

---

# 五、远端共同工作区

每个项目必须声明自己的远端共同工作区。

本地 `C:\...`、`D:\...`、`/home/...` 只是执行副本或证据目录，不是共同事实源。

正确流程：

```text
远端读取
→ 本机执行
→ 报告
→ Git提交
→ 推送
→ 远端回读核验
```

远端核验通过后才算正式事实。

---

# 六、默认最短读取顺序

```text
1. SKILL.md
2. CANONICAL-IDENTITY-GATE.md（母技能身份门禁）
3. NO-FREE-EXPLORATION-GATE.md（禁止自由探索门禁）
4. 项目远端工作区声明
5. 当前项目四步结果
6. 最终Codex完整命令包
```

不要为了“理解更多”扩大阅读范围。

---

# 七、状态

```text
技能版本（SKILL_VERSION）=1.9.0
简洁四步法（SIMPLE_FOUR_STEP_METHOD）=YES
禁止自由探索（NO_FREE_EXPLORATION）=YES
虚拟层允许攻击迭代（VIRTUAL_ITERATION_ALLOWED）=YES
实测层禁止循环重规划（NO_REAL_EXECUTION_REPLAN_LOOP）=YES
完整命令包一次执行（COMPLETE_COMMAND_PACK_EXECUTION）=YES
独立新路线单独99（INDEPENDENT_99_PATH_FOR_NEW_RESEARCH）=YES
单一物理极限（SINGLE_T_PHY_TOTAL_REFERENCE）=YES
远端核验（REMOTE_VERIFY_REQUIRED）=YES
```
