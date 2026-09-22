# v4.5.4 Virtual -> Real Handoff

This handoff is part of VIRTUAL completion. It is not a third method step.

## Frozen real artifact

- shared repository: cuiqinggang/codex-private-skills
- frozen commit: daf1d1b059daf5f975de414579c3ab14c1519f3b
- frozen path: docs/first-principles/20260922-v4.5.4/REAL-ENTRY-FROZEN.ps1
- git blob sha: 629be3ce49dd951d23b583c3a51678db704b5a46
- ASCII-only: PASS
- live GitHub dependency inside real runner: NONE
- live git dependency inside real runner: NONE

## One user action

Paste this single PowerShell block. It invokes Codex and hands it the complete frozen REAL contract.

```powershell
$repo   = 'C:\Users\A\Documents\Codex\codex-private-skills'
$commit = 'daf1d1b059daf5f975de414579c3ab14c1519f3b'
$path   = 'docs/first-principles/20260922-v4.5.4/REAL-ENTRY-FROZEN.ps1'

codex exec --ephemeral --skip-git-repo-check --sandbox workspace-write -C $repo --color never @"
【ESTE-20260922-001｜极限短时间引擎 v4.5.4｜实】
只执行冻结合同，不分析、不重新设计、不现场修复。

冻结提交：$commit
冻结文件：$path

执行规则：
- 先检查该 commit 是否已存在于本地仓库。
- 若已存在，禁止联网，直接使用本地对象。
- 若不存在，只允许获取分支 codex/first-principles-physical-limit-convergence-v4.5.4；若第一次 git fetch 因传输错误失败，原样重试一次；禁止修改代理或系统设置。
- 获取后必须确认冻结 commit=$commit 存在。
- 用 git show 从该 commit 读取 $path，写到 $env:TEMP\REAL-ENTRY-FROZEN-v4.5.4.ps1，编码必须为 ASCII。
- 执行：pwsh -NoProfile -File $env:TEMP\REAL-ENTRY-FROZEN-v4.5.4.ps1
- 完整原样返回现实输出，不添加方案，不修改冻结文件。

如果两次获取都失败，只返回：
HANDOFF_DELTA=GIT_TRANSPORT_FAIL
ACTION=STOP
RETURN_TO_GPT=YES
"@
```

## Timing rule

The Codex active interval is part of the same TASK_TIME_ID and must be added to T_VALID_ACTIVE_GLOBAL.
Human idle before pasting the command is excluded.
