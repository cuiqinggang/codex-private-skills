# 【千问3.8 27B1｜本地智能体能力边界现实验收｜01｜实】
# METHOD=极限短时间引擎 v4.7.1
# TASK_TIME_ID=QWEN38-27B1-20260923-182700+0800
# 只执行冻结现实合同；禁止现场重新设计。

$ErrorActionPreference = 'Stop'
$Repo = 'C:\Users\A\Documents\Codex\codex-private-skills'
$Branch = 'codex/qwen38-27b1-v4.7.1-real-handoff-01'
$MethodBranch = 'codex/first-principles-physical-limit-convergence-v4.7.1'
$Work = 'C:\Users\A\Documents\Codex\2026-09-23\qwen38-27b1-v47-real-01'

if (-not (Test-Path -LiteralPath $Repo)) {
  Write-Host 'REALITY_DELTA=SHARED_REPO_MISSING'
  Write-Host 'VALID_REAL=FAIL'
  Write-Host 'ACTION=STOP_RETURN_TO_VIRTUAL'
  exit 2
}

New-Item -ItemType Directory -Force -Path $Work | Out-Null

git -C $Repo fetch origin ("refs/heads/{0}:refs/remotes/origin/{0}" -f $Branch)
if ($LASTEXITCODE -ne 0) {
  Write-Host 'REALITY_DELTA=FROZEN_QWEN_BRANCH_FETCH_FAIL'
  Write-Host 'VALID_REAL=FAIL'
  Write-Host 'ACTION=STOP_RETURN_TO_VIRTUAL'
  exit 2
}
git -C $Repo fetch origin ("refs/heads/{0}:refs/remotes/origin/{0}" -f $MethodBranch)
if ($LASTEXITCODE -ne 0) {
  Write-Host 'REALITY_DELTA=METHOD_V471_FETCH_FAIL'
  Write-Host 'VALID_REAL=FAIL'
  Write-Host 'ACTION=STOP_RETURN_TO_VIRTUAL'
  exit 2
}

$Files = @{
  'QWEN38-AGENT-CAPABILITY-REALITY-RUNNER-v1.py' = 'workspaces/qwen38-bonsai2-256k/QWEN38-AGENT-CAPABILITY-REALITY-RUNNER-v1.py'
  'Qwen3.8-27B-Bstar-Executor-Cert-Suite-v3.json' = 'workspaces/qwen38-bonsai2-256k/Qwen3.8-27B-Bstar-Executor-Cert-Suite-v3.json'
  'BONSAI2-256K-FINAL-v46-v2.py' = 'workspaces/qwen38-bonsai2-256k/BONSAI2-256K-FINAL-v46-v2.py'
  'QWEN38-AGENT-V47-REAL-HANDOFF-01.md' = 'workspaces/qwen38-bonsai2-256k/QWEN38-AGENT-V47-REAL-HANDOFF-01.md'
}

foreach ($Name in $Files.Keys) {
  $Spec = ('origin/{0}:{1}' -f $Branch, $Files[$Name])
  $Text = git -C $Repo show $Spec
  if ($LASTEXITCODE -ne 0) {
    Write-Host ('REALITY_DELTA=FROZEN_FILE_READ_FAIL:{0}' -f $Name)
    Write-Host 'VALID_REAL=FAIL'
    Write-Host 'ACTION=STOP_RETURN_TO_VIRTUAL'
    exit 2
  }
  $Text | Set-Content -LiteralPath (Join-Path $Work $Name) -Encoding utf8
}

$MethodSpec = ('origin/{0}:{1}' -f $MethodBranch, 'skills/first-principles-physical-limit-convergence/SKILL.md')
git -C $Repo show $MethodSpec | Set-Content -LiteralPath (Join-Path $Work 'METHOD-v4.7.1.md') -Encoding utf8
if ($LASTEXITCODE -ne 0) {
  Write-Host 'REALITY_DELTA=METHOD_V471_READ_FAIL'
  Write-Host 'VALID_REAL=FAIL'
  Write-Host 'ACTION=STOP_RETURN_TO_VIRTUAL'
  exit 2
}

$Prompt = @'
【千问3.8 27B1｜本地智能体能力边界现实验收｜01｜实】

TASK_TIME_ID=QWEN38-27B1-20260923-182700+0800
TASK_SEQUENCE=01
METHOD=极限短时间引擎 v4.7.1
PHASE=实

你只是冻结合同执行器，不是设计者。

必须先读取：
1. .\METHOD-v4.7.1.md
2. .\QWEN38-AGENT-V47-REAL-HANDOFF-01.md

禁止：
- 修改代理、FlClash、Windows 系统设置；
- 更换模型；
- 修改题目、runner 或 verifier；
- 让 Codex 替 Bonsai 回答测试题；
- 因某道能力题 FAIL 而现场修复；
- 清零 TASK_TIME_ID 或序号；
- 在现实阶段重新设计方案。

只执行以下冻结链：

A. 零 GPU runner 自检：
python .\QWEN38-AGENT-CAPABILITY-REALITY-RUNNER-v1.py --suite .\Qwen3.8-27B-Bstar-Executor-Cert-Suite-v3.json --out .\result --self-test

要求：
SELF_TEST=PASS
atomic_anchor_count=64
pairwise_total=800
pairwise_missing=0
jev_source_count=240
thinking_source_count=96

任何一项不满足：
REALITY_DELTA=CAPABILITY_RUNNER_SELFTEST_FAIL
VALID_REAL=FAIL
ACTION=STOP_RETURN_TO_VIRTUAL
立即停止，GPU_RUNS=0。

B. 自检 PASS 后，运行唯一现实入口：
python .\QWEN38-AGENT-CAPABILITY-REALITY-RUNNER-v1.py --suite .\Qwen3.8-27B-Bstar-Executor-Cert-Suite-v3.json --out .\result --reality --include-256k

能力题 FAIL 的语义：
它是“能力边界证据”，不是整个 Reality 失败，不得修题或替模型回答。

Reality 硬失败只有：
- runner/模型/runtime 无法启动；
- 证据结果文件不可读；
- 测量数量不完整；
- 256K Reality runner 非零退出；
- 发生 crash/OOM 且冻结 fallback 也失败。

现实完成后读取：
.\result\CAPABILITY-REALITY-RESULT.json

必须核对：
atomic=64
structured_decision=24
thinking_route=16
tool=8

若测量链完整且 256K runner PASS：
REAL_MEASUREMENT_COMPLETE=PASS

然后输出：
ATOMIC_PASS=<n>/64
STRUCTURED_DECISION_PASS=<n>/24
THINKING_ROUTE_PASS=<n>/16
TOOL_SELECTION_PASS=<n>/8
TOOL_EXECUTION_PASS=<n>/8
CAPABILITY_BOUNDARY_STATUS=FULL_PASS 或 BOUNDARY_FOUND
LOCAL_DECISION_MIN_MS=<值>
LOCAL_DECISION_P50_MS=<值>
LOCAL_DECISION_MAX_MS=<值>
LONG_CONTEXT_REALITY=PASS
RESULT_JSON=<完整路径>
REALITY_DELTA=NONE
VALID_REAL=PASS
ACTION=STOP_RETURN_TO_GPT_FINAL_JUDGE

若硬失败：
只输出最小 Reality Delta，保存已有证据，然后：
VALID_REAL=FAIL
ACTION=STOP_RETURN_TO_VIRTUAL

最后一行必须原样：
【千问3.8 27B1｜本地智能体能力边界现实验收｜01｜实】
'@

$DispatchTimestamp = '2026-09-23T22:52:44+08:00'
$ClosedRealStart = '2026-09-23T18:27:00+08:00'
$Sw = [System.Diagnostics.Stopwatch]::StartNew()

codex exec --ephemeral --skip-git-repo-check --sandbox workspace-write -C $Work --color never $Prompt
$CodexExit = $LASTEXITCODE

$Sw.Stop()
$End = Get-Date -Format o
Write-Host ('TASK_TIME_ID=QWEN38-27B1-20260923-182700+0800')
Write-Host ('TASK_SEQUENCE=01')
Write-Host ('T_CLOSED_REAL_START={0}' -f $ClosedRealStart)
Write-Host ('GPT_DISPATCH_TIMESTAMP={0}' -f $DispatchTimestamp)
Write-Host ('CODEX_ACTIVE_END_TIMESTAMP={0}' -f $End)
Write-Host ('CODEX_PROCESS_ACTIVE_MS={0}' -f [Math]::Round($Sw.Elapsed.TotalMilliseconds,3))
Write-Host ('CODEX_EXIT={0}' -f $CodexExit)
Write-Host 'TIME_RESET=NO'
Write-Host 'NEXT_SEQUENCE=02'
Write-Host '【千问3.8 27B1｜本地智能体能力边界现实验收｜01｜实】'
exit $CodexExit
