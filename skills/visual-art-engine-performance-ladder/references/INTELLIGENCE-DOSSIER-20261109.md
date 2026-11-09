# 通用视觉生成引擎 V3.3：专项情报扩搜与成熟配方资料库

日期：2026-11-09。接续 V3.2；本次是扩大搜索、实读工程和分类决策，没有新增 GPU 推理或本机视频能力认证。

## 这次纠正的核心

上一轮过早从“寻找成熟能力”收窄成“补一个原样品的取证”。一个样品不能代表成熟能力资料齐全；某个整合包有问题也不能推出同类成熟方法不存在。本轮先建立可比较的作品、原工程和实践反馈组，再选择最简的已公开方法。

优先投入前端情报搜集，是为了降低部署、失败和返工的完整成本。用户提出的“前面多花一分、后面节约十倍”是决策原则，不是本次已测出的倍率。

本轮归档 55 组检索/核查返回记录、395 个规范化去重来源入口；实读解析 **25 份工作流 JSON**，读取 **5 个新增 Remotion 项目的 package.json 与 Root.tsx**。另逐项索引 **LivePortrait 9 组官方配对、FASHN 6 组官方换装配对、Sonic 9 组图片/音频/工作流样例、LatentSync 3 组官方视频/音频输入**。这些不是相加后的“成功作品数”；官方输入、公开成片、独立反馈、本机结果分别记录。

机器可读文件：

- [原配方核查清单](RECIPE-MANIFEST-20261109.json)：25 份工作流的原仓库、路径、blob SHA、模型、输入引用、节点类型和待核项。
- [具名样例与工程索引](CASE-POOL-20261109.json)：可逐个打开的输入配对和工程入口，不计算所有可能组合。
- [实践反馈账本](PRACTICE-EVIDENCE-20261109.json)：正面、负面、完整度、去重分组和适用边界。
- [来源总表](SOURCE-REGISTRY-20261109.json)：广搜入口；标明仅搜索命中或已打开页面。官方源码实读在工程清单中另列。
- 既有本机验收继续看 [V3.2 证据](FEEDBACK-CASE-REVIEW-20261109.md)，不重复部署或重跑。

## 分类比较和当前选择

这里的“优先复刻”表示外部材料足以支持继续照已有方法做同类作品；不代表本机已验收，更不代表任意题材都能一次成功。

| 类别 | 已收集的比较组 | 当前优先路线与理由 | 适用范围及替代 |
|---|---|---|---|
| 人像表情、头像动画 | LivePortrait 原生 9 配对；KJ 3 工作流；AdvancedLivePortrait 5 工作流；Windows 实作与社区作品 | **原生 LivePortrait 常规人像模式**；原输入、官方 Windows 包、命令/GUI 和多个实践入口齐 | 正脸/小幅头动；需要可编辑表情时选 Advanced 原例，不叠加背景修补链 |
| 静态照片数字人口播/唱歌 | Sonic 9 样例；MuseTalk；LatentSync；EchoMimic；Hallo | **先比较 Sonic 原图+原音频的最小配方、MuseTalk 已公开的短正脸案例** | Sonic 与 MuseTalk 不混称同一路线；唱歌组合另有 16GB 成片，不能直接继承到本机 |
| 已有视频改口型 | LatentSync 官方 3 组输入；1.5 Wrapper JSON；1.6 双模型配对测试；InfiniteTalk 两种工程 | **短、近正脸用版本对齐的 LatentSync 原生配方**；较大头动再比较 InfiniteTalk V2V | 1.5 与 1.6 显存要求不同；公开测试的六次运行只有一个场景 |
| 长口播/双人说话 | InfiniteTalk I2V、V2V、官方多说话人工作流；MultiTalk 旧资料 | **保留 InfiniteTalk 原生/Kijai 方案作为较强整包候选** | 3090 的一秒视频需几十秒至一分钟这一实测范围不能说实时；双人与单人分别验 |
| 视频只换脸 | FaceFusion 原生/Pinokio；VisoMaster 官方免费包；ReActor；Rope | **先比较 VisoMaster 官方免费 Windows 包与 FaceFusion 免费原生/Pinokio** | 官方免费包与第三方付费打包站分开；手动 FaceFusion 官方明确不面向初学者 |
| 静态服装展示 | FASHN 6 配对；Leffa；CatVTON；IDM-VTON；独立多类别测试 | **FASHN 1.5 原生方法**；无需手工 mask，本机已有固定案例两次运行 | 普通服装展示优先；复杂花纹、精确版型保真另验；不当作连续视频换装 |
| 连续视频换衣 | CatV2TON、MagicTryOn 含 1.3B/Turbo、Wan VACE 换衣作者工作流 | **本轮仍未认证满足“免费、简洁、多方容易复做”的完整方案** | 不改称静态换装加图生视频；继续保留原作者结果、数据入口和 VACE 完整工程线索 |
| 整个人物/全身动作替换 | Wan2.2 Animate 官方 JSON；Hearmeman 免费工程；Frizzy 旧版/Ultimate；MimicMotion/AnimateDiff | **先官方原生 Animate；显存受限才选作者已支持的量化分支** | 使用参考图+动作视频；快舞、手部、遮挡另选已有合格例；不把节点数量直接当难度 |
| 图生视频、景物、产品短镜头 | SVD 原例；Wan 5B/14B I2V；FramePack；LTX I2V | **质量优先比较 Wan 14B 已分享加速配方；简单景物可用 Wan 5B 原生** | SVD 旧山景 14 帧只继承已做部分；FramePack 原包对 20 系显卡未验证，不列本机首选 |
| 纯文字视频、首尾帧过渡 | Wan 5B/14B；LTX 2.3/2.5；官方首尾帧工作流 | **按作品质量和控制需求选官方窄任务模板** | 带参考图/首尾帧的方案不能登记为纯文字盲测 |
| 原声音驱动画面、同步音视频 | LTX 2.3 IA2V 仙人掌案例；2.5 I2V/T2V；Frizzy 多模式实作 | **先固定版本的官方单任务模板，再考虑作者整合文件** | 2.3/2.5 及其 adapter 不随意混用；3060 实作不代表 2080 Ti 的精度内核已适配 |
| 字幕、播客、音乐可视化、代码演示、品牌短片 | Audiogram 既有实测；HelloWorld、Music Visualization、Overlay、CodeHike、TikTok 全工程 | **现成 Remotion 工程改公开 props/素材**，确定性渲染链最短 | 模板质量适用于图文/动效；不是写实人物表演能力；Prompt-to-Video 模板含付费模型 API，另列 |
| 动漫放大、补帧、去背景及合成 | Real-ESRGAN 官方视频例与三段对比；RIFE；RVM；Video2X | **先原配方已有后期；独立需要时用对应原生/便携分支** | Video2X 当前预编译要求 AVX2；i5-3570 不匹配，不走现场编译解决；补帧不能修正错误动作 |

## 1. 人像动画：从一个样品扩成可选的原配方组

官方原生工程：[KlingAIResearch/LivePortrait](https://github.com/KlingAIResearch/LivePortrait)。读取 app.py，确认 6 组 I2V 与 3 组启用的 V2V 配对，未把注释掉的条目或任意交叉组合计入。

- I2V：s9/d0、s6/d0、s10/d0、s5/d18、s7/d19、s2/d13。
- V2V：s13/d0、s18/d6、s20/d0。
- 原生最短使用方式：取作者 Windows 包或原环境，装原权重，指定原 source/driving，运行原 inference.py 或 app.py；通过后只换作者支持的人像输入。
- [KJ 示例目录](https://github.com/kijai/ComfyUI-LivePortraitKJ/tree/main/examples)：图片驱动、实时、视频驱动 3 份 JSON 已读。
- [Advanced 示例目录](https://github.com/PowerHouseMan/ComfyUI-AdvancedLivePortrait/tree/main/sample/workflows)：静态表情编辑、提取表情、带表情迁移、无驱动视频动画、向视频插入表情 5 份 JSON 已读。3/4 节点的是静态功能，不能当视频成片数。

实践不是只有官方展示：[WellWells](https://wellstsai.com/en/post/live-portrait/) 给出 Windows 完整步骤、日志、输入 s6/d0 和 MP4；另有 [GTX1060 6GB 实作](https://www.reddit.com/r/StableDiffusion/comments/1dzp864)、[头像教程/素材工作流](https://www.reddit.com/r/StableDiffusion/comments/1dwz27s)、[Viki 作品](https://www.reddit.com/r/StableDiffusion/comments/1dwhp0f/comfyui_liveportrait_viki/)。其中同帖抖动反馈用于限定镜头，不能把“谢谢分享”计成功。

决定：常规正脸、小幅表情已有更充分外部支持，可直接选择原生或具名样例安排简单复刻。不要为了复现每一个网络视频的历史字节先做复杂考据。上一轮下载的 s6/d0 作品只检查了三个静态帧，完整运动审看与本机推理仍分开记录。

## 2. 数字人和口型：补齐原输入、输出与多条实践入口

### Sonic 最小照片口播

[Sean-Bradley/ComfyUI-Sonic](https://github.com/Sean-Bradley/ComfyUI-Sonic) 和[作者教程](https://sbcode.net/genai/lipsync-sonic/)提供 9 张配对输入图、9 张工作流 PNG、example.mp3、模型下载和放置位置。逐个索引，非随机拼九个组合。PNG 工作流的内嵌元数据尚未在本轮解包，不能写成另有九份 JSON 已解析。

已有[Pixaroma 原创教程](https://www.youtube.com/watch?v=3pN2KA6-G0I)，以及[独立唱歌组合](https://www.reddit.com/r/comfyui/comments/1legiju)：Flux+ACE-Step+Sonic，全本地、4060Ti 16GB/64GB RAM、10 秒 576 方形 25fps，作者报少于 15 分钟。这是另一操作者的成片实践，但它使用 smthemex 节点，不能自动证明 Sean-Bradley 同封装、32GB RAM 或本机耗时。

### MuseTalk / LatentSync 配对资料

[第一人称配对测试](https://musetalkai.com/musetalk-vs-latentsync/)公开同一输入视频、音频、两种输出、六次文件、配置和测量记录。测试者并非这两个模型的官方作者；本轮按作者报告引用，未独立重跑。

- MuseTalk 1.5：code 0a89dec45a0192b824e3cf4daf96c239440c5ed8；model 2bcb936e2fddb4d86db4c62fd45b387d0c061571。FP16，batch=2，bbox_shift=0，extra_margin=10，jaw，cheek 90/90。
- LatentSync 1.6：code a229c3948406bc2cf6eaf4873e662e70c6a04746；model c42c7e6c8e9c213626389fa7d9a3c444b8536353。20 steps，guidance=1.5，seed=1247，DeepCache interval3/branch0，stage2_512。
- 同一约 3.6 秒近静止场景各三次，完整输入/输出可取；三次重复不算三类场景或三个独立用户。可解码不等于口型质量合格。本次不把该测试当普适质量排名。
- 原始设置/命令记录：[CSV](https://musetalkai.com/wp-content/uploads/2026/10/d24-method-and-configs.csv)。

[LatentSync 官方](https://github.com/bytedance/LatentSync)还包含 demo1/2/3 视频+音频；[Wrapper 样例](https://github.com/ShmuelRonen/ComfyUI-LatentSyncWrapper/tree/main/example_workflows)已读的是 1.5 文件，不能改个名字当 1.6。社区[1.5 原创示例](https://www.reddit.com/r/comfyui/comments/1je0xpz/best_lip_sync_latentsync_update_to_15/)和[实际使用问答](https://www.reddit.com/r/comfyui/comments/1i2gnuu)补足操作反馈。

决定：先拿现成近正脸案例对照，选择满足清晰度和口型要求的已有路线。旧本机 MuseTalk 嘴软样片保持未过；有新完整方法资料后可以另选合格案例，不把旧坏片当整个模型家族的否定。

## 3. InfiniteTalk、双人和半身数字人

[bluespork 原工程](https://github.com/bluespork/InfiniteTalk-ComfyUI-workflows)两份 JSON 均已读取：[I2V 发布/教程](https://www.reddit.com/r/StableDiffusion/comments/1n0aiqa/infinite_talk_lipsynci2v_comfyui_workflow/)、[V2V 发布/教程](https://www.reddit.com/r/StableDiffusion/comments/1n3c5hq/infinite_talk_lipsyncv2v_comfyui_workflow/)有明确成片、配置与时间。两帖按同一发布者分组，不算两个独立复现者。

补充[官方 InfiniteTalk](https://github.com/MeiGen-AI/InfiniteTalk)、[Kijai 原例](https://github.com/kijai/ComfyUI-WanVideoWrapper/tree/main/example_workflows)、Comfy 官方多说话人模板；官方模板引用女人/男人两路音频与两人图。后者是多说话人输入工作流，不能凭文件名认定任意双人长对白都成熟。

[EchoMimic v2](https://github.com/antgroup/echomimic_v2)附有半身图片、中文音频和配置。[Hallo2 与 Echo v1 的独立对照](https://www.reddit.com/r/StableDiffusion/comments/1g6h0ug)明确使用别人的首帧/音频，给出 6 steps、cfg1、30fps、16kHz 和加速模式。v1/v2 不混用；手部问题明显的半身例不进入高质量简单方案首选。

决定：资料组已经明显扩大；优先窄任务原例，不把“无限时长”当质量或速度保证。

## 4. 换脸：成熟工具和简单入口分开选

[VisoMaster 官方项目](https://github.com/visomaster/VisoMaster)提供免费 Windows/NVIDIA 包，README 链接 [v0.1.1 安装文件](https://github.com/visomaster/VisoMaster/releases/download/v0.1.1/VisoMaster_Setup.exe)及便携启动方式。名称相近的付费站、Studio 或 Fusion/mod 不等于这一版本。

[FaceFusion 原生文档](https://docs.facefusion.io/installation)与 [Pinokio 入口](https://github.com/facefusion/facefusion-pinokio)可取；源码免费与官方商业安装器分别登记。最新 README 明说手动安装需要技术技能，因此本机已有健康环境/原生 Pinokio 成熟脚本优先，不把复制安装命令包装成人人一键。

[实际使用比较帖](https://www.reddit.com/r/StableDiffusion/comments/1m7lrdp)同时包含 FaceFusion 长期使用、VisoMaster 选择及运行快慢反馈；[视频实作教程](https://www.youtube.com/watch?v=3pp7qw19nuA)给出实拍操作和面部选择建议。[ReActor 多参考图反馈](https://www.reddit.com/r/comfyui/comments/1lc5u9v/best_way_to_swap_face_if_i_have_57_images_of_the/)只支持该用户的换脸体验，不扩大成全视频角度保真。

决定：已有多个可比较入口，不再只守一个失败整合包。源脸和目标视频由用户有权使用的素材提供；按工具标准导入、选脸、预览、导出即可形成该方法的最小工作任务，不要求必须拿到某博主未公开的私人脸图。尚未本机验收。

## 5. 换装：六组原配对、多类别反馈和真实边界

[FASHN 官方 Space app.py](https://huggingface.co/spaces/fashn-ai/fashn-vton-1.5/blob/main/app.py)当前文件 revision 846236d；[素材目录](https://huggingface.co/spaces/fashn-ai/fashn-vton-1.5/tree/main/assets/examples)已打开。配对：
1. person1.png + garment1.jpeg，one-pieces/model；
2. person2.png + garment2.webp，tops/model；
3. person3.png + garment3.jpeg，tops/flat-lay；
4. person4.png + garment4.webp，tops/model；
5. person5.png + garment5.jpeg，bottoms/flat-lay；
6. person6.png + garment6.webp，one-pieces/model。

这些是运行输入配方，不能冒充六份已下载输出。[官方研究页](https://fashn.ai/research/vton-1-5)另有多组输入/结果展示，含裙裤转换、宽大衣物、头发/纹身等对照；不把广告视频服务当开源模型成果。

独立实践扩展为三组有边界的资料：
- [Allure Commerce 实测](https://www.allurecommerce.com/blogs/tech-talk/testing-ai-virtual-try-on-for-fashion-commerce)：对多个类别、托管与自托管方法做对照；FASHN 1.5 在自托管部分，1.6/Max 在商业 API 部分。不能把商业秒级价格转给免费模型。
- [AfriVTON-Bench 作者研究](https://dev-tyta.github.io/projects/afrivton.html)：报告 1,012 人衣配对、FASHN 1.5 与 Leffa、50 steps/cfg2.5/seed42。它是批量研究实绩线索，展示复杂非洲纹样保真不足，不能当 1,012 次高质量简单复做；页面 GitHub 按钮只指个人主页，完整复现实验包仍需单独定位。
- [Ionio 作者比较](https://www.ionio.ai/blog/vton)：记录普通上下装、裙装和托管 handler 差异。裙装枚举/handler 错误属于该封装问题，不等于本机已通过的官方红裙不成立。

决定：FASHN 的现成资料比上一轮充分，普通静态展示仍优先。两次本机固定红裙结果继续有效，新衣服/复杂纹样分别验。Leffa 与 CatVTON 保留替代而非强行补丁；NC 权重不放入默认商用路线。

连续换装另看 [CatV2TON](https://github.com/Zheng-Chong/CatV2TON)、[MagicTryOn](https://github.com/vivoCameraResearch/Magic-TryOn)、[VACE 作者换衣方案](https://tensor.art/workflows/890948473564743267)。前两者有结果/脚本/测试数据入口；MagicTryOn 还有小模型与 Turbo，但自定义预处理、环境及第三方容易复做反馈尚未齐。VACE 两阶段原图编辑+时序传播可以作为作者既有方案研究，但不自创一个静态换装加图生视频链来冒充精确视频换装成熟能力。

## 6. 动作迁移和普通视频：从工程库反查完整配方

[Comfy 官方模板库](https://github.com/Comfy-Org/workflow_templates)已实际读取 9 个模板，覆盖 LivePortrait、Animate、InfiniteTalk、Wan 5B/14B、首尾帧和 LTX 两代。

Wan 2.2 官方[教程与模型入口](https://docs.comfy.org/tutorials/video/wan/wan2_2)有明确模型和文件夹：
- 5B 原生：wan2.2_ti2v_5B_fp16 + umt5_xxl_fp8_e4m3fn_scaled + wan2.2_vae。当前图共 13 个序列化节点，LoadImage 初始旁路，不能以默认队列结果冒称 I2V；按作者界面启用图片分支属于已有接口配置。
- 14B I2V：高噪/低噪模型和对应加速 LoRA；不能把高低模型、T2V/I2V、VAE 互换。
- 首尾帧：两个图片输入，单列控制任务。
- Animate：参考图、驱动视频、检测/分割/姿态/原生生成；原图有这些环节不等于需要我们自己创造。

独立样例与反馈：
- [12GB 14B 加速实作](https://www.reddit.com/r/comfyui/comments/1mlcv9w/fast_5minuteish_video_generation_workflow_for_us/)明确 Q4、文本 Q5、Lightning、2+3 steps、49 帧/约 640 像素，作者报约 5 分钟。记录其卸载节点与输入条件，不能承诺本机相同用时。
- [5B/16GB 基准作者](https://vram16.ullu-egg.com/en/models/wan2-2-ti2v-5b/)提供实测设置下载；[3060Ti/32GB 实作](https://note.com/ai_scouter/n/n5445e07f242c)报告短片生成和景物适用范围；[DCAI 作者实践](https://www.digitalcreativeai.net/en/post/wan-2_2-high-quality-ai-video-generation-comfyui)同时保留 5B 语义失真反例。三者不是完全同设置的成功率样本。
- [Hearmeman Animate 成片/免费工程](https://www.reddit.com/r/comfyui/comments/1nr3vzm/wan_animate_workflow_replace_your_character_in/)和[免费 JSON](https://drive.google.com/file/d/1ev82ILbIPHLD7LLcQHpihKCWhgPxGjzl/view?usp=sharing)可分开于其可选付费云模板。后者下载内容本轮未解析，不能记成已核 JSON。

[Frizzy 整理库](https://github.com/Thefrizzy1/The_frizzy1-Workflows)的两个 GGUF 图、Animate 旧图和两个 Ultimate 图已实读，并读相应模型表。它是值得利用的整包资料源，作者提供多模式成片/输入/下载/测试环境；不是只发现一个例子。原图存在改名 LoRA、旧绝对输出路径等，优先其已修订版本或官方原生图，不据此否定整个模型家族。其自动 doctor 会安装节点，当前只读审核，不向共享 ComfyUI 执行安装。

决定：为同类作品保留原生、量化和作者整合三种可比较分支，再按已展示作品质量/整包完整度选，不把最低节点数或最新版本作为唯一指标。

## 7. LTX 原声音画与多模式案例

[官方兼容表](https://docs.ltx.io/open-source-model/reference/workflow-asset-compatibility/)明确 2.3、2.5、原生 Python 和 ComfyUI 的资产边界。已读 2.3 T2V、2.3 IA2V、2.5 I2V JSON。

[官方仙人掌说话案例](https://comfy.org/hub/workflows/talking-character/)提供 cactus_man.png、ltx_23_audio.mp3、提示词和工作流。云上 Run 可能收费；下载的本地配方另查权重许可和资源，不能把官方云 UI 当免费本地实现。

[Frizzy LTX2.5 Ultimate](https://github.com/Thefrizzy1/The_frizzy1-Workflows/tree/main/workflows/ltx/ltx-2.5-ultimate-12gb)有原图、两个预览 MP4、JSON、models.json、下载位置与模式记录。作者称 3060 12GB/32GB、960×512、4 秒，T2V/I2V/首尾帧/姿态/部分 VFX 完成；Ingredients 只得到面板网格，未过。一个整包的一个模式失败不否定其他已展示模式；也不能把所有菜单项一并认证。nvfp4 等加载路径在 2080Ti 上仍需确认，不因总显存更大就默认兼容。

决定：这是此前漏掉的实质资料组，纳入比较；本机优先单模式官方原例，暂不同时加载所有可选权重或自创兼容补丁。

## 8. 模板视频：六个具体工程入口

读取了官方模板注册表；排除空画布、SaaS 框架和需要付费生成 API 的示例，保留六个具体内容工程：

| 工程 | 现成内容 | 本轮实际核对 |
|---|---|---|
| [Audiogram](https://github.com/remotion-dev/template-audiogram) | 播客字幕、波形、背景 | 继承本机 27.136 秒视频两次渲染 |
| [HelloWorld](https://github.com/remotion-dev/template-helloworld) | 标题/标志动画 | 原树、package、Root，3 个 Composition |
| [Music Visualization](https://github.com/remotion-dev/template-music-visualization) | 封面/音频可视化 | 原树、package、Root 与原演示 MP3 地址 |
| [Overlay](https://github.com/remotion-dev/template-overlay) | 直播/品牌动态覆盖层 | 原树、package、Root |
| [CodeHike](https://github.com/remotion-dev/template-code-hike) | 动态代码演示 | 原树、package、Root 与 4 个原代码样例 |
| [TikTok](https://github.com/remotion-dev/template-tiktok) | 视频+动态字幕 | 原树、package、Root、原 sample-video、字体与许可；Whisper.cpp 英文默认模型另需下载 |

最短方法是取得原工程、按锁文件安装、启动 Studio、选择已有 Composition、按原参数渲染，然后改已有 props 或素材。不从零让模型写一个新模板再宣称复刻。

[官方目录](https://www.remotion.dev/templates)还有视频预览与源码入口。Stargazer 的 main 树请求 404，未解析为完整工程，留在线索；不把失败请求隐藏。Remotion 有个人/小团队免费条件，按当前许可范围使用，不能承诺所有企业免费。

## 9. 后期能力：找到更简单的成熟入口，也提前排除硬件坑

- [Real-ESRGAN 官方动漫视频说明](https://github.com/xinntao/Real-ESRGAN/blob/master/docs/anime_video_model.md)：原模型、inference_realesrgan_video.py、三段输入输出对比及 Windows Vulkan 包。按原生程序做放大，不自行重写推理核心。
- [RIFE 官方](https://github.com/hzwer/ECCV2022-RIFE)：两段慢动作展示、示例视频、inference_video.py；作者提供 2080Ti 基准和 Practical-RIFE 对扩散短片的既有例。只在原动作正确时作补帧。
- [RVM 官方](https://github.com/PeterL1n/RobustVideoMatting)：整套 showreel 原视频可取、MobileNetv3 权重与 convert_video 文档；[bycloud Windows 实作](https://www.youtube.com/watch?v=_oN9yyRi3HY)是另一作者步骤。两条 bycloud 频道视频按一人分组。
- [Video2X 官方](https://github.com/k4yt3x/video2x)：新 GUI/安装器与多模型处理，比手工拆帧更简；但预编译要求 AVX2，已知 i5-3570 的 [Intel 规格](https://www.intel.com/content/www/us/en/products/sku/65702/intel-core-i53570-processor-6m-cache-up-to-3-80-ghz/specifications.html)只列 AVX。因此当前机不采用它的默认预编译包，也不现场编译作为绕行。
- [独立老音乐录像处理](https://www.reddit.com/r/AIRemastered/comments/1ies2dp)有免费 Video2X 成品链接与伪影反馈；不能以“有文件”宣称高保真修复。

决定：成熟方法还要匹配这台设备；情报阶段排除硬件不符，正是减少后段成本。输出 4K/8K 尺寸不等于恢复了原来没有的真实细节。

## 新的运行规则：资料先行，避免两种过度

1. 常见类别先建立多个可比作品/配方与不同操作者反馈组，不找到一个就结束。至少三种具名作品/配置、两条不同操作者成片反馈可作检索参考目标；不是强行凑数的验收条件。
2. 先原作者库/模板库反查素材与工程，再搜第一人称复现、问题区和按硬件过滤。作者多案例证明覆盖；不同操作者证明外部可实践；二者都需要。
3. 精确复刻某原作，才要求该原作输入与版本完整对应。学习公开方法制作同类作品，可用作者配套样例、默认值和用户有权使用的相近素材；不因某博主未公开私人素材，把成熟工具误判为无能力。
4. 官方原生图、已验证量化图和作者整合图分别比较。原配方已有剪辑可原样保留；自创反复修补不算简单成熟方法。
5. 正反反馈按镜头、质量目标、版本和硬件解释。反复抽卡、重画手部、改核心、多补丁的作品，不进入“简单一次照做”的优先组。
6. 学习免费不等于商用许可相同；不买教程/API/打包器/云算力。无意新增费用时不用收费按钮。已有本机结果继续继承。
7. 收敛依据是新增资料是否仍会改变选型、是否存在更简单完整的既有分支。不得用任意搜索条数、固定搜索时间预算或“看起来够了”提前终止。
8. 当前未满足完整条件的类别继续检索已有方案；不转入自研。没有统计分母不写 95%/99% 成功率；没有起止时刻不宣称完整 T_VALID 优化倍率。

## 本次验收和未完成

已完成的是广搜索引、官方/作者工程实读、输入与工作流的逐项映射、公开实践正反证据和分类选择。新来源只按实际读到的内容归档；未播放的片子不写“我已完整观看”。公开页面可能改版/失效，执行前用原 revision/blob 校对。

没有新增推理，没有将 25 个文件写成 25 项成功能力；没有把官方样例数写成独立用户数；没有代替用户确认艺术质量。连续视频换装、双人高清长对白、任意复杂剧情仍保留明确缺口，但现在有多条同类分支和原材料入口可继续选择。

下一步按实际用途，从这些已经收齐较多资料的组中选“最简单且质量匹配”的原配方，做最小必要验证；不再从少量工具的失败反复修坏片。
