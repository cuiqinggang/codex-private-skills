# 标准 Reality Benchmark Suite R1｜极限短时间自动化闭环 v2.0

```ini
PAGE_NAME=极限短时间自动化闭环 v2.0
SUITE=ETAL-v2.0-BENCHMARK-SUITE-R1
STATE=10
OBJECTIVE=T*=min(T_VALID)
PURPOSE=用已经完成、适度复杂、可重复的真实任务测量不同成熟路径的现实端到端极限时间
```

## 1. 测试方法

本项目不是只测试一种固定架构。

先建立若干**已经完成的真实标准题**，每道题都固定：
- Reality 目标；
- 输入；
- FINAL_VALID；
- 环境；
- 时间边界；
- 验收方式。

然后让不同成熟路径执行同一道题：

```text
Direct Mature Control
GPT / Work
GPT / Work + Codex
Manus 2.0 Benchmark
其他成熟整解 / 成熟组合
未来优化后的 Virtual Mature 路径
```

只有同题、同 VALID、同现实边界的时间才可直接比较。

## 2. 三个时间概念

### 唯一优化目标

```text
T* = min(T_VALID)
```

每条路径从统一现实起点到 FINAL_VALID 的完整时间。

### Direct Mature Reference

```text
T_DIRECT_MATURE_REF
```

直接调用已经完成的成熟最终方案所需的现实有效时间。

它用于观察：
- 任务本身在当前环境至少需要多少现实执行时间；
- GPT / Codex / Agent 编排增加了多少调度、思考和交接开销。

它不是第二优化目标。

### 当前现实物理极限观测值

```text
T_REAL_PHYSICAL_STAR_CASE
= min(同一标准题当前所有已测 VALID 路径的 T_VALID)
```

含义：
**当前固定 Reality、环境和成熟能力集合下，已经真实观测到的最短有效端到端时间。**

它不是宇宙绝对常数；环境、输入、供应商或成熟能力变化后可以被新的 Reality 打破。

## 3. 攻击迭代

每轮完成后：

```text
收集各路径 T_VALID
→ 找当前 T_REAL_PHYSICAL_STAR_CASE
→ 分解较慢路径的时间损失
→ 删除无收益层
→ 组合更成熟、更短的现成路径
→ Virtual Mature
→ 计算新的预期 T_VALID
→ Reality
→ 与当前 T_REAL_PHYSICAL_STAR_CASE 比较
→ 有收益则升级基线
```

Codex、Browser、n8n、OpenClaw、GitHub、MCP 等都只是可被测、被组合、被删除的成熟能力。

## 4. Benchmark Case 001｜抖音极速直下 Windows v1.0.0

### 为什么选它

这是已经完成的用户级适度复杂真实任务，覆盖：
- 自然语言目标；
- Windows；
- clipboard；
- URL 提取；
- Web / Browser；
- 登录态复用；
- 主路径失败后的自动 fallback；
- 后台浏览器；
- 文件下载；
- 媒体候选选择；
- 本地文件；
- 视频 / 音频 / 完整性验证；
- 用户级 FINAL_VALID。

因此比纯计算 microbenchmark 更适合测试“自动化闭环”。

### 固定现实目标

```text
给定同一条当前有效的抖音分享链接
→ 获取完整视频
→ 输出 Windows 桌面
→ 无需人工浏览器操作
→ 无需人工 media URL 交接
→ 浏览器正常不露出
→ 文件可播放
→ 图像正常
→ 音频存在且可播放
→ 视频完整
```

### FINAL_VALID

```ini
DESKTOP_OUTPUT=YES
DOWNLOAD_PASS=YES
VIDEO_PLAYBACK=YES
VIDEO_IMAGE_NORMAL=YES
AUDIO_PRESENT=YES
AUDIO_PLAYBACK=YES
COMPLETE_VIDEO=YES
WINDOW_VISIBLE=NO
MANUAL_BROWSER_ACTION=NO
MANUAL_MEDIA_HANDOFF=NO
```

执行器自身的 Done / PASS 不能替代这些现实门。

### 输入冻结规则

同一比较轮必须使用同一条有效分享链接和同一目标媒体。

如果外部平台使旧链接失效：
1. 冻结一条新的有效样本；
2. 同一轮所有路径全部改用新样本；
3. 旧轮时间保留为历史，不跨样本直接比较。

### 历史时间说明

Reality 02 曾观测一键时间约 25.073 秒；Reality 03 曾观测约 153.098 秒。

但后续用户级检查发现旧产物存在播放 / 音频 VALID 缺口，因此这两个值**不得作为 Case 001 的最终物理基线**。

Case 001 必须从最终完成版重新测得：

```text
T_DIRECT_MATURE_REF_CASE_001
```

## 5. Calibration Anchor 000｜JEV Probability Engine P0 v0.4.0

JEV P0 不作为 Case 001 的替代，而作为计时系统与极限攻击方法的短时校准锚。

已认证现实事实：

```ini
VERSION=v0.4.0
STATUS=REAL_P0_CERTIFIED
BENCHMARK=PE-P0-GENERAL-01
CANDIDATE=JPE-P0-S2-PERSISTENT-TRANSPORT-V2
T_REAL_STAR_MS=560.9819
P50_MS=648.87
P95_MS=988.8238
MAX_MS=1285.2925
MEASURED_RUNS=30
PASS_RUNS=30
FAIL_RUNS=0
HTTP_REQUESTS=67/67
```

固定时间边界：

```text
T0 = formal public input read 之前
T1 = VerifyRealityAsync 完成并写完 per-run manifest 之后
```

计时内包含：
输入读取、状态/问题构建、sharding、serialization、2 次并行 HTTP、解析、本地执行、dependency waits、receipt verification、manifest write。

来源：
- branch: `codex/jev-probability-engine-p0-v0.4.0`
- certification: `skills/first-principles-physical-limit-convergence/components/jev-probability-engine-p0-extreme/certifications/v0.4.0/REALITY_CERTIFICATION.md`

## 6. Case 001 路径矩阵

第一轮：

```text
C0 Direct Mature Final Solution
   → T_DIRECT_MATURE_REF_CASE_001

P1 GPT / Work
   → T_VALID_WORK_CASE_001

P2 GPT / Work + Codex
   → T_VALID_WORK_CODEX_CASE_001

B1 Manus 2.0
   → T_REF_MANUS_CASE_001
```

后续：
- 其他成熟完整方案；
- 其他成熟执行器；
- 更小成熟组合；
- Virtual Mature 优化路径。

每条新路径都必须跑同一 Case 001。

## 7. 第一轮结束条件

必须真实得到至少：

```ini
T_DIRECT_MATURE_REF_CASE_001=<measured>
T_VALID_WORK_CASE_001=<measured or FAIL>
T_VALID_WORK_CODEX_CASE_001=<measured or NOT_NEEDED>
T_REF_MANUS_CASE_001=<measured or FAIL>
T_REAL_PHYSICAL_STAR_CASE_001=<min VALID measured>
```

然后才进入“分析 → 删除 → 组合 → Virtual Mature → Reality 再攻击”。

## 8. 后续 Benchmark Cases

Case 001 只是第一题。

后续继续加入不同类型的已完成真实任务，以避免只优化一种工作负载：
- 浏览器 / 本地文件型；
- 编码 / 工程型；
- 信息检索 / 分析型；
- 长任务 / 恢复型；
- 定时 / 触发型。

每个 Case 自己有一个 `T_REAL_PHYSICAL_STAR_CASE`；不同任务类型不强行混成同一个数。
