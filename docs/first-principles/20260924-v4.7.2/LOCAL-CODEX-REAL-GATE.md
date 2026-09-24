# v4.7.2 本机 Codex 有限循环状态门现实认证

四定位：`【极限短时间引擎｜v4.7.2状态门现实认证｜G01-A01｜实】`

目的：不重新设计方法，只验证本机 Codex 能按冻结的有限循环状态规则机械 ALLOW/BLOCK。

硬边界：不修改代理/系统设置；不 git fetch；不写 Temp/AppData 可执行脚本；不修改技能包。

必须测试：
1. G01-A01-虚 -> G01-A01-实：合法。
2. G01-A03-实 FAIL -> G01-A04-虚：合法。
3. G01-A03-实 STRUCTURAL FAIL -> G02-A01-虚：合法。
4. G01-A06-实 FAIL -> G02-A01-虚：合法。
5. G01-A06-实 FAIL -> G01-A07-虚：必须 BLOCK。
6. 同一 FREEZE_ID 第二次 REAL：必须 BLOCK。
7. `T_CLOSED_REAL_NOW_MS=300000` 时，`TIME_GAP_MS=105580.6241`，`TIME_STATE=OVER_TARGET`。
8. 用户可见第一行缺少完整横向状态锚：必须 BLOCK。

计时：第一项动作记录 CODEX_ACTIVE_START_TIMESTAMP；最后记录 CODEX_ACTIVE_END_TIMESTAMP 和 CODEX_PROCESS_ACTIVE_MS。

最终只有 8/8 符合预期才 PASS。

返回：
`METHOD=extreme-short-time-engine-v4.7.2`
`REALITY_FOUNDATION=local-ai-reality-foundation@1.1.7`
`FINITE_CYCLE_TESTS=8`
`FINITE_CYCLE_PASS=8`
`LOCAL_CODEX_STATE_GATE=PASS|FAIL`
`REALITY_DELTA=<NONE或最小差异>`
`CODEX_PROCESS_ACTIVE_MS=<真实值>`
`ACTION=STOP`
`RETURN_TO_GPT=YES`

最后一行原样回显：
`【极限短时间引擎｜v4.7.2状态门现实认证｜G01-A01｜实】`
