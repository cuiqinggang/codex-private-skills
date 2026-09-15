# FAST PATH（成熟最短路径）

正常任务默认只读本文件；方法定义来自 `mature-replication-four-column` 的第一性原理四列法 V4.0。

## WHAT TO DO FIRST（首先做什么）

1. 固定任务合同、成功条件、输入输出、质量底线与 `T_START/T_END`。
2. 固定 `CURRENT（当前真实状态）` 与可恢复实现。
3. 把非任务必需动作移到 `RESULT_READY（结果就绪）` 后。
4. 依次填写 `EXTERNAL FRONTIER（外部成熟前沿）`、`FIRST-PRINCIPLES PHYSICAL TIME（第一性原理物理时间）` 与 `ITERATIVE CONVERGENCE（迭代收敛）`。
5. 建立 REQUEST（请求）/ QUEUE（排队）/ EXECUTE（执行）/ RESULT（结果）宏观时间账。
6. 只细分最大的现实可消除时间块，用物理因果链证明删除它会缩短关键路径。
7. 一次只改一个主要变量；短周期真实运行。
8. 绝对结果明显更快则 `KEEP（保留）`，否则 `ROLLBACK（回滚）`。
9. 以新 CURRENT 重做四列分析并循环。
10. 接近 `REALITY FLOOR（当前现实下界）` 后，最后才做 `CERTIFICATION（最终认证）` 与 99 冻结。

## 候选卡

```text
CURRENT_BEST_MS=
TARGET_BLOCK=
CURRENT_BLOCK_MS=
PHYSICAL_REQUIRED_MS=
REMOVABLE_MS=
OVERLAPPABLE_MS=
EXPECTED_GAIN_MS=
EXPECTED_NEW_TOTAL_MS=
IMPLEMENTATION_COST=
```

预计收益小于 1 ms 时暂不做；优先攻击至少 2 ms 的可行低风险大块。该阈值是性能候选筛选，不是 ROI 门禁。

## 最低结果验证

- 匹配自己提交的 prompt identity（任务身份）；
- successful completion（成功完成）；
- 获得最终 PNG bytes（PNG 字节）；
- PNG 结构有效、256×256、完整 decode（解码）；
- 必要的结果身份确认。

同一语义不得重复 decode、hash、history fetch 或文件 reopen。

## 短周期裁决

```text
PREVIOUS_BEST_MS=
NEW_P50_MS=
NEW_P95_MS=
ABSOLUTE_GAIN_MS=
IMPROVEMENT_PERCENT=
VALID=5/5
KEEP_OR_ROLLBACK=
```

未变快时不要扩大统计；检查目标路径是否仍存在、是否新增同步点、重复 encode/copy 或等待。

## WHAT NOT TO DO（不要做什么）

- 不创造“撕裂法”或另一套四列法。
- 不以 measurement engineering（测量工程）代替 performance engineering（性能工程）。
- 不让 evidence（证据）、Git、日志或知识同步进入计时段。
- 不把冷启动负担误当稳态关键路径。
- 不同时修改两个主要变量。
- 不为卡死检测给毫秒路径添加 watchdog 或 polling。
- 不默认读完整历史；异常才查 FAILURE INDEX。
- 不扫描 H/K；K 仅在用户明确批准具体备份时使用。

## 完成条件

固定任务保持，最低验证通过，剩余时间账可解释，最大可行低风险可消除块小于 0.5–1 ms，并通过最终认证时，才能冻结 `P0_99=YES` 与 `P0_FREEZE=YES`。
