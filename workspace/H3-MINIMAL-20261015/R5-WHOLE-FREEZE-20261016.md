# H3 R5 整套执行冻结
2026-10-16；基线R4首次469.167秒/热态172.128秒。只验证厨房640×352、124帧、24FPS、Turbo4、原音频合同，不认证原片高清效果或物理极限。
整体分析见skills/video-extreme-time-engine/references/H3_WHOLE_ROUTE_R5.md；本冻结补全最后LoRA准入结论。
固定代码：chunk-star7 2.18.7@e03ee508dd9aedf6189d3f31d063691909f5aced；保留独立FP16 2.0.14。源码_linear_can_reuse_weights允许标准ComfyUI权重补丁；CastBiasWeightContext准备后复制私有权重，复用不绕过标准LoRA。外部forward替换则回退。原生W4A8命中不是成功前提；禁止预先计入其收益。
只新增MiniMaxH3ActivationChunkStar7在LoRA之后，Guider/Scheduler均连接新节点：RoPE8192、MLP4096、QKV4096、out_proj4096兼容字段、reuse_mlp_weights=true、attention_backend=comfy_kitchen_int8、auto_halve_on_oom=true、disable_dynamic_prefetch=off、verbose=true。沿用上游20–24GB成熟起点，不运行中试参；发生自动减块要记录，不能隐瞒。
其余输入、模型、LoRA、sigma、sampler、步数、VAE、音轨、输出规格与资源策略不变。不安装无关依赖升级、不使用稀疏/跳算/超分/修脸/预览。已有功能模块导入通过才启动候选。
整套流程：原生输入及条件缓存→既有FP16主模型与LoRA→CK分块和权重复用→原生音视频VAE→原编码与一次视频解码检查。首次与热态分别计时，其他候选已在整体分析排除。
测试是一批两情景：PREP seed3013从重启服务无节点缓存开始；成功后MEASURE seed3014在同服务缓存有效时运行。每情景一个唯一prompt_id；禁止重发。采样/解码节点、事件、5秒GPU/RAM记录，服务端/客户端/交付前解码时间分列。900秒单任务保护预算，RAM94或RAM88且GPU<20持续30秒定向中断，错误即对账，不添加新参数续跑。
质量初验与R4相同：全124帧解码、12抽帧及全部缩略图、音轨解码；追加音频有限值检测。该初验不是完整听审或像素等价认证。
晋级：同合同完整生成时间优于相应R4且质量/资源无退化才记录改进；若首次/热态结论不同必须分列，不能统一宣称最优。单样本不证明稳定性。未胜出恢复R4服务，保留全部候选证据。
R4原脚本/流程/插件和文件哈希不改。切服务先检查空队列及8196实际PID归属；候选独立日志。结束清除本次授权、官方/free释放模型，桌面输出结果并持久化回读。
状态：设计审查完成；执行前还需固定源码/DLL完整性和节点注册准入通过。不是VIRTUAL_MATURE极限认证。
