# v4.7.4 本机 Codex 状态门现实认证 01-02

定位：
【整体闭环极限时间引擎4.7版｜v4.7.4状态门认证｜01-02｜实】 极限锚03:14.419

FREEZE_ID=V474-STATE-GATE-01-02
REAL_WORKDIR=C:\AI\Mature-Download-Router-Real-Test
REAL_WORKDIR_PROVEN=YES

只做状态门现实认证，不重新设计方法，不现场修规则。

关键执行入口规则：
1. 所有本地命令工具调用必须直接指定 workdir=`C:\AI\Mature-Download-Router-Real-Test`。
2. 禁止先从默认目录启动 PowerShell/cmd/node 后再 `cd`。
3. 第一条本地动作必须是无副作用进程启动预检。
4. 预检建议：PowerShell 7 只输出 `PROCESS_SPAWN_PRECHECK=PASS`。
5. 若该已验证窄目录仍出现相同 1344：若当前执行器已经存在已授权、已证明可工作的备用执行通道，可原样重试一次；否则立即 STOP，不得绕过安全策略。

进程预检 PASS 后，再核对以下 8 项：
1. `01-01虚 -> 01-01实`：允许。
2. `01-03实 FAIL -> 01-04虚`：允许。
3. `01-03实`出现结构性现实差异 -> `02-01虚`：允许。
4. `01-06实 FAIL -> 02-01虚`：允许。
5. `01-06实 FAIL -> 01-07虚`：阻断。
6. 同一 FREEZE_ID 第二次 REAL：阻断。
7. 极限锚不是 `194419.3759ms`：阻断。
8. 虚完成但现实任务没有发布/自动发送：阻断。

只有进程预检 PASS 且 8/8 全部符合预期才 PASS。

禁止：修改代理、系统设置、FlClash；git fetch；修改技能包；现场改规则。

最终只返回：
METHOD=extreme-short-time-engine-v4.7.4
REALITY_FOUNDATION=local-ai-reality-foundation@1.1.7
STATE=01-02
FREEZE_ID=V474-STATE-GATE-01-02
REAL_WORKDIR=C:\AI\Mature-Download-Router-Real-Test
PROCESS_SPAWN_PRECHECK=PASS|FAIL
TESTS=8
PASS_COUNT=<0-8>
LOCAL_CODEX_STATE_GATE=PASS|FAIL
REALITY_DELTA=<NONE或最小差异>
ACTION=STOP
RETURN_TO_GPT=YES

最后一行原样回显：
【整体闭环极限时间引擎4.7版｜v4.7.4状态门认证｜01-02｜实】 极限锚03:14.419
