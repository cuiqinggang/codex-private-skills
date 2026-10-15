# H3 模型创建与 LoRA 临时内存审查
日期：2026-10-16。仅只读源码、safetensors 文件头和既有遥测；未启动生成、未修改服务或原配置。

## 结论
存在具体改进空间，但尚无已证明更快的完整新方案。首要定位范围是采样准备交接和逐层 LoRA 临时张量，而非凭文件大小猜测、再关动态加载或再开全局锁页。

## 新证据
1. 实际独立 FP16 插件 nodes.py 406-434 调用原生 state_dict loader，预选 FP16 operations，非加载完整 BF16 后再复制整套 FP16。model_patcher.py 430-460 的普通 clone 共享 model 和备份；只有 force_deepcopy / disable_dynamic 委托等特定分支重新创建。不能按 clone 次数算大模型副本。
2. utils.py 96-155 的 AIMDO safetensors loader 用 mmap/frombuffer；前缀替换和 model_base.py 358 的 pop 转移是引用/字典操作，不是张量深拷贝。
3. sd.py 2258 后 model.load_model_weights(assign=model_patcher.is_dynamic())。ops.py 495 的普通 lazy loader 在非 assign 时 clone，且 Windows torch.empty commit 有源码警告。但 W4A8 MixedPrecisionOps 用自定义 _load_quantized_module，权重按量化格式加载，不能把普通层复制规则套到全部 12.54 GB 模型上，也不能说已证明 R7 复制整套权重。
4. 文件头实读：主模型 12,540,858,008 bytes；LoRA 314,878,200 bytes，其中 BF16 张量 314,825,728 bytes；encoder 5,242,467,968 bytes。它们是磁盘/张量存储量，不等于进程峰值。
5. LoRA 共 416 张量、208 A/B 对。最大 fc1 B=[28672,r] A=[r,5376]，完整乘积 154,140,672 元素，FP16 294 MiB，FP32 588 MiB。weight_adapter/lora.py 268-283 明确先 mm 得到完整 lora_diff，再缩放、可能转换并加到 weight；因此低秩小文件也产生大矩阵临时内存。208 对的展开量不能相加作为并发峰值。
6. 动态 LowVramPatch 使用 weight.dtype 计算；普通 patch_weight_to_device 有独立 dtype 选择，calculate_weight 默认 intermediate_dtype FP32。不能宣称全部合并都在 CPU 或全部 FP32。
7. ops.py 293-332 对非 resident 权重做反量化、LoRA、重新量化，签名有效时写回 resident；已有复用机制。R5 chunk 私有快照是单次 QKV/MLP 调用内复用，并非永久全模型缓存；直接再加全模型缓存可能扩大峰值。
8. R7 telemetry.json 实读：视频 VAE 加载 RAM 从63.1%至89.3%；编码器阶段峰89.5%；条件阶段尾63.4%；主模型创建首63.9%、末77.8%；330.008秒78.9%；335.264秒进入采样准备已91.5%，GPU仍12011MiB；399.056秒99.0%。主模型创建与采样准备必须区分，VAE创建本身也有显著峰值。
9. 遥测只有整机 RAM/GPU，没有进程 private bytes、commit、硬缺页率和逐函数内存。无法将 RAM 增量唯一归因 LoRA 或声称已经确认换页耗时。

## 整套候选的选择
保留 R4 动态加载、禁锁页、原模型/LoRA/质量合同及成果。R5 的热态优势保留为候选；已有数值差异不能自动视为同质量。
优先可研究的计算改进：对标准、无 DoRA/reshape/自定义变换的 LoRA 按输出行分块 mm+原顺序缩放/转换/累加，只限制差值临时缓冲，不更换 LoRA、不一次常驻全模型。不应直接用 addmm/fused 替代并宣称数值等价；算术舍入和量化边界必须检查。
例如最大层按2048行，单个差值由294/588 MiB变为21/42 MiB（FP16/FP32）；这是该缓冲的算术上限，不是整机节省量，不能消除完整目标权重或保证速度更快。增加 kernel 次数可能更慢；若瓶颈在 CPU 卸载，此优化可能不触及主要问题。
生命周期改进：编码完成后避免无用 encoder/VAE 副本同主模型准备重叠，但普通 unload->CPU 不等于释放 RAM。必须保留后续解码需要的 VAE、热态复用以及其它项目，不能盲清整个缓存。
排除：全局关闭动态、全局锁页、全模型展开预合并、再建无界常驻缓存、仅改变缓存大小、用量化模型文件大小推导可用空间。

## 若进入实现/验证的准入
先在隔离实现中验证标准 LoRA 分块路径和 unsupported fallback，记录实际 CPU/GPU 分配设备、dtype、单层峰值、resident命中；避免全局替换共享 ComfyUI。
全流程测量必须同时包含模型创建、权重准备、条件、采样、解码、输出，不能只报低峰值或局部耗时。
必须先冻结独立资源守护：interrupt 后有界等待并核实终局；超时只清理本次明确PID/队列服务，不能让监控退出而重负载仍继续。
只有同输入、同质量、同计时条件完整跑完才比较：R4首次469.167秒，热172.128秒；R5首次490.504秒、热49.707秒。新方案尚未实现/实测，不能晋级或承诺省多少秒。

本轮产物：项目 audit_weight_headers.py、WEIGHT-MEMORY-HEADER-AUDIT.json；本审查报告。现有证据已足以淘汰盲改开关，但不足以判定各函数耗时份额；如需精确份额，必须补带逐函数资源记录的受保护诊断运行。
