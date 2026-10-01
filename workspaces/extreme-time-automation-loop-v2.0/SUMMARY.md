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

REALITY_CONTRACT=WORKING_BASELINE_R3_EXISTING_PAID_CORE

CORE_BRAIN=GPT
CORE_BRAIN_FIXED=YES
GPT_NATIVE_AGENTIC_CANDIDATE=ChatGPT Work

CODEX_ROLE=MATURE_TECHNICAL_EXECUTOR_CANDIDATE
CODEX_FIXED=NO

EXISTING_PAID_CAPACITY_ALLOWED=YES
NEW_INCREMENTAL_PAID_DEPENDENCY=FORBIDDEN_BY_DEFAULT

MANUS_2_ROLE=BENCHMARK_ONLY
BACKUP_PATH_REQUIRED=YES

PRIMARY_WINNER=NOT_YET_CERTIFIED
```

## 当前正式理解

1. 不是 FREE-FIRST。
2. 用户已经付费拥有的 GPT / Codex 能力应充分利用。
3. GPT 是固定核心超级大脑。
4. ChatGPT Work 是当前最值得先测的 GPT 原生成熟长任务执行形态。
5. Codex 是强技术执行候选，但不是固定核心；只有降低完整 T_VALID 或补齐 VALID 缺口时才进入主链。
6. Manus 2.0 只用现有积分做成熟商业整解 Benchmark，不进入正式生产。
7. 正式方案最终需要独立 Backup，但 Backup 不提前膨胀主链。
8. 默认不为本项目新增长期收费依赖；未来商业 ROI 明确时可由用户重新打开。

## 当前官方现实约束

OpenAI 当前官方说明：
- ChatGPT Work 面向较长、多步骤任务，可使用项目上下文、connected apps、浏览器、本地文件和桌面应用，并支持跨设备 Cloud Work。
- Codex 仍是独立视图，其 history 与 ChatGPT / Work 分开。
- 因此不能假设 Work↔Codex 已经原生零成本自动交接；必须 Reality 测量。

## 当前主链竞争顺序

```text
P1 GPT / ChatGPT Work 原生闭环
↓ 若已 VALID，不加额外层

P2 GPT / Work + Codex
↓ 仅技术/工程任务，交接成本计入 T_VALID

P3 GPT + 最小成熟执行能力组合
↓ 只按现实缺口加入 Browser / GitHub / n8n / OpenClaw / API / MCP / CLI
```

## 当前要测的值

```text
T_VALID_WORK
= GPT / Work 原生路径

T_VALID_WORK_CODEX
= GPT / Work + Codex 路径

T_REF_MANUS
= Manus 2.0 同一任务成熟付费参考

T_VALID_BACKUP
= 后续独立 Backup Reality
```

唯一最终优化目标仍是：
`T*=min(T_VALID)`

## 下一步顺序

```text
1. 固定一个真实任务
2. 先跑 GPT / Work 原生 Reality
3. 只有出现明确工程缺口时，再跑 Work + Codex
4. Manus 2.0 跑同一任务 Benchmark
5. 比较完整 T_VALID + 人工胶水
6. 找 GPT 主链最大的现实时间损失
7. 只用成熟能力攻击该损失点
8. 重测
9. 主链稳定后再选 Backup
```

## 当前文件

- `REALITY_CONTRACT.md`：R3 现实合同
- `MATURE_SOLUTION_COMPETITION_R3_GPT_CORE.md`：当前成熟方案竞争
- `GPT_WORK_PRIMARY_REALITY_001.md`：GPT / Work 原生主链 Reality
- `MANUS_BENCHMARK_REALITY_001.md`：Manus 2.0 Benchmark
- `MATURE_SOLUTION_COMPETITION_R2_FREE_FIRST.md`：SUPERSEDED 历史
- `FREE_PRODUCTION_REALITY_OPENCLAW_001.md`：SUPERSEDED 旧测试设计

当前仍为 STATE=10。未产生主链 Reality 证据前，不进入 Project Freeze。
