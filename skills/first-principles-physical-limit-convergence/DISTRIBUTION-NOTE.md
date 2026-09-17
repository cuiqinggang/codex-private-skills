# DISTRIBUTION NOTE — v1.9.0

## Canonical source

```text
repository=cuiqinggang/codex-private-skills
branch=codex/first-principles-physical-limit-convergence-v1.9.0
path=skills/first-principles-physical-limit-convergence/
skill_id=first-principles-physical-limit-convergence
version=1.9.0
```

Hard rule:

```text
BRANCH_MATCHES_DECLARED_SKILL_VERSION=YES
SKILL_ID_MATCH=YES
VERSION_MATCH=YES
REMOTE_VERIFY=PASS
```

固定历史分支不得长期作为后续版本 canonical source。

语义冲突时，以声明版本对应远端 canonical `SKILL.md` 为准，同时服从更高层级系统/安全/平台约束。

## Lineage isolation

`absolute-time-fireworks-optimization` 是历史祖先/兼容资产，不是当前 mother skill、alias 或 upgrade target。

## v1.9 execution semantic

本版本新增：

```text
PREAUTHORIZED_BATCH_EXECUTION=YES
NO_REPLAN_ON_MAGNITUDE_SURPRISE=YES
NO_OPEN_ENDED_PREFLIGHT_CHAIN=YES
RETURN_TO_GPT_AT_BATCH_BOUNDARY=YES
```

即完整 Virtual-99 后，Codex 可在预定义 batch 内沿预定义分支连续执行；只有材料级重规划触发器才提前返回 GPT。

## Expanded ZIP

会话 ZIP 可以是扩展归档，但不得成为第二真相源或第二方法。
