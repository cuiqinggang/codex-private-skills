# R9 参数、恢复与复用

## 原项目与实证

原项目C:/AI/TenYears-Animatic-20261030；候选R9/FINAL/HotMeal-R9-15s-Human-Review.mp4。
ComfyUI项目C:/AI/MiniMax-H3/projects/H3-MINIMAL-20261015，HTTP8197。核对服务所有权、object_info及队列，不照抄旧8195/8196。
H3 Python在C:/AI/MiniMax-H3/.venv/Scripts/python.exe，既有OpenCV环境在C:/AI/Visual-Art-Engine/envs/vision-core/Scripts/python.exe。
归档已执行脚本在assets/hotmeal-r9/scripts，冻结配置和证据在assets/hotmeal-r9/evidence；完整177项原声/视频见RELEASE-V3.json指向审核包。

| 项目 | 已执行实值 |
|---|---|
| 新A | 73帧/24fps/384×320，seed4021，首末帧及f24中间引导 |
| 新P | 39帧/24fps/384×320，seed4022，首末同一手机参考 |
| 保留B/C | R8原生完整视听73/175帧，不重投 |
| 文本编码 | qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors |
| 采样/缓存 | 20步，SAFE阈值0.08，完整节点以冻结workflow.json为准 |
| 预算 | A/P/B 15:00:000；C据真实16:37:579修正为30:00:000，不改变采样参数 |
| 本片资源 | RAM准入<90%，独立运行保护>=95%，不改其他项目 |
| 修复模型 | 官方RealESRGAN_x2plus.pth，67061725 bytes，SHA256 49fafd45f8fd7aa8d31ab2a22d14d91b536c34494a5cfe31eb5d89c2fa266abb |
| 文件 | 原生384×320修复至768×640，360帧/24fps/15秒，H.264 yuv420p、AAC48kHz |
| 混音 | 两遍响度目标-16 LUFS/truepeak≤-1dBTP；最终实测-16.01 LUFS/-3.93dBTP |

A原生prompt_id=8c44eeb3-57f0-42d3-8331-99c2285de3b2；P=593dc33c-1279-4101-afb1-394a332209d1。它们用于查询历史，不用于重提交。
时间线A[0..49]→P[0..38]→A[50..72]→B[0..72]→C[0..174]，完整360帧，语速1.0，不删接触帧。
生成耗时A04:52:109、P05:13:141；四段修复总批次02:37:910；不是T_VALID，也没有已证同质提速率。

## 已落地的原因修正

- 源资产手机与饭碗落点冲突：先改源布局、保留固定饭碗，再生成；不把端碗误动作只归罪提示词。
- 屏幕：既有OpenCV SIFT+RANSAC单应、内缩玻璃蒙版、逐帧贴固定源照片与文字。保留手/机身/运动，修复后再次合成屏幕；独立边缘复核。39/39有效，误差数字仅属本镜头，不推广任意素材。
- Unicode：历史P含U+FFFD，原配置不改；下一次用config-corrected-next-run.json并检验精确码点。本片通过合成固定文字，无需因此重新投GPU，不将乱码说成全部动作问题唯一原因。
- ASR：复用whispercpp-gpu/Release/whisper-cli.exe及ggml-large-v3.bin；模型SHA1 AD82BF6A9043CEED055076D0FD39F5F186FF8062。不能只查H3环境就说全机没ASR。PowerShell5.1旧包装将ffmpeg stderr当错误，改subprocess捕获，不改模型。
- 听审：两次完整音频判断认出“糟践”，孤立片段/Whisper分歧保留；联网审片会计费，技能写回不再调用。密钥只从既有安全环境读取，不包入值。
- F声音：A原生落碗约0.6—0.8秒，缺明确提示，补1.000秒起、长0.140秒的一次轻通知。B原生音瞬态与首次接触约差-3.3ms；不复用旧否决耳光声。
- 日志：JSONDecoder.raw_decode读取完整JSON对象，避免FFmpeg附加日志Extra data，不因此重做GPU生成。
- 审核器误判：整片工具反左右、漏击打；补帧工具虚构帧号/否认指饭；声音工具编造超片长/重复事件。保留报告并以真实帧/原音纠正，不盲采PASS。

## 接续与能力边界

仅升级技能：执行离线完整性核验，不生成视频。
原项目恢复：先读delivery-state、claim、history及最终SHA，已有结果只审/修对应失败工序，不能删claim重投。UNKNOWN先对账。
新项目复用：复制到新目录，明确变更项目路径、输入、模型、fps/时长和批准条件，先dry-run，不原地执行硬编码档案脚本。
R2八项及后续十三项几何检查为继承限定记录，不因R9升级重计新测。R8 C旧遥测断档仍是缺口。最终人审未发生，本片成功不等于全身物理碰撞、所有动作可靠控制、P0晋级或完整T_VALID提速认证。


## 快照优先级

接续以较后的RELEASE-V3.json、delivery-state.json及FINAL/technical-review.json为准。upstream-disposition.json的remaining及RESTORE/model-manifest.json的资产准备状态是较早快照，留作因果证据，不应据此重做已经完成的修复、声音或技术审核。审核ZIP不含模型权重、全部原项目或R8全部历史，不能宣称是独立重建安装包。
