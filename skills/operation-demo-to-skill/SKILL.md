---
name: operation-demo-to-skill
description: 《操作演示自动技能化》第2版。GPT先判断是否需要演示；需要时在Windows同步记录操作事件与麦克风口述，融合目标解释后以成熟方案优化并生成可验证自动化技能。用户说看我操作、启动双路录制、演示转技能时使用。
metadata:
  version: "2"
  display_name: "《操作演示自动技能化》第2版"
  release_state: "PILOT_DUAL_CAPTURE_TESTED"
---
# 《操作演示自动技能化》第2版

GPT 是规划、意图理解和最终验收主控；Codex 仅在工程适配、脚本和执行复现更合适时调用。不要预设 Codex 更快，也不把人工做法当作最优实现。GPT 先判断是否可直接用成熟 API/CLI/技能达成目标，无需录制则不录；否则启动“操作事件 + 麦克风口述”同步录制。单独已有视频可复用 `codex-video-to-usable-skill-loop`。

## 现有成熟资源与入口

- 录制源：`C:\AI\record-and-replay-evaluation\SKILL.md`（开源 record-and-replay；不得重造事件录制器）。
- 声音：Windows FFmpeg 8.1.1 的 DirectShow 输入 `麦克风 (Web Camera)`，优先使用现有系统设备；视频或声音只是解释意图的补充证据。
- 第2版**薄适配**：`C:\AI\operation-demo-to-skill-v2\capture.mjs`，只组合现有 FFmpeg 和 upstream `desktop-record.mjs` 的启动/停止，记录 UTC 开始/结束及各自产物，不创建新通用调度器。
- Codex `skill-creator` 生成 SKILL.md、按需最小脚本、验收证据；GPT 从口述“为什么”与事件“实际发生什么”推断真正目标。当前尚无自动语音转写服务的已认证接口，不得假装口述已经自动被理解。
- 网络权威方法：`cuiqinggang/codex-private-skills/skills/artificial-single-page-extreme-time-engine/START_HERE.md`，每次读取当时实际路由/版本。先成熟复用门、已有GOOD完整现实基线、最长关键路径/物理限制、≤3强成熟候选、连续虚拟成熟、STOP_GATE、Freeze，之后一次最终 Reality；缺少同边界有效时间则标 UNKNOWN，不宣布极限最优。

## 人工演示时的最短用户入口

1. 用户向 GPT 描述业务目标。GPT 先判断成熟方案是否可以直接完成。若需要演示，明确本轮授权开始后，经 Windows 桥调用：
   `node C:\AI\operation-demo-to-skill-v2\capture.mjs start <唯一英文任务代号>`
2. 只有返回 `status=recording` 后才通知用户开始。用户正常操作，同时对麦克风讲解每步目的、输入条件、为什么点击及期待什么结果；不需要额外手机录制。录制器并非 ChatGPT 原生录制功能。
3. 用户说“结束”后调用：
   `node C:\AI\operation-demo-to-skill-v2\capture.mjs stop <同一任务代号>`
   回读 `result.json`、操作事件/摘要和 `narration-final.wav`。录音与电脑事件以 UTC 开始时间对齐，精确词句和动作映射仍需转写和人工或模型检查，不能把仅有音频文件当成已识别口述。
4. GPT 对目标和方法去冗余、提炼参数与 VALID 判据，比较成熟候选，按引擎完整时间及故障恢复成熟；Codex 仅按需生成脚本/Skill并核验，验收通过后保存可发现的技能和证据。不要把录制过程机械坐标重放视为唯一实现。

## 安全和真实认证边界

桌面记录包含按键/截图，麦克风录音也可能包含语音信息。仅当用户明确开始时录制，在本机保管原始证据，禁止上传原始录制到共同库。保持 FlClash、代理及已登录浏览器不变；不得未经授权执行外部业务发送。当前合成事件 + 合成音频双路 start/stop 已通过，麦克风独立采样成功；真实人员完整演示、语音转写、GPT 与 Codex 竞争/组合时间比较、极限时间认证仍未完成。状态 `PILOT`，不是 `FINAL_VALID`。