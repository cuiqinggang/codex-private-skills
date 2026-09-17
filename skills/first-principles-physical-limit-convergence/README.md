# first-principles-physical-limit-convergence v1.8.0

中文名：**第一性原理物理极限收敛引擎**  
英文名：**First-Principles Physical-Limit Convergence**

v1.8.0 不重写 v1.7.0 的方法核心。它解决一个已经真实发生的治理故障：当前母技能已经独立成新 skill id 后，历史祖先技能仍可能因为旧名称、旧目录或旧版本号被误当成当前母技能继续升级。

因此 v1.8.0 新增最前置门禁：

```text
CANONICAL IDENTITY / LINEAGE ISOLATION
→ 技能优先门禁
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

## 当前唯一母技能身份

```text
CANONICAL_MOTHER_SKILL_ID=first-principles-physical-limit-convergence
CANONICAL_SKILL_VERSION=1.8.0
CANONICAL_SKILL_PATH=skills/first-principles-physical-limit-convergence/
CANONICAL_VERSION_BRANCH=codex/first-principles-physical-limit-convergence-v1.8.0
```

历史 `absolute-time-fireworks-optimization` 只是祖先/兼容资产，不是当前母技能，不是当前升级目标，也不是当前 skill id 的别名。不同 skill id 的版本号不能横向比较。

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

## 默认读取顺序

1. `SKILL.md`
2. `references/CANONICAL-IDENTITY-GATE.md`
3. `references/NO-FREE-EXPLORATION-GATE.md`
4. `references/REMOTE-SHARED-WORKSPACE.md`
5. 项目远端工作区声明
6. GPT 当前完整验证铁路

完整规则见 `SKILL.md`。
