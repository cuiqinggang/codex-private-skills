# 本地 H3 已验证基线与差分恢复，第1版
日期：2026-10-16。方法按用户指定《三人行》V2 C002；Windows桥V7，C优先、A暂停。
状态：原厨房同条件生成成功基线已保存；原片同画质400秒、商业验收及物理极限均未通过。

## 可复用的真实 GOOD
直接读取 ../assets/h3-kitchen-warm-good-20261016.json，保留其实际节点连线和全部参数。它是历史合同，不得重发其中已有prompt_id。
环境：RTX2080Ti22528MiB、RAM32GB；torch2.9.1+cu130；ComfyUI commit 8a33128f2f8c5585c57486c07de481241e70a39c。
模型：W4A8 mixed、Qwen3VL4B FP8 scaled、ClipProj krea2、dynamic cuda:0；视频VAE fp16、音频VAE fp32；Turbo4 LoRA强度1；simple/res_multistep、steps4、denoise1；sigma shift视频12/音频3。
固定640×352、124帧、24FPS、原生音频。启动保留reserve-vram2.5、vram-headroom0.5、disable-pinned-memory；仅ClipProj自定义节点。
项目 C:/AI/MiniMax-H3/projects/H3-MINIMAL-20261015；服务127.0.0.1:8196。资源归属和空队列须现场核对。

|样本|服务端秒|客户端秒|缓存边界|prompt_id|
|---|---:|---:|---|---|
|厨房首次124帧|567.177|571.565|模型节点已缓存，条件重算；不是完整冷启动|acb25cf9-3b9f-4151-ae63-b7dc9300bd41|
|厨房连续1|274.657|275.382|条件节点6命中，seed3014重新采样|6cee62e4-45db-4d75-92c3-c66677c8f82d|
|厨房连续2|323.263|325.528|条件节点6命中，seed3015重新采样|5c0b35b6-963a-4a5a-bff2-d32c06698152|

3/3视频音频解码成功；12帧及全部124帧缩略图审查通过；没有全尺寸完整播放和听审，不能升级为跨场景商业质量认证。热运行平均298.960秒；全部三段平均388.366秒。生成时间不包含研究、审查交付，不能冒充T_VALID。
MP4 SHA256依序：34133acf0fcd5022594be39798efca1139ab9af0521bcfb5956895f332f79369；cd8027864d49d6491debaa323e633d6e0aee5379bd98cef439aa7dc2fb954e53；68caf22c60b1c8fb7ebfb53066ab621e411a5dd5175fb5a2b6e281761d6ba597。
原证据：仓库 workspace/H3-MINIMAL-20261015/FREEZE-124F-WARM-RESULT.md；本机各样本目录contract/history/result及benchmark-summary.json。

## 复用步骤
1. 先核对当前任务的图片、提示词、尺寸、帧数、模型和质量要求；不同任务不得直接继承旧速度或合格结论。
2. 同一服务、单卡串行；同条件批次保持图片和提示词等上游参数不变，只按合同更换种子，使用新prompt_id和唯一输出前缀。首段条件计算计入批次成本。
3. 由ComfyUI原生缓存处理复用，不把旧厨房条件强行用于新人物图片。核对history中的execution_cached及新采样、实际新MP4。
4. 现有benchmark_warm.py有暂停门，先遵守GPU-BASELINE-LOCK.json；本技能保存不授权绕锁或自动重跑。已完成prompt不得重发。
5. 没有资源压力时保留服务/条件缓存；资源异常时优先恢复电脑响应。官方/free后必须标记模型与条件需重建，不能继续称热基准。
6. 对新场景先冻结完整质量合同和整体方案；不以降低尺寸、减帧、减步数冒充同质量提速。

## 已核实 GOOD/BAD 差分
对厨房274.657秒真实contract与原片640×352的838.265秒contract逐字段比较：只有节点6.prompt、节点20.image、节点10.noise_seed、节点15.filename_prefix不同。模型、CUDA、dynamic、采样器、4步、尺寸和124帧相同。
第一项具有条件计算意义的差异是输入图和提示词改变；旧条件缓存不能复用。种子和输出名用于新候选/保存，不解释条件缓存失效。
这证明不是整个模型路线换成CPU，也没有证据证明原厨房同条件热路径已经坏掉。它不能解释838秒中每个阶段的全部差额；输入复杂度、模型搬运、资源压力各自占比尚未知。
原片1024×576为1473.885秒，像素数为640×352的约2.618倍，且条件不同，不能直接与274.657秒热路径比较。
旧H3-P1的288.281990秒是另一个“正面挥手说你好”VALID合同、12步及独立验收，不与本Turbo4厨房或原片合并。

## streaming失败证据与纠正规则
R1只改dynamic→streaming，并在/free后从无条件缓存运行。prompt fc8098a9-4259-4aca-8b8b-66b07aaf69bc。
节点1约37.096秒，约4999MB编码器完整加载cuda:0；节点6约39.13秒开始。180秒无进度事件触发定向中断，服务器296.731秒确认中断，无成片、未进入采样。最终队列空。
内存64–67%左右仍慢，故89%内存不是唯一解释；低GPU利用率不等同CPU推理。
无进度事件不证明死锁；此次中断不能证明自然完成时间或streaming必然无效。不得将该候选升级为默认成熟路线。
失败记录：workspace/H3-MINIMAL-20261015/STREAMING-R1-RESULT-20261016.md。
后续先检查节点6内部tokenize、视觉/文本编码、VAE编码各阶段；复用成熟观测方式，Freeze后一次完整验证。没有分段证据前，不再用猜测改加载方式或无事件时长宣称找准根因。
当前原片任务：ROOT_CAUSE_PARTIAL；VIRTUAL_MATURE=NO；TARGET_400S=NOT_PASSED；PHYSICAL_LIMIT=UNKNOWN。
