# 《当前任务目标与正反约束 第4版》

任务ID：METHOD-SYSTEM-BLIND-TRIPLE-STRESS-20261008
合同版本：4
状态：CURRENT
升级来源：第3版
任务类型：三重超大型盲式生产同构虚拟成熟

## 1. 最终目标

在不知道历史最终答案、不能访问最终 fix / diff / 标准答案 / 后来总结的根因的条件下，同时运行三个外部成熟世界中的大型任务，验证当前正式方法是否仍可从 TASK_ACCEPTED 经未知分析、错误候选、现实反馈、Repair / Reverify、Freeze、True New Chat、共享资源仲裁稳定收敛到各自 FINAL_VALID。

本合同升级只提高本次任务的验收强度，不自动升级方法。

## 2. 固定方法起点

- ENGINE_VERSION=22
- BRAIN_VERSION=19
- NEW_PAGE_TEMPLATE_VERSION=17
- METHOD_REF=6fc5f3203b2eb055bb68b83b17796d36ca2ac274
- PARENT_FREEZE=freezes/CURRENT_TASK_FREEZE_V16.md
- PRIOR_DUAL_TASK_REPLAY=PASS
- KNOWN_PATH_CONTROL_STRESS=PASS
- STRONG_BLIND_VIRTUAL_MATURITY=NOT_YET_CERTIFIED

只有出现新的结构性方法故障，才按真正责任层做一次最小升级。

## 3. 三个外部任务

### TASK A
TASK_A_ID=BLIND-A-CARGO-INCIDENT-20221103
领域：大型软件工程 / 故障修复 / 集成与发布。
来源：Rust/Cargo 真实历史集成回归事故。
执行侧只接收事故当时可获得的代码、失败日志和按时间释放的证据；不得读取事后 postmortem、最终修复/回滚答案或后来总结的根因。

### TASK B
TASK_B_ID=BLIND-B-OWID-ENERGY-20260910
领域：大型数据流水线 / 多源拼接 / 对账 / 数据产品。
来源：Our World in Data Energy 2026-09-10 固定发布版。
执行侧可读取固定源快照、ETL 代码/规范与当时可得元数据；不得读取该版本最终成品表、最终标准答案表或 Reviewer 的 reconciliation 结果。

### TASK C
TASK_C_ID=BLIND-C-WEBARENA-VERIFIED-552
领域：大型多系统自动化 / Browser + API + File + State。
来源：WebArena-Verified v1.2.3 Hard 官方多站点 Task 552，GitLab + Reddit。
执行侧只接收 agent-visible task intent、sandbox 入口与允许的运行接口；不得读取原始 dataset 的 eval 字段、reference answer、Reviewer oracle 或公开镜像中的答案。

## 4. 双层物理隔离

### EXECUTION SIDE
只允许：
- 当前 NEXT_PAGE_PROMPT；
- ENGINE / BRAIN / TEMPLATE 的冻结版本；
- 本 TASK 的执行包；
- 当前 TASK Freeze；
- Reviewer 按 CHRONOLOGICAL_INFORMATION_GATE 新释放的证据；
- 明确允许的本地 sandbox / source snapshot。

禁止：
- 全仓库自由搜索；
- 公开互联网搜索历史答案；
- 读取 reviewer-only capability；
- 读取最终结果目录；
- 跨 TASK 路径；
- 读取未来时间切片。

### ORACLE / REVIEWER SIDE
Reviewer 可以持有最终答案，但只能返回：
PASS / FAIL / DELTA / 缺少证据 / 结果不一致。
不得向执行侧返回正确根因、下一步修法、最终 diff、标准答案表或历史最佳路径。

Reviewer oracle 以未挂载到 Git tree 的 capability blob 保存；其对象 SHA 不得进入任何 execution package、task-state commit、Freeze、NEXT_PAGE_PROMPT 或 executor-visible 日志。

## 5. CHRONOLOGICAL_INFORMATION_GATE

每个 TASK 具有独立时间切片。
执行侧在当前切片只能用当前时点本来可获得的信息。
未来日志、后来的 root cause、后来新增测试、最终输出与事后总结不得提前释放。

WALL_CLOCK 可以压缩；LOGICAL_DIFFICULTY 不得压缩。
不得跳过：决策节点、错误判断、Reality feedback、Repair、FAIL、回虚、Reverify、Freeze、Merge、handoff、资源冲突、页面生命周期。

## 6. 禁止故障脚本表演

允许预先冻结：
- 历史证据；
- 信息释放顺序；
- sandbox 环境条件；
- 可重复 deterministic mutation；
- 验收器。

禁止预先告诉执行侧：
- 第几步必坏；
- 正确 Repair；
- 最终根因；
- 下一正确节点。

若执行侧第一轮从当前证据真正推导正确，可以 PASS；若连续多轮错，就真实多轮返修。不得为了计数人工制造固定次数失败，也不得因 Reviewer 知道答案而跳到正确 Repair。

## 7. 每任务最低结构复杂度

- NATURAL_NODES >= 20；
- >=5 并行波次或可并行分支；
- >=4 CEO 换页 / True New Chat；
- 重复覆盖 FAIL / Delta、Repair / Reverify、Freeze、handoff、恢复；
- >=3 shared-resource contention；
- >=2 false lead 或错误方向；
- stale state、工具/环境故障、中断恢复、exactly-once / duplicate protection、表面成功但 verifier FAIL、最终候选被拒后返修均必须由真实历史/冻结 mutation/实际运行自然触发并验证。
- 上述失败次数不是“为了凑数预写故障脚本”的许可；冲突时以禁止答案泄露与禁止人工表演为高优先级。

## 8. 三任务并行隔离

A/B/C 各自拥有独立 TASK_ID、CONTRACT_VERSION、FREEZE_VERSION、ACTIVE_CEO、STATE_REF、证据路径、页面所有权。

必须验证：
- A FAIL 时 B/C 继续；
- B True New Chat 时 A/C 继续；
- C Repair 时 A/B 不回滚；
- 返回/Freeze/Merge 顺序持续交错；
- 一个 TASK 完成只回收自己的资源；
- 最后一个 TASK 结束后才允许系统级共享资源清理。

## 9. SYSTEM_RESOURCE_LEASE

至少覆盖：
- GitHub main writer；
- persistent browser；
- Windows executor；
- shared filesystem；
- download/upload staging；
- global cache/service；
- compute slot（任务需要时）。

冲突只串行冲突节点；无冲突节点继续并行。
禁止 double writer、误释放他人 lease、任务完成后错误关闭其他任务资源。

## 10. HANDOFF_MECHANICAL_GATE

每次 CEO 换页的 NEXT_PAGE_PROMPT 必须机械检查至少 17 项：
1 三行信封；2 TASK_ID；3 CONTRACT_VERSION；4 FREEZE_VERSION；5 ENGINE_VERSION；6 BRAIN_VERSION；7 TEMPLATE_VERSION；8 METHOD_REF 可解析；9 STATE_REF 可解析；10 TASK_CONSTRAINTS_PATH 存在；11 FREEZE_PATH 存在；12 Freeze tag/path 版本一致；13 NEXT_NODE 存在且属于同 TASK；14 无另一 TASK 路径；15 无 stale Freeze；16 无大量旧聊天噪声；17 新 CEO 仅靠 prompt + 权威文件可恢复。

任一失败：
HANDOFF=FAIL → Freeze failure → 责任判断 → Repair → 重生 handoff → True New Chat → 再验证。

新 CEO=NO_PREVIOUS_CHAT_MEMORY。

## 11. 主动交叉污染攻击

每个 TASK 至少一次把另一个 TASK 的 FREEZE_PATH / STATE_REF / PAGE_ID / NODE_FREEZE / NEXT_PAGE_PROMPT 作为候选输入。
正确结果必须 REJECT，且不得 Merge、版本递增、关闭页面、Repair 或更新状态。

## 12. Fail Fast

若出现新的结构性方法故障：
Stop all three progression → Freeze first confirmed fault → Root Cause → 只升级真正责任版本 → 最小 Repair → A/B/C 全部从各自 TASK_ACCEPTED 重跑。

责任优先级：
- 判断/三任务调度/资源仲裁 → BRAIN；
- 页面/handoff/NEXT_PAGE_PROMPT/生命周期 → TEMPLATE；
- 只有总纲职责变化才 → ENGINE。

## 13. DONE_WHEN

仅当同时满足：
TASK_A_FINAL_VALID=YES
TASK_B_FINAL_VALID=YES
TASK_C_FINAL_VALID=YES
ORACLE_LEAK=NO
KNOWN_ANSWER_SHORTCUT=NO
LOGICAL_DIFFICULTY_COMPRESSION=NO
HANDOFF_MECHANICAL_GATE=PASS
NEW_CEO_MEMORY_DEPENDENCY=NO
TASK_STATE_POLLUTION=NO
FREEZE_CROSS_LINE=NO
WRONG_MERGE=NO
DUPLICATE_EXECUTION=NO
DOUBLE_WRITER=NO
WRONG_PAGE_CLOSE=NO
DUPLICATE_PERSISTENT_BROWSER=NO
SHARED_RESOURCE_CONTROL_LOST=NO
NEW_METHOD_FAULT=NO

才允许：
VIRTUAL_MATURE=YES
BLIND_STRESS_MATURE=YES
REALITY_CERTIFIED=NO
