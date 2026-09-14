# 已确认失败经验

- Historical fixed baseline can misclassify candidates：同一 unchanged baseline 曾出现 30.0504、33.20215、35.60995 ms；旧 32.55975 ms + 单批 2% 门限无法分离时间漂移。
- Baseline drift exceeded old decision threshold：同期 A 自身可发生超过毫秒级候选阈值的趋势，必须 interleave、pair、bracket 并单独裁决 drift。
- `p>0.05` does not prove equivalence：pilot order effect 的幅度超过当时 MDE，即使 permutation p=0.083 也只能 INCONCLUSIVE。
- Post-hoc rule changes cannot rehabilitate an old batch：看到结果后修改规则只能产生新协议和新 runner SHA；旧批角色不变。
- MDE cannot be trusted before null Type-I calibration：必须先验证生产 KEEP 的错误率，再生成 FINAL_MDE。
- 11.185% null false-positive rate is invalid：旧 2.4 ms MDE 管线在 gain=0 的 false positive 为 11.185%，已由统计审计取代。
- Shared-A bracket observations are clustered, not IID：共享 A_before/A_after 的 comparisons 必须整体 cluster；不得跨 block 拼接后独立 bootstrap。
- Raw history response must be archived：解析 bool 不足以复核 completed/status/prompt/output；必须留无损正文与 SHA。
- Statistical implementation changes require a new runner SHA：任何 CI/null/MDE/order/drift/bracket 实质改动都必须新 SHA、新 selftest、新 A/A。
- Superseded experiments remain evidence but cannot enter authoritative decisions：旧原始数据、慢样本、失败均保留，但标记 PILOT/PREAUDIT/SUPERSEDED 后不得参与 FINAL_MDE、KEEP 或 ROLLBACK。
- Null calibration PASS does not imply A/A PASS：最终新 runner 的 null false KEEP 与双向 rejection 均校准通过，但完全相同实现仍产生 formal effect=3.24545 ms、95% CI=[0.579475,5.953475] 且超过 noise floor；必须 `AA_CALIBRATION=FAIL` 并锁定候选。
