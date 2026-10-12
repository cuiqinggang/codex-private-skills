---
name: codex-h3-video-production-v2
description: 在既有视频极限短时间引擎血缘中执行 Codex+H3 V2.0 全帧真实源图制作。适用于用户明确要求逐帧真实生成、首帧与上一合格帧继承、连续性验收以及原帧序列无插帧成片的短视频；不适用于普通剪辑或仅需稀疏关键帧的视频。
metadata:
  version: "2.0.0-method"
  status: METHOD_SPEC_READY_REALITY_PENDING
  parent: video-extreme-time-engine
  authority-path: skills/video-extreme-time-engine/versions/codex-h3-v2.0
---

# Codex+H3 视频制作技能包 V2.0

本版本是全帧源图连续制作规范。56 张真实生成源图对应 56 帧视频，以 24 FPS 编码，视频时长为 56/24 = 2.333333 秒。现实生产认证仍待通过；包文件写入、静态检查通过或存在候选视频均不能替代现实认证。

权威血缘为 `skills/video-extreme-time-engine/`。父包 v0.5 的 `FREEZE.md`、`CASE-H3-P1.md` 与历史证据保持原件；本版本不继承其 VALID 或 T*。远端已经存在的 `CODEX_H3_V2_FULL_FRAME.md` 是本次方法来源，新增版本目录补齐合同、模板与复用入口，不建立竞争权威包。

## 触发与最短开工检查

触发词：Codex+H3 V2.0、全帧源图、56 张真实源图、连续逐帧生图、Reality Test 02、无插帧保真编码。下一次相同任务先读本入口、[VERSION.md](VERSION.md)、[最近使用记录](RECENT_USE_LOG.md)，再按当前失败入口读取必要合同。

开工时复用当前 C 盘正式源及现有 Codex、生图/参考编辑接口、FFmpeg、音频工具。按 Knowledge Brain 的 INDEX → ROUTING_MAP → 一个相关分类索引 → Top-K 定向资产检查已有方法，记录读取路径。禁止扫描 H/K、修改代理、重建成熟工具链或重复下载模型。若 C 正式源缺失，记 `BLOCKED_C_SOURCE_MISSING`，不得回退 H/K。ROI 与精确标签门禁当前暂停，不因父包或历史模板自动重启。

接口检查必须确认真实图像模型调用及双参考编辑能力；记录模型标识、调用 ID、参数、执行时间与来源，接口没有暴露的字段写 `NOT_EXPOSED`。Codex CLI 的文本回复、返回成功码、文件名或随机哈希不能证明实际生图。

## 执行顺序与硬门禁

1. 恢复并只读核对 V1 旧结果；新结果独立存放。V1 的 8 张源图覆盖 56 帧方案废止为 V2 正式生产路线。
2. 固定商业规格、56 帧编号和统一动作轨迹；冻结本次执行参数与验收条件，并保留合同版本及哈希。
3. Codex 调用真实图像生成能力制作首帧。每帧后续调用都必须将首帧与上一张合格源图真实输入模型。相邻依赖链串行，独立的文件检查/音频准备可并行。
4. 逐帧验收主体、道具、场景、光照、轨迹和摄影品质；记录 PASS / REVISE / REJECT。当前帧失败则修复它并复验，禁止把失败帧传给下一帧。
5. 只有 56 张逐帧来源证据完整、每帧 PASS、连续性通过，才开启正式 A 模式编码。源图缺失、重复伪装、来源未证或任何 REVISE / REJECT 都使编码门禁关闭。
6. FFmpeg 按编号原序列无插帧编码，处理合法可听且配合动作的音轨。必要尺寸/色彩转换保留原图与派生映射，不计为新的模型生成。
7. 技术、画面、声音独立验收；实际逐帧观看和播放听检未发生时写 NOT_DONE。只有所有必要条件有实证通过，才写 `FINAL_VALID=YES`。
8. H3 是按需独立候选；只有实际接口支持且确有必要才运行，保留 A 模式原片。H3 输出不能自动认定保留全部源帧。
9. 将真实生成、返工、处理、编码、验收的耗时及失败证据写入 [验收模板](templates/FINAL_TEST_RESULT.md) 与最近使用记录。技术结果为准，不为了结束任务修改判定。

## 渐进读取路由

| 当前工作 | 必要文件 |
| --- | --- |
| 全帧生成、尺寸处理、编码 | [METHOD_V2.md](references/METHOD_V2.md) |
| 动作编排、逐帧与相邻帧验收 | [FRAME_CONTINUITY.md](references/FRAME_CONTINUITY.md) |
| 最终指标、播放、音频和商业判定 | [ACCEPTANCE.md](references/ACCEPTANCE.md) |
| 生成失败、手部漂移、冻结或环境阻塞 | [FAILURE_RECOVERY.md](references/FAILURE_RECOVERY.md) |
| 新任务 | [PROJECT_BRIEF.md](templates/PROJECT_BRIEF.md) |
| 收尾与复用 | [FINAL_TEST_RESULT.md](templates/FINAL_TEST_RESULT.md)、[RECENT_USE_LOG.md](RECENT_USE_LOG.md) |

静态部署证据见 [验收页面](acceptance/index.html) 与 `acceptance/static_check.json`。本地包完成不等于 GitHub 持久化；只有远端实际写入、回读和提交记录齐全才报告远端升级完成。后续改变经过认证并冻结的文件时新增版本，禁止原地改动冻结原件。
