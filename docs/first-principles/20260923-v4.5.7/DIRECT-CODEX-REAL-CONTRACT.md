# v4.5.7 Direct Codex REAL Contract

This is a self-contained GPT -> Codex handoff. The user does not run an outer PowerShell wrapper.

## Exact four-position label

```text
【极限短时间引擎｜ESTE-20260922-001现实验证｜01｜实】
```

Fields:

1. 页面名 = 极限短时间引擎
2. 任务名 = ESTE-20260922-001现实验证
3. 序号 = 01
4. 阶段 = 实

Codex must echo the exact same label at the beginning and end.

## Contract

```text
【极限短时间引擎｜ESTE-20260922-001现实验证｜01｜实】

只执行冻结合同，不重新设计，不现场修复，不读取任何 Skill 文件。

你是 Codex REAL 执行器。

现实硬约束：
- 不执行 git fetch。
- 不写 .git/FETCH_HEAD 或其他 Git 元数据作为启动前提。
- 不写 Temp/AppData 中的可执行 .ps1。
- 不修改代理、系统设置、FlClash 或虚拟网卡。
- 不把 w32tm /query /source 作为硬依赖。
- PowerShell 只作为你内部的确定性本机工具。

计时要求：
- 第一项动作必须立即用 PowerShell 读取：
  CODEX_ACTIVE_START_TIMESTAMP=[DateTimeOffset]::Now
  CODEX_START_TICK=[System.Diagnostics.Stopwatch]::GetTimestamp()
  CODEX_STOPWATCH_FREQUENCY=[System.Diagnostics.Stopwatch]::Frequency
- 保存这三个实际数值在本轮执行上下文中，不写临时脚本。
- 最终输出前，再读取 CODEX_ACTIVE_END_TIMESTAMP 和 CODEX_END_TICK。
- 使用真实 start tick / end tick / frequency 计算：
  CODEX_PROCESS_ACTIVE_MS=(END_TICK-START_TICK)*1000/FREQUENCY
- 禁止估算时间。

唯一现实验证：
1. PowerShell 主版本必须 >= 7。
2. 运行：
   nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits
   第一块 GPU 必须为 NVIDIA GeForce RTX 2080 Ti。
   显存必须为 22528 MiB，允许绝对误差 <= 32 MiB。
3. 只检查以下路径是否存在：
   C:\AI\Playwright-Native-AI-Browser
   C:\AI\OpenHands-Canvas
   C:\AI\Bonsai2-27B-256K
4. 不做 GPU workload，不启动浏览器，不启动模型。

如果全部通过，只返回以下机器结果，加真实计时字段：
METHOD=extreme-short-time-engine-v4.5.7
PHASE=REAL
REALITY_FOUNDATION=local-ai-reality-foundation@1.1.2
VALID_REAL=PASS
POWERSHELL_REALITY=PASS
GPU_REALITY=PASS
ASSET_PATHS=PASS
REALITY_DELTA=NONE
CODEX_ACTIVE_START_TIMESTAMP=<真实值>
CODEX_ACTIVE_END_TIMESTAMP=<真实值>
CODEX_PROCESS_ACTIVE_MS=<真实值>
ACTION=STOP
RETURN_TO_GPT=YES

如果任一项失败：
METHOD=extreme-short-time-engine-v4.5.7
PHASE=REAL
REALITY_FOUNDATION=local-ai-reality-foundation@1.1.2
VALID_REAL=FAIL
REALITY_DELTA=<最小具体差异>
CODEX_ACTIVE_START_TIMESTAMP=<真实值>
CODEX_ACTIVE_END_TIMESTAMP=<真实值>
CODEX_PROCESS_ACTIVE_MS=<真实值>
ACTION=STOP
RETURN_TO_GPT=YES

不要添加方案，不要修复。

最后一行必须原样回显：
【极限短时间引擎｜ESTE-20260922-001现实验证｜01｜实】
```
