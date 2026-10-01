# Benchmark Case 001｜抖音极速直下 Windows v1.0.0

```ini
CASE_ID=ETAL-v2.0-CASE-001
TYPE=MODERATE_COMPLEXITY_USER_E2E
STATUS=READY_FOR_REALITY_BASELINE
HISTORICAL_PROJECT=抖音极速直下 Windows v1.0.0
OBJECTIVE=T*=min(T_VALID)
```

## 目标

用一个已经完成的适度复杂真实项目，固定成所有路径共享的标准测试题。

不是重新开发“抖音极速直下”。

每个候选路径的任务是：

> 接到相同用户目标后，自动识别并复用世界 / 工作区中已经成熟的解决能力，用最短有效路径得到最终有声、可播放、完整视频，并完成现实验收。

## 固定 VALID

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

## 现实环境

- Windows 10；
- 现有成熟桌面入口 / 工作区可作为世界成熟能力被检索复用；
- 现有 Playwright profile / 登录态只有在该候选路径依法选择时才可复用；
- FlClash / Windows 网络代理禁止修改；
- 不为 Benchmark 新造下载器、Browser framework 或 Adapter。

## 输入

每一轮开始时冻结：
- 一条当前有效抖音分享链接；
- 对应目标 aweme；
- 同一轮所有候选使用同一样本。

旧历史样本可以优先尝试；若已失效，换新样本后整轮重新基线。

## 统一 Flow Start

```text
候选系统已经收到：
“把这条抖音分享链接以完整有声可播放视频下载到 Windows 桌面”
以及同一冻结样本，
并且不再等待用户补充信息的现实时间点。
```

## 统一 Flow End

```text
桌面目标文件已经真实存在，
机器 verifier 完成图像 / 音频 / 完整性检查，
并且满足全部 FINAL_VALID 的现实时间点。
```

不需要用户再手工打开播放器证明机器可验证事实。

## C0｜Direct Mature Control

直接运行最终完成版成熟方案。

目的：
- 测任务本体 + 已成熟执行链的现实时间；
- 得到 `T_DIRECT_MATURE_REF_CASE_001`；
- 定位智能编排层额外开销。

C0 不参加“谁是未来智能主链”的选择，只做物理参考。

## P1｜GPT / Work

GPT 作为核心大脑，只使用它认为必要的成熟能力。

不得人为要求必须调用 Codex。

输出：
`T_VALID_WORK_CASE_001`

## P2｜GPT / Work + Codex

Codex 是测评对象。

只有路径定义明确包含 Codex 时运行。

所有：
- 交接；
- session 切换；
- 等待；
- 执行；
- 回传；
- 验收
全部计时。

输出：
`T_VALID_WORK_CODEX_CASE_001`

## B1｜Manus 2.0

使用现有积分，仅作为成熟商业整解参考。

输出：
`T_REF_MANUS_CASE_001`

Manus 不进入最终正式生产方案。

## 当前 Reality 结果表

| Path | VALID | T_VALID | User Interventions | Recovery | Notes |
|---|---|---:|---:|---:|---|
| C0 Direct Mature | PENDING | PENDING | PENDING | PENDING | first baseline |
| P1 GPT / Work | PENDING | PENDING | PENDING | PENDING | primary intelligent path |
| P2 Work + Codex | PENDING | PENDING | PENDING | PENDING | Codex assessed, not assumed |
| B1 Manus 2.0 | PENDING | PENDING | PENDING | PENDING | benchmark only |

## 当前极限值

Reality 完成前：

```ini
T_DIRECT_MATURE_REF_CASE_001=NOT_MEASURED
T_VALID_WORK_CASE_001=NOT_MEASURED
T_VALID_WORK_CODEX_CASE_001=NOT_MEASURED
T_REF_MANUS_CASE_001=NOT_MEASURED
T_REAL_PHYSICAL_STAR_CASE_001=NOT_MEASURED
```

不得用旧的失效 VALID 时间填充。
