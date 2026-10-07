# 三重超大型盲式任务选择与难度审核

CONTRACT_VERSION=4
METHOD=ENGINE22 / BRAIN19 / TEMPLATE17
DECISION=ACCEPT_A_B_C_FOR_BLIND_EXECUTION
ORACLE_CONTENT_PRESENT=NO

## TASK A — BLIND-A-CARGO-INCIDENT-20221103

来源：Rust/Cargo 2022-11-03 真实集成与 nightly 发布事故。
为什么成熟：大型 Cargo/Rust 代码库；真实 merge/sync/CI/perf/revert/release 证据链；事故有完整时间线，且有机械 build/test/CI/release 验收。
为什么不是玩具：跨 Cargo feature resolver、Rust submodule sync、CI/perf bot、release automation、nightly release；真实过程中存在错误初判、调查、CI timeout、回滚与手工发布干预。
执行侧可见：buggy integration 状态、当时失败日志、当时已有代码/测试、按时间释放的新证据。
Reviewer 独占：事后 postmortem、最终根因、最终处置答案及完整时间线。

自然控制节点（不等于预写修复）：
A01 接收 sync 后异常；A02 解析 perf/build failure；A03 独立复现；A04 rustc/native/Cargo 归因分支；A05 Cargo 子模块范围收敛；A06 dependency-graph 最小化；A07 feature-resolver 路径调查；A08 optional dependency 分支；A09 host/proc-macro/build dependency 分支；A10 compare recent Cargo changes；A11 candidate rollback；A12 candidate direct patch；A13 release-risk compare；A14 CI request；A15 CI observation；A16 timeout/stale-state 判断；A17 release deadline判断；A18 nightly automation control；A19 retry/requeue；A20 merge/revert verification；A21 reproducer regression test；A22 ecosystem smoke check；A23 release candidate verify；A24 manual release path；A25 post-release verify；A26 freeze/final handoff。
NATURAL_NODES=26。

并行波次可覆盖：复现/代码调查/CI日志、依赖图/feature resolver、release risk/rollback、reproducer/ecosystem smoke、CI/release verifier。
难度判定：PASS。

## TASK B — BLIND-B-OWID-ENERGY-20260910

来源：Our World in Data Energy 固定发布版 2026-09-10。
为什么成熟：公开生产数据产品；14 类源/来源集合；固定 release；ETL 代码与 catalog 元数据公开；最终产品可机械比对。
复杂性：Energy Institute、Ember、EIA、历史重建、regions、population、GDP 等多源；country/region canonicalization；units；source stitching；missing/overlap；derived metrics；最终 wide table。
执行侧可见：源快照/许可的 metadata、ETL source tree、schema contract、源级异常反馈。
Reviewer 独占：固定版本最终 table/bytes、最终 reconciliation、canonical cardinality/sentinel 集。

自然控制节点：
B01 source manifest；B02 snapshot pin；B03 schema ingest EI；B04 schema ingest Ember global；B05 Ember Europe；B06 EIA；B07 historical reconstructions；B08 regions；B09 population；B10 GDP；B11 country normalization；B12 ISO mapping；B13 year/date normalization；B14 unit conversion；B15 duplicate-key detection；B16 malformed/missing handling；B17 source overlap arbitration；B18 regional aggregation；B19 energy supply stitching；B20 electricity stitching；B21 fossil production stitching；B22 derived share；B23 per-capita；B24 annual change；B25 schema mapping；B26 cross-source reconciliation；B27 final table build；B28 mechanical validation；B29 rejected-delta repair loop；B30 freeze/final publish candidate。
NATURAL_NODES=30。

并行波次：source ingestion；normalization；energy/electricity/fossil branches；derived metrics；reconciliation/verifier。
难度判定：PASS。

## TASK C — BLIND-C-WEBARENA-VERIFIED-552

来源：ServiceNow WebArena-Verified v1.2.3，Hard subset 官方 task 552；GitLab + Reddit 两站。
为什么成熟：812-task verified benchmark 的 hard subset；任务、reference/evaluator 经审计；Network trace + AgentResponse deterministic scoring；环境可自托管并可 reset。
为什么不是简单网页：跨论坛信息读取与 GitLab Web IDE 写入；必须形成结构化文件并产生真实 commit；浏览器行为另由 API/HAR evaluator 机械核验；可纳入 session、env-control、exactly-once 和 state recovery。

自然控制节点：
C01 sandbox health；C02 env init；C03 auth/session；C04 task load；C05 Reddit forum定位；C06 sort/order确认；C07 recent-post capture branch1；C08 branch2；C09 branch3；C10 branch4；C11 branch5；C12 URL canonicalization；C13 duplicate/order verify；C14 GitLab repo定位；C15 default branch读取；C16 Web IDE open；C17 directory path；C18 file compose；C19 local JSON parse；C20 pre-submit state read；C21 commit submit；C22 ambiguous-ack/read-after-write；C23 exactly-once guard；C24 HAR capture；C25 response artifact；C26 offline evaluator；C27 evaluator delta；C28 repair/reverify；C29 final Git tree verify；C30 freeze/final handoff。
NATURAL_NODES=30。

并行波次：forum read/canonicalization；GitLab preflight/file preparation；HAR/state capture；evaluator/local validation；recovery/idempotency.
难度判定：PASS。

## 盲测特别说明

失败/Repair 的数量不由本文件预写。Reviewer 只冻结历史信息顺序、真实环境故障类或 deterministic mutation，并只返回 PASS/FAIL/DELTA；执行侧必须自己推导原因和下一动作。这样满足“高压覆盖”而不退化成背故障脚本。
