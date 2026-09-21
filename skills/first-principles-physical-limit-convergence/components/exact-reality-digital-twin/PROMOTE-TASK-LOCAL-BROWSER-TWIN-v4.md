# Task-local Browser Twin → 唯一正式 Twin 提升合同 v4

## 定位
- 核心：高智能虚拟成熟
- 阶段：STEP 3 冻结成果正式提升与最终验收
- 只吸收 v3 现实差异：stash pop 在 exact-reality-digital-twin/manifest.json 产生唯一 Git unmerged 冲突。
- 禁止重新设计 Browser R3 / Twin；禁止重新采集；禁止重新跑 T1/T2/T3/O1。

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

远端冻结基线 HEAD：
d8566eeddbf512eb6b7aeb464c35ba7de6fb1612

隔离 worktree：
C:\Users\A\Documents\Codex\worktrees\first-principles-v3.1.9-promotion

冲突目标：
skills\first-principles-physical-limit-convergence\components\exact-reality-digital-twin\manifest.json

## -1. 本轮远端权威冻结

执行开始第一件事：

```text
git fetch origin codex/first-principles-physical-limit-convergence-v3.1.9
REMOTE_AUTHORITY_HEAD=$(git rev-parse origin/codex/first-principles-physical-limit-convergence-v3.1.9)
```

从这一刻起，本轮只认该 `REMOTE_AUTHORITY_HEAD`；执行中即使远端之后又变化，也不得漂移到新的 HEAD。

v4 合同与远端 manifest 都必须使用：

```text
git show <REMOTE_AUTHORITY_HEAD>:<path>
```

读取。

最终 push 前若远端实际 HEAD 已不再等于 `REMOTE_AUTHORITY_HEAD`：
REALITY_DELTA=REMOTE_BRANCH_MOVED_DURING_PROMOTION
STOP。
禁止自动追新 HEAD。

## 0. 冲突边界门禁
先只读：
git status --short
git ls-files -u
git stash list

必须满足：
- 只有上述 exact Twin manifest 处于 unmerged；
- stash 仍保留；
- 其它 partial changes 全部属于 v2/v3 提升合同目标文件。

若还有第二个 unmerged 文件或未知文件：
REALITY_DELTA=UNEXPECTED_UNMERGED_OR_PARTIAL_CHANGE
STOP。

禁止再次 stash pop。
禁止 reset。
禁止 clean。
禁止 checkout --ours / --theirs。
禁止删除 stash。

## 1. 唯一冲突解决算法

### 1.1 远端 HEAD 为 manifest 唯一基底
从远端冻结 HEAD
d8566eeddbf512eb6b7aeb464c35ba7de6fb1612
读取：

skills/first-principles-physical-limit-convergence/components/exact-reality-digital-twin/manifest.json

必须验证远端 blob SHA256/内容可读取。

然后使用 PowerShell/.NET 普通文件 I/O，把该远端 JSON 内容 byte-for-byte 写入本地冲突 manifest。

禁止使用 apply_patch。

写回后：
- JSON parse PASS；
- 不得含 <<<<<<< / ======= / >>>>>>>；
- git add 仅该 manifest，用于标记冲突已解决；
- git ls-files -u 必须为空。

stash 继续保留，不再应用。

## 2. 在远端基底上确定性形成最终正式 manifest

对刚恢复的 JSON 做 parse → 精确字段更新 → serialize。
不得删除任何历史字段，除非字段本身被下面的新正式状态覆盖。

最终必须至少满足：

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
promotion_contract = PROMOTE-TASK-LOCAL-BROWSER-TWIN-v4.md
promotion_target_version = 1.3.0
write_path = POWERSHELL_DOTNET_DETERMINISTIC_IO
blocked_write_path = APPLY_PATCH_WINDOWS_1344
release_adaptation = FORMAL_ENGINE_PATH_PLUS_COMPONENT_VERSION

browser_reality_authority.fingerprint =
9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd

browser_reality_authority.canonical_golden_sha256 =
1c67a634e0c0fc24ed057752358f4c20a6c05550be6146fd8d11b1a723f25e08

browser_reality_authority.reality_profile_validation = PASS
browser_reality_authority.browser_golden_replay = PASS
browser_reality_authority.material_delta_count = 0
browser_reality_authority.shadow_isolation = PASS

保留 virtual_fusion / virtual_99_hardening_legacy 作为历史字段；
其中旧的 NOT_YET 不能再作为当前 browser_r3 / environment_99 状态。

## 3. 继续执行 v3 的正式发布适配

### 3.1 正式测试路径
目标：
skills\first-principles-physical-limit-convergence\components\exact-reality-digital-twin\tests\test_browser_twin.py

只允许精确变更：

旧：
WORKSPACE = Path(__file__).resolve().parents[2]
ENGINE = WORKSPACE / "TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW" / "exact-reality-digital-twin" / "ENGINE.py"

新：
REALITY_WORKSPACE = Path(r"C:\Users\A\playwright-browser-automation5-final-reality-competition-work")
COMPONENT_ROOT = Path(__file__).resolve().parents[1]
ENGINE = COMPONENT_ROOT / "ENGINE.py"

run_mode 中：
str(WORKSPACE)
→
str(REALITY_WORKSPACE)

### 3.2 当前正式组件版本
正式 ENGINE.py：
VERSION = "1.3.0"
顶部当前组件 docstring 版本 = 1.3.0

必须保留现实证据 provenance：
METHOD_VERSION = "3.1.7"
EXPECTED_BROWSER_FINGERPRINT = 9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd
EXPECTED_GOLDEN_SHA256 = 1c67a634e0c0fc24ed057752358f4c20a6c05550be6146fd8d11b1a723f25e08
EXPECTED_TASK_SHA256 不变
EXPECTED_VALID_SHA256 不变
EXPECTED_REALITY_PACK_MANIFEST_SHA256 不变

正式 test_browser_twin.py：
engine_version 断言 1.1.0 → 1.3.0

但必须保持：
profile["method_version"] == "3.1.7"
profile["twin_source_version"] == "1.1.0"

## 4. 母技能和 Reality Anchor 正式状态
确保：

母技能 VERSION = 3.1.9
Reality Anchor VERSION = 1.3.0
Exact Twin VERSION = 1.3.0

母技能 manifest 只做最终状态同步：
- reality_anchor.version = 1.3.0
- reality_anchor.browser_r3.real_capture = PASS
- reality_anchor.browser_r3.browser_twin_input_ready = true
- reality_anchor.browser_r3.fingerprint = 9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd
- reality_anchor.browser_r3.safe_final_promotion = PASS
- reality_anchor.parent_method = first-principles-physical-limit-convergence@3.1.9
- exact_reality_digital_twin.current_repo_version = 1.3.0
- exact_reality_digital_twin.promotion_target_version = 1.3.0
- exact_reality_digital_twin.promotion_contract = components/exact-reality-digital-twin/PROMOTE-TASK-LOCAL-BROWSER-TWIN-v4.md
- exact_reality_digital_twin.promotion_status = PROMOTED_PASS
- exact_reality_digital_twin.environment_99 = PASS

不得改变三个核心。

## 5. 写入规则
只允许：
- PowerShell
- .NET File I/O
- Python 标准库本地 JSON/text 精确写入

禁止 apply_patch。
每个文本替换必须 old pattern exactly 1 occurrence。
不满足立即 STOP。

## 6. 最终验收
按顺序：

1. git ls-files -u = empty
2. 正式 Browser Twin unittest = 6/6 PASS
3. 正式 ENGINE selftest：
   engine_version=1.3.0
   passed=24
   case_count=24
   virtual_contract_99=PASS
4. Reality Profile validation = PASS
5. Browser Golden Replay = PASS
6. Twin Critical Unknown Count = 0
7. Material Reality/Twin Delta Count = 0
8. Shadow Isolation = PASS
9. Reality Mutated = NO
10. Browser R3 fingerprint 精确匹配
11. R3 safe final promoted = PASS
12. Secret plaintext zero remote = PASS
13. git diff --check = PASS
14. git status 仅合同目标文件
15. commit
16. push 同一分支
17. remote readback HEAD + VERSION/manifest/ENGINE/test SHA

全部 PASS 才允许：
FULL_BROWSER_TWIN=YES
PLAYWRIGHT_REALITY_SHADOW_BASELINE=PASS
ENVIRONMENT_99=PASS

任一失败：
REALITY_DELTA=<实际事实>
ACTION=STOP
RETURN_TO_GPT=YES

## 6.5 本地通过后的唯一 Git 同步算法

本节只处理“本地 worktree 起点早于 REMOTE_AUTHORITY_HEAD”这一事实，不改变发布内容。

1. 所有第 6 节本地验收先 PASS。
2. 将当前合同允许的目标文件创建一个本地 promotion commit：
   TEMP_PROMOTION_COMMIT=<sha>
3. 执行：
   git rebase <REMOTE_AUTHORITY_HEAD>
4. 若 rebase 无冲突：继续。
5. 若发生冲突：
   - 只允许 exact-reality-digital-twin/manifest.json 一个冲突文件；
   - 若出现第二个冲突文件：REALITY_DELTA=UNEXPECTED_REBASE_CONFLICT；abort rebase；STOP。
6. 若唯一冲突仍是 exact Twin manifest：
   - 不选 ours/theirs；
   - 按本合同第 2 节“最终正式 manifest”从 JSON 重新确定性生成；
   - git add 仅该 manifest；
   - 使用非交互 rebase continue；
   - 禁止编辑其它文件。
7. rebase 完成后必须再次完整执行第 6 节 1–14 验收。
8. 再次读取远端 HEAD；必须仍等于 REMOTE_AUTHORITY_HEAD。
9. 普通 push，禁止 force / force-with-lease。
10. remote readback HEAD 必须等于 push 后本地 HEAD。

rebase 前后的业务文件语义必须一致；以测试、Fingerprint、Delta、Shadow 与关键 JSON 字段复验为准。

## 7. stash 收尾
只有 commit + push + remote readback 全 PASS 后：
- stash 仍只作为历史恢复点存在；
- 本任务不删除 stash。
后续是否清理 stash 属于独立维护，不影响本验收。

## 8. 最终回传
PROMOTION_RESULT=
SOURCE_GATES=
CONFLICT_RESOLUTION=REMOTE_HEAD_MANIFEST_REBUILD
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
