---
name: operation-demo-to-skill
description: 《操作演示自动技能化》第3版。GPT先判断是否可直接完成；必要时复用成熟Windows事件录制和可选麦克风音频，提炼业务目的并生成、验收可复用技能。用户说演示操作、录制成技能、操作转自动化时使用。
metadata:
  version: "3"
  display_name: "《操作演示自动技能化》第3版"
  state: "MINIMAL_BASELINE_PASS_OPTIONAL_AUDIO_PILOT"
---
# 《操作演示自动技能化》第3版

## 唯一主轴
1. GPT明确任务目标、输入输出、VALID和权限，优先判断既有成熟API/CLI/Skill是否可以直接实现；可以则不录制。
2. 需要演示时，只调用已有 `C:\AI\record-and-replay-evaluation\SKILL.md`。Windows浏览器录制优先语义定位，桌面则记录原生操作事件与必要截图。录制完成先检查完整性，再调用现成摘要器。
3. GPT理解真实目的，并对照动作证据；使用现成 `skill-creator`，由 GPT 或按需 Codex 生成实际 `SKILL.md`。优先成熟 API/CLI 实现业务，不机械模仿鼠标坐标。关键目标含糊则报告 UNKNOWN。
4. 在独立合法测试目录按技能正式入口执行，校验正确输出、重复执行、失败恢复，保存原始证据位置、版本、SHA及同边界完整耗时。
5. 按网络权威 `cuiqinggang/codex-private-skills/skills/artificial-single-page-extreme-time-engine/START_HERE.md` 实行 GOOD 现实基线→最多三个成熟候选→连续虚拟成熟和完整时间→STOP_GATE→Freeze→一次最终 Reality。不可将自检耗时冒充 T_VALID 或最优认证。

## 可选麦克风
- 用户实际需要解释操作目的时，才额外启用已验证 Windows FFmpeg DirectShow 麦克风 `麦克风 (Web Camera)`。事件流是主记录；音频为可选补充，录音或转写失败不能使已经有效的基础技能无效。
- 本机已有 FFmpeg 8.1.1、faster-whisper 1.2.1及缓存语音模型。已验证真实麦克风短采集、合成英语语音转写，尚未验证真人中文同会话精确对齐。
- 旧版 `C:\AI\operation-demo-to-skill-v2\capture.mjs` 属实验性双路编排，不作为第3版生产默认入口。不得重造通用协调器。需要并录时复用成熟进程能力，保留实际起点与时间偏移，只有对齐验证通过才利用口述做语义判断。

## 已核实的本机证据
- v3最简合成录制+摘要：`C:\AI\record-and-replay-evaluation\evaluation-v1\evidence\v3-minimal-20261010\result.json`，PASS 2714.433ms。
- 既有实例技能实际生成两份UTF-8中文文件：`C:\AI\record-and-replay-evaluation\evaluation-v1\evidence\v3-file-result-20261010\manifest.json`，内容相同、哈希相同。
- 录音真实短采集和合成语音转写证据仍保存v2，不把它们冒充本次同会话真人测试。新录制自动技能生成、三模式同边界竞速、完整虚拟时间最优仍为 UNKNOWN。
- 网络权威方法优先、本地执行副本次之；本地私有录制和原始音频不得上传GitHub。保持代理、浏览器原状态及已授权权限边界。

## 使用入口
用户说“启动第3版演示技能化，先判断是否需要录制”。GPT先执行复用门，必要时确认独立录制环境、再启动录制并等用户完成。完成后主动分析、生成技能、执行验收及优化，不把工具启动当作任务完成。

当前状态：`MINIMAL_PATH_PASS / OPTIONAL_AUDIO_TESTED_SEPARATELY / VIRTUAL_MATURE=NO / FINAL_VALID=NO`。