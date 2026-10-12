# 全帧真实源图视频任务模板

TASK_ID=<任务标识>
SKILL_VERSION=2.0.0-method
AUTHORITY_PATH=skills/video-extreme-time-engine/versions/codex-h3-v2.0
SPEC_STATUS=<准备/本次冻结>
REALITY_STATUS=PENDING
FINAL_VALID=NO

## 路径和恢复

C 正式工作区：<绝对路径>；V1 对照：<绝对路径，只读>；原图：<source_frames>；派生编码输入：<encoding_frames>；失败候选：<attempts>；日志：<logs>；候选与最终视频：<video>。
已有资产实际核对：<清单/尺寸/来源/哈希/读取记录>。C 正式源缺失时 BLOCKED_C_SOURCE_MISSING，H/K 不扫描、不备份。

## 商业规格

目标：<场景与质量>；主体/道具数量：<逐项固定>；相机与光线：<固定>；动作：<统一轨迹>。
N=56；FPS=24；T=N/FPS=2.333333 秒；源图 PNG，frame_001.png–frame_056.png；编码尺寸=864×480；编码 H.264 / AAC。
原图实际尺寸：<实际读取>；尺寸处理：<不需要/统一处理方法>；原图到派生映射：<路径>。

## 接口、环境与冻结

Codex 实际执行方式：<调用>；生图/编辑工具：<真实调用路径>；模型：<实查值或 NOT_EXPOSED>；双参考输入已验证：<证据>；FFmpeg 版本：<实际>；H3：<NOT_RUN/NOT_AVAILABLE/已验证接口>；音频来源与工具：<实际>。
首帧合格后固定身份参考：<路径与哈希>；上一合格帧：<动态引用规则>；轨迹文件：<路径>。
56 帧动作编排与冻结参数：<轨迹/提示词/合同版本/哈希/冻结时间>。ROI 与精确标签门禁保持暂停。

## 合同与证据

依照 METHOD_V2、FRAME_CONTINUITY、ACCEPTANCE 与 FAILURE_RECOVERY。每次调用记录真实来源、两张输入参考、提示词、参数/NOT_EXPOSED、输出原图、时间、SHA-256、错误及验收。
逐帧 PASS / REVISE / REJECT；失败当前帧不向后传递。56 张全部来源与连续性 PASS 才开启正式 A 编码。
禁止复制/改名/元数据/插帧伪装，禁止重复帧或生成式重绘冒充 A 模式。H3 独立保留候选，未跑写 NOT_RUN。

## 验收负责人及工具能力

逐帧看图：<实际验收者/方式>；24 FPS 真实播放：<实际可用方式>；声音实际听检：<实际可用方式>；商业整体验收：<实际执行者>。
任何能力未可用须写 NOT_DONE/BLOCKED；不得把技术数字当作已经观看或听检。最终只有 TECHNICAL / VISUAL / AUDIO、播放、听检及商业质量均实证通过才 FINAL_VALID=YES。

## 计时与收尾

任务接受：<时区时间>；各帧调用与返工、派生处理、编码、音频、验收计时：<日志>；最后必要验收通过时间：<通过后填写>。
输出 FINAL_TEST_RESULT.md、文件校验清单、最近使用记录、GitHub 写入与回读证据。真实耗时记录不启用暂停的 ROI 计算。旧结果、失败候选、工具与模型保持。
