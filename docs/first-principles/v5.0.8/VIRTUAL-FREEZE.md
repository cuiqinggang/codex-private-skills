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

## 对 v5.0.7 Reality 返回的判定
该次 UnicodeEncodeError 返回虽然正确 STOP，但没有回传数值整体时间/本次尝试时间，因此：
RETURN_CONTROL_EVENT_COMPLETE=NO

它不能作为一个完整的时间连续控制事件。
Reality Delta 本身仍保留有效。

VIRTUAL_MATURE=YES
TIME_MODEL_FREEZE=PASS
REALITY_REENTRY=BLOCKED_UNTIL_ENCODING_DELTA_ABSORBED
