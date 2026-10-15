---
name: artificial-single-page-extreme-time-engine
description: 《三人行》第2版已全局激活的当前正式入口。GPT担任CEO先虚拟成熟与冻结，按需复用Codex Ultra连续运行层执行及现实验收，故障由GPT差分分析后重新验证；兼容明确指定的旧A/B路线及冻结任务METHOD_REF。
---

# 《三人行》第2版｜全局正式激活裁定（2026-10-16）
DEFAULT_METHOD=SANRENXING_V2
STATUS=FROZEN_ACTIVE
ACTIVATION_ID=SRX-V2-C002-GLOBAL-ACTIVE-20261016
SOURCE_FREEZE_ID=SRX-V2-C002-SAVED-F001
METHOD_REF=skills/artificial-single-page-extreme-time-engine/method-freezes/SANRENXING_V2_C002_F001_20261012/SANRENXING_V2.md@78ffb94c4cacd07662b83a59042bc0fe3e7f69e7
METHOD_SNAPSHOT_COMMIT=78ffb94c4cacd07662b83a59042bc0fe3e7f69e7
ACTIVATION_SCOPE=NEW_TASKS_AND_UNPINNED_SANRENXING_REQUESTS
LEGACY_TASKS=KEEP_EXISTING_METHOD_REF
GLOBAL_FINAL_VALID=NOT_CLAIMED

用户明确批准第2版作为全局默认方法。本激活裁定优先于第2版冻结源文件内历史的 REVIEW_PENDING_NOT_ACTIVE / FROZEN_SAVED_NOT_ACTIVE / DEFAULT_METHOD=V1 标志，但不篡改冻结原件、Manifest、测试证据或其有限验收结论。正式加载一律读取上述固定提交的 C002 冻结正文及配套兼容矩阵；原第25版执行大脑、任务合同正反约束与全部旧文件继续按适用条件继承，出现遗漏读原文，以不降低硬约束为准。旧任务继续固定自身 METHOD_REF 与 TASK_STATE_REF，明确旧A/B路线沿用自己的ROUTE；仅用户显式授权的任务迁移才更新其指针。Exactly-once、安全授权、必要Freeze与独立回读不变。方法激活不等于未测试功能实际通过。

---
# 自动化A/B极限短时间引擎：标准稳定入口

用户说“使用自动化B极限短时间引擎完成【任务】”时**直接选择B路线最新版本**；说“使用自动化A…”则直接选A；只说“使用自动化A/B引擎”才按最终有效时间与任务形态选择。第一步从网络权威仓库读取同目录 `START_HERE.md`，禁止先去C盘找方法。它按固定 `routes/A/ROUTE.md` 或 `routes/B/ROUTE.md` 读取最新版；接续任务只读该TASK_ID专属CURRENT指针，用户不必手动提供版本。

GPT始终负责实际规划、执行、纠错、质量验收与持续推进；n8n、Dot、Codex、Playwright MCP、Windows桥只在确有必要且权限允许时提供成熟状态/连接/代码工具等能力。卡点修复后继续原任务，到合同 DONE_WHEN、合法冻结或可证实BLOCKED才停止。

A/B 只比较完成**同一实质成果**的完整有效时间；A派发合并、B重新建页重新理解都属于全链路成本，不得以局部成本作结论。持久化必须有真实写入确认，未经授权不做有副作用的业务发送；不得将虚拟计划当成现实成功。

权威仓库：`cuiqinggang/codex-private-skills`；本文件仅作为稳定加载入口，不硬编码可能变动的版本号或单个任务冻结号。

## 持久化故障自动分流门（默认执行，不等用户提醒）

每当本任务需要保存、更新、发布技能文件或冻结状态，而写入未成功时，**立即自动进入此门**，不得只答复“写入失败”就结束任务。此门是已有 GitHub Contents API 成熟方法的触发器，不新增系统、不绕过任何限制：

1. **判定失败发生的层次**。区分 A. 还没向工具发起有效调用／参数或路径错误，B. GitHub 返回常规 HTTP 错误，C. 工具调用返回未知（查明提交是否已存在，禁止重复写入），D. 平台明确拒绝这一具体请求。记录原始返回而非猜测。
2. **A/B 类按官方路径完成诊断**：只读检查仓库权限、分支、目标文件是否存在和 SHA；按官方 Contents API 的 create_file/update_file 契约核对参数。对于真实 409/422，核对冲突与字段后才允许受控重试；提交后独立回读正文与 commit SHA。
3. **区分通道健康和内容获准**：如果不是针对同一受阻动作的安全拒绝，可以对独立无害的测试文件进行一次正常官方 create→read 检查，确认连接和权限。测试成功**仅能证明通道健康**，不得以此重提明确遭拒的相同动作。
4. **D 类尊重限制**：若平台明确拒绝某一具体请求，记录其范围、错误、时间及当前仓库状态；不换工具、改凭据、拆分内容、改写等价意图重复提交以规避限制。允许继续无副作用诊断和其他不受影响的任务；必要时提交正常支持审核。
5. **修复后自动继续原任务**：非安全拒绝故障一旦恢复，执行原合同后续步骤直到 DONE_WHEN；回读通过前不得宣称已发布。每次报告写清已尝试的官方动作、返回、下一步，不以“我记住了”代替物化证据。

本门专门修复历史反例：先前曾仅检查 GitHub push 权限便停止，直到用户再次要求才进行了无害 Contents API 小文件创建与回读（commit `db04c118276bfe6e41fa89ee107cf2c7f42242a9`，PASS）。**今后必须主动完成适用的分流，而非等待催促。**

## GitHub官方文件写入与故障判定（已验证成熟方法）

网络权威仓库更新优先使用已连接的**GitHub官方Contents API**：读取目标文件及现有blob SHA → 仅修改必要内容 → 已有文件用 `update_file`（携带原SHA），新文件用 `create_file` → 记录返回的commit SHA → 再从正式仓库独立回读，核对版本、正文及路径。不同文件顺序提交，避免多对象组合写入与未知中间态；只有回读通过才声明已持久化。

原始真实证据与边界：`method-freezes/ENGINE28_TIME_BASELINE_FIRST_FREEZE_20261010.md` 第3、5节。历史Git Data `create_tree` 在平台**预派发安全检查**遭拒，官方Contents API则曾成功写入28版引擎和25版大脑，但这**不意味着**Contents API能绕过相同平台安全限制。遇实际GitHub HTTP409/422时仅按冲突/参数规则核对；遇ChatGPT/OpenAI预派发拒绝，记录原文、时间、目标和主分支是否变化，停止该被拒绝动作，不通过换工具、拆分同一受阻意图或改用其他凭据规避，必要时走正规支持审核。

特别注意：**当前第29版统一方法尚未正式激活**；在`ENGINE.md`、`START_HERE.md`完成真实获准发布并回读之前，入口仍以仓库实际文件状态为准，不能将任务合同或冻结声明为统一29版已上线。
