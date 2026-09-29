# v5.6.5 虚拟成熟记录

VERSION=v5.6.5
FREEZE_ID=FPLC-v5.6.5-AUTHORITY-TIME-SEMANTICS-R2
VIRTUAL_MATURE=PASS
REALITY_CERTIFIED=NO
FINAL_VALID=NO

## 根因修正

此前时间问题反复复杂化的根因，是把“如何取得时间”逐渐变成了流程本身的目的。

v5.6.5 恢复原始目标：
时间是测量和优化整体效率的工具，不是为了满足时间规则而运行。

因此删除以下强约束：
- 必须从状态10建立完整五状态时间链；
- 为缺失历史状态补时间；
- 某个特定单调计时 API 是 Reality 启动条件；
- 因高精度 API 不可用而停止业务状态；
- 为时间源建立多层协议分支。

保留的核心只有：
- 本轮实际起点；
- 实际关键节点时间；
- 本轮流程耗时 T_FLOW；
- 被优化任务的 T_VALID；
- 最短有效时间 T*。

## 定向测试

TEST_RESULTS=13 PASS / 0 FAIL

PASS:
1. start_at_30
2. no_historical_time_required
3. flow_origin_frozen
4. tick_not_gate
5. auto_real_time
6. transitions_unchanged
7. dispatch_unchanged
8. three_line_header
9. tvalid_only_on_final
10. final_tvalid
11. flow_and_tvalid_separate
12. clock_regression_fail_closed
13. timezone_required

## 结论

时间模型已经回到单中心：
VALID 前提下追求整体极限效率。

本次没有重做引擎，也没有扩大架构。允许冻结并进入 Reality 交接。


## R2 根因补充：协议语义必须唯一

DSE Reality 实际回报显示：
- 执行器把全部案例 PASS 后的最终状态写成100；
- 把包含资料定位/更正/恢复的整轮耗时标成 T_VALID。

核对实际合同后确认：
- DSE 命令写了“不得自行宣布 FINAL_VALID / DONE”，但没有把 STATE=100 同样机械封闭；
- v5.6.5 Runtime 原来又确实把 state40 PASS 直接转为100；
- v5.6.5 虽定义 T_FLOW / T_VALID，但 Runtime 原来允许最终阶段直接接收外部 t_valid_ms。

因此优先归因为：
FINALIZATION_AUTHORITY_CONTRACT_AMBIGUITY
TIME_SEMANTICS_CONTRACT_AMBIGUITY

而不是先归因为 EXECUTOR_NONCOMPLIANCE。

## R2 最小修复

只修改：
- Reality 40 PASS 默认留40并 RETURN_TO_GPT；
- GPT Final Reviewer 显式签100；
- T_VALID 改为 T_VALID_START / T_VALID_END 机械推导；
- 禁止外部 t_valid_ms 直接写入。

不修改：
- DSE 决策正文；
- 其他状态转移；
- SHA256 证据；
- 三行核心显示；
- T_FLOW 简化模型。

## R2 定向行为验证

TEST_RESULTS=6 PASS / 0 FAIL

VIRTUAL_MATURE=PASS
REALITY_CERTIFIED=NO
FINAL_VALID=NO
