# 数字人原作重选：品质在先，旧片拒收

日期：2026-11-09，北京时间。

## 本轮决定

用户已明确拒收 `avatar-promo.mp4`：人物选择不合要求，文案空泛，表现死板、缺少动态和艺术感，并指出口型不对；要求停止该片的验证和修改。

原人物确实来自公开的 D24 测试案例；三张介绍卡片是本轮自制的排版，不是公开精品原作。错误在于把“资料完整、程序已有、能运行”放在了人物和成片品质之前。两次生成、解码和相似度记录保留为运行事实，不计合格能力；该片不再进入口型复测、修补或宣传默认路线。

现行顺序只保留三件事：先找符合宣传目的、有品质的实际成片；再核对原制作方法、可用素材和实际使用者反馈；条件齐后按已有配方复刻。品质不合格就换原作，不修坏片。省成本的前提是品质合格。

## 已取到的原作参考

以下视频均为外部原作者输出，不是本机新生成。预览只截取开头八秒并适当缩小尺寸，保留原水印，不改动作速度。它们用于选人物和动态水准，不能将表演/歌唱样片自动登记为宣传口播交付。

| 参考 | 已观察的画面 | 来源与方法资料 | 当前资格 |
|---|---|---|---|
| A：录音棚女声 | 暖色灯光、有空间层次和专业录音环境，人物表情、头肩随表演变化 | [原项目与成片库](https://github.com/MeiGen-AI/InfiniteTalk)；[该条原视频](https://github.com/user-attachments/assets/3263c5e1-9f98-4b9b-8688-b3e497460a76)；[配套录音棚人像](https://github.com/MeiGen-AI/InfiniteTalk/blob/main/examples/single/ref_image.png)；[原生配置入口](https://github.com/MeiGen-AI/InfiniteTalk/blob/main/examples/single_example_image.json) | 优先的形象与表现候选；原图和通用配方已定位，本机未复刻，原片逐案例参数尚未完全配对 |
| B：蓝裙人物 | 明确的人物造型、礼服材质、柔和用光，原视频为静图/生成结果并列，可看头部、表情和姿态变化 | [Wan-S2V 作者成片页](https://humanaigc.github.io/wan-s2v-webpage/)；[该条原视频](https://humanaigc.github.io/wan-s2v-webpage/content/v3/video/banquan/22.mp4)；[官方免费原生工作流说明](https://docs.comfy.org/tutorials/video/wan/wan2-2-s2v) | 人物美感与动态参考；没有将该条原图、原声及精确配置配齐，不作为立即执行的整包 |
| C：白板功能介绍 | 人物位于真实场景中，用手势和头部变化配合白板上的产品功能信息 | [InfiniteTalk 原作](https://meigen-ai.github.io/InfiniteTalk/videos/i2v/0.mp4)；[项目成片页](https://meigen-ai.github.io/InfiniteTalk/) | 比空泛三卡片更接近功能讲解目的；原作可看，具体素材配对和艺术选型仍待审核 |

A 使用的通用项目代码当前提交为 `50aa0a94184315407a991ae804d9b58d6d311ba8`。仓库提供原图、音频、单人配置及低显存/量化分支，但不能据此把其所有发布视频称为同一个固定输入包：本轮核对发现，仓库的 `examples/single/1.wav` 约10.68秒，而 A 发布输出约40秒，音轨不是同一份。该差异已经记录，不能隐去后宣称原声原配置完整一致。原作音轨可以提取作方法复用输入，但应标明来自成片，不能冒称作者原始 WAV。

## 实作反馈与配方核查

- [Pixaroma 的 InfiniteTalk 实作教程](https://www.youtube.com/watch?v=JN6CFU02Rms) 与 [新版视频模型教程](https://www.youtube.com/watch?v=Z8JlJdXdVg4) 属于同一发布者。其 [免费工作流站](https://workflows.pixaroma.com/) 的当前 Ep06 包已实际下载，包含17个流程，其中有单人短段与延长等 InfiniteTalk 分支。包内没有 Media Inputs，引用的 `WanWoman.png` 等图像不在包内；不把“JSON到手”当具体原作素材已齐。
- [UkieTechie 的实际比较](https://www.reddit.com/r/StableDiffusion/comments/1n97g93/is_there_an_advantage_of_using_wan_22_with/) 报告用 Kijai 的 Wan2.1 InfiniteTalk 原示例获得较好的表情和口型；尝试混用 Wan2.2 分支未成功。采用原配套分支，不自行换底座。
- [另一位作者的同输入比较](https://note.com/ultracrab/n/n3dfe8759578d) 使用原工作流比较 S2V、InfiniteTalk I2V 和已有视频再配音，口播倾向 InfiniteTalk。此测试为动漫风格，不能直接扩大成当前写真人物或本机质量认证。
- [Wan-S2V 原生教程](https://docs.comfy.org/tutorials/video/wan/wan2-2-s2v) 已明确说明，通用四步 Lightning LoRA 会损失动态和质量，原始二十步是另一条既有分支。不能为省时默认使用低动态分支后再补救。
- 新发现的 LongCat Avatar 1.5 演示有电影式场景，但 [公开的12GB尝试](https://www.reddit.com/r/comfyui/comments/1ufx4p5/longcat_avatar_15_workflow_with_the_correct_nodes/) 实际输出为黑屏，不能把搜索摘要中的“15分钟跑完”算成功。较大显存的测试也不能自动套到本机。它暂作画面参考，不作本轮低成本主线。

以上是不同作者/整合者的条件性实践信息，没有代表性成功率分母。教程数量不等于合格作品数量。

## 真正面向宣传的成熟展示流程

[HeyGen 官方产品出镜教程](https://www.heygen.com/academy/more-about-avatars/how-to-add-products-to-your-avatar) 提供了“人物＋产品图→挑选组合图→文案和配音→人物动作→导出”的现成操作路径，并有多场景版本。它比单纯的模型对口型测试更接近用户所说的宣传目的。

这里把它登记为用途和展示方法候选；公开教程免费不等于生成免费，该流程可能消耗平台额度。本轮没有购买、注册、登录或调用付费生成，也没有冒充已在该平台出片。后续比较时须区分“免费资料”和“实际生成成本”。

宣传文案要讲具体对象、可见成果或用户收益。缺少具体产品时，先选择具名且可展示的内容，不再使用“这是一个数字人演示、准备文案就能制作”这类空泛自我说明替代宣传文案。

## 保留与接续

- 本轮只有原作检索、下载、画面筛选、资料配对和片段预览，没有运行新数字人模型。
- 当前没有把 A/B/C 任一条认证为“本机已经具备、任意换文案都稳定成功”的成熟能力。
- 用户此前提供的剧情原片及其他路线原位保留。
- D24旧片归档为 `USER_REJECTED_QUALITY`；技术日志保留，后续不复测、不修补，也不再推荐。

NEXT_PAGE_PROMPT：先读本记录及用户拒收结论，禁止回到D24旧片口型验证或卡片修改。优先审核高品质且符合宣传目的的原作，核对原图/音轨/原工作流及独立实际反馈。A录音棚原作是形象表现候选，B蓝裙是美感参考，C白板是功能讲解参考；它们都不是本机新增认证。准确区分通用配方和某条原作的完整输入包，不能隐藏A原片音轨与仓库例声音频不一致的问题，不把缺素材的流程称为整包。未齐就继续找同类完整成熟案例。


官网部分样例注明仅作学术展示，当前只作为选片参考；后续实际宣传使用自有或有适用授权的人像与音轨。
