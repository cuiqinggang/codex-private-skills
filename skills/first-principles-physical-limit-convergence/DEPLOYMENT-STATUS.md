# v4.1.0 Deployment Status

```text
METHOD_VERSION=4.1.0
MATURITY_STATUS=DISCUSSION_REFINEMENT_ACTIVE
LOCAL_DEPLOYMENT=DEFERRED
CODEX_DEPLOY_COMMAND=PUBLISH_FORBIDDEN
```

原因：当前正在通过讨论把“一虚一实”本身做成熟。用户明确要求在方法冻结前不要反复本地部署。

本分支从 v4.0.0 继承的旧 deploy 文档/runner 只作为历史材料，不得用于 v4.1 当前部署。

解除门禁必须由用户明确认为当前 v4.x 已暂时成熟，并要求进入本地部署。

在此之前：
- 可以继续更新远端 v4.1 方法文件；
- 可以继续更新 Foundation；
- 可以继续做纯虚拟合同检查；
- 不发布 Codex 本地部署命令；
- 不启动 Bonsai GPU v4.1 verifier 修复现实工作，除非用户另行切回该任务。
