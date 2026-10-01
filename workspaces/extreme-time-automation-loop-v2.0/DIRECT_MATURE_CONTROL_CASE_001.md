# C0 Direct Mature Control｜Benchmark Case 001

```ini
TASK_ID=ETAL-v2.0-CASE001-C0
CASE_ID=ETAL-v2.0-CASE-001
ROLE=PHYSICAL_EXECUTION_REFERENCE
PATH=DIRECT_FINAL_MATURE_SOLUTION
OBJECTIVE=MEASURE_T_DIRECT_MATURE_REF_CASE_001
```

## 作用

C0 不测 GPT、Codex 或 Agent 智能。

它只回答：

> “已经知道最终成熟方案以后，这道现实任务本体在当前环境中实际最快能跑到什么量级？”

因此 C0 是物理执行参考，不参加智能主链选型。

## 默认冻结样本

优先使用历史已验证样本：

```text
URL=https://v.douyin.com/kvcOhIpTbkg/
AWEME_ID=7689648259010235663
```

如果该样本当前失效：
- 自动换一条当前有效样本；
- 记录新的 URL / AWEME_ID；
- 本轮 P1/P2/B1 全部使用同一新样本；
- 旧轮不与新轮直接比较。

## C0 起点

为了只测成熟执行链，C0 的物理参考边界是：

```text
C0_T0 =
冻结样本已经进入成熟方案所要求的正式输入位置
（例如剪贴板已经是该分享链接），
随后正式入口被触发的时刻。
```

## C0 终点

```text
C0_T1 =
目标 MP4 已在桌面真实存在，
并且机器 verifier 已确认：
图像正常 + 音频存在/可播放 + 视频完整 + 无人工浏览器/media交接。
```

## VALID

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

## R1 测量

第一轮先追求最快获得可信参考：

```text
1 functional run
→ 若 PASS
→ 3 measured valid runs
```

记录：
- MIN
- P50
- MAX

定义：

```text
T_DIRECT_MATURE_REF_CASE_001 = MIN(valid measured runs)
```

如果 Reality 波动大或后续竞争结果接近，再把认证扩展到更多轮次。

## 重要

历史 Reality 02 的约 25.073 s 和 Reality 03 的约 153.098 s 均不能直接填入本基线，因为后续最终用户 VALID 曾因音频 / 播放问题重新打开。

必须以最终完成版重新实测。
