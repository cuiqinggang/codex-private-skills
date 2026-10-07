# DOUYIN-ULTRA-DIRECT-V1 — R2 Reality Freeze

【抖音极速直下｜DOUYIN-ULTRA-DIRECT-V1-R2-REALITY｜04｜实】
状态机：100｜R1=DELTA_FROZEN｜R2=PASS_FROZEN｜EXACTLY_ONCE=PASS｜FINAL_VALID=YES
时间锚：FORMAL_START=2026-10-07T19:12:30.0243660+08:00｜CORE_START=2026-10-07T19:12:30.559857+08:00｜FINAL_VALID=2026-10-07T19:12:34.453102+08:00｜CORE_T_VALID=3,893.298ms｜ENTRY_TO_FINAL_VALID=4,428.736ms｜BASELINE=20,923.291ms

## 正式结论

FORMAL_REALITY_COUNT_R2=1
FORMAL_ENTRY_START_COUNT_R2=1
SECOND_R2_REALITY=NO
FINAL_VALID=YES

同一样本、同质量 VALID 下：
BASELINE_T_VALID=20,923.291ms
R2_ENTRY_TO_FINAL_VALID=4,428.736ms
OBSERVED_SAVING=16,494.555ms
OBSERVED_REDUCTION=78.833%

当前样本正式 T*=4,428.736ms。

## READY_STATE

用户已完成共同前置动作：
复制抖音分享文本/短链到剪贴板。

SESSION_READY_STATE=PASS
auth_reused=true

生产用户操作仍只有：
复制链接 → 双击桌面“抖音极速直下” → 自动完成。

## R2 现实阶段

clipboard_ms=0.639
parse_ms=2,628.234
auth_reused=true
download_ms=1,124.818
verify_ms=95.617
CORE_T_VALID=3,893.298ms

隐藏入口启动到 FINAL_VALID：
ENTRY_TO_FINAL_VALID=4,428.736ms

## 质量

selected_stream:
width=1920
height=1080
size_bytes=7,757,637
bitrate=2,909,022

URL order:
1. www.douyin.com
2. v5-dy-ov-experiment.zjcdn.com
3. v3-dy-o.zjcdn.com

actual winner:
chosen_host=www.douyin.com
download_candidate_index=0

## 最终文件

C:\Users\A\Desktop\douyin_7691904650921374885_20261007-191233.mp4

bytes=7,757,637
duration=21.333333
video=h264
audio=aac
resolution=1920x1080

独立 post-process ffprobe=PASS
desktop douyin_*.mp4 count：6 → 7

## 候选字节保护

Reality 前后完全一致：
run.py=a5f4894dc865032af96994acee64dbc549323ca0121b700e52fd0a7691a8f02d
run-hidden.vbs=fdc6dc587dd7278a22f9aeb1e6c4b82d48d6a5bfeccebcc2dcc47494b9abea33
SKILL.md=e31e2d3abd21df4e4d9ba29924d046f83387d92ce6677f2adcbfa004ae8a19a4
formal candidate entry=fdc6dc587dd7278a22f9aeb1e6c4b82d48d6a5bfeccebcc2dcc47494b9abea33

Reality 期间未改冻结候选。

## 入口比较最终结论

A. 桌面双击
- 同机直接启动；
- 没有模型/远程工具时间税；
- 作为 T* 主入口。

B. GPT 技能调用
- 共用同一 run.py；
- 用户只需复制链接后说“下载抖音”；
- 增加 ChatGPT 推理 + Remote Desktop 工具调用时间；
- 因此不宣称比桌面双击更快；
- 作为便利入口正式保留。

C. API 原生 MCP
- 仅解析/读取能力，不能独立把 MP4 写入 Windows 桌面；
- 不作为完整下载入口。

## 边界

本次 4.428736s 是当前同一样本、当前网络/CDN/session READY_STATE 下的正式 Reality 结果，不保证每条视频都固定为该数值。
新视频会受到解析、网络、文件大小和 CDN 波动影响。
主路失败时自动回退既有成熟本地下载器，用户无需改操作。

## 发布

允许：
- 把冻结 core 设为桌面正式入口；
- 发布 skills/douyin-ultra-direct 技能包；
- 技能包与桌面入口共用同一核心。

FINAL_VALID=YES