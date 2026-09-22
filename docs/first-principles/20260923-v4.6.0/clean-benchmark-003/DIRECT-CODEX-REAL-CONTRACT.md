【极限短时间引擎｜v4.6.0干净闭环验证｜01｜实】

TASK_TIME_ID=ESTE-20260923-003
TASK_SEQUENCE=01
GPT_DISPATCH_TIMESTAMP=2026-09-23T03:36:15+08:00
ACTIVE_TOTAL_BEFORE_DISPATCH=00:02:29

只执行冻结合同，不重新设计，不现场修复，不读取任何 Skill 文件。
你是 Codex REAL 执行器。

第一项动作立即记录：
CODEX_ACTIVE_START_TIMESTAMP=[DateTimeOffset]::Now
CODEX_START_TICK=[System.Diagnostics.Stopwatch]::GetTimestamp()
CODEX_STOPWATCH_FREQUENCY=[System.Diagnostics.Stopwatch]::Frequency

现实验证：
1. 确认 PowerShell 主版本 >= 7。
2. 执行只读 GPU 探针：
   nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits
   要求第一块 GPU = NVIDIA GeForce RTX 2080 Ti；显存 = 22528 MiB，允许绝对误差 <= 32 MiB。
   对该只读探针，完整可解析且满足冻结语义门的 stdout 优先于 nonzero exit status；exit status 只保留为诊断。
3. 检查以下路径存在：
   C:\AI\Playwright-Native-AI-Browser
   C:\AI\OpenHands-Canvas
   C:\AI\Bonsai2-27B-256K
4. 不执行 git fetch；不写 .git/FETCH_HEAD；不写 Temp/AppData 可执行脚本；不改代理/系统设置；不运行 GPU workload、浏览器或模型。

最终输出前记录：
CODEX_ACTIVE_END_TIMESTAMP=[DateTimeOffset]::Now
CODEX_END_TICK=[System.Diagnostics.Stopwatch]::GetTimestamp()
CODEX_PROCESS_ACTIVE_MS=(CODEX_END_TICK-CODEX_START_TICK)*1000/CODEX_STOPWATCH_FREQUENCY

最终有效条件：
POWERSHELL_REALITY=PASS AND GPU_REALITY=PASS AND ASSET_PATHS=PASS

全部通过时只返回：
METHOD=extreme-short-time-engine-v4.6.0
PHASE=REAL
REALITY_FOUNDATION=local-ai-reality-foundation@1.1.3
VALID_REAL=PASS
POWERSHELL_REALITY=PASS
GPU_REALITY=PASS
GPU_PROBE_STDOUT=<真实值>
GPU_PROBE_EXIT_STATUS=<真实值>
ASSET_PATHS=PASS
REALITY_DELTA=NONE
CODEX_ACTIVE_START_TIMESTAMP=<真实值>
CODEX_ACTIVE_END_TIMESTAMP=<真实值>
CODEX_PROCESS_ACTIVE_MS=<真实值>
ACTION=STOP
RETURN_TO_GPT=YES

若失败则 VALID_REAL=FAIL，并返回最小 REALITY_DELTA；不得现场修复。

最后一行必须原样输出：
【极限短时间引擎｜v4.6.0干净闭环验证｜01｜实】
