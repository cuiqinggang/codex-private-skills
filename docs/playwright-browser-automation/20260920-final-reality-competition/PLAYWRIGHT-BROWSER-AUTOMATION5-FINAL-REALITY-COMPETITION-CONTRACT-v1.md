【playwright浏览器自动化5｜冻结最终现实极限竞争测试｜1｜高智能虚拟成熟】

# Playwright 浏览器自动化5 — 最终现实极限竞争测试合同 v1

## 0. 方法归属

本合同由 GPT 页面完成并冻结。

核心归属：

高智能虚拟成熟

方法权威：

first-principles-physical-limit-convergence v3.1.5

唯一优化指标：

T_VALID

唯一目标：

T_STAR = min(T_VALID)

Codex / Reasonix / 本地执行器在本合同中的角色只有：

RUN
MEASURE
RECORD
RETURN
STOP

它们没有以下权限：

- 决定最终产品；
- 修改候选路线；
- 修改测试任务；
- 修改计时边界；
- 修改 VALID；
- 修改重复次数；
- 修改 winner rule；
- 自行修复；
- 自行增加 fallback；
- 自行增加路线；
- 根据中途成绩提前终止慢路线；
- 根据结果重写实现；
- 现场重新虚拟成熟。

任何需要改变冻结内容的问题：

记录现实差异
-> STOP
-> 返回 GPT 页面

---

## 1. 冻结实现来源

本地冻结工作区：

C:\Users\A\playwright-browser-automation5-step2-work

冻结本地提交：

6a8c3b0dfb98bfd3312df319dbd31b0ffd7ed629

可执行冻结已通过：

- 22/22 tests PASS
- 26/26 simulations PASS
- 58/58 manifest hashes PASS
- F1 executable package PASS
- F2 executable package PASS
- F3 executable package PASS
- Jev typed path PASS
- Open-agent path PASS
- Recovery package PASS
- STEP3 harness executable PASS
- Final router code frozen PASS
- All route interfaces unified PASS

正式冻结 SHA256：

RESULT.md=c2135912acee0a9821431a406a775534accddabcdfb516b33b1cc8ebeb130ad1
RESULT.json=97b3e7db2397bf9711015a2a61adf55be953d2c19b760bd8e1ba783104a8f080
TEST-MATRIX=6bad5bcb8f1dea52bef930f878af4660f607eb349a7e1d207f9cd90b197b42e1
MANIFEST=a4b27d4f1953200d050a729285701c3b73aac200538de2b779bc6f1b4b8ecca1
STEP3-COMMAND-V2=a15960a5d8af06a5d272bd6342e44dd21c6fd051fea384e7ccce8b0b2cf0d6c5

执行前必须核对本地 HEAD 与上述冻结证据。

任何冻结实现、manifest、harness 或 command hash 不一致：

SOURCE_FREEZE_GATE=BLOCKED
ACTION=STOP

不得自行重建或修复。

---

## 2. 最终候选

三个 browser execution finalists 固定为：

F1 = PLAYWRIGHT_NATIVE_DIRECT_PERSISTENT
F2 = PLAYWRIGHT_COMPILED_REPLAY
F3 = PERSISTENT_CDP_BATCHED_HELPER

辅助能力固定为：

JEV = FINITE_CLOSED_SEMANTICS_ONLY_MAX_ONE_REQUEST
OPEN_AGENT = OPEN_PROBLEM_OR_INVALID_UNCERTAIN_ONE_JEV_ONLY
RECOVERY = ON_DEMAND_ONLY

禁止 F4/F5。
禁止修改 F1/F2/F3 定义。

---

## 3. 最终产品的比较单位

浏览器没有一个适用于所有任务的单一“极限秒数”。

因此最终产品按任务族形成 winner map。

固定任务族：

A = 确定性已知路径
B = 有限闭合语义判断
C = 重复已解决工作流
D = 开放复杂浏览器推理
E = 现实变化/恢复
CAP = 完整能力合同

最终产品允许：

一个 CODE 最小路由器
+
不同任务族各自现实最快的 VALID 路线

不要求一个 browser engine 赢所有任务族。

---

## 4. 主计时口径：T_VALID_FULL

唯一主指标为 T_VALID_FULL。

### COLD

起点：

harness 接受该次正式任务，且候选浏览器进程尚未运行。

终点：

冻结 independent verifier 首次确认完整 VALID 结果。

必须计入：

- browser/session startup；
- 必要 initial navigation；
- 页面状态读取；
- 模型调用；
- 浏览器动作；
- 页面等待；
- 必要恢复；
- 达到可验证结果前的所有必要工作。

不得预热后伪装 COLD。

### WARM

前提：

同一候选进程/context 已经处于冻结的 ready initial state。

起点：

harness 接受该次任务。

终点：

independent verifier 首次确认完整 VALID。

任务特定动作全部计入。
准备下一轮 initial state 的工作不允许偷偷算进前一轮，也不允许在当前轮起点后排除。

### RECONNECT

前提：

浏览器继续存在，控制连接按冻结合同断开。

起点：

harness 发出本轮 reconnect task。

终点：

重连后的冻结任务取得 independent VALID 结果。

---

## 5. VALID 规则

每次 attempt 必须满足：

- 目标任务完整完成；
- 独立 verifier PASS；
- 非法输出=0；
- 重复发送/重复副作用=0；
- 无未授权 human intervention；
- 模型调用数不超过冻结上限；
- 不修改生产架构；
- 不修改代理/FlClash/系统网络；
- 不破坏用户 Profile；
- 原始 timing / trace / error / recovery 证据完整。

FAIL、UNAVAILABLE、endpoint failure、dependency missing 都必须保留。

不得删除失败 attempt。

路线在某任务族只有规定的所有 attempts 都满足该族 VALID，才进入该族速度比较。

---

## 6. 冻结运行矩阵

### A1 — 确定性 Golden 任务

使用 frozen executable-freeze package 中已经程序化的同一 deterministic fixture / golden task。

F1：
- COLD x10
- WARM x20
- RECONNECT x10

F2：
- COLD x10
- WARM x20
- RECONNECT：仅当 frozen F2 contract 已定义 reconnect；否则 N/A，不得现场新增

F3：
- COLD x10
- WARM x20
- RECONNECT x10

要求：
同输入、同 VALID、同 verifier、同 timing boundary。

### B1 — 有限闭合语义

B-CODE 子集：
- x20
- CODE 可唯一决定时 model calls 必须为 0

B-JEV 子集：
- x10
- 每例最多 1 次 canonical typed Jev request
- Jev retry=0
- ensemble=0
- probability fusion=0
- hidden second request=0

执行 browser route 使用 frozen B-family package，不得临场选择新路线。

### C1 — 重复已解决工作流

使用同一组 frozen solved-workflow fixtures。

F1：
- WARM x20
- COLD x10

F2：
- WARM x20
- COLD x10

F3：
- WARM x20
- COLD x10

F2 compiler 不计入每次 repeated runtime；但 compiler 本身必须是 STEP2 已冻结产物，不能在现实测试中重新探索页面。

若 precondition 不满足：
ROUTE_NOT_APPLICABLE
按冻结合同记录，不允许 F2 自己 fallback。

### D1 — 开放复杂推理

只运行 frozen eligible open-agent route：

- 每个冻结 D-family case x5
- 每次最多 1 次开放规划调用
- 规划后 deterministic execution
- 每步重新规划=禁止
- agent 选择浏览器 route=禁止

此族若现实证据不足：
D_GLOBAL_LIMIT_CLAIM=NOT_ALLOWED

### E1 — 恢复

对每个冻结故障：

- SESSION_LOST x3
- STALE_STATE x3
- TARGET_CHANGED x3
- BROWSER_CRASH x3
- NETWORK_INTERRUPTION x3
- CONTRACT_DRIFT x3

正常路径必须：

RECOVERY_OVERHEAD=0

只有故障信号出现后才能触发 recovery。

### CAP — 正常功能能力

对 frozen capability matrix 中每一个正式能力用例：

每个 x3。

至少按冻结能力包验证当前实际包含的：

- navigation
- state read
- locate
- click
- input
- wait/synchronization
- tab/new tab
- upload
- download
- profile/session
- long page/content
- structured text/table/json/code
- interruption/recovery
- PDF/MD capability（仅 frozen package 已有实现时）

若某项在 frozen matrix 中仍是 UNKNOWN：
CAPABILITY_STATUS=UNKNOWN
FINAL_PRODUCT_COMPLETE=NO
不得由 Codex现场补实现。

---

## 7. Jev 官方同口径一致性挑战

这不是第二 KPI，只是已知成熟现实路线的一致性检查。

官方参考来源：

browser-use/jev-ultrafast

冻结公开源码参考：

main SHA=1231850a0bf1a0c0341fe408ef1668dbbfdfac46

官方任务：

URL:
https://www.google.com/travel/flights?hl=en

Goal:
Find one-way flights from Zurich to London on September 20, 2026, for one adult in economy. Stop when matching flight options are visible.

官方验证内容：
- one-way
- Zurich
- London
- September 20, 2026
- one adult
- economy
- matching flight options visible

官方报告：
VIDEO_RUN_MS=7073
OPTIMIZED_MEDIAN_MS=7092
ORIGINAL_MEDIAN_MS=9450

官方 compatible timing boundary：
- browser setup excluded
- initial navigation excluded
- clock starts at first prediction after initial homepage observation
- includes model calls, generated text, browser work, stale decisions, waits/loading
- clock ends at accepted DONE
- fresh independent post-run verification outside compatible clock

### J0 参考臂

若可在隔离环境中按冻结公开源码和依赖安全运行：
运行官方 optimized reference x3，用于本机环境校准。

不得修改 upstream source。
不得把 J0 作为最终产品候选。
J0 只作 reference arm。

若依赖/凭据/页面现实导致不能运行：
J0_LOCAL_REFERENCE=UNAVAILABLE
记录原因并继续其他冻结测试。
不得为 J0 修改系统或代理。

### J1 FIRST-SEEN 挑战

用于测试未预先编译该具体任务的 fastest eligible final system path。

F2 在 FIRST-SEEN 中不得使用该任务的预编译 replay。

每个 eligible frozen route：
WARM compatible boundary x10。

JEV_REFERENCE_BEAT_MEDIAN=PASS 当且仅当：
- 所有规定 attempts VALID；
- median compatible elapsed < 7092 ms。

JEV_VIDEO_BEAT=PASS 当且仅当：
- 至少一个 VALID attempt < 7073 ms。

### J2 REPEATED 挑战

在一次合法成功解决并由 STEP2 frozen compiler 具备该类重复能力后，允许 F2 参加 repeated task。

WARM x20。

该结果用于 repeated-production family，不得伪称为 first-seen apples-to-apples。

### 重要规则

主产品 winner 仍只使用 T_VALID_FULL。

JEV_COMPAT 时间单独记录。

不得用排除 initial navigation 的 JEV_COMPAT 时间替代主 T_VALID_FULL。

---

## 8. 统计与唯一 Winner Rule

每个 route / task / condition 必须保留所有 attempt。

必须报告：

- count
- valid_count
- fail_count
- minimum
- median
- maximum
- P95（样本足够时，仅诊断）

Winner rule：

1. VALID first。
2. 只有该任务族所有规定 attempts 满足 VALID 的路线进入 winner comparison。
3. 然后只比较同任务、同输入、同条件、同边界下的 minimum T_VALID_FULL。
4. minimum 更低者赢。
5. 精确并列保留并列。
6. 不使用 median、P95、成本、token、模型次数作为第二 tie-breaker。
7. median/P95 只作为稳定性诊断。
8. 若存在同边界已知成熟路线更快，则 PHYSICAL_LIMIT_CLAIM=FAIL。

Codex 可以运行已冻结 winner-selector 生成：

PROVISIONAL_WINNER_MAP

但不得把它改成最终产品状态。

最终产品 winner map 由 GPT 页面读取现实数据后决定并冻结。

---

## 9. 防止“测试即开发”

Reality test 中禁止：

- edit F1/F2/F3；
- edit Jev prompt/schema；
- edit open-agent prompt；
- edit recovery contract；
- edit router；
- edit winner-selector；
- edit verifier；
- change thresholds；
- change run counts；
- create new route；
- skip slow run；
- delete failed attempt；
- change initial state；
- change timing start/stop；
- change task after seeing result；
- install a replacement architecture。

若测试所需 frozen package 缺失或无法执行：

REALITY_DELTA=<exact issue>
ACTION=STOP

不得修。

---

## 10. 结果产物

必须新建独立结果目录，例如：

docs/playwright-browser-automation/20260920-final-reality-competition/results/

至少生成：

FINAL-REALITY-RAW-RUNS-v1.jsonl
FINAL-REALITY-SUMMARY-v1.json
FINAL-REALITY-SUMMARY-v1.md
FINAL-REALITY-CAPABILITY-v1.json
FINAL-REALITY-JEV-COMPAT-v1.json
PROVISIONAL-WINNER-MAP-v1.json
REALITY-DELTA-v1.json
ARTIFACT-HASHES-v1.json

每个 raw attempt 必须包含：

route_id
family
case_id
condition
attempt_index
valid
status
t_valid_full_ms
jev_compatible_ms_if_applicable
component_times
model_calls
jev_calls
open_agent_calls
browser_protocol_calls_if_observable
recovery_triggered
error
artifact_paths
contract_version
source_commit

所有结果：
写后回读
JSON/JSONL parse
SHA256
git diff --check

不 push，除非用户明确授权。

---

## 11. Codex 最终回传

Codex 只回传现实事实，不给产品设计建议。

固定字段：

METHOD_AUTHORITY=3.1.5
CORE=高智能虚拟成熟
FROZEN_SOURCE_COMMIT=
SOURCE_FREEZE_GATE=
A_VALID=
A_WINNER_PROVISIONAL=
A_MIN_T_VALID_FULL_MS=
B_VALID=
B_CODE_MODEL_CALLS=
B_JEV_MAX_REQUESTS=
C_VALID=
C_WINNER_PROVISIONAL=
C_MIN_T_VALID_FULL_MS=
D_VALID=
E_VALID=
CAPABILITY_STATUS=
J0_LOCAL_REFERENCE=
J1_FIRST_SEEN_VALID=
J1_BEST_ROUTE=
J1_MIN_COMPAT_MS=
J1_MEDIAN_COMPAT_MS=
JEV_REFERENCE_BEAT_MEDIAN=
JEV_VIDEO_BEAT=
J2_REPEATED_VALID=
J2_BEST_ROUTE=
J2_MIN_COMPAT_MS=
ALL_FAILURES_RETAINED=
TEST_CONTRACT_MUTATION=
PRODUCTION_MUTATION=
PROVISIONAL_WINNER_MAP=
REALITY_DELTA=
ACTION=STOP
EVIDENCE_FILES=
SHA256=

如果任何需要改变冻结设计的问题出现：
ACTION=STOP
不得继续。

---

## 12. 本轮结束后的权力边界

本次 Codex 回传以后：

Codex STOP。

下一步只能回 GPT 页面。

GPT 页面负责：

现实数据
+ VALID
+ T_VALID
+ Jev consistency evidence
+ capability status
+ T_PHY bounds
-> 最后一次高智能虚拟成熟
-> 冻结 FINAL_PRODUCT_WINNER_MAP
-> 冻结正式 MVT Browser Automation 产品状态
-> 再生成最终最小现实确认命令

Codex 不得在本轮直接宣布最终产品完成。

【playwright浏览器自动化5｜冻结最终现实极限竞争测试｜1｜高智能虚拟成熟】
