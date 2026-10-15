# H3 Streaming R1 实验合同｜2026-10-16
任务：H3_STREAMING_R1_20261016；方法三人行V2 C002，执行桥V7 C。
承接F001与ENCODER-LOADING-C001；用户本轮明确授权实际验证后再寻求极限时间。
虚拟审查：dynamic已观察到慢条件处理；resident长期占显存不选；选择现有ClipProj0.1.13 streaming整体加载后允许卸载。CUDA路径、模型、精度、原图、原提示词、seed3013、640×352/124帧、Turbo4保持。候选SHA26423809c7bd4dab63eb959ee4a9dbc62e26d99cf86a8343cc5dd77e62dacdb7；仅输出前缀换唯一任务名。
资源生命周期：编码器需约5GB权重及运行缓冲；插件先调用ComfyUI free_memory并force_full_load。编码后允许回RAM，不永久占GPU；主DiT继续原动态方式。当前系统RAM65.4%、可用11869945856字节，队列空。已/free清过模型及条件缓存，因此此轮为重载路径，不能与热条件缓存274秒等同，也不是与旧838秒严格同运行状态的因果A/B。
观测：使用已有aiohttp连接ComfyUI原生WebSocket，记录executing/progress/history；节点切换时刻给出近似节点墙钟，分辨率约1秒，不能称独立CUDA算子耗时。每5秒采样psutil与nvidia-smi，含观测开销。
保护预算（本次实验保护，不是性能标准或阈值寻优）：启动RAM>=80%不提交；运行RAM>=94%或RAM>=88%且GPU<20持续30秒、节点/进度180秒无变化、全程900秒任一满足，即向本prompt_id发送官方定向interrupt。中断响应并不等于执行已终止；通过history确认，60秒未确认则标INTERRUPT_PENDING并人工对账，绝不重发任务。
Exactly-once：独立submission.claim、intent、receipt；不自动重试提交。旧三个入口generation_allowed=false保持；只在锁中授权本任务。
验收：生成124帧、音视频解码、抽样画面与旧640对照；不得将低清诊断合格冒充原片质量合格。若成功且改善，再依据分段数据选择后续净收益候选，不立刻叠加未知优化，不承诺400秒或物理极限。结果不合格则保存失败证据并停止该候选。
状态：候选审查已完成，批准单次受控Reality；VIRTUAL_GLOBAL_OPTIMUM=UNKNOWN、PHYSICAL_LIMIT=UNKNOWN。
