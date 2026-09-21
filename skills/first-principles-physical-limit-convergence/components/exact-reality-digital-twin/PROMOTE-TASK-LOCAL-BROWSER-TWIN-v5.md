# Task-local Browser Twin → 唯一正式 Twin 提升合同 v5

## 定位
- 核心：高智能虚拟成熟
- 阶段：STEP 3 冻结成果正式提升与最终验收
- 只吸收 v4 的 Git 引用现实差异。
- 禁止重新设计 Browser R3 / Twin；禁止重新采集；禁止重新运行 T1/T2/T3/O1。

## 已知冻结事实
SOURCE_GATES=PASS
BROWSER_R3_FINGERPRINT_SHA256=9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd
MATERIAL_REALITY_TWIN_DELTA_COUNT=0
SHADOW_ISOLATION=PASS
REALITY_MUTATED=NO
TASK_LOCAL_BROWSER_TWIN_TESTS=6/6 PASS
LEGACY_SELFTEST=24/24 PASS
HISTORICAL_T_STAR_REAL_MS=1525.09

分支：
codex/first-principles-physical-limit-convergence-v3.1.9

执行开始时 GitHub 远端权威 HEAD：动态读取并冻结为 REMOTE_AUTHORITY_HEAD。\n
隔离 worktree：
C:\Users\A\Documents\Codex\worktrees\first-principles-v3.1.9-promotion

唯一当前 unmerged 文件：
skills\first-principles-physical-limit-convergence\components\exact-reality-digital-twin\manifest.json

## 0. 远端权威引用必须显式刷新

禁止使用普通：
git fetch origin <branch>
之后直接假设 origin/<branch> 已更新。

唯一允许：

git fetch origin ^
  refs/heads/codex/first-principles-physical-limit-convergence-v3.1.9:refs/remotes/origin/codex/first-principles-physical-limit-convergence-v3.1.9

然后：

REMOTE_AUTHORITY_HEAD=$(git rev-parse refs/remotes/origin/codex/first-principles-physical-limit-convergence-v3.1.9)

必须同时满足：
- REMOTE_AUTHORITY_HEAD 非空；
- git show REMOTE_AUTHORITY_HEAD:.../PROMOTE-TASK-LOCAL-BROWSER-TWIN-v5.md 可读；
- 该 v5 文件内容包含“唯一正式 Twin 提升合同 v5”；
- 远端 manifest 的 promotion_contract 指向 v5。

否则：
REALITY_DELTA=REMOTE_AUTHORITY_REF_INVALID
STOP。

本轮禁止使用 FETCH_HEAD 作为 authority。
从这里开始冻结 REMOTE_AUTHORITY_HEAD；执行期间不得漂移。

## 1. 当前冲突边界
只读：

git status --short
git ls-files -u
git stash list

必须：
- 只有 exact Twin manifest unmerged；
- stash retained；
- 其它 partial changes 只属于 v2/v3/v4 允许的 promotion 文件。

否则 STOP。

禁止：
- stash pop
- reset
- clean
- checkout --ours
- checkout --theirs
- 删除 stash

## 2. 唯一 manifest 冲突解决

从冻结 authority 读取：\n\ngit show <REMOTE_AUTHORITY_HEAD>:skills/first-principles-physical-limit-convergence/components/exact-reality-digital-twin/manifest.json

此内容为唯一基底。

使用 PowerShell/.NET 普通文件 I/O byte-for-byte 写回本地 manifest。

必须：
- JSON parse PASS
- 无 conflict markers
- git add 仅该 manifest
- git ls-files -u = empty

然后按本合同第 3 节确定性形成最终正式 manifest。

## 3. 最终正式 manifest

必须形成：

component_id = exact-reality-digital-twin
version = 1.3.0
parent_method = first-principles-physical-limit-convergence@3.1.9
reality_anchor_skill = reality-execution-environment-anchor@1.3.0
canonical_single_implementation = true

host_r2.status = READY
host_r2.contract_selftest = 24/24 PASS

browser_r3.real_capture = PASS
browser_r3.fingerprint = 9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd
browser_r3.twin_input_ready = true
browser_r3.golden_replay = PASS
browser_r3.reality_twin_delta = 0
browser_r3.shadow_run = PASS

environment_99 = PASS

promotion_status = PROMOTED_PASS
promotion_contract = PROMOTE-TASK-LOCAL-BROWSER-TWIN-v5.md
promotion_target_version = 1.3.0
write_path = POWERSHELL_DOTNET_DETERMINISTIC_IO
blocked_write_path = APPLY_PATCH_WINDOWS_1344
release_adaptation = FORMAL_ENGINE_PATH_PLUS_COMPONENT_VERSION
conflict_resolution = FROZEN_REMOTE_HEAD_MANIFEST_REBUILD

browser_reality_authority.fingerprint =
9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd

browser_reality_authority.canonical_golden_sha256 =
1c67a634e0c0fc24ed057752358f4c20a6c05550be6146fd8d11b1a723f25e08

browser_reality_authority.reality_profile_validation = PASS
browser_reality_authority.browser_golden_replay = PASS
browser_reality_authority.material_delta_count = 0
browser_reality_authority.shadow_isolation = PASS

保留 legacy / virtual_fusion 历史字段，但历史 NOT_YET 不得覆盖当前 browser_r3 / environment_99 状态。

## 4. 正式发布适配
继续完全沿用 v4 已冻结规则：

### 测试路径
test_browser_twin.py：

WORKSPACE = Path(__file__).resolve().parents[2]
ENGINE = WORKSPACE / "TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW" / "exact-reality-digital-twin" / "ENGINE.py"

改成：

REALITY_WORKSPACE = Path(r"C:\Users\A\playwright-browser-automation5-final-reality-competition-work")
COMPONENT_ROOT = Path(__file__).resolve().parents[1]
ENGINE = COMPONENT_ROOT / "ENGINE.py"

run_mode 中：
str(WORKSPACE)
→
str(REALITY_WORKSPACE)

### 正式组件版本
ENGINE.py：
VERSION = "1.3.0"
docstring 当前正式组件版本 = 1.3.0

必须保留：
METHOD_VERSION = "3.1.7"
EXPECTED_BROWSER_FINGERPRINT 不变
EXPECTED_GOLDEN_SHA256 不变
EXPECTED_TASK_SHA256 不变
EXPECTED_VALID_SHA256 不变
EXPECTED_REALITY_PACK_MANIFEST_SHA256 不变

test_browser_twin.py：
engine_version 断言 1.1.0 → 1.3.0

必须保留：
profile["method_version"] == "3.1.7"
profile["twin_source_version"] == "1.1.0"

## 5. 版本和母 manifest
必须：

MOTHER_VERSION=3.1.9
REALITY_ANCHOR_VERSION=1.3.0
EXACT_TWIN_VERSION=1.3.0

母 manifest 最终同步：
- reality_anchor.version = 1.3.0
- reality_anchor.parent_method = first-principles-physical-limit-convergence@3.1.9
- reality_anchor.browser_r3.real_capture = PASS
- reality_anchor.browser_r3.browser_twin_input_ready = true
- reality_anchor.browser_r3.fingerprint = 9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd
- reality_anchor.browser_r3.safe_final_promotion = PASS
- exact_reality_digital_twin.current_repo_version = 1.3.0
- exact_reality_digital_twin.promotion_target_version = 1.3.0
- exact_reality_digital_twin.promotion_contract = components/exact-reality-digital-twin/PROMOTE-TASK-LOCAL-BROWSER-TWIN-v5.md
- exact_reality_digital_twin.promotion_status = PROMOTED_PASS
- exact_reality_digital_twin.environment_99 = PASS

## 6. 写入规则
只允许：
- PowerShell
- .NET File I/O
- Python 标准库本地 JSON/text 精确写入

禁止 apply_patch。

每个文本替换 old pattern 必须 exactly 1 occurrence。

## 7. 本地验收
必须全部 PASS：

1. git ls-files -u = empty
2. 正式 Browser Twin unittest = 6/6 PASS
3. 正式 ENGINE selftest = 24/24 PASS
4. engine_version = 1.3.0
5. Reality Profile validation = PASS
6. Browser Golden Replay = PASS
7. Twin Critical Unknown Count = 0
8. Material Reality/Twin Delta Count = 0
9. Shadow Isolation = PASS
10. Reality Mutated = NO
11. Browser R3 fingerprint 精确匹配
12. R3 safe final promoted = PASS
13. Secret plaintext zero remote = PASS
14. git diff --check = PASS
15. git status 只含合同目标文件

## 8. 唯一 Git 收口

本地验收全部 PASS 后：

1. 创建一个本地 promotion commit。
2. 此 commit 的父提交允许早于 REMOTE_AUTHORITY_HEAD。
3. 执行：
   git rebase <REMOTE_AUTHORITY_HEAD>
4. 若无冲突，继续。
5. 若有冲突：
   - 只允许 exact Twin manifest 一个文件；
   - 用本合同第 3 节最终 JSON 再机械生成；
   - git add 该 manifest；
   - 非交互 rebase continue。
6. 若出现第二个冲突：
   REALITY_DELTA=UNEXPECTED_REBASE_CONFLICT
   abort rebase
   STOP。
7. rebase 后重新完整执行第 7 节。
8. 再次读取 GitHub 远端分支实际 HEAD；必须仍等于本轮开始冻结的 REMOTE_AUTHORITY_HEAD
9. 普通 push。
10. 禁止 force / force-with-lease。
11. remote readback HEAD 必须等于本地 HEAD。

## 9. stash
stash 保留，不再 pop，不删除。

## 10. 最终状态
全部 PASS 才允许：

FULL_BROWSER_TWIN=YES
PLAYWRIGHT_REALITY_SHADOW_BASELINE=PASS
ENVIRONMENT_99=PASS

否则 STOP。

## 11. 最终回传
PROMOTION_RESULT=
SOURCE_GATES=
REMOTE_AUTHORITY_HEAD=
CONFLICT_RESOLUTION=FROZEN_REMOTE_HEAD_MANIFEST_REBUILD
UNMERGED_FILES=
MOTHER_VERSION=
REALITY_ANCHOR_VERSION=
EXACT_TWIN_VERSION=
BROWSER_TWIN_TESTS=
LEGACY_SELFTEST=
BROWSER_R3_FINGERPRINT_SHA256=
MATERIAL_REALITY_TWIN_DELTA_COUNT=
SHADOW_ISOLATION=
REALITY_MUTATED=
R3_SAFE_FINAL_PROMOTED=
SECRET_PLAINTEXT_ZERO_REMOTE=
FULL_BROWSER_TWIN=
PLAYWRIGHT_REALITY_SHADOW_BASELINE=
ENVIRONMENT_99=
STASH_RETAINED=
COMMIT=
BRANCH=
HEAD=
REALITY_DELTA=
ACTION=STOP
