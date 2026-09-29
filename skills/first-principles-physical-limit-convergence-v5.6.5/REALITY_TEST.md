# v5.6.5 Reality 最小认证

目标：只认证“简化时间模型”在真实流程中不会丢时间、不会用时间规则卡住流程、不会混淆 T_FLOW 与 T_VALID/T*。

## 当前 Reality 起点

本轮从状态30真实交接开始。
不补状态10/20历史时间。

## 必测

1. Codex 实际收件时建立本轮现实起点：FLOW_START_STATE=30、FLOW_START_TIME=真实收件时间。
2. 状态30→40 后记录真实 STATE_TIME。
3. 不要求 STATE10_TIME / STATE20_TIME。
4. 不调用、不依赖 Stopwatch.GetTimestamp 或其他特定计时 API 才允许继续。
5. 三行核心头完整。
6. T_FLOW 由本轮起点到当前节点机械计算。
7. 本轮若尚未形成最终 VALID 任务结果，T_VALID=尚未产生。
8. 局部测试耗时不得冒充 T_VALID。
9. 状态机、业务判断、SHA256证据不变。
10. Reality 阶段不得现场修改 Freeze/Runtime 来取得 PASS。

## 返回

完成真实检查后停在状态40，返回 GPT 审核：

RETURN_TO_GPT=YES
REALITY_CERTIFIED 由 GPT 决定
FINAL_VALID 由 GPT 决定

不得自行宣布状态100 / DONE。


## R2 定点 Reality 检查

11. 状态40业务/证据 PASS 后，Reality Executor 必须停在40并 RETURN_TO_GPT=YES。
12. Reality Executor 不得自行生成 STATE=100 / FINAL_VALID / REALITY_CERTIFIED / DONE。
13. GPT Final Reviewer 是唯一允许签入100的角色。
14. 最终数值 T_VALID 必须有独立 T_VALID_START / T_VALID_END。
15. 未记录独立 T_VALID 边界时，必须输出 T_VALID=尚未产生；禁止用 T_FLOW 替代。
