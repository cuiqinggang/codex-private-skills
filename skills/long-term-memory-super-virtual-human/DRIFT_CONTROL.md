# 长期记忆超级虚拟人｜长流程防漂移 v0.1

## 结论

当前采用两层结构：

```text
稳定规则层：Skill / AGENTS.md / 项目规范
+
单任务权威层：TASK_CONTRACT / Reality Contract / Source of Truth
```

不是只靠“模型记住原目标”。

## 为什么

长流程常见失效不是单纯智力不足，而是：
- 目标被中间问题替代；
- 范围不断扩大；
- 子任务完成被误判为最终完成；
- 上下文过长后遗漏约束；
- 执行器自行补充未授权目标。

## 权威任务合同最小字段

```text
TASK_ID
FINAL_REALITY_GOAL
IN_SCOPE
OUT_OF_SCOPE
HARD_BOUNDARIES
DONE_WHEN
CURRENT_STATE
NEXT_ACTION
EVIDENCE_REQUIRED
FLOW_START
```

## 运行规则

- 长任务开始时生成或确认唯一权威任务合同；
- 所有计划、子智能体和执行器都引用同一 TASK_ID；
- 改目标必须显式更新权威合同；
- 与合同冲突的新增范围默认停止；
- 每个重要阶段回看 DONE_WHEN；
- Checkpoint 必须记录当前合同版本。

## 与市场成熟方法的关系

这不是纯自创方法。

成熟 Agent/编码生态普遍使用“项目指令文件 + 规格/计划/任务文件 + 验证”来降低长流程漂移。

本项目不复制某个框架，而是保留其中最小有效机制：
**稳定规则 + 单任务 Source of Truth + Reality 验证。**

是否优于只用 Prompt、只用 Checkpoint 或更完整 Spec-Driven Development，必须用同批正式任务比较完整 T_VALID。
