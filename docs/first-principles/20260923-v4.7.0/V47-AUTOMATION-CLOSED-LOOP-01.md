# V47-AUTOMATION-CLOSED-LOOP-01

## 目标

在 v4.7.0 双时间单闭环合同下，对已有 GPT↔Codex v1.5.2 + Playwright Native AI Browser 做兼容性/回归认证，不从零研发。

用户只允许一次初始提交；中间普通 transport、结果回传、Reality Delta 回虚、第二次冻结与第二次执行全部自动完成。

## 业务范围

使用低风险、可验证、无敏感副作用的 toy WRITE_FILE 作为控制面验收业务效果。该 PASS 只证明自动闭环控制面，不外推为任意业务动作授权。

## 单闭环

USER INITIAL INPUT -> GPT VIRTUAL -> AUTO GPT_TO_CODEX -> CODEX REAL -> AUTO CODEX_TO_GPT -> GPT JUDGE -> INJECTED RECOVERABLE REALITY DELTA -> AUTO RETURN VIRTUAL -> AUTO SECOND FREEZE -> AUTO SECOND EXECUTION -> VERIFIER PASS -> GPT FINAL_VALID -> USER NOTIFIED

## Reality Delta 注入

禁止通过改变代理、网络、权限、系统设置、GitHub 可用性来制造故障。
第一次执行使用无副作用注入：REALITY_DELTA=V47_INJECTED_RECOVERABLE_CONTROL_DELTA；BUSINESS_EFFECT_WRITTEN=NO；RETURN_TO_GPT=YES。
GPT 必须自动重新成熟并冻结第二次执行；第二次才允许完成 toy WRITE_FILE 和 verifier。

## 硬门

INITIAL_USER_INPUT_COUNT=1
MANUAL_MIDDLE_COPY_PASTE=0
MANUAL_CODEX_INPUT=0
MANUAL_RESULT_RELAY=0
MANUAL_BROWSER_ROUTING=0
GPT_TO_CODEX=AUTO
CODEX_TO_GPT=AUTO
REALITY_DELTA_RETURN=AUTO
SECOND_FREEZE=AUTO
SECOND_EXECUTION=AUTO
BUSINESS_EFFECT_DUPLICATE=0
FINAL_VALID=PASS
CLOSED_LOOP_AUTONOMOUS=PASS

## 时间合同

T_MATURE_STAR 固定引用当前成熟锚 00:03:14.419；本验收不重新定义它。
T_CLOSED_REAL_START 在用户唯一初始提交时自动打点。
T_CLOSED_REAL_END 在 GPT FINAL_VALID=PASS 时自动打点。
T_CLOSED_REAL=END-START，任何等待、失败、回虚、用户离开均不重置。
同时把每个墙钟区间唯一归因到 v4.7.0 诊断桶。

## 浏览器回归策略

已有 30/30 Playwright 性能证据不默认重跑完整 30-run benchmark。
本验收只验证当前 closed-loop transport 的兼容性、会话恢复、send/wait_extract、结果回传和多轮无人值守。
只有发现 Browser Reality drift 或性能异常，才升级为完整 R3 30-run reality verify。

## GPT↔Codex 回归策略

复用 v1.5.2 A/B/C 三条成熟简单路径。路径选择必须服从当前现实和 T_CLOSED_REAL，不允许为了维护某条 transport 而阻塞任务。
A/B/C 任一路正常完成均可作为 transport PASS；中间不得由用户复制粘贴。
自然 failover 若本次没有真实发生，不得伪造为已验证。

## 最终输出

T_MATURE_STAR=
T_CLOSED_REAL=
T_CLOSED_REAL_MODE=AUTOMATED
CLOSED_REAL_ATTRIBUTION=
MANUAL_MIDDLE_INTERVENTIONS=
GPT_TO_CODEX=
CODEX_TO_GPT=
REALITY_DELTA_RETURN=
SECOND_FREEZE=
SECOND_EXECUTION=
BUSINESS_EFFECT_DUPLICATE=
CLOSED_LOOP_AUTONOMOUS=
FINAL_VALID=
REALITY_DELTA=

AUTOMATION_SAVED_TIME 和 AUTOMATION_REDUCTION_PERCENT 只有在同任务精确 manual baseline 存在时才计算；不能用“用户报告几个小时”伪造百分比。
