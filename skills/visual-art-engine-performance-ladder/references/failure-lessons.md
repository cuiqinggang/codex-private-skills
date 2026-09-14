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
- Same algorithm is not the same execution path：旧 A/A 把 `measured-A/B` 写进 `SaveImage.filename_prefix`、`/view` 输出身份和计时内 raw/evidence 路径；服务端 execution effect 为 0，而客户端控制路径主导假差异。arm label 必须纯 metadata，并以 normalized workflow SHA 相等及 timed/workflow/HTTP leak=0 自测阻断复犯。
- Root-cause repair and overall A/A are separate：label-blind 后 formal CI 从全正变为跨 0、effect 落入 noise floor，足以确认标签污染修复；但 order-effect equivalence CI 仍过宽，所以总体只能 `INCONCLUSIVE`，候选锁不能解除。
- Windows deepest evidence path must be preflighted：长 Stage root 加逐 run 子目录可在目录已创建后仍于深层文件 open 报 `FileNotFoundError`。权威测试前必须真实创建最深路径；必要时使用短、中性、label-blind evidence root。
- Earlier parallelism can be slower：在 SaveImage `executed` 后立即并发 history 与 `/view`/本地 read，会争用尚未完成发布的服务端和文件路径；本轮 history 拉长到 12–30 ms、`/view` 拉长到 20–27 ms。并行化必须由 segment evidence 证明，不能凭结构直觉。
- Relative confirmation is not absolute 99：R6 两批 paired effect 的 CI 都全正，但 candidate pooled P50=`41.5258 ms`，慢于历史 `32.55975 ms`，且 A/A drift gate FAIL。因此“候选相对更快”不能改写成“当前绝对极限”。
- Pick neither a smoke nor the best batch：8-run smoke 曾得到 `32.9893 ms`，两个 confirmation 却为 `44.33395/39.18285 ms`。最终报告必须合并独立 confirmation 分布，禁止挑最快 smoke、min 或单批 median。
