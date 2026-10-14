# GitHub → Windows 桥｜2026-10-15 现实验收冻结（当前状态）

```ini
SCOPE=GITHUB_ACTIONS_TO_WINDOWS_SELF_HOSTED_RUNNER
ACCEPTANCE=V2_BOUNDED_SMALL_NON_SENSITIVE_EVIDENCE_5_OF_5_PASS
SAMPLE_RUNS=38603199346,38603459215,38603580797,38603712945,38603850316
SHA_TESTED=f55521366c8fb6e0fc9845c67def4993b9831df1
MEAN_FULL_WALL_SECONDS=35.2
OBSERVED_RANGE_SECONDS=30..38
LEGACY_FULL_BACKUP=RETAINED
PERMANENT_ZERO_FAULT=NOT_PROVEN
ALL_TASKS_EQUIVALENT=NOT_PROVEN
DIRECT_MCP_PATH=NOT_TESTED_IN_THIS_ACCEPTANCE
```

## 当前结论和固定分流（不再为几秒微调生产执行器）

- **V2 有界非敏感小证据任务**：优先使用现有 `.github/workflows/windows-bridge-v2-bounded-artifact.yml`；Windows 自托管 Runner 运行任务、GitHub 托管 Runner 校验证据并运行官方 `actions/upload-artifact@v4`。五次独立 Run 首次尝试均 PASS，官方 Artifact 实际生成，30、36、36、36、38 秒。该路线已绕开原先 Windows 上下载第三方 Action ZIP 的薄弱环节。
- **FAST 不需要官方 Artifact 时**：保留 `.github/workflows/windows-bridge-v1-fast.yml`；已实测 [Run 38602210133](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38602210133) 27 秒。
- **原 FULL**：保留现有正式路线供不适配 V2 的任务和回退；[Run 38601884050](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38601884050) 97 秒成功，另有 144 秒成功样本；既往外部 Action 下载超时**不能**据此宣称已经永久根除。
- **使用 V2 的硬边界**：当前 ZIP Base64 上限为 480000 字符、托管端解码 ZIP 上限 360000 字节；只处理经审查的非敏感、小型、成功任务的证据。由于工作流日志可能显示 Base64 证据变量，**禁止传递密钥、个人敏感资料、保密业务输出**。限额超出、任务失败需保全证据、需验证回调或需额外业务语义时，不准虚称 V2 等价于 FULL；应依据合同采用经验证的替代路径。
- **限制如实记录**：Windows 失败时 `hosted-artifact` 不执行；五轮实际回调均为 `CALLBACK_NOT_CONFIGURED`；远端失败保全与回调未验收。官方 Artifact 成功不代表这两项完成。
- **停止规则**：当前短周期 5/5 合格；不重复相同算术负载以追逐 1–2 秒提升。只有出现真实故障、合同变更或新要求（失败证据保全、敏感证据、回调）时，才按成熟基线→最小差分修复→独立现实验收重开工作。
- **安全边界**：不调整 FlClash/Windows 代理，不重启或替换已运行的执行桥，不替换旧的 METHOD_REF；本次仅更新状态文档，无生产工作流代码变更。

冻结证据：
[R1](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38603199346) ·
[R2](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38603459215) ·
[R3](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38603580797) ·
[R4](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38603712945) ·
[R5](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38603850316)。

---

## 历史记录（原桥 0.1.2 阶段；“Runner 未上线”等结论现已过期）

# v2.0 无人执行桥

```ini
BRIDGE_SKILL_VERSION=0.1.2
STATIC_GATE=PASS
REALITY_RUN_ID=36899361139
WINDOWS_REALITY=QUEUED_WAITING_SELF_HOSTED_RUNNER
```

## 最小任务入口

```text
workspaces/extreme-time-automation-loop-v2.0/bridge/tasks/<TASK_ID>.json
```

新任务 JSON 进入 main 后，工作流先做静态门禁；只有发现恰好一个任务 JSON 发生变化，才调度本地 Windows。

## 当前已走通

```text
任务JSON提交
→ GitHub workflow触发
→ PowerShell解析 PASS
→ 任务合同 PASS
→ Windows Reality queued
```

当前唯一缺口：
目标 Windows 尚无在线 [self-hosted, Windows, X64] runner。

## 一次性接入

```text
skills/extreme-time-automation-bridge/bootstrap/Install-GitHubSelfHostedRunner.ps1
```

安装后当前已排队的 ETAL-BRIDGE-SMOKE-001 可以直接被领取，不需要重新设计桥。

## 非任务提交

v0.1.2 起，技能包/文档/执行器更新只做 hosted 静态检查，不再制造本地 runner 队列。
