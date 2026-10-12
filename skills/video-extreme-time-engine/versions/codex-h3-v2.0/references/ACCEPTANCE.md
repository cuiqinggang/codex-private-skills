# 完整现实验收合同

包的静态验证与作品现实验收独立。技术、画面、声音各自记 PASS / FAIL / NOT_DONE / BLOCKED，证据不足不得使用 PASS。正式目标 N=56、FPS=24、视频流时长 56/24 秒，目标编码尺寸 864×480。

## 源图门禁

逐帧模型调用、真实双参考输入、原图与派生关系完整；恰好 56 张正式源图、56 个逐帧 PASS、55 个相邻关系通过。原始生成数量、失败候选数量、接受数量分开报告。未完成源图门禁时不得正式编码，`FINAL_VALID=NO`。

## TECHNICAL_PASS

- 实际 MP4 存在、可完整解码，体积与内容合理；不能只靠扩展名或成功退出码。
- ffprobe/解码实际计数为 56 帧，视频帧率为 24/1，视频时长为 56/24 秒；比较容差与来源须明确。
- 视频 PTS 严格递增，相邻视频帧间隔为 1/24 秒（允许封装 time_base 的量化误差），首帧从预期起点开始，无跳跃、丢帧、额外帧或坏帧。
- 源图 001–056 与视频顺序一对一。压缩或色彩转换后的像素不应要求哈希完全相同；通过解码图对齐、图像差异及目视核对证明映射，保存对照证据。
- H.264 / AAC 兼容性、尺寸与色彩转换如实记录；AAC 尾部 padding 与容器时长独立解释，不能靠额外视频重复帧补齐。
- 视频完整解码和音频实际解码成功，无损坏日志。

## VISUAL_PASS

- 对实际成片的 56 帧逐帧看图：手部、道具、布料、透明玻璃、光线、背景和动作全过程通过。
- 检查精确重复、近重复、冻结段、运动反向、闪烁与抖动。冻结检测只定位可疑区间，须区分正常停顿、动作不足和播放器/编码异常。
- 实际按 24 FPS 播放观看，开始/结束完整、动作自然、无明显卡顿、无破坏商业质量的变形或漂移。
- 联系表、ffmpeg freezedetect、差分或光流数值都不能替代实际播放观感。没有播放能力则记录 `PLAYBACK_REVIEW=NOT_DONE`，画面最终验收未完成。

## AUDIO_PASS

- 声音有合法可追踪来源，真实存在并完整解码。
- 检查实际电平、异常静音、爆音/削波与杂音；AAC 音轨存在不能代替声音质量通过。
- 声音内容配合厨房环境及布料动作；实际播放听检能听见，音画时序协调。
- 仅有峰值/RMS 数字时可报告技术可听候选，不能报告已经听检。无人或无工具实际听到声音时 `LISTEN_REVIEW=NOT_DONE`。

## 判定

```text
FRAME_GATE = ALL_56_SOURCE_PROVEN_AND_REVIEWED_PASS
TECHNICAL_PASS = YES/NO/NOT_DONE/BLOCKED
VISUAL_PASS = YES/NO/NOT_DONE/BLOCKED
AUDIO_PASS = YES/NO/NOT_DONE/BLOCKED
PLAYBACK_REVIEW = PASS/FAIL/NOT_DONE
LISTEN_REVIEW = PASS/FAIL/NOT_DONE
COMMERCIAL_REVIEW = PASS/FAIL/NOT_DONE
FINAL_VALID = YES only when every required condition has evidence and PASS
```

H3 未执行写 `NOT_RUN`，不填想象的对照结果。实际总耗时从接受任务到最后必要条件通过记录；尚未通过时记录已耗时，不能用候选耗时冒充 T_VALID。与 V1 比较注明不同来源规格，不将 8 图方案认证直接继承为 56 图方案认证。不计算暂停的 ROI、收益倍数或回收期。

证据清单至少包括：真实模型调用与引用、56 个原图哈希、派生处理映射、逐帧验收、相邻连续性、编码命令和版本、ffprobe/完整解码/PTS、冻结与重复分析、实际播放审核记录、音频来源与检测、实际听检记录、最终文件清单及 `FINAL_TEST_RESULT.md`。未获取的证据显式列入未完成事项。
