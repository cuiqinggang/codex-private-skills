# FirstBlockCache Safe 非生成准入冻结 2026-10-17
方法：三人行第3版；C通道；不提交GPU推理。
## 源码固定
固定公开代码 d474755360cc1784df1b7c933ca28195e55e3445（v1.1.1）；仓库 duckyshell/ComfyUI-MiniMaxH3-FirstBlockCache。
本机隔离目录：C:\AI\MiniMax-H3\projects\H3-MINIMAL-20261015\isolated-plugins\ComfyUI-MiniMaxH3-FirstBlockCache
nodes.py SHA256=F81296B76585AA287D820E9A4B9C69CBF738D757391605E6CFAF9F28247AE53A。
项目custom_nodes中的同名Junction指向隔离目录，无源码修改，无依赖安装/模型下载。
## 非生成准入证据
独立8197 ComfyUI服务使用只含ClipProj、Star7 FP16加载器、FirstBlockCache的插件白名单；显存保护--reserve-vram 2.5、--vram-headroom 0.5、--disable-pinned-memory不变。专用数据库sqlite:///:memory:，与原8196服务隔离。
/object_info/ApplyMiniMaxH3FirstBlockCache注册PASS；/queue运行及待执行均空；独立服务日志无数据库锁错误。
本机 ComfyUI model_patcher存在set_model_patch_replace/add_wrapper_with_key，原生H3的50个double_block替换入口已确认。
通过模拟原生模型的无GPU Python测试：H3 Safe预设阈值0.08成功安装50个块补丁及OUTER_SAMPLE/DIFFUSION_MODEL两个包装器，MOCK_PATCH_PASS，CUDA推理次数0。模拟对象不能代替真实权重加载、真实模型实例的补丁执行。
缓存重置：源码在采样开始/结束reset；形状/dtype/device不符或sigma逆转清理；每轮首块仍计算，最多连续命中2次；Safe temporal_guard默认False，剩余视频局部画质漂移风险须通过真实质量门。
## 冻结决策
INSTALL_PASS / REGISTRATION_PASS / MOCK_PATCH_PASS / DB_ISOLATION_PASS / NO_GENERATION_PASS。
REAL_MODEL_PATCH_AND_VRAM_PEAK=NOT_VERIFIED。并无任何新增高清图片生成，也没有实际缓存命中/采样提速证据。
此前GPU占用约21GB/22.5GB，单凭当前空队列不足以授权真实生成。下一次五帧Reality前必须先确认所有8196/8197及其他GPU任务归属、GPU显存剩余空间、系统RAM、运行队列与新缓存额外显存，避免对现有服务造成影响；不得随意杀进程或停用代理。
准入冻结为 CONDITIONAL_GO：非生成接口准入PASS，GPU现实生成暂不执行；仅在资源预算、模型补丁真实实例、守护与安全保护通过后允许独立一次5张1024x576、20步、seed3013真实验收。否则NO_GO。不得宣称FirstBlockCache比R2快或质量等同。
