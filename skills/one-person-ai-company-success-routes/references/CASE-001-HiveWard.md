# CASE-001 - HiveWard

任务标准：按 `HIVEWARD-ONE-PERSON-AI-COMPANY-REFERENCE-REVIEW-20260528` 的详细标准审查；HiveWard 只作为一人 AI 公司路线案例之一，不作为唯一结论。

## 项目定位

HiveWard 的定位是“一人公司的 Agent Company 工作台”：不是替代 OpenClaw、Claude Code、Codex、Hermes 等执行体，而是在其上方建立公司、CEO、Leader、业务蓝图、审批、运行历史和复盘层。它的价值不在“又一个聊天框”，而在把多个 harness 组织成可调度、可审批、可复用、可审计的业务节点。

## 证据

- 本地源码：`H:\AI\_explore\one-person-ai-company-success-routes-20260528\sources\repos\HiveWard`。
- Git HEAD：`6f4524b483a1be8cef72baed8843c881d6c4901f`，提交时间 `2026-05-28T09:06:40+08:00`。
- README 关键描述：`README.md:13`, `README.md:49`, `README.md:53`, `README.md:70-78`。
- mock 边界：`README.md:132`, `docs\development-setup.md:48-50`, `.env.example:14-17`。
- 截图证据：`screenshots\HiveWard\hiveward-blueprint-studio.png`, `hiveward-inbox.png`, `hiveward-history.png`, `hiveward-runs.png`。
- License：`LICENSE` 为 Apache-2.0。

## 架构图文字版

```text
Company
  -> CEO role seat
     -> sees Leaders, blueprints, runs, inbox, risks
     -> creates delegation/proposal items instead of mutating silently
  -> Leader role seats
     -> one Leader owns exactly one business blueprint
     -> explains blueprint, failures, approvals, proposals
  -> Blueprint DAG
     -> Agent nodes call external harnesses
     -> Manager nodes coordinate manager_slot ports
     -> Slot nodes carry parallel lanes / routed work
     -> approval/send live in agent config
  -> Run engine
     -> starts blueprint runs, tracks node status, can cancel
     -> pauses on approval and resumes after approve/reject/reply
  -> Inbox / History
     -> governance gate for proposed changes and delegations
     -> durable replay surface for run summaries and chat history
  -> Runtime adapters
     -> OpenClaw gateway or mock fallback
     -> Codex/Claude/Hermes/Beta CLI harness concepts
```

## 关键文件

- `packages\shared\src\company.ts`：公司概念和默认公司模型。
- `packages\shared\src\roles.ts`：CEO、Leader、Architecture Blueprint 的角色目录。
- `packages\shared\src\blueprint.ts`：Blueprint、Agent、Manager、Slot、Run 结构和默认蓝图。
- `packages\shared\src\api.ts`：API 合约，包含 `HarnessId = openclaw | claudeCode | codex | google | cursor | opencode | hermes`，以及 inbox、approval、run、history 类型。
- `packages\shared\src\inboxSubmission.ts`：chat 到 inbox 的正式提交边界。
- `packages\adapter\src\sdk-runtime\factory.ts`：runtime adapter 选择。
- `packages\adapter\src\sdk-runtime\codex-runtime.ts`、`claude-runtime.ts`、`cli-runtime.ts`：外部执行体适配思路。
- `apps\api\src\routes\apiRouter.ts`：蓝图运行、inbox、approval、runtime-overview、chat-history 路由。
- `docs\skills\hiveward-ceo\SKILL.md`：CEO 角色规则。
- `docs\skills\hiveward-leader\SKILL.md`：Leader 角色规则。

## 核心机制判断

1. Company 是业务上下文容器，不只是项目目录。它绑定目标、角色目录、蓝图、运行记录、收件箱和仪表盘状态。
2. CEO / Leader 是长期 role seat，不等价于一次 prompt。CEO 看全局，Leader 只看绑定蓝图，降低跨业务线混乱。
3. Blueprint 是可执行业务 DAG；Agent 负责执行，Manager 负责路由，Slot 负责并行/分派通道。
4. Approval / send 不应是散乱副作用，而应作为 Agent 配置和 run pause 状态被记录。
5. Inbox 是治理边界：chat 不能直接改蓝图，必须形成 proposal/delegation，再经审批。
6. History/run summary 是复盘资产，适合映射到“昨日重现法”的成功/失败样本库。
7. Runtime adapter 把执行能力外置，HiveWard 只做编排和治理；这点适合用户现有 Codex、OpenClaw、Hermes 体系。

## 不成熟风险

- 项目处于早期，star 和生态尚小；不能把它当作唯一路线。
- 真实 runtime 适配涉及 OpenClaw/Codex/Claude/Hermes 等多种环境，生产接入风险高。
- 自动更新逻辑存在 `git pull` / `npm install` 能力，必须在本体系中禁用或改成人工审核。
- README 中出现 Beta CLI harness，稳定性和安全边界需逐项验证。
- 蓝图 UI/审批体验还需用长期运行数据验证，不宜直接承载真实业务发送。

## 对 Polsia / 一人 AI 公司系统的映射

| HiveWard 机制 | Polsia / 本地系统映射 | 吸收动作 |
|---|---|---|
| Company | AICompany Dashboard 的公司/业务线容器 | 吸收为顶层 context asset |
| CEO role seat | Codex/Hermes 的总控任务入口 | 吸收，但必须保留人工最终责任 |
| Leader per Blueprint | 每条 revenue path / workflow 的负责人 | 吸收为业务线 owner |
| Blueprint DAG | ECC/技能包/任务流程的可执行路线图 | REPLAY，先做控制台原型 |
| Agent runtime adapter | OpenClaw、Codex、Hermes、ComfyUI 等执行体 | 吸收接口，不直接接生产 |
| Inbox approval | 审批门、发送前人工确认 | 必须吸收 |
| Run history | 运行报告、任务复盘、昨日重现样本 | 必须吸收 |
| Mock fallback | 安全 replay / read-only 验证 | 必须吸收 |

## 是否进入技能包

建议进入。吸收的不是整套安装，而是“公司容器 + CEO/Leader 角色席位 + 蓝图 DAG + Inbox 审批 + Run History + 外部执行体适配”的系统设计。暂缓真实接入 OpenClaw、Claude、Codex、Hermes；下一阶段只做控制台原型和 mock replay。
