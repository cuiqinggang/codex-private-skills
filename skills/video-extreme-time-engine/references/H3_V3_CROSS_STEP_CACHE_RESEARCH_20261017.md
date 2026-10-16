# H3高清五帧跨采样步缓存复用成熟方案研究（2026-10-17）
方法：三人行V3、C通道只读检查+公开成熟项目。未新增GPU生成。
## 关键纠正
本机 ComfyUI 源码 comfy/ldm/minimax/model.py 的联合视频/音频模型包含50个DiTBlock；5帧不是分别生成5张再按帧顺序重复，而是20次对时序潜变量联合迭代。因此可复用项主要为相邻**去噪步骤**的模型输出、块残差和可安全缓存的条件编码；不能简单直接重复上一张图或任意复用上一步噪声预测，否则改变去噪动力学。
## 成熟优先候选（最多3）
A MiniMaxH3 FirstBlockCache (duckyshell)：每步算首块，剩余网络残差变化小则缓存；H3 Safe受保护窗口10~95%且最多连续2次命中；H3 Fast阈值0.10。RTX5090同attention内测量约1.44-1.49x采样速度，作者明确近似而非无损，不保证SM75性能。https://github.com/duckyshell/ComfyUI-MiniMaxH3-FirstBlockCache
B MiniMaxH3 TeaCache (Icyoung)：跨timestep特征/输出缓存，作者自述1024x576 20步124帧INT8 ConvRot在CMP170HX 64GB上306.22→102.08秒（整次），不代表2080Ti 5帧或质量无损。https://github.com/Icyoung/ComfyUI-MiniMaxH3-TeaCache
C T8 MiniMax H3 Block Cache：首块总是计算，在音频/视频变化足够小时复用剩余块；实验性，作为质量风险反例优先级低。https://github.com/T8mars/comfyui-minimax-h3-blockcache-T8
论文依据：CVPR2025 TeaCache https://openaccess.thecvf.com/content/CVPR2025/html/Liu_Timestep_Embedding_Tells_Its_Time_to_Cache_for_Video_Diffusion_CVPR_2025_paper.html ; ICLR2025 FasterCache https://proceedings.iclr.cc/paper_files/paper/2025/hash/518046d86bbc41a0707727c38301ad8e-Abstract-Conference.html。
## 本机检查
C通道确认 ComfyUI/custom_nodes 目前没有这些独立缓存插件；本机Minimax源码50个DiTBlock，R2 20步采样332.610秒，R5分块采样339.344秒，后者仅减少临时激活峰值、不实现跨去噪步跳块，因此不具备上述缓存加速。
## 兼容与质量边界
缓存不是纯函数结果可无损重用：噪声潜变量、timestep、运动区域都改变；需要变化阈值/保护窗口、强制定期完整计算、音视频联动保护，且同seed也不保证和未缓存像素等价。禁止把不同GPU帧数或热态成绩当作本机预计时间。缓存类节点彼此不可叠加，且与原R5 patch可能存在嵌套冲突。优先从原R2无R5分块工作流出发，插入唯一一个成熟缓存节点、保留INT8/seed/20步/5帧/提示词/VAE全部条件。
## 下一步准入
优先只读评估A/B实现对SM75、torch、ComfyUI 0.34、Minimax H3原生50块、音频条件、加载器兼容；评估强制全算步、最大连续命中次数、缓存占用和保护，质量验证计划包括对R2各五帧逐帧面部服饰及逐帧运动/亮度变化。若选中唯一候选再单次受保护Reality。同质量认证之前不保证物理极限/3倍/具体目标时间。保存R2 463.266秒与R5 452.188秒、采样332.610/339.344作为已有历史实测，不重投。
