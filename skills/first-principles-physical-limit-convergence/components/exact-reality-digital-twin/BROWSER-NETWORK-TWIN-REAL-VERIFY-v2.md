# Browser + Network Twin 冻结现实验证 v2

定位：第三核心「高智能虚拟成熟」的冻结方案现实验证。
CURRENT_STEP=3。

禁止重新设计方案。

## 固定输入
读取：
- ENGINE.py
- BROWSER-TWIN-INPUT-CONTRACT-v2.md
- VIRTUAL-FUSION-STATUS-v2.txt
- reality-execution-environment-anchor/BROWSER-REALITY-R3-ACCEPTANCE.md
- reality-execution-environment-anchor/collectors/browser-reality-r3-timing.mjs
- reality-execution-environment-anchor/collectors/browser-reality-r3.mjs
- reality-execution-environment-anchor/collectors/browser-host-network-r3.ps1

## 固定执行顺序

1. 只使用“已经存在”的真实浏览器控制通道，优先级固定：
   A. 当前会话已经可调用的 Playwright 浏览器控制工具；
   B. 已存在的 Playwright BrowserServer endpoint；
   C. 已存在的 CDP endpoint。
   禁止为了通过验证而启动一个替代浏览器。

2. 如果 A/B/C 都不存在：
   REALITY_DELTA=NO_EXISTING_BROWSER_ATTACH_PATH
   ACTION=STOP
   RETURN_TO_GPT=YES

3. Attach 成功后，不改变当前现实浏览器状态。
   先执行三个预声明轻量计时运行：T1/T2/T3。
   任一次失败即 STOP；禁止补第 4 个 timing run。

4. T1/T2/T3 全部完成后，执行一个预声明 O1 可观测运行。
   O1 不能替代任何 timing run，也不进入 T_VALID。

5. 把 T1/T2/T3 + O1 输入 ENGINE.py：
   - validate
   - replay
   - reality/twin diff
   - benchmark（只测 Twin 本地重放开销）

6. 只有以下全部成立：
   GOLDEN_TASK_REALITY_REPRODUCED=3_OF_3
   BROWSER_CRITICAL_UNKNOWN_COUNT=0
   TWIN_REPLAY=PASS
   REALITY_TWIN_DELTA_COUNT=0
   OBSERVATION_PERTURBATION=NO
   BROWSER_R3_FINGERPRINT_CREATED=YES
   才允许 BROWSER_TWIN_INPUT_READY=YES。

7. T_VALID 固定：
   T_VALID=min(T1,T2,T3)
   O1 不计入 T_VALID。

8. 任何失败：
   只记录 REALITY_DELTA
   STOP
   RETURN_TO_GPT
   禁止 Codex 自行改变路线。

最终回传：
ATTACH_PATH=
T1_MS=
T2_MS=
T3_MS=
T_VALID_MS=
O1=
BROWSER_CRITICAL_UNKNOWN_COUNT=
GOLDEN_TASK_REALITY_REPRODUCED=
TWIN_REPLAY=
REALITY_TWIN_DELTA_COUNT=
TWIN_REPLAY_OVERHEAD_P50_MS=
BROWSER_R3_FINGERPRINT=
BROWSER_TWIN_INPUT_READY=
FULL_BROWSER_TWIN=
ENVIRONMENT_99=
REALITY_DELTA=
ACTION=STOP
