# CANONICAL IDENTITY GATE — v1.8.0

本文件解决一个具体故障：当前母技能已经从旧 `absolute-time-fireworks-optimization` 演化为独立技能后，执行者仍可能因为历史名称、旧目录、旧 main 内容或旧说明，把新的方法升级误写回祖先技能。

## 1. 当前唯一母技能身份

```text
CANONICAL_MOTHER_SKILL_ID=first-principles-physical-limit-convergence
CANONICAL_DISPLAY_NAME_ZH=第一性原理物理极限收敛引擎
CANONICAL_DISPLAY_NAME_EN=First-Principles Physical-Limit Convergence
CANONICAL_SKILL_VERSION=1.8.0
CANONICAL_SKILL_PATH=skills/first-principles-physical-limit-convergence/
CANONICAL_VERSION_BRANCH=codex/first-principles-physical-limit-convergence-v1.8.0
```

正式母技能升级只能写入上述 skill id / path 的当前版本分支。

## 2. 旧技能的关系

```text
LEGACY_ANCESTOR_SKILL_ID=absolute-time-fireworks-optimization
RELATIONSHIP=HISTORICAL_ANCESTOR_COMPATIBILITY_ASSET
CURRENT_MOTHER_SKILL=NO
CURRENT_METHOD_UPGRADE_TARGET=NO
ALIAS_OF_CURRENT_MOTHER_SKILL=NO
```

`absolute-time-fireworks-optimization` 是方法演化历史中的祖先/旧工程资产。它可以保留历史案例、兼容资料和旧冻结资产，但不能因为“方法源自它”就把当前母技能升级继续写回该目录。

同理，`mature-replication-four-column` 是历史方法来源/参考资产，不是当前母技能本体。

## 3. 每次修改母技能前必须先做身份门禁

```text
REQUESTED_MOTHER_SKILL_ID
REQUESTED_DISPLAY_NAME
CURRENT_REMOTE_BRANCH
CURRENT_SKILL_PATH
CURRENT_SKILL_VERSION
LINEAGE_ROLE
```

必须得到：

```text
REQUESTED_MOTHER_SKILL_ID == first-principles-physical-limit-convergence
CURRENT_SKILL_PATH == skills/first-principles-physical-limit-convergence/
LINEAGE_ROLE == CURRENT_MOTHER_SKILL
```

任何一项不成立：

```text
CANONICAL_IDENTITY_GATE=BLOCKED
→ DO NOT MODIFY LEGACY SKILL
→ LOCATE CURRENT VERSION BRANCH
→ READ CURRENT SKILL.md
→ RETURN TO GPT IF STILL AMBIGUOUS
```

## 4. 版本升级规则

当前正式谱系：

```text
v1.0.0
→ v1.1.0
→ v1.2.0
→ v1.3.0
→ v1.4.0
→ v1.5.0
→ v1.6.0
→ v1.7.0
→ v1.8.0
```

后续版本必须从当前最高正式版本继续演化，不得因为旧技能还有 `v2.x` 编号而把版本号切回旧谱系。

版本号属于当前 skill id 自己的谱系；不同 skill id 的版本号不可横向比较大小，也不可据此判断“哪个更新”。

## 5. 分发源规则

技能 canonical source 必须同时满足：

```text
REMOTE_REPOSITORY=cuiqinggang/codex-private-skills
BRANCH_MATCHES_DECLARED_SKILL_VERSION=YES
PATH=skills/first-principles-physical-limit-convergence/
SKILL_ID_MATCH=YES
VERSION_MATCH=YES
REMOTE_VERIFY=PASS
```

禁止把固定的旧 `v1.0.0` 分支长期写成所有新版本的 canonical branch。

## 6. 与 v1.7.0 的关系

v1.8.0 不改变 v1.7.0 已经冻结的核心方法：

- `NO_FREE_EXPLORATION=YES`；
- Codex 只做确定性验证器/执行器；
- GPT 提供完整验证铁路；
- 单一 `T_PHY_TOTAL_REFERENCE`；
- 远端共同工作区；
- MRE / REAL_STATE_MODEL；
- 成熟方案收割；
- 完整虚拟99铁路；
- 残余虚拟收敛；
- 组合生命周期 ROI；
- Final Certification / 99 / FREEZE。

v1.8.0 只增加“先确认你正在修改的是谁”的母技能身份门禁，防止方法升级写错谱系。

## 7. 验收句

任何母技能升级开始前必须能够输出：

```text
CANONICAL_IDENTITY_GATE=PASS
CANONICAL_MOTHER_SKILL_ID=first-principles-physical-limit-convergence
CANONICAL_SKILL_VERSION=1.8.0
LEGACY_ANCESTOR_MUTATION=NO
```
