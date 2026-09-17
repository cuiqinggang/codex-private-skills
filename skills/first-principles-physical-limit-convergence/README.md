# first-principles-physical-limit-convergence v1.7.0

中文名：**第一性原理物理极限收敛引擎**

v1.7.0 的核心不是增加更多实验，而是把执行边界锁死：

```text
技能优先门禁
→ 单一端到端 T_PHY_TOTAL_REFERENCE
→ MRE / REAL_STATE_MODEL
→ 成熟方案收割
→ GPT完整虚拟99铁路
→ Codex确定性短验证
→ 返回GPT
→ 残余虚拟收敛
→ 组合生命周期ROI
→ Final Certification
→ 99 / FREEZE
```

## 最强项目规则

```text
NO_FREE_EXPLORATION=YES
CODEX_ROLE=DETERMINISTIC_VALIDATOR_EXECUTOR
CODEX_MAY_DESIGN_TEST_PLAN=NO
CODEX_MAY_ADD_CANDIDATE=NO
CODEX_MAY_EXTEND_ITERATION=NO
CODEX_MAY_PROFILE_WITHOUT_GPT_PLAN=NO
GPT_COMPLETE_VALIDATION_RAILROAD_REQUIRED=YES
```

任务命令可以更具体、更严格，但不能弱化“禁止自由探索”。未被 GPT 铁路预定义的实验、候选、追加运行、profiling 或参数搜索一律停止并返回 GPT。

## 物理极限板

每个固定任务只保留一个正式物理极限对比标准：

```text
T_PHY_TOTAL_REFERENCE = 一个端到端时间数字或区间
```

分块极限只用于内部计算，不再与总极限并列展示。它是理论物理参照，不等于实测机器 benchmark，也不直接等于 99 门槛。

## 共同工作区

共同工作区必须是项目声明的远端在线权威空间。本地 `C:\...`、`D:\...`、`/home/...`、clone/worktree 只属于执行副本或证据目录。新工程事实只有 push 并 remote verify 后才能成为共同事实。

完整规则见 `SKILL.md`，最高优先级执行门禁见 `references/NO-FREE-EXPLORATION-GATE.md`。
