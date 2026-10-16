# V3 R5高清五帧分块静态兼容审查（2026-10-17）
方法：《三人行》第3版；连接：V9.0的C通道。状态：STATIC_PASS / RUNTIME_NOT_VERIFIED / FINAL_VALID=NO。
## 已验证事实
本机原R2工作流1024×576、5帧、20步、seed3013、原生INT8 ConvRot；R5原工作流640×352、124帧、Turbo4、W4A8及Turbo LoRA。R5的分块节点MiniMaxH3ActivationChunkStar7 接收/输出MODEL；本机安装目录下存在节点源码，__init__.py包含映射加载。不能将原R5性能数字直接迁移。
通过C通道使用Python解析两个JSON，完成差分工作流结构检查：15节点、17处引用全部存在；只新增节点30并更改BasicGuider节点7、BasicScheduler节点9的model引用至30。节点30接受R2原SigmaShift节点3输出；不引入Turbo LoRA，不改变seed、20步、1024×576、5帧、原始INT8模型、条件编码、提示词、采样器、解码及输出。**这是图结构静态PASS，不代表插件成功初始化/运行/无损/提速。**
静态冻结文件：`C:\AI\MiniMax-H3\projects\H3-MINIMAL-20261015\V3-R2-R5-CHUNK-STATIC-CANDIDATE-NOT-RUN.json`。本地审查报告：`V3-R5-HD-COMPATIBILITY-FREEZE-20261017.md`。
R2历史总463.266秒，采样332.610秒(71.8%)；R3总555.985秒，采样438.782秒。既有5张×2照片规格与哈希PASS，缩放视觉检查R2略优但仍非完整原尺寸品质认证。历史R5 49.707秒/172.128秒是不同合同。
## 方案比较
A保持R2原生INT8：唯一已证明的同规格较快基线；非物理极限。
B R2+R5分块+comfy_kitchen_int8：图结构静态PASS；运行时节点注册、权重补丁、显存峰值、高清20步质量等价与真实端到端正净收益未证。分块可能降低峰值内存，但存在额外kernel调用成本。
C R2热态驻留/编码缓存：必须另行定义同热/冷的可比合同，不把热态和未知缓存条件混算。
整套判断：采样是主要瓶颈，但B/C未证明正净收益、非退化，不能虚报优于A。8188和8196无监听，未提交新任务。一次受保护Reality仍未发生（0次），FINAL_VALID=NO。
## 执行停止与后续准入
先本地只读/非生成核验object_info注册、backend、资源守护、队列与有无冲突；若运行时检查可通过且有可信正净收益依据，再冻结唯一候选并在同输入/seed/1024×576/5帧/20步下执行一次受保护Reality。测试质量、端到端时间、RAM/VRAM、SHA256；失败恢复R2，不删除任何成果。不修改代理/FlClash/既有浏览器。