# v4.5.10 Direct Codex REAL Contract

Sequence source: `TASK-SEQUENCE-LEDGER.json`; expected sequence for this handoff = `02`. Dispatch timestamp and active-total metadata are mandatory and are filled at the moment GPT emits this contract.

```text
【极限短时间引擎｜ESTE-20260922-001现实验证｜02｜实】
```

Four-position label must be echoed exactly at the beginning and end.

## Contract

```text
【极限短时间引擎｜ESTE-20260922-001现实验证｜02｜实】

TASK_TIME_ID=ESTE-20260922-001
TASK_SEQUENCE=02
GPT_DISPATCH_TIMESTAMP=2026-09-23T03:05:25+08:00
ACTIVE_TOTAL_BEFORE_DISPATCH=00:49:15.700 (LOWER_BOUND)
TIME_ACCOUNTING_STATUS=LOWER_BOUND_DUE_TO_LEGACY_UNINSTRUMENTED_INTERVALS

只执行冻结合同，不重新设计，不现场修复，不读取任何 Skill 文件。

你是 Codex REAL 执行器。

现实硬约束：
- 不执行 git fetch。
- 不写 .git/FETCH_HEAD 或其他 Git 元数据作为启动前提。
- 不写 Temp/AppData 中的可执行 .ps1。
- 不修改代理、系统设置、FlClash 或虚拟网卡。
- 不把 w32tm /query /source 作为硬依赖。
- PowerShell 只作为你的内部确定性本机工具。

计时：
第一项动作立即记录：
CODEX_ACTIVE_START_TIMESTAMP=[DateTimeOffset]::Now
CODEX_START_TICK=[System.Diagnostics.Stopwatch]::GetTimestamp()
CODEX_STOPWATCH_FREQUENCY=[System.Diagnostics.Stopwatch]::Frequency

保存真实值在本轮执行上下文，不写临时脚本。

现实验证：

A. PowerShell
- 确认 PowerShell 主版本 >= 7。
- 若不满足：REALITY_DELTA=POWERSHELL_MAJOR_LT_7。

B. GPU 只读探针
执行：
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits

该命令是只读、无副作用、输出结构已冻结的探针。
必须同时记录：
GPU_PROBE_STDOUT=<原始第一条有效非空行>
GPU_PROBE_EXIT_STATUS=<真实退出码或执行层报告>

语义有效门：
- 从 stdout 第一条有效非空行解析 GPU name 和 memory.total。
- 若 GPU name = NVIDIA GeForce RTX 2080 Ti
  且 memory.total = 22528，允许绝对误差 <= 32 MiB，
  且 stdout 完整、可解析、无矛盾，
  则 GPU_REALITY=PASS。
- 即使 GPU_PROBE_EXIT_STATUS != 0，也不得仅凭退出码把上述有效语义证据判 FAIL。
- 非零退出码此时只作为诊断字段保留。
- 只有 stdout 缺失、截断、无法解析、与要求矛盾，才判 GPU_REALITY=FAIL。

C. 现实资产路径
只检查：
C:\AI\Playwright-Native-AI-Browser
C:\AI\OpenHands-Canvas
C:\AI\Bonsai2-27B-256K

三个路径全部存在：
ASSET_PATHS=PASS
否则：
ASSET_PATHS=FAIL
REALITY_DELTA=PATH_MISSING:<具体路径>

禁止运行 GPU workload、浏览器、模型。

结束计时：
最终输出前记录：
CODEX_ACTIVE_END_TIMESTAMP=[DateTimeOffset]::Now
CODEX_END_TICK=[System.Diagnostics.Stopwatch]::GetTimestamp()

计算：
CODEX_PROCESS_ACTIVE_MS=(CODEX_END_TICK-CODEX_START_TICK)*1000/CODEX_STOPWATCH_FREQUENCY

最终有效条件：
POWERSHELL_REALITY=PASS
AND GPU_REALITY=PASS
AND ASSET_PATHS=PASS

满足时只返回：

METHOD=extreme-short-time-engine-v4.5.10
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

若任一最终有效条件失败，只返回同样字段，但：
VALID_REAL=FAIL
REALITY_DELTA=<最小具体差异>

不要因为只读 GPU 探针的 nonzero exit 覆盖已经通过的完整语义证据。
不要添加方案，不要修复。

最后一行必须原样输出：
【极限短时间引擎｜ESTE-20260922-001现实验证｜02｜实】
```
