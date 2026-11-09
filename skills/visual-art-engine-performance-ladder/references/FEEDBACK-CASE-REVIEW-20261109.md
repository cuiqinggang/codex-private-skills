# V3.2：作品、完整配方与真实复现反馈审核

日期：2026-11-09，北京时间。目标：用免费可取、步骤简单、已有好作品和真实使用反馈的配方建立能力。本文完成跨类别资料审核和既有成果复核；没有新增模型推理，不把审核候选登记为新能力，也不声称穷尽全网。

## 结论与阅读顺序

先看本节与分类表；需要执行某类时，只读对应案例、来源和原配方。

- 找回三项有本机成品的原案例：Remotion 官方播客模板、FASHN 官方静态红裙换装、SVD 官方山景短样。前两项有两次重复运行记录；SVD 当前已读证据只覆盖一次原样复现。均未证明任意新内容迁移。
- 新增核查外部使用者的实际反馈。LivePortrait 的小幅头部/表情迁移、SVD 的短景物图生视频，已有多个第一人称实践信号；没有统计分母，不能写成功率 95%/99% 或承诺几乎必成。
- LivePortrait、FaceFusion、Wan Animate/WanGP 都有真实成功反馈，也有抖动、画质、安装或版本回退问题。它们属于可优先补齐具体案例的候选；目前没有把“工具好用”升级成“这个高清原作的完整配方已配齐”。
- FASHN 固定原案例的本机重复通过继续有效；本轮新增的独立开源版反馈不足，不能把商业 API 评价拼成同版本免费配方的高成功率证据。
- H3 R4 的五秒镜头保留原有内部验收，但用了多段生成、重定时和局部口型/闭口修补，不能作为本轮“直接简单复刻”的准入样本。
- 当前本机：Windows 10、RTX 2080 Ti 22528 MiB、32GB RAM。显存容量不替代架构、软件版本和实际可用内存匹配。

## 开始运行前的简单决策

1. **先选具体作品。** 原成品的清晰度、动作、连续性及适用声音本来就符合用途；输入图或下载视频的分辨率不能冒充生成结果分辨率。
2. **配方与作品配对。** 成品、原始输入、代码/权重版本、原工作流、参数、作者已有后期及环境对应同一案例。缺项写清，不凭题目补猜。
3. **看独立实践。** 优先具体成品、已执行步骤、输入条件、硬件、耗时和失败范围；支持容易复做的反馈须来自实际操作者。作者宣传、转载、同一人跨帖、复制 README 的 fork、点赞和“求工作流”不能算独立成功。
4. **比较反例。** 正反反馈按版本、硬件和镜头类型对齐。某用户只证明安装成功，不能计为画质成功；有人靠大量补丁做成，也不能计为本次简单路线。反例用于限定场景，不把单个失败当行业不存在成熟办法的证据。
5. **判定是否直接试做。** 作品合格、整包齐、多个实际实践支持、已知问题有作者文档内的简单处理、当前条件匹配，才安排最小完整原样复刻。否则继续补资料或换同类案例。公开反馈的总体成功率通常未知，只作有条件的定性决策。
6. **复刻后才登记。** 真实成品审核通过，再验重复；改提示词或换一组相近素材后另验迁移。普通原配方剪辑/合成可保留；需自创修补链或反复抽卡则不晋级。不能用审核文字代替实际执行。

不规定论文数、星数、教程数或固定复现概率门槛。免费指不购买教程、整合包、API 或云算力；本机计算、电费、下载与时间成本仍需记录。学习许可与商业交付许可分开记录。

## 分类决策表

| 类别 | 首选具体路线 | 已找到的正面实践 | 反例/当前缺口 | 本轮结论 |
|---|---|---|---|---|
| 播客、字幕波形、模板短视频 | Remotion Audiogram 原工程 | 本机完整 27.136 秒视频两次渲染；外部有 Remotion 创作实绩 | 外部泛 Remotion 案例不等于同一 Audiogram 配方复现；新音频字幕未测 | 继承固定原工程重复通过 |
| 静态人物换装 | FASHN VTON 1.5 官方第一个红裙案例 | 本机原程序两次相同结果，无修图或挑种子 | 独立开源版实践数量与条件仍不足；新衣服未测 | 继承固定静态案例重复通过；不能叫视频换装 |
| 景物图生视频 | ComfyUI 官方 SVD 14 帧山景 | 原样复现有完整证据；同架构 2080 Ti 社区成片，另有他人复现反馈 | 社区扩展配方和原生基础配方有差别；本机重复与换图未测 | 保留单案例复现；优先补重复/迁移 |
| 人像表情、头部动作 | LivePortrait 人类模式，小幅、近正脸 | GTX1060 6GB 成品和工作流；Viki 创作者实作及实际用户正反馈 | 抖头、形变和复杂场景对齐反馈；高清成品与完全一致配方未配齐 | 优先补齐原案例，尚未本机运行 |
| 单人数字人口播/口型 | MuseTalk 1.5 正面真人短样 | 用户报告低显存短音频可运行；本机已产出 8 秒文件 | 本机嘴部柔化，未匹配高清同案例基准；侧转有闪烁反馈 | 已执行但质量未过；不重投同一坏样来认证 |
| 只换脸 | FaceFusion 免费源码/官方 Pinokio 路线 | 有用户反馈易用、稳定及 Windows 安装成功 | 手动安装官方不推荐初学者；不同版本有严重变慢、模糊和依赖反馈；精确合格案例包未锁 | 候选；不用付费安装器代替免费完整配方 |
| 全身动作、整个人物替换 | Wan2.2 Animate 原工作流；WanGP 界面候选 | 12GB/32GB 带工作流实作；他人采用该流程；WanGP 实际使用者反馈操作简单 | 精度/compile/手部/快速动作问题；不少分享修改节点或尺寸；本机未验证匹配配方 | 候选；按原作者支持分支补齐整包后再试 |
| 双人对白 | MultiTalk 的双人两路音频案例 | 使用者存在成功配置和具体耗时记录 | 同帖同时出现长耗时/OOM；成功多为低清、量化、LoRA 配置，未对应高质量双人原作 | 暂缓本机推理，继续锁一个同条件完整案例 |
| 连续视频换装 | CatV2TON | 作者发布视频推理与结果 | 本轮未取得足够独立“简单复做且成品优秀”的同配方反馈；研究脚本不等于简洁产品入口 | 资料候选；不启动新模型部署 |
| 可控剧情、古装双人镜头 | 具体作者完整工程；旧 H3 仅保留历史 | 旧 R4 有五秒内部验收记录 | 旧片依赖多次修补；尚未锁定满足这次要求的完整免费原作配方 | 不将旧修补路线收入简单能力 |
| 补帧、超分、导出 | 原配方已有 RIFE/FFmpeg；超分另选原案例 | RIFE 可携二进制和模型；已有本机局部使用；用户有满意结果反馈 | 有遮挡/切镜伪影；补帧不能纠正错误动作；高质量超分案例另配 | 支持节点，不能独立代表精品成片能力 |

视频翻译、配音、音效、自动字幕、降噪/分离、参考视频分析保留在旧 17 类报告。它们不是本轮新增完成的复现；本次未把 HeyGen/Synthesia 的付费业务案例当作免费配方。不得用“分类已覆盖”宣称每类已掌握。

## 重点案例与可执行边界

### A. LivePortrait：外部反馈较丰富，但只支持限定场景

- 原始方法、权重与人类模式入口见 [S01]；官方有独立 Windows 包 [S02]，无需购买第三方整合包。当前列出的 20240829 包约 5.27GB，下载和部署不应称为零成本。
- 两个独立创作者分别分享了 GTX1060 6GB 测试 [S03] 和 Viki 表情作品 [S04]，前者提供工作流和运行用时，后者有实际使用者的成功与抖动反馈。同帖多个简单赞美不当作多个完整复现报告。
- 后续实际使用者反馈跨场景对齐费事、表情编辑清晰度下降 [S05]。跨帖重复的同一段作者叙述只算一份。
- 官方对驱动视频要求清楚：头部为主、近正面中性起始、小肩部运动、合适裁切 [S01]。优先匹配这些条件，不选择大侧转、全身舞蹈或复杂遮挡验证这个窄能力。
- **本轮没有安装运行。** 原本已有 s6.jpg 与 d0.mp4，但旧材料对应的默认 GIF 太小，不能替代高清目标成品；应先取得同一案例的合格原输出和参数对应关系。缺这一配对是本轮的交接缺口，不是“网上不存在成熟方案”的结论。
- 后续只走作者原人类模式或具名原工作流，先原样例、再换一个原作者支持的人像。动物模式需额外依赖，单列，不由人类模式通过自动认证。

补充发现：[S40] 是独立操作者的 Windows 完整实践文章，包含默认 s6+d0 的实际日志、成品 MP4 链接、GUI 步骤和另一个输入实例；[S41] 为官方项目展示工程，能定位原始 MP4。当前已定位默认成品文件 https://wellstsai.com/post/live-portrait/demo.mp4 ，尚未下载检视其实际画质/规格、核对精确代码与权重版本；这是可继续补齐的具名入口，不能再笼统称“缺少公开成品”。

### B. FaceFusion：工具易用反馈存在，版本和模型必须锁定

- 免费源码和官方 Pinokio 工程可取 [S06–S07]；不购买官方收费安装器或不明第三方整合包。
- [S08] 有使用者认为操作简便、稳定的直接反馈，另有用户附和使用经验；但已删除的主帖不是可重放的完整作品来源。
- [S09] 记录不同版本同一配置的严重性能退化；[S10] 有低分辨率脸部结果和调参负担反馈。它们不是本机测量，也不证明所有版本都失败。
- **本轮没有运行。** 仍需一条可观看且质量合格的原短片，配齐输入脸、目标片、模型名/版本、遮罩/增强/编码参数和免费原步骤。不能仅凭“FaceFusion 好用”宣称换脸作品准入通过。

### C. Wan Animate / WanGP：有成品实绩，不能混合不同版本背书

- [S11] 是一个带具体工作流的 12GB/32GB 实作，提供分辨率/帧数和性能记录；同帖也记录禁用编译分支的成功反馈。保留作者文档中的支持分支，不自行发明优化链。
- [S12] 用户实际采用相关路线，但改变 GGUF 节点、降低规格，并反馈快速动作与手部限制。不能把其自述的运行成功频率外推到本机、原精度或高画质任务。
- [S13] 官方完整工作流可取；[S14] WanGP 官方提供 GUI 和旧显卡适配说明。RTX20 系列不能直接照搬 RTX30+ 的注意力加速配置。
- [S15–S16] 有独立使用者认为 WanGP 安装和操作方便；它们证明工具入口体验，不证明任意模型或我们指定的高清作品一次成功。
- [S17] 的更新反馈同时包含改善与后续 OOM 反例；不为追新升级正在正常工作的环境。
- **本轮没有新推理。** 本机已保存原工作流与输入的事实继续继承；仍需按同一成品锁定权重、预处理、参数和实际软件版本。选完再使用隔离任务环境，不改变健康共享 ComfyUI。

### D. MuseTalk / MultiTalk：运行成功和合格口型分开判定

- MuseTalk 原代码与输入、执行程序已保留 [S18]。外部低显存用户报告七秒音频完成 [S19]；该报告不提供足以计算总体成功率的样本集合。
- 本机旧 R1 已出 8 秒 200 帧文件，但观察到口部柔化；权重发布哈希和同案例高清原结果未完全配对。当前是已执行、质量未过、原因未完全定位，不能混称未做或模型必然不成熟。
- [S20] 的实际使用者提到侧转闪烁，不能把正面真人效果推广到动漫、侧脸或复杂双人。
- MultiTalk [S21] 有双人输入和代码。[S22–S23] 同时记录低显存可行配置、OOM、长耗时及不同效果。下一次先锁原作对应的两路对白配方，唱歌或单人样片不能代验双人轮流说话。

### E. 换装：已成功的静态原案例继承，视频另审

- FASHN 本机原案例两次无修补输出相同，原配方和文件见下节。它已证明这个案例可以简单重放，不能因本轮外部反馈证据不足抹掉真实成功。
- 开源版作者发布、配方和权重可取 [S24]；[S25] Reddit 发帖及“awesome”不是独立执行反馈。[S26] 是商业 API 评测，不能等同开源版的本机复现。
- [S27] CatV2TON 论文/官方推理脚本已发布，但本轮未取得足够对应的独立简单实践；保留候选，不把静态模型逐帧运行描述成已解决视频时序。
- 当前不重做已通过的 FASHN 红裙案例；下一步应补独立同版本实践和原作者支持的新素材迁移，不能拿默认例子反复成功代替泛化。

## 既有成果的本轮复核

这是旧成果继承与只读复核，没有新增渲染或模型生成。所有历史用时都是对应阶段用时，完整 T_VALID 仍未知。

| 案例 | 本轮直接查看/读取 | 继续有效的结论 | 尚未证明 |
|---|---|---|---|
| FASHN 红裙静态换装 | 最新 FASHN-Replay-Recipe、两次结果对账、本机 repeat-output-check；实际查看四栏原人物/衣服/官方/本机图 | 原程序两次输出字节与像素一致；576×823，原命令 07:20:334 / 05:11:605；无改算法、无修图、无挑种子 | 新人物/衣服、视频、总体成功率与完整 T_VALID |
| Remotion Audiogram | 完整 R2 记录、本机原 Root.tsx 和渲染记录；重新解码文件，查看 3.5/9/17/25 秒画面 | 原工程完整视频两次渲染；1080×1080，30fps，814帧，27.136秒；渲染 00:49:074 / 00:43:968 | 自动转录、新内容迁移、真人生成；这次未听审整条音轨 |
| SVD 官方山景 | 原生 history/workflow、14 帧质量账本、原作/本机对照；重新读媒体参数并查看关键帧 | 1024×576、14帧、10fps、1.4秒；单案例原样复现有证据，像素并非完全相同 | 重复运行、换图、提示词、人物表演或高清口播 |
| H3 R4 五秒尾镜 | 最新制作记录、R4 验收和本机 CURRENT | 五秒参考辅助成片通过内部验收记录继续保留 | 简洁原配方、新任务可直接迁移、整段成片；不代签用户审美批准 |

SVD 没有自然语言提示词入口，应按“换输入图/允许参数”检验迁移。FASHN 同理主要换人物图/衣服图。不能为满足“改提示词”字面要求而另造提示词层。

### 已有原配方和成果入口

- FASHN：[原配方及全部限定范围](https://chatgpt.com/library?file_id=libfile_fde3_f-667a43def9ac81919b5e3a0b4c23b7e4_937029f1505c8191917e0968911c47f5&account_id=personal)，[真实四栏对照](https://chatgpt.com/library?file_id=libfile_fde3_f-c42f5015b3ec8191be583aed8c541b80_937029f1505c8191917e0968911c47f5&account_id=personal)。本机 `C:/AI/Video-Recipe-Reproduction-20261108/FASHN-Official-R1/`。
- Remotion：[完整原工程视频](https://chatgpt.com/library?file_id=libfile_fde3_f-81f8401148bc819192732711c29ef45e_937029f1505c8191917e0968911c47f5&account_id=personal)。本机 `C:/AI/Video-Recipe-Reproduction-20261108/Mature-AV-R2/`，原程序 `npx remotion render`，沿用成功目录和锁定依赖，不重复安装。
- SVD：[原作/本机视频对照](https://chatgpt.com/library?file_id=libfile_982b9a1fe644819188dcd3f6756d7120&account_id=personal)，[原生证据包](https://chatgpt.com/library?file_id=libfile_301f1afa71f881919e8136388e837416&account_id=personal)。本机 `C:/AI/Video-Recipe-Reproduction-20261108/`；后续先核对服务和原任务，不覆盖 once.claim 或重发原编号。
- [此前 17 类完整记录](https://chatgpt.com/library?file_id=libfile_fde3_f-12d10efbb39c819190b0c36ca84565bd_937029f1505c8191917e0968911c47f5&account_id=personal)，当前 R4 结论覆盖下方历史表格；不要误读旧“FASHN 未执行”行。

## 来源账本

以下是本轮实际检索/打开的原始项目或操作者自述；网页抓取状态、只读证据和操作者自述分别记录。Reddit 部分网页直接打开不可用，下列实践内容来自搜索返回的正文；未声称逐段播放原视频或下载了每个作者工程。

| ID | 来源 | 类型与用途 |
|---|---|---|
| S01 | https://github.com/KlingAIResearch/LivePortrait | 作者原代码、输入规范与默认调用 |
| S02 | https://huggingface.co/cleardusk/LivePortrait-Windows | 官方免费 Windows 包；文件树核查当前包大小 |
| S03 | https://www.reddit.com/r/StableDiffusion/comments/1dzp864 | 独立创作者，GTX1060 测试及工作流；实际运行/抖动反馈 |
| S04 | https://www.reddit.com/r/StableDiffusion/comments/1dwhp0f/comfyui_liveportrait_viki/ | 独立创作者成品及正反操作反馈 |
| S05 | https://www.reddit.com/r/comfyui/comments/1kheaz4/is_liveportrait_still_actively_being_used/ | 使用者跨场景对齐与清晰度限制 |
| S06 | https://github.com/facefusion/facefusion | 官方源码与安装边界 |
| S07 | https://github.com/facefusion/facefusion-pinokio | 作者免费安装工程，未在本轮安装 |
| S08 | https://www.reddit.com/r/StableDiffusion/comments/1oykglu/removed/ | 主帖已删；剩余使用者易用反馈，只作辅助 |
| S09 | https://www.reddit.com/r/FaceFusion/comments/1wfalx6/severe_performance_regression_starting_with_380/ | 同一操作者按版本比较的性能反例 |
| S10 | https://www.reddit.com/r/StableDiffusion/comments/1kr9z1x | 低画质与调参负担反例 |
| S11 | https://www.reddit.com/r/comfyui/comments/1nnt6qz/wan_22_animate_workflow_for_low_vram_gpu_cards/ | 创作者完整工作流入口与实际硬件条件 |
| S12 | https://www.reddit.com/r/StableDiffusion/comments/1ottnjh/removed/ | 主帖已删；采用工作流的用户反馈及限制，不能算完整原作 |
| S13 | https://docs.comfy.org/tutorials/video/wan/wan2-2-animate | 官方原工作流与教程 |
| S14 | https://github.com/deepbeepmeep/WanGP | 原项目由 Wan2GP 重定向至 WanGP；GUI 与旧显卡分支 |
| S15 | https://www.reddit.com/r/StableDiffusion/comments/1qv8k1a/i_love_you_wangp/ | 独立使用者界面/操作体验 |
| S16 | https://www.reddit.com/r/StableDiffusion/comments/1qrv1r7/anyone_try_wan2gp_without_comfy/ | 多位使用者安装/运行边界；仅 UI 可见不当作生成成功 |
| S17 | https://www.reddit.com/r/StableDiffusion/comments/1wyujqe/wan2gp_has_been_updated_with_amazing_memory/ | 性能改善及后来 OOM/批量退化反馈 |
| S18 | https://github.com/TMElyralab/MuseTalk | 官方模型、配方与已知输入要求 |
| S19 | https://www.reddit.com/r/StableDiffusion/comments/1tf550j/best_lip_sync_model_for_low_vram/ | 低显存实际操作者短音频运行结果 |
| S20 | https://www.reddit.com/r/comfyui/comments/1x1ihf7/h3_character_swap_works_great_but_my_swapped_face/ | 实作侧脸闪烁反例 |
| S21 | https://github.com/MeiGen-AI/MultiTalk | 官方双人模型与输入 |
| S22 | https://www.reddit.com/r/StableDiffusion/comments/1m2jx8f | 多位操作者，成功设置与长耗时同时保留 |
| S23 | https://www.reddit.com/r/StableDiffusion/comments/1mpgfyb | 8GB 成功/OOM 反馈，内存和分辨率条件不同 |
| S24 | https://github.com/fashn-AI/fashn-vton-1.5 | 官方免费开源代码、参数与许可 |
| S25 | https://www.reddit.com/r/StableDiffusion/comments/1qq8dy7/fashn_vton_v15_efficient_maskless_virtual_tryon/ | 发布及讨论，不当作实际复现成功 |
| S26 | https://fal.ai/learn/tools/best-virtual-try-on-apis-2026 | 服务商实测 API，版本/部署不等同开源原配方 |
| S27 | https://github.com/Zheng-Chong/CatV2TON | 官方视频换装推理脚本与结果 |
| S28 | https://comfyanonymous.github.io/ComfyUI_examples/video/ | SVD 原作品、原工作流及输入入口 |
| S29 | https://www.reddit.com/r/StableDiffusion/comments/183bv6d | 2080 Ti SVD 成品；同帖其他操作者运行反馈；扩展配方需区别 |
| S30 | https://www.reddit.com/r/StableDiffusion/comments/1ahsspd | SVD 基础工作流易用反馈；不是完整质量验收 |
| S31 | https://github.com/remotion-dev/template-audiogram | 官方免费工程及参数入口 |
| S32 | https://www.remotion.dev/templates/audiogram | 官方预览和模板用途 |
| S33 | https://www.remotion.dev/docs/license/pricing | 本轮核查个人/至多三人公司免费使用条件；不是全部组织都免费 |
| S34 | https://www.reddit.com/r/ClaudeAI/comments/1qmur79/i_made_this_video_in_1_hour_using_claude_remotion/ | 实际 Remotion 成品，作者用了多次提示；不计一步完成 |
| S35 | https://www.reddit.com/r/OpenAI/comments/1xomuq2/i_used_chatgpt_with_remotion_to_create_a_10minute/ | 作者实绩与配方线索；承认局部粗糙，不当精品模板认证 |
| S36 | https://github.com/nihui/rife-ncnn-vulkan | 作者可携二进制、模型与用法 |
| S37 | https://www.reddit.com/r/StableDiffusion/comments/12otdo0 | 实际补帧用户满意反馈；不代表所有动作有效 |
| S38 | https://github.com/hzwer/Practical-RIFE/issues/34 | 操作者伪影反例及版本条件 |
| S39 | https://huggingface.co/cleardusk/LivePortrait-Windows/discussions/6 | 安装包长路径问题及维护者说明；不采用回帖推广的软件 |
| S40 | https://wellstsai.com/en/post/live-portrait/ | 独立操作者的原样例日志、成品 MP4 和 GUI 实践 |
| S41 | https://github.com/liveportrait/liveportrait.github.io | 官方原展示工程，可定位 MP4；不是本机运行证据 |

## 接续：只补真实缺项

1. 三项原案例不重做已通过部分；原重复和迁移分开记。SVD 若补重复，以新任务编号/新输出目录沿原配方执行；原生产任务先对账。
2. 下一项优先 LivePortrait 的近正脸小动作：补齐合格高清原成品与完全对应配方、核查同条件实践，再做原样例与一次相近素材迁移。已有低清 GIF 不够认证高清能力。
3. 换脸/整人替换继续在已找到的作者整包中配对原作，不靠新加节点、反复调参或重抽来让路线过关。未执行保持未执行，不能写 FAIL。
4. 每个实际样片保存入口、输入、版本、原命令/工作流、运行日志、原生任务标识、成品与正常速度声画审核；实际下载或输入不公开的案例退回候选。
5. 简洁配方里允许原作者已有的剪辑合成，全部成本计入完整 T_VALID。跨页起点缺失继续填未知；不以采样、渲染、进程退出或 HTTP200 代替交付验收。

NEXT_PAGE_PROMPT：接续 V3.2 外部反馈审核与既有三项原案例；先读本文件和 CASE-STATUS-20261109.json。保留 FASHN/Remotion 固定原案例的重复通过，SVD 仅单案例复现，H3 修补成果不作简单准入。优先补 LivePortrait 高清同案例成品与配方对应，不重开全网名单，不购买整合包，不把尚未执行的路线写失败；选定后原样复刻、独立审片、复跑、再验相近素材迁移。
