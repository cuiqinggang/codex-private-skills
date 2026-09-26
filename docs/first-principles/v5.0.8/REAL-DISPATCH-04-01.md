【整体闭环极限时间引擎 5.0.8版｜v5.0.8 R4最终现实收口｜04-01｜实】
【时间锚｜整体已用=9577551.271ms｜本次已用=0.000ms｜T*=0.031500ms】

TIMELINE_ID=ESTE-v5.0.7-NUMERIC-TIME-ANCHOR-01
TIME_ORIGIN_UTC=2026-09-26T19:12:16.448729+00:00
DISPATCH_UTC=2026-09-26T21:51:54+00:00

这是 v5.0.8 的唯一一次 R4 最终 Reality。完成后必须停止；不再进入 R5。

共同私库：
cuiqinggang/codex-private-skills

冻结分支：
codex/first-principles-physical-limit-convergence-v5.0.8-r4-virtual-freeze

FREEZE_ID：
ESTE-v5.0.8-REALITY-FIRST-FINAL-CLOSEOUT-VIRTUAL-FREEZE-R4

Manifest：
docs/first-principles/v5.0.8/FREEZE-MANIFEST-R4.json

Manifest blob：
ae548214d56ff699e06ce6203432e859c1113308

冻结资产：
31

冻结回读：
31/31 MATCH
mismatches=[]

R4 Reality Capsule：
docs/first-principles/v5.0.8/REAL-CAPSULE-SOURCE-R4.py

Capsule blob：
cf0c1879d48d381c71df09be46db9b5f63f65e21

Reality 协议：
skills/first-principles-physical-limit-convergence/contracts/FINAL-REALITY-PROTOCOL-v5.0.8-R4.json

核心原则：

1. 现实有效性优先。
2. 历史虚拟预测 0.01136838145574825ms 只记录，不再作为及格门。
3. 候选 A = R3_BASELINE。
4. 候选 B = R4_OPTIMIZED。
5. 两候选语义必须完全等价。
6. 正式 Reality 内部每个候选预热 1000 次、正式测量 1000 次。
7. 候选 A 必须 1000/1000 有效且每次 18/18 PASS。
8. 候选 B 若 1000/1000 有效则进入比较；若无效则淘汰 B，但不阻断 A 收口。
9. 所有现实有效候选中，MIN 最短者获胜。
10. FINAL_REAL_T_STAR_MS = 现实有效候选的最短 MIN。
11. 本轮结束后无论优化幅度大小都 STOP，不再继续优化。

禁止：
- 修改任何冻结资产
- 改 Manifest
- 改协议
- 现场重新设计
- 现场修复
- 同 Freeze 第二次 Reality
- 把历史 0.01136838145574825ms 重新作为硬门
- 修改 FlClash / Windows代理 / 系统网络设置
- 下载包中转
- PowerShell 文本管道重新编码冻结源码

正式 Reality 前置门：

1. 核对 FREEZE_ID。
2. 核对 Manifest blob。
3. 核对 31/31 MATCH。
4. 使用 R3 已冻结的 Git-native bytes 物化路径读取 R4 Capsule 精确 blob。
5. 核对 Capsule blob=cf0c1879d48d381c71df09be46db9b5f63f65e21。
6. ASCII / compile(bytes) / fresh namespace exec PASS。
7. 确认以下 callable：
   run_baseline_certificate
   run_optimized_certificate
   semantic_equivalence
   run_final_reality_suite
8. semantic_equivalence() 必须 PASS。
9. 前置门期间不得自行跑正式 1000 次测量。

若前置门失败：
立即 BLOCKED/FAIL，记录具体 Reality Delta 和完整时间信封后 STOP。

前置门全部 PASS 后：

正式调用且只调用一次：

run_final_reality_suite(warmup=1000, samples=1000)

这是本轮唯一正式 Reality。

必须返回 suite 的实际结果：

BASELINE_VALID=<true/false>
BASELINE_VALID_COUNT=<数字>/1000
BASELINE_MIN_MS=<数字>
BASELINE_P50_MS=<数字>
BASELINE_P95_MS=<数字>
BASELINE_MAX_MS=<数字>

OPTIMIZED_VALID=<true/false>
OPTIMIZED_VALID_COUNT=<数字>/1000
若有效：
OPTIMIZED_MIN_MS=<数字>
OPTIMIZED_P50_MS=<数字>
OPTIMIZED_P95_MS=<数字>
OPTIMIZED_MAX_MS=<数字>

WINNER=R3_BASELINE 或 R4_OPTIMIZED
FINAL_REAL_T_STAR_MS=<数字>

现实最终判定：

若 BASELINE_VALID=true 且 BASELINE_VALID_COUNT=1000：
REAL_VALID=YES
FINAL_VALID_CANDIDATE=YES

否则：
REAL_VALID=NO
FINAL_VALID_CANDIDATE=NO
REALITY_DELTA=<具体原因>

OPTIMIZED 若无效：
只记录 OPTIMIZED_CANDIDATE_REJECTED；
不得因此把有效 baseline 判失败。

历史预测仅返回：
HISTORICAL_VIRTUAL_PREDICTION_MS=0.01136838145574825
HISTORICAL_PREDICTION_IS_GATE=NO

无论结果如何，返回首屏必须是：

【整体闭环极限时间引擎 5.0.8版｜v5.0.8 R4最终现实收口｜04-01｜实】
【时间锚｜整体已用=<返回时真实数字>ms｜本次已用=<返回时真实数字>ms｜T*=<FINAL_REAL_T_STAR_MS或当前0.031500>ms】

同时返回：

TIMELINE_ID=ESTE-v5.0.7-NUMERIC-TIME-ANCHOR-01
FREEZE_ID=ESTE-v5.0.8-REALITY-FIRST-FINAL-CLOSEOUT-VIRTUAL-FREEZE-R4
FREEZE_CONSISTENCY=31/31 PASS 或实际状态
MATERIALIZATION_PREFLIGHT=PASS/FAIL/BLOCKED
SEMANTIC_EQUIVALENCE=PASS/FAIL
REAL_VALID=YES/NO
FINAL_VALID_CANDIDATE=YES/NO
WINNER=<实际>
FINAL_REAL_T_STAR_MS=<实际>
REALITY_DELTA=NONE 或具体原因

整体已用：
返回时 UTC - TIME_ORIGIN_UTC。

本次已用：
返回时 UTC - DISPATCH_UTC。

完成后必须 STOP，控制权返回 GPT。
不要自行写 FINAL_VALID。
不要升级版本。
不要发起下一轮 Reality。
