# 《三人行》第4版｜低新增成本 Gemini 条件并行执行（冻结发布）
VERSION=SANRENXING_V4
FREEZE_ID=SRX-V4-F001-20261019
STATUS=FROZEN_PUBLISHED
DEFAULT_METHOD=SANRENXING_V4
PARENT=SANRENXING_V3.md
WINDOWS_BRIDGE=skills/gpt-windows-execution-bridge/SKILL.md@V10.0
LEGACY_TASKS=KEEP_PINNED_METHOD_REF
GLOBAL_FINAL_VALID=NOT_CLAIMED

## 0. 继承与目标
完整继承《三人行》第3版（包含第2版 C002 固定继承、GPT CEO 主执行、Orca 按需、Exactly-once、质量门、连续修复、T*=min(T_VALID)、历史冻结）和 Windows 执行桥 V10 C→A→B 路由。不修改已冻结的 V3 或已固定旧方法的任务。不重建浏览器或调度器，不更改 FlClash、代理和登录 Profile。

## 1. 唯一新增执行路线（条件启用）
GPT CEO 判断一批任务能否独立并行、是否有可核验的 DONE_WHEN；普通任务仍 GPT 自执行，只有能获得净收益才派发。Gemini 官网已登录且账户权益允许、浏览器/正式 MCP 及目标页健康、任务可安全提交、额度可用、质量验收可完成时，启用 GPT→C→已存在 Playwright 专用浏览器→Gemini 官方网页的多任务路线。
- 默认候选并发=3 个独立 Gemini 页面。只有独立任务不少于6、环境健康且预计净收益为正，才可选6并行；2并行是较低资源起点。不是必须每次启动3或6个，不是无限并发授权。生产默认是候选策略，批量多轮稳定性及账户额度长期评估仍未认证。
- 每项任务唯一 marker、独立页面和质量合同。按可用的原 Profile/CDP owner，通过正式技能及成熟会话协议执行，单任务最多发送一次；UNKNOWN 先只读对账，不重复发送。GPT 收完整答案、代码/表格，独立运行验收；失败单项按成熟 REUSE_GATE 修复，必要时转 GPT 自执行或现有 GPT→Codex V5，避免耗费 Codex 额度。
- **Gemini 不可用时直接跳过本分支**：账号未登录、权益不足、限额、页面异常、工具不可调用、环境无法在合理时间内恢复、任务质量不达标或合规限制；保持 GPT 自执行/C 通道优先，必要时再按成熟净收益路由至 Codex。Gemini 不是 Windows C/A/B 的故障替代通道；C/A/B 仍是连接链路。
- 不依赖“云端电脑”是否存在；以最终可验证的业务成果、完整有效时间、成功率与额度为准。不得假设多标签必然并行或订阅份额无限。
- 单任务流程：输入合同→必要现实基线/物理下界→成熟方案→派发→等待/只读恢复→回收→独立QA→记录 T_VALID。适合极限方案的问题可选 UltraFusion 6.1B 多视角，但不强制每个任务经过九方案。

## 2. 现实验收（2026-10-19，首次容量实测）
专用浏览器本机正式证据：C:\AI\Playwright-Native-AI-Browser\reports\GEMINI-PARALLEL-2-3-6-ACCEPTANCE-20261019.md，原始 JSON 同目录。
- 两任务并行：78178ms；2/2 合格，原始单元测试 8/8 PASS。
- 三任务并行：62195ms；3/3 合格，测试 12/12 PASS。曾在发送前发生 CDP attach 超时，页面目标恢复后才成功；此恢复成本未计入 62195ms。
- 六任务并行：120044ms；6/6 合格，测试 24/24 PASS；完整派发到第六任务约28456ms。六并行与三并行不同批次、不同任务组合，吞吐比约仅3.6%净提升，不能直接宣称长期加速倍数。
- 先前同类复杂 DAG 编码：Gemini Argon 106863ms，pytest 12/12 + 独立4/4；Codex CLI gpt-6.1-sol Medium 246063ms，pytest 27/27 + 独立4/4。Codex 受服务重连及本地写盘/环境检查影响；单轮不能证明纯模型速度普遍差异。

## 3. 状态、成本及复发处理
每批记录 TASK_ID、marker、页面 URL、时钟起止、发送时刻、独立质量验收、完整 batch T_VALID、额外人工干预、额度/拒绝/排队、失败及首次差异。任何用户已发送且回执未知的操作禁止重发。
若 Playwright connectOverCDP 在 9223 WebSocket 已接通后超时，按原浏览器技能包 references/V1.1-STALLED-TARGET-RECOVERY-20261018.md 先逐个只读探测页面 target 是否无响应；不清理 Profile、抢占 owner、乱关用户正在编辑的页面。不得只因为 /json/version PASS 就认定会话健康。
无论本方法是否冻结，单批 QA PASS 不等同跨会话断点恢复、长期稳定性、账户每日任务限额或总体商业生产 FINAL_VALID 全部通过。

## 4. 加载与生效
正式入口：同目录 SKILL.md 和 START_HERE.md 顶部 V4 指针；新任务默认生效。加载本文件→V3正文及其既有依赖→Windows V10正式入口→按任务需用原专用浏览器 canonical skill。不可自动改动任何旧任务已固定 METHOD_REF。用户明确要求 V3 时仍按 V3。

## 5. 三轮自动成熟闭环（2026-10-19 增补）
新任务默认同时读取 `SRX_V4_THREE_ROUND_AUTOLOOP_20261019.md`。按 S0-S9 固定状态流程执行，最多三轮优化；持续自主恢复与验收，遵守 V10 C→A→B 路由。该增补目前是已落盘规则，端到端自动恢复验收通过前不得声称生产闭环已上线。
