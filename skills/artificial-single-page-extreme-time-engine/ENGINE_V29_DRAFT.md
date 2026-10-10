# 《自动化单页面极限短时间引擎》第29版｜双执行者与弹性三级拓扑（待验收草案）

VERSION=ENGINE29_DRAFT
STATUS=PROPOSED_NOT_ACTIVE
DATE=2026-10-10
AUTHORITY=cuiqinggang/codex-private-skills/main
INHERITS=ENGINE.md@28; BRAIN.md@25; routes/A/ROUTE.md@A29; routes/B/ROUTE.md@B33
T_VALID_REAL=UNKNOWN
VIRTUAL_MATURE=NO
FINAL_VALID=NO
ACTIVATION=FORBIDDEN_UNTIL_PASS

> 本文件是用户已批准记录、尚未通过对照验收的第29版候选规则，不是公共 ENGINE29 已发布。当前唯一公共总纲仍为 `ENGINE.md` 第28版，A路线已激活 A29 专用浏览器布局，B路线仍为 B33。不得改旧任务 METHOD_REF / TASK_STATE_REF、稳定路线指针或原浏览器所有权。

## 1. 唯一目标与角色选型

唯一标准 `T*=min(T_VALID)`，前提是同一个原始任务、同样输入、同样成功验收、相同授权和安全约束。任何局部执行、模型速度、页面数量、Agent 数量均不能单独代表极限总效率。

**GPT 与 Codex 都是合法的并行任务执行和验收候选者。** 默认由 GPT CEO 作统一任务规划、自然节点划分、证据审核与全局归并，但不能因为偏好 GPT 就免除 Codex 作为 CEO/规划者或独立执行者的对照；不能因为 Codex 强于编码就预先宣布它在总流程更快。

每个候选都要纳入相同的实际质量和总时间对比：
- **G（GPT主导）**：GPT 规划、执行、审查；按需使用现有技能包与获准工具。
- **C（Codex主导）**：Codex 规划、分派、执行、审查；受现有工具、授权、上下文和文件权限约束。
- **H（混合）**：GPT CEO 统筹、执行有优势的节点，Codex 按需承担代码实现、静态审查、专项检查、异常定位及并行任务协调；具体切分依据实测而不是固定岗位印象。

同一个任务内允许不同节点选用不同候选。选择时计算 `T_total_valid = 规划 + 派发 + 排队 + 执行 + 工具与模型调用 + 交接/上下文恢复 + 冲突等待 + 故障返工 + 验收 + 用户操作 + 必要的部署维护摊销`，并明确版本、样本、运行次序与测量单位；未知则为 UNKNOWN，禁止编造倍率或置信度。

## 2. 最少必要页面与三级上限

- **普通任务**：默认现有已登录专用AI浏览器中的单一 GPT CEO 页面自行完成一个自然节点；当前页健康时不强制新页或下级执行页。实际任务已有效完成即可结束，不必人为制造换页。
- **较大任务**：仅在确认可独立、上下文隔离或并行有总净收益时，按需创建少量 Executor 页面；可以分配给 GPT 或 Codex。每个节点单独 TASK_ID/NODE_ID/OWNER/输入/输出/验收/冻结，回传证据并归并。
- **特大型任务**：允许**最多三级责任拓扑**：一级总 CEO → 二级模块 CEO（例如3个）→ 三级具体 Executor（每模块可分若干个）。允许二级CEO自己直接执行，不强迫满三级。总CEO唯一更新母任务全局 CURRENT；二级仅写获授权的模块独立状态，三级仅写自己的节点成果，父级只经显式核验合并。不同模块可并行，依赖节点不得伪并行；不在同一父任务上设置多个全局写者。
- 页面复用与换页：自然节点达到合法 DONE_WHEN/STOP_GATE → 先保存并核验 Freeze → 受许可的唯一新页确认接管 → 旧页退役。当前页健康或状态不完整时不切换。不得只因上下文长度、页面数量或模板规定而制造无净收益的换页。
- 同一专用浏览器实例不意味着标签无冲突；共享 Chrome Profile、焦点、剪贴板、同一资源写入及 Cookie 等必须按实际冲突范围隔离。不得改 FlClash 代理、新增浏览器身份，不能关闭其他用户/任务的标签。

## 3. 原生能力复用 / 授权与故障门禁

先使用真实已存在的 SKILL、GitHub 官方 Contents API、Codex 原生子智能体、既有 Windows 执行桥和 Playwright MCP；不得自行开发通用状态机、队列、调度器、资源锁、浏览器控制层或重试系统。每个任务必须先满足 REUSE_GATE。

Codex 可作为监督/审核者，也可作为实际执行者，但**监督不等于具有控制 GPT 聊天或自动发送的授权**。要由 GPT 真正执行，必须已有可核验的获准执行入口与目标标签归属；绝不通过 Codex、CDP、UIA 或其他替换工具绕过 B33 保护锁、之前明确的平台安全拒绝或一次性发送门禁。无法合法自动触发 GPT 新聊天时，明确标记 GPT_BROWSER_REALITY=NOT_TESTED，继续对不依赖该动作的并行事项作只读验收。

Exactly-once 三态保持：CONFIRMED_DONE 不重做；CONFIRMED_NOT_DONE 可受控重做；UNKNOWN 禁止盲重发并保留证据。冻结先于关闭；所有失败可定位、可恢复，不能以无发送的虚拟检查冒充真实多标签运行。

## 4. 同任务对照与并行度实验（只定义合同，未声称完成）

对 G / C / H 三候选分别在可合法复用的同一类真实任务和同一个 DONE_WHEN 下测试，按 **并行度 1、2、4、8** 分别记录成功完成数量、完整批次墙钟时间、单任务延迟分布、重试/冲突、tokens或工具成本。不能只比较首个完成或单轮平均耗时。顺序随机或交叉轮换以减小缓存、网络、模型负载等顺序偏差。取可信重复次数，按用户的真实使用规模衡量部署/维护摊销，不做无意义百万次估算。

同一批样本需分清两类问题：
1. **单任务完工时延**：从 TASK_ACCEPTED 到 FINAL_VALID；并行切分增加合并成本。
2. **多任务吞吐 / 批次有效时间**：从同批 TASK_ACCEPTED 到全部目标 VALID；8路不一定快于4路或2路，须实测。

无相同边界现实基线 `T_BASE_REAL`、可信整体虚拟 `T_VIRTUAL_BEST` 与真实授权最终验证时，`GAIN_PERCENT`、`SPEEDUP`、`T_VALID_REAL` 均记录 UNKNOWN。沿用“现实成熟GOOD基线→物理界限→最多3成熟候选→连续虚拟成熟→STOP_GATE→整套Freeze→最终1次Reality”的总纲。

## 5. 编号任务包：8项可以独立启动，绝不提前声称完成

下列各项可由 Codex 原生多子智能体或多个隔离 CLI 会话并行审核；当涉及 GPT 网页真实执行时，只在获准且唯一归属的专用标签运行。每个任务提交自己的 PASS/FAIL/UNKNOWN、证据、时间和反例，分派成功与节点完成分开计数。

| 编号 | 题目 | 必须验收的差分 |
|---|---|---|
| E29-01 | GPT单CEO简单任务 | 不额外派发/换页，同质量FINAL_VALID与完整时间 |
| E29-02 | GPT多节点自然换页 | Freeze可回读、恢复无历史噪声、非法时拒绝换页 |
| E29-03 | GPT CEO + 1~3执行页 | 标签唯一归属、并行独立性、合并质量/时间 |
| E29-04 | 最多三级大型任务 | 总CEO→3模块CEO→各2执行者，唯一全局写者 |
| E29-05 | Codex专项执行与审计 | 与GPT同质代码/问题解决比对，审查非代替实做 |
| E29-06 | 混合GPT+Codex角色分配 | 兼容单CEO、不同Agent交接和净收益核算 |
| E29-07 | 并发、故障与安全 | 共享浏览器冲突、UNKNOWN、Freeze失败、保护页不误操作 |
| E29-08 | 公平时间实验 | G/C/H × 并行1/2/4/8，同合同T_VALID、吞吐及回滚 |

每个子任务的最小回传字段：`CASE_ID | ACTOR | INPUT_SHA_OR_HASH | TASK/NODE/OWNER | BASELINE | METHOD_REF | TASK_STATE_REF | STATUS(VIRTUAL/REAL) | VALID | T_START/T_END | T_VALID | STRONGEST_COUNTEREXAMPLE | EVIDENCE | NEXT`。若无原始日志或证据，只能标 UNKNOWN / NOT_TESTED。

## 6. 发布、继承与冻结边界

当前只记录候选架构与验收任务：`DESIGN_RECORDED=YES`，`VIRTUAL_MATURE=NO`，`REALITY=NOT_TESTED`，`PUBLIC_ENGINE29_ACTIVE=NO`。

不得因为本草案文件创建成功，就修改公共 `ENGINE.md` 28版版本头、A29/B33 ROUTE、旧任务 CURRENT、B33 PROTECTED_CHAT_HARD_STOP；新公共 ENGINE29 只有在虚拟成熟和对应的合法现实验收后，通过官方Contents API差分发布与独立回读，再由明确的正式入口激活。遇 GitHub 或 Codex 任何安全策略拒绝，仅保留拒绝原文和实际状态，停止该受阻动作，不换通道规避。
