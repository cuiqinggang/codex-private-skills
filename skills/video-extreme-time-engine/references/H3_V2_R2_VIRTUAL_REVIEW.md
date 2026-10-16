# 第2版 R2：整套虚拟复审与最短图片冻结

## 任务和证据
沿用用户参考的静态画质，1024×576、5帧PNG；不生成五秒视频或音频。方法为已激活《三人行》V2 C002，Windows优先使用V7的C通道。
F001的实际失败点是主模型创建至采样准备的内存峰值，165.469秒RAM90.1%保护，无LoRA、无图。复审以此为BAD，不把失败批次172.187秒当成功成绩。V1 172.128秒是另一基本规格，保留为GOOD，不能跨规格宣布胜负。

## 完整成熟路径比较
| 路径 | 已有资料/基础 | 本机适配判断 |
|---|---|---|
| 32B NVFP4＋原生INT8＋20步 | 官方完整模板；F001本机实际证据 | 已在当时资源状态失败，不原样重试 |
| 标准4B CLIP＋ClipProj v3.1＋原生INT8＋20步 | 上游完整图、模型、加载建议和405次图像/297次语音测量报告；本机已有4B与节点 | 本轮选择。保留主模型、VAE、采样和尺寸，优先削减条件模型负担 |
| 标准4B CLIP＋ClipProj v3.1＋W4A8 | 2080Ti成熟公开案例及本机V1成功组件 | 低内存备选；会额外改变主模型量化，不作为本轮首测，也不承诺同质量 |

ClipProj作者仍标注proof of concept；完整资料与已有本机组件支持将其作为可复现候选，不代表本机高品质已认证。v3.1改进重点是多语言语音，没有证据证明静态画质必然高于v3；本轮选择官方推荐的26MB ridge文件，避免无必要的大投影与额外组件。
不采用自研内存分配、LoRA分块、自编CUDA、全局关dynamic或开锁页、草稿缓存/稀疏注意力。LMS与二采/超分仍是后续质量候选，本轮不叠加。

## 选定的整套组合
同一参考第216帧与原提示词、seed3013 → CLIPLoader(krea2/default，现有Qwen3-VL-4B FP8) → ClipProjApply(v3.1 ridge) → 原生H3 I2V条件；
原生FL2VA INT8 ConvRot → 现有Star7受保护FP16加载 → sigma12/3 → res_multistep/simple 20步 → 原生VAEDecode → SaveImage五张。
保留dynamic、disable-pinned-memory、reserve-vram2.5、vram-headroom0.5。没有LoRA。音频仅为联合latent内部结构，不解码或保存。

## 整套反例审查
1. 条件编码：小编码器必须是VL且4B，loader类型krea2、投影输入2560输出5120；使用上游单卡建议的标准加载器＋Apply，让Comfy正常管理卸载。不因旧all-in-one节点存在就认定V1发生固定驻留；V1已用dynamic，F001则是官方32B，二者事实分开。
2. 质量：原celeb-v2投影校准没有图像token；采用有公开说明的v3.1，仍保留20步和原生INT8，避免同时用短步数/额外量化掩盖画质变化。最终质量由实际图像审查决定。
3. 资源：编码器文件从15.687GB降至5.242GB，另加26.256MB投影；这是存储规模对比，不能直接认定整机峰值降低同样数值。保留独立RAM90%保护与900秒预算；不靠释放用户其他应用或放宽阈值。
4. 精度与解码：保护插件在载入后set_model_compute_dtype(float16)，保留敏感FP32区和量化分发；早期manual cast日志不能独立证明最终计算路径。固定Comfy源码的H3 VAE支持FP16/FP32，并自带256像素空间/17帧时序分块，不额外叠加无必要解码插件。
5. 完整计时/失败：一次提交，包含编码、主模型准备、采样、解码、保存和图片尺寸/可读性检查。服务启动和准备另列，不能把纯采样当全程。没有完整同质量成功基线，不能认证物理极限或百分比加速。失败须由独立进程定向回收本次服务并对账，不自动重投。

## 版本和冻结
FREEZE_ID=H3-HQ-V2-MIN-R2-F002-20261016。
投影：NicoLab28/ClipProj-MiniMax-H3，revision=2ebdbcdc27a29a9607efdb221a9afcb9a0cdd808，文件mmh3-4b-ClipProj-v3.1.safetensors，26256128字节。
SHA256=0184e5c8d666a131962506d21949c2d8a8c6f33445b7b5e347e9a7e0a5baa819；下载实际11.125秒且哈希通过。
API图、执行脚本、节点源码、输入及原配置均按本机freeze.json固定SHA；实际schema、下拉模型项、空队列和资源准入通过后才提交。
本轮只执行该完整候选一次。VIRTUAL_REVIEW=COMPLETE_FOR_MINIMUM_IMAGE_TEST，GLOBAL_OPTIMUM=UNKNOWN，QUALITY=WAIT_REALITY；不把静态复审宣称为高品质视频已成熟。
本机目录C:/AI/MiniMax-H3/projects/H3-MINIMAL-20261015/V2R2_MIN_20261016；脚本run_v2r2_min.py。旧F001与V1文件不覆盖。

## 原始资料
- https://github.com/nicolab28/ComfyUI-ClipProj （单卡标准加载建议、完整图与限制）
- https://huggingface.co/NicoLab28/ClipProj-MiniMax-H3/blob/main/bench3.1/README.md （测量报告，不能代替本机验收）
- https://github.com/star7code/minimax-h3-fp16-exact-star7 （SM75精度保护、量化和LoRA边界）
- https://github.com/IvenKooLab/minimax-h3-turing （同级硬件成熟路径及失败经验）
- https://github.com/reventadirecta/MiniMax-H3-ComfyUI-8GB-VRAM （完整低内存工作流；显卡架构不同，不能直接继承时间）
- https://github.com/Comfy-Org/ComfyUI/blob/8a33128f2f8c5585c57486c07de481241e70a39c/comfy/sd.py （原生VAE实现）
