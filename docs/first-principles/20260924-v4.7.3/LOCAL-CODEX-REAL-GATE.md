# v4.7.3 本机 Codex 极简状态门现实认证

用户可见定位：
【极限短时间引擎｜v4.7.3极简状态门认证｜01-01｜实】 极限锚03:14.419

只验证状态门，不重新设计方法。

必须验证：
1. 01-01虚 -> 01-01实：允许。
2. 01-03实 FAIL -> 01-04虚：允许。
3. 01-03实出现结构性现实差异 -> 02-01虚：允许。
4. 01-06实 FAIL -> 02-01虚：允许。
5. 01-06实 FAIL -> 01-07虚：阻断。
6. 同一 FREEZE_ID 第二次 REAL：阻断。
7. 极限锚不是 194419.3759ms：阻断。
8. 虚完成但现实任务未发布：阻断。

8/8 全符合预期才 PASS。

禁止改代理、系统设置、FlClash；禁止 git fetch；禁止修改技能包；禁止现场修规则。

最终返回：
METHOD=extreme-short-time-engine-v4.7.3
REALITY_FOUNDATION=local-ai-reality-foundation@1.1.7
STATE_FORMAT=NN-NN
MAX_REAL_ATTEMPTS_PER_GENERATION=6
TESTS=8
PASS_COUNT=8
LOCAL_CODEX_STATE_GATE=PASS|FAIL
REALITY_DELTA=<NONE或最小差异>
ACTION=STOP
RETURN_TO_GPT=YES

最后一行原样回显：
【极限短时间引擎｜v4.7.3极简状态门认证｜01-01｜实】 极限锚03:14.419
