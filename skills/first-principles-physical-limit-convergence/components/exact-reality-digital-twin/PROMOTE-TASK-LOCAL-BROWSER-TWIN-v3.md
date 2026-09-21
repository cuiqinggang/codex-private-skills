# Task-local Browser Twin → 唯一正式 Twin 提升合同 v3

## 定位
- 核心：高智能虚拟成熟
- 阶段：STEP 3 冻结成果正式提升与最终验收
- v1：apply_patch 被 Windows 1344 阻断，历史保留。
- v2：确定性 PowerShell/.NET 写入成功，但正式测试仍保留 task-local 路径和旧组件自报版本，验收 0/6。
- v3：只修“正式发布适配层”，禁止改变 Browser R3 / Twin 业务逻辑、现实证据、Fingerprint、Golden、Shadow、Delta 或时间基线。

## 已知事实
SOURCE_GATES=PASS
BROWSER_R3_FINGERPRINT_SHA256=9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd
MATERIAL_REALITY_TWIN_DELTA_COUNT=0
SHADOW_ISOLATION=PASS
REALITY_MUTATED=NO
TASK_LOCAL_BROWSER_TWIN_TESTS=6/6 PASS
LEGACY_SELFTEST=24/24 PASS
HISTORICAL_T_STAR_REAL_MS=1525.09

当前 partial worktree：
C:\Users\A\Documents\Codex\worktrees\first-principles-v3.1.9-promotion

## 0. Partial changes 门禁
先只读：
git status --short
git diff --binary

只允许 v2 合同目标文件的 partial changes。
若出现额外文件：
REALITY_DELTA=UNEXPECTED_PARTIAL_WORKTREE_CHANGE
STOP。

禁止 reset / checkout / clean 覆盖未知变化。

## 1. 正式测试脚本路径适配

目标正式测试：
skills\first-principles-physical-limit-convergence\components\exact-reality-digital-twin\tests\test_browser_twin.py

不得重新复制 task-local test 覆盖该文件。

只允许使用 PowerShell/.NET 精确替换以下发布锚点：

旧：
WORKSPACE = Path(__file__).resolve().parents[2]
ENGINE = WORKSPACE / "TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW" / "exact-reality-digital-twin" / "ENGINE.py"

新：
REALITY_WORKSPACE = Path(r"C:\Users\A\playwright-browser-automation5-final-reality-competition-work")
COMPONENT_ROOT = Path(__file__).resolve().parents[1]
ENGINE = COMPONENT_ROOT / "ENGINE.py"

并把 run_mode 中：
str(WORKSPACE)

精确改为：
str(REALITY_WORKSPACE)

含义必须保持严格分离：
- COMPONENT_ROOT：正式代码位置
- REALITY_WORKSPACE：已经现实认证过的 R3 / Reality Pack 输入位置

禁止改变 EXPECTED_ACTIONS 或任何业务断言。

## 2. 正式组件版本适配

目标：
skills\first-principles-physical-limit-convergence\components\exact-reality-digital-twin\ENGINE.py

只允许：
- VERSION = "1.3.0"
- 顶部 docstring 中当前正式组件版本同步为 1.3.0

必须保留：
METHOD_VERSION = "3.1.7"
EXPECTED_BROWSER_FINGERPRINT = "9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd"
EXPECTED_GOLDEN_SHA256 = "1c67a634e0c0fc24ed057752358f4c20a6c05550be6146fd8d11b1a723f25e08"
EXPECTED_TASK_SHA256
EXPECTED_VALID_SHA256
EXPECTED_REALITY_PACK_MANIFEST_SHA256

这些是现实证据 provenance（来源版本），不得升级或伪造。

## 3. 正式测试版本断言适配

在正式 test_browser_twin.py 中只允许把：

self.assertEqual(result["engine_version"], "1.1.0")

改成：

self.assertEqual(result["engine_version"], "1.3.0")

以下现实来源断言必须保持原样：
profile["method_version"] == "3.1.7"
profile["twin_source_version"] == "1.1.0"

解释：
- engine_version=1.3.0：当前正式发布组件版本。
- method_version=3.1.7 / twin_source_version=1.1.0：产生这份 Browser Reality/Twin 证据时的冻结来源版本。

## 4. 写入方式
只允许：
- PowerShell
- .NET File I/O
- Python 标准库的本地文本替换（若当前直接可运行）

禁止 apply_patch。
禁止启动任何浏览器。
禁止重新运行 Browser R3 / T1 / T2 / T3 / O1。
禁止修改 Profile / 网络 / Cookie / 登录态。
禁止重新设计 Twin。

每个精确替换必须断言：
- old pattern exactly 1 occurrence
- replacement exactly 1 occurrence
否则 STOP。

## 5. 验收顺序

1. python -m unittest discover 运行正式 test_browser_twin.py
   必须 6/6 PASS。

2. 单独运行正式 ENGINE.py selftest
   必须：
   engine_version=1.3.0
   passed=24
   case_count=24
   virtual_contract_99=PASS

3. 正式 Browser 验收必须继续：
   REALITY_PROFILE_VALIDATION=PASS
   BROWSER_GOLDEN_REPLAY=PASS
   TWIN_CRITICAL_UNKNOWN_COUNT=0
   MATERIAL_REALITY_TWIN_DELTA_COUNT=0
   SHADOW_ISOLATION=PASS
   REALITY_MUTATED=NO

4. 版本：
   MOTHER_VERSION=3.1.9
   REALITY_ANCHOR_VERSION=1.3.0
   EXACT_TWIN_VERSION=1.3.0

5. secret plaintext remote scan PASS。
6. git diff --check PASS。
7. git status 仅含合同允许的目标文件。
8. commit。
9. push：
   codex/first-principles-physical-limit-convergence-v3.1.9
10. remote readback HEAD + 关键文件 SHA。

## 6. 最终状态

只有全部 PASS 才允许：

FULL_BROWSER_TWIN=YES
PLAYWRIGHT_REALITY_SHADOW_BASELINE=PASS
ENVIRONMENT_99=PASS

任一步失败：
REALITY_DELTA=<实际事实>
ACTION=STOP
RETURN_TO_GPT=YES
禁止换路线。

## 7. 最终回传
PROMOTION_RESULT=
SOURCE_GATES=
RELEASE_ADAPTATION=FORMAL_ENGINE_PATH_PLUS_COMPONENT_VERSION
MOTHER_VERSION=
REALITY_ANCHOR_VERSION=
EXACT_TWIN_VERSION=
BROWSER_TWIN_TESTS=
LEGACY_SELFTEST=
BROWSER_R3_FINGERPRINT_SHA256=
MATERIAL_REALITY_TWIN_DELTA_COUNT=
SHADOW_ISOLATION=
REALITY_MUTATED=
FULL_BROWSER_TWIN=
PLAYWRIGHT_REALITY_SHADOW_BASELINE=
ENVIRONMENT_99=
SECRET_PLAINTEXT_ZERO_REMOTE=
COMMIT=
BRANCH=
HEAD=
REALITY_DELTA=
ACTION=STOP
