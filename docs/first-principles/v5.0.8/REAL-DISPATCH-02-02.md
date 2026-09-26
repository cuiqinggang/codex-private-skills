【整体闭环极限时间引擎5.0.2版｜v5.0.8双端数值时间锚现实认证R2｜02-02｜实】
【时间锚｜整体已用=4441551.271ms｜本次已用=0.000ms｜T*=0.011368381ms】

TIMELINE_ID=ESTE-v5.0.7-NUMERIC-TIME-ANCHOR-01
TIME_ORIGIN_UTC=2026-09-26T19:12:16.448729+00:00
DISPATCH_UTC=2026-09-26T20:26:18+00:00

共同私库分支：
codex/first-principles-physical-limit-convergence-v5.0.8-virtual-freeze

冻结：
ESTE-v5.0.8-DUAL-END-NUMERIC-TIME-ASCII-CAPSULE-VIRTUAL-FREEZE-R2

完整 Manifest：
docs/first-principles/v5.0.8/FREEZE-MANIFEST-R2.json
Manifest blob：
de30a26c9c3f67084910f42931bac3201da991a9

冻结回读：
22/22 MATCH

只执行冻结 Reality Capsule：
docs/first-principles/v5.0.8/REAL-CAPSULE-SOURCE-R2.py

严格保持原状态机和共同私库直读主路径。不要下载，不要重新确定本地位置，不要现场修复，不要重新设计。

Reality 计时前先完成前置物化门：
1. 读取精确冻结 blob；
2. 核对 blob；
3. 确认源码为 ASCII-only；
4. compile；
5. 在 fresh namespace 中 exec；
6. 确认 run_reality_certificate 存在且 callable。

不要通过会重新编码源码文本的 PowerShell 字符串管道转发冻结源码。

上述前置物化全部 PASS 后，才开始证书计时：
T_VALID_START = 紧接调用 run_reality_certificate() 之前；
T_VALID_END = 18/18 PASS 返回后立即记录。

Reality 门：
T_VALID_REAL_MS <= 0.01136838145574825 ms

无论 PASS、FAIL 或 BLOCKED，返回首屏都必须使用同一数值时间信封：

【整体闭环极限时间引擎5.0.2版｜v5.0.8双端数值时间锚现实认证R2｜02-02｜实】
【时间锚｜整体已用=<数值>ms｜本次已用=<数值>ms｜T*=0.011368381ms】

整体已用：
用返回时 UTC - TIME_ORIGIN_UTC 计算。

本次已用：
用返回时 UTC - DISPATCH_UTC 计算。

若 PASS，另外必须返回：
REAL_T=<T_VALID_REAL_MS>ms
CERTIFICATE=18/18 PASS
TIME_GATE=PASS
REAL_PASS=YES

若在证书调用前 FAIL/BLOCKED：
证书计时=0.000ms（未启动）
REAL_PASS=NO
REALITY_DELTA=<具体原因>

若证书启动后 FAIL：
必须返回真实证书计时和 Reality Delta。

任何返回如果缺少数值整体时间、本次时间或冻结 T*，视为 CONTROL_EXCHANGE_INVALID。

报告后停止，不继续修复或重试。
