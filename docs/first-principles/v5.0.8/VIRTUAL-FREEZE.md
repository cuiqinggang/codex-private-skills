# 整体闭环极限短时间引擎 v5.0.8｜控制边界显性时间连续性虚拟冻结

FREEZE_ID=ESTE-v5.0.8-CONTROL-BOUNDARY-TIME-VIRTUAL-FREEZE-R1

## 保持不变
- 顶层仍只有：虚 -> 实。
- v5.0.5 原状态机不变。
- 共同私库直读主路径不变。
- v5.0.7 数值时间锚继续有效。

## v5.0.8 修正
时间连续性不再只由内部账本证明。

任何会改变以下任一事项的节点，都属于 CONTROL_BOUNDARY：
- 关键方案定案；
- 虚拟成熟收口；
- Freeze 提交；
- 控制权 GPT -> Codex；
- 控制权 Codex -> GPT；
- PASS / FAIL / BLOCKED 结果；
- FAIL 返回虚；
- FINAL_VALID。

每个 CONTROL_BOUNDARY 必须显式显示同一 Timeline 的数值时间快照。

最少必须显示：
- T_CLOSED_LOOP_ELAPSED_MS
- T_BOUNDARY_SEGMENT_ELAPSED_MS

已有冻结极限时还必须显示：
- T_STAR_MS

Reality 返回：
- PASS：整体累计 + 本次尝试 + 冻结T* + 现实T_VALID；
- FAIL/BLOCKED：整体累计 + 本次尝试 + 冻结T*；
- 证书未启动时允许“证书计时=0.000ms（未启动）”，但本次尝试耗时必须为真实数字。

状态词不能代替时间数字。

## 显示策略
内部小动作不要求刷屏。
关键控制边界必须显式显示。

因此：
ALWAYS COUNT
+
PRINT AT CONTROL BOUNDARY

不是：
PRINT EVERY STEP

## 虚拟测试
- 返回边界完整性矩阵：512/512 PASS，仅完整 1/512 允许；
- 随机往返闭环：20000/20000 PASS；
- Timeline 重建：0；
- 控制边界时间遗漏：0；
- 整体累计时间倒退：0；
- 10轮完整验证 MIN=274.027449ms，P50=280.736542ms。


## GPT / Codex 双端统一

v5.0.8 不再把 GPT 和 Codex 当成两套时间逻辑。

统一使用同一个最小时间信封：
- LOCATOR
- TIMELINE_ID
- T_CLOSED_LOOP_ELAPSED_MS
- T_EXCHANGE_ELAPSED_MS
- T_STAR_MS
- 必要结果

GPT -> Codex 派发：
必须带同一个时间信封。

Codex -> GPT 返回：
PASS / FAIL / BLOCKED 都必须带更新后的同一个时间信封。

GPT 接回时再次校验：
- TIMELINE_ID 不变；
- 整体累计时间不倒退；
- 冻结 T* 不漂移；
- 返回结果的必要时间数字齐全。

如果证书没有启动：
T_CERTIFICATE_ELAPSED_MS=0.000 可以成立，但必须明确 NOT_STARTED；
本次 Reality 尝试的 T_EXCHANGE_ELAPSED_MS 仍必须是实际数字，失败成本不能消失。

这不是增加第三阶段，而是：
一套信封 + 一套校验器 + 双向复用。

双端虚拟测试：
- GPT -> Codex 去程：32/32 PASS，仅完整 1/32 允许；
- Codex -> GPT FAIL/BLOCKED 回程：512/512 PASS，仅完整 1/512 允许；
- Codex -> GPT PASS 回程：1024/1024 PASS，仅完整 1/1024 允许；
- 完整随机往返链：20000/20000 PASS；
- Timeline 重建：0；
- T* 交接漂移：0；
- 整体累计时间倒退：0；
- 返回时间缺失：0。

共享校验器 100000 次局部基准：
MIN=0.001021ms
P50=0.001092ms
P95=0.001172ms
说明：这是校验器局部开销，不是整体 T*。

## 对 v5.0.7 Reality 返回的判定
该次 UnicodeEncodeError 返回虽然正确 STOP，但没有回传数值整体时间/本次尝试时间，因此：
RETURN_CONTROL_EVENT_COMPLETE=NO

它不能作为一个完整的时间连续控制事件。
Reality Delta 本身仍保留有效。

VIRTUAL_MATURE=YES
TIME_MODEL_FREEZE=PASS
REALITY_REENTRY=BLOCKED_UNTIL_ENCODING_DELTA_ABSORBED
