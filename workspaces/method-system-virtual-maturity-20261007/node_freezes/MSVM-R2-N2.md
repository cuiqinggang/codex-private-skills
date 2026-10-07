# NODE_FREEZE
NODE_FREEZE_ID=MSVM-R2-N2
TASK_ID=METHOD-SYSTEM-VIRTUAL-MATURITY-20261007
PARENT_FREEZE_VERSION=3
NODE_GOAL=成熟最终媒体有效性与发布合同
STATUS=PASS
VIRTUAL_LOOP=COMPLETE
STOP_GATE=PASS

## 冻结方案
- 最终产物必须是新鲜MP4，含video+audio，能够正常播放。
- 优先H.264/AVC + AAC；仅容器存在、仅音频、仅视频、HEVC无音频均不算FINAL_VALID。
- 所有候选必须先分类；允许AV_COMPLETE，或VIDEO_ONLY+AUDIO_ONLY明确配对后无损/最小合并。
- staging完成后由独立ffprobe验证，再atomic publish到桌面。
- verifier失败时不得把产物发布为成功。
