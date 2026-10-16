# FirstBlockCache Safe + R2 首选准入审查｜2026-10-17
方法：《三人行》V3，C通道只读审查；未新增GPU推理；状态：SOURCE_COMPAT_PASS，RUNTIME_REGISTRATION_NOT_VERIFIED，VRAM_PEAK_NOT_VERIFIED。
## 固定证据
本机C:\AI\MiniMax-H3\ComfyUI\comfy\model_patcher.py有set_model_patch_replace（约667行）、get_model_object（约750行）、add_wrapper_with_key（约1343行）。原生H3 model.py约723-737行读取patches_replace['dit'][('double_block', i)]，遍历50个DiT块。故FirstBlockCache的关键接口形状可静态匹配；仍需安装到隔离白名单的运行时object_info及模型补丁实例化非生成验证。
公开FirstBlockCache源码GitHub blob SHA 20fd054cc0f2e34df2f987d5ffe40fea29424da7（nodes.py）。预设H3 Safe阈值0.08、窗口10%-95%、最多连续缓存2次；sample wrapper在OUTER_SAMPLE前reset、finally再次reset；begin_call使用形状/dtype/device及uuid分隔状态，sigma回升/形状变化时清除；首次比较前cache为空必完整计算；首个block仍每步执行，缓存命中跳过后49块，保存remaining_blocks_residual。
注意：Safe默认temporal_guard=False；仅Custom支持temporal_guard=True且需人工设等同Safe的阈值/window/hit上限。不应声称Safe默认有逐帧保护。输出复用为近似数值而非完全同像素。同一uuid下prompt等条件语义变化时，依靠OUTER_SAMPLE reset；必须验证采样生命周期包装实际触发。
明显兼容风险：额外残差/首块输出的clone显存开销，本机22.5GB上曾使用约20.5-21GB；GPU剩余容量较小，单凭接口静态匹配不能允许推理。需预估/记录缓存峰值以及检测是否引起额外卸载和速度逆转；动态显存调度与本机Comfy malloc graph交互要用真实日志验证。
TeaCache竞争候选源码teacache.py SHA 28115de99d653263f3dbe0fabe723fff28343660，nodes.py经源码核对：使用set_model_unet_function_wrapper、按输入rel_l1与累积阈值复用前次模型输出，预设start=2/end=-2；state在node.apply时创建，并非OUTER_SAMPLE每次重置。没有FirstBlock式uuid/形状/sigma逆转/每次采样reset/最多连续命中保护。对H3联合视频音频返回类型，代码用torch.Tensor类型假设，需要实际确认（不可直接作为安全一号候选）。
## 本轮决策
FirstBlockCache Safe单独连接R2节点3 SigmaShift输出，经新增缓存节点接原Guider和Scheduler。不能叠R5分块、T8、EasyCache、CacheDiT或其他double_block替换。保持原INT8 ConvRot、seed3013、1024x576、5帧、20步、VAE、提示词及资源保护。来源固定且审查后方可部署，不立即提交GPU生成。
运行时准入必须确认插件导入与节点object_info、完整model.clone/patch回调、第一次采样cache=0、每次重置、模型输入signature、OOM保护；缓存自身带来的GPU峰值和真实命中数量无法从静态源码认证。只有安全通过后才能Freeze一次现实生成，再比较R2全程463.266秒、采样332.610秒和逐帧质量。
当前FIRSTBLOCK_STATIC=PASS；TEACACHE_COMPETITOR=DEFER；REALITY=0；FINAL_VALID=NO。
