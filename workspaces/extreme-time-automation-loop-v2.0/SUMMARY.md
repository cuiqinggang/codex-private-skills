# 极限短时间自动化闭环 v2.0｜当前接续摘要

```ini
PAGE_NAME=极限短时间自动化闭环 v2.0
PROJECT_VERSION=v2.0
STATE=10
VIRTUAL_MATURE=NO
PROJECT_FREEZE=NO
FINAL_VALID=NO

CONSTITUTION_VERSION=v0.3
CONSTITUTION_FREEZE=YES
CONSTITUTION_FREEZE_ID=ETAC-v0.3-FREEZE-R1

OBJECTIVE=T*=min(T_VALID)
MATURE_SOLUTION_EXISTS=TRUE
NO_NEW_IMPLEMENTATION_ESCAPE=TRUE
CHANGE_SCOPE=ROOT_CAUSE_SCOPE

REALITY_CONTRACT=WORKING_BASELINE_R2_FREE_FIRST
PRODUCTION_PAID_DEPENDENCY=FORBIDDEN
PRODUCTION_INCREMENTAL_SUBSCRIPTION_COST=0
PAID_BENCHMARK=Manus 2.0
PAID_BENCHMARK_ROLE=REFERENCE_ONLY
FREE_PRODUCTION_FRONT_RUNNER=OpenClaw
PRODUCTION_WINNER=NOT_YET_CERTIFIED
```

## 当前正式变化

1. 正式生产改为 FREE-FIRST：长期主链不得依赖必须付费才能持续使用的能力。
2. Manus 2.0 不再是生产候选，只用现有积分跑一次成熟付费 Benchmark，得到 `T_REF_MANUS`。
3. ChatGPT Work 因属于付费能力，退出生产候选。
4. OpenClaw 成为当前最重要免费成熟整解候选。
5. Codex Free、现有免费模型池、既有成熟 Browser 技能、n8n Community Edition 只作为成熟免费组件按缺口加入。
6. OpenClaw Windows Computer Use 当前官方仍属 experimental，不能直接作为成熟生产证据。
7. 付费商业能力只有未来出现明确商业 ROI 且用户明确重开成本门时，才重新进入生产候选。

## 当前比较模型

```text
T_REF_MANUS = Manus 2.0 同一真实任务端到端 T_VALID
T_VALID_FREE = 免费生产候选同一任务端到端 T_VALID
GAP = T_VALID_FREE - T_REF_MANUS
```

GAP 只用于定位剩余时间损失；唯一优化目标仍是免费 VALID 候选里的 `min(T_VALID)`。

## 当前 Reality 文件

- `REALITY_CONTRACT.md`：R2 FREE-FIRST 工作合同
- `MATURE_SOLUTION_COMPETITION_R2_FREE_FIRST.md`：免费生产候选竞争
- `MANUS_BENCHMARK_REALITY_001.md`：Manus 2.0 付费基准任务
- `FREE_PRODUCTION_REALITY_OPENCLAW_001.md`：OpenClaw 免费生产 Reality

## 下一步顺序

```text
1. Manus 2.0 跑一次同任务 Benchmark
   → 得到 T_REF_MANUS

2. 本机 OpenClaw 只读现状核验
   → 版本 / Gateway / Sessions / Automations / Browser
   → 免费模型池
   → Codex Free 可用性
   → 不先升级、不先改造

3. 若升级是已成熟且明显必要的路径
   → 复用既有 OpenClaw upgrade skill

4. OpenClaw 免费路径跑同一 Reality
   → 得到 T_VALID_FREE

5. 计算 GAP
   → 找最大现实时间损失

6. 只用成熟免费能力攻击最大 GAP
   → 重测
   → 有完整 T_VALID 收益才保留
```

当前仍为 STATE=10。未跑完两条 Reality 前，不宣布生产主路径 Freeze。
