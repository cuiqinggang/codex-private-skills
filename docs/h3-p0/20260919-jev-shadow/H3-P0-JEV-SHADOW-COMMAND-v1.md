# H3-P0 Jev Shadow Command v1

状态：READY / SHADOW_ONLY / GPU_RUNS=0

## 目标

使用已经冻结的 H3-P0 历史事实作为 known-answer dataset，通过 OpenRouter Decisions API 调用 TypeSafe Jev 1.13，测量：

- 25 个语义 known-answer 的准确率与关键错误数；
- 22 个真实 H3-P0 formal attempt 的 deterministic QC 代码复现与本机纳秒级基线；
- mega / family / case 三种批处理方式的端到端 P50/P95；
- confidence threshold 与零错误自动覆盖率；
- 每轮实际 API cost；
- 哪些节点适合 CODE / JEV / GPT；
- 是否达到 GATED_SHADOW_PASS。

本命令绝不重新运行 H3 GPU，绝不修改 H3-P0 FINAL_99。

## 权威输入

分支：

`codex/first-principles-physical-limit-convergence-v3.1.2-jev-h3p0-shadow`

必须读取：

1. `skills/first-principles-physical-limit-convergence/references/JEV-DECISION-ACCELERATOR-v0.1.md`
2. `docs/h3-p0/20260919-jev-shadow/H3-P0-JEV-SHADOW-DATASET-v1.json`
3. `docs/h3-p0/20260919-jev-shadow/h3_p0_jev_shadow.py`

## API Key 硬规则

`OPENROUTER_API_KEY` 只能存在于本机进程环境或安全凭据存储中。

禁止写入 GitHub、文件、日志、prompt、result JSON、命令行参数或 shell history。

若环境变量不存在：

`RETURN OPENROUTER_KEY_MISSING`

不得要求把 key 写进仓库，不得通过降低隐私策略绕过。

## 隐私路由

每个 Jev request 固定：

```json
{
  "provider": {
    "zdr": true,
    "data_collection": "deny"
  }
}
```

如果没有符合条件的 endpoint：

`RETURN PRIVACY_ROUTE_UNAVAILABLE`

禁止自动删除 ZDR 或改成 data_collection=allow。

## 执行

从仓库根目录：

```powershell
git fetch origin
git switch codex/first-principles-physical-limit-convergence-v3.1.2-jev-h3p0-shadow
git pull --ff-only

python -m py_compile docs/h3-p0/20260919-jev-shadow/h3_p0_jev_shadow.py

python docs/h3-p0/20260919-jev-shadow/h3_p0_jev_shadow.py --model typesafe/jev-1.13 --modes mega,family,case --repeats 5
```

禁止启动 ComfyUI/H3；禁止修改任何冻结 H3 文件。

## 验收

必须存在：

- `H3-P0-JEV-SHADOW-RESULT-v1.json`
- `H3-P0-JEV-SHADOW-RESULT-v1.md`

并验证：

```text
H3_GPU_RUNS=0
FROZEN_H3_MUTATED=NO
API_KEY_IN_RESULT=NO
API_KEY_IN_GIT_DIFF=NO
```

第一轮只允许三种裁决：

```text
GATED_SHADOW_PASS
ADVISORY_ONLY
REJECT_FOR_CONTROL
```

`GATED_SHADOW_PASS` 仍不等于生产成熟，只代表允许进入下一次低风险 real gated control-plane 验证。

## 写回共同工作区

只提交本轮结果文件；不要改历史 H3-P0 冻结事实。

```powershell
git add docs/h3-p0/20260919-jev-shadow/H3-P0-JEV-SHADOW-RESULT-v1.json docs/h3-p0/20260919-jev-shadow/H3-P0-JEV-SHADOW-RESULT-v1.md
git diff --cached --check
git diff --cached | Select-String -Pattern 'sk-or-|OPENROUTER_API_KEY='
```

上一步如果出现任何真实 key，立即停止并清除，不得提交。

若无 secret：

```powershell
git commit -m "exp: record H3-P0 Jev shadow result"
git push origin HEAD:codex/first-principles-physical-limit-convergence-v3.1.2-jev-h3p0-shadow
git ls-remote origin refs/heads/codex/first-principles-physical-limit-convergence-v3.1.2-jev-h3p0-shadow
```

## 回传

只回传这些字段：

```text
H3_P0_JEV_SHADOW_COMPLETE=YES|NO
REMOTE_HEAD=<sha>
MODEL=<resolved model>
SEMANTIC_CASES=25
FORMAL_QC_CASES=22
DETERMINISTIC_QC_ACCURACY=<value>
DETERMINISTIC_QC_NS_PER_DECISION=<value>
H3_GPU_RUNS=0
BEST_BATCH_MODE=mega|family|case|NONE
ACCURACY_MEAN=<value>
ACCURACY_MIN=<value>
CRITICAL_ERRORS=<n>
INVALID_OUTPUTS=<n>
BEST_THRESHOLD=<value|NONE>
AUTO_COVERAGE=<value|NONE>
ACCEPTED_ACCURACY=<value|NONE>
RUN_P50_MS=<value>
RUN_P95_MS=<value>
COST_USD_PER_RUN=<value>
ROLE=GATED_SHADOW_PASS|ADVISORY_ONLY|REJECT_FOR_CONTROL
```
