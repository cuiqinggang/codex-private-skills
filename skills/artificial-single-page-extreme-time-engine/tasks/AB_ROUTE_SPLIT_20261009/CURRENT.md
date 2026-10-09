# A/B路线分叉任务｜唯一当前状态指针

TASK_ID=AB_ROUTE_SPLIT_20261009
STATUS=IN_PROGRESS
CONTRACT_VERSION=2
FREEZE_VERSION=2
FREEZE_ID=AB-ROUTES-F002
METHOD_A=A28/A25/A18
METHOD_B=B30/B27/B20
METHOD_REF=315cdc78054047c75b1e177fdebc4c008fac3ab6
TASK_STATE_REF=4872de172552429f4daea4ab5831acf3013ffaa3
CONTRACT_PATH=skills/artificial-single-page-extreme-time-engine/tasks/AB_ROUTE_SPLIT_20261009/CURRENT_TASK_CONSTRAINTS_V2.md
FREEZE_PATH=skills/artificial-single-page-extreme-time-engine/tasks/AB_ROUTE_SPLIT_20261009/freezes/CURRENT_TASK_FREEZE_V2.md
NEXT=按冻结F002继续同一成果A/B完整有效时间验证；未授权新Reality。

## 读取门
1. 从GitHub网络权威库`cuiqinggang/codex-private-skills`读取上述真实`TASK_STATE_REF`中的合同与冻结文件；校验TASK_ID、版本与F002一致。方法在`METHOD_REF`固定提交读取，避免之后版本推进改写本次历史方法。
2. 初次/未来接续如用户允许升级方法，先通过`routes/A/ROUTE.md`或`routes/B/ROUTE.md`取得当时的当前方法提交并根据任务版本演进；未收到升级指令不能用`main`的新方法静默篡改旧方法证据。
3. 本文件是只属于此TASK_ID的可变入口。每次新的合法Freeze必须先保存不可变版本文件并确认GitHub提交，再更新本指针；更新冲突拒绝覆盖。冻结节点后再交接页面。
