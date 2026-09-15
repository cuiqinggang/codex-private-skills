# FAST PATH（成熟最短路径）

1. 定义 `TASK_COMPLETED（任务完成）`。
2. 测量 `CURRENT（当前真实状态）` 的 `T_END_TO_END`。
3. 查 `EXTERNAL FRONTIER（外部成熟前沿）`。
4. 推导 `FIRST-PRINCIPLES PHYSICAL LIMIT（第一性原理物理极限）` 所要求的最低必要路径。
5. 找最大的现实时间损失。
6. `De-Armoring（去重甲）`：删除、合并、后移、并行或替换非必要路径。
7. 执行真实测试，并检查 `TASK_COMPLETED == TRUE`。
8. 更快则 `KEEP（保留）`；否则 `ROLLBACK（回滚）`。
9. 把结果设为 `NEW CURRENT（新的当前状态）`。
10. 重新做四列分析。
11. 需要节点才自然产生节点。
12. 没有明显现实大块时，准备 `99 / FREEZE`。
13. 写入正式阶段报告与必要结构化事实。
14. 将正式事实同步到 `cuiqinggang/codex-private-skills`，精确提交、推送，并验证远端。
15. 只有 `SHARED_REPO_SYNC=PASS`、`LOCAL_HEAD == ORIGIN_HEAD` 且 `WORKTREE_CLEAN=YES` 时，`99=YES / FREEZE=YES` 才正式生效。

结构由四列分析自然产生：能整体完成就不建节点；只有真实因果依赖才产生节点。不要预设 PLAN、STAGE、NODE 或 SYSTEM 层级。

产生可复用新事实时，自动化模式附加闭环：

`GPT 分析 → Codex 执行 → 本机证据 → 正式结果包 → GitHub 共同事实源 → 远端验证 → GPT 重新读取 → 下一轮`

只读回答、纯解释、未执行方案草拟、读取已有事实或不改变 CURRENT 的查询不强制创建 Git commit。

需要网页通信时，按 [EXECUTION BRIDGE（执行桥梁）](EXECUTION-BRIDGE.md) 调用 `playwright-native-ai-browser`。每轮只交付一个明确高价值动作。
