# 极限短时间自动化闭环 v2.0

```ini
PROJECT=极限短时间自动化闭环
VERSION=v2.0
STATE=10
PHASE=GPT_CORE_REALITY_COMPETITION
VIRTUAL_MATURE=NO
PROJECT_FREEZE=NO
FINAL_VALID=NO

CONSTITUTION_VERSION=v0.3
CONSTITUTION_FREEZE_ID=ETAC-v0.3-FREEZE-R1

OBJECTIVE=T*=min(T_VALID)
MATURE_SOLUTION_EXISTS=TRUE
NO_NEW_IMPLEMENTATION_ESCAPE=TRUE
CHANGE_SCOPE=ROOT_CAUSE_SCOPE

CORE_BRAIN=GPT
CORE_BRAIN_FIXED=YES
EXISTING_PAID_CAPACITY_ALLOWED=YES
NEW_INCREMENTAL_PAID_DEPENDENCY=FORBIDDEN_BY_DEFAULT

CODEX_ROLE=MATURE_TECHNICAL_EXECUTOR_CANDIDATE
CODEX_FIXED=NO

MANUS_2_ROLE=BENCHMARK_ONLY
BACKUP_PATH_REQUIRED=YES
```

## 1. 项目目标

把用户过去亲自承担的复制、转发、提醒、换页、恢复上下文、普通故障纠偏、跨工具接力等“人肉胶水”尽量自动消除。

唯一目标：

```text
T* = min(T_VALID)
```

## 2. v2.0 当前正式结构

### 固定核心
GPT 是当前正式超级大脑，负责：
- 理解现实目标；
- Reality Contract；
- 成熟方案检索与组合；
- 决策、纠偏与恢复；
- FINAL_VALID；
- 整体 T_VALID 收敛。

### 原生主链候选
优先测试 ChatGPT Work：

```text
用户目标
→ GPT / ChatGPT Work
→ 原生工具 / connected apps / browser / files
→ FINAL_VALID
```

若 Work 单独已 VALID，不额外加入执行层。

### 技术执行候选
Codex 是强成熟技术执行器，但不是固定核心：

```text
Work 单独存在明确技术缺口
或
加入 Codex 能降低完整 T_VALID
→ 才加入 Codex
```

### 其他成熟能力
JEV-native / Playwright、GitHub、n8n、OpenClaw、API、MCP、CLI 等只按现实缺口加入。

## 3. 成本原则

本项目不是 FREE-FIRST。

正确原则：

```text
已经付费拥有的能力 → 充分使用
新增持续付费依赖 → 默认不加
```

未来若出现明确商业 ROI，用户可重新打开新增付费能力竞争。

## 4. Manus 2.0

Manus 2.0 只用现有积分做成熟商业整解 Benchmark：

```ini
PRODUCTION=NO
BENCHMARK=YES
REFERENCE=T_REF_MANUS
```

即使 Manus 更快，也不自动进入未来正式主链。

## 5. 独立备份

最终正式方案必须有 Backup。

Backup：
- 不要求 GPT 与 Codex 同时正常；
- 平时不与主链并行消耗资源；
- 主链异常时提供最低可用恢复能力；
- 只由成熟现成能力组成。

Backup 在主链结构明确后再单独 Reality 竞争。

## 6. v2.0 不再做什么

- 不重新开发新的 orchestrator；
- 不把状态机 / 三行头 / 四字段视为不可替代；
- 不保护 Codex；
- 不因某组件免费就优先；
- 不因某组件收费就排除已经拥有的能力；
- 不因为 Manus 是成熟商业产品就把它加入生产。

## 7. 当前 Reality 顺序

```text
A1. GPT / ChatGPT Work 原生路径
    → T_VALID_WORK

A2. 只有需要时：GPT / Work + Codex
    → T_VALID_WORK_CODEX

B. Manus 2.0 同任务 Benchmark
   → T_REF_MANUS

C. 主链稳定后：
   独立 Backup Reality
   → T_VALID_BACKUP
```

## 8. 当前状态

仍为：

```ini
STATE=10
VIRTUAL_MATURE=NO
PROJECT_FREEZE=NO
```

当前不是继续设计架构，而是进入 Reality。
