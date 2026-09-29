# v5.6.4 虚拟成熟记录

VIRTUAL_MATURE=PASS
REALITY_CERTIFIED=NO
FINAL_VALID=NO
FREEZE_ID=FPLC-v5.6.4-REALITY-TIME-DISPATCH-CONTRACT-R1

## 根因

v5.6.3 的 advance → render → _dispatch_command 正式出口已经能生成完整三行。
现实缺陷来自 GPT/宿主 Reality 文本可能绕过该合同。

## 最小升级

只固化：
- Reality 三行必填
- GPT_DISPATCH_TIME 与 TASK_ACCEPTED 分离
- 收件现场冻结 accepted_clock + accepted_tick_ns
- 缺任一时间要素 fail-closed
- 重复故障分层诊断

不修改：
- 10→20→30→40→100 状态机
- T_VALID 机械计算核心
- 实体证据 SHA256
- DSE / 业务 Freeze
- 其他已 PASS 部分

## 虚拟验证

原缺陷命令：
LOCATOR_PRESENT=YES
STATE_HEADER_PRESENT=NO
TIME_ANCHOR_PRESENT=NO
→ DISPATCH_READY=NO

02 生产同构样本：
LOCATOR_PRESENT=YES
STATE_HEADER_PRESENT=YES
TIME_ANCHOR_PRESENT=YES
TASK_ACCEPTED_CREATED_AT_RECEIPT=YES
TIME_ORIGIN_FROZEN_ONCE=YES
T_VALID_MECHANICALLY_DERIVED=YES
→ PASS

结论：
方案边界单一，已有现实样本证明可行，允许冻结并进入 v5.6.4 Reality。
