> STATUS=SUPERSEDED_BY_R2_FREE_FIRST  
> Current: `MATURE_SOLUTION_COMPETITION_R2_FREE_FIRST.md`  
> R1 is retained only as historical evidence before the FREE-FIRST production constraint.

# 成熟端到端方案竞争 R1｜极限短时间自动化闭环 v2.0

```ini
ROUND=R1
DATE=2026-10-01
STATE=10
PURPOSE=只保留值得进入真实 Reality 的成熟整解候选
WINNER=NOT_YET_CERTIFIED
```

## 1. R1 结论

第一轮官方能力核验后，候选分为两类：

### A. 完整整解 Reality 候选
1. **ChatGPT Work（含 Plugins / Cloud Browser / Desktop Local Work / Scheduled Tasks）**
2. **Manus 2.0（Cascade / Studio / Cloud Computer / Computer Use / Automations）**

这两项已经具备“目标驱动 + 项目连续 + 浏览器/应用执行 + 后台/自动化”的完整产品形态，值得直接进入真实任务竞争。

### B. 成熟基础设施 / 组件候选
3. Microsoft Copilot Studio
4. Zapier AI / Agents / Workflows
5. n8n

这些产品很成熟，但当前证据更像“需要用户先搭工作流/Agent/机器/租户”的自动化平台。它们可解决具体缺口，但暂不作为 v2.0 的第一轮完整整解，避免重新把用户变成系统搭建者。

## 2. 合同覆盖矩阵

| Reality Contract 关键项 | ChatGPT Work | Manus 2.0 | Copilot Studio | Zapier | n8n |
|---|---|---|---|---|---|
| 自然语言给最终目标 | 原生 | 原生 | 支持 Agent，但通常需先配置 | Agent 支持 | AI Agent 支持，通常需先搭 workflow |
| 项目 / 上下文持续 | Projects / Work chats | Cascade / Project | Agent / flow 状态 | Zap / Agent run | workflow executions |
| Web 自动执行 | Cloud Browser / built-in browser | Cloud browser / Browser Operator | Computer Use | 主要依赖 app actions | 主要依赖 nodes / 外接浏览器 |
| 本地 Windows / Desktop | Desktop Work 可授权本地文件/应用 | Computer Use / Remote Control | Computer Use GA | 非当前官方核心证据 | 非完整原生整解 |
| 用户离开后继续 | Cloud Work 可后台继续 | Cloud Computer / automations | Autonomous agent background | Zaps / agents 后台 | workflows 后台 |
| 定时 / 触发 / 监控 | Scheduled Tasks；支持部分 app events | Automations | agent flows / triggers | 成熟 trigger-action | 成熟 trigger / schedule |
| 跨应用 | Plugins / connected apps | integrations + browser/computer | connectors / flows | 9000+ apps | API/node 生态 |
| 必要时审批 | 原生重要操作审批 | 有审批/权限机制；R10模拟审批成立 | 支持权限/agent governance | Human in the Loop | Human-in-the-loop tool calls |
| 普通失败恢复 | 有任务状态；需 Reality 验证恢复质量 | 内部证据 R8 支持多故障恢复 | flow / runtime 能力成熟 | run history / workflow controls | failed execution retry |
| 自动验收 / 抗假完成 | 需要 Reality 验证 | 内部证据仍 PARTIAL | 需设计验证 | 需设计验证 | 需设计验证 |
| 低搭建成本 | 高 | 高 | 低 | 中 | 低 |
| 当前完整整解资格 | YES-CANDIDATE | YES-CANDIDATE | COMPONENT / ENTERPRISE-CANDIDATE | COMPONENT | COMPONENT |

## 3. ChatGPT Work｜R1 事实

官方当前资料确认：

- Work 是为较长、多步骤任务设计的 Agent，可跨已连接应用、文件和 Web 工作并生成成品。
- Project 可把聊天、文件和指令放在一起。
- Cloud Work 对话可以跨 Web / Mobile / Desktop 同步。
- Cloud Browser 能在用户离开对话或关闭电脑后继续工作，需要登录、信息或确认时暂停。
- Desktop Work 可以在授权后使用本地文件和桌面应用。
- Scheduled Tasks 可以一次、周期、监控变化，并支持部分 Gmail / Slack / GitHub 事件触发。
- Plugins 可同时用于 Work 与 Codex。
- 局限：某些网站 / 登录 / 交易仍可能要求用户接管；Codex 仍是独立视图与历史，Work↔Codex 是否能做到完全无人工交接需要 Reality 验证。

### R1 判断
进入完整整解 Reality。

关键测试点不是“会不会做任务”，而是：
1. 能否在一个真实任务里把 Work、插件、浏览器、本地文件/应用与必要 Codex 能力连续起来；
2. 页面/设备切换后是否仍无需用户做人肉上下文搬运；
3. 普通失败能否自动恢复；
4. 机器可验事实能否自动验收而不要求用户确认。

## 4. Manus 2.0｜R1 事实

官方当前资料确认：
- Cascade 维持一个连接项目，并按需加入专门能力；
- Studio 可处理电脑现有文件和工具；
- Cloud Computer 可作为自动化常驻运行环境；
- Remote Control / Computer Use 可以在授权会话里操作本地文件、浏览器和应用；
- Automations 可在信号触发时启动工作；
- Cue 提供多 Agent 团队形态。

共同工作区已有 R1-R10 Reality 证据：
- 规划、目标保持、多故障恢复、备用路径、依赖调度、多 Agent、局部失败隔离、抢占恢复、幂等均已有现实证据；
- 同 Project 状态连续性 SUPPORTED；
- 定时自动化 SUPPORTED_WITH_DELAY；
- 浏览器执行 SUPPORTED_SCOPED；
- 但自验证 / 假完成抵抗 / 硬隔离仍 PARTIAL；
- 用户 Windows 本机完整执行在旧 R1-R10 中为 NOT_TESTED_ENV；
- 跨天、重启、断电、供应商失效仍未证明。

### R1 判断
进入完整整解 Reality。

优先补的不是更多模拟测试，而是一条真实本机/自动化端到端任务。

## 5. Microsoft Copilot Studio｜R1 事实

- Computer Use 已 GA，可控制 Windows Web 和桌面应用，并明确适合后台 autonomous agents；
- Agent flows 支持触发、动作和确定性工作流；
- 但正式使用通常涉及 Copilot Studio 用户 / tenant license、环境与机器配置；
- Cloud PC pool 等部分运行形态仍有 Preview 成分。

### R1 判断
成熟且强，但当前用户是单人极限时间场景；先放入成熟基础设施池，不先承担完整整解主路径。

## 6. Zapier｜R1 事实

- 官方称其有 9000+ app 生态，可建设端到端业务自动化；
- Agents / AI by Zapier 可执行跨应用动作；
- Human in the Loop 可暂停、收集信息或审批后继续；
- workflow / trigger 生态非常成熟。

### R1 判断
对于 SaaS/API 任务是强成熟方案，但“本地 Windows + 通用电脑操作 + 项目级长任务”不是本轮官方证据的原生完整闭环，因此暂列成熟组件/特定域整解。

## 7. n8n｜R1 事实

- 成熟 workflow automation，支持大量 API / node 集成；
- 有 execution history、失败执行 retry；
- AI Agent tool calls 支持 Human-in-the-loop；
- 可 Cloud 或 self-host。

### R1 判断
它解决“编排”很好，但用户当前目标是减少搭建与人肉胶水，不是建设自己的编排系统。因此保持成熟组件身份；只有完整候选出现它无法覆盖的确定缺口时再调用。

## 8. R1 后的最短路径

```text
Reality Contract R1
→ 完整候选只保留 ChatGPT Work + Manus 2.0
→ 设计同一个真实 Smoke Task
→ 分别跑 Reality
→ 产生各自 T_VALID + 人工介入 + 恢复/验收证据
→ 保留更短有效路径
→ 再攻击剩余 T_VALID 瓶颈
```

不再花时间做大范围功能表。

## 9. 首个 Reality Smoke Task 要求

任务必须同时覆盖：
- 一次自然语言目标；
- 至少 2 类工具/环境（例如 Web + 文件，或 Web + GitHub）；
- 至少 1 个可机器验收的现实产物；
- 至少 1 次跨阶段持续推进；
- 不允许用户复制中间消息；
- 普通失败如出现，应由候选自行恢复；
- 最终只以现实结果和证据判定 VALID。

建议优先选择用户本来就要做的一项真实工作，而不是专门制造 Benchmark。

## 10. 官方来源（2026-10-01 核验）

OpenAI:
- https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
- https://help.openai.com/en/articles/20001280-using-cloud-browser-in-chatgpt
- https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt
- https://help.openai.com/en/articles/20001256-plugins-in-chatgpt

Manus:
- https://help.manus.im/zh-CN/articles/17190150-manus-2-0-%E6%9C%89%E5%93%AA%E4%BA%9B%E6%96%B0%E5%8A%9F%E8%83%BD

Microsoft:
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/computer-use
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview
- https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-licensing

Zapier:
- https://help.zapier.com/hc/en-us/articles/24393442652557-Build-an-agent-in-Zapier-Agents
- https://help.zapier.com/hc/en-us/articles/38733184458765-Use-Human-in-the-Loop-to-pause-Zap-workflows-pending-human-review

n8n:
- https://docs.n8n.io/
- https://docs.n8n.io/workflows/executions/all-executions/
