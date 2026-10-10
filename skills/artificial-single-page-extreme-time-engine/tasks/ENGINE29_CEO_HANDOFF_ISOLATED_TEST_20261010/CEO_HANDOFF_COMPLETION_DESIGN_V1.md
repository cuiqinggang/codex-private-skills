# 第29版 GPT CEO 自动接续｜剩余设计完备版 v1（只读、未激活）
STATUS=DESIGN_COMPLETE_NOT_DEPLOYED
MODE=TEST_ONLY
METHOD=ENGINE28/BRAIN25/TEMPLATE18; ENGINE29=PROPOSED_NOT_ACTIVE
TASK_ID=ENGINE29_CEO_HANDOFF_ISOLATED_TEST_20261010
FREEZE_ID=ENGINE29-CEO-ISOLATED-F001
REPO=cuiqinggang/codex-private-skills
CURRENT_PATH=skills/artificial-single-page-extreme-time-engine/tasks/ENGINE29_CEO_HANDOFF_ISOLATED_TEST_20261010/CURRENT.md
FREEZE_PATH=skills/artificial-single-page-extreme-time-engine/tasks/ENGINE29_CEO_HANDOFF_ISOLATED_TEST_20261010/ENGINE29-CEO-ISOLATED-F001.md
HANDOFF_PROMPT_SOURCE=skills/artificial-single-page-extreme-time-engine/tasks/ENGINE29_CEO_HANDOFF_ISOLATED_TEST_20261010/CEO_HANDOFF_V2_READONLY.md
FINAL_VALID=NO

## 目标和保留的既有成果
只补全“旧 CEO Freeze → 合法新聊天接管 → 精确文件回读 → 接续确认 → 下一轮”的设计；不涉及 Reasonix、8788 或新 n8n 编排。F001 的自动发送和收到回复为已有局部实测；新 CEO 独立读取 Freeze 尚未得到可归属的新会话读取证据。F002 的发送操作遭平台安全拒绝，因此不得使用 CDP、Playwright、UIA、n8n、脚本或其他调用方式重放这一被拒动作。

## 输入与唯一状态
1. 原任务保持单一 ACTIVE_CEO；CURRENT 是动态索引，不覆盖历史 F001。TASK_ID、FREEZE_ID、MODE、阶段、OWNER、NEXT、证据定位是必需字段。
2. 当前已回读的 GitHub 原始 F001 文件与 CURRENT 必须互相匹配，且 TEST_ONLY。禁止只凭一条简短状态码猜路径。
3. 不将本设计文件写成公共 ENGINE29 已激活；不修改 ENGINE.md、BRAIN.md、路线所有权、浏览器登录态或旧 F001。

## 一次交接的全流程
A. 旧 CEO 先将当前任务状态用 GitHub 官方文件 API 提交 Freeze；随后按精确路径再次读取，校验 TASK_ID/FREEZE_ID、真实 SHA 与 NEXT；写入 CURRENT 指向同一 Freeze 后同样回读，才标记 PREPARED。
B. 仅在正式允许、能够明确控制独立测试会话且具有目标标签所有权的自动启动/提交能力已实际可用时，使用 CEO_HANDOFF_V2_READONLY.md 中的单次提示词启动新 CEO。没有该能力时保持 PREPARED_NOT_SENT，不得假定已提交。
C. 新 CEO 必须自己通过 GitHub 连接器按精确路径 fetch_file 读取 CURRENT、对应 Freeze，独立校验两个文件的 TASK_ID/FREEZE_ID、TEST_ONLY 和 SHA，并在新会话保存可回读的工具证据；仅复制了“接续确认”字样不算 READ_PROOF。
D. 新 CEO 回传包含 TASK_ID、FREEZE_ID、读取证据路径/提交 SHA、接管状态的确认；旧 CEO 核查回执后才允许转移 ACTIVE_CEO，旧页只可按既有授权安全退役。确认失败旧 CEO 保留、不得关闭。
E. 下一轮在新任务节点完成时重复 A-D，至少两次有效交接才视为 CONTINUOUS_HANDOFF_PASS；每轮使用新 Freeze ID、独立可追溯的发送 ID 和新会话标识。

## 不可省略的失败分支
- 文件缺失/SHA 变化/索引不一致：STOP_HANDOFF，恢复到最近一次已验证 Freeze，不发送。
- GitHub 写入成功但回读未知：先查提交记录和文件 SHA，禁止盲目重复写。
- 新聊天发送未知：通过同一合法接口查询提交/会话结果，禁止自动重发。
- 新会话只回复确认但没有新会话 fetch_file 证据：READ_UNPROVEN，不能接管。
- 两个 CEO 同时尝试写 CURRENT：停止交接并按现有唯一所有权合同恢复，禁止自行实现锁/调度器。
- 正式发送入口缺失或平台拒绝：SEND_BLOCKED_AUTHORIZATION；仅保留已有只读工作，不得通过别的工具绕过。
- 不同会话来源证据混用：EVIDENCE_MISMATCH，禁止合并 PASS。

## 最小现实验收用例（独立隔离测试，不做真实业务发送）
R1：旧 CEO Freeze 提交+回读成功，CURRENT 指针一致。
R2：由平台明确允许的自动化入口一次创建全新测试聊天并提交 V2 一次；记录会话 ID、提交结果、时间。
R3：在 R2 新聊天中真实按路径 fetch_file 两份文件，留下可归属该会话的工具读取证据，并正确回复“CEO接续测试确认”。
R4：旧 CEO 核对接收证据并确认新 CEO 接管；从新 CEO 进行第二轮 R1-R3，完成连续交接。
R5：注入一次缺文件/不一致/重复发送未知场景，验证停止并不误发、不丢最后合法 Freeze。
PASS_GATE=R1..R5全部有真实可回读证据 && 没有未经许可的聊天发送 && 无错误覆盖。
时间从 TASK_ACCEPTED 到可验证回执；未知记 UNKNOWN，不编造秒数。

## 现在实际状态与下一动作
DESIGN=COMPLETE
GITHUB_F001_CURRENT_FREEZE_READ=PASS（旧会话/本次会话的只读验证）
F001_HISTORICAL_SEND_REPLY=PARTIAL_PASS
NEW_CEO_OWN_SOURCE_READ=NOT_PROVEN
AUTHORIZED_AUTOMATED_MESSAGE_ENTRY=NOT_CONFIRMED
R2_TO_R5=NOT_TESTED
FINAL_VALID=NO
NEXT=只在正式允许的独立聊天自动启动/发送能力可被核实后运行 R2→R5；否则保留冻结并可继续做其他合法只读工作。
