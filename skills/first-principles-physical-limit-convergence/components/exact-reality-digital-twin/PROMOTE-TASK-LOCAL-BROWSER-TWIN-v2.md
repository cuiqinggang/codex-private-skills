# Task-local Browser Twin → 唯一正式 Twin 提升合同 v2

## 定位
- 核心：高智能虚拟成熟
- 阶段：STEP 3 冻结成果正式提升与现实验收
- 本合同只修正发布写入方式，不改变任何 Browser R3 / Twin 设计、证据、门禁或时间基线。
- v1 因 Windows Sandbox SetTokenInformation 1344 阻断 apply_patch，保留为历史证据。

## 已知现实
SOURCE_GATES=PASS
TASK_LOCAL_BROWSER_TWIN_TESTS=6/6 PASS
LEGACY_SELFTEST=24/24 PASS
BROWSER_R3_FINGERPRINT_SHA256=9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd
MATERIAL_REALITY_TWIN_DELTA_COUNT=0
SHADOW_ISOLATION=PASS
REALITY_MUTATED=NO
HISTORICAL_T_STAR_REAL_MS=1525.09

## 唯一变化
禁止使用 apply_patch 或任何会触发 Windows sandbox child-token 写入路径的补丁工具。

只允许使用已经现实可用的普通 PowerShell/.NET 文件 I/O：
- Copy-Item / CopyTo
- [IO.File]::ReadAllBytes / WriteAllBytes
- [IO.File]::ReadAllText / WriteAllText

写入范围严格限制在隔离 worktree：
C:\Users\A\Documents\Codex\worktrees\first-principles-v3.1.9-promotion

禁止修改浏览器、Profile、网络、代理、Cookie、登录态。
禁止重跑 Browser R3、T1/T2/T3、O1。
禁止重新设计 Twin。

## 0. 先处理已有 partial changes
先只读：
git status --short
git diff --binary

若发现任何不属于本提升合同目标文件的变化：
REALITY_DELTA=UNEXPECTED_PARTIAL_WORKTREE_CHANGE
STOP。

若 partial changes 全部属于目标提升文件，则保留并逐文件继续机械校验；禁止 reset/checkout 覆盖未知变化。

## 1. 源目录
Task-local Twin：
C:\Users\A\playwright-browser-automation5-final-reality-competition-work\TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW

Browser R3 final：
C:\Users\A\playwright-browser-automation5-final-reality-competition-work\R3-BROWSER-REALITY\final

## 2. 机械复制
使用普通 PowerShell/.NET I/O 复制，不使用 patch：

### 唯一 Twin
源：
TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW\exact-reality-digital-twin\ENGINE.py
TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW\tests\test_browser_twin.py
TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW\PLAYWRIGHT_GOLDEN_REALITY_PROFILE.json
TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW\BROWSER-PROFILE-VALIDATION.json
TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW\BROWSER-REALITY-REPLAY.json
TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW\BROWSER-REALITY-TWIN-DELTA.json
TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW\BROWSER-SHADOW-ISOLATION.json
TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW\BROWSER-REALITY-REPLAY-AFTER-SHADOW.json

目标：
skills\first-principles-physical-limit-convergence\components\exact-reality-digital-twin\ENGINE.py
skills\first-principles-physical-limit-convergence\components\exact-reality-digital-twin\tests\test_browser_twin.py
skills\first-principles-physical-limit-convergence\components\exact-reality-digital-twin\reality-profiles\playwright-golden\<上述六个 JSON>

### R3 safe final
源：
R3-BROWSER-REALITY\final\BROWSER-R3-FINAL-ANCHOR.json
R3-BROWSER-REALITY\final\BROWSER-R3-FINGERPRINT.json
R3-BROWSER-REALITY\final\BROWSER-R3-MANIFEST.json

目标：
skills\reality-execution-environment-anchor\snapshots\2026-09-21-r3-browser-final\

只复制 safe final；禁止 raw。

复制后每个文件必须 byte-for-byte SHA256 一致。

## 3. 版本与状态文件
不用 patch。使用 PowerShell/.NET 精确写入或 JSON parse→modify→serialize：

- 母技能 VERSION = 3.1.9
- Reality Anchor VERSION = 1.3.0
- Exact Twin VERSION = 1.3.0

manifest 必须反映：
- Browser R3 real capture = PASS
- Browser twin input ready = YES
- Browser R3 fingerprint = 9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd
- Reality Profile validation = PASS
- Browser Golden Replay = PASS
- Material Reality/Twin Delta Count = 0
- Shadow Isolation = PASS
- Reality Mutated = NO
- Full Browser Twin = YES
- Environment-99 = PASS
- Historical T* = 1525.09 ms

不得删除历史字段；v1.2.0/v3.1.8 路线留在 Git 历史。

## 4. 验收
按顺序机械执行：

1. 源/目标 SHA256 对比全部 PASS
2. python -m unittest discover 运行正式 test_browser_twin.py → 6/6 PASS
3. 正式 ENGINE legacy selftest → 24/24 PASS
4. 读取正式 reality profile / replay / delta / shadow JSON，确认：
   - REALITY_PROFILE_VALIDATION=PASS
   - BROWSER_GOLDEN_REPLAY=PASS
   - TWIN_CRITICAL_UNKNOWN_COUNT=0
   - MATERIAL_REALITY_TWIN_DELTA_COUNT=0
   - SHADOW_ISOLATION=PASS
   - REALITY_MUTATED=NO
5. secret plaintext remote scan PASS
6. git diff --check PASS
7. git status 只允许本合同目标文件
8. commit
9. push 同一冻结分支
10. remote readback HEAD 与关键文件 SHA

任一步失败：
REALITY_DELTA=<实际事实>
ACTION=STOP
RETURN_TO_GPT=YES
禁止换路线。

## 5. 最终回传
PROMOTION_RESULT=
SOURCE_GATES=
WRITE_PATH=POWERSHELL_DOTNET_DETERMINISTIC_IO
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
ENVIRONMENT_99=
SECRET_PLAINTEXT_ZERO_REMOTE=
COMMIT=
BRANCH=
HEAD=
REALITY_DELTA=
ACTION=STOP
