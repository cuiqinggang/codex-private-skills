【playwright浏览器自动化5｜STEP2虚拟99全局收敛｜1】

# Playwright 浏览器自动化5 — STEP 2 Virtual-99 全局收敛命令 v1

CURRENT_STEP=2
STEP_NAME=VIRTUAL_99
METHOD_VERSION=3.1.4
ONLY_OBJECTIVE=T_VALID
OBJECTIVE=T_STAR=min(T_VALID)

## 0. 方法权威

先读取：
仓库=cuiqinggang/codex-private-skills
分支=codex/first-principles-physical-limit-convergence-v3.1.4
文件=skills/first-principles-physical-limit-convergence/SKILL.md
VERSION=3.1.4

若版本或 CURRENT_STEP 冲突：
SKILL_GATE=BLOCKED
ACTION=STOP

禁止进入 STEP 3，禁止现实浏览器运行。

## 1. STEP 1 冻结输入

STEP1_CLOSEOUT=PASS
NEXT_ALLOWED_STEP=2_VIRTUAL_99
INCUMBENT_BASELINE_STATUS=PASS_WITH_KNOWN_LIMITS
NORMAL_FUNCTION_STATUS=PASS
STEP1_BLOCKERS=NONE

现实时间：
CURRENT_GOLDEN_T_VALID_MS=5125.62
CURRENT_COLD_BROWSER_READY_MS=2361.19
HISTORICAL_COLD_P50_MS=309.64
HISTORICAL_COLD_P95_MS=392.4
HISTORICAL_BUSINESS_T_VALID_MIN_MS=29668.53
HISTORICAL_BUSINESS_T_VALID_MEDIAN_MS=31281.055
HISTORICAL_BUSINESS_T_VALID_MAX_MS=43071.1

现实差异：
COLD_SAMPLE_ABOVE_HISTORICAL_P95
CDP_9222_ENDPOINT_404
SHARED_MCP_NOT_RERUN
REASONIX_LIVE_ABSORPTION_NOT_RETESTED

未知项：
REAL_PAGE_PROTOCOL_CALL_COUNT
SHARED_PROFILE_LOGIN_STATE
AI_RESOURCE_ORCHESTRATOR_PROFILE_STATE
REAL_SITE_CURRENT_DISTRIBUTION
PDF_CAPABILITY

Jev：
JEV_PUBLIC_REFERENCE=9.450s_TO_7.092s_DIFFERENT_BOUNDARY
LOCAL_VERIFY02=SAFE_BUT_NOT_TIME_99

STEP 1 证据文件：
PLAYWRIGHT-BROWSER-AUTOMATION5-STEP1-MATURE-REALITY-RESULT-v1.md
PLAYWRIGHT-BROWSER-AUTOMATION5-STEP1-MATURE-REALITY-RESULT-v1.json
PLAYWRIGHT-BROWSER-AUTOMATION5-STEP1-CAPABILITY-MATRIX-v1.json
PLAYWRIGHT-BROWSER-AUTOMATION5-STEP1-TVALID-BASELINE-v1.json
PLAYWRIGHT-BROWSER-AUTOMATION5-STEP1-MATURE-SOLUTION-REALITY-POOL-v1.md

优先回读上一 STEP 1 本地工作区并校验已有 SHA256；若暂时不可见，使用以上冻结摘要继续，禁止重跑 STEP 1。

## 2. 唯一目标与 VALID

唯一指标：
T_VALID=任务正式开始到第一个完整、正确、可用、满足 VALID 的现实结果出现的端到端时间。
T_STAR=min(T_VALID)

没有第二 KPI。

任何同 VALID、同计时边界的已知成熟路线 i 必须满足：
T_STAR <= T_i

若以后最终结果慢于某个已知 VALID 成熟路线：
PHYSICAL_LIMIT_CLAIM=FAIL
RETURN_TO_STEP2=YES

VALID 至少要求：
- 完整实现当前任务必要功能；
- 结果正确；
- 不删必要步骤伪造速度；
- 登录态、Profile、上传、下载、标签页、复杂页面、恢复、长页面、PDF/MD 等在需要它们的任务中可用；
- 允许不同任务族使用不同成熟 fast path；
- 最终可以是一个统一系统内部包含多条成熟专用路线。

ONE_FINAL_SYSTEM 不等于只能有 ONE_BROWSER_ENGINE。

## 3. 现役浏览器身份

C:\AI\Playwright-Native-AI-Browser 的身份仅为：

INCUMBENT_MATURE_BASELINE
STRONG_CANDIDATE
NOT_FORCED_BACKBONE
NOT_PROTECTED_WINNER

禁止因为历史投入预选它获胜，也禁止为了追新而预先淘汰它。

## 4. 成熟能力池

必须吸收 STEP 1 Mature Reality Pool 与仓库已有历史成果，至少包括：

- 当前 Playwright Native；
- Playwright 官方成熟机制；
- Jev / typesafe/jev-1.13；
- browser-use / jev-ultrafast；
- Stagehand observe/action 复用与缓存思想；
- workflow-use / deterministic workflow 思想；
- Browser Harness / BrowserCode / persistent-CDP 类低往返架构；
- BrowserGym；
- WebArena-Verified / Hard；
- JEV-VIRTUAL-99-v2、shadow、Verify-02、Reality Delta；
- STEP 1 捕获的其他有现实证据成熟路线。

只允许：
DISCOVER
COPY
ADAPT
COMPOSE
MATCH
VERIFY_MODEL
TIME_OPTIMIZE

禁止从零重造成熟世界已解决的浏览器能力。

## 5. 第一性原理时间模型

对每个主要任务族建立：

T_VALID =
T_ENTRY
+ T_BROWSER_OR_SESSION_READY
+ T_STATE_ACQUISITION
+ T_DECISION
+ T_ACTION
+ T_WAIT
+ T_VERIFY
+ T_RECOVERY_IF_REQUIRED

并拆成：

T_UNAVOIDABLE
T_REMOVABLE_OVERHEAD
T_CURRENT
T_PHY_LOWER_BOUND

所有数字标记来源等级：
MEASURED_LOCAL
MEASURED_PUBLIC
DERIVED_FROM_MEASURED
INFERRED_MODEL
UNKNOWN

不把现有实现开销当物理下限，不把公开宣传数字当物理下限。

## 6. 必须建立的任务族

FAMILY_A deterministic known path：
优先 CODE / direct Playwright / direct browser script。
目标 MODEL_CALLS=0，最小协议往返，事件驱动等待。

FAMILY_B finite closed semantic decision：
CODE pre-handler -> compact state -> maximum one canonical Jev typed request -> browser action -> CODE verifier。
禁止旧 always-on ensemble、多 view、多 Jev rescue。

FAMILY_C repeated solved workflow：
优先 deterministic compiled/cached workflow + 参数注入 + verifier。
无现实漂移时不重新大模型探索。

FAMILY_D open complex browser reasoning：
允许 Codex / DeepSeek / Reasonix / mature browser agent。
只在 VALID 真正需要开放推理时使用，并尽量只推理一次、后续确定化。

FAMILY_E recovery / changed reality：
只在失败真实发生时触发，不允许 always-on fallback。

## 7. 候选架构池

至少虚拟比较：

ROUTE_A=现役 Playwright Native 去除可删除开销
ROUTE_B=deterministic compiled/workflow fast path
ROUTE_C=Jev-style atomic state + one finite decision
ROUTE_D=persistent browser/CDP low-round-trip mature runtime
ROUTE_E=incumbent + Jev + deterministic cache hybrid
ROUTE_F=按任务族选择最低 T_VALID 路线的 minimal router
ROUTE_G=STEP1 mature pool 中任何能严格降低 T_VALID 的成熟组合

可以合并和删除，不要求全部进入 finalist。

## 8. 淘汰规则

满足任一即从 ACTIVE 删除：

- 不满足 VALID；
- 同任务下被另一成熟路线严格更快且无必要能力优势；
- 增加模型调用却没有减少更大的时间项；
- 增加协议往返却没有 VALID 收益；
- always-on verifier/fallback/ensemble 只增加时间；
- 成熟世界已有更简单更快替代；
- 需要从零重写成熟能力。

历史保留，ACTIVE 执行权删除。

## 9. Jev / Codex / DeepSeek / Reasonix 职责

JEV 不是第二目标，只是成熟能力。

固定职责：
CODE = state + frozen contract 可唯一确定
JEV = CODE 无法唯一确定、但答案空间闭合的有限语义判断，最多一次 canonical typed request
Codex/DeepSeek/Reasonix = 开放问题或一次最小 Jev 仍不能确定

任何 CODE 可唯一决定的工作：
DO_NOT_CALL_JEV

任何已成功编译/缓存的重复路径：
DO_NOT_CALL_JEV
DO_NOT_CALL_GPT

Codex/DeepSeek/Reasonix 不得预先排除；若某类开放任务只有它们才能以最低 VALID T_VALID 完成，可以进入最终系统。

## 10. STEP 1 未知项处理

对每个 UNKNOWN 分类：

CLASS_A=不影响 Virtual-99 冻结，可留 STEP 3 测量
CLASS_B=影响排序，但可用保守边界建模
CLASS_C=没有该事实无法冻结现实验证合同

只有出现 CLASS_C 才：
VIRTUAL_99=BLOCKED
MISSING_REALITY_FACT=<exact item>
ACTION=STOP

禁止在 STEP 2 自行跑现实浏览器补数据。

## 11. Virtual-99 故障推演

至少推演：
页面结构变化、locator 漂移、stale state、popup/new tab、iframe/frame、upload/download、long page、PDF/MD、login/session、network delay、模型/API delay、invalid output、workflow drift、recovery、browser restart、profile state、dynamic target、重复任务、首次未知任务。

原则：
FAILURE_HANDLING_WHEN_NEEDED != ALWAYS_ON_OVERHEAD

任何每次都执行且显著增加 T_VALID 的安全/验证结构，必须证明是 VALID 必需，否则删除。

## 12. 最终系统形式

若单一 runtime 不可能在所有任务族最快，允许冻结：

ONE_FINAL_SYSTEM =
MINIMAL_ROUTER
+ MULTIPLE_MATURE_SPECIALIZED_FAST_PATHS

路由优先由 CODE 决定；
CODE 不能决定且属于闭合语义时才允许一次 Jev；
禁止每次先调用大模型决定“该用哪个浏览器”。

## 13. 冻结 STEP 3 验证合同

STEP 2 最终必须生成完整且不可在 STEP 3 现场修改的 Real Verify 合同。

若虚拟证据已明确支配：
FINALIST_COUNT=1

若仍存在只能靠现实数据判断的竞争者：
FINALIST_COUNT=2..3

但必须在 STEP 2 预先冻结：
- 每条 route 完整实现；
- 相同任务；
- 相同 VALID；
- 相同输入；
- 相同计时边界；
- 相同 verifier；
- cold/warm/reconnect 分类；
- 重复次数；
- PASS/FAIL；
- winner rule；
- 禁止 STEP 3 现场改方案。

winner rule 只有：
VALID first
then minimum T_VALID

其他指标仅诊断。

## 14. Jev 一致性检查

只有 SAME_TASK + SAME_VALID + SAME_TIMING_BOUNDARY 时才直接比较 Jev 公布数字。

若三者相同：
FINAL_SAME_BOUNDARY_T <= KNOWN_MATURE_JEV_T
否则不能宣称全局极限。

若不可比：
JEV_DIRECT_COMPARISON=NOT_VALID

禁止改变主 T_VALID 计时边界去追公开 benchmark。

## 15. 输出文件

创建：

docs/playwright-browser-automation/20260920-step2-virtual99/
PLAYWRIGHT-BROWSER-AUTOMATION5-STEP2-VIRTUAL99-RESULT-v1.md
PLAYWRIGHT-BROWSER-AUTOMATION5-STEP2-VIRTUAL99-RESULT-v1.json
PLAYWRIGHT-BROWSER-AUTOMATION5-STEP2-T-PHY-v1.md
PLAYWRIGHT-BROWSER-AUTOMATION5-STEP2-T-PHY-v1.json
PLAYWRIGHT-BROWSER-AUTOMATION5-STEP2-ROUTE-MATRIX-v1.json
PLAYWRIGHT-BROWSER-AUTOMATION5-STEP2-FAST-PATH-TABLE-v1.json
PLAYWRIGHT-BROWSER-AUTOMATION5-STEP2-FAILURE-SIMULATION-v1.md
PLAYWRIGHT-BROWSER-AUTOMATION5-STEP3-REAL-VERIFY-CONTRACT-v1.md
PLAYWRIGHT-BROWSER-AUTOMATION5-STEP3-REAL-VERIFY-CONTRACT-v1.json
PLAYWRIGHT-BROWSER-AUTOMATION5-STEP3-REAL-VERIFY-COMMAND-v1.md

全部：
写后回读
JSON 解析
SHA256
git diff --check

禁止修改生产浏览器和 v3.1.4 母技能。
禁止执行 STEP 3。

## 16. PASS 条件

只有同时满足：

METHOD_AUTHORITY=3.1.4
CURRENT_STEP=2
STEP1_CLOSEOUT_INPUT=PASS
ONLY_OBJECTIVE=T_VALID
VALID_CONTRACT=FROZEN
MATURE_CAPABILITY_POOL_ABSORBED=YES
T_PHY_MODEL=COMPLETE_OR_EXPLICITLY_BOUNDED
TASK_FAMILIES=FROZEN
ACTIVE_ROUTE_SET=MINIMIZED
DETERMINISTIC_FAST_PATH_MAXIMIZED=YES
UNNECESSARY_MODEL_CALLS_REMOVED=YES
UNNECESSARY_BROWSER_ROUND_TRIPS_REMOVED=YES
JEV_ROLE=FINITE_CLOSED_SEMANTICS_ONLY
OPEN_AGENT_ROLE=OPEN_PROBLEM_ONLY
FAILURE_SIMULATION=PASS
NO_ARCHITECTURE_PRESELECTION=YES
STEP3_CONTRACT=FROZEN
STEP3_COMMAND_CREATED=YES
REAL_BROWSER_RUNS_IN_STEP2=0
PRODUCTION_ARCHITECTURE_MUTATION=0
VIRTUAL_99=PASS
NEXT_ALLOWED_STEP=3_REAL_VERIFY
ACTION=STOP

才允许：
VIRTUAL_MATURITY=PASS
VIRTUAL_99=PASS

否则：
VIRTUAL_99=BLOCKED
BLOCKER=<exact blocker>
ACTION=STOP

## 17. 最终回传

只回传：

METHOD_AUTHORITY=
CURRENT_STEP=
STEP1_CLOSEOUT_INPUT=
ONLY_OBJECTIVE=
VALID_CONTRACT=
TASK_FAMILIES=
T_PHY_SUMMARY=
ACTIVE_ROUTE_SET=
ELIMINATED_ROUTES=
FINALIST_COUNT=
FINALISTS=
EXPECTED_FASTEST_PATH_BY_FAMILY=
JEV_ROLE=
OPEN_AGENT_ROLE=
FAILURE_SIMULATION=
STEP3_CONTRACT=
STEP3_COMMAND=
REAL_BROWSER_RUNS_IN_STEP2=
PRODUCTION_ARCHITECTURE_MUTATION=
VIRTUAL_MATURITY=
VIRTUAL_99=
NEXT_ALLOWED_STEP=
ACTION=
EVIDENCE_FILES=
SHA256=

若 VIRTUAL_99=PASS，同一最终回复必须附最短 STEP 3 handoff，但不得自行执行。

最后一行必须原样返回：

【playwright浏览器自动化5｜STEP2虚拟99全局收敛｜1】
