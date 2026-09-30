# JARVIS v1 — STATE=10 资料整合与候选能力地图 R1

页面：贾维斯版本2  
项目：JARVIS v1.0  
母方法：整体闭环极限短时间引擎 v5.6.5  
阶段：STATE=10 / RESEARCH_INTEGRATION_ONLY  
VIRTUAL_MATURE=NO  
FREEZE=NO

> 本文件只做资料收集、逻辑推理、整合、分析与候选职责映射。不是虚拟成熟，不进入20，不代表任何新组件已部署。

## 1. 目标

把已经存在的成熟能力与现实证据拼成一套最小 JARVIS 候选能力地图，回答四件事：

1. 哪些能力已经有现实证据；
2. 每个能力最适合承担什么职责；
3. 哪些只是备份/参考，不应进入固定主链；
4. 下一阶段真正需要验证的最小系统级问题是什么。

原则：DISCOVER → COPY → ADAPT → COMPOSE → VERIFY。  
大道至简：不因为“有很多工具”就把所有工具塞进每个任务。

## 2. 证据等级

- A = 用户环境中有 Reality/真实运行证据，可直接作为候选职责依据；
- B = 历史成熟资产/组件级证据充分，但尚未作为 JARVIS 整体联通；
- C = 当前公开产品能力，尚未在用户环境验证；
- D = 仅概念/未知，不进入候选主链。

## 3. 核心模块结论

### 3.1 Manus 2.0
证据：A。R1-R10 已统一归档。  
用途：云端长任务、多Agent编排、浏览器执行、研究、普通故障恢复。  
边界：硬隔离、真实权限、假完成抵抗、自验证、跨平台交付仍部分；跨天/重启/断电/供应商失效未证实。

候选定位：
- LONG/CLOUD EXECUTOR
- MULTI_AGENT MANAGER
- SECONDARY BROWSER EXECUTOR

不建议定位：
- 唯一总控
- 唯一Verifier
- 唯一状态存储
- 唯一灾备

### 3.2 JEV-native Playwright R3 编译热态版
证据：B（组件 Reality 已有 30/30 VALID）。  
技能 ID：playwright-native-ai-browser  
权威目录：C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser  
历史 Reality：
- MIN 272.98 ms
- P50 304.46 ms
- P95 424.48 ms
- MAX 448.97 ms

用途：确定性浏览器动作、已登录态网页操作、作为本地/专用浏览器主候选。  
边界：这些是组件先验，不是 JARVIS 整体 T*。

候选定位：
- PRIMARY DETERMINISTIC BROWSER EXECUTOR

### 3.3 DSE v1.0.3
证据：A。正式定位：LIGHTWEIGHT DECISION GATE。  
Runtime：DEFINE → FACT → COMPARE → DECIDE。  
Reality：6/6 VALID，6项安全违规计数全部0。  
T_FLOW=960449.004 ms；T_VALID 尚未独立认证。

用途：仅在自动流程遇到权限/选择/继续停止等决策点时调用。  
禁止扩张成 Planner / Executor / Verifier / Recovery / Workflow Orchestrator。

候选定位：
- DECISION GATE ONLY

### 3.4 n8n
证据：A/B 混合。
历史真实部署：
- n8n 2.38.7
- localhost:5678
- 持久化卷 n8n-local_n8n_data
- artifacts: C:\AI\n8n\artifacts
- 已有真实 workflow 与 Reasonix/DeepSeek artifact 闭环资料

现实资料包：
- N8N-EVIDENCE-20260928-01
- C:\AI\n8n-evidence\N8N-EVIDENCE-20260928-01
- ZIP SHA256 8abe5dcc194a81ad01789d01a4812d617c403df9777a28e87a2a25105f8bc67f

已确认成熟链：
n8n → 8788 adapter → Reasonix → DeepSeek → artifact → n8n verifier → response

注意：采集时 8787/8788 未监听，execution 表为空；这表示当前运行态未知，不抹掉历史能力证据。

候选定位：
- AUTOMATION / DAG CONTROL PLANE
- SCHEDULING / RETRY / EVENT ENTRY
- 不作为每个任务固定跳点

### 3.5 Codex
证据：A/B。
- 已有真实 GPT→Codex 派发、收件、执行与时间证据；
- GPT-Codex Orchestrator v1.5.2 具 Path A/B/C、transport、简单 recovery 资产；
- 旧 orchestrator 不能接管当前 v5.6.5 状态机；
- Codex 不得自行宣布100，Reality 后应回 GPT/JARVIS 最终审核。

当前公开产品还支持 Windows Computer Use / Browser Use，可见、点击和输入 Windows 应用；这是 C 级当前产品能力，尚未计入用户环境的 JARVIS Reality。

候选定位：
- PRIMARY LOCAL CODING / FILE / CLI EXECUTOR
- LOCAL WINDOWS EXECUTOR 候选
- 复杂实现与修复执行器

### 3.6 Reasonix / DeepSeek / DSH
证据：B。
历史 JARVIS Personal AI OS 已定义标准任务包：
DSH_TASK_READY + 唯一 task_id → 本地接力 → DSH/Reasonix → DeepSeek → 测试/修正 → 结果回收。

已确认原则：
- DSH 可用时 dsh --profile headless；
- DSH 当前成熟度不足时，切 Reasonix/其他成熟执行端，不投入大量插件开发；
- Reasonix 可承担 DeepSeek Flash/Pro 与工具执行；
- 同 task_id 只发送一次；超时不盲重发。

DeepSeek V4 Pro 另有已验证备份路径：
DeepSeek API → CCX localhost:13000/v1 → CC Switch/Codex provider → deepseek-v4-pro。
它证明“非 OpenAI 模型/provider”可用，但若依赖 Codex 客户端，不等于完整的“OpenAI 产品全部失效灾备”。

候选定位：
- LOW-COST / NON-OPENAI MODEL EXECUTION
- OpenAI 模型不可用时的第一层备份
- 完整 OpenAI 产品不可用时，应优先走 Reasonix/本地接力而非 Codex UI

### 3.7 状态与恢复
已有成熟事实：
- GitHub 共同工作区可保存权威证据与接续状态；
- n8n 有持久化卷与 artifact；
- Manus 有同 Project 连续性但长期状态只 PARTIAL；
- JARVIS Personal AI OS 已定义 JSON/Markdown 状态文件与 task_id 去重；
- 历史还有 restart/resume 与 Hermes 恢复型技能/备份资产。

大道至简结论：
当前不需要新增 Redis/Postgres/大型状态服务作为 JARVIS 前置条件。

候选定位：
- AUTHORITATIVE PROJECT STATE = Git/GitHub workspace
- RUNTIME TASK STATE = JSON/Markdown task ledger + task_id/idempotency
- WORKFLOW STATE = n8n persistence when n8n is used
- EXECUTOR CHECKPOINT = task-specific checkpoint/artifact

### 3.8 Verifier
现实教训：
- Manus SELF_VERIFICATION=PARTIAL；
- Codex 不得自签100；
- v5.6.5 已采用原始证据 + SHA256 + GPT最终审核语义；
- n8n 旧链已有 Code verifier，后续虚拟候选移除了单纯 verified=true 权威。

大道至简结论：
不新造“Verifier 平台”。Verifier 是一个独立职责层：

1. deterministic acceptance / schema / hash / oracle；
2. 执行器原始证据；
3. 非执行器的最终审核者。

候选定位：
- PRIMARY = deterministic verifier + JARVIS controller final audit
- EXECUTOR SELF-CHECK = 只作辅助，不作为最终权威

## 4. 最小候选职责图（非冻结）

USER / ChatGPT-JARVIS Controller
        |
        +-- DSE v1.0.3（只在需要决策时）
        |
        +-- n8n（只有需要调度/DAG/定时/事件时）
        |
        +-- EXECUTION ROUTE
        |     +-- Codex：本地编码/文件/CLI/复杂实现
        |     +-- JEV-native：确定性浏览器
        |     +-- Manus：云端长任务/多Agent/动态浏览器
        |     +-- Reasonix + DeepSeek：低成本/非OpenAI模型路线
        |
        +-- STATE
        |     +-- Git/GitHub 工作区
        |     +-- task ledger / artifact / checkpoint
        |     +-- n8n persistence（仅n8n任务）
        |
        +-- VERIFIER
              +-- deterministic checks
              +-- raw evidence + SHA256
              +-- JARVIS final audit

核心原则：
- 简单任务：Controller → 单一执行器 → Verifier；
- 只有需要时才插 DSE；
- 只有需要 DAG/定时才插 n8n；
- 只有复杂云端任务才上 Manus；
- 只有网页动作才上 JEV/Browser；
- 不把全部组件串成固定流水线。

## 5. 灾备分层

### L1：OpenAI 模型不可用
Reasonix / DeepSeek 或 DeepSeek API 路线。已有成熟证据基础。

### L2：OpenAI 产品/客户端不可用
目标候选：
local relay / n8n → Reasonix → DeepSeek → artifact → deterministic verifier。
这条才是真正应承担“OpenAI 产品不可用时仍能继续核心工作”的候选路径。

当前状态：结构与历史组件资料存在，但还没有作为 JARVIS v1 做整体认证。

### L3：本机重启/机器故障
已有 restart/resume 与历史恢复资产可复用，但 JARVIS v1 尚未形成统一恢复合同。

## 6. 当前外部成熟方案扫描（2026-10-01）

### OpenAI Dots
公开资料显示 Dots 是 always-on agent，可跨应用长期追踪目标并与 Codex/ChatGPT Work 等能力结合。
判断：REFERENCE_ONLY。
原因：
- 对长期个人助手架构有参考价值；
- 但它属于 OpenAI 供应商本身，不能解决“OpenAI不可用”灾备；
- 用户当前 JARVIS 已有更细粒度、可控、可替换组件，不应因新品发布立刻重构。

### Meta Muse
公开资料显示 Muse 采用隔离云端 Linux VM / sandbox 形态，并可执行终端类任务。
判断：BACKUP_CANDIDATE / REFERENCE_ONLY。
原因：
- 可作为未来独立云执行器/灾备供应商候选；
- 当前没有用户环境 Reality，因此不进入主链。

### Codex Windows Computer Use
OpenAI 官方当前文档显示 Codex 已支持 Windows Computer Use、Browser Use 和远程继续任务。
判断：LOCAL_WINDOWS_CANDIDATE。
原因：
- 可能减少自建 GUI 接力器工作；
- 但目前只算公开产品能力，尚未替代用户已有 JEV/本地成熟资产。

外部扫描结论：没有发现必须立即推翻当前 JARVIS 候选结构的新能力。

## 7. 目前真正的最小缺口

### G1 — 角色接口合同
需要在下一阶段明确：
- Controller 给 Executor 的最小 Task Contract；
- Executor 返回的 Result Contract；
- State / checkpoint 最小字段；
- Verifier 输入与最终结论字段。

这属于“完整候选定义”，不是新系统开发。

### G2 — 当前运行态绑定
以下资产有历史证据，但 JARVIS v1 尚未统一确认“当前可调用入口”：
- JEV-native 本地入口；
- n8n / 8788 adapter；
- Reasonix；
- DSH（若保留）；
- Codex Windows Computer Use（若采用）。

这不是资料不足，而是未来 Reality/environment binding 问题。

### G3 — 完整非OpenAI灾备闭环
需要最终证明：
OpenAI product unavailable
→ local/n8n
→ Reasonix/DeepSeek
→ artifact
→ deterministic verifier
→ result

当前属于候选，不应在STATE=10资料阶段假装已通过。

### G4 — JARVIS系统级恢复
需要定义最小恢复对象：
- task_id
- last valid state
- checkpoint/artifact path
- executor route
- retry/idempotency status
- next safe action

不需要先建设重型状态数据库。

## 8. 已经不再属于“资料缺口”的问题

以下资料已经足够，不应继续搜索到无穷：
- Manus 一般能力；
- JEV 浏览器组件速度与有效性；
- DSE 是否可用；
- n8n 是否具有成熟控制平面基础；
- Codex 是否可以承担本地执行；
- DeepSeek/Reasonix 是否存在非OpenAI模型执行路线；
- 是否必须新增大型数据库/总线/第二套复杂看板。

## 9. 本轮结论

STATE=10 保持不变。

资料/逻辑整合结论：
- RESEARCH_SUFFICIENT_FOR_CANDIDATE_MAP=YES
- COMPONENT_ROLE_MAP=PRODUCED
- MINIMUM_GAPS=IDENTIFIED
- NEW_MANUS_TESTS_REQUIRED=NO
- NEW_HEAVY_INFRA_REQUIRED=NO
- VIRTUAL_MATURE=NO
- FREEZE=NO

下一步仍在 STATE=10，但已经从“资料搜索”进入：
**完整候选接口定义 / Candidate Contract Draft**

它仍不是虚拟成熟。完成接口合同后，才具备开始系统级虚拟成熟的输入条件。
