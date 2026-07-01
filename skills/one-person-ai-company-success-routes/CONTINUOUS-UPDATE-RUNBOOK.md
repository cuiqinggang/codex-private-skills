# Continuous Update Runbook

## 如何执行一次轻量更新

1. 打开 `UPDATE-CADENCE.md` 的轻量关键词。
2. 搜索公开网页、GitHub、官方 docs、社区分享、失败复盘。
3. 只记录公开来源，不登录、不保存 token。
4. 新候选写入 `WATCHLIST.md`。
5. 重大变化同步 `ROUTE-MATRIX.md`。
6. 写 `reports\periodic-updates\YYYYMMDD-light-update.md`。
7. 更新 `CHANGELOG.md`。

## 如何执行一次周复盘

1. 汇总过去 7 天 light update。
2. 去重：同一项目只保留一条 canonical route。
3. 检查 license、成熟度、更新状态、风险。
4. 对高价值路线补 case study 或 route evaluation。
5. 更新 `WATCHLIST.md`、`ROUTE-MATRIX.md`、`CASES.md`、`ABSORPTION-RULES.md`。
6. 写 weekly review。

## 如何执行一次月度复盘

1. 重评估所有 ABSORB/REPLAY/WATCH 路线。
2. 标记 supersede、upgrade、deprecated。
3. 输出 Top 10 路线、Top 5 Dashboard 机制、Top 5 暂停路线。
4. 判断是否新建技能包或更新主技能包索引。
5. 写 monthly route review。

## 如何判断是否需要深度 case study

需要满足至少两个条件：

- 与一人 AI 公司高度相关。
- 有可验证开源代码、官方 docs 或真实运营证据。
- 能映射到现有体系。
- 有可复用机制，而不是单纯营销。
- mock/read-only/demo 可验证。

## 如何把新路线合并进技能包

1. 先写 intake。
2. 再判断 ABSORB/REPLAY/WATCH/REJECT。
3. 需要深入则写 case study。
4. 把机制写入 `ROUTE-MATRIX.md`、`CASES.md`、`SOURCE-OF-TRUTH-MAP.md`。
5. 如改变治理或 replay 规则，更新 `ABSORPTION-RULES.md`、`REPLAY-METHOD.md`、`GOVERNANCE.md`。
6. 更新 `CHANGELOG.md`。

## 如何同步到 AICompany Dashboard

仅同步信息架构和字段建议：route card、case card、approval gate、run history、watchlist 状态、credential status。不要同步真实 key、生产配置或真实连接器。
