# TASK B EXECUTION PACKAGE

TASK_ID=BLIND-B-OWID-ENERGY-20260910
CONTRACT_VERSION=4
ROLE=EXECUTION_SIDE
ORACLE_ACCESS=DENIED
FINAL_PRODUCT_ACCESS=DENIED

## 目标

从冻结的 2026-09-10 source snapshots / ETL source / schema contract 构建 OWID Energy 发布候选，并通过 Reviewer 的机械 reconciliation。执行侧不知道固定版本最终表内容。

## 可见输入类别

- Energy Institute energy statistics snapshot；
- Ember global/europe electricity snapshots；
- U.S. EIA international energy snapshot；
- historical energy/electricity reconstructions；
- OWID regions/ISO mapping；
- OWID population；
- Maddison GDP；
- 2026-09-10 对应 ETL 代码与非最终-output schema/processing contract。

## 必须处理

ingestion → schema normalization → country/region normalization → year/date handling → unit conversion → missing/malformed → duplicate-key → source overlap/priority → aggregation/stitching → population/GDP joins → per-capita/share/change derivation → final wide-table candidate → reconciliation.

主键候选必须显式验证，不得静默保留 duplicate country-year。

## 盲区

禁止访问：
- 2026-09-10 fixed owid_energy.csv/parquet/feather；
- catalog 中可直接泄露最终成品的 advanced download；
- final standard answer table；
- Reviewer canonical cardinality/sentinel/hash/reconciliation；
- 另一 TASK 的任何 state。

允许读取的 public/source host 必须使用 allowlist；final product host/path 由 harness deny。

## Reality / Delta

Reviewer 只返回 PASS / FAIL / DELTA 类型，不返回正确值。
若某 source branch 验证失败，只返修该 branch；全局 schema/contract 故障才触发系统级规则。
stale snapshot、unit conflict、duplicate/overlap、missing/malformed 等必须由实际证据触发，不预写正确修法。

## 初始 NEXT_NODE

B01=FREEZE_SOURCE_MANIFEST_AND_PROVENANCE
