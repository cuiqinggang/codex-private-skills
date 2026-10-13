# V3 候选｜现场审计、三路线虚拟成熟与 Reality 结果（2026-10-13）

TASK_ID=CODEX-H3-V3-COMMERCIAL-20261013
STATE=VIRTUAL_ROUTE_SELECTED / REALITY_READINESS_CHECKED / NO_NEW_H3_RENDER
SELECTED=A_CLOUD_H3_REF2VA
FINAL_VALID=NO
COMMERCIAL_QUALITY_PASS=UNKNOWN
LICENSE_CONFIRMED=NO
T_VALID_REAL=UNKNOWN
PHYSICAL_OPTIMUM=UNKNOWN
METHOD_PROMOTION=NO
PARENT_V2_UNCHANGED=YES

## 1. 官方资料与可用技能
- 模型发布：https://github.com/MiniMax-AI/MiniMax-H3 （原生音视频；4–15s；24fps；云端最高2K）。
- 官方通用可移植提示词技能：https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing （REF模式六段；BASE三段）。
- 官方品牌宣传/极简广告技能：https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/brand-promo-video-generator （该类技能依赖MiniMax Hub专用工具，不可在Codex直接调用；仅复用导演、镜头表、真实素材验收方法）。
- 官方云端CLI：https://github.com/MiniMax-AI/cli （MiniMax-H3 V2）。
- ComfyUI官方模板：https://docs.comfy.org/tutorials/video/minimax/minimax-h3 （原生T2V / I2V / R2V及多帧参考）。
- 本地商用许可证信息：https://support.comfy.org/articles/6065098425-minimax-commercial-licensing-who-needs-a-license-and-how-to-get-one；Comfy Cloud作品包含商业使用权，本地权重生成商业作品需要额外许可，其他平台应核对各自实际条款。

## 2. V2 正式基线回读（不是推测）
- 本人的共同工作区仓库 main 原权威：skills/video-extreme-time-engine/versions/codex-h3-v2.0/acceptance/reality-test-02-20261012/RESULT.md，状态 BLOCKED_PRECISE_LOCAL_TEMPORAL_EDIT，FINAL_VALID=NO。
- Windows正式结果：C:/AI/Polsia-Codex-20261011/outputs/codex-h3-v2-20261012/FINAL_TEST_RESULT.md。
- 正式C链001–003合格；第004帧真实尝试3次失败：前2次微步移动过大，第3次基本不动；004–056共53张缺失、正式56帧MP4未生成。
- Windows另一目录 C:/AI/Codex-H3-Video-V2 下虽有旧A/B阶段frame_004.png等文件，不是正式C链的第四张合格源图。
- 26个不同模型输出为A/B/C各轮真实尝试合计，不能充当26/56验收进度。旧B音轨单独听检过，不等于15秒新视频的音画合格。

## 3. 本轮Windows实际只读预检
- Windows执行桥可读本地 C:/AI/MiniMax-H3、V2旧工作区、正式C状态。
- 实际检测本机TCP端口8188/8193/8194都未监听；没有现成ComfyUI H3生成服务。
- 磁盘模型已安装：H3 fl2va/ref2va pruned INT8模型各19.53GiB，Qwen3VL编码器14.61GiB，视频VAE4.85GiB，音频VAE0.56GiB；存在Turbo LoRA。模型在盘不代表服务上线/商业许可已有。
- NVIDIA RTX 2080 Ti 22528MiB，总显存中当时已使用2423MiB；设备在线。
- 当前PowerShell会话未发现 MINIMAX_API_KEY/MINIMAX_API_TOKEN 环境变量；PATH无mmx命令。只说明本次会话未配置，不能推断用户浏览器账号或其他安全凭据不存在。
- 历史 H3-05 实际渲染107帧、864x480、24FPS、20步、4.458333秒视频，用时1743.805秒，技术解码PASS但人工视觉质量未被完整接受。另一5帧静态TE-Speed用时400.248秒，不能外推15秒生产速度或成功质量。
- 本轮未启动ComfyUI大型推理，未发起付费API任务、未消耗云生成额度、未产出或实际播放新的15秒H3成片。Reality仅为接口/资源/证据预检，不是生产验收。没有合法事实支持FINAL_VALID=YES。

## 4. 三路同合同虚拟成熟结论（非现实生成评分）
统一15秒厨房布料广告场景、16:9、24FPS、真实身份锚点、音画同步与商用权利；所有路线使用同一独立验收清单。 
A: 云端 H3 Ref2VA 可输入多参考，原生连续音视频，在线2K与商业交付较贴合；依赖实际账号额度、价格和用户授权，画质/速度未知。综合最优先，待现实验证。
B: 云端 H3 FL2VA 首尾帧控制，适用于稳定单镜头，但当前没有真实合格的15秒尾帧，须额外制作并验收；为次选。
C: 本地ComfyUI H3 R2V / Multiframe 参考，有模型与历史运行记录但当前服务离线，长片耗时、显存及本地商用许可负担；只有具备许可且现场资源评估正收益时备用。
旧V2全56张方法保留为特殊合同比较基线，在当前通用商业短片目标不选为默认。
结论：选择A作为冻结待Reality候选，B/C保留条件性回退，但不宣称已经制作商业片、速度提升或达到物理最优。

## 5. 下次正式Reality唯一合同
前置：经用户许可的官方H3云账号/API已有效连通、使用额度/实际费用明确、素材有合适权利；不得接触FlClash/代理、另开浏览器或把系统密钥写进仓库。详情见同目录 PRODUCTION_PROMPT.md。
输出：官方真实task_id、模型、提示词hash、图片引用SHA、任务创建/排队/生成/下载/验收时间，真实计费、15秒视频原件及SHA、声画逐段实际审查、商业授权记录。同一规格与V2真实基线对照，T_VALID计入等待与返工。不得用本地测试证明云端质量，或用静态预检替代生产Reality。按真实失败GOOD/BAD/FIRST_DELTA有限修复，三次同类失败冻结；只有完成可播放、有声、连贯、具有许可的真实成片后，FINAL_VALID才能从NO升级为YES。
