# TASK A EXECUTION PACKAGE

TASK_ID=BLIND-A-CARGO-INCIDENT-20221103
CONTRACT_VERSION=4
ROLE=EXECUTION_SIDE
ORACLE_ACCESS=DENIED
PUBLIC_ANSWER_SEARCH=DENIED

## 目标

处理一次 Rust/Cargo 集成路径中的真实 build regression，并在 nightly 发布风险窗口内得到机械可验证的安全结果。你不知道最终历史答案。

## 初始可见信息 T0

时间切片：2022-11-03 10:26 UTC。
- rust-lang/rust 刚合入一次 Cargo 同步，相关集成/性能机器人报告 build failure。
- 失败表现不是单一 benchmark 数字退化，而是部分真实 package 无法 compile。
- 可检查当前 Rust/Cargo 代码、该 sync 之前已存在的测试、bot 在当时已经公开的 failure 输出。
- 允许并行调查 rustc、Cargo、native dependency/config、dependency graph、recent synced changes。
- 不得读取事后 postmortem、后来发布的 root-cause 总结、最终 revert/fix diff 或后来才产生的 CI 日志。

## 执行原则

1. 先复现并建立最小失败图，不猜答案。
2. 每个候选都必须给可证伪条件。
3. Reviewer 只会返回 PASS / FAIL / DELTA / 缺少证据 / 结果不一致。
4. 若需要未来证据，申请 NEXT_EVIDENCE；不得自行搜索历史答案。
5. release deadline 是真实约束；“代码看起来修了”不等于 FINAL_VALID。
6. 所有 merge/retry 必须 exactly-once；CI 状态必须重新读取，不用 stale green/red。
7. 新 CEO 只能读本文件、当前 Freeze、明确释放证据与冻结方法文件。

## 工具/信息边界

允许：
- exact historical source snapshot；
- local build/test/reproducer；
- Reviewer 明确释放的 evidence slice；
- 当前 task 的 state/freeze。

禁止：
- GitHub/global web 搜索 incident title/PR/issue；
- 读取其他 TASK；
- 读取 reviewer capability；
- 用当前聊天中曾见过的历史答案。

## 初始 NEXT_NODE

A01=TRIAGE_BUILD_REGRESSION_FROM_T0
