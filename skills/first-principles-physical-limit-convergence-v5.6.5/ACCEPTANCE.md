# v5.6.5 时间模型简化验收

FREEZE_ID=FPLC-v5.6.5-AUTHORITY-TIME-SEMANTICS-R2

## 必须满足

1. 唯一目标仍为 T*=min(T_VALID)。
2. 时间明确区分 T_FLOW 与 T_VALID/T*。
3. 本轮可从实际状态10/20/30/40中的任一点开始，不要求补造之前状态时间。
4. 本轮起点建立一次后不重置。
5. 每个本轮实际经历的关键状态具有真实 STATE_TIME。
6. 具体单调时钟/API 不得成为状态推进硬门。
7. T_FLOW 仅由本轮实际起点到当前节点的可比较真实时间机械产生；不可比较则显示未知。
8. T_VALID 仅代表已经满足 VALID 的任务实际有效时间；局部耗时不得冒充。
9. T* 只在同一 VALID 规格、可比候选中取最小值。
10. 不同本轮起点的 T_FLOW 必须保留起点状态，不得伪装成同一区间。
11. 三行核心头仍存在，并直接显示本轮起点、当前节点、T_FLOW、T_VALID、T*。
12. 状态机、业务判断、SHA256、DSE、共同工作区规则不因本次升级改变。

## 虚拟成熟门

定向测试：13 PASS / 0 FAIL。
原 v5.6.4 的复杂时间源分层、历史五状态补齐、特定 API fallback 规则不再作为 v5.6.5 合同要求。

REALITY_CERTIFIED=NO
FINAL_VALID=NO


## R2 定点验收

13. Reality Executor 在状态40 PASS 后必须保持40并 RETURN_TO_GPT。
14. 普通 Reality 路径不得生成 STATE=100。
15. 只有 final_review=True 且 reviewer="GPT" 才允许 40→100。
16. 非 GPT reviewer 请求 final_review 必须拒绝。
17. 外部直接传 t_valid_ms 必须拒绝。
18. 有 T_VALID_START / T_VALID_END 且时间可比较时，T_VALID 由二者机械计算。
19. 缺 T_VALID_START 或 T_VALID_END 时，即使最终审核通过，T_VALID 仍为尚未产生。
20. T_FLOW 不得作为 T_VALID 的直接输入。
