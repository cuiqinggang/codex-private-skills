# CANONICAL IDENTITY GATE — v1.9.0

本文件防止当前母技能被历史祖先技能、旧目录或旧版本号覆盖。

## 1. 当前唯一母技能身份

```text
CANONICAL_MOTHER_SKILL_ID=first-principles-physical-limit-convergence
CANONICAL_DISPLAY_NAME_ZH=第一性原理物理极限收敛引擎
CANONICAL_DISPLAY_NAME_EN=First-Principles Physical-Limit Convergence
CANONICAL_SKILL_VERSION=1.9.0
CANONICAL_SKILL_PATH=skills/first-principles-physical-limit-convergence/
CANONICAL_VERSION_BRANCH=codex/first-principles-physical-limit-convergence-v1.9.0
```

## 2. 历史技能关系

```text
LEGACY_ANCESTOR_SKILL_ID=absolute-time-fireworks-optimization
RELATIONSHIP=HISTORICAL_ANCESTOR_COMPATIBILITY_ASSET
CURRENT_MOTHER_SKILL=NO
CURRENT_METHOD_UPGRADE_TARGET=NO
ALIAS_OF_CURRENT_MOTHER_SKILL=NO
```

`mature-replication-four-column` 也是历史方法来源/参考资产，不是当前母技能本体。

## 3. 修改前身份门禁

必须核对：

```text
REQUESTED_MOTHER_SKILL_ID
CURRENT_REMOTE_BRANCH
CURRENT_SKILL_PATH
CURRENT_SKILL_VERSION
LINEAGE_ROLE
```

要求：

```text
REQUESTED_MOTHER_SKILL_ID == first-principles-physical-limit-convergence
CURRENT_SKILL_PATH == skills/first-principles-physical-limit-convergence/
CURRENT_SKILL_VERSION == 1.9.0
LINEAGE_ROLE == CURRENT_MOTHER_SKILL
```

不满足：

```text
CANONICAL_IDENTITY_GATE=BLOCKED
-> DO NOT MODIFY LEGACY SKILL
-> LOCATE CURRENT VERSION BRANCH
-> READ CURRENT SKILL.md
-> RETURN_TO_GPT IF STILL AMBIGUOUS
```

## 4. 正式谱系

```text
v1.0.0
-> v1.1.0
-> v1.2.0
-> v1.3.0
-> v1.4.0
-> v1.5.0
-> v1.6.0
-> v1.7.0
-> v1.8.0
-> v1.9.0
```

不同 skill id 的版本号不可横向比较。

## 5. 分发源规则

```text
REMOTE_REPOSITORY=cuiqinggang/codex-private-skills
BRANCH_MATCHES_DECLARED_SKILL_VERSION=YES
PATH=skills/first-principles-physical-limit-convergence/
SKILL_ID_MATCH=YES
VERSION_MATCH=YES
REMOTE_VERIFY=PASS
```

## 6. v1.9 与 v1.8 的关系

v1.9 保留 v1.8 的 canonical identity、NO_FREE_EXPLORATION、单一 T_PHY、MRE、成熟方案、Virtual-99、ROI、Final Certification。

唯一方法级修正：把“每个正常结果都回 GPT”改成“预授权 batch 内按预定义分支连续执行；只在 batch boundary 或 MATERIAL_REPLAN_TRIGGER 返回 GPT”。

```text
PREAUTHORIZED_BATCH_EXECUTION=YES
NO_REPLAN_ON_MAGNITUDE_SURPRISE=YES
NO_OPEN_ENDED_PREFLIGHT_CHAIN=YES
```

## 7. 验收

```text
CANONICAL_IDENTITY_GATE=PASS
CANONICAL_MOTHER_SKILL_ID=first-principles-physical-limit-convergence
CANONICAL_SKILL_VERSION=1.9.0
LEGACY_ANCESTOR_MUTATION=NO
```
