---
name: high-roi-low-cost-execution-gate
description: 在编写或部署 Codex 命令包、技能包、项目方案、自动化任务前执行高收益低成本量化门禁，并在完成后核对实际收益。用户提到“值不值得做”“高收益低成本”“ROI”“投入产出”“先小试”“不要重复建设”“节省多少时间/费用”或要求创建命令包、技能包、项目方案、自动化时使用。
---

# 高收益低成本执行门禁

中文名称：高收益低成本执行门禁  
英文目录名：`high-roi-low-cost-execution-gate`  
用途：先证明值得做，再允许执行；完工后用实测数据决定保留、调整或下线。  
${REDACTED_SECRET}
调用方式：`$high-roi-low-cost-execution-gate`，或在上述触发场景中自动调用。

## 开工门禁

在实施前输出以下字段，不得用“价值很大”等定性词替代数字：

1. 中文名称、英文目录名、用途、保存位置、调用方式。
2. 真实问题、每月发生次数、单次损失时间/费用、现有替代方案。
3. 预计一次性投入时间/费用、每月预计使用次数、每月预计节省时间/费用、成功率变化。
4. 功能是否重复、证据等级、评估周期、收益/成本倍数和回收期。
5. 决策：`EXECUTE`、`PILOT_ONLY`、`DO_NOT_BUILD` 或 `BLOCKED_MISSING_DATA`。

详细口径和默认阈值见 [ROI-GATE-RULE.md](references/ROI-GATE-RULE.md)。需要确定性计算时运行：

```powershell
${REDACTED_SECRET}
```

## 决策约束

- `EXECUTE`：证据可验证，非重复建设，预计收益明显高于成本，并满足门槛。
- `PILOT_ONLY`：有潜力但证据不足，或收益只略高于成本；只做最小可测版本，禁止重型部署。
- `DO_NOT_BUILD`：收益低于成本、低频、重复建设、成功率不改善或维护负担抵消收益。
- `BLOCKED_MISSING_DATA`：必填字段缺失；不得先做后补数字。

若已有成熟技能、脚本、模板或自动化，优先复用或增量修改。不得为了满足“做一个包”的形式而复制功能。

## 完工验收

完成后使用 [POST-IMPLEMENTATION-RESULT-TEMPLATE.md](references/POST-IMPLEMENTATION-RESULT-TEMPLATE.md) 报告：

- 实际节省时间和费用；
- 实际减少的步骤、文件和规则；
- 实际成功率变化；
- 预计值与实际值偏差；
- `KEEP`、`TUNE`、`REMOVE` 或 `EXTEND_PILOT` 决策。

没有观察期数据时，必须写“尚无实测”，只可报告结构变化和预计收益，不得冒充实际节省。

## 防落灰绑定

- 开工前：先运行 Knowledge Brain / 现有技能复用检查，再执行本门禁。
- 失败复盘入口：[FAILURE-REVIEW.md](references/FAILURE-REVIEW.md)。
- 最近使用记录：[RECENT-USE-LOG.md](references/RECENT-USE-LOG.md)。
- 全局规则补丁：[AGENTS-PATCH-DRAFT.md](references/AGENTS-PATCH-DRAFT.md)。
- 每次 `EXECUTE` 或 `PILOT_ONLY` 都要定义数据采集方法和复查日期。

