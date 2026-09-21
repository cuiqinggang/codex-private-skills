# Task-local Browser Twin → 唯一正式 Twin 提升合同 v1

## 定位

- 母方法：first-principles-physical-limit-convergence@3.1.9
- 核心归属：高智能虚拟成熟
- 阶段：冻结成果发布 / 现实机械验收
- 设计权：GPT 页面
- 执行权：Codex 仅 EXECUTE → VERIFY → REPORT → STOP

本合同不是新方案，不重新采集 Browser R3，不重新运行 T1/T2/T3，不重新设计 Twin。
它只把已经现实通过的 task-local Browser Twin 成果提升为共同私库中的唯一正式 Twin。

## 1. 已冻结的现实依据

本机权威工作区：

C:\Users\A\playwright-browser-automation5-final-reality-competition-work

Browser R3 权威输入：

C:\Users\A\playwright-browser-automation5-final-reality-competition-work\R3-BROWSER-REALITY\final

Task-local Twin：

C:\Users\A\playwright-browser-automation5-final-reality-competition-work\TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW

必须机械核验：

- R3_CANONICAL_GOLDEN_SHA256 = 1c67a634e0c0fc24ed057752358f4c20a6c05550be6146fd8d11b1a723f25e08
- BROWSER_R3_FINGERPRINT_SHA256 = 9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd
- BROWSER_CRITICAL_UNKNOWN_COUNT = 0
- BROWSER_TWIN_INPUT_READY = YES
- BROWSER_R3_REAL_CAPTURE = PASS
- REALITY_DELTA = NONE

Task-local Twin 必须机械核验：

- REALITY_PROFILE_ID = PLAYWRIGHT_GOLDEN_REALITY_PROFILE
- REALITY_PROFILE_VALIDATION = PASS
- LEGACY_SELFTEST = PASS (24/24)
- BROWSER_GOLDEN_REPLAY = PASS
- SAME_TASK = PASS
- SAME_VALID = PASS
- SAME_BUSINESS_RESULT = PASS
- SAME_CRITICAL_BROWSER_BEHAVIOR = PASS
- TWIN_CRITICAL_UNKNOWN_COUNT = 0
- MATERIAL_REALITY_TWIN_DELTA_COUNT = 0
- SHADOW_ISOLATION = PASS
- REALITY_MUTATED = NO
- PLAYWRIGHT_REALITY_SHADOW_BASELINE = PASS
- 自动化测试 = 6/6 PASS
- HISTORICAL_T_STAR_REAL_MS = 1525.09

任一不满足：STOP，不提升。

## 2. 唯一允许的提升

目标分支：

codex/first-principles-physical-limit-convergence-v3.1.9

目标唯一组件：

skills/first-principles-physical-limit-convergence/components/exact-reality-digital-twin

目标版本：

- 母技能：3.1.9
- Reality Anchor：1.3.0
- Exact Twin：1.3.0

只允许：

1. 保留 Git 历史中的 v1.2.0，不删除历史。
2. 把 task-local exact-reality-digital-twin 的 Browser Reality 能力提升进入唯一组件；禁止创建第二个正式 Twin。
3. 保留并复验 legacy Host/Codex 24/24。
4. 把 Browser R3 的三个 final 安全文件复制到：
   skills/reality-execution-environment-anchor/snapshots/2026-09-21-r3-browser-final/
   - BROWSER-R3-FINAL-ANCHOR.json
   - BROWSER-R3-FINGERPRINT.json
   - BROWSER-R3-MANIFEST.json
5. 只允许提交 safe final；禁止 raw trace/HAR/storage/cookie/token/authorization。
6. 把 task-local 正式安全输出复制到唯一 Twin 的 reality-profiles/playwright-golden/：
   - PLAYWRIGHT_GOLDEN_REALITY_PROFILE.json
   - BROWSER-PROFILE-VALIDATION.json
   - BROWSER-REALITY-REPLAY.json
   - BROWSER-REALITY-TWIN-DELTA.json
   - BROWSER-SHADOW-ISOLATION.json
   - BROWSER-REALITY-REPLAY-AFTER-SHADOW.json
7. 把 task-local tests/test_browser_twin.py 作为正式回归测试纳入唯一 Twin。
8. 更新 VERSION / manifest / README / CANONICAL / ACCEPTANCE，使状态与现实结果一致。

## 3. 删除 v3.1.8 的错误主线假设

v3.1.8 的以下路径降级为历史实验，不再作为 Browser Twin READY 的前置条件：

- browser-reality-r3-timing.mjs 经 Codex Code Mode VM 动态 import
- T1/T2/T3 + O1 作为 Browser R3 → Twin 输入的强制前置

原因：
Browser R3 已由 Canonical Golden 的原生 Node/Playwright R3 Observer Seam 完成现实 3/3，并已经产生可用 R3 Fingerprint。
其 observability 时间不冒充 T_VALID。

唯一现实时间基线继续保留：

HISTORICAL_T_STAR_REAL_MS=1525.09

以后若优化 T_VALID，属于核心①「极限短时间」的新独立任务，不得阻断已经通过的 Reality/Twin 等价性。

## 4. 提升后验收

必须全部 PASS：

- MOTHER_VERSION=3.1.9
- REALITY_ANCHOR_VERSION=1.3.0
- EXACT_TWIN_VERSION=1.3.0
- R3_SAFE_FINAL_PROMOTED=PASS
- BROWSER_R3_FINGERPRINT_SHA256=9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd
- REALITY_PROFILE_VALIDATION=PASS
- LEGACY_SELFTEST=24/24 PASS
- BROWSER_TWIN_TESTS=6/6 PASS
- BROWSER_GOLDEN_REPLAY=PASS
- MATERIAL_REALITY_TWIN_DELTA_COUNT=0
- SHADOW_ISOLATION=PASS
- REALITY_MUTATED=NO
- SECRET_PLAINTEXT_ZERO_REMOTE=PASS
- FULL_BROWSER_TWIN=YES
- PLAYWRIGHT_REALITY_SHADOW_BASELINE=PASS

Environment-99 只在上述全部通过后写：
ENVIRONMENT_99=PASS

任何失败：
REALITY_DELTA=<实际事实>
ACTION=STOP
RETURN_TO_GPT=YES

Codex 禁止自行修复、重设计、补跑新 R3、重做 timing 或另建 Twin。

## 5. 最终回传

仅回传：

MOTHER_VERSION=
REALITY_ANCHOR_VERSION=
EXACT_TWIN_VERSION=
R3_SAFE_FINAL_PROMOTED=
BROWSER_R3_FINGERPRINT_SHA256=
REALITY_PROFILE_VALIDATION=
LEGACY_SELFTEST=
BROWSER_TWIN_TESTS=
BROWSER_GOLDEN_REPLAY=
MATERIAL_REALITY_TWIN_DELTA_COUNT=
SHADOW_ISOLATION=
REALITY_MUTATED=
SECRET_PLAINTEXT_ZERO_REMOTE=
FULL_BROWSER_TWIN=
PLAYWRIGHT_REALITY_SHADOW_BASELINE=
HISTORICAL_T_STAR_REAL_MS=
ENVIRONMENT_99=
REALITY_DELTA=
ACTION=
BRANCH=
HEAD=
