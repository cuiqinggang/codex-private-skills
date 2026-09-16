# EXECUTION CLOSURE CONTRACT

```text
SHARED_FACT_SOURCE=cuiqinggang/codex-private-skills
SHARED_REPO_LOCAL=C:\Users\A\Documents\Codex\codex-private-skills
SHARED_REPO_SYNC_REQUIRED=YES
```

新事实正式完成链：

```text
LOCAL RESULT
-> FORMAL REPORT / STRUCTURED FACT
-> SHARED REPOSITORY
-> EXACT STAGE
-> COMMIT
-> PUSH
-> REMOTE VERIFY
```

门禁：`LOCAL_TASK_RESULT=PASS AND SHARED_REPO_SYNC=PASS => STAGE_COMPLETE=YES`。此前 `FINAL != PASS / 99 != YES / FREEZE != YES`。

Git 禁止：`git add .`、`git reset --hard`、force push、删除其他任务成果、覆盖陌生 dirty changes。必须 fetch、明确基线、精确 stage、保护未知 dirty worktree、commit、push、remote verify。

只读解释、已有事实查询、未执行草案且不产生新工程状态时允许 `SHARED_REPO_SYNC_REQUIRED=NO`。

新版一旦产生以下事实必须同步：T_PHY、T_MACHINE_STAR、ASSUMPTION_LEDGER、target revision、V1/Vn benchmark、DELTA_T_REDUCIBLE、KEEP/ROLLBACK、multi-agent mode/资源决策、Failure Index、99/FREEZE、下一轮输入。
