---
name: ai-resource-orchestrator
description: Route an AI task to the lowest-cost verified executor and reasoning effort that can still meet its quality, capability, and safety requirements; use for cost-quality routing across Codex, Codex subagents, Reasonix, Playwright, or human confirmation.
metadata:
  version: "2.0.1"
  maturity: "METHOD_VERIFIED_RESOURCE_PARTIAL"
---

# AI Resource Orchestrator 2.0 Core

完成一件事：在质量底线、能力要求和安全边界得到满足的前提下，为任务选择成本最低的已验证执行路径。

## 成熟成功态与四列法：实际执行规则

接单、复用成熟方案、分派、验收、返工或保存经验时，先读取 [接入合同](references/method-integration.md) 和其中的唯一四列法正式入口；ARO 仍是唯一资源调度，不调用 MOA 再回调自己。

- **接单分析**：先确定产物、通过标准、输入与限制，再倒推必需能力，形成有来源的紧凑四列记录。
- **成熟方案匹配**：先已有匹配技能，再 find-skills 原始正文，再官方成熟方案；核对适用前提，合格即停。
- **资源分派**：用四列表中真实缺口选择能力，再按原路由合同选资源、模型与力度；只适配差异。
- **成果验收**：读取实际成果与回执，对照原成功态；未知证据保持 UNKNOWN，不以关键词或完成自述判通过。
- **失败修复/返工**：更新同一四列表，有新证据才改一个明确因素；复测原失败对象并回归受影响能力，不降标准。
- **经验复用**：仅把实测成功部分连同来源、版本、边界与证据写入最近使用记录；下一任务先查该记录与失败复盘。

短任务直接完成，只保留必要紧凑记录，不强制网页、表格展示、四个文件、多智能体或逐步确认。

## 固定决策顺序

1. 尊重用户明确指定的执行者、档位或强度；若不可用、不安全或明显无法满足质量，说明原因后选择最接近的成熟替代。
2. 识别硬要求：真实网页、登录态、上传下载、并行独立工作、指定 Reasonix、外部副作用或人工确认。
3. 选择最低充分档位：`经济档 / 标准档 / 高质量档 / 极限档`。不因任务篇幅长就自动升档；看推理复杂度、错误代价、可验证性和工具链。
4. 只选择一个主执行路径。子代理、浏览器和复核均为按需能力，不默认启用。
5. 执行后检查用户要求和可观察结果。质量未达标时允许一次有依据的升级或成熟回退；同一执行器、同一根因不得循环重试。
6. 返回任务结果。除非用户要求审计，不输出冗长的内部路由过程。

需要作出档位、执行者或强度选择时，读取 [路由合同](references/routing-contract.md)。涉及图片、视频、音轨或文件移交时，按需读取 [已实测媒体交接](references/multimodal-handoff.md)，按真实附件能力选择资源，并分别验收送达、理解、加工、回传和字节保真。

## 核心执行器

- **Codex 主智能体**：默认执行路径；适合普通问答、分析、编码、文件处理和总流程控制。
- **Codex 子代理**：仅在任务可独立并行、需要隔离取证或独立复核时使用；不能只为显得复杂而启用。
- **Reasonix**：仅通过既有官方入口 `reasonix run`；适合低风险、边界明确、输出容易验收且成本敏感的任务。不可用时回退 Codex。
- **Playwright 原生 AI 浏览器**：仅在任务必须操作真实网页、登录态、上传下载或取得浏览器证据时调用既有成熟技能；不得用普通网页摘要冒充浏览器执行。
- **人工确认**：付款、发布、删除、敏感写入、登录授权或其他重大外部副作用必须在动作前确认。

不得增加 Omnigent、ACP、ACPX、数据库、常驻服务或新的执行器包装器来完成普通路由。

## 最小路由输出

需要显示路由决定时，只输出：

```text
ROUTE_TIER=<ECONOMY|STANDARD|HIGH_QUALITY|EXTREME>
PRIMARY_EXECUTOR=<CODEX|CODEX_SUBAGENT|REASONIX|PLAYWRIGHT|HUMAN_CONFIRMATION>
REASONING_EFFORT=<LOW|MEDIUM|HIGH|MAX>
WHY=<一条可验证的选择理由>
FALLBACK=<NONE|CODEX|HUMAN_CONFIRMATION>
```

执行任务时，不得以这五行代替用户真正需要的结果。

## 成本与质量门禁

- 先满足任务的硬能力和质量底线，再比较成本。
- 没有可信价格或额度证据时，不编造精确费用；只使用 `较低 / 常规 / 较高 / 最高合理` 的相对判断。
- 简单任务不得默认启动子代理、浏览器或二次复核。
- 高风险任务不得为了省成本降到无法可靠完成的执行器或强度。
- 新增执行器、自动学习、持续监控和精确计费均不属于 2.0 Core；只有出现真实缺口并完成成熟复刻四列归因后，才可进入后续版本。

## 失败与回退

- 先区分 `MISSING`、`EXISTING_BUT_BYPASSED`、`FALSE_POSITIVE`、`EXTERNAL_FAILURE`、`UNVERIFIED`，不要把外部网络或测试器故障写成路由器功能失败。
- 首选执行器失败时保存原始错误；只有换路径能改变根因时才回退一次。
- Reasonix 失败可回退 Codex；Playwright 失败只有在用户并不要求真实浏览器证据时才能改用非浏览器结果，否则明确报告阻塞。
- 权限、付款、登录或敏感动作不能用自动回退绕过人工确认。

发布、安装或升级验收时读取 [验收合同](references/acceptance-contract.md)。从 1.0 升级、保留旧版或回退时读取 [迁移与回退](references/migration-and-rollback.md)。需要核对本版复用来源时读取 [成熟基线](references/mature-baseline.md)。

