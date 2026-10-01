# 成熟方案竞争 R3｜GPT CORE + 可替换执行层｜极限短时间自动化闭环 v2.0

```ini
ROUND=R3
DATE=2026-10-01
STATE=10

CORE_BRAIN=GPT
CORE_BRAIN_FIXED=YES
EXISTING_PAID_CAPACITY_ALLOWED=YES
NEW_INCREMENTAL_PAID_DEPENDENCY=FORBIDDEN_BY_DEFAULT

GPT_NATIVE_AGENTIC_CANDIDATE=ChatGPT Work
CODEX=PRIMARY_TECHNICAL_EXECUTOR_CANDIDATE
CODEX_FIXED=NO

MANUS_2=BENCHMARK_ONLY
BACKUP_PATH=REQUIRED
PRIMARY_WINNER=NOT_YET_CERTIFIED
```

## 1. R3 修正

R2 的 FREE-FIRST 过度收紧，错误地把用户已经付费拥有的 GPT / Codex 能力当成需要排除的收费依赖。

R3 正式修正为：

```text
已经拥有的强能力 → 充分使用
新增长期付费依赖 → 默认不加
```

## 2. 固定核心

**GPT = 超级大脑。**

GPT 负责：
- 目标理解；
- Reality Contract；
- 世界成熟方案检索；
- 决策与组合；
- 故障归因；
- 重新选路；
- FINAL_VALID 判断；
- 整体 T_VALID 收敛。

## 3. GPT 原生成熟执行形态｜ChatGPT Work

OpenAI 当前官方产品已经把 Work 定义为长任务、多步骤 Agent：

- 可在 Project 中使用上下文；
- 可使用 connected apps / plugins；
- 可使用 Cloud Browser；
- 桌面端可在授权后处理本地文件和桌面应用；
- Cloud Work 可以跨 web / mobile / desktop 续接；
- Work 可运行一次、按计划重复、按触发器启动或监控变化。

因此主链不应先假设需要外部 orchestrator。

优先 Reality：

```text
用户目标
→ GPT / ChatGPT Work
→ 原生工具与成熟 connected apps
→ FINAL_VALID
```

若这一条已经满足 VALID，就不因为历史上习惯使用 Codex 而额外加入 Codex。

## 4. Codex 的正确角色

OpenAI 官方当前明确：Codex 仍是独立视图，历史与 ChatGPT / Work 分开。

因此：

```ini
CODEX_ROLE=MATURE_TECHNICAL_EXECUTOR_CANDIDATE
CODEX_FIXED=NO
AUTO_HANDOFF_ASSUMED=NO
```

Codex 优先用于：
- 编码；
- repository / terminal / developer tools；
- 工程修改；
- 测试；
- 技术长流程。

只有当某任务加入 Codex 后能：
- 让原本不 VALID 的任务变 VALID；或
- 降低完整 T_VALID，

才进入该任务的主链。

否则由 GPT / Work 直接完成。

## 5. 当前主链候选顺序

### P1｜GPT / ChatGPT Work 原生闭环
当前第一条要验证的路径。

### P2｜GPT / Work + Codex
仅用于技术/工程任务，且必须把 Work↔Codex 的上下文与交接成本计入完整 T_VALID。

### P3｜GPT + 最小成熟执行能力
按具体缺口调用：
- JEV-native / Playwright；
- GitHub；
- n8n；
- OpenClaw；
- API / MCP / CLI；
- 其他成熟现成能力。

不固定组件数；只保留本任务实际需要的最小组合。

## 6. Manus 2.0

```ini
PRODUCTION=NO
BENCHMARK=YES
USE_EXISTING_CREDITS_ONLY=YES
```

输出：
`T_REF_MANUS`

只回答：
> 一个成熟商业整解对同一 Reality 可以做到多快？

它不进入未来正式主链。

## 7. Backup｜独立备份路径

正式方案最终必须有 Backup。

要求：
- 不要求 GPT 与 Codex 同时正常；
- 主链故障时能恢复最低可用工作能力；
- 只由成熟现成能力组成；
- 平时不与主链并行消耗资源；
- 只在故障 / 灾备 Reality 启用。

备份候选以后单独竞争，不提前固定。

## 8. 现在真正应该测什么

按价值排序：

```text
A1. GPT / Work 原生主链
    → T_VALID_WORK

A2. 对确实需要工程执行的任务：
    GPT / Work + Codex
    → T_VALID_WORK_CODEX

B. Manus 2.0 Benchmark
   → T_REF_MANUS

C. 独立 Backup
   → T_VALID_BACKUP
```

当前先做 A+B；Backup 等主链结构明确后再 Reality。

## 9. 比较逻辑

如果 Work 单独 VALID：

```text
Work
vs
Work + Codex
vs
Manus Reference
```

只有 Work+Codex 的完整 T_VALID 更优，Codex 才保留在该类任务主链。

如果 Work 单独不 VALID，而 Codex 补齐工程缺口，则 Codex 属于必要成熟执行组件。

## 10. 下一步

```text
① 用一个真实任务先跑 GPT / Work 原生路径
② 同一任务中若确有技术执行缺口，再跑 GPT / Work + Codex
③ Manus 2.0 跑同一 Reality Benchmark
④ 比较 T_VALID 与人工胶水
⑤ 找 GPT 主链最大时间损失点
⑥ 只引入成熟能力攻击该损失点
⑦ 重测
⑧ 主链稳定后再选择 Backup
```

不新增架构；不保护 Codex；也不浪费已经拥有的 GPT / Codex 能力。
