# H3 编码器加载差分定位 C001｜2026-10-16

承接GPU-BASELINE-F001-20261016.md；生成仍暂停。本次只读源码/日志和生成隔离候选，无推理、无模型加载、无性能认证。

## 已确认
- 最早可观察到的长停顿落在节点6 MiniMaxH3ImageToVideo的条件编码路径：先resize→clip.tokenize→clip.encode_from_tokens_scheduled，后vae.encode。日志长期只有Krea2TEModel约4999MB prepared，随后才出现VideoVAE和MiniMaxH3主模型准备。因此不应将最早停顿笼统归因于主DiT加载。
- prepared/staged日志不证明全部权重已经驻留GPU，也无法单靠日志分离磁盘读入、搬运与编码算子的精确耗时。
- 节点1 ClipProjLoader配置mode=dynamic、device=cuda:0。插件0.1.13源码说明dynamic为逐层分页，最低峰值占用、最慢编码。旧274–323秒热运行缓存命中节点6，绕过了这段成本；不是此配置后来从GPU漂移到CPU。
- 当前文件与固定上游nicolab28/ComfyUI-ClipProj@c01ba8fb8f41b4f2094dbd0b185cdc238fb6134c的clipproj_nodes.py Git blob SHA完全一致：2291f8c1603d812a8d607579ce25a7e7a15704c9。
- 原片首帧1038×576，小于厨房1681×936；节点会先缩放到目标尺寸。排除直接把更大原图未缩放输入作为解释。
- _encode调用mm.load_models_gpu，execution_device来自patcher.load_device；未发现显式CPU推理配置。低GPU利用率与系统页面读入是等待线索，不是CPU推理证明。

## 复用的成熟候选
只将节点1 mode由dynamic改成插件现有streaming。该模式disable_dynamic=True、force_full_load=True；由ComfyUI先申请空间，将编码器整体加载到GPU；随后允许卸载回RAM，让采样使用显存。resident常驻模式被排除为首选，因为会长期减少DiT显存空间；不采用gpu-only或全局改精度。
保留W4A8主模型、Qwen4B、Turbo4、步数、输入图、提示词、种子、尺寸、帧数和启动参数。streaming不是零RAM方案，也不保证更低RAM；必须考虑峰值、搬运、下一阶段卸载和整体时间。
候选文件：C:/AI/MiniMax-H3/projects/H3-MINIMAL-20261015/workflow_reference_streaming_C001.json
SHA256：26423809c7bd4dab63eb959ee4a9dbc62e26d99cf86a8343cc5dd77e62dacdb7。
静态差分仅1项：节点1 mode dynamic→streaming。未提交；不能直接重用旧输出前缀和旧任务回执提交，未来验证需独立唯一任务身份并遵守锁。

## 边界与下一节点
可以确认所选加载模式是明确的低内存慢编码路线，并且旧测速隐藏了该阶段；尚不能量化它对838.265秒的贡献，不能宣布全部根因已确认/已修复。缺进程级硬缺页与逐阶段计时，安全软件扫描也没有本机归因证据。不开关杀毒，不修改代理，不安装新推理组件。
下一步先对整套streaming候选完成资源生命周期与质量风险审查，冻结有阶段计时/受控中断的最小验证；不得直接再跑无监控长片，也不得未经版本化更新绕过GPU-BASELINE-LOCK.json。
